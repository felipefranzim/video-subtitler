"""Módulo para geração de arquivos SRT."""

import srt
from datetime import timedelta
from typing import List
from src.translator import SubtitlePair
import os
from config.settings import settings

def generate_srt_files(pairs: List[SubtitlePair], base_name: str) -> tuple[str, str]:
    """
    Gera arquivos SRT para inglês e português.
    
    Args:
        pairs: Lista de pares de legendas
        base_name: Nome base para os arquivos
        
    Returns:
        Tupla com caminhos dos arquivos SRT (inglês, português)
    """
    settings.ensure_dirs()
    
    srt_en_path = os.path.join(settings.TEMP_DIR, f"{base_name}_en.srt")
    srt_pt_path = os.path.join(settings.TEMP_DIR, f"{base_name}_pt.srt")
    
    subs_en = []
    subs_pt = []
    
    for idx, pair in enumerate(pairs, 1):
        start = timedelta(seconds=pair.start)
        end = timedelta(seconds=pair.end)
        
        subs_en.append(srt.Subtitle(
            index=idx,
            start=start,
            end=end,
            content=pair.text_en
        ))
        
        subs_pt.append(srt.Subtitle(
            index=idx,
            start=start,
            end=end,
            content=pair.text_pt
        ))
    
    with open(srt_en_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs_en))
    
    with open(srt_pt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs_pt))
    
    return srt_en_path, srt_pt_path