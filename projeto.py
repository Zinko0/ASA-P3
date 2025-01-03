import pulp



entrada = input()
fabricas, paises, criancas = map(int, entrada.split())

lista_fabricas = []
lista_paises = []
lista_criancas = []

stocks_sum = 0
min_brinquedos_sum = 0
n_exportacoes = 0
fabricas_por_pais = {}

for i in range(fabricas):
    linha = input()
    ident_fabrica, ident_pais_fabrica, stock_max = map(int, linha.split())
    lista_fabricas.append((ident_fabrica, ident_pais_fabrica, stock_max,n_exportacoes))
    stocks_sum += stock_max
    if ident_pais_fabrica not in fabricas_por_pais:
        fabricas_por_pais[ident_pais_fabrica] = []
    fabricas_por_pais[ident_pais_fabrica].append(ident_fabrica)


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
    
# Cria o problema de programação linear
# Define o problema de maximização
prob = pulp.LpProblem("Distribuicao_de_Presentes", pulp.LpMaximize)

# Cria as variáveis de decisão
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(criancas) for j in lista_criancas[i][2]), cat='Binary')

# Função objetivo: Maximizar o número de presentes distribuídos
prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2])

# Restrição: Cada criança deve receber exatamente um presente desejado ou nada
for i in range(criancas):
    prob += pulp.lpSum(x[i, j] for j in lista_criancas[i][2]) <= 1

# Restrição: Cada país deve receber pelo menos o número mínimo de brinquedos
for pais in lista_paises:
    ident_pais = pais[0]
    min_brinquedos = pais[2]
    limite_exportacoes = pais[1]
    prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if lista_criancas[i][1] == ident_pais) >= min_brinquedos

    # Restrição: Todas as fábricas de um país devem exportar no máximo o limite de exportações
    prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if j in fabricas_por_pais[ident_pais] and lista_criancas[i][1] != ident_pais) <= limite_exportacoes
    
    # Restrição: O estoque de cada fábrica não pode ser excedido
    for fabrica in lista_fabricas:
        ident_fabrica = fabrica[0]
        stock_max = fabrica[2]
        prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if j == ident_fabrica) <= stock_max

        # Restrição: Todas as fábricas de um país devem exportar no máximo o limite de exportações
        ident_pais_fabrica = fabrica[1]
        if ident_pais_fabrica == ident_pais:
            prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if j == ident_fabrica) <= limite_exportacoes



# Resolve o problema
prob.solve(pulp.PULP_CBC_CMD(msg=False))

if pulp.LpStatus[prob.status] != 'Optimal':
    print("-1")
else:
    # Imprime os resultados
    print(int(pulp.value(prob.objective)))


    


"""# Restrição: Todas as fábricas de um país devem exportar no máximo o limite de exportações
for pais in lista_paises:
    ident_pais = pais[0]
    limite_exportacoes = pais[1]
    for fabrica in lista_fabricas:
        ident_fabrica = fabrica[0]
        ident_pais_fabrica = fabrica[1]
        if ident_pais_fabrica == ident_pais:
            prob += pulp.lpSum(x[i, j] for i in range(criancas) for j in lista_criancas[i][2] if j == ident_fabrica) <= limite_exportacoes"""