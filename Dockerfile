FROM python:3.12-alpine3.19

# Configurar la zona horaria
ENV TZ=America/Bogota

# Copia los archivos de la aplicación al contenedor
COPY . /app

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala los requisitos del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script de la aplicación
CMD ["python", "app.py"]
