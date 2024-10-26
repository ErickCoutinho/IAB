import tkinter as tk
import ttkbootstrap as ttk  # Adiciona ttkbootstrap para usar temas

class ResultadosInterface(ttk.Toplevel):
    def __init__(self, nomes_processados, nomes_atrasados, nomes_cartorio, dicionario_correspondencias, nomes_devolvidos, nomes_tarifas):
        super().__init__()

        self.title("Resultados do Processamento")
        self.geometry("800x600")

        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical para o Canvas
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # Frame que conterá todos os widgets
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Título
        titulo = ttk.Label(scrollable_frame, text="Resultados do Processamento", font=("Arial", 16), bootstyle="info")
        titulo.pack(pady=10)

        # Labels para quantidade de nomes
        label_quantidade_processados = ttk.Label(scrollable_frame, text=f"Nomes Extraidos do TXT: {len(nomes_processados)}", font=("Arial", 12), bootstyle="primary")
        label_quantidade_processados.pack(pady=5)

        label_quantidade_correspondentes = ttk.Label(scrollable_frame, text=f"Nomes Correspondentes: {len(dicionario_correspondencias)}", font=("Arial", 12), bootstyle="primary")
        label_quantidade_correspondentes.pack(pady=5)

        label_quantidade_atrasados = ttk.Label(scrollable_frame, text=f"Nomes Atrasados: {len(nomes_atrasados)}", font=("Arial", 12), bootstyle="primary")
        label_quantidade_atrasados.pack(pady=5)

        label_quantidade_devolvidos = ttk.Label(scrollable_frame, text=f"Nomes Devolvidos: {len(nomes_devolvidos)}", font=("Arial", 12), bootstyle="primary")
        label_quantidade_devolvidos.pack(pady=5)

        label_quantidade_cartorio = ttk.Label(scrollable_frame, text=f"Nomes do Cartório: {len(nomes_cartorio)}", font=("Arial", 12), bootstyle="primary")
        label_quantidade_cartorio.pack(pady=5)

        label_quantidade_tarifas = ttk.Label(scrollable_frame, text=f"Nomes Tarifas: {len(nomes_tarifas)}", font=("Arial", 12), bootstyle="primary")
        label_quantidade_tarifas.pack(pady=5)

        # Frame para os nomes
        self.frames_listas = []
        self.frames_listas.append(self.create_frame(scrollable_frame, "Nomes Extraidos do TXT", nomes_processados))
        self.frames_listas[-1].pack(fill="both", expand=True, padx=10, pady=5)

        self.frames_listas.append(self.create_frame(scrollable_frame, "Nomes Correspondentes", dicionario_correspondencias))
        self.frames_listas[-1].pack(fill="both", expand=True, padx=10, pady=5)

        self.frames_listas.append(self.create_frame(scrollable_frame, "Nomes Atrasados", nomes_atrasados))
        self.frames_listas[-1].pack(fill="both", expand=True, padx=10, pady=5)

        self.frames_listas.append(self.create_frame(scrollable_frame, "Nomes Devolvidos", nomes_devolvidos))
        self.frames_listas[-1].pack(fill="both", expand=True, padx=10, pady=5)

        self.frames_listas.append(self.create_frame(scrollable_frame, "Nomes do Cartório", nomes_cartorio))
        self.frames_listas[-1].pack(fill="both", expand=True, padx=10, pady=5)

        self.frames_listas.append(self.create_frame(scrollable_frame, "Nomes Tarifas", nomes_tarifas))
        self.frames_listas[-1].pack(fill="both", expand=True, padx=10, pady=5)

        # Botão para fechar a janela
        fechar_button = ttk.Button(scrollable_frame, text="Fechar", command=self.destroy, bootstyle="danger")
        fechar_button.pack(pady=10)

    def create_frame(self, parent, title, nomes):
        frame = ttk.LabelFrame(parent, text=title, padding=10, bootstyle="info")

        # Frame interno para lista e trackbar
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True)

        # Listbox com nomes
        lista = tk.Listbox(list_frame, selectmode=tk.SINGLE, height=10, width=180)
        for nome in nomes:
            lista.insert(tk.END, nome)

        lista.pack(side=tk.LEFT, fill="both", expand=True)

        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=lista.yview)
        lista.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Trackbar individual para cada Listbox
        trackbar_individual = tk.Scale(frame, from_=1, to=20, orient=tk.HORIZONTAL, label="Ajuste da Lista")
        trackbar_individual.set(10)  # Valor inicial da altura
        trackbar_individual.pack(fill="x", padx=10, pady=5)
        trackbar_individual.bind("<Motion>", lambda e, l=lista: self.adjust_list(l, trackbar_individual))

        return frame

    def adjust_list(self, lista, trackbar):
        """Ajusta o tamanho de um Listbox individual."""
        lista.config(height=trackbar.get())
