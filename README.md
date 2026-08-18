<div align="center">
  <img src="./injectio-logo.png" alt="Injectio IA" width="520">

  <p><strong>Segurança documental antes que o conteúdo alcance a inteligência artificial.</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12">
    <img src="https://img.shields.io/badge/Streamlit-Interface-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/FastAPI-API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/status-em%20desenvolvimento-6D43FF?style=flat-square" alt="Status">
  </p>
</div>

O Injectio IA é uma aplicação desenvolvida em Python para inspecionar documentos PDF e identificar possíveis tentativas de prompt injection. O projeto analisa texto visível, conteúdo oculto e metadados, organiza as evidências encontradas e produz uma classificação de risco auditável.

O foco inicial são documentos jurídicos, unindo conhecimento de domínio em Direito, desenvolvimento de software e segurança aplicada a sistemas de IA.

O problema

Um PDF aparentemente legítimo pode conter instruções criadas para induzir um modelo de IA a ignorar regras, alterar respostas ou revelar informações. O Injectio IA atua como uma camada de inspeção anterior ao processamento pelo modelo.

Principais recursos

Upload e análise de documentos PDF em uma interface Streamlit

Detecção de padrões suspeitos em texto visível

Identificação de instruções em conteúdo invisível

Inspeção de metadados do arquivo

Score de risco de 0 a 100

Classificação em baixo, médio, alto ou crítico

Evidências com categoria, severidade, página e trecho de origem

Relatório técnico em JSON

API REST para integração

Avaliação com accuracy, precision, recall e F1-score

Testes automatizados com pytest

Tecnologias

Python

Streamlit

PyMuPDF e pypdf

FastAPI e Uvicorn

Pytest

Executando localmente

1. Crie o ambiente virtual

python -m venv .venv

No Windows:

.venv\Scripts\activate

No Linux ou macOS:

source .venv/bin/activate

2. Instale as dependências

pip install -r requirements.txt

3. Execute a interface

streamlit run app.py

API

uvicorn main:app --reload

Documentação interativa: http://127.0.0.1:8000/docs

GET  /health
POST /analisar-seguranca

Testes

pip install -r requirements-dev.txt
pytest -q

Avaliação do detector

python avaliar_dataset.py

O repositório inclui 26 PDFs sintéticos para validação funcional. As métricas desse conjunto não representam desempenho garantido em documentos reais.

Estrutura do projeto

injectio-ia/
├── .streamlit/
│   └── config.toml
├── dataset/
├── tests/
├── app.py
├── avaliar_dataset.py
├── detector.py
├── extractor.py
├── patterns.py
├── main.py
├── iniciar.bat
├── iniciar_api.bat
├── injectio-hero.png
├── injectio-logo.png
├── .gitignore
├── README.md
├── requirements.txt
└── requirements-dev.txt

Categorias observadas

Instruction Override

System Prompt Injection

Role Manipulation

Decision Manipulation

Prompt Leakage

Data Exfiltration

Restriction Bypass

Hidden Instruction

Metadata Injection

Limitações

O Injectio IA é um projeto experimental e não substitui revisão humana ou ferramentas especializadas de segurança. O detector atual utiliza padrões heurísticos e um conjunto sintético de validação; documentos reais podem exigir estratégias adicionais.

Próximas evoluções

Ampliação e diversificação do dataset

Avaliação com documentos reais anonimizados

Aprimoramento da análise de conteúdo ofuscado

Comparação entre estratégias heurísticas e modelos de linguagem

Testes de robustez e redução de falsos positivos

Autora

Desenvolvido por Ana Flávia de Morais Bitu 

GitHub: https://github.com/anaflaviabitu