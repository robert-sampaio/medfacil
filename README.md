# 🏥 MedFácil Clínicas — Sistema Inteligente de Triagem e Alocação

> \*\*Projeto de Extensão de Sistemas Inteligentes\*\*  
> Ciência da Computação + Sistemas de Informação · Turmas 43 + 44 + 185 · Santo Amaro  
> Professor: Felipe Santos — felipesantos@uni9.pro.br  
> Data de Entrega: \*\*22 de Maio de 2026\*\*

\---

## 👤 Integrantes

|Nome Completo|RA|
|-|-|
|Robert França de Queiroz Sampaio|2222201445|

> \*Projeto individual — não é necessária descrição de contribuições por integrante.\*

\---

## 🏢 A Empresa

**Nome:** MedFácil Clínicas *(empresa fictícia)*  
**Ramo de Atuação:** Saúde — Clínicas e Unidades de Pronto Atendimento (UPA)  
**Contexto:** Rede de unidades de atendimento médico localizada em São Paulo, com foco em atendimentos de média complexidade nas especialidades de Clínica Geral, Pediatria e Ortopedia.

\---

## ❗ O Problema

A MedFácil Clínicas enfrenta três problemas críticos de gestão operacional:

1. **Filas longas e imprevisíveis** — tempo médio de espera superior a 90 minutos em horários de pico, sem qualquer sistema de previsão de demanda.
2. **Alocação ineficiente de médicos** — os turnos são definidos manualmente, gerando sobrecarga em picos e ociosidade em horários de baixa demanda, elevando o custo operacional.
3. **Ausência de dados e KPIs gerenciais** — a diretoria não possui dashboards nem indicadores para embasar decisões estratégicas.

**Solução proposta:** Desenvolver um sistema baseado em IA e análise de dados que analise padrões históricos de atendimento, otimize a alocação de médicos via Pesquisa Operacional (PLI), garanta conformidade com a LGPD e documente todo o processo com metodologias de Gestão de Projetos.

\---

## 📁 Estrutura do Repositório

```
medfacil-projeto/
│
├── README.md                          ← Este arquivo
│
├── 01\_gestao/
│   ├── project\_charter.docx           ← Termo de Abertura do Projeto
│   ├── eap.xlsx                       ← Estrutura Analítica do Projeto
│   ├── gantt.xlsx                     ← Cronograma Gantt
│   └── matriz\_raci.xlsx               ← Matriz de Responsabilidades
│
├── 02\_analise\_dados/
│   ├── 01\_etl.py                      ← Pipeline ETL (limpeza e transformação)
│   ├── 02\_eda.ipynb                   ← Análise Exploratória (Jupyter Notebook)
│   ├── 03\_kpis\_dashboard.py           ← KPIs e geração de gráficos
│   ├── data/
│   │   ├── raw/                       ← Dataset original (Kaggle)
│   │   └── processed/                 ← Dataset limpo pós-ETL
│   └── output/
│       └── charts/                    ← Gráficos exportados (.png)
│
├── 03\_pesquisa\_operacional/
│   ├── modelo\_pli.py                  ← Modelo PLI com PuLP
│   ├── cenarios.py                    ← 3 cenários de análise
│   └── resultados\_po.xlsx             ← Resultados do solver
│
├── 04\_seguranca/
│   ├── mapeamento\_lgpd.docx           ← Inventário de dados pessoais
│   ├── matriz\_gut.xlsx                ← Matriz GUT de riscos
│   └── politica\_autenticacao.docx     ← Política de controle de acesso
│
├── 05\_entrega\_final/
│   ├── documento\_final\_abnt.pdf       ← Documento consolidado (ABNT)
│   └── video\_apresentacao.mp4         ← Vídeo de 10 minutos
│
└── requirements.txt                   ← Dependências Python
```

\---

## 🛠️ Stack Tecnológico

### Linguagem e Ambiente

