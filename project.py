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