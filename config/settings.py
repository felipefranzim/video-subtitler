import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    FFMPEG_PATH: str = os.getenv("FFMPEG_PATH", r"C:\ProgramData\chocolatey\bin\ffmpeg.exe")
    INPUT_DIR: str = "input"
    OUTPUT_DIR: str = "output"
    TEMP_DIR: str = "temp"
    
    # Configurações de legenda
    FONT_SIZE_TOP: int = 16  # Português (superior)
    FONT_SIZE_BOTTOM: int = 20  # Inglês (inferior)
    FONT_COLOR_TOP: str = "yellow"
    FONT_COLOR_BOTTOM: str = "white"
    
    @classmethod
    def ensure_dirs(cls):
        for d in [cls.INPUT_DIR, cls.OUTPUT_DIR, cls.TEMP_DIR]:
            os.makedirs(d, exist_ok=True)

settings = Settings()