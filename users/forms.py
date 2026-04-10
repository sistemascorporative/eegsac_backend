from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import EstudianteUser

class EstudianteUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = EstudianteUser
        fields = ('email', 'usuario')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # 🔥 AQUÍ SE ENCRIPTA
        if commit:
            user.save()
        return user


class EstudianteUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EstudianteUser
        fields = ('email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial["password"]