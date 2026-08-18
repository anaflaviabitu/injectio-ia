import base64
import html
import json
import os
import tempfile
from pathlib import Path
from typing import Any

import streamlit as st

from avaliar_dataset import avaliar_dataset
from detector import detectar


BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "injectio-logo.png"
HERO_PATH = BASE_DIR / "injectio-hero.png"

st.set_page_config(
    page_title="Injectio IA | Segurança documental",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def safe(value: Any, fallback: str = "Não informado") -> str:
    return html.escape(str(value if value not in (None, "") else fallback))


LOGO_URI = data_uri(LOGO_PATH)
HERO_URI = data_uri(HERO_PATH)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root{
        --ink:#070914;--ink-2:#0c1022;--panel:#0f1428;--panel-2:#141a31;
        --line:rgba(255,255,255,.105);--white:#f8f8fb;--muted:#a2a7ba;
        --violet:#6d43ff;--violet-2:#8a67ff;--cyan:#38c5d4;
        --green:#39d39f;--amber:#ffb550;--red:#ff5e76;
    }
    html{scroll-behavior:smooth;scroll-padding-top:105px}
    body,[class*="css"]{font-family:"DM Sans",sans-serif}
    .stApp{
        color:var(--white);
        background:
            radial-gradient(circle at 78% 35%,rgba(46,80,177,.13),transparent 27rem),
            radial-gradient(circle at 42% 60%,rgba(109,67,255,.08),transparent 30rem),
            var(--ink);
    }
    [data-testid="stHeader"]{height:0;background:transparent;border:0}
    [data-testid="stToolbar"],[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none}
    .block-container{max-width:1500px;padding:5.9rem 2.7rem 4rem}
    .nav{
        position:fixed;top:.65rem;left:50%;z-index:1000001;
        width:min(1500px,calc(100vw - 5.4rem));transform:translateX(-50%);
        display:flex;align-items:center;justify-content:space-between;gap:2rem;
        min-height:58px;margin:0;padding:0 1rem;
        background:rgba(7,9,20,.82);border:1px solid rgba(255,255,255,.075);
        border-radius:13px;box-shadow:0 12px 32px rgba(0,0,0,.22);
        backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
    }
    .brand{display:flex;align-items:center;gap:.75rem;color:#fff;font-family:"Manrope",sans-serif;font-size:1.25rem;font-weight:700;letter-spacing:-.04em}
    .brand-logo{display:block;width:178px;height:auto;filter:brightness(0) invert(1)}
    .brand-mark{position:relative;display:grid;place-items:center;width:34px;height:34px;color:#fff;font-size:1.25rem;font-weight:800}
    .brand-mark:before{content:"";position:absolute;inset:2px;border-left:3px solid #fff;border-bottom:3px solid var(--violet);transform:skew(-13deg);border-radius:3px}
    .brand span{color:var(--violet-2)}
    .nav-links{display:flex;align-items:center;gap:1.75rem}
    .nav-link{color:#d5d7e1!important;font-size:.78rem;font-weight:500;text-decoration:none!important;transition:.2s ease}
    .nav-link:hover{color:#fff}
    .nav-cta{padding:.62rem .92rem;color:#fff!important;border:1px solid var(--violet-2);border-radius:10px;font-size:.74rem;font-weight:600;text-decoration:none!important;transition:.2s ease}
    .nav-cta:hover{background:rgba(109,67,255,.16);box-shadow:0 10px 25px rgba(74,38,188,.2)}
    .hero-shell,[data-testid="stHorizontalBlock"]:has(.hero-copy){
        position:relative;min-height:520px;padding:1.8rem 2.2rem 1.6rem;overflow:hidden;
        border:1px solid rgba(131,94,255,.55);border-radius:0 130px 0 0;
    }
    .hero-shell:before,[data-testid="stHorizontalBlock"]:has(.hero-copy):before{
        content:"";position:absolute;left:28%;top:-1px;width:32%;height:110%;
        border-left:1px solid rgba(115,78,255,.6);border-right:1px solid rgba(115,78,255,.6);
        transform:skew(-14deg);pointer-events:none;
    }
    .hero-shell:after,[data-testid="stHorizontalBlock"]:has(.hero-copy):after{
        content:"";position:absolute;right:-50px;top:0;width:46%;height:100%;
        border:1px solid rgba(56,197,212,.26);border-radius:44% 0 0 44%;pointer-events:none;
    }
    .hero-copy{position:relative;z-index:4;padding-top:2.4rem}
    .kicker{display:flex;align-items:center;gap:.55rem;color:#a398df;font-size:.68rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase}
    .kicker:before{content:"";width:25px;height:1px;background:var(--cyan)}
    .hero-copy h1.headline{
        max-width:620px;margin:.9rem 0 1.15rem;color:#fff!important;
        font-family:"Manrope",sans-serif!important;font-size:clamp(3rem,4.1vw,4.6rem)!important;
        font-weight:800!important;line-height:.96!important;letter-spacing:-.07em!important;
        text-transform:uppercase;word-break:normal!important;overflow-wrap:normal!important;hyphens:none!important;
    }
    .hero-copy h1.headline .headline-primary{display:block;color:#fff!important}
    .hero-copy h1.headline .headline-accent{display:block;color:var(--violet)!important;text-shadow:0 0 40px rgba(109,67,255,.18)}
    .hero-text{max-width:450px;color:#c0c4d2;font-size:.98rem;line-height:1.6}
    .hero-art{position:relative;z-index:3;display:grid;align-items:center;min-height:450px;isolation:isolate}
    .hero-art img{width:108%;max-width:none;margin-left:-9%;mix-blend-mode:lighten;filter:drop-shadow(0 28px 48px rgba(0,0,0,.3))}
    .code-note{position:absolute;z-index:2;color:rgba(80,119,203,.33);font-family:monospace;font-size:.58rem;line-height:1.7;white-space:pre}.code-note.top{left:39%;top:14%}.code-note.bottom{left:34%;bottom:8%}
    .upload-zone{position:relative;z-index:8;max-width:350px;margin-top:1.7rem}
    [data-testid="stFileUploader"]{max-width:350px}
    [data-testid="stFileUploaderDropzone"]{
        min-height:58px;padding:.25rem .35rem;background:linear-gradient(135deg,#7848ff,#5729e8);
        border:1px solid rgba(165,140,255,.42);border-radius:11px;
        box-shadow:0 16px 35px rgba(77,38,210,.28);transition:.25s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover{transform:translateY(-2px);box-shadow:0 20px 42px rgba(77,38,210,.38)}
    [data-testid="stFileUploaderDropzoneInstructions"]{display:none}
    [data-testid="stFileUploaderDropzone"] button{
        display:flex!important;align-items:center!important;justify-content:center!important;
        width:100%;height:45px;color:#fff!important;background:transparent!important;border:0!important;
        font-size:0!important;font-weight:700!important;letter-spacing:.13em!important;text-transform:uppercase!important;
    }
    [data-testid="stFileUploaderDropzone"] button>*{display:none!important}
    [data-testid="stFileUploaderDropzone"] button:after{content:"ANALISAR DOCUMENTO  →";font-size:.74rem;letter-spacing:.13em}
    [data-testid="stFileUploaderFile"]{color:#fff;background:var(--panel);border:1px solid var(--line);border-radius:10px}
    .privacy{display:flex;align-items:center;gap:.48rem;margin-top:.7rem;color:#777f99;font-size:.67rem}.privacy span{color:var(--green)}
    .section-label{margin:2.8rem 0 .9rem;color:#8e94aa;font-size:.68rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
    .metrics{display:grid;grid-template-columns:1.35fr repeat(3,1fr);gap:.75rem}
    .metric,.summary,.evidence,.legal-card,.quality,.empty-panel{
        background:linear-gradient(145deg,rgba(20,26,49,.96),rgba(12,16,34,.96));
        border:1px solid var(--line);box-shadow:0 18px 45px rgba(0,0,0,.16);
    }
    .metric{position:relative;overflow:hidden;min-height:122px;padding:1rem;border-radius:16px}
    .metric:first-child:after{content:"";position:absolute;right:-35px;bottom:-45px;width:110px;height:110px;background:radial-gradient(circle,rgba(109,67,255,.26),transparent 68%);border-radius:50%}
    .label{color:#7f879f;font-size:.64rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase}
    .metric-value{margin-top:.7rem;color:#fff;font-family:"Manrope",sans-serif;font-size:1.72rem;font-weight:700;letter-spacing:-.04em}
    .metric-hint{margin-top:.18rem;color:#777f96;font-size:.68rem}
    .overview{display:grid;grid-template-columns:1.25fr .75fr;gap:.75rem;margin-top:.75rem}
    .summary{padding:1.1rem;border-radius:16px}.summary.safe{border-left:3px solid var(--green)}.summary.medium{border-left:3px solid var(--amber)}.summary.high{border-left:3px solid var(--red)}
    .summary-title{margin:.4rem 0 .25rem;color:#fff;font-size:1rem;font-weight:700}.summary-copy{color:#969db1;font-size:.78rem;line-height:1.55}
    .track{height:7px;margin:.8rem 0 .48rem;overflow:hidden;background:#20263c;border-radius:20px}.fill{height:100%;background:linear-gradient(90deg,var(--cyan),var(--violet));border-radius:inherit}
    .stTabs [data-baseweb="tab-list"]{gap:.25rem;margin-top:1.3rem;border-bottom:1px solid var(--line)}
    .stTabs [data-baseweb="tab"]{height:46px;padding:.55rem .85rem;color:#828aa1;font-size:.76rem}
    .stTabs [aria-selected="true"]{color:#fff!important;border-bottom-color:var(--violet)!important}
    .subhead{margin:1.5rem 0 .7rem}.subhead-title{color:#fff;font-size:.9rem;font-weight:700}.subhead-copy{margin-top:.18rem;color:#788096;font-size:.7rem}
    .tags{display:flex;flex-wrap:wrap;gap:.4rem}.tag,.pill{display:inline-flex;padding:.34rem .57rem;color:#bcb2ff;background:rgba(109,67,255,.11);border:1px solid rgba(130,100,255,.2);border-radius:999px;font-size:.67rem;font-weight:600}
    .evidence{padding:1rem;margin-bottom:.65rem;border-radius:15px}.evidence-head{display:flex;flex-wrap:wrap;align-items:center;gap:.35rem;margin-bottom:.72rem}.evidence-title{margin-right:auto;color:#fff;font-size:.8rem;font-weight:700}.evidence .pill{color:#858da3;background:rgba(255,255,255,.035);border-color:var(--line)}
    .details{display:grid;grid-template-columns:repeat(3,1fr);gap:.48rem}.detail{padding:.68rem;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.055);border-radius:10px}.detail-value{margin-top:.23rem;color:#c9cdd8;font-size:.73rem;line-height:1.45;word-break:break-word}
    .snippet{margin-top:.6rem;padding:.78rem;color:#adb4c5;background:#090c19;border-left:2px solid var(--violet);border-radius:3px 9px 9px 3px;font-family:monospace;font-size:.7rem;line-height:1.55;white-space:pre-wrap;word-break:break-word}
    .legal-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.55rem}.legal-card{min-height:91px;padding:.85rem;border-radius:13px}.legal-value{margin-top:.36rem;color:#e2e4eb;font-size:.78rem;font-weight:600;line-height:1.48}
    .quality-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem}.quality{padding:.83rem;border-radius:13px}.quality-value{margin-top:.35rem;color:#fff;font-size:1.2rem;font-weight:700}
    .footnote{margin-top:.62rem;color:#666f87;font-size:.67rem;line-height:1.5}
    .anchor{display:block;position:relative;top:-105px;visibility:hidden}
    .info-section{position:relative;margin-top:5rem;padding:1.2rem 0 2rem;border-top:1px solid var(--line)}
    .info-kicker{color:var(--cyan);font-size:.65rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase}
    .info-title{max-width:760px;margin:.65rem 0 1.8rem;color:#fff;font-family:"Manrope",sans-serif;font-size:clamp(1.9rem,3.4vw,3.15rem);font-weight:700;line-height:1.06;letter-spacing:-.05em}
    [data-testid="stMarkdownContainer"] h1 a,[data-testid="stMarkdownContainer"] h2 a,[data-testid="stMarkdownContainer"] h3 a,.hero-copy a{display:none!important}
    .steps-grid,.tech-grid,.security-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}
    .step,.info-card{position:relative;overflow:hidden;min-height:180px;padding:1.15rem;background:linear-gradient(145deg,rgba(20,26,49,.9),rgba(10,14,29,.92));border:1px solid var(--line);border-radius:15px}
    .step-number{display:grid;place-items:center;width:31px;height:31px;color:#c8c0ff;background:rgba(109,67,255,.13);border:1px solid rgba(123,91,255,.22);border-radius:9px;font-size:.7rem;font-weight:700}
    .info-card-icon{color:var(--violet-2);font-family:"Manrope",sans-serif;font-size:1.35rem;font-weight:700}
    .info-card-title{margin-top:1rem;color:#fff;font-size:.88rem;font-weight:700}.info-card-copy{margin-top:.4rem;color:#858da3;font-size:.74rem;line-height:1.55}
    .about-editorial{position:relative;display:grid;grid-template-columns:1.05fr .95fr;gap:3rem;align-items:center;min-height:330px;padding:2.4rem;overflow:hidden;background:radial-gradient(circle at 18% 20%,rgba(109,67,255,.22),transparent 24rem),linear-gradient(135deg,#11152b,#0a0d1b);border:1px solid rgba(122,92,255,.25);border-radius:0 75px 0 0}
    .about-editorial:after{content:"";position:absolute;right:-65px;bottom:-105px;width:260px;height:260px;border:1px solid rgba(56,197,212,.18);border-radius:50%;box-shadow:0 0 0 45px rgba(109,67,255,.025),0 0 0 90px rgba(109,67,255,.018)}
    .about-statement{position:relative;z-index:2;color:#fff;font-family:"Manrope",sans-serif;font-size:clamp(2.5rem,4.3vw,4.4rem);font-weight:800;line-height:.94;letter-spacing:-.07em;text-transform:uppercase}.about-statement span{display:block;color:transparent;-webkit-text-stroke:1px var(--violet-2)}
    .about-content{position:relative;z-index:2}.about-lead{color:#d6d8e2;font-size:1rem;font-weight:600;line-height:1.55}.about-copy{margin-top:.7rem;color:#9299ae;font-size:.82rem;line-height:1.68}
    .about-tags{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1.2rem}.about-tag{padding:.38rem .58rem;color:#bdb4ff;background:rgba(109,67,255,.1);border:1px solid rgba(126,96,255,.2);border-radius:999px;font-size:.65rem;font-weight:600}
    .about-author{display:flex;align-items:center;gap:.65rem;margin-top:1.4rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.08)}.about-monogram{display:grid;place-items:center;width:34px;height:34px;color:#fff;background:linear-gradient(145deg,#7548ff,#4830ad);border-radius:10px;font-size:.68rem;font-weight:700}.about-name{color:#fff;font-size:.73rem;font-weight:600}.about-role{margin-top:.12rem;color:#737c94;font-size:.62rem}
    .definition-layout{display:grid;grid-template-columns:1.08fr .92fr;gap:4.5rem;align-items:end}
    .definition-lead{max-width:690px;color:#f2f2f7;font-family:"Manrope",sans-serif;font-size:clamp(1.2rem,1.7vw,1.65rem);font-weight:600;line-height:1.45;letter-spacing:-.025em}.definition-lead span{color:var(--violet-2)}
    .definition-copy{max-width:610px;margin-top:1rem;color:#8f96ab;font-size:.82rem;line-height:1.72}
    .definition-accent{position:relative;padding:0 0 .15rem 1.35rem;border-left:1px solid var(--violet-2)}.definition-accent:before{content:"";position:absolute;left:-3px;top:0;width:5px;height:32px;background:var(--cyan);border-radius:99px;box-shadow:0 0 18px rgba(56,197,212,.45)}
    .definition-accent-label{color:#9b8cff;font-size:.62rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase}.definition-accent-text{max-width:520px;margin-top:.65rem;color:#d7d9e3;font-size:.84rem;line-height:1.65}
    .threat-flow{position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:1.8rem;margin-top:3rem;padding-top:1.45rem;border-top:1px solid rgba(255,255,255,.11)}.threat-flow:before{content:"";position:absolute;left:0;top:-1px;width:25%;height:1px;background:linear-gradient(90deg,var(--cyan),var(--violet));box-shadow:0 0 14px rgba(109,67,255,.35)}
    .flow-stage{position:relative;padding-right:1rem}.flow-stage:before{content:"";position:absolute;top:-1.75rem;left:0;width:7px;height:7px;background:var(--ink);border:2px solid var(--violet-2);border-radius:50%;box-shadow:0 0 0 5px var(--ink)}
    .flow-stage-number{color:#7560e8;font-size:.58rem;font-weight:700;letter-spacing:.12em}.flow-stage-title{margin-top:.48rem;color:#fff;font-size:.77rem;font-weight:700}.flow-stage-copy{max-width:230px;margin-top:.28rem;color:#747d95;font-size:.66rem;line-height:1.5}
    .empty-panel{margin-top:1.2rem;padding:2.5rem 1rem;text-align:center;border-radius:17px}.empty-title{color:#fff;font-size:.88rem;font-weight:700}.empty-copy{max-width:450px;margin:.35rem auto 0;color:#747d93;font-size:.72rem;line-height:1.5}
    .stDownloadButton>button{min-height:42px;color:#fff;background:linear-gradient(135deg,#7447ff,#562be2);border:0;border-radius:10px;font-size:.73rem;font-weight:600}
    [data-testid="stAlert"],.stCode{border-radius:12px}
    @media(max-width:1100px){
        .block-container{padding:5.4rem 1.2rem 3rem}.nav{top:.55rem;width:calc(100vw - 2.4rem)}.nav-links{display:none}.brand-logo{width:170px}.hero-shell,[data-testid="stHorizontalBlock"]:has(.hero-copy){min-height:auto;padding:1.7rem 1.2rem;border-radius:0 80px 0 0}.hero-copy{padding-top:1.5rem}.hero-art{min-height:360px}.hero-copy h1.headline{font-size:clamp(3rem,6vw,3.9rem)!important}
        .metrics,.quality-grid{grid-template-columns:repeat(2,1fr)}.overview{grid-template-columns:1fr}.steps-grid,.tech-grid,.security-grid{grid-template-columns:repeat(2,1fr)}.threat-flow{grid-template-columns:repeat(2,1fr);row-gap:2.7rem}.definition-layout{grid-template-columns:1fr;gap:2rem}
    }
    @media(max-width:650px){
        .block-container{padding:5rem .75rem 2.5rem}.nav{top:.45rem;width:calc(100vw - 1.5rem);min-height:56px;padding:0 .75rem}.brand-logo{width:160px}.nav-cta{display:none}.hero-shell,[data-testid="stHorizontalBlock"]:has(.hero-copy){padding:1rem;border-radius:0 55px 0 0}.hero-copy{padding-top:1rem}.hero-copy h1.headline{font-size:2.55rem!important}.hero-text{font-size:.88rem}.hero-art{min-height:280px}.hero-art img{width:116%;margin-left:-8%}
        .metrics,.quality-grid,.details,.legal-grid,.steps-grid,.tech-grid,.security-grid,.about-editorial,.threat-flow{grid-template-columns:1fr}.about-editorial{gap:1.7rem;padding:1.5rem;border-radius:0 45px 0 0}.threat-flow{gap:2.5rem;border-top:0;border-left:1px solid rgba(255,255,255,.11);padding:0 0 0 1.25rem}.threat-flow:before{width:1px;height:25%;top:0;background:linear-gradient(var(--cyan),var(--violet))}.flow-stage:before{top:.28rem;left:-1.58rem}.info-section{margin-top:3.5rem}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def risk_status(level: str) -> tuple[str, str, str]:
    statuses = {
        "baixo": ("safe", "Documento sem alertas relevantes", "Nenhum indício significativo de manipulação foi localizado."),
        "medio": ("medium", "Revisão recomendada", "Alguns sinais merecem validação antes do uso em sistemas de IA."),
        "alto": ("high", "Risco elevado detectado", "Há evidências consistentes de interferência no processamento automático."),
        "critico": ("high", "Documento potencialmente hostil", "Múltiplos indícios críticos foram encontrados. Evite processar o arquivo sem revisão."),
    }
    return statuses.get(str(level).lower(), statuses["baixo"])


def section(title: str, description: str) -> None:
    st.markdown(
        f'<div class="subhead"><div class="subhead-title">{safe(title)}</div>'
        f'<div class="subhead-copy">{safe(description)}</div></div>',
        unsafe_allow_html=True,
    )


def tag_list(values: list[Any], fallback: str) -> str:
    items = values or [fallback]
    return '<div class="tags">' + "".join(f'<span class="tag">{safe(item)}</span>' for item in items) + "</div>"


def detail(label: str, value: Any) -> str:
    return f'<div class="detail"><div class="label">{safe(label)}</div><div class="detail-value">{safe(value)}</div></div>'


def render_nav() -> None:
    brand = f'<img class="brand-logo" src="{LOGO_URI}" alt="Injectio IA">' if LOGO_URI else '<div class="brand"><span class="brand-mark">i</span>Injectio <span>IA</span></div>'
    st.markdown(
        f'<nav class="nav">{brand}'
        '<div class="nav-links"><a class="nav-link" href="#prompt-injection" target="_self">O que é</a>'
        '<a class="nav-link" href="#como-funciona" target="_self">Como funciona</a>'
        '<a class="nav-link" href="#tecnologia" target="_self">Tecnologia</a>'
        '<a class="nav-link" href="#seguranca" target="_self">Segurança</a>'
        '<a class="nav-link" href="#sobre" target="_self">Sobre</a>'
        '<a class="nav-cta" href="#analise" target="_self">Iniciar análise&nbsp;&nbsp;→</a></div></nav>',
        unsafe_allow_html=True,
    )


def render_hero() -> Any:
    left, right = st.columns([.95, 1.05], gap="small")
    with left:
        st.markdown(
            '<span id="analise" class="anchor"></span><div class="hero-copy"><div class="kicker">Segurança documental inteligente</div>'
            '<h1 class="headline"><span class="headline-primary">Documentos seguros.</span><span class="headline-accent">IA protegida.</span></h1>'
            '<div class="hero-text">Identifique instruções ocultas antes que elas alcancem seus sistemas de inteligência artificial.</div>'
            '<div class="upload-zone">',
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "ANALISAR DOCUMENTO",
            type=["pdf"],
            help="Selecione um documento PDF para iniciar a análise.",
            label_visibility="collapsed",
        )
        st.markdown(
            '<div class="privacy"><span>✓</span>Processamento privado · PDF de até 200 MB</div></div></div>',
            unsafe_allow_html=True,
        )
    with right:
        if HERO_URI:
            st.markdown(
                f'<div class="hero-art"><div class="code-note top">&gt; analysis.run\n&gt; scanning.layers\n&gt; detect.hidden.instructions</div>'
                f'<img src="{HERO_URI}" alt="Documento jurídico sendo analisado">'
                '<div class="code-note bottom">&gt; possible.risk.detected\n&gt; target: ai_model\n&gt; severity: analyzing</div></div>',
                unsafe_allow_html=True,
            )
    return uploaded


def analyze(uploaded: Any) -> dict[str, Any]:
    path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temporary:
            temporary.write(uploaded.getvalue())
            path = temporary.name
        with st.spinner("Inspecionando conteúdo, metadados e estrutura..."):
            return detectar(path)
    finally:
        if path and os.path.exists(path):
            os.unlink(path)


def render_overview(security: dict[str, Any]) -> None:
    score = max(0, min(int(security.get("score_risco", 0)), 100))
    level = str(security.get("nivel_risco", "baixo"))
    evidences = security.get("evidencias", [])
    metrics = [
        ("Score de risco", f"{score}/100", "Pontuação consolidada"),
        ("Classificação", level.upper(), "Nível atual"),
        ("Evidências", len(evidences), "Ocorrências localizadas"),
        ("Páginas", security.get("total_paginas", 0), "Conteúdo processado"),
    ]
    markup = '<div class="section-label">Resultado da inspeção</div><div class="metrics">'
    for label, value, hint in metrics:
        markup += (
            f'<div class="metric"><div class="label">{safe(label)}</div>'
            f'<div class="metric-value">{safe(value)}</div><div class="metric-hint">{safe(hint)}</div></div>'
        )
    st.markdown(markup + "</div>", unsafe_allow_html=True)
    css_class, title, description = risk_status(level)
    confidence = str(security.get("confianca", "não informada")).upper()
    st.markdown(
        '<div class="overview">'
        f'<div class="summary {css_class}"><div class="label">Parecer automático</div>'
        f'<div class="summary-title">{safe(title)}</div><div class="summary-copy">{safe(description)}</div>'
        f'<div class="summary-copy" style="margin-top:.38rem">Confiança: <strong>{safe(confidence)}</strong></div></div>'
        '<div class="summary"><div class="label">Intensidade</div>'
        f'<div class="summary-title">{score}%</div><div class="track"><div class="fill" style="width:{score}%"></div></div>'
        '<div class="summary-copy">Severidade e recorrência dos sinais detectados.</div></div></div>',
        unsafe_allow_html=True,
    )


def render_security(security: dict[str, Any]) -> None:
    section("Sinais identificados", "Categorias associadas ao diagnóstico.")
    st.markdown(tag_list(security.get("categorias", []), "Nenhuma categoria relevante"), unsafe_allow_html=True)
    section("Evidências", "Ocorrências que contribuíram para o score.")
    evidences = security.get("evidencias", [])
    if not evidences:
        st.markdown('<div class="empty-panel"><div class="empty-title">Nenhum sinal relevante</div><div class="empty-copy">O documento foi processado sem evidências técnicas significativas.</div></div>', unsafe_allow_html=True)
        return
    for index, evidence in enumerate(evidences, 1):
        page = f"Página {evidence['pagina']}" if evidence.get("pagina") else "Metadado"
        extra = evidence.get("subcategoria") or evidence.get("campo_metadado") or evidence.get("sinal_visual") or "Não informado"
        st.markdown(
            '<article class="evidence"><div class="evidence-head">'
            f'<div class="evidence-title">Evidência {index}</div>'
            f'<span class="pill">{safe(evidence.get("categoria", "Sem categoria"))}</span>'
            f'<span class="pill">{safe(str(evidence.get("severidade", "indefinida")).upper())}</span>'
            f'<span class="pill">{safe(page)}</span></div><div class="details">'
            f'{detail("Tipo", evidence.get("tipo"))}{detail("Correspondência", evidence.get("correspondencia"))}'
            f'{detail("Detalhe", extra)}</div><div class="snippet">{safe(evidence.get("trecho", "Trecho não disponível"))}</div></article>',
            unsafe_allow_html=True,
        )


def render_quality() -> None:
    section("Desempenho do detector", "Métricas do conjunto interno de validação.")
    try:
        metrics = avaliar_dataset("dataset")
        values = [("Acurácia", metrics["accuracy"]), ("Precisão", metrics["precision"]), ("Recall", metrics["recall"]), ("F1-score", metrics["f1"])]
        st.markdown(
            '<div class="quality-grid">'
            + "".join(f'<div class="quality"><div class="label">{safe(label)}</div><div class="quality-value">{value:.0%}</div></div>' for label, value in values)
            + "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="footnote">Validação interna com {safe(metrics.get("total", 0))} PDFs sintéticos. Os resultados não representam desempenho garantido em documentos reais.</div>',
            unsafe_allow_html=True,
        )
    except (FileNotFoundError, KeyError, TypeError, ValueError):
        st.markdown('<div class="footnote">As métricas aparecerão quando o conjunto de avaliação estiver disponível.</div>', unsafe_allow_html=True)


def render_info_sections() -> None:
    st.markdown(
        '<span id="prompt-injection" class="anchor"></span><section class="info-section">'
        '<div class="info-kicker">Entenda a ameaça</div><div class="info-title">O que é Prompt Injection?</div>'
        '<div class="definition-layout"><div><div class="definition-lead">Uma instrução escondida em um documento pode fazer a IA <span>ignorar regras, alterar respostas ou expor informações.</span></div>'
        '<div class="definition-copy">Esse ataque é chamado de prompt injection. Ele transforma um arquivo aparentemente comum em um canal para comandos que a IA pode interpretar como legítimos.</div></div>'
        '<div class="definition-accent"><div class="definition-accent-label">A barreira do Injectio IA</div><div class="definition-accent-text">Antes do envio ao modelo, o PDF é examinado em suas camadas de conteúdo, metadados e estrutura. Sinais suspeitos são destacados com evidências verificáveis.</div></div></div>'
        '<div class="threat-flow">'
        '<div class="flow-stage"><div class="flow-stage-number">01</div><div class="flow-stage-title">Arquivo confiável</div><div class="flow-stage-copy">O documento parece seguro para uso.</div></div>'
        '<div class="flow-stage"><div class="flow-stage-number">02</div><div class="flow-stage-title">Comando oculto</div><div class="flow-stage-copy">Uma instrução maliciosa passa despercebida.</div></div>'
        '<div class="flow-stage"><div class="flow-stage-number">03</div><div class="flow-stage-title">Interpretação pela IA</div><div class="flow-stage-copy">O modelo pode tratar o comando como legítimo.</div></div>'
        '<div class="flow-stage"><div class="flow-stage-number">04</div><div class="flow-stage-title">Resposta comprometida</div><div class="flow-stage-copy">A análise é alterada ou informações são expostas.</div></div>'
        '</div></section>'
        '<span id="como-funciona" class="anchor"></span><section class="info-section">'
        '<div class="info-kicker">Como funciona</div><div class="info-title">Da entrada do PDF ao parecer de segurança.</div>'
        '<div class="steps-grid">'
        '<div class="step"><div class="step-number">01</div><div class="info-card-title">Envio do documento</div><div class="info-card-copy">O PDF é recebido em ambiente isolado e preparado para inspeção.</div></div>'
        '<div class="step"><div class="step-number">02</div><div class="info-card-title">Análise multicamada</div><div class="info-card-copy">Conteúdo, metadados e estrutura são avaliados em busca de padrões suspeitos.</div></div>'
        '<div class="step"><div class="step-number">03</div><div class="info-card-title">Resultado auditável</div><div class="info-card-copy">Você recebe score, classificação, evidências rastreáveis e relatório técnico.</div></div>'
        '</div></section>'
        '<span id="tecnologia" class="anchor"></span><section class="info-section">'
        '<div class="info-kicker">Tecnologia</div><div class="info-title">Engenharia aplicada à leitura segura de documentos.</div>'
        '<div class="tech-grid">'
        '<div class="info-card"><div class="info-card-icon">{ }</div><div class="info-card-title">Detecção por padrões</div><div class="info-card-copy">Regras especializadas reconhecem comandos, tentativas de desvio e sequências incomuns.</div></div>'
        '<div class="info-card"><div class="info-card-icon">PDF</div><div class="info-card-title">Análise estrutural</div><div class="info-card-copy">Inspeção de texto, propriedades, objetos e camadas presentes no arquivo.</div></div>'
        '<div class="info-card"><div class="info-card-icon">◫</div><div class="info-card-title">Camadas ocultas</div><div class="info-card-copy">Inspeção de elementos invisíveis e conteúdos que podem passar despercebidos na leitura convencional.</div></div>'
        '</div></section>'
        '<span id="seguranca" class="anchor"></span><section class="info-section">'
        '<div class="info-kicker">Segurança</div><div class="info-title">Proteção antes que o documento alcance a IA.</div>'
        '<div class="security-grid">'
        '<div class="info-card"><div class="info-card-icon">01</div><div class="info-card-title">Processamento temporário</div><div class="info-card-copy">O arquivo é removido da área temporária assim que a análise é concluída.</div></div>'
        '<div class="info-card"><div class="info-card-icon">02</div><div class="info-card-title">Evidências rastreáveis</div><div class="info-card-copy">Cada alerta preserva categoria, severidade, página e trecho de origem.</div></div>'
        '<div class="info-card"><div class="info-card-icon">03</div><div class="info-card-title">Revisão humana</div><div class="info-card-copy">O parecer apoia a decisão profissional sem substituir a validação do usuário.</div></div>'
        '</div></section>'
        '<span id="sobre" class="anchor"></span><section class="info-section">'
        '<div class="info-kicker">Sobre o projeto</div><div class="about-editorial">'
        '<div class="about-statement">Direito encontra<span>tecnologia.</span></div>'
        '<div class="about-content"><div class="about-lead">Uma camada de segurança entre documentos jurídicos e inteligência artificial.</div>'
        '<div class="about-copy">O Injectio IA nasceu da união entre conhecimento jurídico e desenvolvimento de software. O projeto identifica instruções ocultas em PDFs e organiza evidências técnicas para apoiar uma adoção de IA mais segura e verificável.</div>'
        '<div class="about-tags"><span class="about-tag">Python</span><span class="about-tag">Streamlit</span><span class="about-tag">PyMuPDF</span><span class="about-tag">LegalTech</span><span class="about-tag">Cibersegurança</span></div>'
        '<div class="about-author"><div class="about-monogram">◈</div><div><div class="about-name">Desenvolvido por</div><div class="about-role">Ana Flávia Bitu</div></div></div></div></div>'
        '</section>',
        unsafe_allow_html=True,
    )


def main() -> None:
    render_nav()
    uploaded = render_hero()
    if uploaded is None:
        render_info_sections()
        return
    try:
        security = analyze(uploaded)
    except Exception as error:
        st.error("Não foi possível concluir a análise. Verifique se o PDF é válido e tente novamente.")
        with st.expander("Detalhes técnicos"):
            st.code(str(error))
        return
    render_overview(security)
    report = {"arquivo": uploaded.name, "seguranca": security}
    security_tab, technical_tab = st.tabs(["Diagnóstico", "Relatório técnico"])
    with security_tab:
        render_security(security)
    with technical_tab:
        section("Saída técnica", "Dados completos para auditoria e integração.")
        st.code(json.dumps(report, ensure_ascii=False, indent=2), language="json")
        st.download_button(
            "Baixar relatório JSON",
            data=json.dumps(report, ensure_ascii=False, indent=2),
            file_name=f"{Path(uploaded.name).stem}_injectio.json",
            mime="application/json",
        )
    render_quality()
    render_info_sections()


if __name__ == "__main__":
    main()