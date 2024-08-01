import re
import pandas as pd

class Coparticipacao_Automacao:
    def __init__(self, conteudo):
        self.linhas = conteudo.splitlines()
        self.nomes_valores = {}
        self.somas_valores = {}  # Dicionário para armazenar as somas dos valores

    def buscar_nomes(self):
        """Busca e extrai os nomes dos beneficiários usando uma expressão regular."""
        pattern_bloco = re.compile(r'(\d{13}\s+\d{3}\s+([A-Z\s]+))')
        self.nomes = []

        for linha in self.linhas:
            resultado = pattern_bloco.search(linha)
            if resultado:
                nome = resultado.group(2).strip()  # Remove espaços extras e captura apenas o nome
                self.nomes.append(nome)

        return self.nomes

    def buscar_valores(self):
        """Busca os valores da coluna 'Valor Part Cobrado' associados a cada nome encontrado."""
        pattern_bloco = re.compile(r'(\d{13}\s+\d{3}\s+([A-Z\s]+))')
        pattern_valor = re.compile(r'\d{1,3},\d{2}$')
        nome_atual = None
        capturando = False

        for linha in self.linhas:
            nome_match = pattern_bloco.search(linha)
            valor_match = pattern_valor.search(linha)

            if nome_match:
                nome_atual = nome_match.group(2).strip()
                self.nomes_valores[nome_atual] = []
                capturando = True

            if valor_match and nome_atual and capturando:
                self.nomes_valores[nome_atual].append(valor_match.group(0))

            if not valor_match and capturando:
                capturando = False

    def somar_valores(self):
        """Converte strings de valores para float e soma os valores para cada nome."""
        for nome, valores in self.nomes_valores.items():
            total = sum(float(valor.replace(',', '.')) for valor in valores)
            self.somas_valores[nome] = total

    def gerar_dataframe(self, caminho_saida_csv):
        """Gera um DataFrame com nomes e somas dos valores e salva como CSV."""
        data = {'Nome': list(self.somas_valores.keys()),
                'Soma dos Valores': [round(valor, 2) for valor in self.somas_valores.values()]}
        df = pd.DataFrame(data)
        df.to_csv(caminho_saida_csv, index=False, encoding='utf-8', sep=';')
        return df
