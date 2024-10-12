import threading
import tkinter as tk
from tkinter import ttk, messagebox
from utils.file_processing.functions import carregar_arquivo_txt, carregar_arquivo_excel, processar_dados
from interface.interface_auxiliary.loading import fechar_loading, mostrar_loading


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

        self.button_processar = tk.Button(self, text="Processar Dados", command=self.iniciar_processamento)
        self.button_processar.pack(pady=20)

    def carregar_txt(self):
        content = carregar_arquivo_txt()
        if content:
            self.dicionario_nomes_valores = content

    def carregar_excel(self):
        self.excel_file = carregar_arquivo_excel(self.combobox_aba)

    def iniciar_processamento(self):
        """
        Inicia o processamento de dados em um thread separado para evitar travamentos
        da interface, enquanto exibe uma janela de carregamento.
        """
        if self.excel_file and self.dicionario_nomes_valores:
            aba_selecionada = self.combobox_aba.get()
            if aba_selecionada:
                mostrar_loading()
                threading.Thread(target=self.processar, args=(aba_selecionada,)).start()
            else:
                messagebox.showwarning("Aviso", "Por favor, selecione uma aba.")
        else:
            messagebox.showwarning("Aviso", "Por favor, carregue o arquivo TXT e Excel antes de processar.")

    def processar(self, aba_selecionada):
        """
        Método de processamento que será rodado em um thread separado.
        """
        try:
            processar_dados(self.excel_file, aba_selecionada, self.dicionario_nomes_valores)
            self.after(0, lambda: messagebox.showinfo("Sucesso", "Processamento concluído com sucesso!"))
        except Exception as e:
            # Capturar a exceção e exibir na thread principal
            self.after(0, self.mostrar_erro, e)
        finally:
            self.after(0, fechar_loading)

    def mostrar_erro(self, e):
        """
        Método auxiliar para exibir mensagens de erro em uma caixa de diálogo.
        """
        messagebox.showerror("Erro", f"Erro ao processar os dados: {str(e)}")


if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()
