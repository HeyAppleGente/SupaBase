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
    nuevo_id=len(usuarios) + 1
    nuevo_usuario ={
        "id": nuevo_id,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "edad": edad,
        "rol_id": rol_id
    }
    usuarios.append(nuevo_usuario)
    return nuevo_usuario

# --- ENDPOINTS TABLA: PROGRAMAS ---
@app.get("/programas")
def listar_programas():
    return programas

@app.post("/programas")
def crear_programa(nombre: str, codigo: str):
    nuevo_id = len(programas) + 1
    nuevo_prog = {"id": nuevo_id, "nombre": nombre, "codigo": codigo}
    programas.append(nuevo_prog)
    return nuevo_prog

# --- ENDPOINTS TABLA: MATRICULAS (Valida FKs usuario_id y programa_id) ---
@app.get("/matriculas")
def listar_matriculas():
    resultado = []
    for m in matriculas:
        usr = next((u for u in usuarios if u["id"] == m["usuario_id"]), None)
        prog = next((p for p in programas if p["id"] == m["programa_id"]), None)
        resultado.append({
            "id": m["id"],
            "fecha_matricula": m["fecha_matricula"],
            "usuario": usr,
            "programa": prog
        })
    return resultado

@app.post("/matriculas")
def crear_matricula(usuario_id: int, programa_id: int, fecha_matricula: str):
    # Validar integridad referencial de ambas llaves foráneas
    usr_existente = any(u["id"] == usuario_id for u in usuarios)
    prog_existente = any(p["id"] == programa_id for p in programas)
    
    if not usr_existente:
        raise HTTPException(status_code=400, detail="FK Error: El usuario_id no existe.")
    if not prog_existente:
        raise HTTPException(status_code=400, detail="FK Error: El programa_id no existe.")
        
    nuevo_id = len(matriculas) + 1
    nueva_mat = {
        "id": nuevo_id,
        "usuario_id": usuario_id,
        "programa_id": programa_id,
        "fecha_matricula": fecha_matricula
    }
    matriculas.append(nueva_mat)
    return nueva_mat

# --- ENDPOINTS TABLA: ASISTENCIAS (Valida FK matricula_id) ---
@app.get("/asistencias")
def listar_asistencias():
    return asistencias

@app.post("/asistencias")
def registrar_asistencia(matricula_id: int, fecha: str, estado: str):
    # Validar que exista la matrícula correspondiente
    mat_existente = any(m["id"] == matricula_id for m in matriculas)
    if not mat_existente:
        raise HTTPException(status_code=400, detail="FK Error: La matricula_id no existe.")
    
    nuevo_id = len(asistencias) + 1
    nueva_asistencia = {
        "id": nuevo_id,
        "matricula_id": matricula_id,
        "fecha": fecha,
        "estado": estado
    }
    asistencias.append(nueva_asistencia)
    return nueva_asistencia
