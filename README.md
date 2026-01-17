# vetacap

text
# Veta Portfolio Tracker

Script automatizado para extraer **tenencias SHDA** y **cotizaciones CEDEARS** a CSV.

## 🚀 Uso rápido

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt

Configurar credenciales en .env

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

# Configuración SHDA (Broker Veta Capital)

| Variable      | Valor          | Descripción                  |
|---------------|----------------|------------------------------|
| `BROKER_ID`  | `284`          | Broker ID (fijo) [memory:1][conversation_history:4] |
| `DNI`        | `12345678`     | TU DNI real [memory:1][conversation_history:4] |
| `SHDA_USER`  | `qqmelo`       | Usuario SHDA [memory:1][conversation_history:4] |
| `SHDA_PASSWORD` | `quebuscas` | Contraseña SHDA [memory:1][conversation_history:4] |
| `COMITENTE`  | `29000`        | Tu comitente [memory:1][conversation_history:4] |



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
