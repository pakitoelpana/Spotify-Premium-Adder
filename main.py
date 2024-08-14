from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from colorama import Fore, Style
from contextlib import contextmanager
from pystyle import Write, Colors
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random
import pyotp
import os


PAYPAL_STATUS_FILE = 'paypal_status.txt'
EMAIL_CONSTANT = ''
PASSWORD_CONSTANT = ''
SECRET = ''
         

config = json.load(open("config.json", encoding="utf-8"))


def cls(): 
    os.system('cls' if os.name =='nt' else 'clear')


# Show introduction
def show_intro():
    Write.Print(f"""
   \t\t\t      ██▓    ▄▄▄       ██▓███    ██████  █    ██   ██████ 
   \t\t\t     ▓██▒   ▒████▄    ▓██░  ██▒▒██    ▒  ██  ▓██▒▒██    ▒ 
   \t\t\t     ▒██░   ▒██  ▀█▄  ▓██░ ██▓▒░ ▓██▄   ▓██  ▒██░░ ▓██▄   
   \t\t\t     ▒██░   ░██▄▄▄▄██ ▒██▄█▓▒ ▒  ▒   ██▒▓▓█  ░██░  ▒   ██▒
   \t\t\t     ░██████▒▓█   ▓██▒▒██▒ ░  ░▒██████▒▒▒▒█████▓ ▒██████▒▒
   \t\t\t     ░ ▒░▓  ░▒▒   ▓▒█░▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
   \t\t\t     ░ ░ ▒  ░ ▒   ▒▒ ░░▒ ░     ░ ░▒  ░ ░░░▒░ ░ ░ ░ ░▒  ░ ░
   \t\t\t       ░ ░    ░   ▒   ░░       ░  ░  ░   ░░░ ░ ░ ░  ░  ░  
   \t\t\t         ░  ░     ░  ░               ░     ░           ░  
                                                      
    """, Colors.white, interval=0.000)
    print("\n\n")
    
 
def set_cmd_title(title):
    os.system(f'title {title}')

def count_lines(file_path):
    """Conta il numero di righe in un file."""
    try:
        with open(file_path, 'r') as file:
            return sum(1 for line in file if line.strip())
    except FileNotFoundError:
        return 0

def update_title():
    accspotify_count = count_lines('accspotify.txt')
    credentials_count = count_lines('credentials.txt')
    title = f'Spotify Adder By Lapsus - Premium Account: {accspotify_count} - Normal Account: {credentials_count}'
    set_cmd_title(title)

show_intro()



def read_credentials(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def remove_credentials(file_path, email, password):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != f"{email}:{password}":  # Controlla sia l'email che la password
                file.write(line)

def save_account_to_file(email):
    with open('accspotify.txt', 'a') as file:
        file.write(email + '\n')
        

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()

def click_element_with_js(driver, selector):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    driver.execute_script("arguments[0].click();", element)

def disable_credentials_saving(driver):
    try:
        save_credentials_button_selector = 'span.Indicator-sc-acu4qz-0.GuRdu'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, save_credentials_button_selector))).click()
    except Exception as e:
        print(f"Errore durante la disattivazione della memorizzazione delle credenziali: {e}")

@contextmanager
def open_file(file_path, mode='r'):
    """ Context manager for file operations """
    try:
        file = open(file_path, mode)
        yield file
    except IOError as e:
        print(f"Errore di I/O durante l'apertura del file {file_path}: {e}")
    finally:
        file.close()

def read_paypal_status(file_path):
    """ Legge lo stato di PayPal da un file e ritorna True se 'logged_in', False altrimenti """
    try:
        with open_file(file_path) as file:
            status = file.read().strip()
            return status == 'logged_in'
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Errore durante la lettura dello stato di PayPal: {e}")
        return False

def write_paypal_status(file_path, status):
    """ Scrive lo stato di PayPal nel file """
    try:
        with open_file(file_path, 'w') as file:
            file.write('logged_in' if status else 'logged_out')
    except Exception as e:
        print(f"Errore durante la scrittura dello stato di PayPal: {e}")

def remove_file_if_exists(file_path):
    """ Rimuove il file se esiste """
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"Il file {file_path} non esiste.")


