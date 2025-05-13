import sqlite3
conn = sqlite3.connect('asos_weather.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📋 테이블 목록:", tables)
conn.close()