|Tecnologia|Versão|Uso|
|-|-|-|
|Python|3.12.x|Linguagem principal|
|pip|24.x|Gerenciador de pacotes|
|venv|nativo|Ambiente virtual isolado|

### Análise de Dados

|Biblioteca|Versão|Uso|
|-|-|-|
|pandas|2.2.x|ETL, manipulação de DataFrames|
|numpy|1.26.x|Operações numéricas|
|matplotlib|3.9.x|Geração de gráficos|
|seaborn|0.13.x|Visualizações estatísticas|
|jupyter|4.x|Análise exploratória interativa|
|openpyxl|3.1.x|Exportação para Excel|

### Pesquisa Operacional

|Biblioteca|Versão|Uso|
|-|-|-|
|PuLP|2.8.x|Modelagem e resolução PLI|
|scipy|1.13.x|Análise de sensibilidade|
|CBC Solver|bundled|Solver open-source (incluso no PuLP)|

\---

## ⚙️ Como Executar

### 1\. Clonar / abrir o repositório

```bash
# Se estiver usando GitHub:
git clone <URL\_DO\_REPOSITORIO>
cd medfacil-projeto
```

### 2\. Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Windows:
venv\\Scripts\\activate

# macOS/Linux:
source venv/bin/activate
```

### 3\. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4\. Executar o pipeline de Análise de Dados

```bash
# ETL (limpeza e transformação)
python 02\_analise\_dados/01\_etl.py

# KPIs e Dashboard
python 02\_analise\_dados/03\_kpis\_dashboard.py

# EDA interativa (abre no navegador)
jupyter notebook 02\_analise\_dados/02\_eda.ipynb
```

### 5\. Executar o Modelo de Otimização (P.O.)

```bash
python 03\_pesquisa\_operacional/modelo\_pli.py
python 03\_pesquisa\_operacional/cenarios.py
```

\---

## 📦 requirements.txt (conteúdo)

```
pandas==2.2.3
numpy==1.26.4
matplotlib==3.9.2
seaborn==0.13.2
jupyter==4.2.0
openpyxl==3.1.5
PuLP==2.8.0
scipy==1.13.1
```

\---

## 📋 Disciplinas do Projeto

|Disciplina|Entregáveis|
|-|-|
|**Análise de Dados** (Python/ETL)|ETL completo, EDA com Jupyter, 3 KPIs, dashboard com 5+ gráficos|
|**Pesquisa Operacional**|Modelo PLI de alocação de turnos, 3 cenários, análise de sensibilidade|
|**Segurança da Informação**|Mapeamento LGPD, Matriz GUT, Política de Autenticação|
|**Gestão de Projetos**|Project Charter, EAP, Gantt, Matriz RACI, Plano de Comunicação e Custos|

\---

## 🗓️ Cronograma Resumido

|Fase|Período|Atividades|
|-|-|-|
|Fase 1|13–14/Mai|Setup, README, repositório, Project Charter|
|Fase 2|15–16/Mai|ETL, início da EDA, Gestão de Projetos|
|Fase 3|17–18/Mai|EDA completa, KPIs, início do modelo PLI|
|Fase 4|19–20/Mai|Dashboard, modelo PLI completo, Segurança/LGPD|
|Fase 5|21–22/Mai|Documento Final PDF (ABNT), vídeo, entrega|

\---

## 📬 Contato do Professor

**Felipe Santos**  
felipesantos@uni9.pro.br  
*Tempo médio de resposta: 24h a 48h úteis*

\---

## 🔗 Link do Repositório Compartilhado

> \*(Preencher após criar a pasta no Google Drive / OneDrive e compartilhar com o professor com permissão de Leitura/Visualização)\*

**Link:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

> ⚠️ Este link deve constar obrigatoriamente na \*\*introdução do Documento Final em PDF\*\*.

\---

*Organização Acadêmica · Professor Felipe Santos · 2026*

