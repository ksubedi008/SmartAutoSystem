import os
import django

# 1. Setup Django Environment
# Matches your settings folder name 'config'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Matches your actual model names from core/models.py
from core.models import Location, Route

def populate_database():
    # 2. Define the Map (Direct Connections)
    direct_paths = {
        "Kamal Chock": {"Khuttidangi": 2},
        "Khuttidangi": {"Kamal Chock": 2, "Dhulabari Market": 3},
        "Dhulabari Market": {"Khuttidangi": 3, "Dhulabari": 3},
        "Dhulabari": {"Dhulabari Market": 3, "Ittavatta": 3, "Charali": 3, "Jyamargadi": 4},
        "Ittavatta": {"Dhulabari": 3, "Kakarvitta": 3},
        "Kakarvitta": {"Ittavatta": 3},
        "Charali": {"Dhulabari": 3, "Birtamod": 3},
        "Birtamod": {"Charali": 3, "Chandragadhi Airport": 13},
        "Jyamargadi": {"Dhulabari": 4, "Chandragadhi Airport": 6},
        "Chandragadhi Airport": {"Jyamargadi": 6, "Mechi Multiple Campus": 7, "Birtamod": 13},
        "Mechi Multiple Campus": {"Chandragadhi Airport": 7}
    }

    # 3. Create Locations
    print("Creating/Verifying Locations...")
    all_names = list(direct_paths.keys())
    db_locations = {}
    
    for name in all_names:
        # Changed 'Place' to 'Location'
        loc, _ = Location.objects.get_or_create(name=name)
        db_locations[name] = loc

    # 4. Calculate All Routes (Floyd-Warshall Algorithm)
    INF = 9999
    dist = {src: {dest: INF for dest in all_names} for src in all_names}

    # Initialize distances
    for p in all_names:
        dist[p][p] = 0
        if p in direct_paths:
            for neighbor, d in direct_paths[p].items():
                dist[p][neighbor] = d

    # Calculate logic (Finding shortest paths)
    for k in all_names:
        for i in all_names:
            for j in all_names:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # 5. Save to Database
    print("Saving 110 Routes to Database...")
    count = 0
    for src in all_names:
        for dest in all_names:
            if src != dest and dist[src][dest] != INF:
                # Using 'get_or_create' avoids duplicates if you run this twice
                Route.objects.get_or_create(
                    source=db_locations[src],
                    destination=db_locations[dest],
                    defaults={'distance_km': dist[src][dest]} # Changed to 'distance_km'
                )
                count += 1
    
    print("------------------------------------------------")
    print(f"SUCCESS: {count} routes have been added to your system.")
    print("------------------------------------------------")

if __name__ == '__main__':
    populate_database()