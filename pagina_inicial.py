import streamlit as st

def pagina_inicial():
    st.title("AFK")

    # Seção 1
    st.header("Criatividade sem Limites")
    st.write(""" 
    Na **AFK**, nosso aplicativo permite que pessoas com deficiências motoras criem arte de forma intuitiva 
    através de gestos simples capturados pela câmera. Utilizando a tecnologia do **Python MediaPipe**, 
    os movimentos das mãos são traduzidos em linhas, formas e cores diretamente na tela. 
    A interface é projetada para ser acessível, permitindo ajustes de pincéis, cores e efeitos de forma prática, 
    proporcionando uma experiência artística inclusiva e inovadora.
    """)

    # Seção 2
    st.header("Por que Escolher a AFK?")
    st.write(""" 
    Nosso compromisso é com a inclusão e a criatividade. Com a **AFK**, você pode explorar um mundo de arte digital, 
    independentemente de suas limitações motoras. 
    Desenvolvemos uma plataforma que coloca o poder da criação nas suas mãos, literalmente, sem complicações.
    """)

if __name__ == "__main__":
    pagina_inicial()
