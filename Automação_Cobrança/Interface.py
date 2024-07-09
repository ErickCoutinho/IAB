import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from PIL import Image, ImageTk, ImageFont
from openpyxl import load_workbook
from funçoes import processar_arquivos
import threading

def selecionar_arquivo_txt():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos TXT", "*.txt")])
    if file_path:
        txt_path_entry.delete(0, tk.END)
        txt_path_entry.insert(tk.END, file_path)

def selecionar_arquivo_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
    if file_path:
        excel_path_entry.delete(0, tk.END)
        excel_path_entry.insert(tk.END, file_path)
        try:
            wb = load_workbook(filename=file_path, read_only=True)
            sheet_names = wb.sheetnames
            wb.close()
            aba_combo['values'] = sheet_names  # Atualiza o combobox com as abas disponíveis
        except FileNotFoundError:
            messagebox.showerror("Erro", f"O arquivo Excel '{file_path}' não foi encontrado.")

def mostrar_loading():
    global loading_window
    loading_window = tk.Toplevel(root)
    loading_window.title("Carregando...")
    loading_window.geometry("300x100")
    loading_label = tk.Label(loading_window, text="Processando, por favor aguarde...")
    loading_label.pack(pady=20)
    progress_bar = ttk.Progressbar(loading_window, mode='indeterminate')
    progress_bar.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM)
    progress_bar.start()

def esconder_loading():
    loading_window.destroy()

def processar():
    file_path_txt = txt_path_entry.get()
    file_path_excel = excel_path_entry.get()
    aba = aba_combo.get()
    if file_path_txt and file_path_excel and aba:
        threading.Thread(target=executar_processamento, args=(file_path_txt, file_path_excel, aba)).start()
    else:
        messagebox.showerror("Erro", "Selecione um arquivo TXT, um arquivo Excel e uma aba.")

def executar_processamento(file_path_txt, file_path_excel, aba):
    root.after(0, mostrar_loading)
    processar_arquivos(file_path_txt, file_path_excel, aba, txt_area)
    root.after(0, esconder_loading)

# Criar a interface gráfica
root = tk.Tk()
root.title("Selecionar Arquivos e Abas de Arquivos Excel")
root.configure(bg="black")

# Carregar a logo
logo_image = Image.open("SELO+IABRS COMPL_BRANCO.png")
logo_image = logo_image.resize((200, 150), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Fonte DIN (certifique-se de que o arquivo .ttf está no mesmo diretório ou forneça o caminho completo)
font_path = "DIN-Regular.ttf"
din_font = ImageFont.truetype(font_path, 12)

# Frame para a logo
logo_frame = tk.Frame(root, bg="black")
logo_frame.pack(pady=10)
logo_label = tk.Label(logo_frame, image=logo_photo, bg="black")
logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
logo_label.pack()

# Configurações do frame principal
frame = tk.Frame(root, bg="black")
frame.pack(padx=20, pady=20)

# Labels e entradas
labels = ["Selecione o arquivo Bancário:", "Selecione o arquivo Excel:", "Selecione a aba do arquivo Excel:"]
for i, text in enumerate(labels):
    tk.Label(frame, text=text, fg="white", bg="black", font=("DIN", 12)).grid(row=i, column=0, sticky='w', pady=5)

txt_path_entry = tk.Entry(frame, width=50, font=("DIN", 12))
txt_path_entry.grid(row=0, column=1, padx=10)
btn_selecionar_txt = tk.Button(frame, text="Selecionar", command=selecionar_arquivo_txt, font=("DIN", 12))
btn_selecionar_txt.grid(row=0, column=2, padx=10)

excel_path_entry = tk.Entry(frame, width=50, font=("DIN", 12))
excel_path_entry.grid(row=1, column=1, padx=10)
btn_selecionar_excel = tk.Button(frame, text="Selecionar", command=selecionar_arquivo_excel, font=("DIN", 12))
btn_selecionar_excel.grid(row=1, column=2, padx=10)

aba_combo = ttk.Combobox(frame, width=47, state='readonly', font=("DIN", 12))
aba_combo.grid(row=2, column=1, padx=10, columnspan=2)

btn_processar = tk.Button(root, text="Processar Arquivos", command=processar, font=("DIN", 12))
btn_processar.pack(pady=10)

txt_area = scrolledtext.ScrolledText(root, width=100, height=20, font=("DIN", 12), bg="black", fg="white")
txt_area.pack()

root.mainloop()

