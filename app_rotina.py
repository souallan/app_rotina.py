import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Organizador de Trabalho PIERRE", layout="wide")

# --- BANCO DE DADOS ---
conn = sqlite3.connect('rotina_trabalho.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tarefas 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              tarefa TEXT, categoria TEXT, prioridade TEXT, 
              status TEXT, data_criacao TEXT)''')
conn.commit()

# --- INTERFACE ---
st.title("🚀 Organizador de Rotina (Método PIERRE)")
st.markdown("""
**P**endências | **I**mportância | **E**xecução | **R**otina | **R**evisão | **E**stratégia
""")

aba_kanban, aba_nova, aba_gestao = st.tabs(["📋 Quadro Kanban", "➕ Nova Tarefa", "⚙️ Gerenciar Banco"])

# --- ABA: NOVA TAREFA (P de Pendências e I de Importância) ---
with aba_nova:
    st.subheader("📝 Coletar Pendências")
    with st.form("form_tarefa", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_t = st.text_input("O que precisa ser feito?")
            cat_t = st.selectbox("Categoria", ["Reunião", "Projeto", "E-mail/Mensagem", "Relatório", "Outros"])
        with col2:
            # Matriz de Eisenhower simplificada na prioridade
            prio_t = st.selectbox("Nível de Prioridade (Eisenhower)", 
                                 ["🔥 Urgente e Importante", 
                                  "📅 Importante (Não Urgente)", 
                                  "⚡ Urgente (Delegável)", 
                                  "☕ Baixa Prioridade"])
        
        if st.form_submit_button("Adicionar à Lista"):
            if nome_t:
                data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
                c.execute("INSERT INTO tarefas (tarefa, categoria, prioridade, status, data_criacao) VALUES (?, ?, ?, ?, ?)",
                          (nome_t, cat_t, prio_t, "Para Fazer", data_atual))
                conn.commit()
                st.success(f"Tarefa '{nome_t}' coletada!")
                st.rerun()

# --- ABA: QUADRO KANBAN (E de Execução) ---
with aba_kanban:
    df = pd.read_sql_query("SELECT * FROM tarefas", conn)
    
    if not df.empty:
        col_todo, col_doing, col_done = st.columns(3)
        
        with col_todo:
            st.warning("📌 PARA FAZER")
            items = df[df['status'] == 'Para Fazer']
            for _, item in items.iterrows():
                with st.expander(f"{item['tarefa']}"):
                    st.caption(f"Cat: {item['categoria']} | {item['prioridade']}")
                    if st.button("▶️ Começar", key=f"start_{item['id']}"):
                        c.execute("UPDATE tarefas SET status = 'Fazendo' WHERE id = ?", (item['id'],))
                        conn.commit()
                        st.rerun()

        with col_doing:
            st.info("🕒 FAZENDO")
            items = df[df['status'] == 'Fazendo']
            for _, item in items.iterrows():
                with st.expander(f"🛠️ {item['tarefa']}"):
                    st.caption(f"{item['prioridade']}")
                    if st.button("✅ Concluir", key=f"done_{item['id']}"):
                        c.execute("UPDATE tarefas SET status = 'Concluído' WHERE id = ?", (item['id'],))
                        conn.commit()
                        st.rerun()

        with col_done:
            st.success("🏁 CONCLUÍDO")
            items = df[df['status'] == 'Concluído']
            for _, item in items.iterrows():
                st.markdown(f"~~{item['tarefa']}~~ ✅")
    else:
        st.info("Nenhuma tarefa pendente. Use a aba 'Nova Tarefa' para começar.")

# --- ABA: GESTÃO (R de Revisão e E de Estratégia) ---
with aba_gestao:
    st.subheader("📊 Revisão de Dados")
    df_full = pd.read_sql_query("SELECT * FROM tarefas", conn)
    
    if not df_full.empty:
        # Editor para modificações rápidas
        st.write("Edite ou remova tarefas diretamente na tabela:")
        df_editado = st.data_editor(df_full, num_rows="dynamic", hide_index=True, use_container_width=True)
        
        if st.button("💾 Salvar Alterações Gerais"):
            # Limpa e reinseri para sincronizar
            c.execute("DELETE FROM tarefas")
            for _, row in df_editado.iterrows():
                c.execute("INSERT INTO tarefas (id, tarefa, categoria, prioridade, status, data_criacao) VALUES (?, ?, ?, ?, ?, ?)",
                          (row['id'], row['tarefa'], row['categoria'], row['prioridade'], row['status'], row['data_criacao']))
            conn.commit()
            st.success("Revisão salva!")
            st.rerun()
            
        if st.button("🗑️ Limpar todas as tarefas concluídas"):
            c.execute("DELETE FROM tarefas WHERE status = 'Concluído'")
            conn.commit()
            st.rerun()
    else:
        st.write("Sem dados para revisão.")

conn.close()
