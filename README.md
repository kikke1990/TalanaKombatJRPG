# TalanaKombatJRPG

Talana Kombat es un juego donde 2 personajes se enfrentan hasta la muerte. Cada personaje tiene 2
golpes especiales que se ejecutan con una combinación de movimientos + 1 botón de golpe.
Los botones que se usan son
(W)Arriba, (S)Abajo, (A)Izquierda, (D)Derecha,
(P)Puño, (K)Patada

Parte atacando el jugador que envió una combinación menor de botones (movimiento + golpes),
en caso de empate, parte el con menos movimientos, si empatan de nuevo, inicia el con menos
golpes, si hay empate de nuevo, inicia el player 1 (total el player 2 siempre es del hermano
chico)

El proyecto se encuentra desarrollado en python con el framework Django y corresponde a un api, la cual recibe los datos en formato Json, los cuales son usados para pbtener funcionalidades desde una base de datos. Tambien se registra el detalle de cada juego y se devuelve su interpretacion en formato JSON.

Para iniciar el proyecto.

1. Clonar el repositorio.
2. Crear un entono virtual ---> Ej: virtualenv venv
3. Activar el entorno virtual --> ../venv/bin/activate
4. Instalar las dependencias del archivo requeriments ---> pip install -r requirements.txt
5. Iniciar el proyecto con python manage.py runserver 127.0.0.1:8000


API /API/talana/kombat
Method POST

![Alt-Text](/APIBrowser.png)
APIBrowser.png

Retorna una lista con la interpretacion de las acciones enviadas desde lso botones.

ejemplo:
 
 se envia:
    {
        "player1": {
            "movimientos": ["SDD","DSD","SA","DSD"],
            "golpes": ["K","P","K","P"]
        },
        "player2": {
            "movimientos": ["DSD","WSAW","ASA","","ASA","SA"],
            "golpes": ["P","K","K","K","P","k"]
        }
    }
    
   se retorna:
    {
    "respuesta": [
        {
            "action": "Arnaldor se mueve hacia la Derecha"
        },
        {
            "action": "Arnaldor se agacha"
        },
        {
            "action": "Arnaldor se mueve hacia la Derecha"
        },
        {
            "action": "Arnaldor da un Puñetazo"
        },
        {
            "action": "Tony se agacha"
        },
        {
            "action": "Tony se mueve hacia la Derecha"
        },
        {
            "action": "Tony se mueve hacia la Derecha"
        },
        {
            "action": "Tony da una Patada"
        },
        {
            "action": "Arnaldor salta"
        },
        {
            "action": "Arnaldor se agacha"
        },
        {
            "action": "Arnaldor se mueve hacia la Izquierda"
        },
        {
            "action": "Arnaldor salta"
        },
        {
            "action": "Arnaldor da una Patada"
        },
        {
            "action": "Tony conecta un Tonuyuken"
        },
        {
            "action": "Arnaldor se mueve hacia la Izquierda"
        },
        {
            "action": "Arnaldor se agacha"
        },
        {
            "action": "Arnaldor se mueve hacia la Izquierda"
        },
        {
            "action": "Arnaldor da una Patada"
        },
        {
            "action": "Tony se agacha"
        },
        {
            "action": "Tony se mueve hacia la Izquierda"
        },
        {
            "action": "Tony da una Patada"
        },
        {
            "action": "Arnaldor da una Patada"
        },
        {
            "action": "Tony conecta un Tonuyuken"
        },
        {
            "action": "Tony win!"
        }
    ]
}
