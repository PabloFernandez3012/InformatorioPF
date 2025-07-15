from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class FormularioRegistroPersonalizado(UserCreationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        help_text='Requerido. 150 caracteres o menos. Solo letras, números y @/./+/-/_ permitidos.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='''
        Tu contraseña debe cumplir los siguientes requisitos:
        • Al menos 8 caracteres de longitud
        • No puede ser demasiado similar a tu información personal
        • No puede ser una contraseña comúnmente usada
        • No puede ser completamente numérica
        • Debe contener al menos una letra mayúscula
        • Debe contener al menos una letra minúscula
        • Debe contener al menos un número
        • Debe contener al menos un carácter especial (@$!%*?&)
        '''
    )
    
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Ingresa la misma contraseña nuevamente para verificación.'
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if len(password1) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        if not re.search(r'[A-Z]', password1):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        
        if not re.search(r'[a-z]', password1):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
        
        if not re.search(r'\d', password1):
            raise ValidationError('La contraseña debe contener al menos un número.')
        
        if not re.search(r'[@$!%*?&]', password1):
            raise ValidationError('La contraseña debe contener al menos un carácter especial (@$!%*?&).')
        
        if password1.isdigit():
            raise ValidationError('La contraseña no puede ser completamente numérica.')
        
        # Lista de contraseñas comunes
        contraseñas_comunes = [
            'password', 'contraseña', '123456', '12345678', 'qwerty', 
            'abc123', 'password123', 'admin', 'usuario', '123456789',
            'welcome', 'login', 'master', 'superman', 'batman'
        ]
        
        if password1.lower() in contraseñas_comunes:
            raise ValidationError('Esta contraseña es muy común. Elige una diferente.')
        
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')
        
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        
        if len(username) < 3:
            raise ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')
        
        return username
