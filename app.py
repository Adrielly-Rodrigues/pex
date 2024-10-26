import streamlit as st
import json
import pagina_inicial  # Atualiza para importar a página principal diretamente
import jogo_boxe
import jogo_reacao  # Importa o jogo de reação

# Configuração da página com favicon
st.set_page_config(
    page_title="AFK Tecnologia",  # Título da aba do navegador
    page_icon="afk.png",  # Caminho para a imagem do favicon
    layout="wide"  # Layout da página, pode ser "centered" ou "wide"
)

# Função para carregar dados de usuários de um arquivo JSON
def load_users():
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users

# Função para verificar login
def login(username, password):
    users = load_users()
    if username in users and users[username]["senha"] == password:
        return users[username]
    return None

# Função de Logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = "Página Inicial"  # Reseta a página após logout
    st.experimental_rerun()  # Atualiza a página

# Interface de Login
def login_page():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        user_data = login(username, password)
        if user_data:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user_data["role"]
            st.success(f"Bem-vindo, {username}!")
            st.experimental_rerun()  # Atualiza a página
        else:
            st.error("Usuário ou senha incorretos")

# Função principal que redireciona para outras páginas
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.page = "Página Inicial"  # Define a página inicial por padrão

    # Exibir o menu
    show_menu()  # Chama a função do menu

    if st.session_state.logged_in:
        # Redirecionamento com base na página selecionada
        if "page" in st.session_state:
            if st.session_state.page == "Página Inicial":
                pagina_inicial.pagina_inicial()
            elif st.session_state.page == "Configurações":
                import configuracao
                configuracao.config_page()
            elif st.session_state.page == "Usuários" and st.session_state.role == "admin":
                import lista_usuarios
                lista_usuarios.admin_users_page()
            elif st.session_state.page == "Desenhar":
                import desenhar
                desenhar.desenhar_page()
            elif st.session_state.page == "Jogo Boxe":
                jogo_boxe.main()  # Chama a função 'main' do arquivo jogo_boxe.py
            elif st.session_state.page == "Jogo Reação":  # Adiciona o jogo de reação
                jogo_reacao.main()  # Chama a função 'main' do arquivo jogo_reacao.py
            elif st.session_state.page == "Galeria":
                import galeria
                galeria.galeria_page()
            elif st.session_state.page == "Logout":
                logout()
    else:
        # Se não está logado, permite acesso às páginas sem login
        if "page" in st.session_state:
            if st.session_state.page == "Página Inicial":
                pagina_inicial.pagina_inicial()
            elif st.session_state.page == "Configurações":
                import configuracao
                configuracao.config_page()
            elif st.session_state.page == "Desenhar":
                import desenhar
                desenhar.desenhar_page()
            elif st.session_state.page == "Galeria":
                import galeria
                galeria.galeria_page()

        login_page()

def show_menu():
    st.sidebar.title("Menu")

    # Menu de navegação com botões
    if st.sidebar.button("🏠 Página Inicial"):
        st.session_state.page = "Página Inicial"

    if st.sidebar.button("⚙️ Configurações"):
        st.session_state.page = "Configurações"

    if st.sidebar.button("✏️ Desenhar"):
        st.session_state.page = "Desenhar"

    if st.sidebar.button("🥊 Jogo Boxe"):  # Certifique-se que o botão está corretamente chamando a página do jogo
        st.session_state.page = "Jogo Boxe" 
    
    if st.sidebar.button("🎯 Jogo Reação"):  # Botão para o jogo de reação
        st.session_state.page = "Jogo Reação"  # Define a página para o jogo de reação

    if st.sidebar.button("🖼️ Galeria"):
        st.session_state.page = "Galeria"

    if st.session_state.logged_in and st.session_state.role == "admin":  # Exibe "Usuários" apenas para o admin
        if st.sidebar.button("👥 Usuários"):
            st.session_state.page = "Usuários"

    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "Logout"

if __name__ == '__main__':
    main()
