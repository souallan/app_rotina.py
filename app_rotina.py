import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, date

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PIERRE Pro | Executive", layout="wide", page_icon="⚜️")

# --- 2. INJEÇÃO DE CSS DE LUXO ---
st.markdown("""
    <style>
    h1, h2, h3, .stTabs [data-baseweb="tab-list"] button { font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button {
        border-radius: 6px;
        border: 1px solid #D4AF37;
        color: #E2C044;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        color: #121212;
        transform: translateY(-2px);
    }
    div[data-testid="stExpander"] {
        border: 1px solid #333333;
        border-left: 4px solid #D4AF37;
        border-radius: 5px;
        background-color: #1A1C23;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. BANCO DE DADOS ---
conn = sqlite3.connect('rotina_trabalho.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tarefas 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              tarefa TEXT, categoria TEXT, prioridade TEXT, 
              status TEXT, data_criacao TEXT, data_vencimento TEXT, rotina BOOLEAN)''')
conn.commit()

def carregar_dados():
    return pd.read_sql_query("SELECT * FROM tarefas", conn)

# --- 4. CABEÇALHO ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>⚜️ Sistema PIERRE Executive</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Pendências | Importância | Execução | Rotina | Revisão | Estratégia</p>", unsafe_allow_html=True)
st.divider()

t_coleta, t_execucao, t_estrategia, t_revisao, t_controle = st.tabs([
    "📥 1. Coleta (P & I)", 
    "🚀 2. Execução (E & R)", 
    "🗺️ 3. Estratégia", 
    "📊 4. Revisão", 
    "⚙️ 5. Controle"
])

# --- ABA 1: COLETA (P & I) ---
with t_coleta:
    col_form, col_info = st.columns([2, 1])
    with col_form:
        st.subheader("Nova Demanda")
        with st.form("form_luxo", clear_on_submit=True):
            tarefa = st.text_input("Descrição da Tarefa")
            c1, c2 = st.columns(2)
            with c1:
                # Lista quebrada para evitar erros de linha longa
                opcoes_cat = [
                    "Operacional", 
                    "Gestão/Reuniões", 
                    "Desenvolvimento", 
                    "Pessoal"
                ]
                categoria = st.selectbox("Categoria Estratégica", opcoes_cat)
                vencimento = st.date_input("Deadline", date.today())
            with c2:
                opcoes_prio = [
                    "1. 🔥 Ur
