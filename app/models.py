from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    fecha_nacimiento = Column(DateTime, nullable=False)
    
    citas = relationship("Cita", back_populates="paciente")

class Doctor(Base):
    __tablename__ = "doctores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    especialidad = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    
    citas = relationship("Cita", back_populates="doctor")

class Tratamiento(Base):
    __tablename__ = "tratamientos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    precio = Column(Float, nullable=False)
    
    citas = relationship("Cita", back_populates="tratamiento")

class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctores.id"), nullable=False)
    tratamiento_id = Column(Integer, ForeignKey("tratamientos.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String(20), nullable=False, default="programada")
    
    paciente = relationship("Paciente", back_populates="citas")
    doctor = relationship("Doctor", back_populates="citas")
    tratamiento = relationship("Tratamiento", back_populates="citas") 