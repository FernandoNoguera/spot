from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from azure.storage.blob import BlobServiceClient
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import uuid
import base64
import os
import asyncpg
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime

# Dotenv
dotenv_path = join(dirname(__file__), '.env.dev')
load_dotenv(dotenv_path)
load_dotenv(dotenv_path, verbose=True)


# Modelos
class Evento(BaseModel):
    fecha: datetime
    imagen: str
    camara_id: str

class BatchEventos(BaseModel):
    eventos: List[Evento]


# Configuración de la base de datos
USER_DB = os.environ.get("USER_DB")
PASSWORD_DB = os.environ.get("PASSWORD_DB")
HOST_DB = os.environ.get("HOST_DB")
PORT_DB = os.environ.get("PORT_DB")
NAME_DB = os.environ.get("NAME_DB")

async def create_tables():
    conn = await asyncpg.connect(
        user=USER_DB,
        password=PASSWORD_DB,
        database=NAME_DB,
        host=HOST_DB
    )
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id bigserial PRIMARY KEY,
            date_utc timestamp with time zone,
            camera_id text,
            image_url text
        );
    ''')
    await conn.close()
dsn = f'postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}'
async def connect():
    conn = await asyncpg.connect(dsn)
    return conn


# Configuración de la aplicación
app = FastAPI(port=8003)

@app.on_event("startup")
async def startup():
    await create_tables()



origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a Azure Blob Storage
CONTAINER_ABS = os.environ.get("CONTAINER_ABS")
PASSWORD_ABS = os.environ.get("PASSWORD_ABS")
CONN_STR = os.environ.get("CONN_STR")
conn_str = CONN_STR
container_name = CONTAINER_ABS
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(container_name)

# Endpoint para subir imágenes en batch
@app.post("/subir_imagenes")
async def subir_imagenes(eventos: BatchEventos):
    conn = await connect()
    values = []
    for evento in eventos.eventos:
        # Decodificar imagen en base64
        img_bytes = base64.b64decode(evento.imagen)
        # Generar nombre de archivo único
        nombre_archivo = f"{uuid.uuid4()}.jpg"
        # Crear archivo en disco
        with open(nombre_archivo, "wb") as f:
            f.write(img_bytes)
        # Subir archivo a Azure Blob Storage
        blob_client = container_client.get_blob_client(nombre_archivo)
        with open(nombre_archivo, "rb") as data:
            blob_client.upload_blob(data)
        # Eliminar archivo temporal
        os.remove(nombre_archivo)
        # Guardar datos en PostgreSQL
        url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{nombre_archivo}"
        values.append((evento.fecha, evento.camara_id, url))
    query = "INSERT INTO events (date_utc, camera_id, image_url) VALUES ($1, $2, $3)"
    await conn.executemany(query, values)
    await conn.close()
    return {"mensaje": "Imágenes subidas correctamente"}
