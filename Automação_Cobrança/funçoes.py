import re
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from copy import copy
import tkinter as tk


def extrair_nomes_e_valores(content):
    nomes = []
    valores = []
    for line in content:
        if '/01' in line and any(char.isalpha() for char in line):
            partes = line.split()
            nome = []
            for parte in partes[3:]:
                if parte.replace('.', '').replace(',', '').isdigit():
                    break
                nome.append(parte)
            nomes.append(' '.join(nome).strip())
            # Verificar linha seguinte para o valor
            next_line_index = content.index(line) + 1
            if next_line_index < len(content):
                next_line = content[next_line_index]
                if 'DINHEIRO' in next_line or 'D ' in next_line:
                    try:
                        if 'C' in next_line:
                            index_c = next_line.index('C')
                            valor_titulo = next_line[index_c + 1:].strip().split()[0].replace(',', '.')
                        elif 'D ' in next_line:
                            index_d = next_line.index('D ')
                            valor_titulo = next_line[index_d + 1:].strip().split()[0].replace(',', '.')
                        else:
                            continue
                        valores.append(valor_titulo)
                    except (ValueError, IndexError):
                        valores.append("Valor não encontrado")
                else:
                    valores.append("Valor não encontrado")
            else:
                valores.append("Valor não encontrado")
    return list(zip(nomes, valores))


def extrair_data_posicao_csv(file_path_txt):
    with open(file_path_txt, 'r', encoding='utf-8') as file:
        content = file.readlines()
    for line in content:
        if 'POSICAO DO DIA:' in line:
            try:
                data = line.split(':')[-1].strip()
                return data
            except IndexError:
                continue
    return None


def extrair_e_somar_duplas(content):
    taxas = {}
    for i, line in enumerate(content):
        if '/01' in line and any(char.isalpha() for char in line):
            partes = line.split()
            nome = []
            for parte in partes[3:]:
                if parte.replace(',', '').replace('.', '').isdigit():
                    break
                nome.append(parte)
            nome = ' '.join(nome).strip()
            taxas[nome] = 0  # Inicializa com 0 para garantir que o nome tenha uma entrada

            # Verificar os próximos 2 valores na mesma linha ou linhas subsequentes
            soma = 0
            for offset in range(1, 3):
                if i + offset < len(content):
                    next_line = content[i + offset]
                    matches = re.findall(r'(41|07)\s+(\d+,\d+)', next_line)
                    for match in matches:
                        _, numero = match
                        numero = float(numero.replace(',', '.'))
                        soma += numero
            taxas[nome] = soma
    return taxas


def buscar_nomes_excel(file_path_excel, nomes, aba, data_posicao, taxas):
    wb = load_workbook(filename=file_path_excel, data_only=True)
    ws = wb[aba]

    # Verificar e criar coluna "Pago?" se necessário
    pago_col_label = "Pago?"
    pago_col_index = None
    for col in range(1, ws.max_column + 2):
        if col <= ws.max_column and ws.cell(row=1, column=col).value == pago_col_label:
            pago_col_index = col
            break
    if not pago_col_index:
        pago_col_index = ws.max_column + 1
        ws.cell(row=1, column=pago_col_index).value = pago_col_label

    # Verificar se a coluna "DIA PGTO" já existe
    dia_pgto_col_label = "DIA PGTO"
    dia_pgto_col_index = None
    for col in range(1, ws.max_column + 1):
        if ws.cell(row=1, column=col).value == dia_pgto_col_label:
            dia_pgto_col_index = col
            break
    if not dia_pgto_col_index:  # Se "DIA PGTO" não existir, adicione-a
        dia_pgto_col_index = ws.max_column + 1
        ws.cell(row=1, column=dia_pgto_col_index).value = dia_pgto_col_label

    # Verificar se a coluna "Taxa" já existe
    taxa_col_label = "Taxa"
    taxa_col_index = None
    for col in range(1, ws.max_column + 1):
        if ws.cell(row=1, column=col).value == taxa_col_label:
            taxa_col_index = col
            break
    if not taxa_col_index:  # Se "Taxa" não existir, adicione-a
        taxa_col_index = ws.max_column + 1
        ws.cell(row=1, column=taxa_col_index).value = taxa_col_label

    source_col_index = pago_col_index - 1  # Copiando a formatação da coluna anterior
    copiar_formatacao_e_mesclagens(ws, source_col_index, pago_col_index)
    copiar_formatacao_e_mesclagens(ws, source_col_index, dia_pgto_col_index)
    copiar_formatacao_e_mesclagens(ws, source_col_index, taxa_col_index)

    nomes_encontrados, valores_associados = processar_nomes(ws, nomes, pago_col_index, dia_pgto_col_index, taxa_col_index, data_posicao, taxas)
    wb.save(filename=file_path_excel)
    wb.close()
    return nomes_encontrados, valores_associados

