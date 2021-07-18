# Sistema para API de Casas

## Objetivo

Generar una API Rest para el consumo de datos de casas.

## Sobre el proyecto ...

Hice una implementación sencilla sin datos para que puedan generarse ya sea usando la api o la interfaz de administrador, la idea es mostrar un proyecto base con Django para una API Rest, decidí usar Docker y docker-compose para orquestar los servicios y que se tenga todo el ecosistema de la aplicación, para facilitar su implementación así como el manejo del estándar PEP8 para su fácil lectura.

Los dejo para que se diviertan y si tienen algún comentar los veo en los Issues XD


## Ambiente local de desarrollo

Crear archivo .env (en el mismo directorio donde se encuentra docker-compose.yml) con las siguientes variables de ambiente (cambie los valores de acuerdo a su ambiente):

```
DEBUG=True
ALLOWED_HOSTS=*
CORS_ORIGIN_WHITELIST=[]
HABI_DB_NAME=<habi db name>
HABI_DB_USER=<usr>
HABI_DB_PASSWORD=<password>
HABI_DB_HOST=localhost
HABI_DB_PORT=5432
SERVER_NAME=<ejemplo: http://localhost:8000>
APP_LOGLEVEL=DEBUG

```

Instale dependencias (desarrollo)

```
pipenv install --dev
```


Inicie la aplicacion en su ambiente de desarrollo local

```
pipenv run python manage.py collectstatic --no-input
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

Variables de ambiente
---------------------
   
* **DEBUG** 

    Django DEBUG en produccion use DEBUG=False [ver Django settings](https://docs.djangoproject.com/en/2.2/ref/settings/#debug)

* **SECRET_KEY**

    Django SECRET_KEY, en produccion asigne a un valor. [ver Django settings](https://docs.djangoproject.com/en/2.2/ref/settings/#secret-key)

* **ALLOWED_HOSTS**

    [ver Django settings](https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts)

* **CORS_ORIGIN_WHITELIST**

    [ver django-cors-headers](https://pypi.org/project/django-cors-headers/). valor por defecto es `[]`

* **HABI_DB_NAME**

    Nombre de la base de datos postgresql, por defecto postgresql-habi

* **HABI_DB_USER** 

    Nombre del usuario de la base de datos postgresql

* **HABI_DB_PASSWORD**

    Contraseña de la base de datos postgresql

* **HABI_DB_HOST**

    host donde reside la base de datos postgresql

* **HABI_DB_PORT**

    puerto de la base de datos postgresql, por defecto 5432

* **APP_LOGLEVEL**

    El nivel de log que se usara en la aplicacion, puede ser
    CRITICAL, ERROR, WARNING, INFO, DEBUG. el valor por defecto es `INFO`.

* **SERVER_NAME**

    El protocolo y el nombre del servidor, expuesto de la aplicacion:
    `http://localhost:8000`, se usa para formar la url externa cuando se envian notificaciones por correo electronico

    
    
## iniciar los contenedores bd y svc-habi (desarrollo)

Preparar los permisos de directorios

```
mkdir -p postgresql/data
sudo chown -R 70 postgresql/data
```

Iniciar los contenedores

```
docker-compose up -d db-habi svc-habi
```

Para iniciar las pruebas se debe crear un usuario en el servidor de django

```
docker-compose exec svc-habi bash
```

Dentro del contenedor

```
pipenv run python manage.py createsuperuser
```
Nota: el user debe ser "admin" y el password "adminadmin"(temporal)


reconstruir la imagen del contenedor svc-habi django (cuando se cambian dependencias)

```
 docker-compose build --force-rm --no-cache svc-habi
```

## Linters

lint el proyecto con flake8 y pylint (en el mismo directorio que manage.py)

```
pipenv run flake8
pipenv run pylint HABI casas
pipenv run isort .
```


## Creacion de Administrador Principal

```
pipenv run python manage.py createsuperuser
```


## Ejecute las pruebas unitarias

```
pipenv run coverage run --source='.' manage.py test
```

visualice reporte de cobertura de las pruebas

```
pipenv run coverage report
```

o bien genere el mismo reporte en html

```
pipenv run coverage html
```

puede abrir el reporte en htmlcov/index.html


## Cargar datos iniciales (Catalogos)

Como parte del despliege de la aplicacion se pueden cargar los catalogos iniciales por medio de archivos YAML que contienen los registros para cargarse en los catalogos.

Considerando que la bd esta vacia (de lo contrario ocurrira error de integridad al ya existir informacion previa) ejecute lo siguiente, es importante respetar el orden para evitar errores de integridad.

cargar modelos individuales
```
pipenv run python manage.py loaddata estado
pipenv run python manage.py loaddata ciudades
```

Los datos iniciales de los catalogos estan definidos en [casas/fixtures/*.yaml](casas/fixtures/), consulte este directorio para determinar la lista de archivos actualizada.



## API Endpoints

en el modo desarrollo (DEBUG=True), el sistema cuenta con el endpoint `/swagger/` donde se encuentra documentada el API,
o puede consultarla en el ambiente de desarrollo aqui [API desarrollo](http://localhost:8000/swagger/)

Para utlitlzar la interfaz grafica y agregar un inmueble puede hacerlo en [add inmueble](http://localhost:8000/admin/casas/inmueble/add/)

## Problema de "Me gusta".

Para esta parte solo cabe mencionar que la unica recomendacion que recomiendo es  en el modelo inmuebles generar un nuevo campo 
```python
class Inmueble(models.Model):
   ...
    precio = models.PositiveIntegerField("Precio", null=True, blank=True,
                                         validators=[MinValueValidator(1)])
    # la direccion se puede manejar con relacional de modelos "estado", "cuidad", "C.P" y
    # una pequeña descripcion para ejemplos ilustrativos se manejara como un CharField
    direccion = models.CharField(max_length=80, null=False, blank=False)
    like = models.ManyToManyField(User,
                                  verbose_name='Usuarios que dan "Me gusta"',
                                  blank=True)
```

De esta manera se generar un registro por cada usuario que se agrege al modelo del Inmueble como un "Me gusta"
