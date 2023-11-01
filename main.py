import fastapi
import mysql.connector
from pydantic import BaseModel

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="lcpbq9az4jklobvq.cbetxkdyhwsb.us-east-1.rds.amazonaws.com	",
    user="bo308pcse26i5bhg",
    password="k4c63m8edzcp2gkb",
    port="3306",
    database="wb9hlgewc50qddy9"
)

cursor = conn.cursor()

# Crear la tabla en MySQL
cursor.execute('''
    CREATE TABLE contactos (
        email VARCHAR(255) PRIMARY KEY,
        nombre TEXT,
        telefono VARCHAR(20)
    )
''')

# Insertar datos en la tabla
insert_query = '''
    INSERT INTO contactos (email, nombre, telefono)
    VALUES (%s, %s, %s)
'''

contactos_data = [
    ("juan@example.com", "Juan Pérez", "555-123-4567"),
    ("maria@example.com", "María García", "555-678-9012")
]

cursor.executemany(insert_query, contactos_data)

# Confirmar y cerrar la conexión
conn.commit()
conn.close()

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="lcpbq9az4jklobvq.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user="bo308pcse26i5bhg",
    password="k4c63m8edzcp2gkb",
    port="3306",
    database="wb9hlgewc50qddy9"
)

app = fastapi.FastAPI()

class Contacto(BaseModel):
    email: str
    nombres: str
    telefono: str

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contactos (email, nombres, telefono) VALUES (%s, %s, %s)',
                   (contacto.email, contacto.nombres, contacto.telefono))
    conn.commit()
    return contacto

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contactos')
    response = []
    for row in cursor:
        contacto = Contacto(email=row[0], nombres=row[1], telefono=row[2])
        response.append(contacto)
    return response

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contactos WHERE email = %s', (email,))
    row = cursor.fetchone()
    if row is not None:
        contacto = Contacto(email=row[0], nombres=row[1], telefono=row[2])
        return contacto
    else:
        return {"error": "Contacto no encontrado"}

@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto."""
    cursor = conn.cursor()
    cursor.execute('UPDATE contactos SET nombres = %s, telefono = %s WHERE email = %s',
                   (contacto.nombres, contacto.telefono, email))
    conn.commit()
    return contacto

@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contactos WHERE email = %s', (email,))
    conn.commit()
    return Contacto

    """Elimina un contacto."""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contactos WHERE email = ?', (email,))
    conn.commit()
    return Contacto
