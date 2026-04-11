import pdfplumber
import re
import os
from openai import OpenAI
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from ..models import *
from django.conf import settings
from django.db import transaction
from urllib.parse import urljoin
from users.models import EstudianteUser


class UpdateModuloTxtContentView(APIView):
    def put(self, request, pk):
        try:
            # Obtener el módulo
            modulo = Modulo.objects.get(pk=pk)

            # Obtener el contenido enviado en la solicitud
            content = request.data.get("content", "")

            if not content:
                return Response({"detail": "El contenido no puede estar vacío."}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que el archivo existe
            if not modulo.modsrctxt or not modulo.modsrctxt.path:
                return Response({"detail": "El archivo .txt del módulo no existe."}, status=status.HTTP_404_NOT_FOUND)

            # Guardar el nuevo contenido en el archivo
            try:
                with open(modulo.modsrctxt.path, "w", encoding="utf-8") as file:
                    file.write(content)
            except IOError as e:
                return Response({"detail": f"No se pudo escribir en el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Contenido actualizado exitosamente."}, status=status.HTTP_200_OK)
        except Modulo.DoesNotExist:
            return Response({"detail": "Módulo no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GenerarExamenView(APIView):
    def post(self, request):
        try:
            # Validación inicial de la solicitud
            course_id = request.data.get('courseId')
            modules = request.data.get('modules', [])
            if not course_id or not modules:
                return Response(
                    {"detail": "Faltan 'courseId' o 'modules' en la solicitud."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Obtener curso
            curso = self.get_course(course_id)

            # Crear o actualizar el examen
            examen = self.create_or_update_exam(curso, modules)

            # Generar preguntas para cada módulo
            with transaction.atomic():
                preguntas_generadas = self.process_modules_and_generate_questions(modules, examen)                
        
            return Response(
                {"detail": f"Examen generado exitosamente con {preguntas_generadas} preguntas."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"detail": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

    def get_course(self, course_id):
        """Obtiene el curso o lanza un error si no existe."""
        try:
            return Curso.objects.get(curcod=course_id)
        except Curso.DoesNotExist:
            raise ValueError("El curso no existe.")
    

    def create_or_update_exam(self, curso, modules):
        """Crea o actualiza un examen para el curso."""
        try:
            num_questions = sum(int(module["questions"]) for module in modules)
            examen, _ = Examen.objects.get_or_create(
                exacurcod=curso,
                defaults={
                    "exanumpre": num_questions,
                    "exaestregcod": EstadoRegistro.objects.get(pk=1)  # Ejemplo de estado activo
                }
            )
            return examen
        except Exception as e:
            raise ValueError(f"Error al crear o actualizar el examen: {str(e)}")

    
    def process_modules_and_generate_questions(self, modules, examen):
        """Procesa cada módulo y genera preguntas."""
        total_preguntas = 0
        for module_data in modules:
            module_id = module_data.get("name")
            num_questions = int(module_data.get("questions", 0))
            # Validar módulo y número de preguntas
            if not module_id or not num_questions:
                raise ValueError(f"Datos faltantes para el módulo: {module_data}")
            # Obtener módulo y leer contenido
            modulo = self.get_module(module_id)
            content = self.get_module_content(modulo)
            # Generar preguntas usando la API
            questions_data = self.generate_questions(content, num_questions)
            # Guardar preguntas y alternativas
            total_preguntas += self.save_questions_and_alternatives(questions_data, modulo, examen)
        return total_preguntas
    

    def get_module(self, module_id):
        """Obtiene el módulo o lanza un error si no existe."""
        try:
            return Modulo.objects.get(modcod=module_id)
        except Modulo.DoesNotExist:
            raise ValueError(f"El módulo con ID {module_id} no existe.")
    

    def get_module_content(self, modulo):
        """Lee el contenido del archivo del módulo o lanza un error."""
        if not modulo.modsrctxt or not os.path.isfile(modulo.modsrctxt.path):
            raise ValueError(f"El archivo de texto del módulo '{modulo.modcod}' no existe.")
        try:
            with open(modulo.modsrctxt.path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError as e:
            raise ValueError(f"No se pudo leer el archivo del módulo '{modulo.modcod}': {str(e)}")
    
    
    def generate_questions(self, content, num_questions):
        print("num_questions")
        print(num_questions)
        """Genera múltiples preguntas y alternativas usando la API de OpenAI en una sola solicitud"""
        client = OpenAI(
            api_key=os.getenv('OPENAI_KEY', ''),
            project="proj_PEpuhEugHb1JX5coceQkSmCV"
        )  # Asegúrate de configurar tu clave de API

        # Crear los mensajes en el formato correcto
        messages = [
            {"role": "system", "content": "Eres un generador de preguntas tipo examen de opción múltiple en idioma español."},
            {"role": "user", "content": (
                f"Basado en el siguiente contenido:\n{content}\n"
                f"Genera exactamente {num_questions} pregunta(s) de opción múltiple en formato JSON, por favor no enumeres ni les pongas letras a las alternativas y preguntas, "
                "cada pregunta debe tener exactamente 4 alternativas (solo una es correcta) y "
                "aparte de la pregunta debe haber una explicación de la respuesta correcta."
                "El formato json debe incluir: 'question', 'alternatives' (donde cada alternativa tiene 'text'(texto de la alternativa) y 'is_correct' (true o falso por cada alternativa)) y 'explanation'."
            )}
        ]
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=2000,  # Ajusta según sea necesario
                temperature=0.5
            )
            # Verifica que la respuesta tenga contenido
            if not response.choices or not response.choices[0].message.content.strip():
                raise ValueError("La API no devolvió contenido. Verifica los límites de tokens o el contenido enviado.")

            response_text = response.choices[0].message.content
            content = response_text.replace('```json\n', '').replace('\n```', '').strip()
            # Intenta cargar la respuesta como JSON
            questions_data = json.loads(content)
            print(questions_data)

            # Normalizar el JSON: si es un diccionario, convertirlo en una lista
            if isinstance(questions_data, dict):
                questions_data = [questions_data]

            # Verificar que sea una lista
            if not isinstance(questions_data, list):
                raise ValueError("La API no devolvió una lista válida de preguntas.")

            return questions_data

        except json.JSONDecodeError as e:
            # Registra el contenido de la respuesta para verificar el problema
            print("Error en JSON. Respuesta de la API:", response_text)
            raise ValueError(f"Error al interpretar los datos de la API. Verifica el formato JSON devuelto: {str(e)}")
        except Exception as e:
            # Registrar otros errores
            print("Error inesperado en la respuesta de la API:", str(e))
            raise ValueError(f"Error inesperado al procesar la respuesta de la API: {str(e)}")
    

    def save_questions_and_alternatives(self, questions_data, modulo, examen):
        """Guarda preguntas y sus alternativas en la base de datos."""
        total = 0
        for index, question_data in enumerate(questions_data, start=1): #for question_data in questions_data:
            # Combina examen + índice de 2 dígitos, todo como entero
            pregunta_cod_personalizado = int(f"{examen.exacurcod.curcod}{index:02}")  # ejemplo: examen=12 → 1201, 1202...            
            pregunta = Pregunta.objects.create(
                precod=pregunta_cod_personalizado,
                pretex=question_data["question"],
                preexp=question_data["explanation"],
                prenummod=modulo.modcod,
                preexacod=examen,
                preestregcod=EstadoRegistro.objects.get(pk=1)
            )

            # Agrega un contador para las alternativas
            for alt_index, alternative in enumerate(question_data["alternatives"], start=1):
                # Código único para cada alternativa basado en la pregunta + número de alternativa
                alternativa_cod_personalizado = int(f"{pregunta.precod}{alt_index:02}")  # Ej: 120101, 120102, 120201, etc.
                Alternativa.objects.create(
                    altcod=alternativa_cod_personalizado,
                    alttex=alternative["text"],
                    altcor=alternative["is_correct"],
                    altprecod=pregunta,
                    altestregcod=EstadoRegistro.objects.get(pk=1)
                )
            total += 1
        return total



class ModuloTxtContentView(APIView):
    def get(self, request, curso_id):
        # Obtener los módulos asociados al curso
        modulos = Modulo.objects.filter(modcurcod=curso_id)
        contenido_txt = []

        # Leer el contenido de cada archivo .txt en el campo modsrctxt de cada módulo
        for modulo in modulos:
            if modulo.modsrctxt:
                try:
                    with open(modulo.modsrctxt.path, 'r', encoding='utf-8') as file:
                        contenido_txt.append({
                            "modcod": modulo.modcod,
                            "modnom": modulo.modnom,
                            "content": file.read()
                        })
                except UnicodeDecodeError:
                    # Intentar leer con codificación alternativa si UTF-8 falla
                    try:
                        with open(modulo.modsrctxt.path, 'r', encoding='latin-1') as file:
                            contenido_txt.append({
                                "modcod": modulo.modcod,
                                "modnom": modulo.modnom,
                                "content": file.read()
                            })
                    except Exception as e:
                        print(f"Error al leer el archivo {modulo.modsrctxt.path} con codificación alternativa: {e}")
                        contenido_txt.append({
                            "modcod": modulo.modcod,
                            "modnom": modulo.modnom,
                            "content": "Error al leer el contenido del archivo."
                        })
                except Exception as e:
                    # Registrar cualquier otro error y pasar un mensaje de error en el contenido
                    print(f"Error al leer el archivo {modulo.modsrctxt.path}: {e}")
                    contenido_txt.append({
                        "modcod": modulo.modcod,
                        "modnom": modulo.modnom,
                        "content": "Error al leer el contenido del archivo."
                    })
            else:
                contenido_txt.append({
                    "modcod": modulo.modcod,
                    "modnom": modulo.modnom,
                    "content": "Archivo no encontrado."
                })

        # Devolver el contenido de todos los archivos .txt asociados al curso
        return Response(contenido_txt, status=status.HTTP_200_OK)



class ProcessPdfView(APIView):

    def post(self, request, curso_id):
        start_page = request.data.get('startPage')
        end_page = request.data.get('endPage')

        # Convertir a enteros
        try:
            start_page = int(start_page)
            end_page = int(end_page)
        except (ValueError, TypeError):
            return Response({'error': 'startPage y endPage deben ser números enteros'}, status=400)

        # Obtener el curso y la ruta del PDF
        try:
            curso = Curso.objects.get(curcod=curso_id)
            pdf_path = curso.cursrcpdf.path
        except Curso.DoesNotExist:
            return Response({'error': 'Curso no encontrado'}, status=404)

        # Verificar si existe el archivo PDF
        if not pdf_path:
            return Response({'error': 'PDF no encontrado'}, status=404)

        # Extraer el texto y guardarlo en un archivo .txt
        archivo_txt_path, archivo_txt_url = self.extraer_texto(pdf_path, curso_id, start_page, end_page)

        if not archivo_txt_path:
            return Response({'error': 'No se pudo extraer texto del PDF'}, status=400)

        # Limpiar encabezados y pies de página
        texto_limpio = self.clean_header_footer(archivo_txt_path)
        #texto_limpio = self.remove_header_footer_using_ai(texto_extraido, nlp)

        # Eliminar saltos de línea entre oraciones
        texto_final = self.eliminar_saltos_linea(texto_limpio)

        # Guardar el texto limpio en un nuevo archivo .txt (opcional)
        cleaned_txt_path = os.path.join(settings.MEDIA_ROOT, 'curso_txt', f'curso_{curso_id}_{start_page}-{end_page}_cleaned.txt')
        with open(cleaned_txt_path, 'w', encoding='utf-8') as clean_file:
            clean_file.write(texto_final)
        
        # Separar en módulos y guardar en archivos
        modulos_guardados = self.separar_en_modulos(texto_final, curso)
        
        return Response({'archivo_txt': cleaned_txt_path}, status=200)


    def extraer_texto(self, pdf_path, curso_id, inicio_pagina, fin_pagina):
        # Verificación básica del archivo PDF
        if not os.path.isfile(pdf_path):
            return None, None
        
        try:
            # Abrir el archivo PDF
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                if inicio_pagina < 1 or fin_pagina > num_pages:
                    return None, "El rango de páginas especificado está fuera de los límites del PDF."
                
                texto_total = ""

                # Verificar que el rango de páginas sea válido
                for i in range(inicio_pagina-1, fin_pagina):
                    pagina = pdf.pages[i]
                    texto = pagina.extract_text()
                    texto_total += f"\n--- Página {i+1} ---\n{texto if texto else 'No se encontró texto en esta página.'}"

                # Crear la ruta donde se almacenará el archivo .txt
                txt_directory = os.path.join(settings.MEDIA_ROOT, 'curso_txt')
                os.makedirs(txt_directory, exist_ok=True)  # Crea la carpeta si no existe
                txt_file_path = os.path.join(txt_directory, f'curso_{curso_id}_{inicio_pagina}-{fin_pagina}.txt')

                # Guardar el contenido en el archivo .txt
                with open(txt_file_path, 'w', encoding='utf-8') as f:
                    f.write(texto_total)
                
                # Construir la URL pública (correcta) del archivo accesible
                archivo_txt_url = urljoin(settings.MEDIA_URL, f'curso_txt/curso_{inicio_pagina}_{fin_pagina}.txt')
                
                # Devolver la ruta del sistema de archivos y la URL pública
                return txt_file_path, archivo_txt_url

        except FileNotFoundError:
            return None

    
    def clean_header_footer(self, archivo_txt_path, header_footer_lines=3, min_line_length=10):
        """
        Lee un archivo .txt desde su ruta, elimina encabezados y pies de página, y guarda el texto limpio en un nuevo archivo.
        Args:
            archivo_txt_path (str): Ruta del archivo .txt a limpiar.
            header_footer_lines (int): Número máximo de líneas a analizar como encabezado o pie.
            min_line_length (int): Longitud mínima de una línea para considerarla válida.
        Returns:
            str: Ruta del archivo .txt limpio.
        """
        # Leer el contenido del archivo desde la ruta
        try:
            with open(archivo_txt_path, 'r', encoding='utf-8') as file:
                texto_extraido = file.read()
        except Exception as e:
            raise ValueError(f"No se pudo leer el archivo desde la ruta: {e}")

        # Procesar el texto para limpiar encabezados y pies
        page_delimiter_pattern = r'\n--- Página \d+ ---\n'
        text_pages = re.split(page_delimiter_pattern, texto_extraido)
        clean_pages = []

        for page_text in text_pages:
            if not page_text.strip():
                continue

            lines = page_text.split("\n")
            header_candidates = lines[:header_footer_lines]
            footer_candidates = lines[-header_footer_lines:]

            valid_header_lines = [
                line for line in header_candidates
                if len(line.strip()) >= min_line_length
                and not re.match(r'^(Página|Page|\d+)', line, re.IGNORECASE)
            ]

            valid_footer_lines = [
                line for line in footer_candidates
                if len(line.strip()) >= min_line_length
                and not re.match(r'^(Página|Page|\d+|Copyright)', line, re.IGNORECASE)
            ]

            clean_lines = [
                line for line in lines
                if line not in header_candidates or line in valid_header_lines
                if line not in footer_candidates or line in valid_footer_lines
            ]

            clean_pages.append("\n".join(clean_lines))

        clean_text = "\n".join(clean_pages)
        
        return clean_text


    def eliminar_saltos_linea(self, texto):
        patron = r"([a-z])\n([a-z])"
        texto_limpio = re.sub(patron, r"\1 \2", texto)
        return texto_limpio


    def separar_en_modulos(self, texto_final, curso):
        """
        Divide el texto en módulos basándose en encabezados y guarda cada módulo como un archivo .txt.
        Args:
            texto_final (str): Texto procesado y limpio.
            curso (Curso): Objeto del curso para obtener los módulos.
        Returns:
            list: Lista de módulos guardados con sus rutas.
        """
        # Obtener los módulos que pertenecen al curso desde la base de datos
        modulos = Modulo.objects.filter(modcurcod=curso).order_by('modcod')

        if not modulos.exists():
            return {'error': 'No se encontraron módulos asociados a este curso.'}

        # Crear el patrón para identificar módulos basado en "Module X"
        patron_modulo = r"Module\s+(\d+)\s*[-–:]"

        # Dividir el texto en fragmentos usando el patrón de módulos
        modulos_encontrados = re.split(f"({patron_modulo})", texto_final)

        # Verificación de que se encontraron fragmentos válidos
        if len(modulos_encontrados) < 3:
            return {'error': 'No se encontraron fragmentos de texto para los módulos en el archivo.'}

        # Directorio donde se guardarán los archivos txt de los módulos
        modulos_directory = os.path.join(settings.MEDIA_URL, 'modulos_txt')
        os.makedirs(modulos_directory, exist_ok=True)

        modulos_guardados = []

        # Recorrer los fragmentos de texto para identificar y guardar módulos
        for i in range(1, len(modulos_encontrados) - 1, 3):
            encabezado_modulo = modulos_encontrados[i].strip()
            numero_modulo = modulos_encontrados[i + 1].strip()
            contenido_modulo = modulos_encontrados[i + 2].strip()

            # Comparar el número del módulo en el texto con los últimos dos dígitos del ID del módulo
            modulo_obj = next(
                (mod for mod in modulos if str(mod.modcod)[-2:] == numero_modulo.zfill(2)),
                None
            )

            if modulo_obj:
                # Nombre del archivo
                archivo_nombre = f'curso-{curso.curcod}_{modulo_obj.modcod}-{modulo_obj.modnom}.txt'
                ruta_relativa = os.path.join('modulos_txt', archivo_nombre)
                ruta_absoluta = os.path.join(settings.MEDIA_ROOT, ruta_relativa)
                with open(ruta_absoluta, 'w', encoding='utf-8') as f:
                    f.write(f"{encabezado_modulo}\n{contenido_modulo}")
                
                # Guardar la ruta relativa en la base de datos
                modulo_obj.modsrctxt = ruta_relativa  
                modulo_obj.save()

                modulos_guardados.append({
                    'modulo': encabezado_modulo,
                    'archivo': ruta_relativa
                })

        return modulos_guardados


    def remove_header_footer_using_ai(self, text, model, header_footer_length_threshold=50):
        # Patrón para identificar delimitadores de página
        page_delimiter_pattern = r'\n--- Página \d+ ---\n'
        text_pages = re.split(page_delimiter_pattern, text)
        clean_pages = []

        for page_text in text_pages:
            if page_text.strip():
                # Procesar la página con NLP y dividirla en líneas
                doc = model(page_text)
                lines = page_text.split("\n")

                # Identificar candidatos a encabezados y pies de página
                header_candidates = lines[:3]  # Analizar primeras 3 líneas como encabezado
                footer_candidates = lines[-3:]  # Analizar últimas 3 líneas como pie de página

                # Condiciones para identificar encabezados
                valid_headers = [
                    line for line in header_candidates
                    if len(line.strip()) < header_footer_length_threshold
                    and ("Página" in line or "Page" in line or bool(re.search(r'\d', line)))
                ]

                # Condiciones para identificar pies de página
                valid_footers = [
                    line for line in footer_candidates
                    if len(line.strip()) < header_footer_length_threshold
                    and ("Página" in line or "Page" in line or bool(re.search(r'\d', line)))
                ]

                # Retener únicamente líneas que no sean identificadas como encabezados o pies de página
                clean_text = "\n".join(
                    line for i, line in enumerate(lines)
                    if line not in valid_headers and line not in valid_footers
                )
                
                clean_pages.append(clean_text)

        # Combinar las páginas limpiadas sin reinsertar los delimitadores de página
        clean_text_final = "\n".join(clean_pages)
        return clean_text_final



# Guarda el pdf
class GetPdfPagesView(APIView):
    def get(self, request, curso_id):
        try:
            # Obtener el curso correspondiente
            curso = Curso.objects.get(curcod=curso_id)

            # Verificar si hay un archivo PDF asignado y si el archivo existe
            if curso.cursrcpdf and os.path.isfile(curso.cursrcpdf.path):
                pdf_path = curso.cursrcpdf.path
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        num_pages = len(pdf.pages)
                        return Response({'total_pages': num_pages}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'error': f"Error al procesar el PDF: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'error': 'No PDF file found for this course.'}, status=status.HTTP_404_NOT_FOUND)

        except Curso.DoesNotExist:
            return Response({'error': 'Curso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)



class GuardarRespuestasExamenProgramaAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        respuestas_data = request.data.get('respuestas', [])  # Lista de respuestas
        examen_id = request.data.get('examenId')
        programa_id = request.data.get('programaId')
        estudiante_id = request.user.id  # Asumimos que el usuario está autenticado
        
        # Validación de datos recibidos
        if not respuestas_data:
            return Response({"detail": "No se han proporcionado respuestas."}, status=status.HTTP_400_BAD_REQUEST)
        if not examen_id:
            return Response({"detail": "El ID del examen es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        if not programa_id:
            return Response({"detail": "El ID del programa es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            examen = Examen.objects.get(pk=examen_id)
        except Examen.DoesNotExist:
            return Response({"detail": "El examen no existe."}, status=status.HTTP_404_NOT_FOUND)

        try:
            programa = Programa.objects.get(pk=programa_id)
        except Programa.DoesNotExist:
            return Response({"detail": "El programa no existe."}, status=status.HTTP_404_NOT_FOUND)

        try:
            estudiante = EstudianteUser.objects.get(pk=estudiante_id)
        except EstudianteUser.DoesNotExist:
            return Response({"detail": "El estudiante no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el número total de preguntas en el examen
        total_preguntas = Pregunta.objects.filter(preexacod=examen).count()
        
        # Calcular la puntuación por cada respuesta correcta
        puntuacion_por_respuesta_correcta = 20.00 / total_preguntas if total_preguntas > 0 else 0.0
        
        puntuacion_total = 0.0
        
        for pregunta_id, alternativa_id in respuestas_data.items():
            try:
                pregunta = Pregunta.objects.get(pk=pregunta_id)
            except Pregunta.DoesNotExist:
                return Response({"detail": f"La pregunta con ID {pregunta_id} no existe."}, status=status.HTTP_404_NOT_FOUND)

            try:
                alternativa = Alternativa.objects.get(pk=alternativa_id)
            except Alternativa.DoesNotExist:
                return Response({"detail": f"La alternativa con ID {alternativa_id} no existe."}, status=status.HTTP_404_NOT_FOUND)
            
            # Calcular la puntuación según la lógica del negocio
            puntuacion = puntuacion_por_respuesta_correcta if alternativa.altcor else 0.0
            puntuacion_total += puntuacion
            
            # Verificar si ya existe un registro de respuesta para esta pregunta
            respuesta_existente = RespuestaExamenPrograma.objects.filter(
                resproestcod=estudiante,
                resproexacod=examen,
                resproprecod=pregunta,
                resproprocod=programa,
            ).first()

            if respuesta_existente:
                # Actualizar la respuesta existente
                respuesta_existente.resproaltcod = alternativa
                respuesta_existente.respropun = puntuacion
                respuesta_existente.save()
            else:
                # Crear una nueva respuesta si no existe
                nueva_respuesta = RespuestaExamenPrograma(
                    respropun=puntuacion,
                    resproestcod=estudiante,
                    resproexacod=examen,
                    resproprecod=pregunta,
                    resproaltcod=alternativa,
                    resproprocod=programa,
                )
                nueva_respuesta.save()
        
        # Obtener el registro del examen para el estudiante y el curso
        registro_examen, created = RegistroExamenPrograma.objects.get_or_create(
            regexaproestcod=estudiante,
            regexaproexacod=examen,
            regexaproprocod=programa,
        )
        
        # Actualizar la puntuación total y el número de intentos
        registro_examen.regexapropun = puntuacion_total
        registro_examen.regexaproint += 1
        
        # Actualizar el estado del examen según la puntuación obtenida
        estado_aprobado = EstadoExamen.objects.get(estexanom="Aprobado")
        estado_desaprobado = EstadoExamen.objects.get(estexanom="Reprobado")
        if puntuacion_total >= 14:
            registro_examen.regexaproestexacod = estado_aprobado
        else:
            registro_examen.regexaproestexacod = estado_desaprobado

        registro_examen.save()
        
        # Calcular el promedio de todas las puntuaciones de exámenes del estudiante en el programa
        registros_examen = RegistroExamenPrograma.objects.filter(
            regexaproestcod=estudiante,
            regexaproprocod=programa
        )
        promedio_puntuacion = registros_examen.aggregate(promedio=Avg('regexapropun'))['promedio']
        
        return Response({"message": "Respuestas guardadas o actualizadas con éxito."}, status=status.HTTP_200_OK)


class GuardarRespuestasExamenCursoAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        respuestas_data = request.data.get('respuestas', [])  # Lista de respuestas
        examen_id = request.data.get('examenId')
        estudiante_id = request.user.id  # Asumimos que el usuario está autenticado
        
        # Validación de datos recibidos
        if not respuestas_data:
            return Response({"detail": "No se han proporcionado respuestas."}, status=status.HTTP_400_BAD_REQUEST)
        if not examen_id:
            return Response({"detail": "El ID del examen es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            examen = Examen.objects.get(pk=examen_id)
        except Examen.DoesNotExist:
            return Response({"detail": "El examen no existe."}, status=status.HTTP_404_NOT_FOUND)

        try:
            curso = Curso.objects.get(pk=examen_id)
        except Curso.DoesNotExist:
            return Response({"detail": "El curso no existe."}, status=status.HTTP_404_NOT_FOUND)

        try:
            estudiante = EstudianteUser.objects.get(pk=estudiante_id)
        except EstudianteUser.DoesNotExist:
            return Response({"detail": "El estudiante no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el número total de preguntas en el examen
        total_preguntas = Pregunta.objects.filter(preexacod=examen).count()
        
        # Calcular la puntuación por cada respuesta correcta
        puntuacion_por_respuesta_correcta = 20.00 / total_preguntas if total_preguntas > 0 else 0.0
        
        puntuacion_total = 0.0
        
        for pregunta_id, alternativa_id in respuestas_data.items():
            try:
                pregunta = Pregunta.objects.get(pk=pregunta_id)
            except Pregunta.DoesNotExist:
                return Response({"detail": f"La pregunta con ID {pregunta_id} no existe."}, status=status.HTTP_404_NOT_FOUND)

            try:
                alternativa = Alternativa.objects.get(pk=alternativa_id)
            except Alternativa.DoesNotExist:
                return Response({"detail": f"La alternativa con ID {alternativa_id} no existe."}, status=status.HTTP_404_NOT_FOUND)
            
            # Calcular la puntuación según la lógica del negocio
            puntuacion = puntuacion_por_respuesta_correcta if alternativa.altcor else 0.0
            puntuacion_total += puntuacion
            
            # Verificar si ya existe un registro de respuesta para esta pregunta
            respuesta_existente = RespuestaExamenCurso.objects.filter(
                rescurestcod=estudiante,
                rescurexacod=examen,
                rescurprecod=pregunta,
            ).first()

            if respuesta_existente:
                # Actualizar la respuesta existente
                respuesta_existente.rescuraltcod = alternativa
                respuesta_existente.rescurpun = puntuacion
                respuesta_existente.save()
            else:
                # Crear una nueva respuesta si no existe
                nueva_respuesta = RespuestaExamenCurso(
                    rescurpun=puntuacion,
                    rescurestcod=estudiante,
                    rescurexacod=examen,
                    rescurprecod=pregunta,
                    rescuraltcod=alternativa,
                )
                nueva_respuesta.save()

        estado_pendiente = EstadoExamen.objects.get(estexanom="Reprobado")  # o Pendiente

        # Obtener el registro del examen para el estudiante y el curso
        registro_examen, created = RegistroExamenCurso.objects.get_or_create(
            regexacurestcod=estudiante,
            regexacurexacod=examen,
            regexacurcurcod=curso,
            defaults={
                "regexacurestexacod": estado_pendiente,
                "regexacurpun": 0.0,
                "regexacurint": 0
            }
        )
        
        # Actualizar la puntuación total y el número de intentos
        registro_examen.regexacurpun = puntuacion_total
        registro_examen.regexacurint += 1
        
        # Actualizar el estado del examen según la puntuación obtenida
        estado_aprobado = EstadoExamen.objects.get(estexanom="Aprobado")
        estado_desaprobado = EstadoExamen.objects.get(estexanom="Reprobado")
        if puntuacion_total >= 14:
            registro_examen.regexacurestexacod = estado_aprobado
        else:
            registro_examen.regexacurestexacod = estado_desaprobado

        registro_examen.save()
        
        return Response({"message": "Respuestas guardadas o actualizadas con éxito."}, status=status.HTTP_200_OK)