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

# --- TRAVA DE SEGURANÇA (HASH SHA-256) ---
HASH_ORIGINAL = "4719a103f4bd9e1465718e6a0ada06cd74033e13c3404a006a0e1bb79c5b44c2" 

# --- DESTINATÁRIOS OFICIAIS (EIXO GO/SP + MONITORAMENTO) ---
DESTINATARIOS = [
    "corregedoria@pm.go.gov.br",           # Corregedoria PMGO
    "caop.controleexterno@mpgo.mp.br",      # MPGO Atividade Policial
    "direitoshumanos@mpgo.mp.br",           # MPGO Direitos Humanos
    "corregedoria@policiamilitar.sp.gov.br",# Corregedoria PMESP
    "ouvidoria@ouvidoria-policia.sp.gov.br",# Ouvidoria Polícias SP
    "pcd@mpf.mp.br",                        # MP Federal (Proteção PCD)
    "deusefielweb2001@gmail.com"            # Sua cópia de segurança
]

def disparar_protocolo(motivo):
    print(f"⚠️ ATIVANDO DISPARO: {motivo}")
    
    user = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    if not user or not password:
        print("Erro: Credenciais não encontradas nos Secrets.")
        return

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = ", ".join(DESTINATARIOS)
    msg['Subject'] = f"🚨 EMERGÊNCIA: PROTOCOLO GO-2025 ATIVADO ({motivo})"

    corpo = f"""
    ALERTA DE SEGURANÇA DIGITAL - REF: PROTOCOLO GO-2025
    Este disparador automático foi ativado devido a: {motivo}.

    O sinal de integridade de FELIPE DA SILVA CAMPANHA DANTAS (PCD - CID F20.8) foi interrompido.
    Este sistema monitora possíveis casos de Abuso de Autoridade e Operações Irregulares.

    DOSSIÊ COMPLETO E PROVAS CUSTODIADAS:
    https://webnice-cloud.github.io/ahaahaha/

    Solicita-se a imediata intervenção dos órgãos de controle de GO e SP para garantir a integridade física e legal do autor.
    """
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        # Uso de SSL Direto (Porta 465) para maior compatibilidade com órgãos GOV
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(user, password)
        server.sendmail(user, DESTINATARIOS, msg.as_string())
        server.quit()
        print("✅ Protocolo enviado aos órgãos competentes.")
    except Exception as e:
        print(f"❌ Falha crítica no disparo: {e}")

def verificar_integridade():
    # 1. Checagem de Sabotagem (Hash)
    sha256 = hashlib.sha256(open(ARQUIVO_ALVO, 'rb').read()).hexdigest()
    if sha256 != HASH_ORIGINAL:
        disparar_protocolo("VIOLAÇÃO DE INTEGRIDADE (TENTATIVA DE SABOTAGEM)")
        return True

    # 2. Checagem de Vida (Dead Man's Switch)
    with open(ARQUIVO_LOG, 'r') as f:
        data_str = f.read().strip()
        ultima_vez = datetime.strptime(data_str, "%Y-%m-%d")
    
    if datetime.now() - ultima_vez > timedelta(days=DIAS_LIMITE):
        disparar_protocolo("AUSÊNCIA DE SINAL (DEAD MAN SWITCH)")
        return True
    
    print(f"✓ Sistema íntegro. Último sinal: {data_str}. Status: Vigilância Ativa.")
    return False

if __name__ == "__main__":
    verificar_integridade()
