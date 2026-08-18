import csv
from pathlib import Path

from detector import detectar


def carregar_rotulos(base: Path) -> dict[str, int]:
    arquivo = base / "labels.csv"
    rotulos = {}
    if arquivo.exists():
        with arquivo.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                nome = row.get("arquivo") or row.get("file") or row.get("filename")
                valor = row.get("label") or row.get("classe") or row.get("target")
                if nome is not None and valor is not None:
                    rotulos[nome] = int(valor)
    return rotulos


def avaliar_dataset(caminho_dataset: str = "dataset") -> dict:
    base = Path(caminho_dataset)
    arquivos = sorted((base / "legitimos").glob("*.pdf")) + sorted((base / "manipulados").glob("*.pdf"))
    rotulos = carregar_rotulos(base)
    tp = tn = fp = fn = 0
    resultados = []
    for caminho in arquivos:
        esperado = rotulos.get(caminho.name)
        if esperado is None:
            esperado = 1 if "_injetado" in caminho.stem else 0
        resultado = detectar(str(caminho))
        previsto = resultado["classe"]
        if esperado == 1 and previsto == 1:
            tp += 1
        elif esperado == 0 and previsto == 0:
            tn += 1
        elif esperado == 0 and previsto == 1:
            fp += 1
        else:
            fn += 1
        resultados.append(
            {
                "arquivo": caminho.name,
                "esperado": esperado,
                "previsto": previsto,
                "score_risco": resultado["score_risco"],
                "nivel_risco": resultado["nivel_risco"],
            }
        )
    total = max(1, tp + tn + fp + fn)
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "total": tp + tn + fp + fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "matriz": {"tp": tp, "tn": tn, "fp": fp, "fn": fn},
        "resultados": resultados,
    }


if __name__ == "__main__":
    resultado = avaliar_dataset()
    print(f"Documentos: {resultado['total']}")
    print(f"Accuracy: {resultado['accuracy']:.2%}")
    print(f"Precision: {resultado['precision']:.2%}")
    print(f"Recall: {resultado['recall']:.2%}")
    print(f"F1-score: {resultado['f1']:.2%}")
    print(resultado["matriz"])
