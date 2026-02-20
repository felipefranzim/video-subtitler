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
    Processa um vídeo completo: transcreve, traduz e adiciona legendas.
    
    Args:
        video_path: Caminho do vídeo de entrada
        
    Returns:
        Caminho do vídeo processado com legendas
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    print(f"📹 Processando: {video_name}")
    
    # Etapa 1: Extrair áudio
    print("🎵 Extraindo áudio...")
    audio_path = extract_audio(video_path)
    
    # Etapa 2: Transcrever áudio (inglês)
    print("📝 Transcrevendo áudio...")
    segments = transcribe_audio(audio_path)
    print(f"   └── {len(segments)} segmentos encontrados")
    
    # Etapa 3: Traduzir para português
    print("🌐 Traduzindo para português...")
    subtitle_pairs = translate_segments(segments)
    
    # Etapa 4: Gerar arquivos SRT
    print("📄 Gerando arquivos de legenda...")
    srt_en, srt_pt = generate_srt_files(subtitle_pairs, video_name)
    
    # Etapa 5: Renderizar legendas no vídeo
    print("🎬 Renderizando vídeo com legendas...")
    output_path = render_subtitles(video_path, srt_en, srt_pt, video_name)
    
    # Etapa 6: Gerar thumbnail
    print("🖼️ Gerando thumbnail...")
    thumbnail_path = os.path.join(settings.OUTPUT_DIR, f"{video_name}_subtitled.jpg")
    generate_thumbnail(output_path, thumbnail_path)
    
    print(f"✅ Concluído! Vídeo salvo em: {output_path}")
    return output_path

def main():
    """Ponto de entrada da aplicação."""
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_video>")
        print("Exemplo: python main.py input/meu_video.mp4")
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