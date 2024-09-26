import os
import shutil
import random
import string
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, clips_array
import yt_dlp

def download_first_video_from_url(video_url, progress_callback):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'outtmpl': 'downloaded_video.mp4',
    }

    progress_callback("Téléchargement de la vidéo...")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    return "downloaded_video.mp4"

def cut_video_in_segments(video_path, segment_duration=70, progress_callback=None):
    video = VideoFileClip(video_path)
    duration = video.duration
    segment_paths = []

    progress_callback("Découpage de la vidéo en segments...")
    
    for i in range(0, int(duration), segment_duration):
        start_time = i
        end_time = min(i + segment_duration, duration)
        output_filename = f"segment_{i // segment_duration + 1}.mp4"
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_filename)
        segment_paths.append(output_filename)
    
    return segment_paths

def resize_and_crop_video(video_path, target_width=1080, target_height=960):
    video = VideoFileClip(video_path)
    video_resized = video.resize(height=target_height)
    if video_resized.w > target_width:
        x_center = video_resized.w // 2
        video_cropped = video_resized.crop(x_center=x_center, width=target_width)
    else:
        video_cropped = video_resized
    return video_cropped

def select_random_satisfying_video(segments_folder):
    segment_videos = [f for f in os.listdir(segments_folder) if f.endswith(".mp4")]
    
    if not segment_videos:
        raise Exception(f"Aucune vidéo trouvée dans le dossier {segments_folder}.")
    
    selected_video = random.choice(segment_videos)
    return os.path.join(segments_folder, selected_video)

def generate_random_filename(part_number):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{random_string}_partie{part_number}.mp4"

def combine_with_satisfying_video(main_video_path, satisfying_video_path, part_number):
    main_video = resize_and_crop_video(main_video_path, target_width=1080, target_height=960)
    satisfying_video = resize_and_crop_video(satisfying_video_path, target_width=1080, target_height=960)
    final_video = clips_array([[main_video], [satisfying_video]])

    final_video_with_text = final_video.resize(newsize=(1080, 1920))
    
    output_filename = generate_random_filename(part_number)
    final_video_with_text.write_videofile(output_filename, fps=24, codec='libx264', bitrate='5000k')
    
    return output_filename

def clean_up_temp_files(files_to_delete):
    for temp_file in files_to_delete:
        try:
            if os.path.isfile(temp_file):
                os.remove(temp_file)
                print(f"Fichier temporaire supprimé: {temp_file}")
            else:
                print(f"Le fichier {temp_file} n'existe pas ou a déjà été supprimé.")
        except Exception as e:
            print(f"Erreur lors de la suppression de {temp_file}: {e}")

def process_youtube_video(video_url, segments_folder, upload_folder, progress_callback, stop_event):
    video_path = download_first_video_from_url(video_url, progress_callback)

    segments = cut_video_in_segments(video_path, progress_callback=progress_callback)

    part_number = 1
    total_parts = len(segments)  # Total des segments
    temp_files = [video_path]

    for segment in segments:
        if stop_event.is_set():
            progress_callback("Processus arrêté.")
            return

        progress_callback(f"Traitement du segment {part_number}...", part_number, total_parts)

        satisfying_segment = select_random_satisfying_video(segments_folder)

        final_video = combine_with_satisfying_video(segment, satisfying_segment, part_number)

        final_video_path = os.path.join(upload_folder, final_video)
        shutil.move(final_video, final_video_path)
        progress_callback(f"Vidéo finale {part_number} déplacée vers {upload_folder}: {final_video_path}", part_number, total_parts)

        part_number += 1
        temp_files.append(segment)

        if stop_event.is_set():
            progress_callback("Processus arrêté pendant le traitement.")
            return

    progress_callback("Nettoyage des fichiers temporaires...", part_number, total_parts)
    clean_up_temp_files(temp_files)

    progress_callback("Lancement de run2.py...", part_number, total_parts)
    subprocess.run(["python", "d:/test400/run2.py"], check=True)