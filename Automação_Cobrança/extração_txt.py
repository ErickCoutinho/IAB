import re


# Caminho do arquivo
file_path = 'arquivos txts\\julho\\12_07Resumo_Contabil_20240717.txt'

# Ler o conteúdo do arquivo
with open(file_path, 'r', encoding='utf-8') as file:
    content_txt = content = file.readlines()

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
"""for nome, valor in nomes_valores:
    print(f"Nome: {nome}, Valor: {valor}")
print(len(nomes_valores))"""


def extrair_e_somar_duplas(content):
    resultados = []
    i = 0
    while i < len(content):
        line = content[i]
        if '/01' in line and any(char.isalpha() for char in line):
            partes = line.split()
            nome = []
            for parte in partes[3:]:
                if parte.isdigit() or re.match(r'\d+,\d+', parte):
                    break
                nome.append(parte)
            nome = ' '.join(nome).strip()

            # Procurar valores nas linhas subsequentes
            valor_41 = valor_07 = 0

            # Procurar o valor após "07"
            if i + 1 < len(content):
                proxima_linha = content[i + 1]
                match_07 = re.search(r'07\s+(\d+,\d+)', proxima_linha)
                if match_07:
                    valor_07 = float(match_07.group(1).replace(',', '.'))

            # Procurar o valor após "41"
            if i + 2 < len(content):
                proxima_linha = content[i + 2]
                match_41 = re.search(r'41\s+(\d+,\d+)', proxima_linha)
                if match_41:
                    valor_41 = float(match_41.group(1).replace(',', '.'))

            soma = valor_41 + valor_07
            resultados.append((nome, f"{soma:.2f}"))

        i += 1

    return resultados


resultados = extrair_e_somar_duplas(content_txt)
for nome, soma in resultados:
    print(f"Nome: {nome}, Soma: {soma}")
