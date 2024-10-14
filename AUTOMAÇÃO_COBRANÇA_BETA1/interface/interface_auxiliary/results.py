import tkinter as tk

class ResultadosInterface(tk.Toplevel):
    def __init__(self, nomes_processados, nomes_atrasados):
        super().__init__()

        self.title("Resultados do Processamento")
        self.geometry("600x400")

        # Título
        titulo = tk.Label(self, text="Resultados do Processamento", font=("Arial", 16))
        titulo.pack(pady=10)

        # Frame para os nomes processados
        frame_processados = tk.LabelFrame(self, text="Nomes Processados", padx=10, pady=10)
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

        # Botão para fechar a janela
        fechar_button = tk.Button(self, text="Fechar", command=self.destroy)
        fechar_button.pack(pady=10)
