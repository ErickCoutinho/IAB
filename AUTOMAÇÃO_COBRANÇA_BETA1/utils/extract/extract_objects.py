import re
from datetime import datetime

file_path = '../../documents/txts/12_07Resumo_Contabil_20240717.txt'


def ler_arquivo(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
        return content
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return []


def extrair_nomes(content):
    nomes_extraidos = {}  # Dicionário para armazenar a linha e o nome correspondente

    for i, line in enumerate(content):
        if ('/01' in line or '/00' in line) and any(char.isalpha() for char in line):  # Verifica se a linha contém '/01' e letras
            try:
                partes = line.split()
                nome = []
                for parte in partes[3:]:
                    if parte.replace(',', '').replace('.',
                                                      '').isdigit():
                        break
                    nome.append(parte)
                nome = ' '.join(nome).strip()
                if nome:
                    nomes_extraidos[i + 1] = nome  # Armazena a linha (chave) e o nome (valor) no dicionário
            except Exception as e:
                continue

    return nomes_extraidos


def extrair_valores(content):
    try:
        valores_c = {}
        valores_g = {}
        valores_j = {}
        valores_d = {}

        for i, line in enumerate(content):
            if '/01' in line or '/00' in line:
                try:
                    next_line_index = i + 1
                    if next_line_index < len(content):
                        next_line = content[next_line_index].strip()
                        try:
                            # Limitar a busca entre os caracteres 14 e 40
                            substring = next_line[11:35]
                            if 'C' in substring:
                                index_c = substring.index('C') + 14  # Corrige o índice para o próximo uso
                                if next_line[index_c + 1].isspace() or next_line[index_c + 1].isdigit():
                                    valor_c = next_line[index_c + 1:].strip().split()[0].replace(',', '.')
                                    valores_c[next_line_index + 1] = valor_c
                            if 'G' in substring:
                                index_g = substring.index('G') + 14
                                if next_line[index_g + 1].isspace() or next_line[index_g + 1].isdigit():
                                    valor_g = next_line[index_g + 1:].strip().split()[0].replace(',', '.')
                                    valores_g[next_line_index + 1] = valor_g
                            if 'J' in substring:
                                index_j = substring.index('J') + 14
                                if next_line[index_j + 1].isspace() or next_line[index_j + 1].isdigit():
                                    valor_j = next_line[index_j + 1:].strip().split()[0].replace(',', '.')
                                    valores_j[next_line_index + 1] = valor_j
                            if 'D' in substring:
                                index_d = substring.index('D') + 14
                                if next_line[index_d + 1].isspace() or next_line[index_d + 1].isdigit():
                                    valor_d = next_line[index_d + 1:].strip().split()[0].replace(',', '.')
                                    valores_d[next_line_index + 1] = valor_d
                        except (ValueError, IndexError):
                            continue
                except Exception as e:
                    print(f"Erro ao extrair valores: {str(e)}")
                    continue
        return valores_c, valores_g, valores_j, valores_d
    except Exception as e:
        print(f"Erro ao extrair valores do arquivo: {str(e)}")
        return {}, {}, {}, {}


def extrair_taxas_bancarias(content):
    taxas_bancarias = {}  # Dicionário para armazenar as taxas bancárias com o número da linha como chave

    for i, line in enumerate(content):
        # expressão regular
        match_41 = re.search(r'41\s+(\d+,\d+)', line)
        if match_41:
            valor_41 = float(match_41.group(1).replace(',', '.'))
            taxas_bancarias[i + 1] = valor_41  # Armazena o valor no dicionário com a linha correspondente como chave

    return taxas_bancarias


def extrair_juros(content):
    juros = {}  # Dicionário para armazenar os juros com o número da linha como chave
    for i, line in enumerate(content):
        # expressão regularo
        match_07 = re.search(r'07\s+(\d+,\d+)', line)
        if match_07:
            # Extrair o valor encontrado após o código "07" e converter para float
            valor_07 = float(match_07.group(1).replace(',', '.'))
            juros[i + 1] = valor_07  # Armazena o valor no dicionário com a linha + 1 como chave

    return juros



def extrair_data_posicao(content):
    """
    Função para extrair a data de posição do arquivo.
    Procura pela linha que contém 'POSICAO DO DIA:' e extrai a data.
    """
    data_posicao = None
    for line in content:
        if 'POSICAO DO DIA:' in line:
            try:
                # Pega a parte da linha após 'POSICAO DO DIA:'
                data_posicao = line.split(':')[-1].strip()
                # Converte a string da data no formato "%d/%m/%Y"
                data_posicao = datetime.strptime(data_posicao, "%d/%m/%Y")
                break

            except (IndexError, ValueError) as e:
                print(f"Erro ao extrair data de posição: {str(e)}")
                continue  # Continua se houver erro na extração ou conversão
    return data_posicao


def extrair_data_vencimento(content):
    """
    Função para extrair a data de vencimento de cada linha, pegando a substring entre os caracteres 64 e 74.
    Se a data não for encontrada ou a conversão falhar, a função pula para a próxima linha.
    """
    datas_vencimento = {}  # Dicionário para armazenar as datas de vencimento com o número da linha como chave

    for i, line in enumerate(content):
        try:
            # Verificar se a linha tem comprimento suficiente
            if len(line) >= 74:
                # Extrair a substring dos caracteres 64 a 74
                data_vencimento_str = line[64:74].strip()  # Pegar a data e remover espaços em branco

                # Converter a data de vencimento para o formato datetime
                data_vencimento = datetime.strptime(data_vencimento_str, "%d/%m/%Y")

                # Armazenar a data no formato dd/mm/yyyy no dicionário
                datas_vencimento[i + 1] = data_vencimento.strftime("%d/%m/%Y")

        except (ValueError, IndexError) as e:
            continue

    return datas_vencimento


