import os
import openai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard

def resposta_gpt_json(prompt, response_type=None, model="gpt-4o-mini"):
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    messages = [
        {
            "role": "system",
            "content": """Você é um nutricionista especializado em elaborar dietas com base nas informações fornecidas pelo cliente.
                          Adapte informações como quais alimentos, quantidades e quantas vezes por dia com base nas informações fornecidas.
                          Você deve retornar apenas o plano de dieta, que deve ser no formato de JSON. Seja bem específico e claro."""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = client.chat.completions.create(model=model, messages=messages, temperature=1)
    response_content = response.choices[0].message.content
    return  response_content

prompt = """
Elabore um plano alimentar para uma pessoa de 30 anos, sexo feminino, que pratica exercícios físicos 5 vezes por semana.
A pessoa deseja perder peso, consome aproximadamente 1500 calorias por dia e prefere evitar glúten e lactose.
Inclua 5 refeições diárias com opções variadas e claras, incluindo frutas, vegetais, proteínas magras e gorduras boas.
"""
validator = resposta_gpt_json(prompt)

# Modelo Pydantic para validar a saída
class DietPlan(BaseModel):
    meals: list = Field(
        ..., description="Lista de refeições diárias, cada uma com alimentos e quantidades"
    )
    calories: int = Field(..., description="Total de calorias no plano")
    preferences: dict = Field(
        ..., description="Restrições ou preferências alimentares (ex.: sem glúten)"
    )
from guardrails import Guard
# Definir Guardrails com Pydantic
guard = Guard.from_pydantic(DietPlan)

try:
    from guardrails import Guard
    res = guard.validate(validator)
    print("Valid JSON passed validation.")
except Exception as e:
    print(f"Validation failed: {e}")