"""Módulo para tradução de texto usando OpenAI GPT."""

from openai import OpenAI
from config.settings import settings
from typing import List
from src.transcriber import TranscriptionSegment
from dataclasses import dataclass

@dataclass
class SubtitlePair:
    """Par de legendas em inglês e português."""
    start: float
    end: float
    text_en: str
    text_pt: str

def translate_segments(segments: List[TranscriptionSegment]) -> List[SubtitlePair]:
    """
    Traduz segmentos de inglês para português.
    
    Args:
        segments: Lista de segmentos transcritos em inglês
        
    Returns:
        Lista de pares de legendas (inglês + português)
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    subtitle_pairs = []
    
    # Processar em lotes para eficiência
    batch_size = 10
    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]
        
        # Preparar texto para tradução em lote
        texts_to_translate = "\n".join([
            f"{idx}. {seg.text}" 
            for idx, seg in enumerate(batch, 1)
        ])
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Você é um tradutor profissional de inglês para português brasileiro.
                    Traduza cada linha mantendo a numeração. Seja natural e fluente.
                    Mantenha o formato: número. tradução"""
                },
                {
                    "role": "user",
                    "content": f"Traduza estas frases:\n{texts_to_translate}"
                }
            ],
            temperature=0.3
        )
        
        # Parsear resposta
        translations = response.choices[0].message.content.strip().split("\n")
        translations = [t.split(". ", 1)[-1] if ". " in t else t for t in translations]
        
        for seg, translation in zip(batch, translations):
            subtitle_pairs.append(SubtitlePair(
                start=seg.start,
                end=seg.end,
                text_en=seg.text,
                text_pt=translation.strip()
            ))
    
    return subtitle_pairs