<div align="center">
  <img src="./injectio-logo.png" alt="Injectio IA" width="480">

  <h3>Segurança documental antes que o conteúdo alcance a IA.</h3>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Streamlit-Interface-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/FastAPI-API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/LegalTech-6D43FF?style=flat-square" alt="LegalTech">
  </p>
</div>

O Injectio IA inspeciona documentos PDF antes do processamento por sistemas de inteligência artificial. A aplicação identifica possíveis tentativas de prompt injection, organiza evidências e apresenta uma classificação de risco auditável.

<p align="center">
  <img src="./docs/injectio-home.png" alt="Página inicial do Injectio IA" width="100%">
</p>

O que o projeto faz

Analisa texto visível, conteúdo oculto e metadados do PDF.

Detecta padrões associados a instruções maliciosas.

Calcula score e nível de risco.

Localiza evidências por página e categoria.

Gera relatório técnico em JSON.

Disponibiliza interface web e API REST.

Como funciona

1. Envio

2. Inspeção

3. Resultado

O usuário seleciona um PDF.

Conteúdo, metadados e camadas ocultas são avaliados.

O sistema apresenta score, classificação e evidências.

Interface

<table>
  <tr>
    <td width="50%" align="center">
      <img src="./docs/injectio-resultado.png" alt="Resultado da inspeção"><br>
      <sub><b>Resultado da inspeção</b></sub>
    </td>
    <td width="50%" align="center">
      <img src="./docs/injectio-funcionamento.png" alt="Funcionamento do Injectio IA"><br>
      <sub><b>Funcionamento e fluxo de análise</b></sub>
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="./docs/injectio-tecnologia.png" alt="Tecnologia e segurança" width="100%"><br>
      <sub><b>Tecnologia e medidas de segurança</b></sub>
    </td>
  </tr>
</table>

Tecnologias

Python · Streamlit · PyMuPDF · pypdf · FastAPI · Uvicorn · pytest

Executar localmente

git clone https://github.com/anaflaviabitu/injectio-ia.git
cd injectio-ia
python -m venv .venv

No Windows:

.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

API e testes

# API
uvicorn main:app --reload

# Testes
pip install -r requirements-dev.txt
pytest -q

Método

Endpoint

Finalidade

GET

/health

Verifica a disponibilidade da API

POST

/analisar-seguranca

Analisa um documento PDF

Estrutura

<details>
<summary>Ver arquivos do projeto</summary>

injectio-ia/
├── app.py
├── main.py
├── detector.py
├── extractor.py
├── patterns.py
├── avaliar_dataset.py
├── dataset/
├── tests/
├── docs/
├── injectio-logo.png
├── injectio-hero.png
├── requirements.txt
└── requirements-dev.txt

</details>

Observação

Projeto experimental baseado em regras heurísticas e um dataset sintético de validação. Os resultados apoiam a análise, mas não substituem revisão humana ou ferramentas especializadas de segurança.

Autora

Ana Flávia Bitu


GitHub: https://github.com/anaflaviabitu