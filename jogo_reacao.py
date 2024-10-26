import cv2
import numpy as np
import time
import random
import streamlit as st
from cvzone.HandTrackingModule import HandDetector

# Inicializando o detector de mãos
detector = HandDetector(maxHands=1)

# Configuração inicial do jogo
BALL_COUNT = 6  # Número fixo de bolas
BALL_RADIUS = 40  # Raio das bolas

# Posicionamento mais espaçado das bolas na tela
BALL_POSITIONS = [(100, 100), (400, 400), (500, 100), (500, 100), (100, 300), (200, 250)]

score = 0  # Pontuação inicial

# Inicializa os estados das bolas (todas começam inativas)
balls = [{'position': pos, 'active': False, 'last_switch': time.time(), 'random_time': random.uniform(1, 3)} for pos in BALL_POSITIONS]

# Função para alternar o estado das bolas com base no tempo e randomizar a troca de estados
def toggle_ball_state(ball, active_time, deactive_time):
    current_time = time.time()
    # Randomiza o tempo de desativação e ativação para cada bola
    if ball['active'] and current_time - ball['last_switch'] >= active_time + ball['random_time']:
        ball['active'] = False
        ball['last_switch'] = current_time
        ball['random_time'] = random.uniform(1, 3)  # Novo tempo aleatório para a próxima ativação
    elif not ball['active'] and current_time - ball['last_switch'] >= deactive_time + ball['random_time']:
        ball['active'] = True
        ball['last_switch'] = current_time
        ball['random_time'] = random.uniform(1, 3)  # Novo tempo aleatório para a próxima desativação

# Função para desenhar as bolas na tela
def draw_balls(img, balls):
    for ball in balls:
        color = (0, 255, 0) if ball['active'] else (255, 0, 0)  # Verde para ativo, vermelho para inativo
        cv2.circle(img, ball['position'], BALL_RADIUS, color, cv2.FILLED)

# Função para verificar se a mão está sobre uma bola ativa e se está fechada
def check_collision(hand, ball, is_fist):
    if ball['active']:
        hand_pos = hand['lmList'][8]  # Pontas do dedo indicador
        distance = np.linalg.norm(np.array(ball['position']) - np.array(hand_pos[:2]))
        if distance < BALL_RADIUS and is_fist:
            return True
    return False

# Função para exibir a pontuação na tela
def display_score(img, score):
    cv2.putText(img, f"Pontos: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Função para exibir o tempo restante na tela
def display_timer(img, remaining_time):
    cv2.putText(img, f"Tempo: {int(remaining_time)}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Função para exibir a pontuação final na tela
def display_final_score(score):
    st.success(f"Fim de Jogo! Sua pontuação final é: {score}")

# Função principal do jogo
def main():
    global score

    st.title("Jogo de Reação - Acessível")
    st.subheader("Escolha sua dificuldade e mova a mão para ativar as bolas piscando!")

    # Escolha de dificuldade
    difficulty = st.selectbox("Selecione a Dificuldade", ("Fácil", "Médio", "Difícil"))

    if difficulty == "Fácil":
        active_time = 2.5  # Bola fica ativa por mais tempo
        deactive_time = 2.5
        game_duration = 30  # Duração do jogo em segundos
    elif difficulty == "Médio":
        active_time = 1.5  # Bola fica ativa por tempo médio
        deactive_time = 1.5
        game_duration = 20  # Duração do jogo em segundos
    elif difficulty == "Difícil":
        active_time = 0.5  # Bola fica ativa por menos tempo (mais rápido)
        deactive_time = 0.5
        game_duration = 15  # Duração do jogo em segundos

    # Botão para iniciar o jogo
    if st.button("Iniciar Jogo"):
        cap = cv2.VideoCapture(0)
        video_feed = st.empty()

        start_time = time.time()  # Marca o início do jogo
        while True:
            elapsed_time = time.time() - start_time
            remaining_time = game_duration - elapsed_time

            if remaining_time <= 0:
                display_final_score(score)  # Exibe a pontuação final ao fim do jogo
                break

            success, img = cap.read()
            if not success:
                st.error("Erro ao acessar a câmera.")
                break

            # Detecta a mão
            hands, img = detector.findHands(img, draw=True)

            if hands:
                hand = hands[0]
                is_fist = hand['type'] == 'Right' and detector.fingersUp(hand) == [0, 0, 0, 0, 0]  # Verifica se a mão está fechada

                # Alterna o estado das bolas com base no tempo randomizado
                for ball in balls:
                    toggle_ball_state(ball, active_time, deactive_time)

                # Verifica colisão com as bolas ativas e se a mão está fechada
                for ball in balls:
                    if check_collision(hand, ball, is_fist):
                        ball['active'] = False  # Desativa a bola ao ser "clicada" com a mão fechada
                        score += 1  # Incrementa a pontuação
                        st.success(f"Bola ativada! Pontuação: {score}")

            # Desenha as bolas e exibe a pontuação e o tempo restante
            draw_balls(img, balls)
            display_score(img, score)
            display_timer(img, remaining_time)

            # Converte para RGB e exibe no Streamlit
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            video_feed.image(img_rgb, channels="RGB", use_column_width=True)

            time.sleep(0.1)  # Controle de taxa de quadros

        cap.release()

if __name__ == "__main__":
    main()
