from datetime import datetime
from utils.association.association import associar_nomes_valores_pagos, associar_nomes_datas_vencimento
from utils.extract.extract_objects import extrair_data_posicao, ler_arquivo

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

r = filtrar_nomes_atrasados(file_path)
print(r)


