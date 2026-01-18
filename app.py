import streamlit as st
import pandas as pd
import SHDA
import io

st.title("🚀 SHDA Portfolio Extractor")

# Estado para credenciales
if 'hb' not in st.session_state:
    st.session_state.hb = None
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = None

# Formulario credenciales (solo si no conectado)
if st.session_state.hb is None:
    st.header("📋 Ingresa tus credenciales")
    broker_id = st.number_input("Broker ID", min_value=1, value=284)
    dni = st.text_input("DNI")
    shda_user = st.text_input("SHDA User", value="mguazzardo")
    shda_password = st.text_input("SHDA Password", type="password")
    comitente = st.text_input("Comitente")
    
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("🔑 Conectar", type="primary"):
            missing = [k for k, v in [('BROKER_ID', broker_id), ('DNI', dni), 
                                      ('SHDA_USER', shda_user), ('SHDA_PASSWORD', shda_password)] 
                      if not v]
            if missing:
                st.error(f"❌ FALTAN: {missing}")
            else:
                try:
                    st.session_state.hb = SHDA.SHDA(broker_id, dni, shda_user, shda_password)
                    st.session_state.comitente = comitente
                    st.success("✅ Conectado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error conexión: {str(e)}")
else:
    st.success(f"✅ Conectado como {st.session_state.hb}")
    
    # Botón para extraer (fuera del form)
    if st.button("📊 Extraer Portfolio", type="primary"):
        with st.spinner("Extrayendo datos..."):
            try:
                tenencias = st.session_state.hb.account(st.session_state.comitente)
                
                tick_col = 'TICK'
                cant_col = 'CANT' 
                pcio_col = 'PCIO'
                impo_col = 'IMPO'
                
                portfolio_core = tenencias[[tick_col, cant_col, pcio_col, impo_col]].copy()
                portfolio_core.columns = ['TICK', 'CANT', 'PCIO', 'IMPO']
                st.session_state.portfolio = portfolio_core
                
                st.success("✅ Portfolio cargado!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error extracción: {str(e)}")

# Mostrar portfolio si existe
if st.session_state.portfolio is not None:
    st.header("✅ Tu Portfolio")
    st.dataframe(st.session_state.portfolio)
    
    # Descarga CSV (funciona perfecto fuera del form)
    
    # Botón reset
    if st.button("🔄 Nueva Conexión"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
