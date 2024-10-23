import threading
import ttkbootstrap as ttk  # Adiciona ttkbootstrap para usar temas
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from interface.interface_auxiliary.results import ResultadosInterface
from utils.file_processing.functions import carregar_arquivo_txt, carregar_arquivo_excel, processar_dados
from interface.interface_auxiliary.loading import fechar_loading, mostrar_loading


class InterfaceApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")

        self.title("Processamento de Arquivos Excel e TXT")
        self.geometry("550x350")

        # Variáveis de controle
        self.excel_file = None
        self.dicionario_nomes_valores = None
        self.dicionario_atrasados = None
        self.dicionario_cartorio = None
        self.dicionario_devolvido = None
        self.dicionario_tarifas = None

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
        (self.dicionario_nomes_valores, self.dicionario_atrasados, self.dicionario_cartorio, self.dicionario_devolvido,
         self.dicionario_tarifas) = carregar_arquivo_txt()
        if self.dicionario_nomes_valores:
            print("Dicionário de nomes e valores carregado com sucesso.")

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
        try:
            dicionario_correspondencias = processar_dados(self.excel_file, aba_selecionada,
                                                          self.dicionario_nomes_valores)

            # Obtém os nomes
            nomes_atrasados = list(self.dicionario_atrasados.keys())
            nomes_processados = list(self.dicionario_nomes_valores.keys())
            nomes_cartorio = list(self.dicionario_cartorio.keys())
            nomes_devolvidos = list(self.dicionario_devolvido.keys())
            nomes_tarifas = list(self.dicionario_tarifas)

            # Passa o dicionário de correspondências para a interface de resultados
            ResultadosInterface(nomes_processados, nomes_atrasados, nomes_cartorio, dicionario_correspondencias,
                                nomes_devolvidos, nomes_tarifas)

            self.after(0, lambda: messagebox.showinfo("Sucesso", "Processamento concluído com sucesso!"))
        except Exception as e:
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
