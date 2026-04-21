import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, date

# --- 1. CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="PIERRE Pro Executive", layout="wide", page_icon="⚜️")

# --- 2. DEFINIÇÃO DE OPÇÕES (Prevenção de Erros de Sintaxe) ---
OPCOES_CAT = ["Operacional", "Gestão/Reunião", "Desenvolvimento", "Pessoal"]
OPCOES_PRIO = ["1. 🔥 Urgente & Importante", "2. 📅 Importante", "3. ⚡ Urgente/Delegar", "4. ☕ Baixo Impacto"]
OPCOES_STATUS = ["Backlog", "Andamento", "Concluído"]

# --- 3. ESTILO CSS CUSTOMIZADO (LUXO) ---
st.markdown("""
    <style>
    .stButton>button { border-radius: 6px; border: 1px solid #D4AF37; color: #E2C044; transition: 0.3s; }
    .stButton>button:hover { background-color: #D4AF37; color: #121212; transform: translateY(-2px); }
    div[data-testid="stExpander"] { border-left: 5px solid #D4AF37; background-color: #1A1C23; border-radius: 8px; }
    .stMetric { background-color: #1A1C23; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- 4. BANCO DE DADOS (V2 para evitar OperationalError) ---
conn = sqlite3.connect('pierre_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tarefas 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              tarefa TEXT, categoria TEXT, prioridade TEXT, 
              status TEXT, data_criacao TEXT, data_vencimento TEXT, rotina BOOLEAN)''')
conn.commit()

def carregar_dados():
    return pd.read_sql_query("SELECT * FROM tarefas", conn)

# --- 5. CABEÇALHO ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>⚜️ Sistema PIERRE Executive</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Gestão de Alta Performance para Rotinas de Trabalho</p>", unsafe_allow_html=True)

tabs = st.tabs(["📥 1. Coleta", "🚀 2. Execução", "🗺️ 3. Estratégia", "📊 4. Revisão", "⚙️ 5. Gestão"])

# --- ABA 1: COLETA (P & I) ---
with tabs[0]:
    st.subheader("Nova Entrada de Dados")
    with st.form("form_pierre", clear_on_submit=True):
        tarefa_input = st.text_input("Descrição da Pendência")
        c1, c2 = st.columns(2)
        with c1:
            cat_input = st.selectbox("Categoria", OPCOES_CAT)
            venc_input = st.date_input("
