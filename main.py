import random
from pymongo import MongoClient
import time
import certifi


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
            if line_data[1] == "Commune":
                senior_isolated_indicator[line_data[2]] = {"indicator" : line_data[3].replace(',', '.'), "type" : line_data[1]}

    for senior in senior_isolated_indicator:
        if senior in population_data:
            senior_isolated_population[senior] = {"pop_alone" : int(population_data[senior] * float(senior_isolated_indicator[senior]['indicator'])) , "type" : senior_isolated_indicator[senior]["type"]}
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

def get_municipality(filename):
    regions = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line_parsed = line.strip().split(';')
            type_entity = line_parsed[1]
            name = line_parsed[2]
            
            if type_entity == 'Province':
                province = name
                regions[province] = {}
            elif type_entity == 'Arrondissement':
                arrondissement = name
                regions[province][arrondissement] = []
            elif type_entity == 'Commune':
                regions[province][arrondissement].append(name)
    return regions            
            
if __name__ == "__main__":
    population_file_path = '200300.csv'
    senior_file_path = '244400.csv' 
    set_random_value()
    population_data = parse_population(population_file_path)
    senior_isolated_population = calculate_senior_isolated_population(senior_file_path, population_data)

    data_to_send = set_coord('communes-belges0.csv',senior_isolated_population)
    
    city_per_mun = get_municipality('244400.csv')

    while True:
        random_value = random.randint(0,len(data_to_send)-1)
        random_profil = data_to_send[random_value]
        #uri = "mongodb+srv://52676:yNHdKFyn3tPVtptZ@cluster0.kswno1o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&authSource=admin"
        uri= "mongodb://127.0.0.1:27017"
        client = MongoClient(uri)        
        try:
            # Connexion à MongoDB
            print("Connecting to MongoDB...")
            db = client.hack_data
            collection = db.data2

            # Je définir l'arrondissement et la province
            commune_to_found = random_profil['commune']
            arrondissement = None
            Province = None
            
            for prov in city_per_mun:
                try:
                    for arrond in city_per_mun[prov]:
                        if commune_to_found in city_per_mun[prov][arrond]:
                            arrondissement = arrond
                            Province = prov
                except:
                    pass
                
            random_profil['arrondissement'] = arrondissement
            random_profil['province'] = Province


            # Insertion collection
            insert_document(collection, random_profil)
            print("Document inserted successfully.")
            
            time.sleep(1)

        except Exception as e:
            print("An error occurred:", e)