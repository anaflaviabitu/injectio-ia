from pathlib import Path

from avaliar_dataset import avaliar_dataset
from detector import detectar
from legal_extractor import extrair_estrutura

BASE = Path(__file__).resolve().parents[1]


def test_dataset_completo_sem_erros():
    resultado = avaliar_dataset(str(BASE / "dataset"))
    assert resultado["total"] == 26
    assert resultado["accuracy"] >= 0.95


def test_documento_legitimo_tem_baixo_risco():
    arquivo = BASE / "dataset" / "legitimos" / "peticao_001.pdf"
    resultado = detectar(str(arquivo))
    assert resultado["classe"] == 0
    assert resultado["score_risco"] < 30


def test_documento_injetado_e_sinalizado():
    arquivo = BASE / "dataset" / "manipulados" / "peticao_001_injetado.pdf"
    resultado = detectar(str(arquivo))
    assert resultado["classe"] == 1
    assert resultado["score_risco"] >= 30
    assert resultado["evidencias"]


def test_evidencia_informa_categoria_e_pagina_quando_aplicavel():
    arquivo = BASE / "dataset" / "manipulados" / "contestacao_001_injetado.pdf"
    resultado = detectar(str(arquivo))
    primeira = resultado["evidencias"][0]
    assert primeira["categoria"]
    assert primeira["severidade"]
    assert primeira["trecho"]


def test_extracao_juridica_retorna_estrutura():
    arquivo = BASE / "dataset" / "legitimos" / "peticao_001.pdf"
    resultado = extrair_estrutura(str(arquivo))
    assert resultado["tipo_documento"]
    assert resultado["total_paginas"] >= 1
    assert "resumo_extrativo" in resultado
