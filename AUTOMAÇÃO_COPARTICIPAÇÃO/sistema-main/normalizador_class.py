import io

class Normalizador:
    def __init__(self):
        self.arquivo_entrada = None
        self.arquivo_saida = io.StringIO()  # Armazena o conteúdo processado em memória

    def definir_arquivo_entrada(self, caminho_arquivo):
        """Define o caminho do arquivo de entrada."""
        self.arquivo_entrada = caminho_arquivo

    def remover_cabecalhos(self, linhas):
        """Remove os cabeçalhos de mudança de página e as linhas subsequentes."""
        i = 0
        while i < len(linhas):
            if "DATASUL Saude - FATURAMENTO" in linhas[i]:
                del linhas[i-2:i + 12]
            else:
                i += 1
        return linhas

    def processar_arquivo(self):
        if not self.arquivo_entrada:
            raise ValueError("O arquivo de entrada não foi definido.")

        # Leitura do arquivo de entrada
        with open(self.arquivo_entrada, "r") as f:
            linhas = f.readlines()

        # Remover cabeçalhos
        linhas_sem_cabecalhos = self.remover_cabecalhos(linhas)

        # Salvar no "arquivo" de saída em memória
        self.arquivo_saida.write(''.join(linhas_sem_cabecalhos))

    def obter_conteudo_saida(self):
        """Retorna o conteúdo do arquivo de saída."""
        self.arquivo_saida.seek(0)  # Move para o início do StringIO
        return self.arquivo_saida.read()
