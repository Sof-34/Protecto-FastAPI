from datetime import datetime

import requests
import streamlit as st
import pandas as pd


def registrar_paciente():
    st.subheader("Registrar Nuevo Paciente")
    with st.form("formulario_paciente"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        fecha_nacimiento = st.date_input("Fecha de Nacimiento")
        
        submitted = st.form_submit_button("Registrar Paciente")
        
        if submitted:
            paciente_data = {
                "pacientes": [{
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": email,
                    "telefono": telefono,
                    "fecha_nacimiento": str(fecha_nacimiento)
                }]
            }
            
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/pacientes/bulk/",
                    json=paciente_data
                )
                if response.status_code == 200:
                    st.success("Paciente registrado exitosamente")
                else:
                    st.error(f"Error al registrar el paciente: {response.text}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")

def buscar_paciente():
    paciente_id = st.text_input("Buscar paciente por ID")
    if st.button("Buscar", key="buscar_paciente_tab2"):
        if paciente_id:
            try:
                response = requests.get(f"http://127.0.0.1:8000/pacientes/{paciente_id}")
                if response.status_code == 200:
                    paciente = response.json()
                    st.write("### Detalles del Paciente")
                    st.write(f"**ID:** {paciente['id']}")
                    st.write(f"**Nombre:** {paciente['nombre']} {paciente['apellido']}")
                    st.write(f"**Email:** {paciente['email']}")
                    st.write(f"**Teléfono:** {paciente['telefono']}")
                    st.write(f"**Fecha de Nacimiento:** {paciente['fecha_nacimiento']}")
                elif response.status_code == 404:
                    st.error("Paciente no encontrado")
                else:
                    st.error("Error al buscar el paciente")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
        else:
            st.warning("Por favor, ingrese un ID")

def ver_pacientes():
    st.markdown("---")
    if st.button("Ver todos los pacientes"):
        try:
            response = requests.get("http://127.0.0.1:8000/pacientes/")
            if response.status_code == 200:
                pacientes = response.json()
                if pacientes:
                    tabla_pacientes = []
                    for paciente in pacientes:
                        tabla_pacientes.append({
                            "ID": paciente['id'],
                            "Nombre": paciente['nombre'],
                            "Apellido": paciente['apellido'],
                            "Email": paciente['email'],
                            "Teléfono": paciente['telefono'],
                            "Fecha Nacimiento": paciente['fecha_nacimiento']
                        })
                    st.table(tabla_pacientes)
                else:
                    st.info("No hay pacientes registrados")
            else:
                st.error("Error al obtener la lista de pacientes")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def actualizar_paciente():
    st.subheader("Actualizar Paciente")
    
    # Input para ID
    paciente_id = st.text_input(" ID del paciente")
    
    # Solo mostrar el resto si hay un ID ingresado
    if paciente_id:
        # Obtener datos actuales del paciente
        response = requests.get(f"http://127.0.0.1:8000/pacientes/{paciente_id}")
        
        if response.status_code == 200:
            paciente = response.json()
            
            # Campos para nuevos datos
            nuevo_nombre = st.text_input("Nombre:", paciente['nombre'])
            nuevo_apellido = st.text_input("Apellido:", paciente['apellido'])
            nuevo_email = st.text_input("Email:", paciente['email'])
            nuevo_telefono = st.text_input("Teléfono:", paciente['telefono'])
            
            # Manejo de la fecha
            fecha_str = paciente["fecha_nacimiento"].split('T')[0]
            fecha_actual = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            nueva_fecha = st.date_input("Fecha de Nacimiento:", fecha_actual)
            
            # Botón de actualizar
            if st.button("Actualizar"):
                # Preparar datos
                datos_actualizados = {
                    "nombre": nuevo_nombre,
                    "apellido": nuevo_apellido,
                    "email": nuevo_email,
                    "telefono": nuevo_telefono,
                    "fecha_nacimiento": str(nueva_fecha)
                }
                
                # Enviar actualización
                actualizar = requests.put(
                    f"http://127.0.0.1:8000/pacientes/{paciente_id}",
                    json=datos_actualizados
                )
                
                # Solo mostrar mensaje de éxito
                if actualizar.status_code == 200:
                    st.success("Actualizado correctamente")
                else:
                    st.error("No se pudo actualizar")
        
        else:
            st.error(f"No se encontró el paciente con ID: {paciente_id}")

