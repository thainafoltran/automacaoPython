import requests
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#PRIMEIRA TABELA
conexao = sqlite3.connect('projeto_rpa.db')
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS piadas (
        id TEXT PRIMARY KEY,
        piada TEXT,
        categoria TEXT
    )
''')

for _ in range(10):
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        id = data['id']
        piada = data['value']
        categoria = ', '.join(data.get('categories', [])) or 'Sem categoria'

        print('Coletando piadas... 🤪')

        cursor.execute('''
            INSERT OR REPLACE INTO piadas (
                id, piada, categoria
            ) VALUES (?, ?, ?)
        ''', (id, piada, categoria))
    else:
        print('Não foi possível encontrar piadas')

conexao.commit()

#SEGUNDA TABELA
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_processados (
        id TEXT PRIMARY KEY,
        piada TEXT,
        categoria TEXT
    )
''')

cursor.execute("SELECT * FROM piadas WHERE categoria LIKE '%dev%'")
dados_processados = cursor.fetchall()

for piada in dados_processados:
    cursor.execute('''
        INSERT OR REPLACE INTO dados_processados (
            id, piada, categoria
        ) VALUES (?, ?, ?)
    ''', piada)

conexao.commit()
conexao.close()

#ENVIANDO O E-MAIL
try:
    print('Enviando seu e-mail... 📨')

    servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_email.starttls()
    servidor_email.login('foltran96t@gmail.com', 'doej qbqb lvhk fjue')  

    remetente = 'foltran96t@gmail.com'
    destinatarios = ['thainafoltran@hotmail.com']
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = ', '.join(destinatarios)
    mensagem['Subject'] = 'Relatório de Piadas do Chuck Norris'

    contagem = len(dados_processados)
    if contagem > 0:
        for idx, piada in enumerate(dados_processados, 1):
            corpo = f"""Foram coletadas {contagem} piadas da categoria de desenvolvedor:\n\n🤣😂Piada{idx}:\n{piada[1]}\n\nEste e-mail foi gerado automaticamente com automação em Python."""
    else:
        corpo = "Nenhuma piada da categoria desenvolvedor foi encontrada! "

    mensagem.attach(MIMEText(corpo, 'plain'))
    servidor_email.sendmail(remetente, destinatarios, mensagem.as_string())

    print('📤 E-mail enviado com sucesso!')
except Exception as erro:
    print(f'Erro ao enviar e-mail: {erro}')
