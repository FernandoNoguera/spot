# Define la imagen base
FROM python:3.9-slim-buster

# Establece el directorio de trabajo en el contenedor
WORKDIR .

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala los paquetes de requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Establece la variable de entorno
ENV PORT=8004

# Expone el puerto
EXPOSE 8004

# Ejecuta la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]