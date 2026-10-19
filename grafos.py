import random
from types import ModuleType
from typing import NamedTuple

# Lista de adjacência: vértice -> conjunto de vizinhos.
Grafo = dict[int, set[int]]

class Aresta(NamedTuple):
    """Aresta {u, v} do grafo, guardada sempre com u < v."""
    u: int
    v: int

    @classmethod
    def cria(cls, grafo: Grafo) -> list["Aresta"]:
        """
        Retorna a lista ordenada das arestas do grafo, cada uma uma única vez.

        Como o grafo é não direcionado, a aresta {u, v} aparece duas vezes na
        lista de adjacência: v está em grafo[u] e u está em grafo[v]. Para não
        contar a mesma aresta duas vezes, ela só é guardada quando u < v.
        """
        lista_arestas: list[Aresta] = []
        for u in sorted(grafo):  # vértices em ordem crescente
            for v in sorted(grafo[u]):  # vizinhos de u em ordem crescente
                if u < v:  # descarta a cópia (v, u) da mesma aresta
                    lista_arestas.append(cls(u, v))
        return lista_arestas

# Gerador aleatório: um random.Random com seed ou o próprio módulo random.
GeradorAleatorio = random.Random | ModuleType

def cria_grafo(numero_de_vertices: int) -> Grafo:
    """
    Cria um grafo com os vértices 1, 2, ..., numero_de_vertices e nenhuma aresta.

    Cada vértice começa com um conjunto de vizinhos vazio.
    """
    grafo: Grafo = {}
    for vertice in range(1, numero_de_vertices + 1):
        grafo[vertice] = set()  # ainda sem vizinhos
    return grafo

def sorteia_aresta(probabilidade_par_de_vertices_virar_aresta: float, random_com_seed: GeradorAleatorio) -> bool:
    """Decide se um par de vértices vira aresta (sorteio de Bernoulli)."""
    return random_com_seed.random() < probabilidade_par_de_vertices_virar_aresta

def gerar_grafo(numero_de_vertices: int, probabilidade_par_de_vertices_virar_aresta: float, random_com_seed: GeradorAleatorio = random) -> Grafo:
    """Gera um grafo simples não direcionado com numero_de_vertices vértices.

    Cada um dos C(numero_de_vertices, 2) pares {u, v} com u != v é sorteado
    de forma independente e vira aresta com probabilidade
    probabilidade_par_de_vertices_virar_aresta. Percorrer apenas pares u < v
    garante que não haja laços nem arestas paralelas.
    """
    grafo: Grafo = cria_grafo(numero_de_vertices)
    for u in range(1, numero_de_vertices + 1):
        for v in range(u + 1, numero_de_vertices + 1):
            if sorteia_aresta(probabilidade_par_de_vertices_virar_aresta, random_com_seed):
                grafo[u].add(v)
                grafo[v].add(u)
    return grafo

def arestas(grafo: Grafo) -> list[Aresta]:
    """Retorna a lista ordenada de arestas (u, v), com u < v."""
    return Aresta.cria(grafo)

def graus(grafo: Grafo) -> dict[int, int]:
    """Retorna um dicionário vértice -> grau (número de vizinhos)."""
    grau_por_vertice: dict[int, int] = {}
    for vertice in grafo:
        grau_por_vertice[vertice] = len(grafo[vertice])  # grau = número de vizinhos
    return grau_por_vertice

def conexo(grafo: Grafo) -> bool:
    """
    Verifica se todos os vértices de grau não nulo estão na mesma componente.

    Vértices isolados (grau 0) não têm ruas e, portanto, não influenciam a
    existência do circuito de Euler; eles são ignorados.

    A verificação é feita com uma busca em largura (BFS) a partir de um
    vértice de grau não nulo: o grafo atende ao critério se a busca alcançar
    todos os vértices de grau não nulo.
    """
    nao_isolados: set[int] = set()
    for vertice, grau in graus(grafo).items():
        if grau > 0:  # vértice com pelo menos uma rua
            nao_isolados.add(vertice)

    # Caso tratado explicitamente: sem vértices de grau não nulo (grafo sem
    # arestas), a afirmação "todos pertencem à mesma componente" é
    # verdadeira por vacuidade. A rejeição do grafo vazio como rede inválida
    # é feita em euleriano(grafo).
    if not nao_isolados:
        return True

    inicio: int = min(nao_isolados)
    visitados: set[int] = {inicio}
    fila: list[int] = [inicio]
    while fila:
        u: int = fila.pop(0)
        for w in grafo[u]:
            if w not in visitados:
                visitados.add(w)
                fila.append(w)

    return nao_isolados <= visitados

