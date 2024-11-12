import streamlit as st

def main():
    st.set_page_config(
        page_title="Sistema Clínica Dental",
        page_icon="🦷",
       
    )
    
    st.title(" Bienvenido Al Sistema Administrativo De La Clínica Dental Care🦷")
    st.write("Seleccione una opción del menú lateral para gestionar pacientes,doctores,tratamientos o citas.")

if __name__ == "__main__":
    main()