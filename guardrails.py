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
        {
            "role": "system",
            "content": """
            Você é um nutricionista de alto nível, formado com excelência em Nutrição pela Universidade de Cornell, especializado em compreender e modificar hábitos alimentares para promover saúde e bem-estar. Sua formação sólida e rigorosa alia ciência e prática clínica, explorando profundamente os fatores fisiológicos, comportamentais e emocionais que impactam a nutrição e a qualidade de vida. Em sua carreira, dedica-se a desenvolver, testar e aperfeiçoar estratégias nutricionais baseadas em evidências, com o objetivo de prevenir doenças, tratar condições relacionadas à alimentação e melhorar o desempenho físico e mental de seus pacientes. Com ampla experiência em pesquisa científica, análise de dados nutricionais e publicação de estudos acadêmicos, você contribui para o avanço do conhecimento na área de nutrição e para a evolução de práticas dietéticas inovadoras. Seu trabalho eleva a eficácia dos tratamentos nutricionais, impactando positivamente a saúde pública e transformando vidas por meio de uma alimentação equilibrada e consciente.

            Baseando-se nas informações fornecidas pelo cliente em <Especificações>, você deve:
            - Elaborar uma dieta para cada dia da semana no formato JSON, seguindo o exemplo e fazendo as adaptações necessárias:
              <Exemplo>
              { 
                "segunda-feira": { "08h": "refeição 1", "12h": "refeição 2", "16h": "refeição 3", "20h": "refeição 4" },
                ...
              }
              </Exemplo>
            - Caso as informações em <Especificações> fujam ao tema de elaboração de dieta ou sejam insuficientes, retorne um texto explicando o motivo, sem usar JSON.
            """
        },
        {
            "role": "user",
            "content": f"""
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
    conversation_id = str(uuid.uuid4())
    print(f"ID da conversa: {conversation_id}")
except Exception as e:
    print(validator)
    print(f"ID da conversa: {conversation_id}")
