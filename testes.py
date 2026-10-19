import random
import unittest

from grafos import Grafo, arestas, circuito_euler, conexo, cria_grafo, euleriano, gerar_grafo, graus, todos_graus_pares, valida_circuito

def grafo_de_arestas(numero_de_vertices: int, arestas: list[tuple[int, int]]) -> Grafo:
    """Monta um grafo com vértices 1..numero_de_vertices a partir de uma lista de arestas."""
    grafo: Grafo = cria_grafo(numero_de_vertices)
    for u, v in arestas:
        grafo[u].add(v)
        grafo[v].add(u)
    return grafo

class TestesObrigatorios(unittest.TestCase):

    def test_grafo_com_euler_C4(self) -> None:
        """C4: deve encontrar um circuito válido."""
        grafo: Grafo = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
        self.assertTrue(euleriano(grafo))
        circuito: list[int] | None = circuito_euler(grafo)
        self.assertIsNotNone(circuito)
        self.assertTrue(valida_circuito(grafo, circuito))

    def test_vertices_impares_P4(self) -> None:
        """P4: os extremos têm grau 1, então não há circuito de Euler."""
        grafo: Grafo = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4)])
        self.assertTrue(conexo(grafo))
        self.assertFalse(todos_graus_pares(grafo))
        self.assertFalse(euleriano(grafo))
        self.assertIsNone(circuito_euler(grafo))

    def test_grafo_desconexo_dois_ciclos(self) -> None:
        """Dois C3 separados: graus pares, mas desconexo, então não é Euleriano."""
        grafo: Grafo = grafo_de_arestas(6, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)])
        self.assertTrue(todos_graus_pares(grafo))
        self.assertFalse(conexo(grafo))
        self.assertFalse(euleriano(grafo))
        self.assertIsNone(circuito_euler(grafo))

    def test_grafo_vazio(self) -> None:
        """Sem arestas: tratado explicitamente como rede inválida."""
        grafo: Grafo = grafo_de_arestas(10, [])
        self.assertEqual(arestas(grafo), [])
        self.assertTrue(conexo(grafo))       # verdadeiro por vacuidade
        self.assertFalse(euleriano(grafo))   # rede inválida (decisão do grupo)
        self.assertIsNone(circuito_euler(grafo))
        self.assertFalse(valida_circuito(grafo, []))

class TestesComplementares(unittest.TestCase):

    def test_gerar_grafo_simples(self) -> None:
        grafo: Grafo = gerar_grafo(10, 0.5, random.Random(0))
        for v in grafo:
            self.assertNotIn(v, grafo[v])            # sem laços
            for w in grafo[v]:
                self.assertIn(v, grafo[w])           # não direcionado
        self.assertEqual(sum(graus(grafo).values()), 2 * len(arestas(grafo)))

    def test_gerar_grafo_extremos(self) -> None:
        self.assertEqual(len(arestas(gerar_grafo(10, 0.0))), 0)
        self.assertEqual(len(arestas(gerar_grafo(10, 1.0))), 45)

    def test_gerar_grafo_reprodutivel(self) -> None:
        grafo1: Grafo = gerar_grafo(10, 0.3, random.Random(1376))
        grafo2: Grafo = gerar_grafo(10, 0.3, random.Random(1376))
        self.assertEqual(grafo1, grafo2)

    def test_circuito_com_subciclos(self) -> None:
        """Dois triângulos com vértice em comum: o Hierholzer precisa encaixar subciclos."""
        grafo: Grafo = grafo_de_arestas(5, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)])
        circuito: list[int] | None = circuito_euler(grafo)
        self.assertTrue(valida_circuito(grafo, circuito))

    def test_circuito_com_vertices_isolados(self) -> None:
        grafo: Grafo = grafo_de_arestas(10, [(2, 5), (5, 7), (7, 2)])
        self.assertTrue(euleriano(grafo))
        self.assertTrue(valida_circuito(grafo, circuito_euler(grafo)))

    def test_k5_euleriano(self) -> None:
        """K5: todos os graus são 4, então é Euleriano."""
        grafo: Grafo = gerar_grafo(5, 1.0)
        self.assertTrue(euleriano(grafo))
        self.assertTrue(valida_circuito(grafo, circuito_euler(grafo)))

    def test_valida_circuito_rejeita_invalidos(self) -> None:
        grafo: Grafo = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
        self.assertFalse(valida_circuito(grafo, [1, 2, 3, 4]))        # não fecha
        self.assertFalse(valida_circuito(grafo, [1, 3, 2, 1]))        # aresta inexistente
        self.assertFalse(valida_circuito(grafo, [1, 2, 1]))           # repete aresta
        self.assertFalse(valida_circuito(grafo, [1, 2, 3, 4, 1, 2, 1]))  # repete aresta
        self.assertFalse(valida_circuito(grafo, None))

if __name__ == "__main__":
    unittest.main(verbosity=2)
