# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y el código de la aplicación al contenedor
COPY requirements.txt requirements.txt
COPY . .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que Flask correrá
EXPOSE 5000

# Define el comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
