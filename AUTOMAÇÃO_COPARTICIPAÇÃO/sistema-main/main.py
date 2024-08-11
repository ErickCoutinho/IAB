import tkinter as tk
from tkinter import StringVar
from ttkbootstrap import Style
from ttkbootstrap import ttk
from defs_adicionais import escolher_arquivo, escolher_local_saida_csv, escolher_arquivo_csv, escolher_arquivo_excel, processar, processar_excel

# Configurar estilo Bootstrap
style = Style(theme='superhero')  # Escolha um tema Bootstrap

# Interface
root = style.master
root.title("Processador de Arquivos Unimed")

# Variáveis de caminho de arquivo
entrada_txt = StringVar()
saida_csv = StringVar()
entrada_csv = StringVar()
entrada_excel = StringVar()

# Frames para organizar o layout
frame_entrada = ttk.Frame(root, padding=10)
frame_entrada.grid(row=0, column=0, sticky="ew")

frame_saida = ttk.Frame(root, padding=10)
frame_saida.grid(row=1, column=0, sticky="ew")

frame_csv = ttk.Frame(root, padding=10)
frame_csv.grid(row=2, column=0, sticky="ew")

frame_excel = ttk.Frame(root, padding=10)
frame_excel.grid(row=3, column=0, sticky="ew")

frame_botoes = ttk.Frame(root, padding=10)
frame_botoes.grid(row=4, column=0, sticky="ew")

# Layout com Labels, Entradas e Botões estilizados
style.configure('TLabel', padding=5)
style.configure('TButton', padding=5)

ttk.Label(frame_entrada, text="Arquivo de entrada - Unimed (.LST):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
ttk.Entry(frame_entrada, textvariable=entrada_txt, width=50).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(frame_entrada, text="Escolher", command=lambda: escolher_arquivo(entrada_txt), bootstyle="primary-outline").grid(row=0, column=2, padx=10, pady=5)

ttk.Label(frame_saida, text="Arquivo de saída (.csv):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
ttk.Entry(frame_saida, textvariable=saida_csv, width=50).grid(row=1, column=1, padx=10, pady=5)
ttk.Button(frame_saida, text="Salvar", command=lambda: escolher_local_saida_csv(saida_csv), bootstyle="success-outline").grid(row=1, column=2, padx=10, pady=5)

ttk.Label(frame_csv, text="Arquivo CSV com Coparticipações:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
ttk.Entry(frame_csv, textvariable=entrada_csv, width=50).grid(row=2, column=1, padx=10, pady=5)
ttk.Button(frame_csv, text="Escolher", command=lambda: escolher_arquivo_csv(entrada_csv), bootstyle="info-outline").grid(row=2, column=2, padx=10, pady=5)

ttk.Label(frame_excel, text="Arquivo Excel para atualizar:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
ttk.Entry(frame_excel, textvariable=entrada_excel, width=50).grid(row=3, column=1, padx=10, pady=5)
ttk.Button(frame_excel, text="Escolher", command=lambda: escolher_arquivo_excel(entrada_excel), bootstyle="warning-outline").grid(row=3, column=2, padx=10, pady=5)

ttk.Button(frame_botoes, text="Processar LST para CSV", command=lambda: processar(entrada_txt, saida_csv), bootstyle="primary").grid(row=4, column=0, padx=10, pady=20)
ttk.Button(frame_botoes, text="Atualizar Coparticipações", command=lambda: processar_excel(entrada_csv, entrada_excel), bootstyle="success").grid(row=4, column=1, padx=10, pady=20)

# Iniciar o loop da interface
root.mainloop()

