import streamlit as st
import cv2
import numpy as np
import random
import time
import jogo_boxe
from cvzone.HandTrackingModule import HandDetector

# Configurações do jogo
BALL_COUNT = 3  # Número inicial de bolas
BALL_SPEED = 2  # Velocidade de queda das bolas
INCREASE_SPEED = 1  # Aumento da velocidade a cada rodada
BALL_APPEAR_INTERVAL = 1.5  # Tempo em segundos entre aparições de bolas

# Inicializa o detector de mãos
detector = HandDetector(maxHands=1)

# Inicializa variáveis do jogo
balls = []
score = 0
game_running = True
last_ball_time = 0

# Função para criar novas bolas
def create_ball():
    x = random.randint(50, 650)
    y = 0
    radius = random.randint(20, 40)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return {'x': x, 'y': y, 'radius': radius, 'color': color}

# Função para desenhar as bolas
def draw_balls(img, balls):
    for ball in balls:
        cv2.circle(img, (ball['x'], ball['y']), ball['radius'], ball['color'], cv2.FILLED)

# Função para desenhar a pontuação na tela
def display_score(img, score):
    cv2.putText(img, f"Pontos: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Função principal do jogo
def main():
    global balls, score, game_running, BALL_SPEED, last_ball_time

    st.title("🏆 Jogo de Boxe! 🥊")
    st.subheader("Use sua mão para clicar nas bolas!")
    st.markdown("""
        **Instruções**:
        - Quando as bolas caírem, feche sua mão sobre elas para "acertá-las".
        - Cada bola que você acertar aumenta sua pontuação!
        - Tente acumular o maior número de pontos possível.
    """)
    st.text("Aperte o botão para começar o jogo!")

    # Botão para iniciar o jogo
    if st.button("Iniciar Jogo"):
        # Reinicia as variáveis do jogo
        balls = []
        score = 0
        game_running = True
        BALL_SPEED = 5
        last_ball_time = time.time()  # Tempo inicial para a primeira bola

        # Captura de vídeo
        cap = cv2.VideoCapture(0)

        # Cria um espaço para exibir o vídeo
        video_feed = st.empty()

        # Executa o loop do jogo
        while game_running:
            success, img = cap.read()
            if not success:
                st.error("Erro ao capturar a câmera.")
                break

            # Processa a imagem para encontrar as mãos
            hands, img = detector.findHands(img, draw=True)

            # Atualiza a posição das bolas
            if time.time() - last_ball_time > BALL_APPEAR_INTERVAL:
                balls.append(create_ball())
                last_ball_time = time.time()  # Atualiza o tempo da última bola

            for ball in balls:
                ball['y'] += BALL_SPEED  # Aumenta a posição Y para fazer a bola descer

            # Verifica se as bolas saíram da tela
            balls = [ball for ball in balls if ball['y'] < 480]

            # Verifica se a mão está fechada
            if hands:
                hand = hands[0]
                if detector.fingersUp(hand) == [0, 0, 0, 0, 0]:  # Mão fechada
                    hand_pos = hand['lmList']  # Posições dos pontos da mão

                    # Verifica colisão com as bolas
                    for ball in balls:
                        # Verifica se a mão fechada colide com a bola
                        if any(np.linalg.norm(np.array([ball['x'], ball['y']]) - np.array([pt[0], pt[1]])) < ball['radius'] for pt in hand_pos):
                            balls.remove(ball)  # Remove a bola
                            score += 1  # Incrementa a pontuação
                            st.success(f"Bola clicada! Pontuação: {score}")
                            break

            # Desenha as bolas e a pontuação na imagem
            draw_balls(img, balls)
            display_score(img, score)

            # Converte a imagem de BGR para RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Exibe a imagem no Streamlit
            video_feed.image(img_rgb, channels="RGB", use_column_width=True)

            # Aumenta a dificuldade
            if score % 10 == 0 and score > 0:
                BALL_SPEED += INCREASE_SPEED

            time.sleep(0.1)  # Controla a taxa de quadros

        cap.release()

if __name__ == "__main__":
    main()
