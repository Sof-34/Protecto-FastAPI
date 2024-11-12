from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


# Operaciones CRUD para Pacientes
def get_paciente(db: Session, paciente_id: int):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

def get_pacientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paciente).offset(skip).limit(limit).all()

def update_paciente(db: Session, paciente_id: int, paciente: schemas.PacienteCreate):
    db_paciente = get_paciente(db, paciente_id)
    for key, value in paciente.dict().items():
        setattr(db_paciente, key, value)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def delete_paciente(db: Session, paciente_id: int):
    paciente = get_paciente(db, paciente_id)
    citas = db.query(models.Cita).filter(models.Cita.paciente_id == paciente_id).all()
    for cita in citas:
        db.delete(cita)
    db.delete(paciente)
    db.commit()
    return {"message": f"Paciente con ID {paciente_id} y sus {len(citas)} citas asociadas fueron eliminados exitosamente"}

def create_pacientes_bulk(db: Session, bulk_pacientes: schemas.BulkPacientesCreate):
    db_pacientes = []
    for paciente in bulk_pacientes.pacientes:
        db_paciente = models.Paciente(**paciente.dict())
        db.add(db_paciente)
        db_pacientes.append(db_paciente)
    
    db.commit()
    for paciente in db_pacientes:
        db.refresh(paciente)
    return db_pacientes

# Operaciones CRUD para Doctores
def get_doctor(db: Session, doctor_id: int):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return doctor

def get_doctores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Doctor).offset(skip).limit(limit).all()

def update_doctor(db: Session, doctor_id: int, doctor: schemas.DoctorCreate):
    db_doctor = get_doctor(db, doctor_id)
    for key, value in doctor.dict().items():
        setattr(db_doctor, key, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor eliminado exitosamente"}

def create_doctores_bulk(db: Session, bulk_doctores: schemas.BulkDoctoresCreate):
    db_doctores = []
    for doctor in bulk_doctores.doctores:
        db_doctor = models.Doctor(**doctor.dict())
        db.add(db_doctor)
        db_doctores.append(db_doctor)
    
    db.commit()
    for doctor in db_doctores:
        db.refresh(doctor)
    return db_doctores

# Operaciones CRUD para Citas
def get_cita(db: Session, cita_id: int):
    cita = db.query(models.Cita).filter(models.Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

def get_citas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cita).offset(skip).limit(limit).all()

def update_cita(db: Session, cita_id: int, cita: schemas.CitaCreate):
    db_cita = get_cita(db, cita_id)
    
    # Verificar que existan las relaciones
    if not db.query(models.Paciente).filter(models.Paciente.id == cita.paciente_id).first():
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    if not db.query(models.Doctor).filter(models.Doctor.id == cita.doctor_id).first():
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    if not db.query(models.Tratamiento).filter(models.Tratamiento.id == cita.tratamiento_id).first():
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")

    for key, value in cita.dict().items():
        setattr(db_cita, key, value)
    db.commit()
    db.refresh(db_cita)
    return db_cita

def delete_cita(db: Session, cita_id: int):
    cita = get_cita(db, cita_id)
    db.delete(cita)
    db.commit()
    return {"message": "Cita eliminada exitosamente"}

def create_citas_bulk(db: Session, bulk_citas: schemas.BulkCitasCreate):
    db_citas = []
    for cita in bulk_citas.citas:
        # Verificar que existan las relaciones para cada cita
        if not db.query(models.Paciente).filter(models.Paciente.id == cita.paciente_id).first():
            raise HTTPException(status_code=404, detail=f"Paciente {cita.paciente_id} no encontrado")
        if not db.query(models.Doctor).filter(models.Doctor.id == cita.doctor_id).first():
            raise HTTPException(status_code=404, detail=f"Doctor {cita.doctor_id} no encontrado")
        if not db.query(models.Tratamiento).filter(models.Tratamiento.id == cita.tratamiento_id).first():
            raise HTTPException(status_code=404, detail=f"Tratamiento {cita.tratamiento_id} no encontrado")
            
        db_cita = models.Cita(**cita.dict())
        db.add(db_cita)
        db_citas.append(db_cita)
    
    db.commit()
    for cita in db_citas:
        db.refresh(cita)
    return db_citas

# Operaciones CRUD para Tratamientos
def get_tratamiento(db: Session, tratamiento_id: int):
    tratamiento = db.query(models.Tratamiento).filter(models.Tratamiento.id == tratamiento_id).first()
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tratamiento

def get_tratamientos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tratamiento).offset(skip).limit(limit).all()

def update_tratamiento(db: Session, tratamiento_id: int, tratamiento: schemas.TratamientoCreate):
    db_tratamiento = get_tratamiento(db, tratamiento_id)
    for key, value in tratamiento.dict().items():
        setattr(db_tratamiento, key, value)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

def delete_tratamiento(db: Session, tratamiento_id: int):
    # Obtener todas las citas asociadas al tratamiento
    citas_asociadas = db.query(models.Cita).filter(models.Cita.tratamiento_id == tratamiento_id).all()
    
    # Eliminar las citas asociadas
    for cita in citas_asociadas:
        db.delete(cita)
    
    # Ahora eliminar el tratamiento
    tratamiento = get_tratamiento(db, tratamiento_id)
    db.delete(tratamiento)
    db.commit()
    
    return {"message": "Tratamiento eliminado exitosamente"}

def create_tratamientos_bulk(db: Session, bulk_tratamientos: schemas.BulkTratamientosCreate):
    db_tratamientos = []
    for tratamiento in bulk_tratamientos.tratamientos:
        db_tratamiento = models.Tratamiento(**tratamiento.dict())
        db.add(db_tratamiento)
        db_tratamientos.append(db_tratamiento)
    
    db.commit()
    for tratamiento in db_tratamientos:
        db.refresh(tratamiento)
    return db_tratamientos