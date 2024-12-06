import os
import json
import unicodedata
from PIL import Image, ImageDraw, ImageFont

# Função para normalizar e corrigir acentuação
def normalize_text(text):
    """
    Normaliza um texto para corrigir acentuação e eliminar caracteres inválidos.
    """
    return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")

# Carregar o JSON (substitua pelo caminho correto do seu arquivo)
response_json = json.loads("outputs/uuid.json")

# Diretório para salvar as imagens
output_directory = "imgs"
os.makedirs(output_directory, exist_ok=True)

# Cores e estilos
background_color = (245, 245, 245)
title_color = (40, 40, 120)
text_color = (60, 60, 60)
highlight_color = (220, 220, 250)

for day, meals in response_json.items():
    width, height = 600, 320
    image = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(image)
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        text_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Adicionar título do dia
    title_text = normalize_text(f"{day.capitalize()} - Planejamento Alimentar")
    draw.rectangle([0, 0, width, 70], fill=highlight_color)
    draw.text((20, 20), title_text, fill=title_color, font=title_font)

    # Ajuste do espaço para as refeições
    y_position = 90 
    line_spacing = 40

    # Calcular a altura total disponível para as refeições (depois do título)
    available_height = height - 90

    # Total de linhas para refeições
    total_lines = len(meals) * 2

    # Ajustar o espaçamento se necessário para que o conteúdo caiba
    if total_lines * line_spacing > available_height:
        line_spacing = available_height // total_lines 

    # Adicionar refeições
    for time, meal in meals.items():
        time_text = normalize_text(f"{time}:")
        meal_text = normalize_text(meal)

        # Adicionar horário
        draw.text((20, y_position), time_text, fill=text_color, font=text_font)

        # Adicionar refeição (quebra de linha automática)
        text_bbox = draw.textbbox((0, 0), meal_text, font=text_font)
        text_width = text_bbox[2] - text_bbox[0]
        if text_width > width - 100:
            words = meal_text.split()
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                test_bbox = draw.textbbox((0, 0), test_line, font=text_font)
                test_width = test_bbox[2] - test_bbox[0]
                if test_width < width - 100:
                    line = test_line
                else:
                    draw.text((100, y_position), line, fill=text_color, font=text_font)
                    y_position += line_spacing
                    line = word
            if line:
                draw.text((100, y_position), line, fill=text_color, font=text_font)
        else:
            draw.text((100, y_position), meal_text, fill=text_color, font=text_font)

        y_position += line_spacing

    # Salvar imagem na pasta imgs
    filename = os.path.join(output_directory, f"{day}.png")
    image.save(filename)
    print(f"Imagem salva em: {filename}")