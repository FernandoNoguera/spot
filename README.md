# Mi Aplicación FastAPI SPOT

## Descripción

Esta es una aplicación es una test de ingreso para SPOT.

## Deploment y documentación del API

- [Deployment](https://api.spot.maelstrom-digital.cl/)
- [Postman documentation](https://documenter.getpostman.com/view/14482878/2s93eYWY8g)
- [documentación Swagger UI ](https://api.spot.maelstrom-digital.cl/docs)
- [Documentacion ReDoc](https://api.spot.maelstrom-digital.cl/redoc)

## Requisitos
- Python 3.7 o superior
- pip
- [Opcional] Docker 

## Instalación

Clona el repositorio:
``` 
git clone https://github.com/FernandoNoguera/spot.git
``` 

Navega hasta la carpeta del proyecto:
``` 
cd spot
``` 


Crea un entorno virtual y actívalo:
``` 
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:
```
pip install -r requirements.txt
``` 

Agregar .env.dev con las credenciales de la aplicación como se muestra en el archivo .env.dev.sample

## Uso

Activa el entorno virtual:
``` 
source .venv/bin/activate
``` 

Inicia el servidor de desarrollo de FastAPI:

``` 
uvicorn app.main:app --reload
``` 

Abre un navegador web y visita [/docs](http://localhost:8004/docs) para acceder a la documentación de la API.

Para detener el servidor, presiona Ctrl + C.

## Docker

También puedes ejecutar la aplicación utilizando Docker

Construye la imagen de Docker:
``` 
docker build -t my-fastapi-app .
``` 

Inicia el contenedor:
``` 
docker run -d --name my-fastapi-container -p 8003:80 my-fastapi-app
``` 
Abre un navegador web y visita [/docs](http://localhost:8004/docs) para acceder a la documentación de la API.
Para detener el contenedor, presiona Ctrl + C y luego ejecuta:

``` 
docker down
``` 

## Test

También puedes ejecutar test:

``` 
pytest test_app.py 
``` 


## Contribución
¡Las contribuciones son bienvenidas! Si deseas colaborar en este proyecto, por favor, abre un "pull request" en GitHub.


