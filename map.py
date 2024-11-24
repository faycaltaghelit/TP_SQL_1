import mysql.connector
import folium

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="belib_db"  # Your database name
)

cursor = db_connection.cursor()

# Query to fetch station data from the database
query = """
SELECT s.nom, s.adresse, s.latitude, s.longitude, c.statut, c.horaires, c.puissance
FROM stations s
LEFT JOIN stationsCara c ON s.station_id = c.station_id
"""
cursor.execute(query)

# Fetch all rows
stations = cursor.fetchall()

# Initialize a Folium map centered on Paris
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Process the station data and add them to the map
for station in stations:
    nom, adresse, latitude, longitude, statut, horaires, puissance = station

    # Create popup information for each station
    popup_content = f"""
        <b>{nom}</b><br>
        Adresse: {adresse}<br>
        Statut: {statut if statut else 'Inconnu'}<br>
        Horaires: {horaires if horaires else 'Non précisés'}<br>
        Puissance: {puissance if puissance else 'Inconnue'} kW
    """

    # Add a marker for each station
    folium.Marker(
        location=[latitude, longitude],
        popup=popup_content
    ).add_to(m)

# Save the map to an HTML file
file_path = r"C:\Users\Hp Omen\Desktop\map.html"  # Update this path as needed
m.save(file_path)

# Close the database connection
cursor.close()
db_connection.close()

print(f"Map has been saved to {file_path}")
