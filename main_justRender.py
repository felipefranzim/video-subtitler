"""
Video Subtitler - Aplicação principal
Adiciona legendas em inglês (inferior) e português (superior) em vídeos.
"""

import os
import sys
from config.settings import settings
from src.audio_extractor import extract_audio
from src.transcriber import transcribe_audio
from src.translator import translate_segments
from src.subtitle_generator import generate_srt_files
from src.video_renderer import render_subtitles, generate_thumbnail

def process_video(video_path: str) -> str:
    """
    Apenas adiciona legendas a partir de arquivos SRT pré-existentes.
    
    Args:
        video_path: Caminho do vídeo de entrada
        
    Returns:
        Caminho do vídeo processado com legendas
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    print(f"📹 Processando: {video_name}")
    
    
    srt_en_path = os.path.join(settings.TEMP_DIR, f"{video_name}_en.srt")
    srt_pt_path = os.path.join(settings.TEMP_DIR, f"{video_name}_pt.srt")
    
    # Etapa 1: Renderizar legendas no vídeo
    print("🎬 Renderizando vídeo com legendas...")
    output_path = render_subtitles(video_path, srt_en_path, srt_pt_path, video_name)
    
    # Etapa 2: Gerar thumbnail
    print("🖼️ Gerando thumbnail...")
    thumbnail_path = os.path.join(settings.OUTPUT_DIR, f"{video_name}_subtitled.jpg")
    generate_thumbnail(output_path, thumbnail_path)
    
    print(f"✅ Concluído! Vídeo salvo em: {output_path}")
    return output_path

def main():
    """Ponto de entrada da aplicação."""
    if len(sys.argv) < 2:
        print("Uso: python main_justRender.py <caminho_do_video>")
        print("Exemplo: python main_justRender.py input/meu_video.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    try:
        output = process_video(video_path)
        print(f"\n🎉 Processamento concluído com sucesso!")
        print(f"   Arquivo de saída: {output}")
    except Exception as e:
        print(f"\n❌ Erro durante o processamento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()