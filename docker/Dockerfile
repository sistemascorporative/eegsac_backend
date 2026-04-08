# Usa la imagen base de Python con la versión deseada
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia el resto de los archivos del proyecto al directorio de trabajo del contenedor
COPY . .

# Expone el puerto 8000 para que la aplicación Django pueda ser accesible desde fuera del contenedor
EXPOSE 8000

# Comando para iniciar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]