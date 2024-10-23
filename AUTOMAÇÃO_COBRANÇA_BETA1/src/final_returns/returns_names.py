from datetime import datetime
from utils.association.association import associar_nomes_valores_pagos, associar_nomes_datas_vencimento, \
    associar_nomes_valores_cartorio, associar_nomes_valores_devolvido, associar_nomes_valores_tarifas
from utils.extract.extract_objects import extrair_data_posicao, ler_arquivo, extrair_nomes

file_path = "../../documents/txts/12_07Resumo_Contabil_20240717.txt"


def filtrar_nomes_finais(file_path):
    """
    Filtra os nomes cujas datas de vencimento têm o mesmo mês e ano da data de posição do dia.
    São os nomes finais, que iram para planilha excel.

    :param file_path: Caminho para o arquivo.
    :return: Dicionário filtrado com nomes e valores cujas datas de vencimento têm o mesmo mês e ano da data de posição.
    """
    try:
        content = ler_arquivo(file_path)

        # Extrair a data de posição do dia usando a função existente
        data_posicao = extrair_data_posicao(content)
        if not data_posicao:
            print("Erro: Data de posição não encontrada.")
            return {}
        # Associar nomes e valores pagos
        valores_pagos_dict = associar_nomes_valores_pagos(file_path)
        # Associar nomes e datas de vencimento
        datas_vencimento_dict = associar_nomes_datas_vencimento(file_path)
        # Dicionário para armazenar nomes com mês e ano de vencimento igual à data de posição
        nomes_filtrados = {}
        # Iterar sobre os valores pagos e verificar se o mês e ano de vencimento é igual à data de posição
        for nome, valor in valores_pagos_dict.items():
            if nome in datas_vencimento_dict:
                data_vencimento_str = datas_vencimento_dict[nome]
                # Converter string para objeto datetime
                data_vencimento = datetime.strptime(data_vencimento_str, "%d/%m/%Y")
                # Se o mês e o ano da data de vencimento forem iguais à data de posição, adicionar ao dicionário
                if data_vencimento.month == data_posicao.month and data_vencimento.year == data_posicao.year:
                    nomes_filtrados[nome] = valor
        return nomes_filtrados

    except Exception as e:
        print(f"Erro ao filtrar nomes por mês de vencimento: {str(e)}")
        return {}


def filtrar_nomes_atrasados(file_path):
    """
    Filtra os nomes cujas datas de vencimento não têm o mesmo mês e ano da data de posição do dia.

    :param file_path: Caminho para o arquivo.
    :return: Dicionário filtrado com nomes e valores cujas datas de vencimento não têm o mesmo mês e ano da data de posição.
    """
    try:
        content = ler_arquivo(file_path)
        # Extrair a data de posição do dia usando a função existente
        data_posicao = extrair_data_posicao(content)
        if not data_posicao:
            print("Erro: Data de posição não encontrada.")
            return {}
        # Associzr nomes e valores pagos
        valores_pagos_dict = associar_nomes_valores_pagos(file_path)
        # Associar nomes e datas de vencimento
        datas_vencimento_dict = associar_nomes_datas_vencimento(file_path)
        # Dicionário para armazenar nomes com mês e ano de vencimento diferente da data de posição
        nomes_filtrados = {}
        # Iterar sobre os valores pagos e verificar se o mês e ano de vencimento é diferente da data de posição
        for nome, valor in valores_pagos_dict.items():
            if nome in datas_vencimento_dict:
                data_vencimento_str = datas_vencimento_dict[nome]
                # Converter string para objeto datetime
                data_vencimento = datetime.strptime(data_vencimento_str, "%d/%m/%Y")
                # Se o mês ou o ano da data de vencimento forem diferentes da data de posição, adicionar ao dicionário
                if data_vencimento.month != data_posicao.month or data_vencimento.year != data_posicao.year:
                    nomes_filtrados[nome] = valor
        return nomes_filtrados
    except Exception as e:
        print(f"Erro ao filtrar nomes por mês de vencimento: {str(e)}")
        return {}


def filtrar_nomes_cartorio(file_path):
    """
    Filtra os nomes cujos valores estão relacionados ao cartório.
    Esses nomes são considerados para algum processamento ou relatório adicional.

    :param file_path: Caminho para o arquivo.
    :return: Dicionário filtrado com nomes e valores associados ao cartório.
    """
    try:
        content = ler_arquivo(file_path)
        # Associar nomes e valores pagos (associando também os valores do cartório)
        valores_cartorio_dict = associar_nomes_valores_cartorio(file_path)  # Função que retorna valores do cartório
        # Dicionário para armazenar nomes relacionados ao cartório
        nomes_filtrados = {}
        # Iterar sobre os valores do cartório e adicionar ao dicionário filtrado
        for nome, valor in valores_cartorio_dict.items():
            if valor > 0:  # Condição para filtrar apenas valores positivos (ou outra lógica conforme necessário)
                nomes_filtrados[nome] = valor

        return nomes_filtrados

    except Exception as e:
        print(f"Erro ao filtrar nomes relacionados ao cartório: {str(e)}")
        return {}


def filtrar_nomes_devolvido(file_path):
    """
    Filtra os nomes cujos valores estão relacionados ao devolvido.
    Esses nomes são considerados para algum processamento ou relatório adicional.

    :param file_path: Caminho para o arquivo.
    :return: Dicionário filtrado com nomes e valores associados ao devolvido.
    """
    try:
        content = ler_arquivo(file_path)
        valores_devolvido_dict = associar_nomes_valores_devolvido(file_path)
        nomes_filtrados = {}
        for nome, valor in valores_devolvido_dict.items():
            if valor > 0:
                nomes_filtrados[nome] = valor
        return nomes_filtrados

    except Exception as e:
        print(f"Erro ao filtrar nomes relacionados ao cartório: {str(e)}")
        return {}


def filtrar_nomes_tarifas(file_path):
    """
    Filtra os nomes cujos valores estão relacionados a tarifas.
    Esses nomes são considerados para algum processamento ou relatório adicional.

    :param file_path: Caminho para o arquivo.
    :return: Dicionário filtrado com nomes e valores associados ao devolvido.
    """
    try:
        content = ler_arquivo(file_path)
        valores_tarifas_dict = associar_nomes_valores_tarifas(file_path)
        nomes_filtrados = {}
        for nome, valor in valores_tarifas_dict.items():
            if valor > 0:
                nomes_filtrados[nome] = valor
        return nomes_filtrados

    except Exception as e:
        print(f"Erro ao filtrar nomes relacionados ao cartório: {str(e)}")
        return {}


def filtrar_nomes_sem_valores(file_path):
    """
    Identifica os nomes que não possuem valores associados ou cujo valor associado é igual a zero.

    :param file_path: Caminho para o arquivo.
    :return: Dicionário filtrado com nomes sem valores ou com valor zero.
    """
    try:
        content = ler_arquivo(file_path)
        nomes_dict = extrair_nomes(content)
        valores_associados_dict = associar_nomes_valores_pagos(file_path)

        # Lista ou dicionário para armazenar os nomes sem valores
        nomes_sem_valores = {}

        # Filtragem dos nomes
        for nome in nomes_dict.values():
            valor = valores_associados_dict.get(nome, None)
            if valor is None or valor == 0:
                nomes_sem_valores[nome] = valor  # Adicionar nome ao dicionário

        return nomes_sem_valores  # Retornar o dicionário com os nomes sem valores

    except Exception as e:
        print(f"Erro ao filtrar nomes sem valores: {str(e)}")
        return {}

r = filtrar_nomes_sem_valores(file_path)
print(r)
