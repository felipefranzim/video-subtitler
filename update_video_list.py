"""Script para atualizar a lista de vídeos no GitHub Pages."""

import os
import json

def update_video_list():
    """Atualiza o arquivo videos.json com os vídeos da pasta output."""
    
    output_dir = "output"
    docs_dir = "docs"
    json_path = os.path.join(docs_dir, "videos.json")
    
    # Garante que a pasta docs existe
    os.makedirs(docs_dir, exist_ok=True)
    
    # Lista vídeos MP4 na pasta output
    videos = []
    
    if os.path.exists(output_dir):
        for filename in sorted(os.listdir(output_dir)):
            if filename.endswith('.mp4'):
                # Remove sufixo _subtitled para o título
                title = filename.replace('_subtitled.mp4', '').replace('_', ' ').title()
                
                videos.append({
                    "title": title,
                    "url": f"../output/{filename}",
                    "description": "Vídeo com legendas em inglês e português"
                })
    
    # Salva o JSON
    data = {"videos": videos}
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Atualizado {json_path} com {len(videos)} vídeo(s)")
    
    for v in videos:
        print(f"   └── {v['title']}")

if __name__ == "__main__":
    update_video_list()
