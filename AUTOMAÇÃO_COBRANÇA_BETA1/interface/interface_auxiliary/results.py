import tkinter as tk

class ResultadosInterface(tk.Toplevel):
    def __init__(self, nomes_processados, nomes_atrasados, nomes_cartorio):
        super().__init__()

        self.title("Resultados do Processamento")
        self.geometry("800x500")

        # Título
        titulo = tk.Label(self, text="Resultados do Processamento", font=("Arial", 16))
        titulo.pack(pady=10)

        # Quantidade de nomes
        quantidade_processados = len(nomes_processados)
        quantidade_atrasados = len(nomes_atrasados)
        quantidade_cartorio = len(nomes_cartorio)

        # Labels para quantidade de nomes
        label_quantidade = tk.Label(self, text=f"Nomes Encontratos TXT: {quantidade_processados}", font=("Arial", 12))
        label_quantidade.pack(pady=5)

        label_quantidade_atrasados = tk.Label(self, text=f"Nomes Atrasados: {quantidade_atrasados}", font=("Arial", 12))
        label_quantidade_atrasados.pack(pady=5)

        label_quantidade_cartorio = tk.Label(self, text=f"Nomes do Cartório: {quantidade_cartorio}", font=("Arial", 12))
        label_quantidade_cartorio.pack(pady=5)

        # Frame para os nomes processados
        frame_processados = tk.LabelFrame(self, text="Nomes Encontratos TXT", padx=10, pady=10)
        frame_processados.pack(fill="both", expand=True, padx=10, pady=5)

        self.lista_processados = tk.Listbox(frame_processados, selectmode=tk.SINGLE)
        for nome in nomes_processados:
            self.lista_processados.insert(tk.END, nome)
        self.lista_processados.pack(fill="both", expand=True)

        # Frame para os nomes atrasados
        frame_atrasados = tk.LabelFrame(self, text="Nomes Atrasados", padx=10, pady=10)
        frame_atrasados.pack(fill="both", expand=True, padx=10, pady=5)

        self.lista_atrasados = tk.Listbox(frame_atrasados, selectmode=tk.SINGLE)
        for nome in nomes_atrasados:
            self.lista_atrasados.insert(tk.END, nome)
        self.lista_atrasados.pack(fill="both", expand=True)

        # Frame para os nomes do cartório
        frame_cartorio = tk.LabelFrame(self, text="Nomes do Cartório", padx=10, pady=10)
        frame_cartorio.pack(fill="both", expand=True, padx=10, pady=5)

        self.lista_cartorio = tk.Listbox(frame_cartorio, selectmode=tk.SINGLE)
        for nome in nomes_cartorio:
            self.lista_cartorio.insert(tk.END, nome)
        self.lista_cartorio.pack(fill="both", expand=True)

        # Botão para fechar a janela
        fechar_button = tk.Button(self, text="Fechar", command=self.destroy)
        fechar_button.pack(pady=10)
