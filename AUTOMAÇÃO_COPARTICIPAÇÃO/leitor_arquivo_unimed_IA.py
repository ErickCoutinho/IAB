import spacy

# Carregar modelo de NER pré-treinado do spaCy
nlp = spacy.load("pt_core_news_sm")

# Leitura do arquivo
file_path = "documents/PART 07.LST"

# Inicialização de variáveis
valores_por_pessoa = {}
nome_atual = None

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Processar o texto com o spaCy
doc = nlp(content)

# Iterar sobre as entidades identificadas
for ent in doc.ents:
    # Identificar entidades de pessoas
    if ent.label_ == "PER":
        nome_atual = ent.text
        if nome_atual not in valores_por_pessoa:
            valores_por_pessoa[nome_atual] = 0.0
    # Identificar valores monetários e associá-los ao nome atual
    elif ent.label_ == "MONEY" and nome_atual:
        valor_part_cobrado_str = ent.text.replace(",", ".").replace("R$", "").strip()
        valor_part_cobrado = float(valor_part_cobrado_str)
        valores_por_pessoa[nome_atual] += valor_part_cobrado

# Exibir os resultados finais
for nome, valor in valores_por_pessoa.items():
    print(f"{nome}: {valor:.2f}")
