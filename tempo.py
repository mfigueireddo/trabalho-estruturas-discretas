import time

class Cronometro:
    """
    Cronômetro que acumula a duração de um ou mais intervalos, em segundos.

    Usa time.perf_counter(), o relógio de maior resolução do Python para
    medir intervalos. Cada par inicia()/para() soma a duração do intervalo
    ao total acumulado.
    """

    def __init__(self) -> None:
        self.inicio: float = 0.0
        self.acumulado: float = 0.0

    def inicia(self) -> None:
        """Marca o começo de um intervalo."""
        self.inicio = time.perf_counter()

    def para(self) -> None:
        """Encerra o intervalo atual e soma sua duração ao total."""
        self.acumulado += time.perf_counter() - self.inicio

    def tempo_acumulado(self) -> float:
        """Retorna a soma das durações de todos os intervalos medidos."""
        return self.acumulado
