# principal.py
import cv2
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyautogui import click
from PIL import ImageGrab
import tkinter as tk
from tkinter import simpledialog
from funcoes_aviao import verificar_icon # Importa a função do bloco separado

# Função para capturar a tela e verificar se a imagem do login existe
def find_image_on_screen(image_path):
    # Carrega a imagem do template
    template = cv2.imread(image_path, 0)
    
    # Verifica se a imagem foi carregada corretamente
    if template is None:
        print(f"Erro: Não foi possível carregar a imagem do caminho {image_path}. Verifique o caminho e tente novamente.")
        return False, None
    
    screen = np.array(ImageGrab.grab())  # Captura a tela atual
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # Converte para escala de cinza
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)  # Compara as imagens
    _, max_val, _, max_loc = cv2.minMaxLoc(result)  # Encontra o ponto de maior correspondência
    
    # Se a correspondência for maior que o limiar, retorna o local
    if max_val > 0.8:  # Limiar de 80% de correspondência
        return True, max_loc
    return False, None

# Função para clicar em uma localização
def click_on_location(location):
    click(location[0], location[1])

# Função para abrir o navegador e acessar a URL
def abrir_plataforma_web(url):
    driver = webdriver.Chrome()  # Inicializa o driver do Chrome
    driver.maximize_window()  # Coloca o navegador em tela cheia
    driver.get(url)  # Abre a URL fornecida pelo usuário
    return driver

# Função para obter informações do usuário (login e senha) através de uma interface gráfica
def obter_informacoes():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Pergunta ao usuário o nome de usuário e senha
    username = simpledialog.askstring("Login", "Digite seu nome de usuário:")
    password = simpledialog.askstring("Senha", "Digite sua senha:", show="*")

    return username, password

# Função principal que controla o processo
def main():
    # Função para criar a interface gráfica e pedir a URL
    root = tk.Tk()
    root.withdraw()
    
    url = simpledialog.askstring("URL", "Digite a URL da plataforma web que deseja abrir:")
    
    if url:
        # Passo 1: Abre a plataforma em tela cheia
        driver = abrir_plataforma_web(url)
        wait = WebDriverWait(driver, 20)  # Espera até 20 segundos para os elementos aparecerem

        # Aguarda o redirecionamento ou outra mudança de página
        time.sleep(5)
        # Passo 2: Verifica se a imagem da página de login está presente
        login_detected, location = find_image_on_screen('src/login_image.png')  # Caminho da imagem da página de login

        if login_detected:
            print("Página de login detectada.")

            login_sucesso = False  # Variável de controle para o loop de tentativas de login

            # Loop de tentativa de login até que o login seja bem-sucedido
            while not login_sucesso:
                    # Passo 3: Pergunta o login e senha ao usuário
                    username, password = obter_informacoes()

                    try:
                        # Localiza o campo de login e senha (ajustado com base no HTML fornecido)
                        login_field = wait.until(EC.presence_of_element_located((By.NAME, "nome")))  # Campo de login
                        password_field = wait.until(EC.presence_of_element_located((By.NAME, "senha")))  # Campo de senha

                        # Limpa os campos e insere o nome de usuário e a senha
                        login_field.clear()
                        login_field.send_keys(username)
                        password_field.clear()
                        password_field.send_keys(password)

                        # Passo 4: Clica no botão "Entrar"
                        enter_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btnEnter")))  # Botão "Entrar"
                        enter_button.click()

                        # Aguarda o redirecionamento ou outra mudança de página
                        time.sleep(5)

                        # Verifica se o login foi bem-sucedido (pode verificar se a URL mudou ou o conteúdo da página)
                        if driver.current_url != url:
                            #print("Login bem-sucedido!")
                            print("Login bem-sucedido! Agora vamos verificar os ícones de aviões verdes.")
                            login_sucesso = True  # Sai do loop se o login foi bem-sucedido
                            
                            # Chama a função para verificar os icones e depois clickar nos aviões correspondentes
                            verificar_icon(driver, 'src/deslike_icon_image.png')
                            
                        else:
                            print("Credenciais incorretas. Tente novamente.")
                
                    except Exception as e:
                        print(f"Erro ao tentar preencher os campos de login: {e}")
                        print("Tente novamente.")
            
            # Mantém o navegador aberto após o login bem-sucedido
            print("Navegador continuará aberto após o login. Pressione Ctrl+C para fechar.")
            while True:
                time.sleep(10)  # Mantém o navegador aberto indefinidamente
        else:
            print("Página de login não detectada.")
    else:
        print("Nenhuma URL foi fornecida.")

# Executa o sistema
if __name__ == "__main__":
    main()
