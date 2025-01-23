import time
import json
from pymongo import MongoClient

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

# 2.2. Consulta con JOINs entre colecciones (simulada)
start_time = time.time()
# Buscar publicaciones, comentarios y usuarios relacionados con el tag "cold"
cold_tag = etiquetas.find_one({"name": "cold"})
posts_with_cold_tag = publicaciones.find({"tags": cold_tag["_id"]})
comments_with_cold_tag = comentarios.find({"tags": cold_tag["_id"]})
users_with_cold_tag = []
for post in posts_with_cold_tag:
    user = usuarios.find_one({"_id": post["author_id"]})
    users_with_cold_tag.append(user)
for comment in comments_with_cold_tag:
    user = usuarios.find_one({"_id": comment["author_id"]})
    users_with_cold_tag.append(user)

print(f"READ - MongoDB (usuarios, publicaciones y comentarios con el tag 'cold') - Tiempo: {
      time.time() - start_time} segundos")

# 2.3. Obtener la cantidad de publicaciones y comentarios y nombre de autor por cada autor
start_time = time.time()
authors_data = []
for user in usuarios.find():
    post_count = publicaciones.count_documents({"author_id": user["_id"]})
    comment_count = comentarios.count_documents({"author_id": user["_id"]})
    authors_data.append({
        "author_name": user["name"],
        "posts_count": post_count,
        "comments_count": comment_count
    })
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