def accept_cookies(driver):
    cookie_accept_button_selector = 'button#onetrust-accept-btn-handler'
    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:
            attempt += 1
            # Prova a trovare il bottone di accettazione dei cookie
            cookie_accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_accept_button_selector)))
            cookie_accept_button.click()
            print(f"{Style.RESET_ALL}{get_current_time()}{Fore.GREEN} [ ✔ ] Cookie accepted successfully!{Style.RESET_ALL}")
            return True  # Esci dalla funzione una volta che il clic è stato eseguito
        except Exception as e:
            formatted_time = f"{Fore.WHITE}{get_current_time()}{Style.RESET_ALL}"
            print(f"{Style.RESET_ALL}{formatted_time}{Fore.RED} [ X ] Unable to accept cookies, Trying again...{Style.RESET_ALL}")
            time.sleep(1)  
    
    print(f"{get_current_time()}{Fore.MAGENTA} [ X ] Max attempts reached. Unable to accept cookies.{Style.RESET_ALL}")
    return False

 
def click_button_with_js2(driver, selector):
    try:
        # Trova l'elemento
        element = driver.find_element(By.CSS_SELECTOR, selector)
        # Esegui il clic tramite JavaScript
        driver.execute_script("arguments[0].click();", element)
        print(f"Bottone cliccato con JavaScript utilizzando il selettore: {selector}")
    except Exception as e:
        pass


def click_login_buttons(driver):
    """ Trova e clicca sui bottoni di login, escludendo quelli con il testo 'Continua con Google' """
    if "login" in driver.current_url:
        try:
            login_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-testid="login-button"]')
            for button in login_buttons:
                if "Continua con Google" not in button.text:
                    try:
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()
                    except Exception as e:
                        print()
        except Exception as e:
            print()

loop_numer = 1

