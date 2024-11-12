from fastapi import FastAPI
from .routes import routes

app = FastAPI(
    title="Sistema de Gestión de Clínica Dental",
    description="¡Bienvenido a la API de Clínica Dental!"
)

@app.get("/", include_in_schema=False)
def root():
    return {"mensaje": "¡Bienvenido a la API de Clínica Dental!"}

# Incluir todas las rutas
app.include_router(routes.router)