# disparando_no_whatsapp.py
import cv2
import numpy as np
import time
from pyautogui import click, locateCenterOnScreen
from PIL import ImageGrab
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

icon_path = 'src/send_icon_image.png'  # Caminho para a imagem do botão de envio

# Função para verificar a mudança de tela e confirmar o login no WhatsApp Web
def verificar_login_com_imagem():
    print("Verificando se o login foi feito...")
    tela_inicial = np.array(ImageGrab.grab())
    time.sleep(5)  # Aguarda 5 segundos para o usuário realizar o login manual

    tela_final = np.array(ImageGrab.grab())

    tela_inicial_gray = cv2.cvtColor(tela_inicial, cv2.COLOR_BGR2GRAY)
    tela_final_gray = cv2.cvtColor(tela_final, cv2.COLOR_BGR2GRAY)

    diferenca = cv2.absdiff(tela_inicial_gray, tela_final_gray)

    non_zero_count = np.count_nonzero(diferenca)

    if non_zero_count > 5000:  # Ajuste o limite conforme necessário
        print("Login detectado com sucesso.")
        return True
    else:
        print("Nenhuma mudança detectada. Login não concluído.")
        return False

# Função principal para enviar a mensagem
def enviar_mensagem(driver):
    try:
        # Verifica se o login já foi feito. Se sim, prossegue com o envio
        login_detectado = verificar_login_com_imagem()
        
        if login_detectado:
            print("Prosseguindo com o envio da mensagem...")
            time.sleep(5)  # Aguarda um tempo adicional para garantir que o WhatsApp Web esteja pronto
            if clicar_botao_enviar_whatsapp():
                time.sleep(5)  # Aguarda mais um pouco para garantir que a mensagem foi enviada
                fechar_aba(driver)  # Fecha a aba após enviar a mensagem
            else:
                print("Não foi possível enviar a mensagem.")
        else:
            print("Login não detectado.")
    except NoSuchWindowException:
        print("A aba do WhatsApp Web já foi fechada ou não está disponível.")
    except WebDriverException as e:
        print(f"Erro do WebDriver: {e}")

# Função para clicar no botão de enviar
def clicar_botao_enviar_whatsapp():
    print("Tentando localizar o ícone de enviar...")
    icone_location = locateCenterOnScreen(icon_path, confidence=0.9)
    if icone_location:
        click(icone_location)
        print("Mensagem enviada com sucesso!")
        return True
    else:
        print(f"Ícone de envio não encontrado: {icon_path}")
        return False

# Função para fechar a aba do WhatsApp Web e voltar para a aba anterior
def fechar_aba(driver):
    print("Fechando a aba do WhatsApp Web.")
    try:
        current_tab = driver.current_window_handle  # Aba atual
        abas = driver.window_handles  # Lista de abas abertas

        # Verifica se há mais de uma aba aberta (aba principal + aba do WhatsApp)
        if len(abas) > 1:
            # Itera por todas as abas para encontrar a do WhatsApp Web
            for aba in abas:
                driver.switch_to.window(aba)
                if "web.whatsapp.com" in driver.current_url:
                    print("Fechando a aba do WhatsApp Web.")
                    driver.close()  # Fecha a aba do WhatsApp Web
                    break
            
            # Volta para a aba original (a que estava antes de abrir o WhatsApp)
            driver.switch_to.window(current_tab)
        else:
            print("Nenhuma outra aba aberta. Não é possível fechar o WhatsApp Web.")
    except NoSuchWindowException:
        print("A aba já foi fechada.")
    except WebDriverException as e:
        print(f"Erro do WebDriver ao fechar a aba: {e}")
