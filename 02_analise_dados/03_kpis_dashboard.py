"""
=============================================================================
MedFácil Clínicas — Projeto de Extensão de Sistemas Inteligentes
=============================================================================
Script  : 03_kpis_dashboard.py
Etapa   : KPIs + Dashboard Visual
Autor   : Robert França de Queiroz Sampaio
Data    : Maio/2026
=============================================================================
DESCRIÇÃO:
  Calcula os 3 KPIs principais do projeto e gera 6 gráficos para o dashboard:

  KPI 1 — Tempo Médio de Espera (TME) por turno e tipo de admissão
  KPI 2 — Taxa de Ocupação por Turno (% de atendimentos por turno)
  KPI 3 — Volume de Atendimentos por Especialidade (condição médica)

  Gráficos gerados:
    G1 — Distribuição do Tempo de Espera por Tipo de Admissão (Boxplot)
    G2 — TME Médio por Turno (Barras)
    G3 — Taxa de Ocupação por Turno (Pizza)
    G4 — Volume de Atendimentos por Condição Médica (Barras Horizontais)
    G5 — Atendimentos por Mês ao Longo do Tempo (Linha)
    G6 — Heatmap de Atendimentos por Hora x Dia da Semana
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

# ---------------------------------------------------------------------------
# 0. CONFIGURAÇÃO
# ---------------------------------------------------------------------------
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "healthcare_clean.csv")
CHART_DIR  = os.path.join(BASE_DIR, "output", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# Paleta de cores MedFácil
COLORS = {
    "primary"  : "#1A3A5C",
    "secondary": "#2E6DA4",
    "accent"   : "#E8734A",
    "light"    : "#D6E4F0",
    "success"  : "#27AE60",
    "warning"  : "#F39C12",
    "danger"   : "#C0392B",
    "gray"     : "#7F8C8D",
}

PALETTE_SHIFTS   = [COLORS["primary"], COLORS["secondary"], COLORS["accent"]]
PALETTE_COND     = sns.color_palette("Blues_r", 6)

plt.rcParams.update({
    "figure.dpi"     : 150,
    "font.family"    : "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize" : 13,
    "axes.titleweight": "bold",
    "axes.labelsize" : 11,
})

print("=" * 65)
print("  MedFácil Clínicas — KPIs & Dashboard")
print("=" * 65)

# ---------------------------------------------------------------------------
# 1. CARREGAMENTO
# ---------------------------------------------------------------------------
print("\n[1/4] Carregando dataset limpo...")
df = pd.read_csv(INPUT_PATH)
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
df["Discharge Date"]    = pd.to_datetime(df["Discharge Date"])
print(f"      {len(df):,} registros carregados.")

# Ordem dos turnos
SHIFT_ORDER = ["Manhã", "Tarde", "Noite"]

# ---------------------------------------------------------------------------
# 2. CÁLCULO DOS KPIs
# ---------------------------------------------------------------------------
print("\n[2/4] Calculando KPIs...")

# --- KPI 1: Tempo Médio de Espera (TME) ---
tme_geral   = df["Wait Time (min)"].mean()
tme_turno   = df.groupby("Shift")["Wait Time (min)"].mean().reindex(SHIFT_ORDER)
tme_tipo    = df.groupby("Admission Type")["Wait Time (min)"].mean().sort_values(ascending=False)

# --- KPI 2: Taxa de Ocupação por Turno ---
ocupacao_turno = df["Shift"].value_counts(normalize=True).reindex(SHIFT_ORDER) * 100

# --- KPI 3: Volume por Condição Médica ---
volume_condicao = df["Medical Condition"].value_counts()

# --- Extras úteis ---
tme_condicao = df.groupby("Medical Condition")["Wait Time (min)"].mean().sort_values(ascending=False)
atend_mes    = df.groupby(df["Date of Admission"].dt.to_period("M")).size().reset_index()
atend_mes.columns = ["Periodo", "Volume"]
atend_mes["Periodo"] = atend_mes["Periodo"].astype(str)

# Heatmap: hora x dia da semana
dia_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dia_ptbr  = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
heat_data = df.groupby(["Weekday", "Hour of Admission"]).size().unstack(fill_value=0)
heat_data = heat_data.reindex(dia_order)

print(f"\n  ┌─────────────────────────────────────────────┐")
print(f"  │              RESUMO DOS KPIs                │")
print(f"  ├─────────────────────────────────────────────┤")
print(f"  │ KPI 1 — TME Geral         : {tme_geral:>6.1f} minutos  │")
for turno in SHIFT_ORDER:
    print(f"  │         TME ({turno:<5})       : {tme_turno[turno]:>6.1f} minutos  │")
print(f"  ├─────────────────────────────────────────────┤")
for turno in SHIFT_ORDER:
    print(f"  │ KPI 2 — Ocupação ({turno:<5})  : {ocupacao_turno[turno]:>6.1f}%          │")
print(f"  ├─────────────────────────────────────────────┤")
for cond, vol in volume_condicao.items():
    print(f"  │ KPI 3 — {cond:<20}  : {vol:>6,} atend.    │")
print(f"  └─────────────────────────────────────────────┘")

# ---------------------------------------------------------------------------
# 3. GERAÇÃO DOS GRÁFICOS
# ---------------------------------------------------------------------------
print("\n[3/4] Gerando gráficos...")

# ── G1: Boxplot — TME por Tipo de Admissão ─────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
tipos = df["Admission Type"].unique()
data_box = [df[df["Admission Type"] == t]["Wait Time (min)"].values for t in ["Emergency", "Urgent", "Elective"]]
bp = ax.boxplot(data_box, patch_artist=True, notch=False,
                medianprops=dict(color="white", linewidth=2))
cores_box = [COLORS["danger"], COLORS["warning"], COLORS["secondary"]]
for patch, cor in zip(bp["boxes"], cores_box):
    patch.set_facecolor(cor)
    patch.set_alpha(0.85)
ax.set_xticklabels(["Emergency", "Urgent", "Elective"])
ax.set_xlabel("Tipo de Admissão")
ax.set_ylabel("Tempo de Espera (minutos)")
ax.set_title("G1 — Distribuição do Tempo de Espera por Tipo de Admissão")
ax.yaxis.grid(True, linestyle="--", alpha=0.5)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "G1_boxplot_tme_tipo.png"), bbox_inches="tight")
plt.close()
print("      G1 salvo.")

# ── G2: Barras — TME Médio por Turno ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(tme_turno.index, tme_turno.values, color=PALETTE_SHIFTS, edgecolor="white", linewidth=1.2)
for bar, val in zip(bars, tme_turno.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
            f"{val:.1f} min", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_xlabel("Turno")
ax.set_ylabel("Tempo Médio de Espera (min)")
ax.set_title("G2 — Tempo Médio de Espera (TME) por Turno")
ax.set_ylim(0, tme_turno.max() * 1.2)
ax.yaxis.grid(True, linestyle="--", alpha=0.4)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "G2_barras_tme_turno.png"), bbox_inches="tight")
plt.close()
print("      G2 salvo.")

# ── G3: Pizza — Taxa de Ocupação por Turno ─────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    ocupacao_turno.values,
    labels=ocupacao_turno.index,
    autopct="%1.1f%%",
    colors=PALETTE_SHIFTS,
    startangle=140,
    pctdistance=0.75,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
for t in autotexts:
    t.set_fontsize(12)
    t.set_fontweight("bold")
    t.set_color("white")
ax.set_title("G3 — Taxa de Ocupação por Turno (%)", pad=20)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "G3_pizza_ocupacao_turno.png"), bbox_inches="tight")
plt.close()
print("      G3 salvo.")

# ── G4: Barras Horizontais — Volume por Condição Médica ────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
condicoes = volume_condicao.sort_values()
bars_h = ax.barh(condicoes.index, condicoes.values,
                 color=PALETTE_COND, edgecolor="white")
for bar, val in zip(bars_h, condicoes.values):
    ax.text(val + 100, bar.get_y() + bar.get_height()/2,
            f"{val:,}", va="center", fontsize=10, fontweight="bold")
ax.set_xlabel("Número de Atendimentos")
ax.set_title("G4 — Volume de Atendimentos por Condição Médica")
ax.xaxis.grid(True, linestyle="--", alpha=0.4)
ax.set_xlim(0, condicoes.max() * 1.12)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "G4_barras_volume_condicao.png"), bbox_inches="tight")
plt.close()
print("      G4 salvo.")

# ── G5: Linha — Atendimentos por Mês ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
x_vals = range(len(atend_mes))
ax.plot(x_vals, atend_mes["Volume"], color=COLORS["secondary"],
        linewidth=2, marker="o", markersize=4, markerfacecolor=COLORS["accent"])
ax.fill_between(x_vals, atend_mes["Volume"], alpha=0.15, color=COLORS["secondary"])

# Mostra rótulo apenas a cada 6 meses para não poluir
step = max(1, len(atend_mes) // 12)
ax.set_xticks(x_vals[::step])
ax.set_xticklabels(atend_mes["Periodo"].iloc[::step], rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Número de Atendimentos")
ax.set_title("G5 — Volume de Atendimentos por Mês (Série Histórica)")
ax.yaxis.grid(True, linestyle="--", alpha=0.4)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "G5_linha_atendimentos_mes.png"), bbox_inches="tight")
plt.close()
print("      G5 salvo.")

# ── G6: Heatmap — Hora x Dia da Semana ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(
    heat_data,
    ax=ax,
    cmap="Blues",
    linewidths=0.3,
    linecolor="white",
    annot=False,
    yticklabels=dia_ptbr,
    cbar_kws={"label": "Nº de Atendimentos"}
)
ax.set_xlabel("Hora do Dia (0–23h)")
ax.set_ylabel("Dia da Semana")
ax.set_title("G6 — Heatmap de Atendimentos por Hora × Dia da Semana")
ax.tick_params(axis="x", labelsize=8)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "G6_heatmap_hora_dia.png"), bbox_inches="tight")
plt.close()
print("      G6 salvo.")

# ---------------------------------------------------------------------------
# 4. EXPORTAÇÃO DOS KPIs EM EXCEL
# ---------------------------------------------------------------------------
print("\n[4/4] Exportando KPIs para Excel...")
import openpyxl

kpi_path = os.path.join(BASE_DIR, "output", "kpis_resumo.xlsx")
with pd.ExcelWriter(kpi_path, engine="openpyxl") as writer:
    # KPI 1
    kpi1 = pd.DataFrame({
        "Turno": tme_turno.index,
        "TME Médio (min)": tme_turno.values.round(1)
    })
    kpi1.to_excel(writer, sheet_name="KPI1_TME_por_Turno", index=False)

    # KPI 2
    kpi2 = pd.DataFrame({
        "Turno": ocupacao_turno.index,
        "Taxa de Ocupação (%)": ocupacao_turno.values.round(1)
    })
    kpi2.to_excel(writer, sheet_name="KPI2_Ocupacao_Turno", index=False)

    # KPI 3
    kpi3 = volume_condicao.reset_index()
    kpi3.columns = ["Condição Médica", "Volume de Atendimentos"]
    kpi3.to_excel(writer, sheet_name="KPI3_Volume_Condicao", index=False)

    # TME por tipo de admissão
    tme_tipo.reset_index().rename(columns={"index": "Tipo", "Wait Time (min)": "TME Médio (min)"}).to_excel(
        writer, sheet_name="TME_por_Tipo_Admissao", index=False
    )

print(f"      KPIs exportados: {kpi_path}")

# ---------------------------------------------------------------------------
# RESUMO FINAL
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("  Dashboard gerado com sucesso!")
print("=" * 65)
print(f"\n  Gráficos salvos em: {CHART_DIR}")
print("    • G1_boxplot_tme_tipo.png")
print("    • G2_barras_tme_turno.png")
print("    • G3_pizza_ocupacao_turno.png")
print("    • G4_barras_volume_condicao.png")
print("    • G5_linha_atendimentos_mes.png")
print("    • G6_heatmap_hora_dia.png")
print(f"\n  KPIs exportados : output/kpis_resumo.xlsx")
print()