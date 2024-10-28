import threading
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
from interface.interface_auxiliary.results import ResultadosInterface
from utils.file_processing.functions import carregar_arquivo_txt, carregar_arquivo_excel, processar_dados
from interface.interface_auxiliary.loading import fechar_loading, mostrar_loading


class InterfaceApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="simplex")

        self.title("Processamento de Arquivos Excel e TXT")
        self.geometry("550x350")

        # Variáveis de controle
        self.excel_file = None
        self.dicionario_nomes_valores = None
        self.dicionario_atrasados = None
        self.dicionario_cartorio = None
        self.dicionario_devolvido = None
        self.dicionario_tarifas = None
        self.dicionario_nao_encontrados = None

        # Widgets

        self.label_arquivo_excel = tk.Label(self, text="Selecione o arquivo Excel:")
        self.label_arquivo_excel.pack(pady=10)
        self.button_arquivo_excel = tk.Button(self, text="Carregar Arquivo Excel", command=self.carregar_excel)
        self.button_arquivo_excel.pack(pady=5)

        self.label_aba = tk.Label(self, text="Selecione a aba:")
        self.label_aba.pack(pady=10)
        self.combobox_aba = ttk.Combobox(self, state='disabled')  # Desabilitado inicialmente
        self.combobox_aba.pack(pady=5)

        self.label_arquivo_txt = tk.Label(self, text="Selecione o arquivo TXT:")
        self.label_arquivo_txt.pack(pady=10)
        self.button_arquivo_txt = tk.Button(self, text="Carregar Arquivo TXT", command=self.carregar_txt,
                                            state='disabled')  # Desabilitado inicialmente
        self.button_arquivo_txt.pack(pady=5)

        self.button_processar = tk.Button(self, text="Processar Dados", command=self.iniciar_processamento)
        self.button_processar.pack(pady=20)

    def carregar_excel(self):
        # Carrega o arquivo Excel e habilita o combobox de abas
        self.excel_file = carregar_arquivo_excel(self.combobox_aba)

        if self.excel_file:
            self.combobox_aba['state'] = 'readonly'  # Habilita a seleção de abas
            self.combobox_aba['values'] = self.excel_file.sheet_names  # Popula o combobox com as abas
            self.combobox_aba.current(0)  # Seleciona a primeira aba por padrão
            self.combobox_aba.bind("<<ComboboxSelected>>",
                                   self.habilitar_selecao_txt)  # Liga o evento de seleção da aba

    def habilitar_selecao_txt(self, event):
        # Habilita a seleção do arquivo TXT após selecionar a aba do Excel
        self.button_arquivo_txt['state'] = 'normal'

    def carregar_txt(self):
        if not self.excel_file:
            messagebox.showwarning("Aviso", "Por favor, carregue o arquivo Excel antes de continuar.")
            return

        aba_selecionada = self.combobox_aba.get()
        if not aba_selecionada:
            messagebox.showwarning("Aviso", "Por favor, selecione uma aba antes de continuar.")
            return

        # Carregar o arquivo TXT e passar o excel_file e aba_selecionada corretamente
        (self.dicionario_nomes_valores, self.dicionario_atrasados, self.dicionario_cartorio, self.dicionario_devolvido,
         self.dicionario_tarifas, self.dicionario_nao_encontrados) = carregar_arquivo_txt(excel_file=self.excel_file,
                                                                                          aba_selecionada=aba_selecionada)
        if self.dicionario_nomes_valores:
            print("Dicionário de nomes e valores carregado com sucesso.")
        else:
            print("Erro ao carregar o arquivo TXT.")

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
            nomes_nao_encontrados = list(self.dicionario_nao_encontrados)

            # Passa o dicionário de correspondências para a interface de resultados
            ResultadosInterface(nomes_processados, nomes_atrasados, nomes_cartorio, dicionario_correspondencias,
                                nomes_devolvidos, nomes_tarifas, nomes_nao_encontrados)

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
