from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="API Académica Relacional en Memoria",
    description="Simulación de base de datos relacional de 5 tablas usando listas de Python",
    version="1.0.0"
)

print("="*30);
#SIMULACIÓN DE TABLAS (ESTRUCTURA RELACIONAL)
print("="*30);

#1. Tabla Roles (PK: id)
roles = [
    {"id":1,"nombre": "Administrador"},
    {"id":2,"nombre": "Instructor"},
    {"id":3,"nombre": "Aprendiz"}
]

#2. Tablas Usuarios (PK: id, FK: rol_id -> roles_id)
usuarios =[
    {"id": 1, "nombre": "Juan", "apellido": "Pérez", "telefono": "3208529637","edad": 25, "rol_id":3},
    {"id" 2, "nombre": "María", "apellido": "Gómez", "telefono": "3208529634", "edad": 35, "rol_id":2}
]

#3. Tabla Programa (PK: id)
programas = [
    {"id": 1, "nombre": "Análisis y Desarrollo de Software", "codigo": "ADSO-2026"},
    {"id": 2, "nombre": "Diseño y Desarrollo de Multimedia", "codigo": "DDM-2026"}
]

#4. Tabla Matriculas (PK: id,)
