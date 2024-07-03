# Caminho do arquivo
file_path = 'arquivos txts\\06_05Resumo_Contabil_20240508 (1).txt'

# Ler o conteúdo do arquivo
with open(file_path, 'r', encoding='utf-8') as file:
    content_txt = content = file.readlines()

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
        if '/01' in line and any(char.isalpha() for char in line):
            partes = line.split()
            nome = []
            for parte in partes[3:]:
                if parte.replace('.', '').replace(',', '').isdigit():
                    break
                nome.append(parte)
            nomes.append(' '.join(nome).strip())
            # Verificar linha seguinte para o valor
            next_line_index = content.index(line) + 1
            if next_line_index < len(content):
                next_line = content[next_line_index]
                if 'DINHEIRO' in next_line or 'D ' in next_line:
                    try:
                        if 'C' in next_line:
                            index_c = next_line.index('C')
                            valor_titulo = next_line[index_c + 1:].strip().split()[0].replace(',', '.')
                        elif 'D ' in next_line:
                            index_d = next_line.index('D ')
                            valor_titulo = next_line[index_d + 1:].strip().split()[0].replace(',', '.')
                        else:
                            continue
                        valores.append(valor_titulo)
                    except (ValueError, IndexError):
                        valores.append("Valor não encontrado")
                else:
                    valores.append("Valor não encontrado")
            else:
                valores.append("Valor não encontrado")
    return list(zip(nomes, valores))

nomes_valores = extrair_nomes_e_valores(content_txt)
for nome, valor in nomes_valores:
    print(f"Nome: {nome}, Valor: {valor}")
print(len(nomes_valores))

