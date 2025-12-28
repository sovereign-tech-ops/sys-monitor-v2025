import hashlib
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# --- CONFIGURAÇÕES DO PROTOCOLO ---
DIAS_LIMITE = 14  # 2 semanas para o Dead Man's Switch
ARQUIVO_ALVO = "index.html"
ARQUIVO_LOG = "last_seen.txt"

# --- TRAVA DE SEGURANÇA (HASH) ---
# Gere seu hash no terminal com: powershell -Command "(Get-FileHash index.html -Algorithm SHA256).Hash.ToLower()"
# E cole o resultado entre as aspas abaixo:
HASH_ORIGINAL = "4719a103f4bd9e1465718e6a0ada06cd74033e13c3404a006a0e1bb79c5b44c2" 

# --- DESTINATÁRIOS (EIXO GO/SP + MONITORAMENTO) ---
DESTINATARIOS = [
    "corregedoria@pm.go.gov.br",           # Corregedoria PMGO
    "caop.controleexterno@mpgo.mp.br",      # MPGO Atividade Policial
    "direitoshumanos@mpgo.mp.br",           # MPGO Direitos Humanos
    "corregedoria@policiamilitar.sp.gov.br",# Corregedoria PMESP
    "ouvidoria@ouvidoria-policia.sp.gov.br",# Ouvidoria Polícias SP
    "pcd@mpf.mp.br"                         # MP Federal (Proteção PCD)
]

def disparar_protocolo(motivo):
    print(f"⚠️ DISPARANDO PROTOCOLO: {motivo}")
    
    # Pega as credenciais guardadas no cofre do GitHub Actions
    user = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    if not user or not password:
        print("Erro: Credenciais SMTP não encontradas nos Secrets.")
        return

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = ", ".join(DESTINATARIOS)
    msg['Subject'] = f"🚨 EMERGÊNCIA: PROTOCOLO GO-2025 ATIVADO ({motivo})"

    corpo = f"""
    ALERTA DE SEGURANÇA DIGITAL - REF: GO-2025
    Este é um disparo automático devido a: {motivo}.

    O sinal de integridade de FELIPE DA SILVA CAMPANHA DANTAS (PCD - CID F20.8) foi interrompido.
    Este sistema monitora casos de Abuso de Autoridade e Operações Fantasmas.

    DOSSIÊ COMPLETO E PROVAS:
    https://webnice-cloud.github.io/ahaahaha/

    Solicita-se intervenção dos órgãos competentes de GO e SP para garantir a integridade do autor.
    """
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.sendmail(user, DESTINATARIOS, msg.as_string())
        server.quit()
        print("✅ E-mails de contingência enviados com sucesso.")
    except Exception as e:
        print(f"❌ Falha no disparo: {e}")

def verificar_integridade():
    # 1. Verifica se o arquivo foi mexido (Sabotagem)
    sha256 = hashlib.sha256(open(ARQUIVO_ALVO, 'rb').read()).hexdigest()
    if sha256 != HASH_ORIGINAL:
        disparar_protocolo("VIOLAÇÃO DE INTEGRIDADE (TENTATIVA DE SABOTAGEM)")
        return True

    # 2. Verifica o tempo desde o último sinal (Dead Man's Switch)
    with open(ARQUIVO_LOG, 'r') as f:
        data_str = f.read().strip()
        ultima_vez = datetime.strptime(data_str, "%Y-%m-%d")
    
    if datetime.now() - ultima_vez > timedelta(days=DIAS_LIMITE):
        disparar_protocolo("AUSÊNCIA DE SINAL (SIGNAL LOSS)")
        return True
    
    print("✓ Sistema íntegro. Próxima verificação em 48 horas.")
    return False

if __name__ == "__main__":
    verificar_integridade()