def eliminar_paciente():
    st.subheader("Eliminar Paciente")
    
    paciente_id = st.text_input("Ingrese el ID del paciente a eliminar")
    if paciente_id:
        try:
            # Primero verificamos si el paciente existe
            verify_response = requests.get(f"http://127.0.0.1:8000/pacientes/{paciente_id}")
            if verify_response.status_code == 200:
                paciente = verify_response.json()
                st.write(f"Paciente a eliminar: {paciente['nombre']} {paciente['apellido']}")
                
                if st.button("Confirmar Eliminación"):
                    response = requests.delete(f"http://127.0.0.1:8000/pacientes/{paciente_id}")
                    if response.status_code == 200:
                        st.success("Paciente eliminado exitosamente")
                    else:
                        st.error("Error al eliminar el paciente")
            elif verify_response.status_code == 404:
                st.error("Paciente no encontrado")
            else:
                st.error("Error al buscar el paciente")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def cargar_pacientes_masivos():
    st.title("Carga Masiva de Pacientes")

    # Widget para subir archivo
    archivo_csv = st.file_uploader("Selecciona el archivo CSV", type=['csv'])

    if archivo_csv is not None:
        try:
            # Leer el archivo CSV
            df = pd.read_csv(archivo_csv)
            
            # Verificar que el CSV tenga las columnas requeridas
            columnas_requeridas = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento']
            if not all(columna in df.columns for columna in columnas_requeridas):
                st.error("El archivo CSV debe contener las columnas: nombre, apellido, email, telefono, fecha_nacimiento")
            else:
                # Mostrar preview de los datos
                st.write("Preview de los datos:")
                st.dataframe(df.head())
                
                if st.button("Cargar Pacientes"):
                    # Preparar datos para la API
                    pacientes = []
                    for _, row in df.iterrows():
                        paciente = {
                            "nombre": str(row['nombre']).strip(),
                            "apellido": str(row['apellido']).strip(),
                            "email": str(row['email']).strip(),
                            "telefono": str(row['telefono']).strip(),
                            "fecha_nacimiento": str(row['fecha_nacimiento']).strip()
                        }
                        pacientes.append(paciente)
                    
                    payload = {"pacientes": pacientes}
                    
                    # Realizar la petición POST
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/pacientes/bulk/",
                            json=payload
                        )
                        
                        if response.status_code == 200:
                            st.success(f"Se cargaron {len(pacientes)} pacientes exitosamente!")
                            
                            # Mostrar detalles de los pacientes creados
                            st.write("Pacientes creados:")
                            df_creados = pd.DataFrame(pacientes)
                            st.dataframe(df_creados)
                        else:
                            st.error(f"Error al cargar los pacientes. Código de estado: {response.status_code}")
                            st.error(f"Detalle del error: {response.text}")
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error de conexión: {str(e)}")
        
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

def main():
    st.set_page_config(page_title="Gestión de Pacientes", page_icon="🏥")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Registrar Paciente", 
        "Ver Pacientes", 
        "Actualizar Paciente", 
        "Eliminar Paciente",
        "Carga Masiva"
    ])
    
    with tab1:
        registrar_paciente()
    
    with tab2:
        st.subheader("Lista de Pacientes")
        buscar_paciente()
        ver_pacientes()
    
    with tab3:
        actualizar_paciente()
    
    with tab4:
        eliminar_paciente()
        
    with tab5:
        cargar_pacientes_masivos()

if __name__ == "__main__":
    main()