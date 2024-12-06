import os
import json
import unicodedata
from fpdf import FPDF

# Função para normalizar e corrigir acentuação
def normalize_text(text):
    """
    Normaliza um texto para corrigir acentuação e eliminar caracteres inválidos.
    """
    return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")

# Configuração da classe para o PDF
class MealPlanPDF(FPDF):
    def header(self):
        self.set_fill_color(60, 120, 216)  # Azul
        self.set_text_color(255, 255, 255)  # Branco
        self.set_font("Arial", "B", 18)
        self.cell(0, 15, "E-prompts - Planejamento Alimentar Semanal", border=0, ln=True, align="C", fill=True)
        self.ln(10)

    def add_day(self, day, meals):
        # Título do dia com fundo colorido
        self.set_fill_color(220, 220, 220)  # Cinza claro
        self.set_text_color(0, 0, 0)  # Preto
        self.set_font("Arial", "B", 14)
        day_title = normalize_text(f"{day.capitalize()}")
        self.cell(0, 10, day_title, ln=True, align="L", fill=True)
        self.ln(5)

        # Refeições do dia
        self.set_font("Arial", "", 12)
        for time, meal in meals.items():
            # Estilo das células de horário e refeição
            self.set_fill_color(245, 245, 245)  # Fundo branco acinzentado
            self.set_text_color(0, 0, 0)  # Preto
            time_text = normalize_text(f"{time}:")
            meal_text = normalize_text(meal)

            # Horário
            self.cell(30, 10, time_text, border=1, align="L", fill=True)
            # Descrição da refeição
            self.multi_cell(0, 10, meal_text, border=1, align="L", fill=True)
            self.ln(2)  # Espaçamento entre refeições

        # Espaço adicional entre os dias
        self.ln(10)

# Carregar o JSON com as refeições (substitua por seu JSON carregado)
response_json = json.loads("outputs/uuid.json")

# Diretório para salvar o PDF
output_directory = "pdfs"
os.makedirs(output_directory, exist_ok=True)  # Cria a pasta pdfs se não existir

# Gerar o PDF
pdf = MealPlanPDF()
pdf.add_page()

for day, meals in response_json.items():
    pdf.add_day(day, meals)

# Salvar o arquivo na pasta pdfs
output_filename = os.path.join(output_directory, "planejamento_alimentar.pdf")
pdf.output(output_filename)
print(f"PDF gerado em: {output_filename}")
