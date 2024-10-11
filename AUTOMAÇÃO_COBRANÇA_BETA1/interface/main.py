import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.file_processing.functions import carregar_arquivo_txt, carregar_arquivo_excel, processar_dados


class InterfaceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Processamento de Arquivos Excel e TXT")
        self.geometry("500x300")

        # Variáveis de controle
        self.excel_file = None
        self.dicionario_nomes_valores = None

        # Widgets
        self.label_arquivo_txt = tk.Label(self, text="Selecione o arquivo TXT:")
        self.label_arquivo_txt.pack(pady=10)
        self.button_arquivo_txt = tk.Button(self, text="Carregar Arquivo TXT", command=self.carregar_txt)
        self.button_arquivo_txt.pack(pady=5)

        self.label_arquivo_excel = tk.Label(self, text="Selecione o arquivo Excel:")
        self.label_arquivo_excel.pack(pady=10)
        self.button_arquivo_excel = tk.Button(self, text="Carregar Arquivo Excel", command=self.carregar_excel)
        self.button_arquivo_excel.pack(pady=5)

        self.label_aba = tk.Label(self, text="Selecione a aba:")
        self.label_aba.pack(pady=10)
        self.combobox_aba = ttk.Combobox(self)
        self.combobox_aba.pack(pady=5)

        self.button_processar = tk.Button(self, text="Processar Dados", command=self.processar)
        self.button_processar.pack(pady=20)

    def carregar_txt(self):
        content = carregar_arquivo_txt()
        if content:
            self.dicionario_nomes_valores = content

    def carregar_excel(self):
        self.excel_file = carregar_arquivo_excel(self.combobox_aba)

    def processar(self):
        if self.excel_file and self.dicionario_nomes_valores:
            aba_selecionada = self.combobox_aba.get()
            if aba_selecionada:
                processar_dados(self.excel_file, aba_selecionada, self.dicionario_nomes_valores)
            else:
                messagebox.showwarning("Aviso", "Por favor, selecione uma aba.")
        else:
            messagebox.showwarning("Aviso", "Por favor, carregue o arquivo TXT e Excel antes de processar.")

if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()
