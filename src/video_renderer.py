"""Módulo para renderizar legendas no vídeo usando FFmpeg."""

import subprocess
import os
from config.settings import settings

def escape_ffmpeg_path(path: str) -> str:
    """
    Escapa um caminho para uso nos filtros do FFmpeg no Windows.
    - Converte para caminho absoluto
    - Usa barras normais (/)
    - Escapa dois pontos (:) e barras invertidas
    """
    abs_path = os.path.abspath(path)
    # Substitui barras invertidas por barras normais
    escaped = abs_path.replace("\\", "/")
    # Escapa os dois pontos (C: -> C\:)
    escaped = escaped.replace(":", "\\:")
    return escaped

def generate_thumbnail(video_path: str, output_path: str, time_seconds: int = 30) -> str:
    """
    Gera uma thumbnail do vídeo.
    
    Args:
        video_path: Caminho do vídeo
        output_path: Caminho de saída da thumbnail (jpg)
        time_seconds: Momento do vídeo para capturar (padrão: 5s)
        
    Returns:
        Caminho da thumbnail gerada
    """
    cmd = [
        settings.FFMPEG_PATH,
        "-i", video_path,
        "-ss", str(time_seconds),
        "-vframes", "1",
        "-q:v", "2",  # Qualidade (2 = alta, menor arquivo)
        "-y",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        # Se falhar no tempo especificado, tenta no início
        cmd[4] = "0"
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg thumbnail error: {result.stderr}")
    
    return output_path

def render_subtitles(
    video_path: str,
    srt_en_path: str,
    srt_pt_path: str,
    output_name: str
) -> str:
    """
    Renderiza duas legendas no vídeo: português em cima, inglês embaixo.
    
    Args:
        video_path: Caminho do vídeo original
        srt_en_path: Caminho do SRT em inglês
        srt_pt_path: Caminho do SRT em português
        output_name: Nome do arquivo de saída
        
    Returns:
        Caminho do vídeo com legendas
    """
    settings.ensure_dirs()
    
    output_path = os.path.join(settings.OUTPUT_DIR, f"{output_name}_subtitled.mp4")
    
    # Escapar caminhos dos arquivos SRT para FFmpeg
    srt_pt_escaped = escape_ffmpeg_path(srt_pt_path)
    srt_en_escaped = escape_ffmpeg_path(srt_en_path)
    
    # Configuração de estilo das legendas
    style_pt = (
        f"FontSize={settings.FONT_SIZE_TOP},"
        f"PrimaryColour=&H00FFFF&,"  # Amarelo (BGR)
        f"OutlineColour=&H000000&,"
        f"BorderStyle=3,"
        f"Outline=2,"
        f"Shadow=1,"
        f",Alignment=2," # Inferior, centralizado horizontalmente
        f"MarginV=60"  # Posição superior
    )
    
    style_en = (
        f"FontSize={settings.FONT_SIZE_BOTTOM},"
        f"PrimaryColour=&H00FFFFFF&,"  # Branco
        f"OutlineColour=&H000000&,"
        f"BorderStyle=3,"
        f"Outline=2,"
        f"Shadow=1,"
        f",Alignment=2," # Inferior, centralizado horizontalmente
        f"MarginV=20"  # Posição inferior (padrão)
    )
    
    # Comando FFmpeg com duas legendas
    # A primeira legenda (português) é posicionada no topo
    # A segunda legenda (inglês) fica na posição padrão (embaixo)
    filter_complex = (
        f"subtitles='{srt_pt_escaped}':force_style='{style_pt}',"
        f"subtitles='{srt_en_escaped}':force_style='{style_en}'"
    )
    
    cmd = [
        settings.FFMPEG_PATH,
        "-i", video_path,
        "-vf", filter_complex,
        "-c:a", "copy",
        "-y",  # Sobrescrever se existir
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")
    
    return output_path