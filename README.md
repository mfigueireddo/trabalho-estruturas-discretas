# Projeto de Grafos – Circuito de Euler

> **Grafo vazio = rede inválida.** Um grafo sem arestas é tratado explicitamente como **rede inválida**: não há nenhuma rua para o robô inspecionar. Por isso `euleriano(grafo)` retorna `False`, `circuito_euler(grafo)` retorna `None` e `valida_circuito(grafo, circuito)` rejeita circuitos vazios.

## Dependências

- Python 3.10 ou superior
- Apenas a biblioteca padrão (`random`, `time`, `unittest`, `dataclasses`, `typing`, `types`). Não há pacotes para instalar.

## Modo debug

Os prints de acompanhamento (`[debug] ...`) são controlados pela constante `DEBUG_MODE`, no topo de `main.py`. Para ligá-los ou desligá-los, altere o valor para `True` ou `False` no código.

## Execução do programa

Os parâmetros do grupo (n = 10, p = 0.3, seed = 1376) estão em `constantes.py`.

```bash
python3 main.py
```

## Execução dos testes

```bash
python3 testes.py
```
