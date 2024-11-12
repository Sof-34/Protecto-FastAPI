import streamlit as st
import requests
from datetime import datetime

def obtener_nombre_paciente(paciente_id):
    response = requests.get(f"http://127.0.0.1:8000/pacientes/{paciente_id}")
    if response.status_code == 200:
        paciente = response.json()
        return f"{paciente['nombre']} {paciente['apellido']}"
    return "No encontrado"

def obtener_nombre_doctor(doctor_id):
    response = requests.get(f"http://127.0.0.1:8000/doctores/{doctor_id}")
    if response.status_code == 200:
        doctor = response.json()
        return f"{doctor['nombre']} {doctor['apellido']}"
    return "No encontrado"

def obtener_nombre_tratamiento(tratamiento_id):
    response = requests.get(f"http://127.0.0.1:8000/tratamientos/{tratamiento_id}")
    if response.status_code == 200:
        tratamiento = response.json()
        return tratamiento['nombre']
    return "No encontrado"

def validar_existencia(paciente_id, doctor_id, tratamiento_id):
    # Verificar paciente
    paciente_response = requests.get(f"http://127.0.0.1:8000/pacientes/{paciente_id}")
    if paciente_response.status_code != 200:
        st.error("El paciente especificado no existe")
        return False
    
    # Verificar doctor
    doctor_response = requests.get(f"http://127.0.0.1:8000/doctores/{doctor_id}")
    if doctor_response.status_code != 200:
        st.error("El doctor especificado no existe")
        return False
    
    # Verificar tratamiento
    tratamiento_response = requests.get(f"http://127.0.0.1:8000/tratamientos/{tratamiento_id}")
    if tratamiento_response.status_code != 200:
        st.error("El tratamiento especificado no existe")
        return False
    
    return True

def registrar_cita():
    st.subheader("Registrar Nueva Cita")
    with st.form("formulario_cita"):
        # Usando text_input en lugar de number_input para IDs
        paciente_id_str = st.text_input("ID del Paciente")
        doctor_id_str = st.text_input("ID del Doctor")
        tratamiento_id_str = st.text_input("ID del Tratamiento")
        
        fecha = st.date_input("Fecha")
        hora = st.time_input("Hora")
        fecha_hora = datetime.combine(fecha, hora).isoformat()
        estado = st.selectbox("Estado", ["", "programada", "completada", "cancelada"])
        
        submitted = st.form_submit_button("Registrar Cita")
        
        if submitted:
            if estado == "":
                st.error("Por favor seleccione un estado")
                return
            
            # Validar que los campos no estén vacíos
            if not paciente_id_str or not doctor_id_str or not tratamiento_id_str:
                st.error("Por favor, complete todos los campos")
                return
            
            try:
                # Convertir los IDs a enteros
                paciente_id = int(paciente_id_str)
                doctor_id = int(doctor_id_str)
                tratamiento_id = int(tratamiento_id_str)
                
                # Verificar que todos los IDs existan
                if validar_existencia(paciente_id, doctor_id, tratamiento_id):
                    cita_data = {
                        "citas": [{
                            "paciente_id": paciente_id,
                            "doctor_id": doctor_id,
                            "tratamiento_id": tratamiento_id,
                            "fecha_hora": fecha_hora,
                            "estado": estado
                        }]
                    }
                    
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/citas/bulk/",
                            json=cita_data
                        )
                        if response.status_code == 200:
                            st.success("Cita registrada exitosamente")
                        else:
                            st.error(f"Error al registrar la cita: {response.text}")
                    except Exception as e:
                        st.error(f"Error de conexión: {e}")
            except ValueError:
                st.error("Por favor, ingrese números válidos para los IDs")

def buscar_cita():
    cita_id = st.text_input("Buscar cita por ID")
    if st.button("Buscar", key="buscar_cita_tab2"):
        if cita_id:
            try:
                response = requests.get(f"http://127.0.0.1:8000/citas/{cita_id}")
                if response.status_code == 200:
                    cita = response.json()
                    
                    st.write("### Detalles de la Cita")
                    st.write(f"**ID de la Cita:** {cita['id']}")
                    st.write(f"**Paciente:** {obtener_nombre_paciente(cita['paciente_id'])}")
                    st.write(f"**Doctor:** {obtener_nombre_doctor(cita['doctor_id'])}")
                    st.write(f"**Tratamiento:** {obtener_nombre_tratamiento(cita['tratamiento_id'])}")
                    st.write(f"**Fecha y Hora:** {cita['fecha_hora']}")
                    st.write(f"**Estado:** {cita['estado']}")
                    
                else:
                    st.error("Cita no encontrada")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
        else:
            st.warning("Por favor, ingrese un ID")

