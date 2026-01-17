import streamlit as st
import pandas as pd
import SHDA
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="Veta SHDA", 
    page_icon="📈",
    layout="wide"
)

st.title("📈 Veta SHDA Portfolio")
st.markdown("**Dashboard en vivo** - Actualización automática")

# ==================== FORMULARIO CREDENCIALES ====================
with st.sidebar:
    st.header("🔑 Conexión SHDA")
    
    with st.form("shda_form", clear_on_submit=False):
        broker_id = st.number_input("Broker ID", value=284, min_value=1)
        dni = st.text_input("DNI", placeholder="12345678", help="Sin puntos/guiones")
        user = st.text_input("Usuario SHDA", placeholder="mguazzardo")
        password = st.text_input("Contraseña SHDA", type="password")
        comitente = st.text_input("Comitente", value="44849", placeholder="44849")
        
        connect_btn = st.form_submit_button("🔌 Conectar", use_container_width=True)
    
    if st.session_state.get("connected", False):
        st.success(f"✅ Conectado: {user}")
        if st.button("🔄 Reconectar", use_container_width=True):
            st.session_state.connected = False
            st.session_state.hb = None
            st.rerun()
    else:
        st.info("👆 Completa y conecta")

# ==================== LÓGICA CONEXIÓN ====================
if connect_btn and all([dni, user, password]):
    try:
        with st.spinner("Conectando SHDA..."):
            hb = SHDA.SHDA(broker_id, dni, user, password)
            st.session_state.hb = hb
            st.session_state.connected = True
            st.session_state.comitente = comitente
            st.rerun()
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.session_state.connected = False

# ==================== DASHBOARD ====================
if st.session_state.get("connected") and st.session_state.get("hb"):
    hb = st.session_state.hb
    comitente = st.session_state.comitente
    
    tab1, tab2 = st.tabs(["💼 Portfolio", "📈 CEDEARS"])
    
    # TAB 1: PORTFOLIO
    with tab1:
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.metric("📊 Activos", len(st.session_state.get("portfolio", 0)))
        
        with col2:
            portfolio_df = st.session_state.get("portfolio")
            if portfolio_df is not None:
                total = portfolio_df['IMPO'].sum()
                st.metric("💰 Total", f"${total:,.0f}")
        
        with col3:
            if st.button("🔄 Actualizar Portfolio", type="primary"):
                with st.spinner("Extrayendo..."):
                    tenencias = hb.account(comitente)
                    
                    # Portfolio limpio
                    portfolio = tenencias[['TICK', 'CANT', 'PCIO', 'IMPO']].copy()
                    portfolio['IMPO'] = pd.to_numeric(portfolio['IMPO'], errors='coerce')
                    portfolio = portfolio.dropna()
                    
                    st.session_state.portfolio = portfolio
                    st.rerun()
        
        # MOSTRAR CSV EN PANTALLA
        if "portfolio" in st.session_state:
            portfolio = st.session_state.portfolio
            
            st.subheader("📋 Portfolio Completo")
            st.dataframe(portfolio.sort_values('IMPO', ascending=False), 
                        use_container_width=True)
            
            # Gráfico
            fig = px.pie(portfolio.head(10), values='IMPO', names='TICK', 
                        title="Top 10 Posiciones")
            st.plotly_chart(fig, use_container_width=True)
            
            # Descarga
            csv = portfolio.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Descargar CSV", csv, "veta_portfolio.csv", "text/csv")
    
    # TAB 2: CEDEARS
    with tab2:
        if st.button("📊 Actualizar CEDEARS", type="secondary"):
            with st.spinner("Cotizando..."):
                cedears = hb.get_cedears("48hs")
                st.session_state.cedears = cedears
        
        if "cedears" in st.session_state:
            cedears = st.session_state.cedears
            st.subheader("📈 CEDEARS 48hs")
            st.dataframe(cedears, use_container_width=True)
            
            csv_c = cedears.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Descargar CEDEARS", csv_c, "veta_cedears.csv")

else:
    st.warning("🔌 Conecta SHDA en la sidebar para ver datos")
    
    st.markdown("""
    ### 🎯 Pasos:
    1. Completa **DNI/Usuario/Contraseña**
    2. Click **🔌 Conectar**
    3. ¡Disfruta tu dashboard!
    """)

# Footer
st.markdown("---")
st.caption(f"Actualizado: {datetime.now().strftime('%H:%M:%S')}")
