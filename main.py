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

#4. Tabla Matriculas (PK: id, FK: usuario_id -> usuarios.id, FK: programa_id -> programa.id)
matriculas = [
    {"id": 1, "usuario_id":1, "programa_id": 1, "fecha_matricula": "2026-02-01"}
]

#5. Tabla Asistencias (PK: id, FK: matricula_id -> matriculas.id)
asistencias = [
    {"id": 1, "matricula_id": 1, "fecha": "2026-02-24", "estado": "Asistió"}
]
print("="*30)
# ENDPOINTS Y ENRUTAMIENTO (OPERACIONES)
print("="*30)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido al Sistema Académico de 5 Tablas Relacionadas"}

# --- ENDPOINTS TABLA: ROLES ---
@app.get("/roles")
def listar_roles():
    return roles

@app.post("/roles")
def crear_rol(nombre: str):
    nuevo_id = len(roles) + 1
    nuevo_rol = {"id": nuevo_id, "nombre": nombre}
    roles.append(nuevo_rol)
    return nuevo_rol

# --- ENDPOINTS TABLA: USUARIOS (Valida FK rol_id) ---
@app.get("/usuarios")
def listar_usuarios():
    #Retorna usuarios inyectando la información de su rol
    resultado = []
    for u in usuarios:
        rol = next((r for r in roles if r["id"] == u["rol_id"]), None)
        resultado.append({
            "id": u["id"],
            "nombre": u["nombre"],
            "apellido": u["apellido"],
            "telefono": u["telefono"],
            "edad": u["edad"],
            "rol": rol
        })
        return resultado

@app.post("/usuarios")
def crear_usuario(nombre: str, apellidos: str, telefono: str, edad: int, rol_id: int):
    #Validar integridad referencial (¿Existe el rol_id?)
    rol_existente = any(r["id"] == rol_id for r in roles)
    if not rol_existente:
        raise HTTPException(status_code=400, detail="Error de llave Foránea: El rol_id no existe en la tabla roles.")
