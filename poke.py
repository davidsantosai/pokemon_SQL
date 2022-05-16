import requests
import mysql.connector
from mysql.connector import Error
import sqlite3


pokemon_name = []
pokemon_imagen = list()
pokemon_habilidad1 = list()
pokemon_habilidad2 = list()
pokemon_ps = list()
pokemon_ataque = list()
pokemon_defensa = list()
pokemon_atqespecial = list()
pokemon_defespecial = list()
pokemon_velocidad = list()
pokemon_tipo1 = list()
pokemon_tipo2 = list()

poke_amount = 898
    
def get_pokemons():
    number = 1
    for i in range(poke_amount):
        url = "https://pokeapi.co/api/v2/pokemon/{}".format(number)
        response = requests.get(url)
        if response.status_code == 200:
            payload = response.json()
            name = payload.get('name',[])
            types = payload.get('types',[])
            ability = payload.get('abilities',[])
            stats = payload.get('stats',[])
            sprite = payload.get('sprites',[])

            pokemon_name.append(name)
            pokemon_imagen.append(sprite['other']['official-artwork']['front_default'])
            pokemon_habilidad1.append(ability[0]["ability"]["name"])
            if len(ability) > 1:
                pokemon_habilidad2.append(ability[1]["ability"]["name"])
            else:
                pokemon_habilidad2.append("")
            pokemon_ps.append(stats[0]["base_stat"])
            pokemon_ataque.append(stats[1]["base_stat"])
            pokemon_defensa.append(stats[2]["base_stat"])
            pokemon_atqespecial.append(stats[3]["base_stat"])
            pokemon_defespecial.append(stats[4]["base_stat"])
            pokemon_velocidad.append(stats[5]["base_stat"])
            pokemon_tipo1.append(types[0]['type']['name'])
            if len(types) > 1:
                pokemon_tipo2.append(types[1]['type']['name'])
            else:
                pokemon_tipo2.append("")
            number += 1
    main()

def create_connection(): 
    conn = None
    try:
        conn = sqlite3.connect("base_datos_sql")
    except Error as e:
        print(e)
    return conn

def create_poke(conn,project):
    sql = '''INSERT INTO pokemones (nombre,imagen,habilidad1,habilidad2,ps,ataque,defensa,atqespecial,defespecial,velocidad,tipo1,tipo2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql,project)
    return cur.lastrowid


def main():
    conn = create_connection()
    with conn:
        for i in range(poke_amount):
            poke = (pokemon_name[i],pokemon_imagen[i],pokemon_habilidad1[i],pokemon_habilidad2[i],pokemon_ps[i],pokemon_ataque[i],pokemon_defensa[i],pokemon_atqespecial[i],pokemon_defespecial[i],pokemon_velocidad[i],pokemon_tipo1[i],pokemon_tipo2[i])
            create_poke(conn, poke)


if __name__ == '__main__': 
    question = input("Create SQL database? [Y / N]").lower()
    if question == "y":
        conexion = sqlite3.connect("base_datos_sql")
        cursor = conexion.cursor()
        cursor.execute("CREATE TABLE pokemones (nombre VARCHAR(30), imagen VARCHAR(100), habilidad1 VARCHAR(30), habilidad2 VARCHAR(30), ps INTEGER, ataque INTEGER,defensa INTEGER,atqespecial INTEGER,defespecial INTEGER,velocidad INTEGER, tipo1 VARCHAR(30),tipo2 VARCHAR(30))")
        get_pokemons()
