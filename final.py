import SHDA
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar .env
load_dotenv()

# Credenciales obligatorias desde .env
broker_id = int(os.getenv('BROKER_ID'))
dni = os.getenv('DNI')
user = os.getenv('SHDA_USER')
password = os.getenv('SHDA_PASSWORD')
comitente = os.getenv('COMITENTE', '44849')

# Validar TODO esté presente
missing = [k for k, v in [('BROKER_ID', broker_id), ('DNI', dni), 
                         ('SHDA_USER', user), ('SHDA_PASSWORD', password)] 
           if not v]
if missing:
    print(f"❌ FALTAN en .env: {missing}")
    print("Crea .env con:")
    print("BROKER_ID=284")
    print("DNI=25070170") 
    print("SHDA_USER=mguazzardo")
    print("SHDA_PASSWORD=tu_contraseña")
    exit(1)

print("✅ Todas las credenciales cargadas desde .env")
hb = SHDA.SHDA(broker_id, dni, user, password)

# === TU CÓDIGO ORIGINAL (funciona perfecto) ===
print("\n=== INSPECCIONANDO PORTFOLIO ===")
tenencias = hb.account(comitente)

print("Columnas disponibles:")
print(tenencias.columns.tolist())
print("\nShape:", tenencias.shape)
print(tenencias.head())

# Columnas detectadas ✓
tick_col = 'TICK'
cant_col = 'CANT' 
pcio_col = 'PCIO'
impo_col = 'IMPO'

portfolio_core = tenencias[[tick_col, cant_col, pcio_col, impo_col]].copy()
portfolio_core.columns = ['TICK', 'CANT', 'PCIO', 'IMPO']
print("\n✅ PORTFOLIO EXTRAÍDO:")
print(portfolio_core.head())
portfolio_core.to_csv('veta_portfolio.csv', index=False)

print("\n¡Listo! veta_portfolio.csv creado.")
