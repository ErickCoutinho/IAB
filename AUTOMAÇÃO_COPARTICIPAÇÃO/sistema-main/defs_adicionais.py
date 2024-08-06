
from normalizador_class import Normalizador
from leitor_unimed_copart import Coparticipacao_Automacao
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


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
        # Forçar a extensão para .xlsx em minúsculo
        if not caminho_excel.lower().endswith('.xlsx'):
            # Remover qualquer extensão atual e adicionar .xlsx em minúsculas
            caminho_excel = caminho_excel.rsplit('.', 1)[0] + '.xlsx'
        else:
            # Garantir que a extensão esteja em minúsculas
            caminho_excel = caminho_excel[:-4] + caminho_excel[-4:].lower()

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


def processar_excel(entrada_csv, entrada_excel):
    try:
        caminho_csv = entrada_csv.get()
        caminho_excel = entrada_excel.get()

        if not caminho_csv or not caminho_excel:
            raise ValueError("Os caminhos dos arquivos CSV e Excel devem ser definidos.")

        # Carregar dados do CSV
        df_csv = pd.read_csv(caminho_csv)

        # Checar se a coluna 'Nome' está presente
        if 'Nome' not in df_csv.columns:
            messagebox.showerror("Erro", "A coluna 'Nome' não está presente no arquivo CSV.")
            return  # Interromper a função se a coluna não estiver presente

        # Carregar o Excel
        encontrados = []
        nao_encontrados = []

        with pd.ExcelWriter(caminho_excel, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            xls = pd.ExcelFile(caminho_excel, engine='openpyxl')
            for sheet_name in xls.sheet_names:
                df_excel = pd.read_excel(xls, sheet_name=sheet_name, engine='openpyxl')

                # Atualizar valores usando o merge para garantir a correspondência correta
                df_merged = pd.merge(df_excel, df_csv, left_on='DEPENDENTE', right_on='Nome', how='left')

                # Atualizar coluna PR_UNITARIO com valores de Soma dos Valores se existir correspondência
                df_merged['PR_UNITARIO'] = df_merged['Valores'].combine_first(df_merged['PR_UNITARIO'])

                # Verificar quais nomes foram encontrados e quais não foram
                encontrados.extend(df_csv['Nome'][df_csv['Nome'].isin(df_merged['DEPENDENTE'])])
                nao_encontrados.extend(df_csv['Nome'][~df_csv['Nome'].isin(df_merged['DEPENDENTE'])])

                # Remover colunas extras do merge
                df_final = df_merged[df_excel.columns.tolist()]

                # Escrever de volta para a planilha Excel
                df_final.to_excel(writer, sheet_name=sheet_name, index=False)

        messagebox.showinfo("Sucesso", "Atualização do arquivo Excel concluída com sucesso!")

        # Exibir os resultados
        exibir_resultados(encontrados, nao_encontrados)

    except Exception as e:
        messagebox.showerror("Erro", str(e))

def exibir_resultados(encontrados, nao_encontrados):
    janela_resultados = tk.Toplevel()
    janela_resultados.title("Resultados da Atualização")

    tk.Label(janela_resultados, text="Nomes Encontrados", font=("Arial", 12, "bold")).pack(pady=5)
    texto_encontrados = tk.Text(janela_resultados, height=10, width=50)
    texto_encontrados.pack(padx=10, pady=5)
    texto_encontrados.insert(tk.END, "\n".join(encontrados))
    texto_encontrados.config(state=tk.DISABLED)

    tk.Label(janela_resultados, text="Nomes Não Encontrados", font=("Arial", 12, "bold")).pack(pady=5)
    texto_nao_encontrados = tk.Text(janela_resultados, height=10, width=50)
    texto_nao_encontrados.pack(padx=10, pady=5)
    texto_nao_encontrados.insert(tk.END, "\n".join(nao_encontrados))
    texto_nao_encontrados.config(state=tk.DISABLED)

    tk.Button(janela_resultados, text="Fechar", command=janela_resultados.destroy).pack(pady=10)

