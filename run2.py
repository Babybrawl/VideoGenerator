import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import subprocess

def click_last_element_with_class_name(class_name):
    elements = driver.find_elements(By.CLASS_NAME, class_name)
    if elements:
        last_element = elements[-1]
        driver.execute_script("arguments[0].scrollIntoView(true);", last_element)
        driver.execute_script("arguments[0].click();", last_element)
        print("Clic sur le dernier élément effectué.")
    else:
        print("Aucun élément trouvé pour la classe donnée.")

def select_video_file():
    all_files = os.listdir(to_upload_folder)
    print("Fichiers trouvés dans le dossier:", all_files)

    partie_files = [f for f in all_files if f.endswith(".mp4") and "partie" in f]
    partie_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    print("Fichiers de partie trouvés et triés:", partie_files)

    for i in range(1, 101):
        expected_file = f"partie{i}.mp4"
        for file in partie_files:
            if f"partie{i}" in file:
                file_path = os.path.join(to_upload_folder, file)
                print(f"Fichier sélectionné : {file}")
                return file_path, i

    raise FileNotFoundError("Aucun fichier approprié trouvé dans le dossier.")

def safe_click(button):
    try:
        button.click()
    except ElementClickInterceptedException:
        print("Un autre élément bloque le bouton. Nouvelle tentative dans 3 secondes...")
        time.sleep(3)
        driver.execute_script("arguments[0].click();", button)

def upload_video_and_finalize(description_text):
    try:
        video_file, part_number = select_video_file()

        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
        file_input.send_keys(video_file)

        span = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "sc-cFShuL hUzoKm")]/div/div/span')))
        description = f"{description_text} Partie {part_number} - {description_text2}"
        span.send_keys(description)

        print("Attente de la fin du téléversement...")

        while True:
            progress_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.publish_progressText_1f6x-')))
            progress_text = progress_span.text.strip()

            print(f"Progression actuelle : {progress_text}")

            if progress_text == "100.0%" or progress_text == "Finishing up…":
                print("Upload complété ou en cours de finalisation. Attente de 5 secondes...")
                time.sleep(5)
                break

            time.sleep(1)  # Attendre une seconde avant de revérifier la progression

        click_last_element_with_class_name('Button__ButtonStyled-bufferapp-ui__sc-16m8s20-2')
        time.sleep(5)

        uploaded_file_path = os.path.join('D:\\test400\\already_uploaded', os.path.basename(video_file))
        shutil.move(video_file, uploaded_file_path)
        print(f"Vidéo téléversée et déplacée : {uploaded_file_path}")
    except Exception as e:
        print(f"Erreur lors de l'upload ou du déplacement : {e}")
        raise  # Lève l'exception pour qu'elle soit capturée par la boucle while
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Erreur lors de la fermeture du driver : {e}")
        subprocess.run(["python", "d:/test400/check_and_run.py"], check=True, shell=True)
        print("Le script check_and_run.py a été exécuté avec succès.")



def open_login_page_and_login():
    driver.get(buffer_login_url)

    email_input = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
    email_input.send_keys(buffer_email)

    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys(buffer_password)

    login_button = driver.find_element(By.ID, 'login-form-submit')
    safe_click(login_button)

    print("Connexion en cours...")
    wait.until(EC.url_to_be(calendar_url))

def navigate_to_calendar_and_click():
    driver.get(calendar_url)

    # Créez un WebDriverWait avec un délai de 10 secondes spécifiquement pour button1
    short_wait = WebDriverWait(driver, 5)

    try:
        button1 = short_wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "style__Modal-bufferapp-ui__sc-1s7w3dz-1 iJpltU")]/button')))
        safe_click(button1)
    except TimeoutException:
        print("Button1 not found within 10 seconds, moving to the next step.")

    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'appshell_base_20pFB.appshell_base_F3oAS.appshell_large_y6VmX.appshell_primary_jgaHy.appshell_button_GE49R')))
    safe_click(button)

    clickable_div = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'appshell_item_5ne-f.appshell_baseItem_da7su.appshell_dropdownItem_NWUDf')))
    safe_click(clickable_div)

    print("Navigation et clic effectués.")

# Variables globales
buffer_email = 'nicolas.babybrawl@gmail.com'
buffer_password = 'NiCoLaS123:)'
buffer_login_url = 'https://login.buffer.com/login?plan=free&cycle=year'
calendar_url = 'https://publish.buffer.com/calendar/week'
to_upload_folder = r"D:\test400\to_upload"

description_text = "cocovoit"
description_text2 = "#fyp #humour"

# Initialisation de Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")  # Désactive l'accélération GPU
options.add_argument("--disable-software-rasterizer")  # Désactive le rasteriseur logiciel
options.add_argument("--disable-extensions")  # Désactive les extensions
options.add_argument("--no-sandbox")  # Désactive le sandboxing
options.add_argument("--disable-dev-shm-usage")  # Utilisation partagée de la mémoire

# Boucle infinie pour relancer le script en cas d'erreur
while True:
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_window_size(1900, 1000)  # Taille minimale de la fenêtre
        driver.minimize_window()  # Minimise la fenêtre dès que possible

        wait = WebDriverWait(driver, 20)
        
        open_login_page_and_login()
        navigate_to_calendar_and_click()
        upload_video_and_finalize(description_text)
        break  # Si tout se passe bien, on sort de la boucle
    except (WebDriverException, FileNotFoundError, Exception) as e:
        print(f"Erreur rencontrée: {e}. Redémarrage dans 5 secondes...")
        time.sleep(5)