def todos_graus_pares(grafo: Grafo) -> bool:
    """Verifica se todos os vértices têm grau par."""
    for grau in graus(grafo).values():
        if grau % 2 != 0:  # achou um grau ímpar
            return False
    return True

def euleriano(grafo: Grafo) -> bool:
    """
    Decide se grafo possui circuito de Euler usando os critérios matemáticos.

    Um grafo não direcionado possui circuito de Euler se, e somente se:
      1. todos os vértices de grau não nulo pertencem à mesma componente
         conexa; e
      2. todos esses vértices possuem grau par.

    Caso tratado explicitamente: um grafo sem arestas satisfaz os dois
    critérios por vacuidade, mas não há nenhuma rua para o robô inspecionar.
    Por decisão do grupo, ele é considerado uma rede inválida e a função
    retorna False.
    """
    if not arestas(grafo):
        return False
    return conexo(grafo) and todos_graus_pares(grafo)

def circuito_euler(grafo: Grafo) -> list[int] | None:
    """
    Constrói um circuito de Euler pelo algoritmo de Hierholzer.

    Retorna a lista de vértices visitados, começando e terminando no mesmo
    vértice, ou None se grafo não possuir circuito de Euler.

    Funcionamento: mantém-se uma pilha com o caminho atual. Enquanto o
    vértice do topo ainda tiver arestas não usadas, avança-se por uma delas
    (removendo-a da cópia do grafo). Quando o topo não tem mais arestas, ele
    é desempilhado para o circuito. Como todos os graus são pares, cada
    caminho que sai de um vértice sempre consegue voltar a ele, e os
    subciclos encontrados vão sendo encaixados no circuito final. O circuito
    sai na ordem inversa e é invertido no final.
    """
    if not euleriano(grafo):
        return None

    # Cópia para não destruir o grafo original ao remover arestas usadas.
    restante: Grafo = {}
    for vertice, vizinhos in grafo.items():
        restante[vertice] = set(vizinhos)  # conjunto novo, independente do original

    # O circuito começa no menor vértice que tem pelo menos uma aresta.
    vertices_com_arestas: list[int] = []
    for vertice in grafo:
        if grafo[vertice]:
            vertices_com_arestas.append(vertice)
    inicio: int = min(vertices_com_arestas)

    pilha: list[int] = [inicio]
    circuito: list[int] = []
    while pilha:
        u: int = pilha[-1]
        if restante[u]:
            w: int = min(restante[u])  # escolha determinística do próximo vizinho
            restante[u].remove(w)
            restante[w].remove(u)
            pilha.append(w)
        else:
            circuito.append(pilha.pop())

    circuito.reverse()
    return circuito

def valida_circuito(grafo: Grafo, circuito: list[int] | None) -> bool:
    """
    Verifica automaticamente se circuito é um circuito de Euler válido de grafo.

    A verificação não depende de como circuito foi construído; ela confere
    diretamente as condições da definição:
      1. circuito começa e termina no mesmo vértice;
      2. cada par consecutivo de circuito é uma aresta de grafo;
      3. nenhuma aresta é percorrida mais de uma vez;
      4. todas as arestas de grafo são percorridas.

    Um circuito vazio ou de um único vértice não percorre nenhuma rua e é
    rejeitado, coerente com o tratamento do grafo vazio como rede inválida.
    """
    if not circuito or len(circuito) < 2:
        return False

    if circuito[0] != circuito[-1]:
        return False

    usadas: set[frozenset[int]] = set()
    for u, v in zip(circuito, circuito[1:]):
        if v not in grafo.get(u, set()):
            return False
        aresta: frozenset[int] = frozenset((u, v))
        if aresta in usadas:
            return False
        usadas.add(aresta)

    return len(usadas) == len(arestas(grafo))
