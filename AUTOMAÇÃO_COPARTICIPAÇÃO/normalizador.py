
def remover_cabecalhos(linhas):
    """Remove os cabeçalhos de mudança de página e as linhas subsequentes."""
    i = 0
    while i < len(linhas):
        if "DATASUL Saude - FATURAMENTO" in linhas[i]:
            del linhas[i-2:i + 12]
        else:
            i += 1
    return linhas


def exibir_linhas(linhas):
    """Exibe as linhas fornecidas."""
    for linha in linhas:
        print(linha.strip())

# Leitura do arquivo de entrada
input_file = "documents\\PART 07.LST"
with open(input_file, "r") as f:
    linhas = f.readlines()


linhas_sem_cabecalhos = remover_cabecalhos(linhas)
exibir_linhas(linhas_sem_cabecalhos)


output_file = "unimed___.txt"
with open(output_file, "w") as f:
    f.writelines(linhas_sem_cabecalhos)

