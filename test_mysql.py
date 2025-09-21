import mysql.connector

# Configuration de la base de données
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Plasma2020@",
    "database": "premierleague_db"
}

try:
    # Tentative de connexion
    conn = mysql.connector.connect(**db_config)
    print("Connexion réussie à la base de données MySQL.")
    # Liste les tables pour vérifier
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Tables dans la base de données :")
    for table in tables:
        print(table[0])
    conn.close()
except mysql.connector.Error as err:
    print(f"Erreur de connexion : {err}")
