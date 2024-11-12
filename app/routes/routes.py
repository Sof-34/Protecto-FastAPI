from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

# Rutas para Pacientes
@router.post("/pacientes/bulk/", response_model=List[schemas.Paciente], tags=["Pacientes"])
def create_pacientes_bulk(bulk_pacientes: schemas.BulkPacientesCreate, db: Session = Depends(get_db)):
    return crud.create_pacientes_bulk(db=db, bulk_pacientes=bulk_pacientes)

@router.get("/pacientes/", response_model=List[schemas.Paciente], tags=["Pacientes"])
def read_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pacientes(db, skip=skip, limit=limit)

@router.get("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def read_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return crud.get_paciente(db, paciente_id=paciente_id)

@router.put("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def update_paciente(paciente_id: int, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.update_paciente(db=db, paciente_id=paciente_id, paciente=paciente)

@router.delete("/pacientes/{paciente_id}", tags=["Pacientes"])
def delete_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return crud.delete_paciente(db=db, paciente_id=paciente_id)

# Rutas para Doctores
@router.post("/doctores/bulk/", response_model=List[schemas.Doctor], tags=["Doctores"])
def create_doctores_bulk(bulk_doctores: schemas.BulkDoctoresCreate, db: Session = Depends(get_db)):
    return crud.create_doctores_bulk(db=db, bulk_doctores=bulk_doctores)

@router.get("/doctores/", response_model=List[schemas.Doctor], tags=["Doctores"])
def read_doctores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_doctores(db, skip=skip, limit=limit)

@router.get("/doctores/{doctor_id}", response_model=schemas.Doctor, tags=["Doctores"])
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return crud.get_doctor(db, doctor_id=doctor_id)

@router.put("/doctores/{doctor_id}", response_model=schemas.Doctor, tags=["Doctores"])
def update_doctor(doctor_id: int, doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.update_doctor(db=db, doctor_id=doctor_id, doctor=doctor)

@router.delete("/doctores/{doctor_id}", tags=["Doctores"])
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return crud.delete_doctor(db=db, doctor_id=doctor_id)

# Rutas para Tratamientos
@router.post("/tratamientos/bulk/", response_model=List[schemas.Tratamiento], tags=["Tratamientos"])
def create_tratamientos_bulk(bulk_tratamientos: schemas.BulkTratamientosCreate, db: Session = Depends(get_db)):
    return crud.create_tratamientos_bulk(db=db, bulk_tratamientos=bulk_tratamientos)

@router.get("/tratamientos/", response_model=List[schemas.Tratamiento], tags=["Tratamientos"])
def read_tratamientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tratamientos(db, skip=skip, limit=limit)

@router.get("/tratamientos/{tratamiento_id}", response_model=schemas.Tratamiento, tags=["Tratamientos"])
def read_tratamiento(tratamiento_id: int, db: Session = Depends(get_db)):
    return crud.get_tratamiento(db, tratamiento_id=tratamiento_id)

@router.put("/tratamientos/{tratamiento_id}", response_model=schemas.Tratamiento, tags=["Tratamientos"])
def update_tratamiento(tratamiento_id: int, tratamiento: schemas.TratamientoCreate, db: Session = Depends(get_db)):
    return crud.update_tratamiento(db=db, tratamiento_id=tratamiento_id, tratamiento=tratamiento)

@router.delete("/tratamientos/{tratamiento_id}", tags=["Tratamientos"])
def delete_tratamiento(tratamiento_id: int, db: Session = Depends(get_db)):
    return crud.delete_tratamiento(db=db, tratamiento_id=tratamiento_id)

# Rutas para Citas
@router.post("/citas/bulk/", response_model=List[schemas.Cita], tags=["Citas"])
def create_citas_bulk(bulk_citas: schemas.BulkCitasCreate, db: Session = Depends(get_db)):
    return crud.create_citas_bulk(db=db, bulk_citas=bulk_citas)

@router.get("/citas/", response_model=List[schemas.Cita], tags=["Citas"])
def read_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_citas(db, skip=skip, limit=limit)

@router.get("/citas/{cita_id}", response_model=schemas.Cita, tags=["Citas"])
def read_cita(cita_id: int, db: Session = Depends(get_db)):
    return crud.get_cita(db, cita_id=cita_id)

@router.put("/citas/{cita_id}", response_model=schemas.Cita, tags=["Citas"])
def update_cita(cita_id: int, cita: schemas.CitaCreate, db: Session = Depends(get_db)):
    return crud.update_cita(db=db, cita_id=cita_id, cita=cita)

@router.delete("/citas/{cita_id}", tags=["Citas"])
def delete_cita(cita_id: int, db: Session = Depends(get_db)):
    return crud.delete_cita(db=db, cita_id=cita_id)