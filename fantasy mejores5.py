import requests
BASE_URL = "https://fantasy.premierleague.com/api"
# Obtener información de jugadores y equipos
datos = requests.get(f"{BASE_URL}/bootstrap-static/").json()
jugadores = datos["elements"]
equipos = {equipo["id"]: equipo["name"] for equipo in datos["teams"]}
# Crear diccionario para encontrar jugadores por ID
jugadores_por_id = {
    jugador["id"]: jugador
    for jugador in jugadores
}
# Obtener las jornadas que ya terminaron
jornadas = [
    jornada for jornada in datos["events"]
    if jornada["finished"]
]
print("======================================")
print(" TOP 5 JUGADORES DE LA PREMIER LEAGUE")
print("======================================")
for jornada in jornadas:
    numero = jornada["id"]
    # Obtener puntos de todos los jugadores de esa jornada
    respuesta = requests.get(
        f"{BASE_URL}/event/{numero}/live/"
    ).json()
    resultados = []
    for jugador in respuesta["elements"]:
        puntos = jugador["stats"]["total_points"]
        jugador_id = jugador["id"]
        informacion = jugadores_por_id[jugador_id]
        nombre = informacion["web_name"]
        equipo = equipos[informacion["team"]]
        resultados.append({
            "nombre": nombre,
            "equipo": equipo,
            "puntos": puntos
        })
    # Ordenar de mayor a menor
    resultados.sort(
        key=lambda x: x["puntos"],
        reverse=True
    )
    # Tomar los 5 primeros
    top5 = resultados[:5]
    print(f"\nJORNADA {numero}")
    print("----------------------------")
    for posicion, jugador in enumerate(top5, start=1):
        print(
            f"{posicion}. {jugador['nombre']} "
            f"({jugador['equipo']}) - "
            f"{jugador['puntos']} puntos"
        )