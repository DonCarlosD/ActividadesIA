# Evaluacion Redes Neuronales Mediapipe

Nombre: Carlos Daniel Ochoa Mejia 

##### Modelar una red neuronal que pueda identificar emociones a travez de los valores obtenidos de los landmarks que genera mediapipe

- Definir el tipo de red reuronal y describir cada una de sus partes.
    - R= Para este ejemplo se usara una MLP debido a que los lanmark son valores numericos en este caso las coordenadas.
        -  Para las capa de entrada tenemos las coordenadas de las lanmark que vamos a recibir.
        - Para las capas ocultas es donde se hace todo el procesamiento para poder aprender y detectar que emocion se esta presenciando
        - Capa de salida por ultimo la capa de salida que son el resultado que obtendremos, sera por medio de etiquetas por ejemplo (Feliz, Enojado, Trise. etc.)

- Definir los patrones a utilizar.
    - Los patrones a utilizar son los siguientes
        - Las entradas que son las coordenadas de los lanmarks 
        - Las salidas que seria la identificacion de las emociones por medio de etiquetas 
- Definir la funcion de activacion, es necesaria para este problema.
    - Para las capas ocutas se usara Relu
    - Para la salida se estara usando Softmax 
- Definir el numero maximo de entradas.
    - para este caso como se quieren detectar las emociones, principalmente para ello los lanmarks  que usaremos son Face Mesh: 468 landmarks × 3 coordenadas = 1,404 entradas.
- ¿Que valores a la salida de la red se podrian esperar?
    - Un vector de probabilidades donde: 
        - Cada neurona representa una emoción (ejemplo:[ 0.02,0.85,0.1,...,0.03 ]).
        - La suma de todos los valores es 1.
        - La emoción predicha es la neurona con mayor probabilidad.
- ¿Cuales son los valores maximos que puede tener el bias?
    - para este caso el bias espera tener valores  arriba de 70% para tener mas efectividad
