from utils.extract.extract_objects import extrair_valores, extrair_nomes, ler_arquivo, extrair_juros, \
    extrair_taxas_bancarias, extrair_data_vencimento
from utils.auxiliary.functions import limpar_valor, buscar_taxa_bancaria, buscar_juros

file_path = "../../documents/txts/12_07Resumo_Contabil_20240717.txt"


def associar_nomes_valores_pagos(file_path):
    try:
        content = ler_arquivo(file_path)

        # Extrair nomes e seus índices (como um dicionário: {linha: nome})
        nomes_dict = extrair_nomes(content)

        # Extrair valores 'C' e taxas bancárias
        valores_c, _, _, _ = extrair_valores(content)
        taxas_bancarias = extrair_taxas_bancarias(content)

        # Dicionário para armazenar a associação entre nome e o valor somado (C + taxa)
        associacoes = {}

        # Iterar sobre o dicionário de nomes (linha: nome)
        for linha, nome in nomes_dict.items():
            indice_valor = linha + 1  # Ajustar o índice do valor (é 1 a mais que o índice do nome)
            # Verificar se há valor 'C' para o índice correspondente
            valor_c = valores_c.get(indice_valor, '0')  # Pegar o valor 'C', ou '0' se não existir
            # Verificar se há taxa bancária para o índice correspondente ou buscar nos próximos índices
            taxa_bancaria = taxas_bancarias.get(indice_valor, '0')  # Pegar a taxa bancária, ou '0' se não existir
            if taxa_bancaria == '0':  # Se a taxa não for encontrada, buscar nos índices subsequentes
                taxa_bancaria = buscar_taxa_bancaria(indice_valor, taxas_bancarias, nomes_dict)
            # Limpar e converter os valores para float usando o método separado
            valor_total = limpar_valor(valor_c) + limpar_valor(taxa_bancaria)
            # Associar o nome ao valor total no dicionário
            associacoes[nome] = valor_total
        return associacoes  # Retorna o dicionário de associações entre nome e valor somado (C + taxa)

    except Exception as e:
        print(f"Erro ao associar nomes e valores: {str(e)}")
        return {}


def associar_nomes_juros(file_path):
    try:
        content = ler_arquivo(file_path)
        # Extrair nomes e seus índices (como um dicionário: {linha: nome})
        nomes_dict = extrair_nomes(content)
        # Extrair juros
        juros_dict = extrair_juros(content)
        # Dicionário para armazenar a associação entre nome e os juros
        associacoes = {}
        # Iterar sobre o dicionário de nomes (linha: nome)
        for linha, nome in nomes_dict.items():
            indice_valor = linha + 1  # Ajustar o índice do valor (é 1 a mais que o índice do nome)

            # Verificar se há juros para o índice correspondente ou buscar nos próximos índices
            juros = juros_dict.get(indice_valor, '0')  # Pegar os juros, ou '0' se não existir
            if juros == '0':  # Se os juros não forem encontrados, buscar nos índices subsequentes
                juros = buscar_juros(indice_valor, juros_dict, nomes_dict)
            # Limpar e converter os valores para float usando o método separado
            juros_total = limpar_valor(juros)
            # Associar o nome aos juros no dicionário
            associacoes[nome] = juros_total
        return associacoes  # Retorna o dicionário de associações entre nome e juros

    except Exception as e:
        print(f"Erro ao associar nomes e juros: {str(e)}")
        return {}


def associar_nomes_datas_vencimento(file_path):
    try:
        content = ler_arquivo(file_path)
        nomes_dict = extrair_nomes(content)
        datas_vencimento_dict = extrair_data_vencimento(content)
        # Dicionário para armazenar a associação entre nome e a data de vencimento
        associacoes = {}
        # Iterar sobre o dicionário de nomes (linha: nome)
        for linha, nome in nomes_dict.items():
            # Verificar se há data de vencimento para o índice correspondente
            data_vencimento = datas_vencimento_dict.get(linha, "Data de vencimento não encontrada")
            # Associar o nome à data de vencimento no dicionário
            associacoes[nome] = data_vencimento
        return associacoes  # Retorna o dicionário de associações entre nome e data de vencimento
    except Exception as e:
        print(f"Erro ao associar nomes e datas de vencimento: {str(e)}")
        return {}


