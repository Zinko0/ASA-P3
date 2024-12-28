import pulp

# Cria o problema de programação linear
entrada = input()
fabricas, paises, criancas = map(int, entrada.split())

lista_fabricas = []
lista_paises = []
lista_criancas = []

stocks_sum = 0
min_brinquedos_sum = 0
for i in range(fabricas):
    linha = input()
    ident_fabrica, ident_pais_fabrica, stock_max = map(int, linha.split())
    lista_fabricas.append((ident_fabrica, ident_pais_fabrica, stock_max))
    stocks_sum += stock_max


for i in range(paises):
    linha = input()
    ident_pais, limite_exportacoes, min_brinquedos = map(int, linha.split())
    lista_paises.append((ident_pais, limite_exportacoes, min_brinquedos))
    min_brinquedos_sum += min_brinquedos

for i in range(criancas):
    linha = input()
    lista = list(map(int, linha.split()))
    id_crianca = lista[0]
    id_pais = lista[1]
    presentes_desejados = lista[2:]
    lista_criancas.append((id_crianca, id_pais, presentes_desejados))

if stocks_sum < min_brinquedos_sum:
    print("-1")
else:
    # Define o problema de maximização
    prob = pulp.LpProblem("Distribuicao_de_Presentes", pulp.LpMaximize)

    # Cria as variáveis de decisão
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(criancas) for j in lista_criancas[i][2]), cat='Binary')

    # Função objetivo: Maximizar o número de presentes distribuídos
    prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2])

    # Restrição: Cada criança deve receber exatamente um presente
    for i in range(criancas):
        prob += pulp.lpSum(x[i, j] for j in lista_criancas[i][2]) == 1

    # Restrição: O presente deve estar na lista de desejos da criança
    for i in range(criancas):
        for j in lista_criancas[i][2]:
            prob += x[i, j] <= 1

    # Restrição: Cada país deve receber pelo menos o número mínimo de brinquedos
    for pais in lista_paises:
        ident_pais = pais[0]
        min_brinquedos = pais[2]
        prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if lista_criancas[i][1] == ident_pais) >= min_brinquedos

    # Restrição: Cada país não pode exportar mais do que o limite de exportações
    for pais in lista_paises:
        ident_pais = pais[0]
        limite_exportacoes = pais[1]
        prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if lista_criancas[i][1] == ident_pais) <= limite_exportacoes

    # Resolve o problema
    prob.solve()    

    # Imprime os resultados
    total_presents = 0
    for i in range(criancas):
        for j in lista_criancas[i][2]:
            if pulp.value(x[i, j]) == 1:
                total_presents += 1
    print(total_presents)


