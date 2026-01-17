# vetacap

text
# Veta Portfolio Tracker

Script automatizado para extraer **tenencias SHDA** y **cotizaciones CEDEARS** a CSV.

## 🚀 Uso rápido

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
Configurar credenciales → Copia .env:
```
bash
cp .env.example .env
# Edita .env con tus datos SHDA
Ejecutar:
```

importante, ejecutar el pip install -r requirements

```
pip install -r requirements.txt
```

Luego

```
python veta_shda.py
📁 Archivos generados
Archivo	Contenido
veta_portfolio.csv	Tenencias limpias (TICK/CANT/PCIO/IMPO)
veta_portfolio_full.csv	Portfolio completo
veta_cedears.csv	Cotizaciones CEDEARS (48hs)
🔧 Configuración .env
COPIA .env.example → .env y completa:
```

BROKER_ID=284                    # Broker ID (fijo)
DNI=12345678                     # TU DNI real
SHDA_USER=mguazzardo             # Usuario SHDA  
SHDA_PASSWORD=tu_contraseña      # Contraseña SHDA
COMITENTE=29000                  # Tu comitente
🛡️ Seguridad
✅ Credenciales en .env (nunca en código)

✅ .env en .gitignore

✅ Fallbacks seguros si falta config

📊 Columnas Portfolio
Columna	Descripción
TICK	Símbolo (GGAL, CELU, etc.)
CANT	Cantidad
PCIO	Precio unitario
IMPO	Importe total
SHDA no encontrada	pip install SHDA
