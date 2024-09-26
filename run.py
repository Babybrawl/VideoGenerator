import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.chrome.service import Service

print('=====================================================================================================')
print('Heyy, vous devez vous connecter manuellement sur TikTok, donc le bot attendra 2 minutes pour que vous vous connectiez manuellement !')
print('=====================================================================================================')
time.sleep(8)
print('Exécution du bot maintenant, préparez-vous et connectez-vous manuellement...')
time.sleep(4)

# Configuration du WebDriver Chrome avec gestion automatique de ChromeDriver
options = webdriver.ChromeOptions()
bot = webdriver.Chrome(service=Service(CM().install()), options=options)
bot.set_window_size(1680, 900)

# Ouverture de la page de connexion TikTok
bot.get('https://www.tiktok.com/login')
print('Attente de 120s pour la connexion manuelle...')
time.sleep(120)  # Augmentation du délai pour permettre la connexion manuelle

# Accès à la page de téléchargement de TikTok
bot.get('https://www.tiktok.com/upload/?lang=en')
time.sleep(3)

# Fonction pour vérifier si un élément existe via XPath
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

# Fonction pour uploader une vidéo
def upload(video_path):
    while True:
        try:
            print(f"Tentative d'upload de la vidéo {video_path}...")
            # Sélection du champ de téléchargement
            file_uploader = bot.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[2]/div/div/input')
            file_uploader.send_keys(video_path)

            # Ajouter la légende de la vidéo
            caption = bot.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/span')
            bot.implicitly_wait(10)
            ActionChains(bot).move_to_element(caption).click(caption).perform()

            with open(r"caption.txt", "r") as f:
                tags = [line.strip() for line in f]

            for tag in tags:
                ActionChains(bot).send_keys(tag).perform()
                time.sleep(2)
                ActionChains(bot).send_keys(Keys.RETURN).perform()
                time.sleep(1)

            time.sleep(5)
            bot.execute_script("window.scrollTo(150, 300);")
            time.sleep(5)

            # Poster la vidéo
            post = WebDriverWait(bot, 100).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[5]/button[2]')
                )
            )
            post.click()
            time.sleep(30)

            # Vérifier si un message d'erreur s'affiche
            if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
                print("Erreur rencontrée lors de l'upload, tentative de ré-upload...")
                reupload = WebDriverWait(bot, 100).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')
                    )
                )
                reupload.click()
            else:
                print('Erreur inconnue, attente de 10 minutes avant une nouvelle tentative...')
                time.sleep(600)  # Attendre 10 minutes
                post.click()
                time.sleep(15)

                if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
                    break

        except Exception as e:
            print(f"Erreur lors de l'upload: {e}")
            time.sleep(30)
        else:
            break  # Sortir de la boucle après avoir téléchargé la vidéo avec succès

# Fonction pour déplacer les vidéos uploadées vers un autre dossier
def move_uploaded_videos(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        video_path = os.path.join(source_folder, filename)
        if os.path.isfile(video_path):
            shutil.move(video_path, os.path.join(destination_folder, filename))
            print(f"Vidéo {filename} déplacée vers {destination_folder}.")

# Chemins des dossiers
source_folder = r"D:\test400\to_upload"
destination_folder = r"D:\test400\already_uploaded"

# Création du dossier de destination s'il n'existe pas
os.makedirs(destination_folder, exist_ok=True)

# Téléchargement des vidéos depuis le dossier source
for filename in os.listdir(source_folder):
    video_path = os.path.join(source_folder, filename)
    if os.path.isfile(video_path):
        upload(video_path)
        print(f"Vidéo {filename} téléchargée avec succès.")
        move_uploaded_videos(source_folder, destination_folder)

# Fermeture du bot après l'upload
bot.quit()
