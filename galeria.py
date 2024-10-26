import streamlit as st
import os

# Modifique isso no seu código galeria.py

def galeria_page():
    st.title("Galeria de Desenhos")

    galeria_dir = "galeria"  # Define o diretório da galeria

    # Verifica se há imagens salvas
    if "saved_images" in st.session_state and st.session_state.saved_images:
        st.subheader("Desenhos Salvos:")
        for img_path in st.session_state.saved_images:
            st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
    else:
        st.write("Nenhum desenho salvo ainda.")
