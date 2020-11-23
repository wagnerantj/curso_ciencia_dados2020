# DEPENDÊNCIAS
# No diretorio raiz do projeto digite o comando abaixo:
# pip install -r requirements.txt
# https://chromedriver.storage.googleapis.com/index.html?path=86.0.4240.22/  *** download do webdriver do chromefrom selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

# Opção 1) Instala o driver do Chrome para o selenium
  # A opção 1 não funciona em alguns computadores.
  # Você saberá se funcionou caso a apareça uma janela do Chrome em branco
driver = webdriver.Chrome(ChromeDriverManager().install())

# Opção 2) Usar o driver do firefox, o geckodriver.
  # Para instalar no windows:
  # 1) Baixe o arquivo para Windows (32 ou 64bits) de https://github.com/mozilla/geckodriver/releases
  # 2) Descompacte o arquivo;
  # 3) Adicione a pasta do arquivo executável na variavel de ambiente PATH.
  #    Veja como adicionar https://knowledge.autodesk.com/pt-br/support/navisworks-products/troubleshooting/caas/sfdcarticles/sfdcarticles/PTB/Adding-folder-path-to-Windows-PATH-environment-variable.html
# driver = webdriver.Firefox()

# Faça o restante do exercicio abaixo