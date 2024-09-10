# Automação de Mensagens no WhatsApp

## Descrição

Este projeto consiste em um script de automação para envio de mensagens no WhatsApp, utilizando **Selenium** e reconhecimento de imagem com **OpenCV**. O código permite o envio automático de mensagens através de uma interface de login manual no WhatsApp Web, detectando quando o login foi realizado e interagindo com os elementos da interface para disparar mensagens.

## Funcionalidades

- Envio automático de mensagens no WhatsApp Web.
- Reconhecimento de elementos de interface utilizando **OpenCV**.
- Gerenciamento de múltiplas abas abertas (WhatsApp Web).
- Fechamento automático da aba após o envio da mensagem.
- Detecção de login via mudança de tela.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada no desenvolvimento do script.
- **Selenium**: Biblioteca usada para automação do navegador.
- **OpenCV**: Utilizado para reconhecimento de imagens e detecção de ícones.
- **PyAutoGUI**: Para simular cliques nos ícones da interface.
- **Tkinter**: Biblioteca para criar interfaces gráficas simples no Python.
- **NumPy:** Para manipulação de arrays e imagens com o OpenCV.
- **Pillow:** Para capturar a tela (usando ImageGrab)

## Requisitos

- Python 3.8+
- Google Chrome (com driver do Selenium para Chrome)

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/usuario/automacao-whatsapp.git
    ```
2. Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure o **ChromeDriver**:
   - Baixe o [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) compatível com a sua versão do Chrome.
   - Adicione o **ChromeDriver** ao **PATH** do seu sistema operacional.

## Como Usar

1. Abra o terminal e execute o script principal:
    ```bash
    python principal.py
    ```
2. O sistema solicitará uma URL. Geralmente, utilizamos uma URL de suporte com login e senha, que já está previamente configurada com a API do WhatsApp para realizar disparos de mensagens ao clicar nos botões de envio.

3. O WhatsApp Web será aberto no navegador caso as imagens do sistema estejam corretamente configuradas. Faça login manualmente.

4. O sistema detectará o login e enviará as mensagens automaticamente.

5. As abas do WhatsApp Web serão fechadas automaticamente após o envio das mensagens, e o sistema continuará clicando nos ícones enquanto eles estiverem disponíveis.

## Contribuindo

Se desejar contribuir para o projeto, fique à vontade para fazer um fork, criar uma branch, e abrir um **Pull Request**. Serão bem-vindas melhorias no código e novas funcionalidades.

## Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

## NOTA:

O sistema ainda apresenta algumas falhas, mas está funcional. Agradecemos pela compreensão.
