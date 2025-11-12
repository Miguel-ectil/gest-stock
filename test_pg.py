import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")

if "?sslmode=" not in url:
    url += "?sslmode=require"

print("🔍 Testando conexão com Supabase...")
try:
    conn = psycopg2.connect(url)
    print("✅ Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar:", e)
