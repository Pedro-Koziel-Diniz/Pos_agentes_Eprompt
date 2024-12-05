import os
import openai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard

load_dotenv()

def resposta_gpt_json(especificacoes, response_type=None, model="gpt-4o-mini"):
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY")

    messages = [
    {"role": "system", "content": """Você é um nutricionista especializado em elaborar dietas com base nas informações fornecidas pelo cliente.
                                     Adapte informações como quais alimentos, quantidades e quantas vezes por dia com base nas informações fornecidas, delimitadas por <Especificações>.
                                     Caso as informações em Especificações fujam ao tema de elaboração de dieta ao sejam insuficientes, retorne um texto corrido (sem ser em json) explicando o motivo.
                                     Você deve retornar apenas o plano de dieta para cada dia da semana, que deve ser no formato de JSON, seguindo o exemplo delimitado por <Exemplo> e adaptando conforme necessário.
                                     <Exemplo>
                                        {
                                            segunda {
                                                                8h: <refeição 1>,
                                                                12h: <refeição 2>,
                                                                16h: <refeição 3>,
                                                                20h: <refeição 4>, etc
                                    </Exemplo> """},

    {"role": "user", "content": f"""
      <Especificações>
      {especificacoes}
      </Especificações>
      """
      }
]
    response = client.chat.completions.create(model=model, messages=messages, temperature=1)
    response_content = response.choices[0].message.content
    return  response_content

especificacoes = input("Insira as informações necessárias para te ajudar a elaborar uma dieta, como seu sexo, idade, altura, peso, estilo de vida e objetivos: ")

validator = resposta_gpt_json(especificacoes)

# Inicialize o Guard com o ValidJson
guard = Guard().use(ValidJson, on_fail="exception")
try:
    guard.validate(validator)
    response_json = json.loads(validator)
    print(response_json)
except Exception as e:
    print(validator)
