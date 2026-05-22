# 🏥 MedFácil Clínicas — Sistema Inteligente de Triagem e Alocação

> **Projeto de Extensão de Sistemas Inteligentes**  
> Ciência da Computação + Sistemas de Informação · Turmas 43 + 44 + 185 · Santo Amaro  
> Professor: Felipe Santos — felipesantos@uni9.pro.br  
> Data de Entrega: **22 de Maio de 2026**

---

## 👤 Integrantes

| Nome Completo | RA |
|---|---|
| Robert França de Queiroz Sampaio | 2222201445 |

---

## 🏢 A Empresa

**Nome:** MedFácil Clínicas *(empresa fictícia)*  
**Ramo de Atuação:** Saúde — Clínicas e Unidades de Pronto Atendimento (UPA)  
**Contexto:** Rede de unidades de atendimento médico localizada em São Paulo, com foco em atendimentos de média complexidade nas especialidades de Clínica Geral, Pediatria e Ortopedia.

---

## ❗ O Problema

A MedFácil Clínicas enfrenta três problemas críticos de gestão operacional:

1. **Filas longas e imprevisíveis** — tempo médio de espera superior a 90 minutos em horários de pico, sem qualquer sistema de previsão de demanda.
2. **Alocação ineficiente de médicos** — os turnos são definidos manualmente, gerando sobrecarga em picos e ociosidade em horários de baixa demanda, elevando o custo operacional.
3. **Ausência de dados e KPIs gerenciais** — a diretoria não possui dashboards nem indicadores para embasar decisões estratégicas.

**Solução proposta:** O sistema utiliza Inteligência Artificial baseada em otimização matemática — especificamente Programação Linear Inteira — para tomar decisões de alocação de recursos de forma autônoma e eficiente, minimizando custo sem intervenção humana. O projeto integra análise de dados, modelagem computacional, segurança da informação e automação de processos em uma solução aplicada ao setor de saúde.

---

## 📁 Estrutura do Repositório

```
medfacil-projeto/
│
├── README.md                          ← Este arquivo
│
├── 01_gestao/
│   ├── project_charter.docx           ← Termo de Abertura do Projeto
│   ├── eap.xlsx                       ← Estrutura Analítica do Projeto
│   ├── gantt.xlsx                     ← Cronograma Gantt
│   └── matriz_raci.xlsx               ← Matriz de Responsabilidades
│
├── 02_analise_dados/
│   ├── 01_etl.py                      ← Pipeline ETL (limpeza e transformação)
│   ├── 02_eda.ipynb                   ← Análise Exploratória (Jupyter Notebook)
│   ├── 03_kpis_dashboard.py           ← KPIs e geração de gráficos
│   ├── data/
│   │   ├── raw/                       ← Dataset original (Kaggle)
│   │   └── processed/                 ← Dataset limpo pós-ETL
│   └── output/
│       └── charts/                    ← Gráficos exportados (.png)
│
├── 03_pesquisa_operacional/
│   ├── modelo_pli.py                  ← Modelo PLI com PuLP (IA — otimização)
│   ├── cenarios.py                    ← 3 cenários de análise e simulação
│   └── resultados_po.xlsx             ← Resultados do solver
│
├── 04_seguranca/
│   ├── mapeamento_lgpd.docx           ← Inventário de dados pessoais
│   ├── matriz_gut.xlsx                ← Matriz GUT de riscos
│   └── politica_autenticacao.docx     ← Política de controle de acesso
│
├── 05_entrega_final/
│   ├── documento_final_abnt.pdf       ← Documento consolidado (ABNT)
│   └── video_apresentacao.mp4         ← Vídeo de 10 minutos
│
└── requirements.txt                   ← Dependências Python
```

---

## 🛠️ Stack Tecnológico

### Linguagem e Ambiente

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.14.x | Linguagem principal |
| pip | 24.x | Gerenciador de pacotes |
| venv | nativo | Ambiente virtual isolado |

### Inteligência Artificial / Métodos Numéricos

| Biblioteca | Versão | Uso |
|---|---|---|
| PuLP | 3.3.x | Modelagem e resolução PLI (IA — otimização) |
| scipy | 1.17.x | Análise de sensibilidade e métodos numéricos |
| numpy | 2.4.x | Operações numéricas vetorizadas |
| CBC Solver | bundled | Solver open-source (incluso no PuLP) |

### Modelagem, Simulação e Análise de Dados

| Biblioteca | Versão | Uso |
|---|---|---|
| pandas | 3.0.x | ETL, manipulação de DataFrames |
| matplotlib | 3.10.x | Geração de gráficos |
| seaborn | 0.13.x | Visualizações estatísticas |
| jupyter | 4.x | Análise exploratória interativa |
| openpyxl | 3.1.x | Exportação para Excel |

---

## ⚙️ Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/robert-sampaio/medfacil
cd medfacil
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Windows (Git Bash):
source venv/Scripts/activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o pipeline de dados

```bash
# ETL — extração, limpeza, anonimização LGPD
python 02_analise_dados/01_etl.py

# KPIs e Dashboard
python 02_analise_dados/03_kpis_dashboard.py

# EDA interativa (abre no navegador)
jupyter notebook 02_analise_dados/02_eda.ipynb
```

### 5. Executar o Modelo de IA (PLI)

```bash
python 03_pesquisa_operacional/modelo_pli.py
```

---

## 📋 Disciplinas do Projeto

| Disciplina | Entregáveis |
|---|---|
| **Inteligência Artificial** | Modelo PLI de alocação de turnos — 3 cenários, análise de sensibilidade, economia de R$ 1.401.600/ano |
| **Métodos Numéricos Computacionais** | Pipeline ETL, operações NumPy/SciPy, KPIs calculados sobre 55.500 registros |
| **Modelagem e Simulação** | Formulação matemática do modelo, 3 cenários de simulação (Baseline, Otimizado, Pico) |
| **Automação de Processos** | Project Charter, EAP, Gantt, Matriz RACI, mapeamento LGPD, Política de Autenticação |

---

## 🗓️ Cronograma Resumido

| Fase | Período | Atividades |
|---|---|---|
| Fase 1 | 13–14/Mai | Setup, README, repositório, Project Charter |
| Fase 2 | 15–16/Mai | ETL, início da EDA, documentação de gestão |
| Fase 3 | 17–18/Mai | EDA completa, KPIs, início do modelo PLI |
| Fase 4 | 19–20/Mai | Dashboard, modelo PLI completo, Segurança/LGPD |
| Fase 5 | 21–22/Mai | Documento Final PDF (ABNT), vídeo, entrega |

---

## 🔗 Repositório

**Link:** https://github.com/robert-sampaio/medfacil

> ⚠️ Este link consta na introdução do Documento Final em PDF.

---

*Organização Acadêmica · Professor Felipe Santos · 2026*
