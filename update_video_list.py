"""Script para atualizar a lista de vídeos no GitHub Pages."""

import os
import json

def update_video_list():
    """Atualiza o arquivo videos.json com os vídeos da pasta output."""
    
    output_dir = "output"
    json_path = os.path.join(output_dir, "videos.json")
    
    # Carrega JSON existente (se houver)
    existing_videos = {}
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Cria dicionário para lookup rápido por URL
            for video in data.get("videos", []):
                existing_videos[video["url"]] = video
    
    # Lista vídeos MP4 na pasta output
    videos = []
    new_count = 0
    
    if os.path.exists(output_dir):
        for filename in sorted(os.listdir(output_dir)):
            if filename.endswith('.mp4'):
                # Verifica se já existe no JSON
                if filename in existing_videos:
                    # Mantém o vídeo existente (preserva originalVideo se já definido)
                    videos.append(existing_videos[filename])
                else:
                    # Novo vídeo - adiciona com originalVideo vazio
                    title = filename.replace('_subtitled.mp4', '').replace('_', ' ').title()
                    
                    # Verifica se existe thumbnail correspondente
                    thumbnail_name = filename.replace('.mp4', '.jpg')
                    thumbnail = thumbnail_name if os.path.exists(os.path.join(output_dir, thumbnail_name)) else None
                    
                    videos.append({
                        "title": title,
                        "url": filename,
                        "thumbnail": thumbnail,
                        "description": "Vídeo com legendas em inglês e português",
                        "originalVideo": ""  # Preencher manualmente com a URL do vídeo original
                    })
                    new_count += 1
    
    # Salva o JSON
    data = {"videos": videos}
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Atualizado {json_path}")
    print(f"   Total: {len(videos)} vídeo(s) | Novos: {new_count}")
    
    for v in videos:
        thumb_status = "✓" if v.get("thumbnail") else "✗"
        original_status = "✓" if v.get("originalVideo") else "✗"
        print(f"   └── {v['title']} (thumb: {thumb_status} | original: {original_status})")

if __name__ == "__main__":
    update_video_list()