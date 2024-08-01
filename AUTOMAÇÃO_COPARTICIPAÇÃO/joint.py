import tkinter as tk
from tkinter import filedialog, messagebox
import io
import re
import pandas as pd

class Normalizador:
    def __init__(self):
        self.arquivo_entrada = None
        self.arquivo_saida = io.StringIO()  # Armazena o conteúdo processado em memória

    def definir_arquivo_entrada(self, caminho_arquivo):
        """Define o caminho do arquivo de entrada."""
        self.arquivo_entrada = caminho_arquivo

    def remover_cabecalhos(self, linhas):
        """Remove os cabeçalhos de mudança de página e as linhas subsequentes."""
        i = 0
        while i < len(linhas):
            if "DATASUL Saude - FATURAMENTO" in linhas[i]:
                del linhas[i-2:i + 12]
            else:
                i += 1
        return linhas

    def processar_arquivo(self):
        if not self.arquivo_entrada:
            raise ValueError("O arquivo de entrada não foi definido.")

        # Leitura do arquivo de entrada
        with open(self.arquivo_entrada, "r") as f:
            linhas = f.readlines()

        # Remover cabeçalhos
        linhas_sem_cabecalhos = self.remover_cabecalhos(linhas)

        # Salvar no "arquivo" de saída em memória
        self.arquivo_saida.write(''.join(linhas_sem_cabecalhos))

    def obter_conteudo_saida(self):
        """Retorna o conteúdo do arquivo de saída."""
        self.arquivo_saida.seek(0)  # Move para o início do StringIO
        return self.arquivo_saida.read()

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

# Funções de seleção de arquivos
def escolher_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        filetypes=[("Arquivos LST", "*.lst"), ("Todos os arquivos", "*.*")]
    )
    if caminho_arquivo:
        entrada_txt.set(caminho_arquivo)

def escolher_local_saida_csv():
    caminho_saida = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV", "*.csv"), ("Todos os arquivos", "*.*")]
    )
    if caminho_saida:
        saida_csv.set(caminho_saida)

def escolher_arquivo_csv():
    caminho_csv = filedialog.askopenfilename(
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
    )
    if caminho_csv:
        entrada_csv.set(caminho_csv)

def escolher_arquivo_excel():
    caminho_excel = filedialog.askopenfilename(
        filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
    )
    if caminho_excel:
        entrada_excel.set(caminho_excel)

# Função para processar o arquivo LST e gerar CSV
def processar():
    try:
        caminho_entrada = entrada_txt.get()
        caminho_saida_csv = saida_csv.get()

        # Verificar se todos os caminhos foram definidos
        if not caminho_entrada or not caminho_saida_csv:
            raise ValueError("Todos os caminhos de arquivos devem ser definidos.")

        # Processar o arquivo com Normalizador
        normalizador = Normalizador()
        normalizador.definir_arquivo_entrada(caminho_entrada)
        normalizador.processar_arquivo()

        # Utilizar o conteúdo processado no Coparticipacao_Automacao
        conteudo_processado = normalizador.obter_conteudo_saida()
        copart = Coparticipacao_Automacao(conteudo_processado)
        copart.buscar_nomes()
        copart.buscar_valores()
        copart.somar_valores()
        copart.gerar_dataframe(caminho_saida_csv)

        messagebox.showinfo("Sucesso", "Processamento concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para atualizar o Excel com os dados do CSV
def processar_excel():
    try:
        caminho_csv = entrada_csv.get()
        caminho_excel = entrada_excel.get()

        if not caminho_csv or not caminho_excel:
            raise ValueError("Os caminhos dos arquivos CSV e Excel devem ser definidos.")

        # Ler arquivos CSV e Excel
        df_csv = pd.read_csv(caminho_csv)
        xls = pd.ExcelFile(caminho_excel)

        # Iterar sobre cada planilha do Excel
        with pd.ExcelWriter(caminho_excel, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            for sheet_name in xls.sheet_names:
                df_excel = pd.read_excel(xls, sheet_name=sheet_name)
                # Verificar correspondência e atualizar PR_UNITARIO
                for idx, row in df_csv.iterrows():
                    dependentes = df_excel[df_excel['DEPENDENTE'] == row['Nome']]
                    if not dependentes.empty:
                        df_excel.loc[df_excel['DEPENDENTE'] == row['Nome'], 'PR_UNITARIO'] = row['Soma dos Valores']
                df_excel.to_excel(writer, sheet_name=sheet_name, index=False)

        messagebox.showinfo("Sucesso", "Atualização do arquivo Excel concluída com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface
# Interface
root = tk.Tk()
root.title("Processador de Arquivos Unimed")

# Variáveis de caminho de arquivo
entrada_txt = tk.StringVar()
saida_csv = tk.StringVar()
entrada_csv = tk.StringVar()
entrada_excel = tk.StringVar()

# Layout
tk.Label(root, text="Arquivo de entrada - Unimed (.LST):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=entrada_txt, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Escolher", command=escolher_arquivo).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Arquivo de saída (.csv):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=saida_csv, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Salvar", command=escolher_local_saida_csv).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Arquivo CSV com Coparticipações:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=entrada_csv, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Escolher", command=escolher_arquivo_csv).grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Arquivo Excel para atualizar:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=entrada_excel, width=50).grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Escolher", command=escolher_arquivo_excel).grid(row=3, column=2, padx=10, pady=5)

tk.Button(root, text="Processar LST para CSV", command=processar).grid(row=4, column=1, padx=10, pady=20)
tk.Button(root, text="Atualizar Excel", command=processar_excel).grid(row=5, column=1, padx=10, pady=20)

# Iniciar o loop da interface
root.mainloop()
