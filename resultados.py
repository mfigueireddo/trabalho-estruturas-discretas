from dataclasses import dataclass

from grafos import Grafo

@dataclass
class ResultadoPrimeiroEuleriano:
    grafo: Grafo
    grafos_gerados: int  # inclui o próprio grafo encontrado

@dataclass
class ResultadoProporcao:
    eulerianos: int = 0
    graus_pares: int = 0
    conexos: int = 0
    vazios: int = 0
    tempo_geracao: float = 0.0
    tempo_total: float = 0.0
