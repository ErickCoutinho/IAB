import pandas as pd
import os

file_path = 'COBRANÇA UNIMED - PLANILHA GERUSA.xlsx'

# CRIAÇÃO DAS ABAS EM ARQUIVOS SEPARADOS

"""output_folder = 'abas'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

xls = pd.ExcelFile(file_path)

for sheet_name in xls.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    new_file_path = os.path.join(output_folder, f'{sheet_name}.xlsx')
    df.to_excel(new_file_path, index=False)
    print(f'Aba {sheet_name} salva em {new_file_path}')"""


