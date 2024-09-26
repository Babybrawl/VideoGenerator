import tkinter as tk
from tkinter import scrolledtext
import threading
from video import process_youtube_video

# Chemins de dossier définis
segments_folder = "segments"
upload_folder = r"D:\test400\to_upload"

def start_processing(video_url, segments_folder, upload_folder, progress_text, stop_event):
    def progress_callback(message, current_part=None, total_parts=None):
        if current_part is not None and total_parts is not None:
            percent = (current_part / total_parts) * 100
            progress_text.insert(tk.END, f"{message} (Progression: {percent:.2f}%)\n")
        else:
            progress_text.insert(tk.END, message + "\n")
        progress_text.see(tk.END)

    # Appeler process_youtube_video avec le bon nombre d'arguments
    process_youtube_video(video_url, segments_folder, upload_folder, progress_callback, stop_event)

def on_start_button_click():
    video_url = video_url_entry.get()
    progress_text.delete(1.0, tk.END)
    stop_event.clear()

    thread = threading.Thread(target=start_processing, args=(video_url, segments_folder, upload_folder, progress_text, stop_event))
    thread.start()

def on_close():
    stop_event.set()
    app.quit()

app = tk.Tk()
app.title("Video Processing Interface")

# Applique un thème moderne et des couleurs personnalisées
app.configure(bg="#2c3e50")

# Labels et champs de saisie
tk.Label(app, text="YouTube Video URL:", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
video_url_entry = tk.Entry(app, width=50, font=("Arial", 12), bd=2, relief="sunken")
video_url_entry.grid(row=0, column=1, padx=10, pady=10)

# Bouton de démarrage
start_button = tk.Button(app, text="Start", command=on_start_button_click, bg="#3498db", fg="#ecf0f1", font=("Arial", 12), bd=2, relief="raised")
start_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)

# Zone de texte pour les messages de progression
progress_text = scrolledtext.ScrolledText(app, height=10, width=70, font=("Courier", 10), bg="#34495e", fg="#ecf0f1", bd=2, relief="sunken")
progress_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Label pour afficher la progression
progress_label = tk.Label(app, text="Progression : 0.00%", bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12))
progress_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Gère la fermeture de la fenêtre
app.protocol("WM_DELETE_WINDOW", on_close)

stop_event = threading.Event()  # Crée l'événement d'arrêt

app.mainloop()
