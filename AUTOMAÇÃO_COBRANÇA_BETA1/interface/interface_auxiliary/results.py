import tkinter as tk

class ResultadosInterface(tk.Toplevel):
    def __init__(self, nomes_processados, nomes_atrasados, nomes_cartorio, dicionario_correspondencias, nomes_devolvidos, nomes_tarifas):
        super().__init__()

        self.title("Resultados do Processamento")
        self.geometry("800x600")

        # Título
        titulo = tk.Label(self, text="Resultados do Processamento", font=("Arial", 16))
        titulo.pack(pady=10)

        # Labels para quantidade de nomes
        label_quantidade_processados = tk.Label(self, text=f"Nomes Extraidos do TXT: {len(nomes_processados)}", font=("Arial", 12))
        label_quantidade_processados.pack(pady=5)

        label_quantidade_correspondentes = tk.Label(self, text=f"Nomes do Correspondentes: {len(dicionario_correspondencias)}", font=("Arial", 12))
        label_quantidade_correspondentes.pack(pady=5)

        label_quantidade_atrasados = tk.Label(self, text=f"Nomes Atrasados: {len(nomes_atrasados)}", font=("Arial", 12))
        label_quantidade_atrasados.pack(pady=5)

        label_quantidade_devolvidos = tk.Label(self, text=f"Nomes Devolvidos: {len(nomes_devolvidos)}", font=("Arial", 12))
        label_quantidade_devolvidos.pack(pady=5)

        label_quantidade_cartorio = tk.Label(self, text=f"Nomes do Cartório: {len(nomes_cartorio)}", font=("Arial", 12))
        label_quantidade_cartorio.pack(pady=5)

        label_quantidade_tarifas = tk.Label(self, text=f"Nomes Tarifas: {len(nomes_tarifas)}", font=("Arial", 12))
        label_quantidade_tarifas.pack(pady=5)


        # Frame para os nomes tarifários

        # Frame para os nomes processados
        self.frame_processados = self.create_frame("Nomes Extraidos do TXT", nomes_processados)
        self.frame_processados.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame para as correspondências
        self.frame_correspondencias = self.create_frame("Nomes Correspondentes", dicionario_correspondencias)
        self.frame_correspondencias.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame para os nomes atrasados
        self.frame_atrasados = self.create_frame("Nomes Atrasados", nomes_atrasados)
        self.frame_atrasados.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame para os nomes devolvidos
        self.frame_devolvidos = self.create_frame("Nomes Devolvidos", nomes_devolvidos)
        self.frame_devolvidos.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame para os nomes do cartório
        self.frame_cartorio = self.create_frame("Nomes do Cartório", nomes_cartorio)
        self.frame_cartorio.pack(fill="both", expand=True, padx=10, pady=5)

        self.frame_tarifas = self.create_frame("Nomes Tarifas", nomes_tarifas)
        self.frame_tarifas.pack(fill="both", expand=True, padx=10, pady=5)

        # Botão para fechar a janela
        fechar_button = tk.Button(self, text="Fechar", command=self.destroy)
        fechar_button.pack(pady=10)

    def create_frame(self, title, nomes):
        frame = tk.LabelFrame(self, text=title, padx=10, pady=10)

        # Listbox com nomes
        lista = tk.Listbox(frame, selectmode=tk.SINGLE)
        for nome in nomes:
            lista.insert(tk.END, nome)

        # Inicialmente escondido
        lista.pack(fill="both", expand=True)
        lista.pack_forget()  # Esconde a lista inicialmente

        # Botão para expandir/colapsar
        toggle_button = tk.Button(frame, text="+", command=lambda: self.toggle_nomes(lista, toggle_button))
        toggle_button.pack(pady=5)

        # Expande a lista
        frame.lista = lista
        frame.toggle_button = toggle_button

        return frame

    def toggle_nomes(self, lista, toggle_button):
        if lista.winfo_ismapped():
            lista.pack_forget()  # Esconde a lista
            toggle_button.config(text="+")  # Muda o texto do botão
        else:
            lista.pack(fill="both", expand=True)  # Mostra a lista
            toggle_button.config(text="-")  # Muda o texto do botão
