import pandas as pd
from tkinter import filedialog, messagebox
from src.final_returns.returns_names import filtrar_nomes_finais

# Função para carregar o arquivo TXT
# Função para carregar o arquivo txt, processar os dados e retornar o dicionário filtrado
def carregar_arquivo_txt():
    file_path = filedialog.askopenfilename(title="Selecione o arquivo .txt", filetypes=[("Arquivo TXT", "*.txt")])
    if file_path:
        try:
            # Chama a função filtrar_nomes_finais para processar o arquivo TXT e obter o dicionário filtrado
            dicionario_nomes_valores = filtrar_nomes_finais(file_path)
            if not dicionario_nomes_valores:
                messagebox.showerror("Erro", "Nenhum nome válido encontrado no arquivo TXT.")
                return None

            print("Arquivo TXT carregado e processado com sucesso.")
            return dicionario_nomes_valores
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo TXT: {str(e)}")
    return None



# Função para carregar o arquivo Excel e escolher a aba
def carregar_arquivo_excel(combobox_aba):
    file_path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Arquivo Excel", "*.xlsx")])
    if file_path:
        try:
            excel_file = pd.ExcelFile(file_path)
            # Populando o combobox com os nomes das abas
            combobox_aba['values'] = excel_file.sheet_names
            combobox_aba.current(0)  # Seleciona a primeira aba por padrão
            print("Arquivo Excel carregado com sucesso.")
            return excel_file
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo Excel: {str(e)}")
    return None


def processar_dados(excel_file, aba_selecionada, dicionario_nomes_valores):
    try:
        df = pd.read_excel(excel_file, sheet_name=aba_selecionada)

        # Filtrar e atualizar a coluna "Total fatura titular"
        for nome, valor in dicionario_nomes_valores.items():
            # Buscar o nome na coluna "Conveniado" (não case-sensitive)
            df['Conveniado'] = df['Conveniado'].str.upper()  # Para evitar problemas com maiúsculas/minúsculas
            mask = df['Conveniado'].str.contains(nome.upper(), na=False)
            if mask.any():
                df.loc[mask, 'Total fatura titular'] = valor

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Sucesso", "Dados processados com sucesso!")
        print("Processamento concluído.")

        # Salvar o arquivo processado
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivo Excel", "*.xlsx")])
        if save_path:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Arquivo Salvo", f"Arquivo salvo em {save_path}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar os dados: {str(e)}")
