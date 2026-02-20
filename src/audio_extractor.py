"""Módulo para extrair áudio de arquivos de vídeo."""

from moviepy import VideoFileClip
import os
from config.settings import settings

def extract_audio(video_path: str) -> str:
    """
    Extrai o áudio de um vídeo e salva como MP3.
    
    Args:
        video_path: Caminho do arquivo de vídeo
        
    Returns:
        Caminho do arquivo de áudio extraído
    """
    settings.ensure_dirs()
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(settings.TEMP_DIR, f"{video_name}.mp3")
    
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)
    video.close()
    
    return audio_path