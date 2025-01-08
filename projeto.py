import pulp

# Cria o problema de programação linear
entrada = input()
fabricas, paises, criancas = map(int, entrada.split())

lista_fabricas = []
lista_paises = []
lista_criancas = []

stocks_sum = 0
min_brinquedos_sum = 0
fabricas_por_pais = {}

for i in range(fabricas + paises + criancas):
    linha = input()

    if i < fabricas:
        ident_fabrica, ident_pais_fabrica, stock_max = map(int, linha.split())

        lista_fabricas.append((ident_fabrica, ident_pais_fabrica, stock_max))
        stocks_sum += stock_max
        if ident_pais_fabrica not in fabricas_por_pais:
            fabricas_por_pais[ident_pais_fabrica] = []
        fabricas_por_pais[ident_pais_fabrica].append(ident_fabrica)

    elif i < fabricas + paises:
        ident_pais, limite_exportacoes, min_brinquedos = map(int, linha.split())
        if limite_exportacoes > 0:  # Verifica se o limite de exportações é maior que 0
            lista_paises.append((ident_pais, limite_exportacoes, min_brinquedos))
            min_brinquedos_sum += min_brinquedos
            
    else:
        lista = list(map(int, linha.split()))
        id_crianca = lista[0]
        id_pais = lista[1]
        presentes_desejados = lista[2:]
        presentes_existentes = []
        for presentes in presentes_desejados:
            if lista_fabricas[presentes-1][2] != 0:
                presentes_existentes.append(presentes)
        lista_criancas.append((id_crianca, id_pais,presentes_existentes))

if stocks_sum < min_brinquedos_sum:
    print("-1")
else:
    # Define o problema de maximização
    prob = pulp.LpProblem("Distribuicao_de_Presentes", pulp.LpMaximize)

    # Cria as variáveis de decisão contínuas
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(criancas) for j in lista_criancas[i][2]), cat='Binary')

    # Função objetivo: Maximizar o número de presentes distribuídos
    prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2])

    # Restrição: Cada criança deve receber no máximo um presente desejado
    for i in range(len(lista_criancas)):
        if len(lista_criancas[i][2]) > 1:
            prob += pulp.lpSum(x[i, j] for j in lista_criancas[i][2]) <= 1

    # Combina as restrições de país e estoque de fábrica
    for ident_pais, limite_exportacoes, min_brinquedos in lista_paises:
        num_stock = sum(f[2] for f in lista_fabricas if f[1] == ident_pais)
        if min_brinquedos > 0:
            prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if lista_criancas[i][1] == ident_pais) >= min_brinquedos
        if limite_exportacoes < num_stock:
            prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if j in fabricas_por_pais.get(ident_pais, []) and lista_criancas[i][1] != ident_pais) <= limite_exportacoes

    # Restrição: O estoque de cada fábrica não pode ser excedido
    for ident_fabrica, _, stock_max in lista_fabricas:
        if stock_max > 0:
            prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if j == ident_fabrica) <= stock_max

    # Resolve o problema
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    if pulp.LpStatus[prob.status] != 'Optimal':
        print("-1")
    else:
        # Imprime os resultados
        print(int(pulp.value(prob.objective)))
