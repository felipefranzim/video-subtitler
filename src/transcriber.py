"""Módulo para transcrição de áudio usando OpenAI Whisper."""

from openai import OpenAI
from config.settings import settings
from dataclasses import dataclass
from typing import List

@dataclass
class TranscriptionSegment:
    """Representa um segmento de transcrição com timestamps."""
    start: float  # Tempo de início em segundos
    end: float    # Tempo de fim em segundos
    text: str     # Texto transcrito

def transcribe_audio(audio_path: str) -> List[TranscriptionSegment]:
    """
    Transcreve um arquivo de áudio usando a API Whisper da OpenAI.
    
    Args:
        audio_path: Caminho do arquivo de áudio
        
    Returns:
        Lista de segmentos com timestamps e texto
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    
    segments = []
    for segment in response.segments:
        segments.append(TranscriptionSegment(
            start=segment.start,
            end=segment.end,
            text=segment.text.strip()
        ))
    
    return segments