def associar_nomes_valores_cartorio(file_path):
    try:
        content = ler_arquivo(file_path)
        # Extrair nomes e seus índices (como um dicionário: {linha: nome})
        nomes_dict = extrair_nomes(content)
        # Extrair valores 'J'
        _, _, valores_j, _ = extrair_valores(content)
        # Dicionário para armazenar a associação entre nome e o valor somado (J)
        associacoes = {}
        # Iterar sobre o dicionário de nomes (linha: nome)
        for linha, nome in nomes_dict.items():
            indice_valor = linha + 1  # Ajustar o índice do valor (é 1 a mais que o índice do nome)
            # Verificar se há valor 'J' para o índice correspondente
            valor_j = valores_j.get(indice_valor, '0')  # Pegar o valor 'J', ou '0' se não existir
            # Limpar e converter o valor para float usando o método separado
            valor_total = limpar_valor(valor_j)
            # Associar o nome ao valor total no dicionário
            associacoes[nome] = valor_total
        return associacoes  # Retorna o dicionário de associações entre nome e valor 'J'
    except Exception as e:
        print(f"Erro ao associar nomes e valores jurados: {str(e)}")
        return {}


def associar_nomes_valores_devolvido(file_path):
    try:
        content = ler_arquivo(file_path)
        # Extrair nomes e seus índices (como um dicionário: {linha: nome})
        nomes_dict = extrair_nomes(content)
        # Extrair valores 'D'
        _, _, _, valores_d = extrair_valores(content)
        # Dicionário para armazenar a associação entre nome e o valor somado (D)
        associacoes = {}
        # Iterar sobre o dicionário de nomes (linha: nome)
        for linha, nome in nomes_dict.items():
            indice_valor = linha + 1  # Ajustar o índice do valor (é 1 a mais que o índice do nome)
            # Verificar se há valor 'J' para o índice correspondente
            valor_d = valores_d.get(indice_valor, '0')  # Pegar o valor 'D', ou '0' se não existir
            # Limpar e converter o valor para float usando o método separado
            valor_total = limpar_valor(valor_d)
            # Associar o nome ao valor total no dicionário
            associacoes[nome] = valor_total
        return associacoes  # Retorna o dicionário de associações entre nome e valor 'D'
    except Exception as e:
        print(f"Erro ao associar nomes e valores jurados: {str(e)}")
        return {}


def identificar_nomes_sem_valores(file_path):
    """
    Identifica os nomes que não possuem valores associados ou cujo valor associado é igual a zero.

    :param file_path: Caminho para o arquivo.
    :return: Lista de nomes sem valores associados ou cujo valor é zero.
    """
    try:
        content = ler_arquivo(file_path)
        nomes_dict = extrair_nomes(content)
        valores_pagos_dict = associar_nomes_valores_pagos(file_path)
        nomes_sem_valores_ou_zero = []
        for linha, nome in nomes_dict.items():
            valor = valores_pagos_dict.get(nome, None)  # Obtém o valor ou None se não existir
            if valor is None or valor == 0:  # Adiciona o nome se o valor for None ou zero
                nomes_sem_valores_ou_zero.append(nome)

        return nomes_sem_valores_ou_zero

    except Exception as e:
        print(f"Erro ao identificar nomes sem valores ou com valor zero: {str(e)}")
        return []


def associar_nomes_valores_tarifas(file_path):
    try:
        content = ler_arquivo(file_path)
        nomes_dict = extrair_nomes(content)
        _, valores_g, _, _ = extrair_valores(content)
        associacoes = {}
        for linha, nome in nomes_dict.items():
            indice_valor = linha + 1
            valor_g = valores_g.get(indice_valor, '0')
            valor_total = limpar_valor(valor_g)
            associacoes[nome] = valor_total
        return associacoes
    except Exception as e:
        print(f"Erro ao associar nomes e valores jurados: {str(e)}")
        return {}