def process_account(driver, email, password, credentials_file):
    global loop_numer
    update_title()
    payment_completed = False
    paypal_status_file = PAYPAL_STATUS_FILE
    paypal_logged_in = read_paypal_status(paypal_status_file)
    try:
        driver.get("https://accounts.spotify.com/en/login")
        
        # Disattiva la memorizzazione delle credenziali
        disable_credentials_saving(driver)

        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-username")))
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-password")))

        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        wait = WebDriverWait(driver, 10)

        click_login_buttons(driver)
                    
        wait = WebDriverWait(driver, 10)

        first_button_selector = '.ButtonInner-sc-14ud5tc-0.liTfRZ.encore-bright-accent-set'
        try:
            first_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, first_button_selector)))
            first_button.click()
            formatted_time = f"{Fore.WHITE}{get_current_time()}{Style.RESET_ALL}"
            print(f"{Style.RESET_ALL}{formatted_time}{Fore.CYAN} [ {loop_numer} ] -=> Typing mail and password... ")
        except Exception as e:
            print(f"{formatted_time}{Fore.RED} [ X ] 'Login' Button Not Found")
            pass
        
        time.sleep(1)
        
        overview_button_selector = 'span[data-encore-id="text"]'
        try:
            overview_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, overview_button_selector)))
            overview_button.click()
            print(f"{Style.RESET_ALL}{formatted_time}{Fore.MAGENTA} [ {loop_numer} ] -=> Logged in the account... ")
        except Exception as e:
            pass

        time.sleep(1)

        if not accept_cookies(driver):
            return
        
        time.sleep(0.5)
        
        second_button_selector = 'div.RowButton-sc-xxkq4e-0.hloSdh'
        try:
            click_button_with_js2(driver, second_button_selector)
            formatted_time = f"{Fore.WHITE}{get_current_time()}{Style.RESET_ALL}"
        except Exception as e:
            print()

        time.sleep(0.5)

        premium_button_selector = 'a.Button-sc-y0gtbx-0.ccOWSC.encore-text-body-medium-bold'
        try:
            premium_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, premium_button_selector)))
            premium_button.click()
            formatted_time = f"{Fore.WHITE}{get_current_time()}{Style.RESET_ALL}"
            print(f"{Style.RESET_ALL}{formatted_time}{Fore.YELLOW} [ {loop_numer} ] -=> about to add the premium... ")
        except Exception as e:
            print(f"{formatted_time}{Fore.RED} [ X ] 'Go to premium' Button Not Found")

            

        trial_button_selector = 'span.ButtonInner-sc-14ud5tc-0.doXQva.sc-67ff8803-1.cFVwIz'
        click_element_with_js(driver, trial_button_selector)

        time.sleep(0.5)
        
        if not payment_completed:
            paypal_button_selector = 'a[data-value="paypal"]'
            try:
                paypal_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, paypal_button_selector)))
                paypal_button.click()
                print(f"{Style.RESET_ALL}{formatted_time}{Fore.RED} [ {loop_numer} ] -=> Adding payment method... ")
            except Exception as e:
                print(f"{formatted_time}{Fore.RED} [ X ] 'Paypal' Button Not Found")

                
            time.sleep(0.5)

            driver.switch_to.default_content()

            complete_purchase_button_selector = 'span.ButtonInner-sc-14ud5tc-0.koRTtz.encore-bright-accent-set.sc-dmXWDj.gtgZlj'
            try:
                complete_purchase_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, complete_purchase_button_selector))
                )
                complete_purchase_button.click()
            except Exception as e:
                print(f"{formatted_time}{Fore.RED} [ X ] 'Continue with the purchase' Button Not Found")
                
                
            if not paypal_logged_in:
                email_input_selector = 'input#email'
                formatted_time = f"{Fore.WHITE}{get_current_time()}{Style.RESET_ALL}"
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, email_input_selector))).send_keys(EMAIL_CONSTANT)
                except Exception as e:
                    print(f"{formatted_time}{Fore.RED} [ X ] 'Email' Button Not Found")

                    
                time.sleep(3)

                next_button_selector = 'button#btnNext'
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector))).click()
                except Exception as e:
                    print(f"{formatted_time}{Fore.RED} [ X ] 'Forward' Button Not Found")

                    
                time.sleep(3)

                password_input_selector = '#login_passworddiv input#password'
                try:
                    password_input = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, password_input_selector))
                    )
                    password_input.send_keys(PASSWORD_CONSTANT)
                except Exception as e:
                    print(f"{formatted_time}{Fore.RED} [ X ] 'Password' Button Not Found")

                    
                time.sleep(3)

                login_button_selector = 'button#btnLogin'
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, login_button_selector))).click()
                except Exception as e:
                    print(f"{formatted_time}{Fore.RED} [ X ] 'Login' Button Not Found")

                time.sleep(3)
                
                
                otp_code = generate_otp(SECRET)
                otp_selectors = [
                    'input#ci-otpCode-0',
                    'input#ci-otpCode-1',
                    'input#ci-otpCode-2',
                    'input#ci-otpCode-3',
                    'input#ci-otpCode-4',
                    'input#ci-otpCode-5'
                ]

                for i, digit in enumerate(otp_code):
                    try:
                        otp_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, otp_selectors[i]))
                        )
                        otp_input.send_keys(digit)
                    except Exception as e:
                        print(f"Error entering OTP code")

                        
                time.sleep(3)
                
                continue_button_selector = 'button.submit-form-button.buttonEffects.css-1mvakau-button_base-text_button_lg-btn_full_width'
                try: 
                    continue_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, continue_button_selector))
                    ) 
                    continue_button.click()
                except Exception as e:
                    print(f"{formatted_time}{Fore.RED} [ X ] 'Continue' Button Not Found")



                continue_button_selector = 'button.submit-form-button.buttonEffects.css-1mvakau-button_base-text_button_lg-btn_full_width'
                try:
                    continue_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, continue_button_selector))
                    )
                    continue_button.click()
                except Exception as e:
                    pass

                paypal_logged_in = True  
                write_paypal_status(paypal_status_file, paypal_logged_in)

            consent_button_selector = 'button#consentButton'
            try:
                consent_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, consent_button_selector)))
                consent_button.click()
                formatted_time = f"{Fore.WHITE}{get_current_time()}{Style.RESET_ALL}"
                print(f"{Style.RESET_ALL}{formatted_time}{Fore.GREEN} [ DONE ] Premium successfully added to: {email}:{password}")
                save_account_to_file(email)
                remove_credentials(credentials_file, email, password)
                update_title()
            except Exception as e:
                pass

            time.sleep(3)

            loop_numer += 1
    
    finally:
        driver.delete_all_cookies()

def main():
     
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-webrtc")
    options.add_argument('--log-level=3')
    options.add_argument('--disable-logging')
    options.add_argument("window-size=1920,1080")
    options.add_argument('--incognito')
    options.add_argument('--disable-save-password')
    # options.add_argument('--headless')

  
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
     
    try:
        credentials_file = 'credentials.txt'
        credentials = read_credentials(credentials_file)

        for credential in credentials:
            email, password = credential.split(':')
            try:
                process_account(driver, email, password, credentials_file)  
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                print(f"Error during process: {email}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
    
    
