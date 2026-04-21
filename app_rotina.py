import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, date

# 1. SETUP
st.set_page_config(page_title="PIERRE", layout="wide")
db = "p3.db" # Novo banco para evitar conflitos

# 2. BANCO
con = sqlite3.connect(db, check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY, n TEXT, c TEXT, p TEXT, s TEXT, d TEXT, v TEXT, r INT)")
con.commit()

# 3. ESTILO
st.markdown("<style>.stButton>button{width:100%; border:1px solid #D4AF37;}</style>", unsafe_allow_html=True)

# 4. TABS
st.title("⚜️ PIERRE Executive")
t1, t2, t3, t4 = st.tabs(["Add", "Work", "View", "Admin"])

with t1:
    with st.form("f"):
        nome = st.text_input("Tarefa")
        cat = st.selectbox("Cat", ["Op", "Gest", "Dev", "Pes"])
        prio = st.selectbox("Prio", ["1.Urg", "2.Imp", "3.Del", "4.Low"])
        venc = st.date_input("Prazo", date.today())
        if st.form_submit_button("Ok"):
            if nome:
                hoje = datetime.now().strftime("%Y-%m-%d")
                cur.execute("INSERT INTO t (n,c,p,s,d,v,r) VALUES (?,?,?,?,?,?,?)",
                            (nome, cat, prio, "Back", hoje, venc.strftime("%Y-%m-%d"), 0))
                con.commit()
                st.rerun()

with t2:
    df = pd.read_sql("SELECT * FROM t", con)
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("📋 Back")
            for _, r in df[df['s'] == 'Back'].iterrows():
                if st.button(f"Go: {r['n']}", key=f"s{r['id']}"):
                    cur.execute("UPDATE t SET s='Run' WHERE id=?", (r['id'],))
                    con.commit()
                    st.rerun()
        with c2:
            st.write("⏳ Run")
            for _, r in df[df['s'] == 'Run'].iterrows():
                if st.button(f"End: {r['n']}", key=f"e{r['id']}"):
                    cur.execute("UPDATE t SET s='Done' WHERE id=?", (r['id'],))
                    con.commit()
                    st.rerun()
        with c3:
            st.write("✅ Done")
            for _, r in df[df['status' if 'status' in df else 's'] == 'Done'].iterrows():
                st.write(f"~{r['n']}~")

with t3:
    df3 = pd.read_sql("SELECT * FROM t", con)
    if not df3.empty:
        st.plotly_chart(px.pie(df3, names='c', hole=.4), use_container_width=True)
