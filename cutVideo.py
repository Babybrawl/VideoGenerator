import os
import math
from moviepy.editor import VideoFileClip
import yt_dlp

def download_video(video_url, output_filename="downloaded_video.mp4"):
    """
    Télécharge la vidéo à partir d'un lien YouTube et la sauvegarde dans le fichier output_filename.
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_filename,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    return output_filename

def get_next_segment_number(segments_folder):
    """
    Retourne le numéro du prochain segment en fonction du nombre de fichiers existants dans le dossier segments.
    """
    if not os.path.exists(segments_folder):
        os.makedirs(segments_folder)
        return 1

    # Liste tous les fichiers du dossier et filtre ceux qui se terminent par .mp4
    existing_files = [f for f in os.listdir(segments_folder) if f.endswith(".mp4")]
    
    if not existing_files:
        return 1

    # Extraire les numéros de fichier et trouver le plus grand
    existing_numbers = [int(f.split('.')[0]) for f in existing_files]
    return max(existing_numbers) + 1

def cut_video_in_segments(video_path, segment_duration=70, start_number=1):
    """
    Découpe la vidéo en segments de segment_duration secondes.
    Numérote chaque segment à partir de start_number et les sauvegarde dans un seul dossier.
    """
    video = VideoFileClip(video_path)
    video_duration = video.duration
    num_segments = math.floor(video_duration / segment_duration)
    
    output_folder = "segments"  # Dossier où les vidéos seront stockées
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Découpe des segments et suppression du son
    current_segment = start_number

    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = start_time + segment_duration

        # Nom du fichier vidéo numéroté
        output_filename = os.path.join(output_folder, f"{current_segment}.mp4")
        video_segment = video.subclip(start_time, end_time).without_audio()

        # Sauvegarder la vidéo sans son
        video_segment.write_videofile(output_filename, codec='libx264', audio=False, fps=24)
        print(f"Segment {current_segment}.mp4 sauvegardé sans son dans le dossier {output_folder}")
        current_segment += 1

    # Fermeture explicite de la vidéo pour éviter des erreurs lors de la suppression
    video.close()

    print(f"Total {current_segment - start_number} segments créés.")

def process_video_from_url(video_url):
    """
    Télécharge une vidéo à partir d'un lien YouTube, puis la découpe en segments de 70 secondes sans son.
    Les segments sont numérotés à partir du numéro calculé selon le contenu du dossier.
    """
    # Téléchargement de la vidéo
    print("Téléchargement de la vidéo...")
    downloaded_video = download_video(video_url)

    # Calcul du start_number basé sur les vidéos déjà présentes
    start_number = get_next_segment_number("segments")
    print(f"Numéro de segment de départ : {start_number}")

    # Découpage en segments sans son
    print("Découpage de la vidéo en segments de 1min10 sans son...")
    cut_video_in_segments(downloaded_video, segment_duration=70, start_number=start_number)

    # Optionnel : supprimer la vidéo téléchargée après découpage
    if os.path.exists(downloaded_video):
        os.remove(downloaded_video)
        print(f"Vidéo téléchargée supprimée : {downloaded_video}")
    else:
        print(f"Impossible de trouver la vidéo téléchargée pour la supprimer : {downloaded_video}")

# Exemple d'utilisation :
video_url = "https://www.youtube.com/watch?v=VS3D8bgYhf4"  # Remplacez par le lien de la vidéo

process_video_from_url(video_url)
