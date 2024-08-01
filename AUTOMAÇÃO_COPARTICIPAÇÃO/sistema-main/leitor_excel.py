import pandas as pd

class LeitorExcel:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.dataframes = {}  # Dicionário para armazenar as planilhas

    def informacoes_colunas(self):
        """Retorna informações sobre as colunas de cada planilha no arquivo Excel."""
        try:
            # Ler todas as planilhas e armazená-las em um dicionário
            self.dataframes = pd.read_excel(self.caminho_arquivo, sheet_name=None)

            # Dicionário para armazenar informações sobre colunas
            info_colunas = {}

            for nome_planilha, df in self.dataframes.items():
                colunas_info = [(coluna, str(df[coluna].dtype)) for coluna in df.columns]
                info_colunas[nome_planilha] = colunas_info

            return info_colunas

        except Exception as e:
            print(f"Erro ao ler o arquivo Excel: {e}")
            return None
