from tkinter import filedialog, messagebox
import pandas as pd
from normalizador import Normalizador
from leitor_unimed_copart import Coparticipacao_Automacao

# Funções de seleção de arquivos
def escolher_arquivo(entrada_txt):
    caminho_arquivo = filedialog.askopenfilename(
        filetypes=[("Arquivos LST", "*.lst"), ("Todos os arquivos", "*.*")]
    )
    if caminho_arquivo:
        entrada_txt.set(caminho_arquivo)

def escolher_local_saida_csv(saida_csv):
    caminho_saida = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV", "*.csv"), ("Todos os arquivos", "*.*")]
    )
    if caminho_saida:
        saida_csv.set(caminho_saida)

def escolher_arquivo_csv(entrada_csv):
    caminho_csv = filedialog.askopenfilename(
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
    )
    if caminho_csv:
        entrada_csv.set(caminho_csv)

def escolher_arquivo_excel(entrada_excel):
    caminho_excel = filedialog.askopenfilename(
        filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
    )
    if caminho_excel:
        entrada_excel.set(caminho_excel)

# Função para processar o arquivo LST e gerar CSV
def processar(entrada_txt, saida_csv):
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
def processar_excel(entrada_csv, entrada_excel):
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
