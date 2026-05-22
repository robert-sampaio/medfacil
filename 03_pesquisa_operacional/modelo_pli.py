"""
=============================================================================
MedFácil Clínicas — Projeto de Extensão de Sistemas Inteligentes
=============================================================================
Script  : modelo_pli.py
Etapa   : Pesquisa Operacional — Programação Linear Inteira (PLI)
Autor   : Robert França de Queiroz Sampaio
Data    : Maio/2026
=============================================================================
DESCRIÇÃO:
  Modelo de alocação de médicos por turno na MedFácil Clínicas.

  NÍVEL DE ANÁLISE: Clínica inteira por turno (Manhã / Tarde / Noite).

  PROBLEMA:
    Determinar quantos médicos alocar em cada turno para cobrir a demanda
    diária de atendimentos, minimizando o custo total de pessoal.

  VARIÁVEL DE DECISÃO:
    x[t] = número de médicos alocados no turno t  (inteiro >= 0)

  FUNÇÃO OBJETIVO:
    Minimizar: soma_t ( custo_hora[t] x horas_turno[t] x x[t] )

  RESTRIÇÕES:
    R1: x[t] x produtividade x horas[t] >= demanda_diaria[t]  (cobertura)
    R2: x[t] >= min_medicos[t]  (mínimo operacional de segurança)
    R3: x[t] <= max_medicos     (limite de contratação)
    R4: x[t] inteiro nao-negativo

  CENÁRIOS:
    C1 — Baseline  : alocação manual atual (20% acima do mínimo = ineficiência)
    C2 — Otimizado : PLI minimiza custo para demanda média diária
    C3 — Pico      : PLI resolve para o dia mais movimentado do histórico
=============================================================================
"""

import pandas as pd
import numpy as np
import pulp
import os

# ---------------------------------------------------------------------------
# 0. CONFIGURAÇÃO
# ---------------------------------------------------------------------------
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "..", "02_analise_dados",
                          "data", "processed", "healthcare_clean.csv")
OUTPUT_DIR = BASE_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 65)
print("  MedFácil Clínicas — Modelo PLI de Alocação de Turnos")
print("=" * 65)

# ---------------------------------------------------------------------------
# 1. LEITURA E PARÂMETROS
# ---------------------------------------------------------------------------
print("\n[1/5] Carregando dados e definindo parâmetros...")

df = pd.read_csv(INPUT_PATH)
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])

TURNOS = ["Manha", "Tarde", "Noite"]
TURNOS_LABEL = {"Manha": "Manhã", "Tarde": "Tarde", "Noite": "Noite"}

# Parâmetros operacionais
HORAS_TURNO   = {"Manha": 8,     "Tarde": 8,     "Noite": 8}
CUSTO_HORA    = {"Manha": 150.0, "Tarde": 150.0, "Noite": 180.0}
PRODUTIVIDADE = 4   # atendimentos/hora por médico
MIN_MEDICOS   = {"Manha": 2, "Tarde": 2, "Noite": 1}
MAX_MEDICOS   = 30

# Mapeia coluna Shift para chaves sem acento
df["Shift_key"] = df["Shift"].map({"Manhã": "Manha", "Tarde": "Tarde", "Noite": "Noite"})

# ---------------------------------------------------------------------------
# 2. CÁLCULO DE DEMANDA
# ---------------------------------------------------------------------------
n_dias = max((df["Date of Admission"].max() -
              df["Date of Admission"].min()).days, 1)

atend_turno_total = df["Shift_key"].value_counts().reindex(TURNOS, fill_value=0)
demanda_media     = (atend_turno_total / n_dias)

