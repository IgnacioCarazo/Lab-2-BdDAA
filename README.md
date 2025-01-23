# Proyecto: MongoDB y Neo4j con Docker

Este proyecto contiene ejemplos de cómo trabajar con MongoDB y Neo4j usando Docker y Docker Compose para simular operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre un conjunto de datos generados aleatoriamente.

## Requisitos

- **Docker**: Para crear y gestionar contenedores.
- **Docker Compose**: Para definir y ejecutar aplicaciones Docker multi-contenedor.
- **Python 3.x**: Para ejecutar los scripts de generación y manipulación de datos.
- **MongoDB**: Base de datos NoSQL.
- **Neo4j**: Base de datos de grafos.

## Instalación

### 1. Instalar Docker

Para instalar Docker en tu sistema, sigue las instrucciones oficiales:

- [Instalar Docker en Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

Verifica que Docker se haya instalado correctamente ejecutando:

```bash
docker --version
```

### 2. Construir y correr los contenedores

Ubicarse en la raíz del proyecto y correr:

```bash
docker-compose up --build
```

### 3. Instalar Python y dependencias

Instalar python con pip:

```bash
sudo apt install python3-pip

```

Para facilidad del proyecto se recomienda realizar su propio 'environment' de python e instalar:

- **faker**
- **pymongo**
- **neo4j**

Por medio del comando pip:

```bash
pip install faker pymongo neo4j

```

### 4. Generar json con los datos

Para esto se va a ejecutar el archivo 'data_generator.py'

### 5. Correr experimentos

Para correr los experimentos existen dos archivos, uno por cada base de datos:

- **mongodb_test.py**
- **neo4j_test.py**

Ejecutar cualquiera de los dos va a imprimir el resultado de las pruebas realizadas y su tiempo de duración realizandolas.
