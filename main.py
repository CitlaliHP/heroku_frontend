import fastapi
import sqlite3
from pydantic import BaseModel

import sqlite3
conn = sqlite3.connect('contactos.db')  # reemplaza 'tu_base_de_datos.db' con el nombre de tu base de datos
cursor = conn.cursor()

# Crear tabla e insertar datos
cursor.executescript('''
    CREATE TABLE contactos (
    email VARCHAR PRIMARY KEY,
    nombre TEXT,
    telefono TEXT
);

INSERT INTO contactos (email, nombre, telefono)
VALUES ("juan@example.com", "Juan Pérez", "555-123-4567");

INSERT INTO contactos (email, nombre, telefono)
VALUES ("maria@example.com", "María García", "555-678-9012");
''')

conn.commit()
conn.close()


# Conexión a la base de datos SQLite
conn = sqlite3.connect('contactos.db')

app = fastapi.FastAPI()


class Contacto(BaseModel):
    email: str
    nombres: str
    telefono: str

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contactos (email, nombres, telefono) VALUES (?, ?, ?)',
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
    cursor.execute('SELECT * FROM contactos WHERE email = ?', (email,))
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
    cursor.execute('UPDATE contactos SET nombres = ?, telefono = ? WHERE email = ?',
                   (contacto.nombres, contacto.telefono, email))
    conn.commit()
    return contacto

@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contactos WHERE email = ?', (email,))
    conn.commit()
    return Contacto
