import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, date

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="PIERRE Pro", layout="wide", page_icon="⚜️")

# --- 2. LISTAS DE OPÇÕES (Movidas para evitar erros de quebra de linha) ---
OPCOES_CAT = ["Operacional", "Gestão", "Estudo", "Pessoal"]
OPCOES_PRIO = ["1. Urgente", "2. Importante", "3. Delegar", "4. Baixo Impacto"]
OPCOES_STATUS = ["Backlog", "Andamento", "Concluído"]

# --- 3. ESTILO CSS ---
st.markdown("""
    <style>
    .stButton>button { border-radius: 6px; border: 1px solid #D4AF37; color: #E2C044; }
    .stButton>button:hover { background-color: #D4AF37; color: #121212; }
    div[data-testid="stExpander"] { border-left: 4px solid #D4AF37; background-color: #1A1C23; }
    </style>
""", unsafe_allow_html=True)

# --- 4. BANCO DE DADOS ---
conn = sqlite3.connect('rotina_trabalho.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tarefas 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              tarefa TEXT, categoria TEXT, prioridade TEXT, 
              status TEXT, data_criacao TEXT, data_vencimento TEXT, rotina BOOLEAN)''')
conn.commit()

def carregar():
    return pd.read_sql_query("SELECT * FROM tarefas", conn)

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>⚜️ PIERRE Executive</h1>", unsafe_allow_html=True)

t1, t2, t3, t4, t5 = st.tabs(["📥 Coleta", "🚀 Execução", "🗺️ Estratégia", "📊 Revisão", "⚙️ Ajustes"])

with t1:
    with st.form("f1", clear_on_submit=True):
        nome = st.text_input("O que precisa ser feito?")
        c1, c2 = st.columns(2)
        cat = c1.selectbox("Categoria", OPCOES_CAT)
        venc = c1.date_input("Prazo", date.today())
        prio = c2.selectbox("Prioridade", OPCOES_PRIO)
        rot = c2.checkbox("É uma Rotina?")
        if st.form_submit_button("Registrar"):
            if nome:
                hoje = datetime.now().strftime("%Y-%m-%d")
                c.execute("INSERT INTO tarefas (tarefa, categoria, prioridade, status, data_criacao, data_vencimento, rotina) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (nome, cat, prio, "Backlog", hoje, venc.strftime("%Y-%m-%d"), rot))
                conn.commit()
                st.rerun()

with t2:
    df = carregar()
