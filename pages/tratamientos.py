import requests
import streamlit as st


def registrar_tratamiento():
    st.subheader("Registrar Nuevo Tratamiento")
    with st.form("formulario_tratamiento"):
        nombre = st.text_input("Nombre")
        descripcion = st.text_input("Descripción")
        precio_str = st.text_input("Precio")
        
        submitted = st.form_submit_button("Registrar Tratamiento")
        
        if submitted:
            if not nombre or not descripcion or not precio_str:
                st.error("Por favor, complete todos los campos")
                return
                
            try:
                # Convertir el precio a número
                precio = float(precio_str)
                
                tratamiento_data = {
                    "tratamientos": [{
                        "nombre": nombre,
                        "descripcion": descripcion,
                        "precio": precio
                    }]
                }
                
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/tratamientos/bulk/",
                        json=tratamiento_data
                    )
                    if response.status_code == 200:
                        st.success("Tratamiento registrado exitosamente")
                    else:
                        st.error(f"Error al registrar el tratamiento: {response.text}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
            except ValueError:
                st.error("Por favor, ingrese un precio válido")

def buscar_tratamiento():
    tratamiento_id = st.text_input("Buscar tratamiento por ID")
    if st.button("Buscar", key="buscar_tratamiento_tab2"):
        if tratamiento_id:
            try:
                response = requests.get(f"http://127.0.0.1:8000/tratamientos/{tratamiento_id}")
                if response.status_code == 200:
                    tratamiento = response.json()
                    st.write("### Detalles del Tratamiento")
                    st.write(f"**ID:** {tratamiento['id']}")
                    st.write(f"**Nombre:** {tratamiento['nombre']}")
                    st.write(f"**Descripción:** {tratamiento['descripcion']}")
                    st.write(f"**Precio:** ${tratamiento['precio']}")
                elif response.status_code == 404:
                    st.error("Tratamiento no encontrado")
                else:
                    st.error("Error al buscar el tratamiento")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
        else:
            st.warning("Por favor, ingrese un ID")

def ver_tratamientos():
    st.markdown("---")
    if st.button("Ver todos los tratamientos"):
        try:
            response = requests.get("http://127.0.0.1:8000/tratamientos/?skip=0&limit=100")
            if response.status_code == 200:
                tratamientos = response.json()
                if tratamientos:
                    tabla_tratamientos = []
                    for tratamiento in tratamientos:
                        tabla_tratamientos.append({
                            "ID": tratamiento['id'],
                            "Nombre": tratamiento['nombre'],
                            "Descripción": tratamiento['descripcion'],
                            "Precio": f"${tratamiento['precio']}"
                        })
                    st.table(tabla_tratamientos)
                else:
                    st.info("No hay tratamientos registrados")
            else:
                st.error("Error al obtener la lista de tratamientos")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def actualizar_tratamiento():
    st.subheader("Actualizar Tratamiento")
    
    tratamiento_id = st.text_input("ID del tratamiento")
    
    if tratamiento_id:
        response = requests.get(f"http://127.0.0.1:8000/tratamientos/{tratamiento_id}")
        
        if response.status_code == 200:
            tratamiento = response.json()
            
            # Campos para nuevos datos
            nuevo_nombre = st.text_input("Nombre:", tratamiento['nombre'])
            nueva_descripcion = st.text_input("Descripción:", tratamiento['descripcion'])
            nuevo_precio_str = st.text_input("Precio:", value=str(tratamiento['precio']))
            
            # Botón de actualizar
            if st.button("Actualizar"):
                try:
                    # Convertir el precio a número
                    nuevo_precio = float(nuevo_precio_str)
                    
                    # Preparar datos
                    datos_actualizados = {
                        "nombre": nuevo_nombre,
                        "descripcion": nueva_descripcion,
                        "precio": nuevo_precio
                    }
                    
                    # Enviar actualización
                    actualizar = requests.put(
                        f"http://127.0.0.1:8000/tratamientos/{tratamiento_id}",
                        json=datos_actualizados
                    )
                    
                    if actualizar.status_code == 200:
                        st.success("Actualizado correctamente")
                    else:
                        st.error("No se pudo actualizar")
                except ValueError:
                    st.error("Por favor, ingrese un precio válido")
        else:
            st.error(f"No se encontró el tratamiento con ID: {tratamiento_id}")

def eliminar_tratamiento():
    st.subheader("Eliminar Tratamiento")
    
    tratamiento_id = st.text_input("Ingrese el ID del tratamiento a eliminar")
    if tratamiento_id:
        try:
            # Primero verificamos si el tratamiento existe
            verify_response = requests.get(f"http://127.0.0.1:8000/tratamientos/{tratamiento_id}")
            if verify_response.status_code == 200:
                tratamiento = verify_response.json()
                st.write(f"Tratamiento a eliminar: {tratamiento['nombre']} - ${tratamiento['precio']}")
                
                if st.button("Confirmar Eliminación"):
                    # Intentamos eliminar el tratamiento
                    response = requests.delete(f"http://127.0.0.1:8000/tratamientos/{tratamiento_id}")
                    
                    if response.status_code == 200:
                        st.success("Tratamiento eliminado exitosamente")
                    else:
                        # Mostrar el mensaje de error del servidor
                        error_message = response.json().get("detail", "Error desconocido")
                        st.error(f"Error al eliminar el tratamiento: {error_message}")
            elif verify_response.status_code == 404:
                st.error("Tratamiento no encontrado")
            else:
                st.error("Error al buscar el tratamiento")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

def main():
    st.set_page_config(page_title="Gestión de Tratamientos", page_icon="💊")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Registrar Tratamiento", "Ver Tratamientos", "Actualizar Tratamiento", "Eliminar Tratamiento"])
    
    with tab1:
        registrar_tratamiento()
    
    with tab2:
        st.subheader("Lista de Tratamientos")
        buscar_tratamiento()
        ver_tratamientos()
    
    with tab3:
        actualizar_tratamiento()
    
    with tab4:
        eliminar_tratamiento()

if __name__ == "__main__":
    main() 