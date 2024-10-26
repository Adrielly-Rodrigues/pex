import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
import os

def desenhar_page():
    st.title("Desenhar com Mãos")

    if "camera_running" not in st.session_state:
        st.session_state.camera_running = False

    if "saved_images" not in st.session_state:
        st.session_state.saved_images = []

    col1, col2 = st.columns([3, 1])

    with col1:
        run_drawing_app()

    st.subheader("Desenhos Salvos:")
    for img_path in st.session_state.saved_images:
        st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)

    st.subheader("Como desenhar?")
    st.write("""    
    Para criar seus desenhos, utilize os seguintes gestos:

    - **1 dedo levantado (indicador)**: desenhe na tela.
    - **2 dedos levantados**: o desenho aparecerá na tela.
    - **Botão 'Salvar'**: passe o dedo sobre o botão para salvar.
    - **Botão 'Apagar'**: passe o dedo sobre o botão para apagar desenhos anteriores.
    - **Trocar de cor**: passe o dedo sobre os círculos de cores para mudar a cor.
    """)

def run_drawing_app():
    detector = HandDetector(detectionCon=0.7, maxHands=1)
    cores = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
    cor_desenho_atual = (255, 0, 0)
    
    modo_borracha = False  # Borracha começa desativada

    botao_raio = 19
    espaco_entre_botoes = 20
    botoes = [
        (100, 80, cores[0]),  # Botão preto
        (100 + botao_raio * 2 + espaco_entre_botoes, 80, cores[1]),  # Botão branco
        (100 + botao_raio * 2 * 2 + espaco_entre_botoes * 2, 80, cores[2]),  # Botão vermelho
        (100 + botao_raio * 2 * 3 + espaco_entre_botoes * 3, 80, cores[3]),  # Botão verde
        (100 + botao_raio * 2 * 4 + espaco_entre_botoes * 4, 80, cores[4]),  # Botão azul
    ]

    botao_salvar = (100 + botao_raio * 2 * 5 + espaco_entre_botoes * 5, 80)
    botao_borracha = (100 + botao_raio * 2 * 6 + espaco_entre_botoes * 6, 80)

    intervalo_salvar = 3
    ultimo_tempo_salvamento = time.time()

    video_feed = st.empty()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Não foi possível acessar a câmera.")
        return

    cap.set(3, 720)
    cap.set(4, 480)

    pontos_atual = []
    pontos_desenhos_anteriores = []
    pontos_buffer = []
    desenhando = False

    while True:
        ret, img = cap.read()
        if not ret:
            st.error("Não foi possível capturar o frame da câmera.")
            break

        for bx, by, cor in botoes:
            cv2.circle(img, (bx, by), botao_raio, cor, cv2.FILLED)

        cv2.circle(img, botao_salvar, botao_raio, (200, 200, 200), cv2.FILLED)
        cv2.putText(img, "S", (botao_salvar[0] - 10, botao_salvar[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.circle(img, botao_borracha, botao_raio, (200, 0, 0), cv2.FILLED)
        cv2.putText(img, "A", (botao_borracha[0] - 10, botao_borracha[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        resultado = detector.findHands(img, draw=True)
        hand = resultado[0] if resultado else None

        if hand:
            lmlist = hand[0]['lmList']
            dedos = detector.fingersUp(hand[0])
            dedosLev = dedos.count(1)

            if dedosLev == 1:
                x, y = lmlist[8][0], lmlist[8][1]
                if modo_borracha:
                    cv2.circle(img, (x, y), 20, (255, 255, 255), cv2.FILLED)
                    pontos_desenhos_anteriores = [
                        (px, py, pcor) for px, py, pcor in pontos_desenhos_anteriores
                        if not (px - 20 < x < px + 20 and py - 20 < y < py + 20)
                    ]
                    
                else:
                    cv2.circle(img, (x, y), 15, cor_desenho_atual, cv2.FILLED)
                    if not desenhando:
                        pontos_atual = []
                        pontos_buffer = []
                        desenhando = True
                    pontos_buffer.append((x, y, cor_desenho_atual))
                    if len(pontos_buffer) > 1:
                        for i in range(len(pontos_buffer) - 1):
                            p1 = pontos_buffer[i]
                            p2 = pontos_buffer[i + 1]
                            for t in np.linspace(0, 1, num=10):
                                x_interp = int((1 - t) * p1[0] + t * p2[0])
                                y_interp = int((1 - t) * p1[1] + t * p2[1])
                                pontos_atual.append((x_interp, y_interp, p1[2]))

            else:
                desenhando = False
                if pontos_atual:
                    pontos_desenhos_anteriores.extend(pontos_atual)
                    pontos_atual = []

            x_mao, y_mao = lmlist[8][0], lmlist[8][1]
            for bx, by, cor in botoes:
                if (bx - botao_raio < x_mao < bx + botao_raio) and (by - botao_raio < y_mao < by + botao_raio):
                    cor_desenho_atual = cor
                    cv2.circle(img, (bx, by), botao_raio + 10, (0, 255, 0), 3)
                    modo_borracha = False  # Desativa a borracha ao mudar de cor

            if (botao_salvar[0] - botao_raio < x_mao < botao_salvar[0] + botao_raio) and (botao_salvar[1] - botao_raio < y_mao < botao_salvar[1] + botao_raio):
                tempo_atual = time.time()
                if tempo_atual - ultimo_tempo_salvamento > intervalo_salvar:
                    salvar_desenho(img, pontos_desenhos_anteriores, pontos_atual)
                    ultimo_tempo_salvamento = tempo_atual

            if (botao_borracha[0] - botao_raio < x_mao < botao_borracha[0] + botao_raio) and \
                    (botao_borracha[1] - botao_raio < y_mao < botao_borracha[1] + botao_raio):
                modo_borracha = not modo_borracha  # Alterna a borracha (ativa/desativa)

        for pontos in pontos_desenhos_anteriores + pontos_atual:
            x, y, cor = pontos
            cv2.circle(img, (x, y), 5, cor, cv2.FILLED)

        video_feed.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), channels="RGB")

def salvar_desenho(img, pontos_desenhos_anteriores, pontos_atual):
    if not os.path.exists("galeria"):
        os.makedirs("galeria")

    for pontos in pontos_desenhos_anteriores + pontos_atual:
        x, y, cor = pontos
        cv2.circle(img, (x, y), 5, cor, cv2.FILLED)

    caminho_arquivo = f"galeria/desenho_{int(time.time())}.png"
    cv2.imwrite(caminho_arquivo, img)

    st.session_state.saved_images.append(caminho_arquivo)
    st.success(f"Desenho salvo em: {caminho_arquivo}")
    st.session_state.saved_images.append(caminho_arquivo)
    st.success(f"Desenho salvo em: {caminho_arquivo}")

    # Adiciona o caminho da imagem salva à lista de imagens salvas no session_state
    st.session_state.saved_images.append(caminho_arquivo)

def main():
    # Configuração da interface do Streamlit
    st.sidebar.title("Menu")
    
    pagina = st.sidebar.selectbox("Escolha uma página", ["Desenhar com Mãos", "Sobre"])

    if pagina == "Desenhar com Mãos":
        desenhar_page()
    elif pagina == "Sobre":
        st.title("Sobre o Aplicativo")
        st.write("Este aplicativo permite que você desenhe usando gestos com as mãos, capturados pela sua câmera. Use os botões para salvar seu desenho ou apagar partes dele com a borracha.")

if __name__ == "__main__":
    main()
