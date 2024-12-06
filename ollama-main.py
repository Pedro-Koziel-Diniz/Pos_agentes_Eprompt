import os
import json
import uuid
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard
from guardrails.hub import ValidJson
from litellm import completion

load_dotenv()

def resposta_llama_json(especificacoes, response_type=None, model="ollama/llama3.2-vision"):
    # Define as mensagens para o modelo
    messages = [
        {
             "role": "system",
            "content": """
            Você é um nutricionista de alto nível, formado com excelência em Nutrição pela Universidade de Cornell, especializado em compreender e modificar hábitos alimentares para promover saúde e bem-estar. Sua formação sólida e rigorosa alia ciência e prática clínica, explorando profundamente os fatores fisiológicos, comportamentais e emocionais que impactam a nutrição e a qualidade de vida. Em sua carreira, dedica-se a desenvolver, testar e aperfeiçoar estratégias nutricionais baseadas em evidências, com o objetivo de prevenir doenças, tratar condições relacionadas à alimentação e melhorar o desempenho físico e mental de seus pacientes. Com ampla experiência em pesquisa científica, análise de dados nutricionais e publicação de estudos acadêmicos, você contribui para o avanço do conhecimento na área de nutrição e para a evolução de práticas dietéticas inovadoras. Seu trabalho eleva a eficácia dos tratamentos nutricionais, impactando positivamente a saúde pública e transformando vidas por meio de uma alimentação equilibrada e consciente.

            Baseando-se nas informações fornecidas pelo cliente em <Especificações>, você deve:
            - Elaborar uma dieta para cada dia da semana no formato JSON, seguindo o exemplo e fazendo as adaptações necessárias sem inserir nada amais que o JSON como resposta
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

    # Faz a chamada ao modelo
    response = completion(model=model, messages=messages, api_base="http://localhost:11434")
    response_content = response['choices'][0]['message']['content']
    return response_content

especificacoes = input("Insira as informações necessárias para te ajudar a elaborar uma dieta, como seu sexo, idade, altura, peso, estilo de vida e objetivos: ")
validator = resposta_llama_json(especificacoes)

# Diretório onde os arquivos serão salvos
output_directory = "outputs"
os.makedirs(output_directory, exist_ok=True)  # Cria a pasta se ela não existir

# Inicialize o Guard com o validador ValidJson
guard = Guard().use(ValidJson, on_fail="exception")
try:
    # Validação do JSON
    guard.validate(validator)
    response_json = json.loads(validator)
    print("JSON validado com sucesso!")

    # Gerar ID único para a conversa
    conversation_id = str(uuid.uuid4())
    print(f"ID da conversa: {conversation_id}")

    # Salvar o JSON na pasta
    output_filename = os.path.join(output_directory, f"{conversation_id}.json")
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(response_json, json_file, indent=4, ensure_ascii=False)
    print(f"JSON salvo com sucesso em: {output_filename}")

except Exception as e:
    # Gerar ID mesmo em caso de erro para rastreamento
    conversation_id = str(uuid.uuid4())
    print("Erro durante a validação do JSON:")
    print(validator)
    print(f"ID da conversa: {conversation_id}")
    print(f"Detalhes do erro: {e}")
