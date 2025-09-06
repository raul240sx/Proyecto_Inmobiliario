# Documentación del Proyecto

## Hito 1

### Requerimiento 1

* Se crea el repositorio agregando un `README` y un `.gitignore` de Python. Una vez creado el repositorio, se abre un Codespace y se modifica el `.gitignore` para ocultar archivos de configuración y variables de entorno, además de carpetas `__pycache__` que se encuentran dentro de otras carpetas en el proyecto de Django.
* Se crea un archivo `docker-compose.yml` para crear contenedores de Django, PostgreSQL y pgAdmin para la visualización, todos conectados a la misma red. En este archivo se configuran los servicios, los cuales llamamos `db` para la base de datos de PostgreSQL, `web` para el servicio de Django y `pgadmin` para el servicio de pgAdmin. Además, se configura la dirección de los volúmenes, los puertos a utilizar (en este caso los por defecto de cada servicio), las credenciales de acceso a las aplicaciones de PostgreSQL, Django y pgAdmin, y la red que compartirán. Adicionalmente, se instala la extensión **Container Tools** de VS Code para una mejor visualización de los contenedores.

```yaml
services:
  db:
    image: postgres
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"
    networks:
      - django_network

  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_DEFAULT_EMAIL}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_DEFAULT_PASSWORD}
      - PGADMIN_CONFIG_PROXY_X_HOST_COUNT=1
      - PGADMIN_CONFIG_PROXY_X_PREFIX_COUNT=1
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - django_network

  web:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/usr/src/app
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_HOST=db
    depends_on:
      - db
    networks:
      - django_network

volumes:
  postgres_data:

networks:
  django_network:
    driver: bridge
```

* Dentro de la configuración del servicio `web` de Django, configuramos que todo se construirá dentro de una carpeta llamada `backend`, la cual también crearemos para reflejar el proyecto. Dentro de esta carpeta se crea un archivo `requirements.txt` con todas las dependencias necesarias para el proyecto de Django. También se crea un `Dockerfile` para ejecutar automáticamente la instalación de las dependencias, entre otras configuraciones.

```dockerfile
# Imagen de Python 3.12
FROM python:3.9

# Variables de entorno para Python
# Evitan archivos .pyc innecesarios y aseguran que la salida de logs no se bufferice
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear un usuario no-root seguro
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -u ${USER_ID} -g appuser -m -s /bin/sh appuser

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiar solo requirements.txt primero
COPY --chown=appuser:appuser requirements.txt .

# Instalar dependencias como root
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar el resto del código como usuario no-root
COPY --chown=appuser:appuser . .

# Cambiar a usuario no-root
USER appuser
```

* En el `requirements.txt`, además de Django, se debe incluir `psycopg2-binary` para la integración de PostgreSQL con Django:

```
django
psycopg2-binary
pillow
python-dotenv
```

* Se crea el archivo `.env` que contiene las variables de entorno con los usernames y las contraseñas de las aplicaciones:

```
POSTGRES_DB=django_postgres
POSTGRES_USER=user
POSTGRES_PASSWORD=1234
PGADMIN_DEFAULT_EMAIL=user@correo.cl
PGADMIN_DEFAULT_PASSWORD=1234
```

* Luego se ejecuta el comando en consola:

```bash
docker-compose up --build
```

Para construir los contenedores. Al ser la primera vez que se levantan, es probable que pgAdmin no funcione correctamente, ya que la instalación de PostgreSQL demora más que la de pgAdmin. La solución es bajar los contenedores y hacer un `up` nuevamente.

Otro error posible es que Django no podrá ejecutar el comando para `runserver` porque aún no hemos creado un proyecto y el archivo `manage.py` no existe. Para solucionarlo:

```bash
docker-compose run web django-admin startproject proyecto_inmobiliario .
```

* Con el proyecto creado, ya es posible bajar los contenedores y subirlos nuevamente para que operen correctamente. Esto se puede comprobar accediendo al puerto 8000 para ver que Django está corriendo, y al 5050 para pgAdmin.
* Se procede a conectar Django con PostgreSQL editando el archivo `settings.py` del proyecto. Se importa `os` y `load_dotenv` para cargar las variables de entorno, se configura el `SECRET_KEY` y `DEBUG` en un `.env` propio del proyecto, y se actualiza la sección `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': '5432',
    }
}
```

* Ahora se puede trabajar con PostgreSQL y se puede borrar el archivo `db.sqlite3`.
* Se crea una app llamada `portal`:

```bash
docker-compose exec web python manage.py startapp portal
```

* Además, se crean las apps `users` para el manejo de usuarios y `locations` para regiones y comunas.


#######################################################################################################

### Requerimiento 2

* Se crean las relaciones entre las tablas según los requerimientos del proyecto. En la imagen adjunta `relacion_modelos.png` se encuentran las relaciones.
* Se crean los modelos en la app `portal`, siguiendo las relaciones. Los modelos `Region` y `Comuna` se encuentran en la app `locations`, y el modelo `PerfilUser` en la app `users`:

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid

# Create your models here.
class Region(models.Model):
    class zonas_de_chile(models.TextChoices):
        norte = "Norte", _("Zona Norte")
        centro = "Centro", _("Zona Centro")
        sur = "Sur", _("Zona Sur")

    zona = models.CharField(max_length=10, choices=zonas_de_chile.choices, null=False, blank=False)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}  | Region: {self.nombre} | Zona: {self.zona}"

class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="comunas")

    def __str__(self):
        return f"{self.nombre} | Pertenece a la región: {self.region}"

class Inmueble(models.Model):
    class TipoInmueble(models.TextChoices):
        casa = "CASA", _("Casa")
        departamento = "DEPARTAMENTO", _("Departamento")
        parcela = "PARCELA", _("Parcela")

    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inmuebles", blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.FloatField(default=0)
    m2_totales = models.FloatField(default=0)
    estacionamientos = models.PositiveIntegerField(default=0)
    habitaciones = models.PositiveIntegerField(default=0)
    banos = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=100)
    precio_mensual = models.DecimalField(max_digits=8, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_inmueble = models.CharField(max_length=20, choices=TipoInmueble.choices)
    arrendado = models.BooleanField(default=False)

class SolicitudArriendo(models.Model):
    class EstadoSolicitud(models.TextChoices):
        pendiente = "PENDIENTE", _("Pendiente")
        aprobada = "APROBADA", _("Aprobada")
        rechazada = "RECHAZADA", _("Rechazada")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name="solicitudes")
    mensaje = models.TextField()
    arrendatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    estado = models.CharField(max_length=20, choices=EstadoSolicitud.choices, default=EstadoSolicitud.pendiente)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uuid} | Persona que solicita: {self.arrendatario} | Estado solicitud: {self.estado}"

class PerfilUser(AbstractUser):
    class TipoUsuario(models.TextChoices):
        arrendador = "ARRENDADOR", _("Arrendador")
        arrendatario = "ARRENDATARIO", _("Arrendatario")

    rut = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=100)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices)

    REQUIRED_FIELDS = ['rut', 'email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_username()} | {self.rut}"
```

* Para que el usuario personalizado funcione correctamente se realiza el siguiente ajuste en `settings.py`:

```python
AUTH_USER_MODEL = 'users.PerfilUser'
```

* Se realizan las migraciones:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```


##########################################################################################

### Requerimiento 3

* Se realizan pruebas dentro de una shell para crear registros en la tabla `Region`, listar los registros, eliminar un registro y volver a listar los registros para comprobar la eliminación. Estas pruebas se pueden apreciar en la imagen adjunta `pruebas_registros_hito_1`.
