import streamlit as st
from jogo_boxe import main as jogo_boxe  # Importa a função principal do jogo de boxe
from jogo_reacao import main as jogo_reacao  # Importa a função principal do jogo de reação

# Função para exibir o menu de navegação
def show_menu():
    if "page" not in st.session_state:
        st.session_state.page = "Página Inicial"  # Página padrão

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Define o estado de login padrão

    if "role" not in st.session_state:
        st.session_state.role = "user"  # Define o papel padrão

    st.sidebar.title("Menu")

    # Condição para exibir os menus baseados no estado de login
    if st.session_state.logged_in:
        # Exibir opções para usuários logados
        if st.sidebar.button("🏠 Página Inicial"):
            st.session_state.page = "Página Inicial"

        if st.sidebar.button("⚙️ Configurações"):
            st.session_state.page = "Configurações"

        if st.sidebar.button("📄 FAQ"):
            st.session_state.page = "FAQ"

        if st.sidebar.button("🎨 Galeria"):
            st.session_state.page = "Galeria"

        if st.sidebar.button("🥊 Jogo de Boxe"):  # Adiciona o botão para o jogo de boxe
            st.session_state.page = "Jogo de Boxe"

        if st.sidebar.button("🎯 Jogo de Reação"):  # Adiciona o botão para o jogo de reação
            st.session_state.page = "Jogo de Reação"

        if st.session_state.role == "admin":  # Exibe "Cadastro" apenas para o admin
            if st.sidebar.button("👥 Cadastro"):
                st.session_state.page = "Cadastro"  # Página de cadastro

        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False  # Desloga o usuário
            st.session_state.page = "Página Inicial"  # Redireciona para a página inicial
    else:
        # Exibir opções para usuários não logados
        if st.sidebar.button("🏠 Página Inicial"):
            st.session_state.page = "Página Inicial"

        if st.sidebar.button("📚 Guia"):
            st.session_state.page = "Guia"

        if st.sidebar.button("🖌️ Desenhar"):
            st.session_state.page = "Desenhar"

        if st.sidebar.button("🥊 Jogo de Boxe"):  # Adiciona o botão para o jogo de boxe para todos os usuários
            st.session_state.page = "Jogo de Boxe"

        if st.sidebar.button("🎯 Jogo de Reação"):  # Adiciona o botão para o jogo de reação para todos os usuários
            st.session_state.page = "Jogo de Reação"

        if st.sidebar.button("🔑 Logar"):
            st.session_state.page = "Login"  # Redireciona para a página de login

# Função para redirecionar a página com base no estado
def render_page():
    if st.session_state.page == "Página Inicial":
        st.write("Bem-vindo à Página Inicial!")
    elif st.session_state.page == "Desenhar":
        # Importa a função de desenho
        from desenhar import desenhar
        desenhar()
    elif st.session_state.page == "Jogo de Boxe":
        # Executa a função do jogo de boxe
        jogo_boxe()  # Chama a função do jogo de boxe
    elif st.session_state.page == "Jogo de Reação":
        # Executa a função do jogo de reação
        jogo_reacao()  # Chama a função do jogo de reação
    elif st.session_state.page == "Login":
        st.write("Página de Login")
    elif st.session_state.page == "Configurações":
        st.write("Página de Configurações")
    elif st.session_state.page == "Galeria":
        st.write("Página da Galeria")
    elif st.session_state.page == "Cadastro" and st.session_state.role == "admin":
        st.write("Página de Cadastro")

# Função principal
def main():
    show_menu()
    render_page()

if __name__ == "__main__":
    main()
