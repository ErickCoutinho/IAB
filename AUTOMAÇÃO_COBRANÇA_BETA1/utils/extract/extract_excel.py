import pandas as pd


def ler_nomes_excel(excel_file, aba_selecionada):
    """
    Lê os nomes da coluna 'Conveniado' do arquivo Excel.

    :param excel_file: O caminho para o arquivo Excel ou objeto ExcelFile carregado.
    :param aba_selecionada: O nome da aba a ser lida.
    :return: Uma lista com os nomes da coluna 'Conveniado'.
    """
    try:
        # Carregar a aba especificada no Excel
        worksheet = pd.read_excel(excel_file, sheet_name=aba_selecionada)

        # Ler os nomes da coluna 'Conveniado' e remover valores nulos
        nomes_excel = worksheet['Conveniado'].dropna().tolist()
        return nomes_excel
    except KeyError:
        print("Erro: A coluna 'Conveniado' não foi encontrada.")
        return []
    except Exception as e:
        print(f"Erro ao ler os nomes do Excel: {str(e)}")
        return []