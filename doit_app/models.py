from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Importar settings para referenciar AUTH_USER_MODEL

# Modelo Genero existente (del código que proporcionaste)
class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Género")

    class Meta:
        ordering = ['nombre']
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        app_label = "doit_app" # Asegura que esté asociado a esta app

    def __str__(self):
        return self.nombre

# Modelo CustomUser existente (del código que proporcionaste), con adiciones
class CustomUser(AbstractUser):
    tipo_usuario_choices = [
        ('usuario', 'Usuario Normal'),
        ('experto', 'Experto'),
    ]
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Género")
    tipo_usuario = models.CharField(max_length=20, choices=tipo_usuario_choices, default='usuario', verbose_name="Tipo de Usuario")
    nacionalidad = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nacionalidad")
    numDoc = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Número de Documento")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    fechaNacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    evidenciaTrabajo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Evidencia de Trabajo")
    experienciaTrabajo = models.TextField(blank=True, null=True, verbose_name="Experiencia de Trabajo")
    hojaVida = models.CharField(max_length=300, blank=True, null=True, verbose_name="Hoja de Vida")

    # NUEVO CAMPO: idTipoDoc del esquema SQL, integrado directamente en CustomUser
    tipo_documento = models.ForeignKey('TipoDoc', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Documento")

    class Meta:
        verbose_name = "Usuario Personalizado"
        verbose_name_plural = "Usuarios Personalizados"
        app_label = "doit_app" # Asegura que esté asociado a esta app

    def __str__(self):
        return self.username

    def is_usuario_normal(self):
        """Retorna True si el usuario tiene el rol 'usuario'."""
        return self.tipo_usuario == 'usuario'

    def is_experto(self):
        """Retorna True si el usuario tiene el rol 'experto'."""
        return self.tipo_usuario == 'experto'

# NUEVOS MODELOS basados en el esquema SQL, adaptados para usar CustomUser

# 2. TipoDoc (del esquema SQL)
class TipoDoc(models.Model):
    Nombre = models.CharField(max_length=50, verbose_name="Nombre del tipo de documento")

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
        db_table = "TipoDoc" # Nombre de la tabla en la base de datos
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 3. Categorias (del esquema SQL)
class Categorias(models.Model):
    Nombre = models.CharField(max_length=50, verbose_name="Nombre de la categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        db_table = "Categorias"
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 4. Pais (del esquema SQL)
class Pais(models.Model):
    Nombre = models.CharField(max_length=50, verbose_name="Nombre del país")

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        db_table = "Pais"
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 5. Departamento (del esquema SQL)
class Departamento(models.Model):
    Nombre = models.CharField(max_length=50, verbose_name="Nombre del departamento")
    idPais = models.ForeignKey(Pais, on_delete=models.CASCADE, verbose_name="País")

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        db_table = "Departamento"
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 6. Ciudad (del esquema SQL)
class Ciudad(models.Model):
    Nombre = models.CharField(max_length=50, verbose_name="Nombre de la ciudad")
    idDepartamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, verbose_name="Departamento")

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        db_table = "Ciudad"
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 7. Rol (del esquema SQL) - Esta tabla se reemplaza por CustomUser.tipo_usuario

# 8. Metodo (del esquema SQL)
class Metodo(models.Model):
    Nombre = models.CharField(max_length=100, verbose_name="Nombre del método de pago")

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"
        db_table = "Metodo"
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 9. Estado (del esquema SQL)
class Estado(models.Model):
    Nombre = models.CharField(max_length=50, verbose_name="Nombre del estado")

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        db_table = "Estado"
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 10. Pagos (del esquema SQL)
class Pagos(models.Model):
    Monto = models.FloatField(verbose_name="Valor del servicio")
    # Renombrado para evitar conflicto con el modelo 'Estado'
    estado_pago_texto = models.CharField(max_length=40, verbose_name="Estado del pago (texto)")
    Fecha = models.DateField(verbose_name="Fecha de pago")
    idMetodo = models.ForeignKey(Metodo, on_delete=models.CASCADE, verbose_name="Método de pago")
    # related_name para evitar conflictos con otras FKs al modelo Estado
    idestado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='pagos_estado', verbose_name="Estado del servicio")

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = "Pagos"
        app_label = "doit_app"

    def __str__(self):
        return f"Pago #{self.id} - Monto: {self.Monto} - Estado: {self.estado_pago_texto}"

# 11. Usuario (del esquema SQL) - Esta tabla se reemplaza por CustomUser.
# Las relaciones ahora apuntan a settings.AUTH_USER_MODEL

# 12. Profesion (del esquema SQL)
class Profesion(models.Model):
    Nombre = models.CharField(max_length=50, verbose_name="Nombre de la profesión")
    Descripcion = models.CharField(max_length=100, verbose_name="Descripción de la profesión")
    # Enlaza con CustomUser
    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario")

    class Meta:
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"
        db_table = "Profesion"
        app_label = "doit_app"

    def __str__(self):
        return self.Nombre

# 13. Servicios (del esquema SQL)
class Servicios(models.Model):
    NombreServicio = models.CharField(max_length=50, verbose_name="Nombre del servicio")
    Precio = models.FloatField(verbose_name="Precio del servicio")
    Ubicacion = models.CharField(max_length=100, verbose_name="Ubicación del experto")
    Descripcion = models.CharField(max_length=150, verbose_name="Breve descripción del servicio")
    Duracion = models.CharField(max_length=50, verbose_name="Duración del servicio")
    # Enlaza con CustomUser
    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario que ofrece el servicio")
    idCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, verbose_name="Ciudad donde se ofrece el servicio")
    idCategorias = models.ForeignKey(Categorias, on_delete=models.CASCADE, verbose_name="Categoría del servicio")
    idestado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='servicios_estado', verbose_name="Estado del servicio")
    idPagos = models.ForeignKey(Pagos, on_delete=models.CASCADE, verbose_name="Pago del servicio")

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        db_table = "Servicios"
        app_label = "doit_app"

    def __str__(self):
        return self.NombreServicio

# 14. Reserva (del esquema SQL)
class Reserva(models.Model):
    Fecha = models.DateField(verbose_name="Fecha de la reserva")
    Hora = models.TimeField(verbose_name="Hora de la reserva")
    # Enlaza con CustomUser
    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas_hechas', verbose_name="Usuario que hace la reserva")
    idEstado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='reservas_estado', verbose_name="Estado de la reserva")
    idServicios = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name="Servicio reservado")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        db_table = "Reserva"
        app_label = "doit_app"

    def __str__(self):
        return f"Reserva #{self.id} - {self.Fecha} {self.Hora}"

# 15. Calificaciones (del esquema SQL)
class Calificaciones(models.Model):
    puntuacion = models.CharField(max_length=50, verbose_name="Puntuación del servicio")
    Comentario = models.CharField(max_length=150, verbose_name="Comentario del servicio")
    Fecha = models.DateField(verbose_name="Fecha del comentario")
    # Enlaza con CustomUser
    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calificaciones_recibidas', verbose_name="Usuario que recibe la calificación")
    idServicios = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name="Servicio calificado")

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        db_table = "Calificaciones"
        app_label = "doit_app"

    def __str__(self):
        return f"Calificación #{self.id} - Puntuación: {self.puntuacion}"
