# Caminho do arquivo
file_path = '10_05Resumo_Contabil_20240511.txt'

# Ler o conteúdo do arquivo
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.readlines()

"""# Função para extrair os nomes
def extrair_nomes(content):
    nomes = []
    for line in content:
        # As linhas com os nomes das pessoas têm um padrão específico,
        # portanto, vamos verificar se elas contêm '/01' e outros identificadores comuns
        if '/01' in line and any(char.isalpha() for char in line):
            partes = line.split()
            # O nome começa na quarta coluna e pode conter mais de um nome
            nome = []
            for parte in partes[3:]:
                if parte.isdigit():  # Se encontrar um número, pare a extração do nome
                    break
                nome.append(parte)
            nomes.append(' '.join(nome).strip())
    return nomes

# Extrair os nomes
nomes = extrair_nomes(content)

# Exibir os nomes
for nome in nomes:
    print(nome)


def extrair_valores(content):
    valores = []
    for line in content:
        if 'DINHEIRO' in line:
            try:
                # Encontre o índice da letra "C" e extraia o valor subsequente
                index_c = line.index('C')
                valor_titulo = line[index_c + 1:].strip().split()[0].replace(',', '.')
                valores.append(valor_titulo)
            except (ValueError, IndexError):
                continue
    return valores

valores = extrair_valores(content)
print("\nValores dos Títulos:")
for valor in valores:
    print(valor)"""


# Função para extrair os nomes
def extrair_nomes_e_valores(content):
    nomes = []
    valores = []

    for line in content:
        # Extrair nomes
        if '/01' in line and any(char.isalpha() for char in line):
            partes = line.split()
            nome = []
            for parte in partes[3:]:
                if parte.isdigit():
                    break
                nome.append(parte)
            nomes.append(' '.join(nome).strip())

        # Extrair valores
        if 'DINHEIRO' in line:
            try:
                index_c = line.index('C')
                valor_titulo = line[index_c + 1:].strip().split()[0].replace(',', '.')
                valores.append(valor_titulo)
            except (ValueError, IndexError):
                continue

    # Associar nomes aos valores na ordem em que foram encontrados
    nome_valor_associado = list(zip(nomes, valores))
    return nome_valor_associado

# Extrair nomes e valores associados
nomes_valores = extrair_nomes_e_valores(content)

# Exibir os nomes e valores associados
for nome, valor in nomes_valores:
    print(f"Nome: {nome} - Valor: {valor}")