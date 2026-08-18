import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from detector import detectar


app = FastAPI(
    title="Injectio IA API",
    description=(
        "API para inspeção de documentos PDF e identificação "
        "de possíveis ataques de prompt injection."
    ),
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _salvar_pdf(arquivo: UploadFile) -> str:
    if not arquivo.filename or not arquivo.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Envie um arquivo PDF.",
        )

    conteudo = await arquivo.read()

    if not conteudo:
        raise HTTPException(
            status_code=400,
            detail="O arquivo está vazio.",
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temporario:
        temporario.write(conteudo)
        return temporario.name


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "versao": "2.1.0",
    }


@app.post("/analisar-seguranca")
async def analisar_seguranca(
    arquivo: UploadFile = File(...),
) -> dict:
    caminho = await _salvar_pdf(arquivo)

    try:
        resultado = detectar(caminho)
        resultado["arquivo"] = arquivo.filename
        resultado.pop("caminho", None)
        return resultado
    finally:
        if os.path.exists(caminho):
            os.unlink(caminho)