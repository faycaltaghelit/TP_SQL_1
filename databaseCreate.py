import requests
import mysql.connector

# Récupérer les données depuis l'API
url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=belib-points-de-recharge-pour-vehicules-electriques-donnees-statiques&rows=1000"
response = requests.get(url)
data = response.json()

# Connexion à la base MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="belib_db"   
)

cursor = db_connection.cursor()

# Création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id VARCHAR(50),
    nom VARCHAR(255),
    adresse TEXT,
    latitude FLOAT,
    longitude FLOAT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stationsCara (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id VARCHAR(50),
    statut VARCHAR(50),
    horaires VARCHAR(50),
    puissance FLOAT
)
""")

# Insérer les données dans les tables
for record in data["records"]:
    fields = record["fields"]
    station_id = fields.get("id_pdc_local")
    nom = fields.get("nom_station", "")
    adresse = fields.get("adresse_station", "")
    coords = fields.get("coordonneesxy", [0, 0])
    latitude, longitude = coords[0], coords[1]
    puissance_nominale = fields.get("puissance_nominale")
    statut_pdc    = fields.get("statut_pdc")
    horaires = fields.get("horaires") 
     
    cursor.execute("""
    INSERT INTO stations (station_id, nom, adresse, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    """, (station_id, nom, adresse, latitude, longitude))
    cursor.execute("""
    INSERT INTO stationsCara (station_id, statut, horaires, puissance)
    VALUES (%s, %s, %s, %s)
    """, (station_id, statut_pdc, horaires, puissance_nominale))

# Commit et fermer la connexion
db_connection.commit()
cursor.close()
db_connection.close()

print("Les donnees ont ete inserees dans la base MySQL.")
