# Pós Agentes Inteligentes - Eprompt

Repositório dedicado para o trabalho final desenvolvido na discipla de Engenharia de Prompts, da pós graduação de Agentes Inteligentes, pela UFG.

Integrantes: Marcos Vinicius, Pedro Koziel e Wagner Filho.

Trabalho desenvolvido: Elaboração de um auxiliar para planejamento de dietas, com base em informações personalizadas do usuário. Foi realizado um trabalho de Engenharia de Prompt para extrair uma melhor performance dos modelos, em conjunto com o framework Guardrails para garantir que o retorno do modelo seja dentro do padrão esperado. Foi utilizada tanto a API da OpenAI quanto Ollama.

Os slides da apresentação podem ser encontrado em: 

https://www.canva.com/design/DAGYRoext_A/pBs01TCz7FhJF-0hiZnMNg/view?utm_content=DAGYRoext_A&utm_campaign=designshare&utm_medium=link&utm_source=editor  

## Estruturação:

**main.py**: Script principal, que recebe input do usuário, conecta na API da OpenAI, e avalia se o output do modelo é compatível com o fromato json, salvando em um arquivo no diretório "outputs".

**ollama-main.py**: Similar ao main.py, porém utilizando Ollama ao invés da OpenAI.

**generate_image.py**: Utilizando o json gerado, cria a imagem de uma tabela com a dieta, separado por dia da semana.

**generate_pdf.py**: Similar ao generate_image.py, porém cria um pdf ao invés de imagens com a dieta gerada.
