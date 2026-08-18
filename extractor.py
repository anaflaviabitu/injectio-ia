from pathlib import Path

import fitz
from pypdf import PdfReader


def extrair_paginas(caminho_pdf: str) -> list[dict]:
    documento = fitz.open(caminho_pdf)
    paginas = []
    for numero, pagina in enumerate(documento, start=1):
        paginas.append({"pagina": numero, "texto": pagina.get_text("text")})
    documento.close()
    return paginas


def extrair_texto(caminho_pdf: str) -> str:
    return "\n".join(item["texto"] for item in extrair_paginas(caminho_pdf))


def extrair_metadados(caminho_pdf: str) -> dict:
    reader = PdfReader(caminho_pdf)
    meta = reader.metadata or {}
    return {
        "titulo": meta.get("/Title", ""),
        "autor": meta.get("/Author", ""),
        "assunto": meta.get("/Subject", ""),
        "keywords": meta.get("/Keywords", ""),
        "criador": meta.get("/Creator", ""),
        "produtor": meta.get("/Producer", ""),
    }


def extrair_texto_invisivel(caminho_pdf: str) -> list[dict]:
    documento = fitz.open(caminho_pdf)
    suspeitos = []
    for numero_pagina, pagina in enumerate(documento, start=1):
        blocos = pagina.get_text("dict").get("blocks", [])
        for bloco in blocos:
            if bloco.get("type") != 0:
                continue
            for linha in bloco.get("lines", []):
                for span in linha.get("spans", []):
                    texto = span.get("text", "").strip()
                    tamanho = float(span.get("size", 12))
                    cor = int(span.get("color", 0))
                    if len(texto) < 4:
                        continue
                    r = (cor >> 16) & 0xFF
                    g = (cor >> 8) & 0xFF
                    b = cor & 0xFF
                    eh_claro = r > 240 and g > 240 and b > 240
                    eh_minusculo = tamanho <= 2
                    if eh_claro or eh_minusculo:
                        suspeitos.append(
                            {
                                "pagina": numero_pagina,
                                "texto": texto,
                                "tamanho_fonte": round(tamanho, 2),
                                "cor_rgb": [r, g, b],
                                "motivo": "cor_invisivel" if eh_claro else "fonte_minuscula",
                            }
                        )
    documento.close()
    return suspeitos


def analisar_pdf(caminho_pdf: str) -> dict:
    caminho = Path(caminho_pdf)
    paginas = extrair_paginas(str(caminho))
    return {
        "caminho": str(caminho),
        "nome": caminho.name,
        "paginas": paginas,
        "total_paginas": len(paginas),
        "texto": "\n".join(item["texto"] for item in paginas),
        "metadados": extrair_metadados(str(caminho)),
        "texto_invisivel": extrair_texto_invisivel(str(caminho)),
    }
