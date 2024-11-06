import tkinter as tk
from tkinter import messagebox, ttk

def mostrar_loading():
    try:
        global loading_window
        loading_window = tk.Toplevel()
        loading_window.title("Carregando...")

        largura = 300
        altura = 150
        largura_tela = loading_window.winfo_screenwidth()
        altura_tela = loading_window.winfo_screenheight()
        x = (largura_tela / 2) - (largura / 2)
        y = (altura_tela / 2) - (altura / 2)
        loading_window.geometry(f"{largura}x{altura}+{int(x)}+{int(y)}")

        loading_label_text = tk.Label(loading_window, text="Processando, por favor aguarde...", font=("Arial", 12))
        loading_label_text.pack(pady=30)

        progress_bar = ttk.Progressbar(loading_window, mode='indeterminate')
        progress_bar.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM, padx=20, pady=20)
        progress_bar.start()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao mostrar a janela de carregamento: {str(e)}")

def fechar_loading():
    if loading_window:
        loading_window.destroy()