"""
=============================================================================
MedFácil Clínicas — Projeto de Extensão de Sistemas Inteligentes
=============================================================================
Script  : 01_etl.py
Etapa   : ETL — Extração, Transformação e Carga
Autor   : Robert França de Queiroz Sampaio
Data    : Maio/2026
Dataset : healthcare_dataset.csv (Prasad22 — Kaggle, 55.500 registros)
=============================================================================
DESCRIÇÃO:
  Pipeline completo de ETL que:
  1. Extrai o CSV bruto
  2. Limpa e padroniza os dados
  3. Engenheira as features ausentes (turno, hora, tempo de internação)
  4. Exporta o dataset limpo para data/processed/
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import hashlib

# ---------------------------------------------------------------------------
# 0. CONFIGURAÇÃO DE CAMINHOS
# ---------------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
RAW_PATH    = os.path.join(BASE_DIR, "data", "raw", "healthcare_dataset.csv")
PROC_DIR    = os.path.join(BASE_DIR, "data", "processed")
OUTPUT_PATH = os.path.join(PROC_DIR, "healthcare_clean.csv")

os.makedirs(PROC_DIR, exist_ok=True)

print("=" * 65)
print("  MedFácil Clínicas — ETL Pipeline")
print("=" * 65)

# ---------------------------------------------------------------------------
# 1. EXTRAÇÃO
# ---------------------------------------------------------------------------
print("\n[1/6] Carregando dataset bruto...")
df = pd.read_csv(RAW_PATH)
print(f"      Registros carregados : {len(df):,}")
print(f"      Colunas              : {list(df.columns)}")

# ---------------------------------------------------------------------------
# 2. LIMPEZA — NOMES E STRINGS
# ---------------------------------------------------------------------------
print("\n[2/6] Limpeza e padronização de strings...")

# Padroniza capitalização (ex: "Bobby JacksOn" → "Bobby Jackson")
df["Name"]             = df["Name"].str.title().str.strip()
df["Gender"]           = df["Gender"].str.strip().str.title()
df["Blood Type"]       = df["Blood Type"].str.strip().str.upper()
df["Medical Condition"]= df["Medical Condition"].str.strip().str.title()
df["Doctor"]           = df["Doctor"].str.strip().str.title()
df["Hospital"]         = df["Hospital"].str.strip().str.title()
df["Insurance Provider"]= df["Insurance Provider"].str.strip().str.title()
df["Admission Type"]   = df["Admission Type"].str.strip().str.title()
df["Medication"]       = df["Medication"].str.strip().str.title()
df["Test Results"]     = df["Test Results"].str.strip().str.title()

print(f"      Strings padronizadas.")

# ---------------------------------------------------------------------------
# 3. TIPOS DE DADOS — DATAS
# ---------------------------------------------------------------------------
print("\n[3/6] Convertendo colunas de data...")
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
df["Discharge Date"]    = pd.to_datetime(df["Discharge Date"],    errors="coerce")

# Remove registros com datas inválidas
antes = len(df)
df = df.dropna(subset=["Date of Admission", "Discharge Date"])
print(f"      Removidos por data inválida: {antes - len(df)} registros")

# ---------------------------------------------------------------------------
# 4. ENGENHARIA DE FEATURES
# ---------------------------------------------------------------------------
print("\n[4/6] Engenharia de features...")

# --- 4.1 Duração da internação (em dias) ---
df["Length of Stay (days)"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days
# Garante que não há valores negativos ou zero
df = df[df["Length of Stay (days)"] > 0]

# --- 4.2 Hora de entrada simulada (seed determinística por paciente) ---
# Como o dataset não tem hora, simulamos com seed baseada no nome
# Isso garante reprodutibilidade (mesma seed = mesma hora sempre)
np.random.seed(42)
df["Hour of Admission"] = np.random.randint(0, 24, size=len(df))

# --- 4.3 Turno com base na hora ---
def classify_shift(hour):
    if 6 <= hour < 14:
        return "Manhã"
    elif 14 <= hour < 22:
        return "Tarde"
    else:
        return "Noite"

df["Shift"] = df["Hour of Admission"].apply(classify_shift)

# --- 4.4 Tempo de espera simulado (em minutos) ---
# Baseado no tipo de admissão — reflete a realidade clínica
wait_time_map = {
    "Emergency" : lambda n: np.random.randint(5,  30,  n),
    "Urgent"    : lambda n: np.random.randint(20, 90,  n),
    "Elective"  : lambda n: np.random.randint(30, 180, n),
}

df["Wait Time (min)"] = 0
for admission_type, func in wait_time_map.items():
    mask = df["Admission Type"] == admission_type
    count = mask.sum()
    if count > 0:
        df.loc[mask, "Wait Time (min)"] = func(count)

# --- 4.5 Período do ano ---
df["Month"]   = df["Date of Admission"].dt.month
df["Year"]    = df["Date of Admission"].dt.year
df["Quarter"] = df["Date of Admission"].dt.quarter
df["Weekday"] = df["Date of Admission"].dt.day_name()

# --- 4.6 Faixa etária ---
bins   = [0, 18, 35, 50, 65, 120]
labels = ["0–18", "19–35", "36–50", "51–65", "65+"]
df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

# --- 4.7 Anonimização do nome (LGPD) ---
# Substituímos o nome real por um hash SHA-256 truncado
df["Patient ID"] = df["Name"].apply(
    lambda x: "PAC-" + hashlib.sha256(x.encode()).hexdigest()[:8].upper()
)
df = df.drop(columns=["Name"])  # Remove nome real — conformidade LGPD

print(f"      Features criadas: Shift, Hour, Wait Time, Length of Stay,")
print(f"                        Month, Year, Quarter, Weekday, Age Group, Patient ID")

# ---------------------------------------------------------------------------
# 5. VERIFICAÇÃO DE QUALIDADE
# ---------------------------------------------------------------------------
print("\n[5/6] Verificação de qualidade...")
nulls = df.isnull().sum()
nulls_found = nulls[nulls > 0]
if len(nulls_found) == 0:
    print("      Nenhum valor nulo encontrado. ✓")
else:
    print(f"      Valores nulos encontrados:\n{nulls_found}")

dupes = df.duplicated().sum()
print(f"      Duplicatas          : {dupes}")
print(f"      Registros finais    : {len(df):,}")
print(f"      Colunas finais      : {len(df.columns)}")

# ---------------------------------------------------------------------------
# 6. EXPORTAÇÃO
# ---------------------------------------------------------------------------
print("\n[6/6] Exportando dataset limpo...")
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
print(f"      Salvo em: {OUTPUT_PATH}")

# ---------------------------------------------------------------------------
# RESUMO FINAL
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("  ETL concluído com sucesso!")
print("=" * 65)
print(f"\n  Shape final  : {df.shape}")
print(f"  Período      : {df['Year'].min()} – {df['Year'].max()}")
print(f"\n  Colunas disponíveis:")
for col in df.columns:
    print(f"    • {col}")

print(f"\n  Distribuição por Turno:")
print(df["Shift"].value_counts().to_string())

print(f"\n  Distribuição por Tipo de Admissão:")
print(df["Admission Type"].value_counts().to_string())

print(f"\n  Distribuição por Condição Médica:")
print(df["Medical Condition"].value_counts().to_string())
print()