import streamlit as st
import pandas as pd
import SHDA
import io

st.title("🚀 SHDA Portfolio Extractor")

# Formulario para credenciales
with st.form("credentials_form"):
    st.header("📋 Ingresa tus credenciales")
    broker_id = st.number_input("Broker ID", min_value=1, value=284)
    dni = st.text_input("DNI", value="25070170")
    shda_user = st.text_input("SHDA User", value="mguazzardo")
    shda_password = st.text_input("SHDA Password", type="password")
    comitente = st.text_input("Comitente", value="44849")
    
    submitted = st.form_submit_button("🔑 Conectar y Extraer Portfolio")
    
    if submitted:
        # Validar credenciales
        missing = [k for k, v in [('BROKER_ID', broker_id), ('DNI', dni), 
                                  ('SHDA_USER', shda_user), ('SHDA_PASSWORD', shda_password)] 
                  if not v]
        if missing:
            st.error(f"❌ FALTAN: {missing}")
            st.stop()
        
        with st.spinner("Conectando a SHDA..."):
            try:
                hb = SHDA.SHDA(broker_id, dni, shda_user, shda_password)
                st.success("✅ Conexión exitosa!")
                
                st.header("📊 Inspeccionando Portfolio")
                tenencias = hb.account(comitente)
                
                st.write("**Columnas disponibles:**")
                st.write(tenencias.columns.tolist())
                st.write(f"**Shape:** {tenencias.shape}")
                st.dataframe(tenencias.head())
                
                # Procesar portfolio
                tick_col = 'TICK'
                cant_col = 'CANT' 
                pcio_col = 'PCIO'
                impo_col = 'IMPO'
                
                portfolio_core = tenencias[[tick_col, cant_col, pcio_col, impo_col]].copy()
                portfolio_core.columns = ['TICK', 'CANT', 'PCIO', 'IMPO']
                
                st.subheader("✅ Portfolio Extraído")
                st.dataframe(portfolio_core)
                
                # Descarga CSV
                csv_buffer = io.StringIO()
                portfolio_core.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="💾 Descargar veta_portfolio.csv",
                    data=csv_buffer.getvalue(),
                    file_name="veta_portfolio.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Verifica tus credenciales y conexión.")

st.info("👆 Ingresa tus datos y presiona 'Conectar y Extraer Portfolio'")
