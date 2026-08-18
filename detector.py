import re

from extractor import analisar_pdf

from patterns import PADROES, PADROES_METADADOS



def _trecho(texto: str, inicio: int, fim: int, raio: int = 110) -> str:
    a = max(0, inicio - raio)
    b = min(len(texto), fim + raio)
    conteudo = re.sub(r"\s+", " ", texto[a:b]).strip()
    return f"...{conteudo}..."


def _buscar_em_paginas(paginas: list[dict]) -> list[dict]:
    evidencias = []
    vistos = set()
    for pagina in paginas:
        texto = pagina.get("texto", "")
        for regra in PADROES:
            for match in re.finditer(regra["regex"], texto, re.IGNORECASE):
                chave = (pagina["pagina"], regra["categoria"], match.group(0).lower())
                if chave in vistos:
                    continue
                vistos.add(chave)
                evidencias.append(
                    {
                        "tipo": "texto_visivel",
                        "categoria": regra["categoria"],
                        "severidade": regra["severidade"],
                        "pagina": pagina["pagina"],
                        "trecho": _trecho(texto, match.start(), match.end()),
                        "correspondencia": match.group(0),
                        "padrao": regra["regex"],
                        "peso": regra["peso"],
                    }
                )
    return evidencias


def _buscar_em_texto_invisivel(itens: list[dict]) -> list[dict]:
    evidencias = []
    for item in itens:
        texto = item.get("texto", "")
        encontrou = False
        for regra in PADROES:
            match = re.search(regra["regex"], texto, re.IGNORECASE)
            if match:
                encontrou = True
                evidencias.append(
                    {
                        "tipo": "texto_invisivel",
                        "categoria": "Hidden Instruction",
                        "subcategoria": regra["categoria"],
                        "severidade": "critica" if regra["severidade"] in {"critica", "alta"} else "alta",
                        "pagina": item.get("pagina"),
                        "trecho": re.sub(r"\s+", " ", texto).strip()[:500],
                        "correspondencia": match.group(0),
                        "padrao": regra["regex"],
                        "peso": max(42, regra["peso"]),
                        "sinal_visual": item.get("motivo"),
                    }
                )
        if not encontrou:
            evidencias.append(
                {
                    "tipo": "texto_invisivel",
                    "categoria": "Hidden Content",
                    "severidade": "baixa",
                    "pagina": item.get("pagina"),
                    "trecho": re.sub(r"\s+", " ", texto).strip()[:500],
                    "correspondencia": "conteúdo invisível",
                    "padrao": item.get("motivo"),
                    "peso": 8,
                    "sinal_visual": item.get("motivo"),
                }
            )
    return evidencias


def _buscar_em_metadados(metadados: dict) -> list[dict]:
    evidencias = []
    for campo, valor in metadados.items():
        texto = str(valor or "")
        if not texto:
            continue
        for padrao in PADROES_METADADOS:
            match = re.search(padrao, texto, re.IGNORECASE)
            if match:
                evidencias.append(
                    {
                        "tipo": "metadado",
                        "categoria": "Metadata Injection",
                        "severidade": "alta",
                        "pagina": None,
                        "trecho": texto[:500],
                        "correspondencia": match.group(0),
                        "padrao": padrao,
                        "peso": 35,
                        "campo_metadado": campo,
                    }
                )
    return evidencias


def _calcular_risco(evidencias: list[dict]) -> tuple[int, str]:
    pesos = sorted((item["peso"] for item in evidencias), reverse=True)
    if not pesos:
        return 0, "baixo"
    score = min(100, pesos[0] + sum(int(p * 0.35) for p in pesos[1:4]))
    if score >= 80:
        return score, "critico"
    if score >= 55:
        return score, "alto"
    if score >= 30:
        return score, "medio"
    return score, "baixo"


def detectar(caminho_pdf: str) -> dict:
    dados = analisar_pdf(caminho_pdf)
    evidencias = []
    evidencias.extend(_buscar_em_paginas(dados["paginas"]))
    evidencias.extend(_buscar_em_texto_invisivel(dados["texto_invisivel"]))
    evidencias.extend(_buscar_em_metadados(dados["metadados"]))
    score, nivel = _calcular_risco(evidencias)
    manipulado = score >= 30
    confianca = "alta" if score >= 55 else "media" if score >= 30 else "alta"
    categorias = sorted({item["categoria"] for item in evidencias})
    return {
        "caminho": caminho_pdf,
        "classe": 1 if manipulado else 0,
        "label": "SUSPEITO" if manipulado else "SEM INDÍCIOS RELEVANTES",
        "confianca": confianca,
        "score_risco": score,
        "nivel_risco": nivel,
        "total_paginas": dados["total_paginas"],
        "categorias": categorias,
        "evidencias": evidencias,
        "metadados": dados["metadados"],
    }


def detectar_lote(caminhos: list[str]) -> list[dict]:
    return [detectar(caminho) for caminho in caminhos]