def ver_citas():
    st.markdown("---")
    if st.button("Ver todas las citas"):
        try:
            response = requests.get("http://127.0.0.1:8000/citas/?skip=0&limit=100")
            if response.status_code == 200:
                citas = response.json()
                if citas:
                    tabla_citas = []
                    for cita in citas:
                        tabla_citas.append({
                            "ID": cita['id'],
                            "Paciente": obtener_nombre_paciente(cita['paciente_id']),
                            "Doctor": obtener_nombre_doctor(cita['doctor_id']),
                            "Tratamiento": obtener_nombre_tratamiento(cita['tratamiento_id']),
                            "Fecha y Hora": cita['fecha_hora'],
                            "Estado": cita['estado']
                        })
                    st.table(tabla_citas)
                else:
                    st.info("No hay citas registradas")
            else:
                st.error("Error al obtener la lista de citas")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def actualizar_cita():
    st.subheader("Actualizar Cita")
    cita_id = st.text_input("ID de la cita")
    
    if cita_id:
        try:
            response = requests.get(f"http://127.0.0.1:8000/citas/{cita_id}")
            if response.status_code == 200:
                cita = response.json()
                
                # Mostrar información actual
                st.write("### Información Actual:")
                st.write(f"**Paciente actual:** {obtener_nombre_paciente(cita['paciente_id'])}")
                st.write(f"**Doctor actual:** {obtener_nombre_doctor(cita['doctor_id'])}")
                st.write(f"**Tratamiento actual:** {obtener_nombre_tratamiento(cita['tratamiento_id'])}")
                
                st.write("### Actualizar información:")
                nuevo_paciente_id_str = st.text_input("ID del Paciente:", value=str(cita['paciente_id']))
                nuevo_doctor_id_str = st.text_input("ID del Doctor:", value=str(cita['doctor_id']))
                nuevo_tratamiento_id_str = st.text_input("ID del Tratamiento:", value=str(cita['tratamiento_id']))
                
                fecha_hora_actual = datetime.fromisoformat(cita['fecha_hora'].replace('Z', '+00:00'))
                nueva_fecha = st.date_input("Fecha:", value=fecha_hora_actual.date())
                nueva_hora = st.time_input("Hora:", value=fecha_hora_actual.time())
                
                nuevo_estado = st.selectbox("Estado:", ["programada", "completada", "cancelada"], 
                                          index=["programada", "completada", "cancelada"].index(cita['estado']))
                
                if st.button("Actualizar"):
                    try:
                        # Convertir los IDs a enteros
                        nuevo_paciente_id = int(nuevo_paciente_id_str)
                        nuevo_doctor_id = int(nuevo_doctor_id_str)
                        nuevo_tratamiento_id = int(nuevo_tratamiento_id_str)
                        
                        if validar_existencia(nuevo_paciente_id, nuevo_doctor_id, nuevo_tratamiento_id):
                            nueva_fecha_hora = datetime.combine(nueva_fecha, nueva_hora).isoformat()
                            datos_actualizados = {
                                "paciente_id": nuevo_paciente_id,
                                "doctor_id": nuevo_doctor_id,
                                "tratamiento_id": nuevo_tratamiento_id,
                                "fecha_hora": nueva_fecha_hora,
                                "estado": nuevo_estado
                            }
                            
                            actualizar = requests.put(
                                f"http://127.0.0.1:8000/citas/{cita_id}",
                                json=datos_actualizados
                            )
                            
                            if actualizar.status_code == 200:
                                st.success("Actualizado correctamente")
                            else:
                                st.error("No se pudo actualizar")
                    except ValueError:
                        st.error("Por favor, ingrese números válidos para los IDs")
            else:
                st.error(f"No se encontró la cita con ID: {cita_id}")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def eliminar_cita():
    st.subheader("Eliminar Cita")
    cita_id = st.text_input("Ingrese el ID de la cita a eliminar")
    
    if cita_id:
        try:
            verify_response = requests.get(f"http://127.0.0.1:8000/citas/{cita_id}")
            if verify_response.status_code == 200:
                cita = verify_response.json()
                st.write(f"Cita a eliminar: ID {cita['id']} - Fecha: {cita['fecha_hora']}")
                
                if st.button("Confirmar Eliminación"):
                    response = requests.delete(f"http://127.0.0.1:8000/citas/{cita_id}")
                    if response.status_code == 200:
                        st.success("Cita eliminada exitosamente")
                    else:
                        st.error("Error al eliminar la cita")
            else:
                st.error("Cita no encontrada")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def main():
    st.set_page_config(page_title="Gestión de Citas", page_icon="📅")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Registrar Cita", "Ver Citas", "Actualizar Cita", "Eliminar Cita"])
    
    with tab1:
        registrar_cita()
    
    with tab2:
        st.subheader("Lista de Citas")
        buscar_cita()
        ver_citas()
    
    with tab3:
        actualizar_cita()
    
    with tab4:
        eliminar_cita()

if __name__ == "__main__":
    main() 