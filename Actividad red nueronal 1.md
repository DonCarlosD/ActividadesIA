# modelar una red neuronal que pueda jugar al 5 en línea sin gravedad en un tablero 20x20
## Definición de red neuronal
Se usará una red neuronal sigmoide para poder acercarnos más al valor 1 y así obtener una respuesta lo más optima posible.
La red neuronal contendra las siguientes partes....

## Patrones a utilizar

los patrones de diseño se esperan recibir en el data set las coordenadas disponibles, así como todos los movimientos que se hicieron para ganar que casilla se colocó primero y donde, como reacciono el enemigo y donde la coloco y como respondimos nosotros para intentar ganar y así captar todas las estrategias posibles para lograr ganar

## Función de activación para este problema

Para este problema la función de activación sera de tipo sigmoide con el objetivo de tener dos salidas para poder escoger las coordenadas donde la IA podrá interactuar

## Maximo de entradas
Al ser este un tablero de 20x20 tenemos largo y ancho, así como el estatus de la casilla si está ya se encuentra ocupada o no, así como si la casilla ocupada es nuestra o del enemigo, de esta manera definimos el número de entradas como 4, donde las dos primeras serán las coordenadas de las casillas y si estas en encuentran disponibles y si es nuestra ficha o no

## Valores de salida se esperan 
Los valores de salida que se esperaría de la red neuronal son 2 valores que serían las coordenadas de la posición de la ficha que se va a colocar

## Valores Maximos del bias




