import random

from constantes import N_GRAFOS_EXPERIMENTO, N_VERTICES, P, SEED
from grafos import Grafo, arestas, conexo, euleriano, gerar_grafo, todos_graus_pares
from resultados import ResultadoPrimeiroEuleriano, ResultadoProporcao
from tempo import Cronometro
from util import debug, imprime_titulo, imprimir_primeiro_euleriano, imprimir_proporcao

# Liga (True) ou desliga (False) os prints de acompanhamento [debug].
DEBUG_MODE: bool = True

def experimento_primeiro_euleriano(numero_de_vertices: int, probabilidade_par_de_vertices_virar_aresta: float, seed: int) -> ResultadoPrimeiroEuleriano:
    """
    Gera grafos aleatórios até encontrar o primeiro com circuito de Euler.

    Retorna o grafo encontrado e quantos grafos foram gerados até ele.
    """
    debug(f"Iniciando busca pelo primeiro grafo Euleriano (n={numero_de_vertices}, p={probabilidade_par_de_vertices_virar_aresta}, seed={seed})...", DEBUG_MODE, linha_em_branco_antes=True)
    random_com_seed: random.Random = random.Random(seed)
    grafos_gerados: int = 0
    while True:
        grafo: Grafo = gerar_grafo(numero_de_vertices, probabilidade_par_de_vertices_virar_aresta, random_com_seed)
        grafos_gerados += 1
        if grafos_gerados % 500 == 0:
            debug(f"{grafos_gerados} grafos gerados, nenhum Euleriano ainda...", DEBUG_MODE)
        if euleriano(grafo):
            debug(f"Grafo Euleriano encontrado após {grafos_gerados} grafos.", DEBUG_MODE)
            return ResultadoPrimeiroEuleriano(grafo, grafos_gerados)

def experimento_proporcao(numero_de_vertices: int, probabilidade_par_de_vertices_virar_aresta: float, seed: int, quantidade_grafos_gerados: int) -> ResultadoProporcao:
    """Gera `quantidade_grafos_gerados` grafos independentes e conta quantos são Eulerianos."""
    debug(f"Iniciando experimento de proporção com {quantidade_grafos_gerados} grafos...", DEBUG_MODE, linha_em_branco_antes=True)
    random_com_seed: random.Random = random.Random(seed)
    resultado: ResultadoProporcao = ResultadoProporcao()

    cronometro_total: Cronometro = Cronometro()
    cronometro_geracao: Cronometro = Cronometro()

    cronometro_total.inicia()

    for i in range(1, quantidade_grafos_gerados + 1):
        if i % 250 == 0:
            debug(f"Processando grafo {i}/{quantidade_grafos_gerados}...", DEBUG_MODE)
        cronometro_geracao.inicia()
        grafo: Grafo = gerar_grafo(numero_de_vertices, probabilidade_par_de_vertices_virar_aresta, random_com_seed)
        cronometro_geracao.para()

        if not arestas(grafo):
            resultado.vazios += 1
        if todos_graus_pares(grafo):
            resultado.graus_pares += 1
        if conexo(grafo):
            resultado.conexos += 1
        if euleriano(grafo):
            resultado.eulerianos += 1

    cronometro_total.para()

    debug("Experimento de proporção finalizado. Calculando tempos...", DEBUG_MODE)
    resultado.tempo_geracao = cronometro_geracao.tempo_acumulado()
    resultado.tempo_total = cronometro_total.tempo_acumulado()

    return resultado

def main() -> None:
    debug("Iniciando programa...", DEBUG_MODE)

    imprime_titulo("Etapa 1: primeiro grafo Euleriano")
    resultado_primeiro: ResultadoPrimeiroEuleriano = experimento_primeiro_euleriano(N_VERTICES, P, SEED)
    debug("Busca concluída. Imprimindo resultado da etapa 1...", DEBUG_MODE, linha_em_branco_antes=True)
    imprimir_primeiro_euleriano(resultado_primeiro.grafo, resultado_primeiro.grafos_gerados, N_VERTICES, P, SEED)

    imprime_titulo("Etapa 2: experimento de proporção")
    resultado_experimento: ResultadoProporcao = experimento_proporcao(N_VERTICES, P, SEED, N_GRAFOS_EXPERIMENTO)
    debug("Experimento concluído. Imprimindo resultado da etapa 2...", DEBUG_MODE, linha_em_branco_antes=True)
    imprimir_proporcao(resultado_experimento, N_GRAFOS_EXPERIMENTO)

    debug("Programa finalizado.", DEBUG_MODE, linha_em_branco_antes=True)

if __name__ == "__main__":
    main()
