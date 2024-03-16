import random
from pymongo import MongoClient
import time

LIST_NAME = []
LIST_PHONE_NUMBER = []

def parse_population(file_path):
    population_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_data = line.strip().split(';')
            population_data[line_data[2]] = int(line_data[3])
    return population_data

def calculate_senior_isolated_population(senior_file_path, population_data):
    senior_isolated_population = {}
    senior_isolated_indicator = {}
    with open(senior_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_data = line.strip().split(';')
            senior_isolated_indicator[line_data[2]] = line_data[3].replace(',', '.')  # Remplacer la virgule par un point

    for senior in senior_isolated_indicator:
        if senior in population_data:
            senior_isolated_population[senior] = int(population_data[senior] * float(senior_isolated_indicator[senior]))
    return senior_isolated_population

def set_random_value():
    with open('data_profil.csv', 'r', encoding='utf-8') as file:
        for line in file:
            line_parsed = line.strip().split(',')
            LIST_NAME.append(line_parsed[0])
            LIST_PHONE_NUMBER.append(line_parsed[1])

def set_coord(path_to_csv, senior_isolated_population):
    profils = []
    coord_area_commune = {}
    
    with open(path_to_csv, 'r', encoding='utf-8') as file:
        for line in file:
            line_data = line.strip().split(';')
            coord = line_data[0].strip().split(',')
            if line_data[2] != 'name':
                coord_area_commune[line_data[2]] = {}
                coord_area_commune[line_data[2]]['coord'] = {'long' : coord[0], 'lat' : coord[1]}
                
    for area in coord_area_commune:
        if area in senior_isolated_population:
            profil = {}
            profil['coord'] = coord_area_commune[area]['coord']
            profil['name'] = LIST_NAME[random.randint(0,len(LIST_NAME)-1)]
            profil['phone'] = LIST_PHONE_NUMBER[random.randint(0,len(LIST_PHONE_NUMBER))-1]
            profil['commune'] = area
            profils.append(profil.copy())
            
            profil.clear()
            
    return profils

# Fonction pour insérer un document dans la collection
def insert_document(collection, data_to_insert):
    collection.insert_one(data_to_insert)

if __name__ == "__main__":
    population_file_path = '200300.csv'
    senior_file_path = '244400.csv' 
    set_random_value()
    population_data = parse_population(population_file_path)
    senior_isolated_population = calculate_senior_isolated_population(senior_file_path, population_data)
    
    data_to_send = set_coord('communes-belges0.csv',senior_isolated_population)
    
    
    while True:
        random_value = random.randint(0,len(data_to_send)-1)
        random_profil = data_to_send[random_value]
        uri = "mongodb://localhost:27017"
        client = MongoClient(uri)
        
        try:
            # Connexion à la base de données MongoDB
            print("Connecting to MongoDB...")
            db = client.hack_data
            collection = db.data

            # Insertion du document dans la collection
            insert_document(collection, random_profil)
            print("Document inserted successfully.")
            
            time.sleep(10)

        except Exception as e:
            print("An error occurred:", e)
