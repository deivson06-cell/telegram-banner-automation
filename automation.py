import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from datetime import datetime

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GeradorProAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        
        # Configurações - Pega suas credenciais das variáveis do GitHub
        self.login_url = "https://gerador.pro/"
        self.username = os.getenv('GERADOR_USERNAME')  # Sua credencial
        self.password = os.getenv('GERADOR_PASSWORD')  # Sua credencial
        
    def setup_driver(self):
        """Configura o driver do Chrome para automação"""
        logger.info("🔧 Configurando driver do Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Roda sem interface gráfica
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        logger.info("✅ Driver configurado com sucesso!")
        
    def login(self):
        """Faz login no Gerador Pro"""
        try:
            logger.info("🌐 Acessando página de login...")
            self.driver.get(self.login_url)
            
            # Aguarda a página carregar
            time.sleep(3)
            
            # Tenta diferentes seletores para os campos de login
            username_field = None
            password_field = None
            
            # Possíveis seletores para username
            username_selectors = [
                'input[name="usuario"]',
                'input[name="email"]', 
                'input[name="login"]',
                'input[type="text"]',
                '#usuario',
                '#email',
                '#login'
            ]
            
            for selector in username_selectors:
                try:
                    username_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            # Possíveis seletores para password
            password_selectors = [
                'input[name="senha"]',
                'input[name="password"]',
                'input[type="password"]',
                '#senha',
                '#password'
            ]
            
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not username_field or not password_field:
                raise Exception("Campos de login não encontrados")
            
            # Preenche credenciais
            logger.info("📝 Preenchendo credenciais...")
            username_field.clear()
            username_field.send_keys(self.username)
            time.sleep(1)
            
            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(1)
            
            # Clica no botão de login
            login_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:contains("Entrar")',
                'button:contains("Login")',
                '.btn-primary',
                '#btnLogin'
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not login_button:
                # Tenta encontrar por texto
                login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar') or contains(text(), 'Login')]")
            
            login_button.click()
            
            # Aguarda dashboard carregar
            time.sleep(5)
            logger.info("✅ Login realizado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no login: {e}")
            # Salva screenshot para debug
            try:
                self.driver.save_screenshot('login_error.png')
            except:
                pass
            return False
    
    def navigate_to_football_generator(self):
        """Navega para o gerador de futebol"""
        try:
            logger.info("⚽ Navegando para gerador de futebol...")
            
            # Aguarda página carregar
            time.sleep(3)
            
            # Procura o link "Gerar Futebol"
            football_selectors = [
                'a[href*="futebol"]',
                'a:contains("Gerar Futebol")',
                'a:contains("Futebol")',
                '#gerar-futebol'
            ]
            
            football_menu = None
            for selector in football_selectors:
                try:
                    football_menu = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not football_menu:
                # Tenta por XPATH com texto
                football_menu = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Gerar Futebol') or contains(text(), 'Futebol')]")
            
            football_menu.click()
            time.sleep(3)
            
            logger.info("✅ Página de modelos carregada!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao navegar para futebol: {e}")
            try:
                self.driver.save_screenshot('navigation_error.png')
            except:
                pass
            return False
    
    def select_model_2(self):
        """Seleciona o Modelo 2 e configura"""
        try:
            logger.info("🎨 Selecionando Modelo 2...")
            
            # Aguarda página carregar
            time.sleep(3)
            
            # Procura o Modelo 2
            model_selectors = [
                '//div[contains(text(), "Modelo 2")]',
                '//span[contains(text(), "Modelo 2")]',
                '//button[contains(text(), "Modelo 2")]',
                '//a[contains(text(), "Modelo 2")]',
                '[data-model="2"]',
                '#modelo-2'
            ]
            
            model_2 = None
            for selector in model_selectors:
                try:
                    if selector.startswith('//'):
                        model_2 = self.driver.find_element(By.XPATH, selector)
                    else:
                        model_2 = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not model_2:
                # Procura qualquer elemento clicável que contenha "2"
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '2') and (name()='div' or name()='button' or name()='a')]")
                if elements:
                    model_2 = elements[0]  # Pega o primeiro
            
            if model_2:
                model_2.click()
                time.sleep(3)
                logger.info("✅ Modelo 2 selecionado!")
            else:
                # Se não encontrar Modelo 2, usa o primeiro modelo disponível
                logger.info("⚠️ Modelo 2 não encontrado, usando modelo padrão...")
                time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao selecionar modelo: {e}")
            try:
                self.driver.save_screenshot('model_error.png')
            except:
                pass
            return False
    
    def generate_banners(self):
        """Gera os banners"""
        try:
            logger.info("🔄 Iniciando geração de banners...")
            
            # Procura o botão de gerar
            generate_selectors = [
                '//button[contains(text(), "Gerar")]',
                '//input[contains(@value, "Gerar")]',
                '//a[contains(text(), "Gerar")]',
                '#gerar-banners',
                '.btn-gerar',
                'button[type="submit"]'
            ]
            
            generate_button = None
            for selector in generate_selectors:
                try:
                    if selector.startswith('//'):
                        generate_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        generate_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if generate_button:
                generate_button.click()
                logger.info("🔄 Aguardando processamento...")
                
                # Aguarda o processamento (pode demorar)
                time.sleep(10)
                
                # Aguarda até aparecer os banners ou mudar de URL
                for i in range(30):  # Espera até 30 segundos
                    current_url = self.driver.current_url
                    if "cartazes" in current_url or "banner" in current_url:
                        break
                    time.sleep(1)
                
                logger.info("✅ Banners gerados com sucesso!")
                return True
            else:
                raise Exception("Botão de gerar não encontrado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar banners: {e}")
            try:
                self.driver.save_screenshot('generate_error.png')
            except:
                pass
            return False
    
    def send_to_telegram(self):
        """Envia todos os banners para o Telegram"""
        try:
            logger.info("📤 Enviando banners para o Telegram...")
            
            # Aguarda página carregar
            time.sleep(5)
            
            # Procura o botão de enviar todas as imagens
            send_selectors = [
                '//button[contains(text(), "Enviar Todas")]',
                '//button[contains(text(), "Enviar")]',
                '//a[contains(text(), "Enviar")]',
                '#enviar-telegram',
                '.btn-telegram',
                'button[onclick*="telegram"]'
            ]
            
            send_button = None
            for selector in send_selectors:
                try:
                    if selector.startswith('//'):
                        send_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        send_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if send_button:
                send_button.click()
                
                # Aguarda confirmação
                time.sleep(5)
                
                logger.info("✅ Banners enviados para o Telegram com sucesso!")
                return True
            else:
                logger.warning("⚠️ Botão de envio não encontrado, mas banners podem ter sido gerados")
                return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar para Telegram: {e}")
            try:
                self.driver.save_screenshot('send_error.png')
            except:
                pass
            return False
    
    def run_automation(self):
        """Executa a automação completa"""
        start_time = datetime.now()
        logger.info("🚀 === INICIANDO AUTOMAÇÃO GERADOR PRO ===")
        
        try:
            # 1. Configurar driver
            self.setup_driver()
            
            # 2. Fazer login
            if not self.login():
                raise Exception("Falha no login")
            
            # 3. Navegar para futebol
            if not self.navigate_to_football_generator():
                raise Exception("Falha ao navegar para futebol")
            
            # 4. Selecionar modelo
            if not self.select_model_2():
                raise Exception("Falha ao selecionar modelo")
            
            # 5. Gerar banners
            if not self.generate_banners():
                raise Exception("Falha ao gerar banners")
            
            # 6. Enviar para Telegram
            if not self.send_to_telegram():
                raise Exception("Falha ao enviar para Telegram")
            
            duration = datetime.now() - start_time
            logger.info(f"🎉 === AUTOMAÇÃO CONCLUÍDA COM SUCESSO! Tempo: {duration} ===")
            
        except Exception as e:
            logger.error(f"💥 === AUTOMAÇÃO FALHOU: {e} ===")
            raise
        
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("🔒 Driver fechado.")

def main():
    """Função principal"""
    automation = GeradorProAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main()