def copiar_formatacao_e_mesclagens(ws, source_col_index, target_col_index):
    for row in range(1, ws.max_row + 1):
        source_cell = ws.cell(row=row, column=source_col_index)
        target_cell = ws.cell(row=row, column=target_col_index)
        if source_cell.has_style:
            target_cell.font = copy(source_cell.font)
            target_cell.border = copy(source_cell.border)
            target_cell.fill = copy(source_cell.fill)
            target_cell.number_format = copy(source_cell.number_format)
            target_cell.protection = copy(source_cell.protection)
            target_cell.alignment = copy(source_cell.alignment)

    new_merges = []
    for merge_cell in ws.merged_cells.ranges:
        if merge_cell.min_col <= source_col_index <= merge_cell.max_col:
            new_range = f"{get_column_letter(target_col_index)}{merge_cell.min_row}:{get_column_letter(target_col_index)}{merge_cell.max_row}"
            new_merges.append(new_range)

    for merge_range in new_merges:
        ws.merge_cells(merge_range)



def processar_nomes(ws, nomes, pago_col_index, dia_pgto_col_index, taxa_col_index, data_posicao, taxas):
    total_fatura_titular_col_index = next((i for i, cell in enumerate(ws[1], 1) if cell.value == "Total fatura titular"), None)
    nomes_encontrados = []
    valores_associados = []
    for nome_procurado in nomes:
        encontrado = False
        for row in ws.iter_rows(min_row=2, values_only=False):
            if nome_procurado == str(row[0].value).strip():
                nomes_encontrados.append(nome_procurado)
                valor = row[total_fatura_titular_col_index - 1].value
                valor_formatado = f"{valor:.2f}" if isinstance(valor, (int, float)) else str(valor) if valor else "Valor não encontrado"
                valores_associados.append(valor_formatado)
                row[pago_col_index - 1].value = "X"
                row[dia_pgto_col_index - 1].value = data_posicao  # Adicionar a data extraída
                row[taxa_col_index - 1].value = f"{taxas.get(nome_procurado, 0):.2f}"  # Adicionar a taxa
                encontrado = True
                break
        if not encontrado:
            valores_associados.append("Valor não encontrado")
    return nomes_encontrados, valores_associados


def processar_arquivos(file_path_txt, file_path_excel, aba, txt_area):
    with open(file_path_txt, 'r', encoding='utf-8') as file:
        content_txt = file.readlines()
    data_posicao = extrair_data_posicao_csv(file_path_txt)
    nomes_valores_txt = extrair_nomes_e_valores(content_txt)
    nomes = [nome for nome, _ in nomes_valores_txt]

    # Extrair e somar duplas (taxas)
    taxas = extrair_e_somar_duplas(content_txt)

    nomes_encontrados, valores_associados = buscar_nomes_excel(file_path_excel, nomes, aba, data_posicao, taxas)
    txt_area.delete('1.0', tk.END)
    txt_area.insert(tk.END, "{:<50} {:<30}\n".format("Nomes encontrados no arquivo TXT", "Valores encontrados no arquivo Excel"))
    txt_area.insert(tk.END, "="*80 + "\n")
    for nome, valor_txt, valor_excel in zip(nomes, [valor for _, valor in nomes_valores_txt], valores_associados):
        txt_area.insert(tk.END, "{:<50} {:<30}\n".format(f"{nome} - {valor_txt}", valor_excel))
    quantidade_nomes = len([nome for nome in nomes if nome in nomes_encontrados])
    txt_area.insert(tk.END, f"Quantidade de nomes correspondentes encontrados: {quantidade_nomes}\n")
