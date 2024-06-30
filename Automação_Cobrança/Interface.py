import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def extrair_nomes_e_valores(content):
    nomes = []
    valores = []
    for line in content:
        if '/01' in line and any(char.isalpha() for char in line):
            partes = line.split()
            nome = []
            for parte in partes[3:]:
                if parte.isdigit():
                    break
                nome.append(parte)
            nomes.append(' '.join(nome).strip())
        if 'DINHEIRO' in line:
            try:
                index_c = line.index('C')
                valor_titulo = line[index_c + 1:].strip().split()[0].replace(',', '.')
                valores.append(valor_titulo)
            except (ValueError, IndexError):
                continue
    return list(zip(nomes, valores))


def buscar_nomes_excel(file_path_excel, nomes, aba):
    try:
        wb = load_workbook(filename=file_path_excel, data_only=True)
        ws = wb[aba]

        # Identificar a última coluna com dados e a coluna "CALCULO UNIMED"
        last_col = ws.max_column
        calc_unimed_col_index = None
        for col in range(1, ws.max_column + 1):
            if ws.cell(row=1, column=col).value == "CALCULO UNIMED":
                calc_unimed_col_index = col
                break

        # Verificar se a coluna "Pago?" já existe
        pago_col_label = "Pago?"
        pago_col_index = None
        for col in range(1, last_col + 1):
            if ws.cell(row=1, column=col).value == pago_col_label:
                pago_col_index = col
                break
        if not pago_col_index:  # Se "Pago?" não existir, adicione-a
            pago_col_index = last_col + 1
            ws.cell(row=1, column=pago_col_index).value = pago_col_label

        # Copiar a formatação da coluna "CALCULO UNIMED" para "Pago?"
        if calc_unimed_col_index:
            for row in range(1, ws.max_row + 1):
                source_cell = ws.cell(row=row, column=calc_unimed_col_index)
                target_cell = ws.cell(row=row, column=pago_col_index)
                if source_cell.has_style:
                    target_cell._style = source_cell._style

            # Preparar para aplicar mesclagens sem alterar o conjunto durante a iteração
            new_merges = []
            for merge_range in ws.merged_cells.ranges:
                if merge_range.min_col <= calc_unimed_col_index <= merge_range.max_col:
                    new_merge_range = f"{get_column_letter(pago_col_index)}{merge_range.min_row}:{get_column_letter(pago_col_index)}{merge_range.max_row}"
                    new_merges.append(new_merge_range)

            # Aplicar as novas mesclagens coletadas
            for merge_range in new_merges:
                ws.merge_cells(merge_range)

        nomes_encontrados = []
        valores_associados = []

        for nome_procurado in nomes:
            encontrado = False
            for row in ws.iter_rows(min_row=2, max_col=ws.max_column, values_only=False):
                if nome_procurado == str(row[0].value).strip():
                    nomes_encontrados.append(nome_procurado)
                    valor = row[33].value if len(row) > 33 else "Valor não encontrado"
                    valor_formatado = f"{valor:.2f}" if isinstance(valor, (int, float)) else str(valor) if valor else "Valor não encontrado"
                    valores_associados.append(valor_formatado)
                    row[pago_col_index - 1].value = "X"
                    encontrado = True
                    break
            if not encontrado:
                valores_associados.append("Valor não encontrado")

        wb.save(filename=file_path_excel)
        wb.close()
        return nomes_encontrados, valores_associados

    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo Excel não foi encontrado.")
        return [], []
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Um erro ocorreu: {str(e)}")
        return [], []


def processar_arquivos(file_path_txt, file_path_excel, aba):
    try:
        with open(file_path_txt, 'r', encoding='utf-8') as file:
            content_txt = file.readlines()
        nomes_valores_txt = extrair_nomes_e_valores(content_txt)
        nomes = [nome for nome, _ in nomes_valores_txt]
        nomes_encontrados, valores_associados = buscar_nomes_excel(file_path_excel, nomes, aba)
        txt_area.delete('1.0', tk.END)
        txt_area.insert(tk.END, "{:<50} {:<30}\n".format("Nomes encontrados no arquivo TXT", "Valores encontrados no arquivo Excel"))
        txt_area.insert(tk.END, "="*80 + "\n")
        for nome, valor_txt, valor_excel in zip(nomes, [valor for _, valor in nomes_valores_txt], valores_associados):
            print(f"Debug: Nome={nome}, Valor TXT={valor_txt}, Valor Excel={valor_excel}")  # Debugging
            txt_area.insert(tk.END, "{:<50} {:<30}\n".format(f"{nome} - {valor_txt}", valor_excel))
        quantidade_nomes = len([nome for nome in nomes if nome in nomes_encontrados])
        txt_area.insert(tk.END, f"Quantidade de nomes correspondentes encontrados: {quantidade_nomes}\n")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Selecione um arquivo TXT e um arquivo Excel válidos.")


def selecionar_arquivo_txt():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos TXT", "*.txt")])
    if file_path:
        txt_path_entry.delete(0, tk.END)
        txt_path_entry.insert(tk.END, file_path)

def selecionar_arquivo_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if file_path:
        excel_path_entry.delete(0, tk.END)
        excel_path_entry.insert(tk.END, file_path)

        try:
            wb = load_workbook(filename=file_path, read_only=True)
            sheet_names = wb.sheetnames
            wb.close()

            if sheet_names:
                aba_combo['values'] = sheet_names  # Preenche as opções do combobox com as abas disponíveis

        except FileNotFoundError:
            messagebox.showerror("Erro", f"O arquivo Excel '{file_path}' não foi encontrado.")

def processar():
    file_path_txt = txt_path_entry.get()
    file_path_excel = excel_path_entry.get()
    aba = aba_combo.get()

    if file_path_txt and file_path_excel and aba:
        processar_arquivos(file_path_txt, file_path_excel, aba)
    else:
        messagebox.showerror("Erro", "Selecione um arquivo TXT, um arquivo Excel e uma aba.")

# Criar a interface gráfica
root = tk.Tk()
root.title("Selecionar Arquivos e Abas de Arquivos Excel")
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)
tk.Label(frame, text="Selecione o arquivo TXT:").grid(row=0, column=0, sticky='w', pady=5)
txt_path_entry = tk.Entry(frame, width=50)
txt_path_entry.grid(row=0, column=1, padx=10)
btn_selecionar_txt = tk.Button(frame, text="Selecionar", command=selecionar_arquivo_txt)
btn_selecionar_txt.grid(row=0, column=2, padx=10)
tk.Label(frame, text="Selecione o arquivo Excel:").grid(row=1, column=0, sticky='w', pady=5)
excel_path_entry = tk.Entry(frame, width=50)
excel_path_entry.grid(row=1, column=1, padx=10)
btn_selecionar_excel = tk.Button(frame, text="Selecionar", command=selecionar_arquivo_excel)
btn_selecionar_excel.grid(row=1, column=2, padx=10)
tk.Label(frame, text="Selecione a aba do arquivo Excel:").grid(row=2, column=0, sticky='w', pady=5)
aba_combo = ttk.Combobox(frame, width=47, state='readonly')
aba_combo.grid(row=2, column=1, padx=10, columnspan=2)
btn_processar = tk.Button(root, text="Processar Arquivos", command=processar)
btn_processar.pack(pady=10)
txt_area = scrolledtext.ScrolledText(root, width=100, height=20)
txt_area.pack()
root.mainloop()