# Demanda do dia de pico
atend_dia = (
    df.groupby([df["Date of Admission"].dt.date, "Shift_key"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=TURNOS, fill_value=0)
)
demanda_pico = atend_dia.max().astype(float)

# Mínimos para cobertura
med_min_media = {
    t: max(MIN_MEDICOS[t],
           int(np.ceil(demanda_media[t] / (PRODUTIVIDADE * HORAS_TURNO[t]))))
    for t in TURNOS
}

print(f"\n      Período analisado : {n_dias} dias")
print(f"      Total atendimentos: {len(df):,}")
print(f"\n      Demanda MÉDIA diária por turno:")
for t in TURNOS:
    print(f"        {TURNOS_LABEL[t]:<6}: {demanda_media[t]:>6.1f} atend./dia  "
          f"| min. médicos necessários: {med_min_media[t]}")
print(f"\n      Demanda de PICO (dia mais movimentado):")
for t in TURNOS:
    print(f"        {TURNOS_LABEL[t]:<6}: {demanda_pico[t]:>6.0f} atend.")

# ---------------------------------------------------------------------------
# 3. SOLVER PLI
# ---------------------------------------------------------------------------
def resolver_modelo(nome, demanda_ref, verbose=True):
    prob = pulp.LpProblem(f"MedFacil_{nome}", pulp.LpMinimize)

    x = {
        t: pulp.LpVariable(f"x_{t}", lowBound=0, cat="Integer")
        for t in TURNOS
    }

    # Objetivo
    prob += pulp.lpSum(
        CUSTO_HORA[t] * HORAS_TURNO[t] * x[t] for t in TURNOS
    ), "Custo_Total"

    # Restrições
    for t in TURNOS:
        prob += x[t] * PRODUTIVIDADE * HORAS_TURNO[t] >= demanda_ref[t], f"Cob_{t}"
        prob += x[t] >= MIN_MEDICOS[t], f"Min_{t}"
        prob += x[t] <= MAX_MEDICOS,    f"Max_{t}"

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    status = pulp.LpStatus[prob.status]
    custo  = pulp.value(prob.objective)
    aloc   = {t: int(pulp.value(x[t]) or 0) for t in TURNOS}
    cap    = {t: aloc[t] * PRODUTIVIDADE * HORAS_TURNO[t] for t in TURNOS}

    if verbose:
        print(f"     Status       : {status}")
        print(f"     Custo diário : R$ {custo:,.2f}" if custo else "     Custo: N/A")
        for t in TURNOS:
            print(f"       {TURNOS_LABEL[t]:<6}: {aloc[t]:>2} médico(s) | "
                  f"Cap: {cap[t]:>3} atend. | "
                  f"Dem: {demanda_ref[t]:>5.1f} | "
                  f"Ocioso: {max(0, cap[t]-demanda_ref[t]):>5.1f}")

    rows = []
    for t in TURNOS:
        rows.append({
            "Turno"               : TURNOS_LABEL[t],
            "Médicos Alocados"    : aloc[t],
            "Custo Turno (R$/dia)": round(aloc[t] * CUSTO_HORA[t] * HORAS_TURNO[t], 2),
            "Demanda (atend.)"    : round(float(demanda_ref[t]), 1),
            "Capacidade (atend.)" : cap[t],
            "Ociosidade (atend.)" : round(max(0, cap[t] - float(demanda_ref[t])), 1),
        })

    return {"nome": nome, "status": status, "custo": custo, "df": pd.DataFrame(rows)}

# ---------------------------------------------------------------------------
# 4. EXECUÇÃO DOS 3 CENÁRIOS
# ---------------------------------------------------------------------------
print("\n[2/5] Executando os 3 cenários...")

# C1 — Baseline: alocação manual (20% a mais = ineficiência real)
print("\n  -> Cenário 1: Baseline (alocação manual, 20% acima do mínimo)...")
c1_rows = []
for t in TURNOS:
    med = max(MIN_MEDICOS[t], int(np.ceil(med_min_media[t] * 1.20)))
    cap = med * PRODUTIVIDADE * HORAS_TURNO[t]
    c1_rows.append({
        "Turno"               : TURNOS_LABEL[t],
        "Médicos Alocados"    : med,
        "Custo Turno (R$/dia)": round(med * CUSTO_HORA[t] * HORAS_TURNO[t], 2),
        "Demanda (atend.)"    : round(float(demanda_media[t]), 1),
        "Capacidade (atend.)" : cap,
        "Ociosidade (atend.)" : round(max(0, cap - float(demanda_media[t])), 1),
    })
c1_df    = pd.DataFrame(c1_rows)
c1_custo = c1_df["Custo Turno (R$/dia)"].sum()
c1 = {"nome": "C1", "status": "Manual", "custo": c1_custo, "df": c1_df}
print(f"     Status       : Manual (sem otimizador)")
print(f"     Custo diário : R$ {c1_custo:,.2f}")
for _, r in c1_df.iterrows():
    print(f"       {r['Turno']:<6}: {r['Médicos Alocados']:>2} médico(s) | "
          f"Cap: {r['Capacidade (atend.)']:>3} atend. | "
          f"Dem: {r['Demanda (atend.)']:>5.1f} | "
          f"Ocioso: {r['Ociosidade (atend.)']:>5.1f}")

# C2 — Otimizado
print("\n  -> Cenário 2: Otimizado (PLI, demanda média)...")
c2 = resolver_modelo("C2_Otimizado", demanda_media)

# C3 — Pico
print("\n  -> Cenário 3: Pico (PLI, dia mais movimentado)...")
c3 = resolver_modelo("C3_Pico", demanda_pico)

# ---------------------------------------------------------------------------
# 5. ANÁLISE DE SENSIBILIDADE
# ---------------------------------------------------------------------------
print("\n[3/5] Análise de Sensibilidade (custo x fator de demanda)...")

fatores   = np.arange(0.70, 1.55, 0.05)
sens_rows = []
for f in fatores:
    dem_f = demanda_media * f
    r     = resolver_modelo(f"Sens_{f:.2f}", dem_f, verbose=False)
    sens_rows.append({
        "Fator"         : round(f, 2),
        "Descrição"     : f"{round(f*100)}% da demanda média",
        "Custo (R$/dia)": round(r["custo"], 2) if r["custo"] else None,
    })

df_sens = pd.DataFrame(sens_rows)
print(df_sens.to_string(index=False))

# ---------------------------------------------------------------------------
# 6. EXPORTAÇÃO
# ---------------------------------------------------------------------------
print("\n[4/5] Exportando resultados...")

xlsx_path = os.path.join(OUTPUT_DIR, "resultados_po.xlsx")
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
    c1["df"].to_excel(writer, sheet_name="C1_Baseline",   index=False)
    c2["df"].to_excel(writer, sheet_name="C2_Otimizado",  index=False)
    c3["df"].to_excel(writer, sheet_name="C3_Pico",       index=False)
    df_sens.to_excel(writer,  sheet_name="Sensibilidade", index=False)

    pd.DataFrame([
        {"Cenário": "C1 — Baseline (manual)",    "Custo R$/dia": round(c1["custo"], 2), "Status": c1["status"]},
        {"Cenário": "C2 — Otimizado (PLI)",      "Custo R$/dia": round(c2["custo"], 2), "Status": c2["status"]},
        {"Cenário": "C3 — Pico (dia crítico)",   "Custo R$/dia": round(c3["custo"], 2), "Status": c3["status"]},
    ]).to_excel(writer, sheet_name="Resumo", index=False)

print(f"      Salvo em: {xlsx_path}")

# ---------------------------------------------------------------------------
# RESUMO FINAL
# ---------------------------------------------------------------------------
economia    = c1["custo"] - c2["custo"]
pct_econ    = (economia / c1["custo"]) * 100 if c1["custo"] else 0
econ_anual  = economia * 365

print("\n" + "=" * 65)
print("  RESUMO COMPARATIVO DOS CENÁRIOS")
print("=" * 65)
print(f"\n  {'Cenário':<35} {'Status':<10} {'Custo/dia':>12}")
print(f"  {'-'*58}")
print(f"  {'C1 — Baseline (manual)':<35} {'Manual':<10} R$ {c1['custo']:>8,.2f}")
print(f"  {'C2 — Otimizado (PLI)':<35} {c2['status']:<10} R$ {c2['custo']:>8,.2f}")
print(f"  {'C3 — Pico (dia crítico)':<35} {c3['status']:<10} R$ {c3['custo']:>8,.2f}")
print(f"\n  Economia diária  (C1 -> C2): R$ {economia:>8,.2f}  ({pct_econ:.1f}%)")
print(f"  Economia anual projetada   : R$ {econ_anual:>8,.2f}")
print(f"\n  Arquivo: {xlsx_path}")
print()