# funcoes_aviao.py
import cv2
import numpy as np
from pyautogui import locateCenterOnScreen
from pyautogui import click
from PIL import ImageGrab
import time
from selenium.webdriver.common.by import By
from disparando_no_whatsapp import enviar_mensagem # Importa a função do bloco separado


# Função para verificar o icone antes de cliclar em qualquer coisa
def verificar_icon(driver, icon_path):
    driver = driver
    # Tenta localizar o ícone na tela
    icone_location = locateCenterOnScreen(icon_path, confidence=0.9)  # Confidence define a precisão da correspondência
    if icone_location:
        print(f"Ícone encontrado: {icon_path}")
        if icon_path == 'src/deslike_icon_image.png':
            clicar_em_avioes_verdes(driver,'src/airplane_icon_verde_image.png')
        return icone_location
    else:
        print(f"Ícone não encontrado: {icon_path}")
        return None


# Função para encontrar e clicar nos ícones de avião verde com scroll via Selenium
def clicar_em_avioes_verdes(driver, image_path, num_max_tentativas=10):
    tentativas = 0
    avioes_encontrados = 0
    match_locations = []  # Armazena locais onde o ícone foi encontrado
    
    # Carrega a imagem do ícone do avião verde e obtém suas dimensões
    template = cv2.imread(image_path)
    template_height, template_width = template.shape[:2]  # Obtém a altura e a largura da imagem

    if template is None:
        print(f"Erro: Não foi possível carregar a imagem do caminho {image_path}. Verifique o caminho e tente novamente.")
        return

    # Realiza scroll e busca os ícones por um número máximo de tentativas
    while tentativas < num_max_tentativas:
        screen = np.array(ImageGrab.grab())  # Captura a tela atual
        screen_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)  # Usa a imagem em cores (RGB)

        # Faz a correspondência de templates em cores
        result = cv2.matchTemplate(screen_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9  # Define um limiar mais rigoroso de correspondência (90%)
        loc = np.where(result >= threshold)  # Localiza todas as correspondências acima do limiar

        # Se encontrou algum ícone de avião verde
        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):  # Para cada correspondência encontrada
                if pt not in match_locations:  # Verifica se a posição já foi clicada
                    match_locations.append(pt)  # Armazena a localização

                    # Calcula o centro do ícone para clicar corretamente
                    center_x = pt[0] + template_width // 2
                    center_y = pt[1] + template_height // 2

                    # Clica no centro da imagem detectada
                    click(center_x, center_y)
                    avioes_encontrados += 1
                    print(f"Avião verde encontrado e clicado na posição central: ({center_x}, {center_y}).")
                    time.sleep(5)  # Aguarda para garantir que o clique foi processado
                    enviar_mensagem(driver)
            
            # Faz scroll na página utilizando Selenium
            driver.execute_script("window.scrollBy(0, 500);")  # Faz o scroll para baixo
            time.sleep(2)  # Aguarda a página atualizar após o scroll

        else:
            print("Nenhum novo avião verde encontrado.")
            break  # Sai do loop se não houver mais ícones
        
        tentativas += 1
    
    print(f"Total de aviões verdes clicados: {avioes_encontrados}")

