import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📈 **Veta SHDA Cloud**")

# ==================== FORMULARIO SIDEBAR ====================
with st.sidebar:
    st.header("🔑 **Login SHDA**")
    
    broker_id = st.number_input("Broker ID", value=284, min_value=1)
    dni = st.text_input("DNI", placeholder="25070170")
    username = st.text_input("Usuario", placeholder="mguazzardo")
    password = st.text_input("Contraseña", type="password")
    comitente = st.text_input("Comitente", value="44849")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 **Conectar**", use_container_width=True):
            if all([dni, username, password]):
                try:
                    import SHDA
                    hb = SHDA.SHDA(broker_id, dni, username, password)
                    st.session_state.hb = hb
                    st.session_state.comitente = comitente
                    st.session_state.connected = True
                    st.success("✅ **Conectado!**")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ **Error**: {str(e)[:100]}")
                    st.session_state.connected = False
            else:
                st.warning("👆 **Completa todos los campos**")
    
    with col2:
        if st.button("🔄 **Limpiar**", use_container_width=True):
            for key in ['hb', 'comitente', 'connected', 'portfolio', 'cedears']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ==================== DASHBOARD ====================
if st.session_state.get('connected') and 'hb' in st.session_state:
    hb = st.session_state.hb
    comitente = st.session_state.comitente
    
    st.sidebar.success(f"**{username}** - {comitente}")
    
    tab1, tab2 = st.tabs(["💼 **Portfolio**", "📈 **Cedears**"])
    
    # TAB 1: PORTFOLIO
    with tab1:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 **Portfolio**", use_container_width=True):
                with st.spinner("**Extrayendo...**"):
                    tenencias = hb.account(comitente)
                    df = tenencias[['TICK', 'CANT', 'PCIO', 'IMPO']].copy()
                    df['IMPO'] = pd.to_numeric(df['IMPO'], errors='coerce')
                    df = df.dropna(subset=['IMPO']).sort_values('IMPO', ascending=False)
                    st.session_state.portfolio = df
        
        with col2:
            if 'portfolio' in st.session_state:
                df = st.session_state.portfolio
                
                # MÉTRICAS
                c1, c2, c3 = st.columns(3)
                c1.metric("**Títulos**", len(df))
                c2.metric("**Total**", f"${df.IMPO.sum():,.0f}")
                c3.metric("**Top**", df.iloc[0].TICK)
                
                # GRÁFICO
                fig = px.pie(df.head(10), values='IMPO', names='TICK', 
                           title="**Top 10 Posiciones**")
                st.plotly_chart(fig, use_container_width=True)
                
                # TABLA
                st.subheader("**Detalle Completo**")
                st.dataframe(df, use_container_width=True)
                
                # DESCARGA
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "**💾 Descargar CSV**", 
                    csv, 
                    "veta_portfolio.csv", 
                    "text/csv",
                    use_container_width=True
                )
    
    # TAB 2: CEDEARS
    with tab2:
        if st.button("🔄 **Cedears 48hs**", use_container_width=True):
            with st.spinner("**Cotizando...**"):
                try:
                    cedears = hb.get_cedears("48hs")
                    st.session_state.cedears = cedears
                    st.success("✅ **Actualizado!**")
                except Exception as e:
                    st.error(f"⚠️ **Cedears**: {e}")
        
        if 'cedears' in st.session_state:
            df = st.session_state.cedears
            st.subheader("**Cotizaciones CEDEARS**")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "**💾 Descargar**", 
                csv, 
                "veta_cedears.csv", 
                use_container_width=True
            )

else:
    st.info("""
    ### 🎯 **3 Pasos**:
    1. **Sidebar** → **DNI/Usuario/Password**
    2. **Conectar** → 🔌
    3. **Portfolio/Cedears** → 📊
    """)
    
    st.balloons()

st.markdown("---")
st.caption("**tercemundo** - Actualizado en vivo")
