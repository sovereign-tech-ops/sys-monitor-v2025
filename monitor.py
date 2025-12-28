import hashlib
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# --- CONFIGURAÇÕES DO PROTOCOLO ---
DIAS_LIMITE = 14  
ARQUIVO_ALVO = "index.html"
ARQUIVO_LOG = "last_seen.txt"

# --- TRAVA DE SEGURANÇA (HASH REAL DO SEU REPOSITÓRIO) ---
HASH_ORIGINAL = "4719a103f4bd9e1465718e6a0ada06cd74033e13c3404a006a0e1bb79c5b44c2" 

# --- DESTINATÁRIOS (CONFIGURADO PARA TESTE SEGURO) ---
DESTINATARIOS = [
    "deusefielweb2001@gmail.com"
]

def disparar_protocolo(motivo):
    print(f"⚠️ DISPARANDO PROTOCOLO: {motivo}")
    
    user = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    if not user or not password:
        print("Erro: Credenciais SMTP não encontradas nos Secrets.")
        return

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = ", ".join(DESTINATARIOS)
    msg['Subject'] = f"🚨 TESTE DE EMERGÊNCIA: PROTOCOLO GO-2025 ({motivo})"

    corpo = f"""
    ESTE É UM TESTE DO SISTEMA DE SEGURANÇA DIGITAL - REF: GO-2025
    
    O gatilho foi ativado por: {motivo}.
    
    Se este e-mail chegou, a conexão entre o GitHub e o seu Gmail está 100% OPERACIONAL.
    O sinal de integridade de FELIPE DA SILVA CAMPANHA DANTAS foi simulado.

    LINK DO DOSSIÊ:
    https://webnice-cloud.github.io/ahaahaha/
    """
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.sendmail(user, DESTINATARIOS, msg.as_string())
        server.quit()
        print(f"✅ E-mail de teste enviado para {DESTINATARIOS}")
    except Exception as e:
        print(f"❌ Falha no disparo: {e}")

def verificar_integridade():
    # 1. Verifica sabotagem
    sha256 = hashlib.sha256(open(ARQUIVO_ALVO, 'rb').read()).hexdigest()
    if sha256 != HASH_ORIGINAL:
        disparar_protocolo("SIMULAÇÃO DE SABOTAGEM (HASH MISMATCH)")
        return True

    # 2. Verifica tempo (Dead Man's Switch)
    with open(ARQUIVO_LOG, 'r') as f:
        data_str = f.read().strip()
        ultima_vez = datetime.strptime(data_str, "%Y-%m-%d")
    
    if datetime.now() - ultima_vez > timedelta(days=DIAS_LIMITE):
        disparar_protocolo("SIMULAÇÃO DE AUSÊNCIA DE SINAL")
        return True
    
    print("✓ Sistema íntegro. Nenhuma regra de disparo foi atingida.")
    return False

if __name__ == "__main__":
    verificar_integridade()
