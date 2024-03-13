# Implementación de Juego Multijugador de Preguntas y Respuestas con Tkinter y Sockets TCP

## Diseño e Implementación:

### Objetivo:
El objetivo de la aplicación es crear un juego multijugador de preguntas y respuestas utilizando la biblioteca Tkinter de Python para la interfaz gráfica y sockets TCP para la comunicación entre el cliente y el servidor.

### Componentes:

- **Cliente:** El cliente es una aplicación de escritorio que muestra preguntas y opciones de respuesta al usuario. Utiliza una GUI creada con Tkinter y se comunica con el servidor a través de sockets TCP para enviar respuestas y recibir nuevas preguntas.
  
- **Servidor:** El servidor es responsable de gestionar múltiples conexiones de clientes. Envía preguntas a los clientes, recibe respuestas y lleva un seguimiento de los puntajes de los jugadores.

## Funcionamiento:

### Cliente:
- El cliente muestra una interfaz gráfica que incluye la pregunta actual y las opciones de respuesta.
- El usuario selecciona una opción y la envía al servidor haciendo clic en el botón correspondiente.
- El cliente actualiza la pregunta y las opciones cuando recibe nuevos datos del servidor.
- Una barra de progreso indica el tiempo restante para responder a la pregunta.
- Si el tiempo se agota, se envía una respuesta predeterminada al servidor.

### Servidor:
- El servidor espera conexiones entrantes de clientes y crea un hilo para manejar cada conexión.
- Envía preguntas a los clientes y recibe respuestas.
- Lleva un registro de los puntajes de los jugadores y los actualiza después de cada pregunta.
- Cuando se completan todas las preguntas, envía el puntaje final de cada jugador.

## Interfaz Gráfica:

- La interfaz gráfica del cliente utiliza etiquetas, botones de opción y una barra de progreso para mostrar la pregunta y las opciones, y para indicar el tiempo restante.
- La interfaz gráfica del servidor muestra los puntajes de los jugadores en una tabla utilizando un widget Treeview de Tkinter.

## Funcionamiento:

1. El servidor se inicia y espera conexiones de clientes en un bucle infinito.
2. Cuando un cliente se conecta, el servidor crea un hilo para manejar la conexión.
3. El servidor envía preguntas a los clientes y recibe respuestas.
4. Los clientes muestran las preguntas y opciones al usuario.
5. Los usuarios seleccionan una opción y la envían al servidor.
6. El servidor lleva un seguimiento de los puntajes de los jugadores.
7. Después de completar todas las preguntas, el servidor envía los puntajes finales a los clientes y cierra las conexiones.

## Conclusión:
El juego multijugador de preguntas y respuestas implementado con Tkinter y sockets TCP proporciona una experiencia interactiva y divertida para múltiples jugadores. La combinación de una interfaz gráfica amigable con la comunicación en tiempo real entre el cliente y el servidor permite una experiencia de juego fluida y envolvente. Además, el uso de hilos en el servidor garantiza que pueda manejar múltiples conexiones de clientes de manera eficiente, lo que es crucial para un juego multijugador.
