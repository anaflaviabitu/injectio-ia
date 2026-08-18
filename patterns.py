PADROES = [
    {"regex": r"ignore\s+(todas\s+as\s+)?instru[çc][õo]es\s+anteriores", "categoria": "Instruction Override", "severidade": "critica", "peso": 45},
    {"regex": r"ignore\s+previous\s+instructions", "categoria": "Instruction Override", "severidade": "critica", "peso": 45},
    {"regex": r"desconsidere\s+(o\s+)?(contexto|instru[çc][õo]es)", "categoria": "Instruction Override", "severidade": "alta", "peso": 38},
    {"regex": r"system\s*:", "categoria": "System Prompt Injection", "severidade": "alta", "peso": 35},
    {"regex": r"(revele|mostre|exiba|retorne).{0,45}(system prompt|prompt do sistema|instru[çc][õo]es internas)", "categoria": "Prompt Leakage", "severidade": "critica", "peso": 45},
    {"regex": r"act\s+as\s+if|you\s+are\s+now|aja\s+como\s+se|a\s+partir\s+de\s+agora\s+voc[eê]\s+[ée]", "categoria": "Role Manipulation", "severidade": "alta", "peso": 32},
    {"regex": r"classifique\s+este\s+(processo|pedido|caso)\s+como", "categoria": "Decision Manipulation", "severidade": "critica", "peso": 45},
    {"regex": r"mark\s+this\s+case\s+as\s+approved", "categoria": "Decision Manipulation", "severidade": "critica", "peso": 45},
    {"regex": r"conceda\s+todos\s+os\s+benef[ií]cios", "categoria": "Decision Manipulation", "severidade": "alta", "peso": 36},
    {"regex": r"o\s+sistema\s+de\s+an[áa]lise\s+deve\s+considerar", "categoria": "Decision Manipulation", "severidade": "alta", "peso": 34},
    {"regex": r"sem\s+restri[çc][õo]es|inteiramente\s+v[áa]lido|bypass|jailbreak|sem\s+limites", "categoria": "Restriction Bypass", "severidade": "media", "peso": 24},
    {"regex": r"(envie|transmita|exfiltre|copie).{0,45}(dados|segredos|credenciais|token|senha)", "categoria": "Data Exfiltration", "severidade": "critica", "peso": 48},
]

PADROES_METADADOS = [
    r"ignore",
    r"system\s*:",
    r"instru[çc][õo]es",
    r"approved",
    r"mark\s+this",
    r"classifique",
    r"jailbreak",
]
