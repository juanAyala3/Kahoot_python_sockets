import socket
import threading
import tkinter as tk
from tkinter import ttk

"""
    ProyEsp1 juego_multijugador
    
                Juan Enrique Ayala Gaspar
                Gaspar Alonso Cardós Uc

    Juego de preguntas y respuestas multijugador utilizando sockets con conexión TCP 
    e hilos para manejar las conexiones de los clientes.
    El servidor envia las preguntas y cada jugador tiene 15 segundos para responder.
"""


# Lista de preguntas sobre países y capitales más difíciles
questions = [
    "¿Cuál es la capital de Francia?",
    "¿Cuál es la capital de Italia?",
    "¿Cuál es la capital de Japón?",
    "¿Cuál es la capital de Canadá?",
    "¿Cuál es la capital de Brasil?",
    "¿Cuál es la capital de Australia?",
    "¿Cuál es la capital de Rusia?",
    "¿Cuál es la capital de China?",
    "¿Cuál es la capital de España?",
    "¿Cuál es la capital de Alemania?"
]

# Opciones para cada pregunta, con la última opción como la respuesta correcta
options = [
    ['París', 'Londres', 'Madrid', 'Bruselas', 'París', ''],  # Respuesta: París
    ['Londres','Roma',  'París', 'Berlín', 'Roma', ''],  # Respuesta: Roma
    ['Pekín', 'Seúl', 'Taipei', 'Tokio', 'Tokio', ''],  # Respuesta: Tokio
    ['Ottawa', 'Toronto', 'Vancouver', 'Montreal', 'Ottawa', ''],  # Respuesta: Ottawa
    ['Sao Paulo', 'Bogotá','Brasilia',  'Río de Janeiro', 'Brasilia', ''],  # Respuesta: Brasilia
    ['Canberra', 'Wellington', 'Sídney', 'Melbourne', 'Canberra', ''],  # Respuesta: Canberra
    ['San Petersburgo','CDMX', 'Moscú', 'Novosibirsk', 'Moscú', ''],  # Respuesta: Moscú
    ['Shanghái', 'Bogotá', 'Pekín', 'Hong Kong', 'Pekín', ''],  # Respuesta: Pekín
    ['Madrid', 'Barcelona', 'Valencia', 'Bilbao', 'Madrid', ''],  # Respuesta: Madrid
    ['Mérida', 'Múnich', 'Berlín', 'Fráncfort del Meno', 'Berlín', '']  # Respuesta: Berlín
]


# Función para manejar la conexión con un cliente
def handle_client(client_socket):
    global jugadores
    correct_answers=0
    nombre_local=nombre
    try:
        for i in range(len(questions)):
            # Envía la pregunta actual al cliente
            question_data = f"{questions[i]}|{'|'.join(options[i])}"
            #print(question_data)
            client_socket.send(question_data.encode())
            # Espera la respuesta del cliente
            response = client_socket.recv(1024).decode().strip()
            int_response = int(response) - 1
            print(f"Respuesta del cliente : {response}")
            # Verifica si la respuesta es correcta
            if options[i][int_response] == options[i][4]:
                correct_answers += 1
                jugadores[nombre_local]=correct_answers
                #print(jugadores[nombre_local])
        # Envía una señal de finalización al cliente
           # print(jugadores.keys())
            #print(jugadores.values()
            
            #se envian los puntajes y nombres de los jugadores al cliente
            client_socket.send(str(jugadores).encode())
            client_socket.recv(1024).decode()
            
        client_socket.send("FIN".encode())
        
        

    finally:
        # Envía el número de respuestas correctas al cliente
        client_socket.recv(1024).decode().strip()
        client_socket.send(str(correct_answers).encode())
        client_socket.close()

#hilo para ir esperando conecciones entrantes de clientes
def acepta_cliente():
    global nombre
    indice=0
    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"[*] Conexión aceptada de {client_addr[0]}:{client_addr[1]}")
        nombre=client_socket.recv(1024).decode()
        jugadores[nombre]=0
        print(f"[*] Nombre de los jugadores: {jugadores.keys()}")
        indice+=1
        # Inicia un nuevo hilo para manejar la conexión con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


# Configuración del servidor

#el servidor escuchará en todas las interfaces de red disponibles en el sistema.
SERVER_HOST = '0.0.0.0'  
SERVER_PORT = 12345

# Inicializa el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
#se aceptaran 5 conexiones y si hay mas las pondra en espera
server_socket.listen(5)

jugadores={}

print(f"[*] Servidor escuchando en {SERVER_HOST}:{SERVER_PORT}")

nombre=""

acepta_handler = threading.Thread(target=acepta_cliente)
acepta_handler.start()


def actualizar_tabla():
    tree.delete(*tree.get_children())  # Limpiar la tabla
    for player, score in jugadores.items():
        tree.insert('', 'end', values=(player, score))
    # Programar la próxima actualización después de 5 segundos
    root.after(2000, actualizar_tabla)


root = tk.Tk()
root.title("Ranking servidor")

tree = ttk.Treeview(root, columns=('Jugador', 'Puntaje'), show='headings')
tree.heading('Jugador', text='Jugador')
tree.heading('Puntaje', text='Puntaje')
tree.pack()

actualizar_tabla()  # Actualizar la tabla inicialmente

root.mainloop()