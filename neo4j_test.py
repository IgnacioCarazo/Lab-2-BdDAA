import time
import json
from neo4j import GraphDatabase

# Cargar los datos desde el archivo JSON
with open('test_data.json', 'r') as f:
    data = json.load(f)

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

# Crear una sesión de Neo4j
driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session()

# Funciones auxiliares para la creación de nodos y relaciones


def create_nodes(session, data):
    # Crear nodos de usuarios
    for user in data["users"]:
        session.run(
            "CREATE (u:User {id: $id, name: $name})",
            id=user["id"],  # Usar "id" en lugar de "_id"
            name=user["name"]
        )

    # Crear nodos de publicaciones
    for post in data["posts"]:
        session.run(
            "CREATE (p:Post {id: $id, title: $title, content: $content, author_id: $author_id})",
            id=post["id"],
            title=post["title"],
            content=post["content"],
            author_id=post["author_id"]
        )

    # Crear nodos de comentarios
    for comment in data["comments"]:
        session.run(
            "CREATE (c:Comment {id: $id, text: $text, author_id: $author_id, post_id: $post_id})",
            id=comment["id"],
            text=comment["text"],
            author_id=comment["author_id"],
            post_id=comment["post_id"]
        )

    # Crear nodos de etiquetas
    for tag in data["tags"]:
        session.run(
            "CREATE (t:Tag {id: $id, name: $name})",
            id=tag["id"],
            name=tag["name"]
        )


def create_relations(session, data):
    # Crear relaciones entre publicaciones y etiquetas
    for post in data["posts"]:
        # Obtener las etiquetas de la publicación de manera segura
        tags = post.get("tags", [])
        for tag_id in tags:
            session.run("""
                MATCH (p:Post {id: $post_id}), (t:Tag {id: $tag_id})
                CREATE (p)-[:HAS_TAG]->(t)
            """, post_id=post["id"], tag_id=tag_id)

    # Crear relaciones entre comentarios y etiquetas
    for comment in data["comments"]:
        # Obtener las etiquetas del comentario de manera segura
        tags = comment.get("tags", [])
        for tag_id in tags:
            session.run("""
                MATCH (c:Comment {id: $comment_id}), (t:Tag {id: $tag_id})
                CREATE (c)-[:HAS_TAG]->(t)
            """, comment_id=comment["id"], tag_id=tag_id)

    # Crear relaciones entre usuarios y publicaciones
    for post in data["posts"]:
        session.run("""
            MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
            CREATE (u)-[:AUTHORED]->(p)
        """, user_id=post["author_id"], post_id=post["id"])

    # Crear relaciones entre usuarios y comentarios
    for comment in data["comments"]:
        session.run("""
            MATCH (u:User {id: $user_id}), (c:Comment {id: $comment_id})
            CREATE (u)-[:COMMENTED]->(c)
        """, user_id=comment["author_id"], comment_id=comment["id"])


# 1. CREATE - Inserción masiva
start_time = time.time()
create_nodes(session, data)
create_relations(session, data)
print(f"CREATE - Neo4j: {time.time() - start_time} segundos")

# 2. READ - Consulta por clave primaria (Usuario)
start_time = time.time()
result = session.run("MATCH (u:User {id: 1}) RETURN u")
usuario = result.single()
print(f"READ - Neo4j (usuario 1): {usuario['u']['name']
                                   } - Tiempo: {time.time() - start_time} segundos")

# 2.1. Imprimir un comentario de cualquier usuario (Comentario de usuario 1)
start_time = time.time()
result = session.run(
    "MATCH (u:User {id: 1})-[:COMMENTED]->(c:Comment) RETURN c LIMIT 1")
comentario = result.single()
print(f"READ - Neo4j (comentario de usuario 1): {
      comentario['c']['content']} - Tiempo: {time.time() - start_time} segundos")

# 2.2. Consulta con relaciones (simulada): Buscar publicaciones, comentarios y usuarios relacionados con el tag "cold"
start_time = time.time()
result = session.run("""
    MATCH (t:Tag {name: 'cold'})<-[:HAS_TAG]-(p:Post)-[:AUTHORED]->(u:User),
          (t)<-[:HAS_TAG]-(c:Comment)-[:COMMENTED]->(u)
    RETURN u, p, c
""")
for record in result:
    user = record["u"]
    post = record["p"]
    comment = record["c"]
print(f"READ - Neo4j (usuarios, publicaciones y comentarios con el tag 'cold') - Tiempo: {
      time.time() - start_time} segundos")

# 2.3. Obtener la cantidad de publicaciones y comentarios por cada autor
start_time = time.time()
result = session.run("""
    MATCH (u:User)-[:AUTHORED]->(p:Post), (u)-[:COMMENTED]->(c:Comment)
    RETURN u.name AS author_name, COUNT(p) AS posts_count, COUNT(c) AS comments_count
""")

print(f"READ - Neo4j (cantidad de publicaciones y comentarios por autor): {
      time.time() - start_time} segundos")

# 3. UPDATE - Actualización masiva (actualizar el nombre de todos los usuarios)
start_time = time.time()
session.run("MATCH (u:User) SET u.name = 'TEST_' + u.name")
print(f"UPDATE - Neo4j: {time.time() - start_time} segundos")

# 4. DELETE - Eliminación masiva (borrar todos los nodos y relaciones)
start_time = time.time()
session.run("MATCH (n) DETACH DELETE n")
print(f"DELETE - Neo4j: {time.time() - start_time} segundos")

# Cerrar sesión
session.close()
driver.close()
