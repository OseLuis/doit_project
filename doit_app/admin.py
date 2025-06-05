# asistencia/admin.py

from django.contrib import admin
from .models import Genero, CustomUser # Importa tus modelos

# Importa UserAdmin del módulo de autenticación de Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Registra Genero (esto ya lo tenías bien)
@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre',) # Muestra el campo 'nombre' en la lista

# Registra CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Esto es para mostrar los campos adicionales en la página de edición de un usuario
    # El 'fieldsets' original de UserAdmin incluye username, password, permisos, etc.
    # Aquí le añadimos un nuevo conjunto de campos para tu información adicional.
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Información Adicional', {'fields': ('genero', 'tipo_usuario', 'nacionalidad', 'numDoc', 'telefono', 'fechaNacimiento', 'evidenciaTrabajo', 'experienciaTrabajo', 'hojaVida')}),)
    )

    # Esto es para mostrar los campos adicionales cuando estás creando un NUEVO usuario desde el admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (('Información Adicional', {'fields': ('genero', 'tipo_usuario', 'nacionalidad', 'numDoc', 'telefono', 'fechaNacimiento', 'evidenciaTrabajo', 'experienciaTrabajo', 'hojaVida')}),)
    )

    # Esto es para mostrar los campos en la tabla resumen cuando ves la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_usuario', 'genero') # Añade campos a la vista de lista

    # Puedes añadir campos de búsqueda si quieres (útil para encontrar usuarios)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'numDoc')

    # Puedes añadir filtros (sidebar)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'tipo_usuario', 'genero')

    # Ordenamiento por defecto en la lista de usuarios
    ordering = ('username',)