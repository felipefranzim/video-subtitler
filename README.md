# AI Video Subtitler

Objetivo do projeto:

- Extrair áudio do vídeo
- Transcrever o arquivo de áudio usando a API Whisper da OpenAI
- Traduzir os segmentos de inglês para português utilizando GPT4
- Renderizar os frames do vídeo com as legendas em inglês e português de forma simultânea

## Pré-requisitos de Instalação

1. FFmpeg (obrigatório)

**Windows:**

```
# Via Chocolatey
choco install ffmpeg

# Ou via Scoop
scoop install ffmpeg
```

**Verificar instalação:**

```
ffmpeg -version
```

2. Python e Dependências

```
# Criar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate

# Instalar dependências
pip install -r requirements.txt

```

## Como usar

```
# 1. Configurar API Key
cp .env.example .env
# Editar .env e adicionar sua OPENAI_API_KEY

# 2. Colocar vídeo na pasta input/
# 3. Executar
python main.py input/seu_video.mp4
```