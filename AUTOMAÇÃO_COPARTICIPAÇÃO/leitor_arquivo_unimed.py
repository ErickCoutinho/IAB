import re

class Coparticipacao_Automacao:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.dados = []
        self.nomes_valores = {}
        self.somas_valores = {}  # Dicionário para armazenar as somas dos valores

    def ler_arquivo(self):
        """Lê o arquivo e armazena as linhas para processamento posterior."""
        with open(self.caminho_arquivo, 'r') as file:
            self.linhas = file.readlines()


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
        # Regex para capturar valores que estão no final da linha
        nome_atual = None
        capturando = False

        for linha in self.linhas:
            nome_match = pattern_bloco.search(linha)
            valor_match = pattern_valor.search(linha)

            if nome_match:
                nome_atual = nome_match.group(2).strip()
                self.nomes_valores[nome_atual] = []
                capturando = True  # Inicia a captura de valores

            if valor_match and nome_atual and capturando:
                self.nomes_valores[nome_atual].append(valor_match.group(0))

            if not valor_match and capturando:
                capturando = False  # Para de capturar valores se uma linha sem valor válido for encontrada

    def exibir_valores(self):
        """Exibe os valores associados a cada nome antes da soma."""
        for nome, valores in self.nomes_valores.items():
            print(f"{nome}: {valores}")

    def somar_valores(self):
        """Converte strings de valores para float e soma os valores para cada nome."""
        for nome, valores in self.nomes_valores.items():
            total = sum(float(valor.replace(',', '.')) for valor in valores)
            self.somas_valores[nome] = total

    def exibir_somas(self):
        """Exibe as somas dos valores associados a cada nome."""
        for nome, soma in self.somas_valores.items():
            print(f"{nome}: {soma:.2f}")

    def exibir_linhas_processadas(self):
        """Exibe as linhas após processamento para verificar mudanças."""
        for linha in self.linhas[:10000]:  # Exibe as primeiras 100 linhas para verificação
            print(linha.strip())

# Uso do código
copart = Coparticipacao_Automacao("unimed___.txt")
copart.ler_arquivo()
copart.buscar_nomes()  # Buscar primeiro todos os nomes para garantir a estrutura de dados
copart.buscar_valores()  # Depois buscar valores associados aos nomes
copart.exibir_valores()
copart.somar_valores()   # Somar os valores para cada nome
copart.exibir_somas()    # Exibir as somas calculada
