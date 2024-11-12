import streamlit as st
import requests

def registrar_doctor():
    st.subheader("Registrar Nuevo Doctor")
    with st.form("formulario_doctor"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        especialidad = st.text_input("Especialidad")
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        
        submitted = st.form_submit_button("Registrar Doctor")
        
        if submitted:
            doctor_data = {
                "doctores": [{
                    "nombre": nombre,
                    "apellido": apellido,
                    "especialidad": especialidad,
                    "email": email,
                    "telefono": telefono
                }]
            }
            
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/doctores/bulk/",
                    json=doctor_data
                )
                if response.status_code == 200:
                    st.success("Doctor registrado exitosamente")
                else:
                    st.error(f"Error al registrar el doctor: {response.text}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")

def buscar_doctor():
    doctor_id = st.text_input("Buscar doctor por ID")
    if st.button("Buscar", key="buscar_doctor_tab2"):
        if doctor_id:
            try:
                response = requests.get(f"http://127.0.0.1:8000/doctores/{doctor_id}")
                if response.status_code == 200:
                    doctor = response.json()
                    st.write("### Detalles del Doctor")
                    st.write(f"**ID:** {doctor['id']}")
                    st.write(f"**Nombre:** {doctor['nombre']} {doctor['apellido']}")
                    st.write(f"**Especialidad:** {doctor['especialidad']}")
                    st.write(f"**Email:** {doctor['email']}")
                    st.write(f"**Teléfono:** {doctor['telefono']}")
                elif response.status_code == 404:
                    st.error("Doctor no encontrado")
                else:
                    st.error("Error al buscar el doctor")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
        else:
            st.warning("Por favor, ingrese un ID")

def ver_doctores():
    st.markdown("---")
    if st.button("Ver todos los doctores"):
        try:
            response = requests.get("http://127.0.0.1:8000/doctores/")
            if response.status_code == 200:
                doctores = response.json()
                if doctores:
                    tabla_doctores = []
                    for doctor in doctores:
                        tabla_doctores.append({
                            "ID": doctor['id'],
                            "Nombre": doctor['nombre'],
                            "Apellido": doctor['apellido'],
                            "Especialidad": doctor['especialidad'],
                            "Email": doctor['email'],
                            "Teléfono": doctor['telefono']
                        })
                    st.table(tabla_doctores)
                else:
                    st.info("No hay doctores registrados")
            else:
                st.error("Error al obtener la lista de doctores")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def actualizar_doctor():
    st.subheader("Actualizar Doctor")
    
    # Input para ID
    doctor_id = st.text_input(" ID del doctor")
    
    # Solo mostrar el resto si hay un ID ingresado
    if doctor_id:
        # Obtener datos actuales del doctor
        response = requests.get(f"http://127.0.0.1:8000/doctores/{doctor_id}")
        
        if response.status_code == 200:
            doctor = response.json()
            
            # Campos para nuevos datos
            nuevo_nombre = st.text_input("Nombre:", doctor['nombre'])
            nuevo_apellido = st.text_input("Apellido:", doctor['apellido'])
            nueva_especialidad = st.text_input("Especialidad:", doctor['especialidad'])
            nuevo_email = st.text_input("Email:", doctor['email'])
            nuevo_telefono = st.text_input("Teléfono:", doctor['telefono'])
            
            # Botón de actualizar
            if st.button("Actualizar"):
                # Preparar datos
                datos_actualizados = {
                    "nombre": nuevo_nombre,
                    "apellido": nuevo_apellido,
                    "especialidad": nueva_especialidad,
                    "email": nuevo_email,
                    "telefono": nuevo_telefono
                }
                
                # Enviar actualización
                actualizar = requests.put(
                    f"http://127.0.0.1:8000/doctores/{doctor_id}",
                    json=datos_actualizados
                )
                
                # Solo mostrar mensaje de éxito
                if actualizar.status_code == 200:
                    st.success("Actualizado correctamente")
                else:
                    st.error("No se pudo actualizar")
        
        else:
            st.error(f"No se encontró el doctor con ID: {doctor_id}")

def eliminar_doctor():
    st.subheader("Eliminar Doctor")
    
    doctor_id = st.text_input("Ingrese el ID del doctor a eliminar")
    if doctor_id:
        try:
            # Primero verificamos si el doctor existe
            verify_response = requests.get(f"http://127.0.0.1:8000/doctores/{doctor_id}")
            if verify_response.status_code == 200:
                doctor = verify_response.json()
                st.write(f"Doctor a eliminar: {doctor['nombre']} {doctor['apellido']}")
                
                if st.button("Confirmar Eliminación"):
                    response = requests.delete(f"http://127.0.0.1:8000/doctores/{doctor_id}")
                    if response.status_code == 200:
                        st.success("Doctor eliminado exitosamente")
                    else:
                        st.error("Error al eliminar el doctor")
            elif verify_response.status_code == 404:
                st.error("Doctor no encontrado")
            else:
                st.error("Error al buscar el doctor")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def main():
    st.set_page_config(page_title="Gestión de Doctores", page_icon="🏥")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Registrar Doctor", "Ver Doctores", "Actualizar Doctor", "Eliminar Doctor"])
    
    with tab1:
        registrar_doctor()
    
    with tab2:
        st.subheader("Lista de Doctores")
        buscar_doctor()
        ver_doctores()
    
    with tab3:
        actualizar_doctor()
    
    with tab4:
        eliminar_doctor()

if __name__ == "__main__":
    main()