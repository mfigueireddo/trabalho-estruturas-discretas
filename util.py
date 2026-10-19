from grafos import Aresta, Grafo, arestas, circuito_euler, conexo, euleriano, graus, todos_graus_pares, valida_circuito
from resultados import ResultadoProporcao

def sim_nao(valor: bool) -> str:
    if valor:
        return "sim"
    return "não"

def ok_falhou(valor: bool) -> str:
    if valor:
        return "OK"
    return "FALHOU"

def debug(mensagem: str, debug_mode: bool, linha_em_branco_antes: bool = False) -> None:
    """Imprime mensagem com o prefixo [debug], apenas quando debug_mode está ligado."""
    if not debug_mode:
        return
    if linha_em_branco_antes:
        print()
    print(f"[debug] {mensagem}")

def exibe_arestas(lista_arestas: list[Aresta]) -> None:
    """Imprime as arestas no formato (u,v), dez por linha."""
    for inicio in range(0, len(lista_arestas), 10):
        textos_arestas: list[str] = []
        for u, v in lista_arestas[inicio:inicio + 10]:
            textos_arestas.append(f"({u},{v})")
        print(" ".join(textos_arestas))

def exibe_graus(grafo: Grafo) -> None:
    """Imprime o grau de cada vértice, um por linha, no formato v1: 2."""
    for v, g in graus(grafo).items():
        print(f"v{v}: {g}")

def exibe_adjacencia(grafo: Grafo) -> None:
    """Imprime a lista de adjacência: um vértice por linha, com seus vizinhos em ordem."""
    for vertice in sorted(grafo):
        textos_vizinhos: list[str] = []
        for vizinho in sorted(grafo[vertice]):
            textos_vizinhos.append(str(vizinho))

        if textos_vizinhos:
            vizinhos: str = ", ".join(textos_vizinhos)
        else:
            vizinhos = "(sem vizinhos)"

        print(f"v{vertice}: {vizinhos}")

def exibe_matriz_adjacencia(grafo: Grafo) -> None:
    """Imprime a matriz de adjacência: 1 onde há aresta e . onde não há."""
    vertices: list[int] = sorted(grafo)

    # Largura da maior etiqueta de vértice, para alinhar as colunas.
    largura: int = 0
    for vertice in vertices:
        largura = max(largura, len(str(vertice)))

    # Cabeçalho com o número de cada coluna.
    cabecalho: list[str] = []
    for vertice in vertices:
        cabecalho.append(str(vertice).rjust(largura))
    print(" " * largura, " ".join(cabecalho))

    # Uma linha por vértice: 1 se há aresta até a coluna, . caso contrário.
    for u in vertices:
        celulas: list[str] = []
        for v in vertices:
            if v in grafo[u]:
                simbolo: str = "1"
            else:
                simbolo = "."
            celulas.append(simbolo.rjust(largura))
        print(str(u).rjust(largura), " ".join(celulas))

def imprime_circuito_euler(circuito: list[int]) -> None:
    """Imprime os vértices do circuito separados por " -> ", como 1 -> 2 -> 8 -> 1."""
    texto: str = ""
    for i, v in enumerate(circuito):
        if i > 0:
            texto += " -> "
        texto += str(v)
    print(texto)

def imprime_titulo(titulo: str) -> None:
    """Imprime um título de etapa destacado, com uma linha em branco antes."""
    barra: str = "=" * max(32, len(titulo))
    print()
    print(barra)
    print(titulo.upper())
    print(barra)

def imprime_subtitulo(subtitulo: str) -> None:
    """Imprime o título de um bloco de dados, com uma linha em branco antes."""
    print()
    print(f"--- {subtitulo} ---")

def imprimir_primeiro_euleriano(grafo: Grafo, grafos_gerados: int, numero_de_vertices: int, probabilidade_par_de_vertices_virar_aresta: float, seed: int) -> None:
    imprime_subtitulo("Parâmetros da geração dos grafos")
    print(f"Número de vértices: {numero_de_vertices}")
    print(f"Probabilidade p: {probabilidade_par_de_vertices_virar_aresta:.2f}")
    print(f"Seed: {seed}")

    imprime_subtitulo("Resultado da busca")
    print("Grafo Euleriano encontrado!")
    print(f"Número de grafos gerados até encontrá-lo: {grafos_gerados}")

    lista_arestas: list[Aresta] = arestas(grafo)
    imprime_subtitulo(f"Arestas do grafo Euleriano encontrado ({len(lista_arestas)})")
    exibe_arestas(lista_arestas)

    imprime_subtitulo("Grau de cada vértice do grafo Euleriano encontrado")
    exibe_graus(grafo)

    imprime_subtitulo("Lista de adjacência do grafo Euleriano encontrado")
    exibe_adjacencia(grafo)

    imprime_subtitulo("Matriz de adjacência do grafo Euleriano encontrado (1 = aresta)")
    exibe_matriz_adjacencia(grafo)

    imprime_subtitulo("Propriedades do grafo Euleriano encontrado")
    print(f"Conexo: {sim_nao(conexo(grafo))}")
    print(f"Todos os graus são pares: {sim_nao(todos_graus_pares(grafo))}")
    print(f"Euleriano: {sim_nao(euleriano(grafo))}")

    circuito: list[int] | None = circuito_euler(grafo)
    assert circuito is not None  # o grafo recebido já é euleriano
    imprime_subtitulo("Circuito de Euler do grafo encontrado")
    imprime_circuito_euler(circuito)

    imprime_subtitulo("Validação automática do circuito")
    print(f"Resultado: {ok_falhou(valida_circuito(grafo, circuito))}")

def imprimir_proporcao(resultado_experimento: ResultadoProporcao, quantidade_grafos_gerados: int) -> None:
    imprime_subtitulo(f"Tempos do experimento com {quantidade_grafos_gerados} grafos")
    print(f"Tempo de geração dos grafos: {resultado_experimento.tempo_geracao:.4f} s")
    print(f"Tempo total (geração + verificação): {resultado_experimento.tempo_total:.4f} s")

    imprime_subtitulo(f"Contagem de propriedades nos {quantidade_grafos_gerados} grafos gerados")
    print(f"Grafos com todos os graus pares: {resultado_experimento.graus_pares}")
    print(f"Grafos conexos (vértices de grau não nulo): {resultado_experimento.conexos}")
    print(f"Grafos vazios (rede inválida): {resultado_experimento.vazios}")

    imprime_subtitulo("Proporção de grafos Eulerianos")
    print(f"Grafos Eulerianos: {resultado_experimento.eulerianos} de {quantidade_grafos_gerados}")
    print(f"Proporção: {resultado_experimento.eulerianos / quantidade_grafos_gerados:.3f}")
