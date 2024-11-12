from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Schemas base (mantener los existentes)
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    fecha_nacimiento: datetime

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    class Config:
        orm_mode = True

class DoctorBase(BaseModel):
    nombre: str
    apellido: str
    especialidad: str
    email: str
    telefono: str

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int
    class Config:
        from_attributes = True

class TratamientoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float

class TratamientoCreate(TratamientoBase):
    pass

class Tratamiento(TratamientoBase):
    id: int
    class Config:
        from_attributes = True

class CitaBase(BaseModel):
    paciente_id: int
    doctor_id: int
    tratamiento_id: int
    fecha_hora: datetime
    estado: str = "programada"

class CitaCreate(CitaBase):
    pass

class Cita(CitaBase):
    id: int
    class Config:
        from_attributes = True

# Solo los schemas para bulk
class BulkPacientesCreate(BaseModel):
    pacientes: List[PacienteCreate]

class BulkDoctoresCreate(BaseModel):
    doctores: List[DoctorCreate]

class BulkTratamientosCreate(BaseModel):
    tratamientos: List[TratamientoCreate]

class BulkCitasCreate(BaseModel):
    citas: List[CitaCreate]