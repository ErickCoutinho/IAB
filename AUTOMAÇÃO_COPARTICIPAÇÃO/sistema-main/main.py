import tkinter as tk
from defs_adicionais import escolher_arquivo, escolher_local_saida_csv, escolher_arquivo_csv, escolher_arquivo_excel, processar, processar_excel

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
tk.Button(root, text="Escolher", command=lambda: escolher_arquivo(entrada_txt)).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Arquivo de saída (.csv):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=saida_csv, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Salvar", command=lambda: escolher_local_saida_csv(saida_csv)).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Arquivo CSV com Coparticipações:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=entrada_csv, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Escolher", command=lambda: escolher_arquivo_csv(entrada_csv)).grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Arquivo Excel para atualizar:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=entrada_excel, width=50).grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Escolher", command=lambda: escolher_arquivo_excel(entrada_excel)).grid(row=3, column=2, padx=10, pady=5)

tk.Button(root, text="Processar LST para CSV", command=lambda: processar(entrada_txt, saida_csv)).grid(row=4, column=1, padx=10, pady=20)
tk.Button(root, text="Atualizar Coparticipações", command=lambda: processar_excel(entrada_csv, entrada_excel)).grid(row=5, column=1, padx=10, pady=20)

# Iniciar o loop da interface
root.mainloop()
