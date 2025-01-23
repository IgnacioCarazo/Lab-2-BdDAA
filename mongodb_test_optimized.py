import time
import json
from pymongo import MongoClient, ASCENDING

# Cargar los datos desde el archivo JSON
with open('test_data.json', 'r') as f:
    data = json.load(f)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
usuarios = db["users"]
publicaciones = db["posts"]
comentarios = db["comments"]
etiquetas = db["tags"]

# Crear índices en campos clave para mejorar el rendimiento de las consultas
usuarios.create_index([("_id", ASCENDING)])
publicaciones.create_index([("author_id", ASCENDING)])
comentarios.create_index([("author_id", ASCENDING)])
etiquetas.create_index([("name", ASCENDING)])

# 1. CREATE - Inserción masiva
start_time = time.time()
usuarios.insert_many(data["users"])
publicaciones.insert_many(data["posts"])
comentarios.insert_many(data["comments"])
etiquetas.insert_many(data["tags"])
print(f"CREATE - MongoDB: {time.time() - start_time} segundos")

# 2. READ - Consulta por clave primaria
start_time = time.time()
usuario = usuarios.find_one({"_id": 1})
print(f"READ - MongoDB (clave primaria): {time.time() - start_time} segundos")

# 2.1. Imprimir un comentario de cualquier usuario
start_time = time.time()
comentario = comentarios.find_one({"author_id": 1})
print(f"READ - MongoDB (comentario de usuario 1): {comentario}")
print(
    f"READ - MongoDB (comentario de usuario 1) - Tiempo: {time.time() - start_time} segundos")

# 2.2. Consulta con JOINs entre colecciones (simulada) usando el Aggregation Pipeline
start_time = time.time()
# Buscar publicaciones, comentarios y usuarios relacionados con el tag "cold"
cold_tag = etiquetas.find_one({"name": "cold"})
pipeline = [
    {
        "$match": {
            "tags": cold_tag["_id"]
        }
    },
    {
        "$lookup": {
            "from": "posts",
            "localField": "_id",
            "foreignField": "author_id",
            "as": "posts"
        }
    },
    {
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "author_id",
            "as": "comments"
        }
    },
    {
        "$project": {
            "_id": 1,
            "name": 1,  # Aseguramos que el nombre del autor esté en el resultado
            "posts": 1,
            "comments": 1
        }
    }
]
resultado = usuarios.aggregate(pipeline)
for usuario in resultado:
    print(f"Usuario con tag 'cold': {usuario.get('name', 'No Name')}")
print(f"READ - MongoDB (usuarios, publicaciones y comentarios con el tag 'cold') - Tiempo: {
      time.time() - start_time} segundos")

# 2.3. Obtener la cantidad de publicaciones y comentarios y nombre de autor por cada autor
start_time = time.time()
pipeline = [
    {
        "$lookup": {
            "from": "posts",
            "localField": "_id",
            "foreignField": "author_id",
            "as": "posts"
        }
    },
    {
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "author_id",
            "as": "comments"
        }
    },
    {
        "$project": {
            "author_name": 1,  # Aseguramos que el nombre esté proyectado correctamente
            "posts_count": {"$size": "$posts"},
            "comments_count": {"$size": "$comments"}
        }
    }
]
resultado = usuarios.aggregate(pipeline)
print(f"READ - MongoDB (cantidad de publicaciones y comentarios por autor): {
      time.time() - start_time} segundos")

# 3. UPDATE - Actualización masiva
start_time = time.time()
usuarios.update_many({}, {"$set": {"name": "TEST_" + "Updated Name"}})
print(f"UPDATE - MongoDB: {time.time() - start_time} segundos")

# 4. DELETE - Eliminación masiva
start_time = time.time()
usuarios.delete_many({})
publicaciones.delete_many({})
comentarios.delete_many({})
etiquetas.delete_many({})
print(f"DELETE - MongoDB: {time.time() - start_time} segundos")
