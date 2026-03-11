#!/bin/bash
# ============================================================
# deploy.sh — Script de deploy para Voz Inclusiva en Railway
# Ejecutar desde: ~/Documents/Projects/voz-inclusiva/backend
# ============================================================

echo "🚀 Iniciando deploy de Voz Inclusiva..."

# 1. Verificar que estamos en la carpeta correcta
if [ ! -f "main.py" ]; then
  echo "❌ Error: No encuentro main.py. Asegúrate de estar en la carpeta backend/"
  exit 1
fi

# 2. Instalar Railway CLI si no está instalado
if ! command -v railway &> /dev/null; then
  echo "📦 Instalando Railway CLI..."
  brew install railway
fi

# 3. Inicializar git si no existe
if [ ! -d ".git" ]; then
  echo "📁 Inicializando repositorio git..."
  git init
  git add .
  git commit -m "🎙 Voz Inclusiva backend v1.0"
fi

# 4. Login en Railway
echo "🔐 Iniciando sesión en Railway (se abrirá el navegador)..."
railway login

# 5. Crear proyecto en Railway
echo "🛤 Creando proyecto en Railway..."
railway init

# 6. Deploy
echo "🚢 Subiendo el backend..."
railway up

# 7. Obtener URL pública
echo ""
echo "✅ Deploy completado. Tu URL pública es:"
railway domain

echo ""
echo "📝 PRÓXIMO PASO:"
echo "   Abre voz-inclusiva.html y cambia esta línea:"
echo "   const API_URL = 'http://localhost:8000';"
echo "   por:"
echo "   const API_URL = 'https://TU-URL.up.railway.app';"
