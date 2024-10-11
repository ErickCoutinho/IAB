def limpar_valor(valor):
    """Limpa e converte o valor para float, removendo pontos extras e corrigindo a separação decimal."""
    # Remove todos os pontos, exceto o último (para separação decimal)
    if isinstance(valor, str):
        valor = valor.replace(',', '.')
        partes = valor.split('.')
        if len(partes) > 2:
            valor = ''.join(partes[:-1]) + '.' + partes[-1]  # Mantém o último ponto como separador decimal
    return float(valor)  # Converte para float


def buscar_taxa_bancaria(linha_inicial, taxas_bancarias, nomes_dict, limite_busca=4):
    """
    Busca a taxa bancária nos índices subsequentes, mas para ao encontrar outro nome ou ultrapassar o limite de busca.
    """
    indice = linha_inicial + 1
    contador = 0  # Contador para limitar o número de linhas verificadas

    while indice not in nomes_dict and contador < limite_busca:  # Continua buscando até encontrar outro nome ou passar do limite
        if indice in taxas_bancarias:  # Se encontrar a taxa bancária, retorna o valor
            return taxas_bancarias[indice]
        indice += 1
        contador += 1

    return 0  # Se encontrar um novo nome ou não encontrar a taxa, retorna 0


def buscar_juros(linha_inicial, juros_dict, nomes_dict, limite_busca=4):
    """
    Busca os juros nos índices subsequentes, mas para ao encontrar outro nome ou ultrapassar o limite de busca.
    """
    indice = linha_inicial + 1
    contador = 0  # Contador para limitar o número de linhas verificadas

    while indice not in nomes_dict and contador < limite_busca:  # Continua buscando até encontrar outro nome ou passar do limite
        if indice in juros_dict:  # Se encontrar os juros, retorna o valor
            return juros_dict[indice]
        indice += 1
        contador += 1

    return 0  # Se encontrar um novo nome ou não encontrar os juros, retorna 0
