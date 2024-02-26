import socket
import tkinter as tk
from tkinter import StringVar, Toplevel
from tkinter import ttk
import threading
from tkinter import simpledialog

"""
    ProyEsp1 juego_multijugador
    
                Juan Enrique Ayala Gaspar
                Gaspar Alonso Cardós Uc

    Juego de preguntas y respuestas multijugador utilizando sockets con conexión TCP 
    e hilos para manejar las conexiones de los clientes.
    El servidor envia las preguntas y cada jugador tiene 15 segundos para responder.
 """



root = tk.Tk()
root.title("Kahoot Juan Ayala - Gaspar Cardós")
root.geometry('500x500')

frame = tk.Frame(root, padx=10, pady=10, bg='#fff')
question_label = tk.Label(frame, height=5, width=28, bg='grey', fg="#fff",
                          font=('Verdana', 20), wraplength=500)

v1 = StringVar(frame)
v2 = StringVar(frame)
v3 = StringVar(frame)
v4 = StringVar(frame)


option1 = tk.Radiobutton(frame, bg="#fff", variable=v1, font=('Verdana', 20), command=lambda: send_option1())
option2 = tk.Radiobutton(frame, bg="#fff", variable=v2, font=('Verdana', 20), command=lambda: send_option2())
option3 = tk.Radiobutton(frame, bg="#fff", variable=v3, font=('Verdana', 20), command=lambda: send_option3())
option4 = tk.Radiobutton(frame, bg="#fff", variable=v4, font=('Verdana', 20), command=lambda: send_option4())

# Funciones para enviar opciones específicas cuando se hace clic en los botones
def send_option1():
    global response
    response="1"
    client_socket.send(response.encode())

def send_option2():
    global response
    response="2"
    client_socket.send(response.encode())

def send_option3():
    global response
    response="3"
    client_socket.send(response.encode())

def send_option4():
    global response
    response="4"
    client_socket.send(response.encode())

# Asociar las funciones de envío a cada botón de opción
option1.config(command=send_option1)
option2.config(command=send_option2)
option3.config(command=send_option3)
option4.config(command=send_option4)


progress_bar = ttk.Progressbar(frame, length=400, mode='determinate', maximum=15)

frame.pack(fill="both", expand="true")
question_label.grid(row=0, column=0)

option1.grid(sticky='W', row=1, column=0)
option2.grid(sticky='W', row=2, column=0)
option3.grid(sticky='W', row=3, column=0)
option4.grid(sticky='W', row=4, column=0)

progress_bar.grid(row=5, column=0, pady=10)

index = 0
correct = 0
time_left = 15  # Ajustar el tiempo límite a 15 segundos

response= None

# Función para manejar la entrada del usuario
def handle_user_input():
    global response
    response = input("Ingrese el número de la respuesta: ")


# Función para desactivar los botones de opción
def disableButtons(state):
    option1['state'] = state
    option2['state'] = state
    option3['state'] = state
    option4['state'] = state

# Configuración del servidor
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Inicializa el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

#nombre = input("Ingrese su nombre: ")

nombre = simpledialog.askstring("Ingresar nombre", "Por favor, ingresa tu nombre:")
client_socket.send(nombre.encode())

try:
    j=0
    while True:
        
        # Recibe la pregunta del servidor
        question_data = client_socket.recv(1024).decode()
        #print(question_data)
        
        if question_data == "FIN":
            print("No hay más preguntas disponibles. ¡Juego terminado!")
            client_socket.send("para que no se concatene".encode())
            break  # Sale del bucle si no hay más preguntas disponibles
        
        root.update() 
        question, *options = question_data.split("|")
        print(f"Pregunta: {question}")
        
        question_label['text'] = question
        
        print("Opciones:")
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")
        
        disableButtons('normal')
        opts = options
        option1['text'] = options[0]
        option2['text'] = options[1]
        option3['text'] = options[2]
        option4['text'] = options[3]
        v1.set(opts[0])
        v2.set(opts[1])
        v3.set(opts[2])
        v4.set(opts[3])

        # Detener completamente la barra de progreso y restablecer su valor a cero
        progress_bar.stop()
        progress_bar['value'] = 0

        # Iniciar la barra de progreso con un nuevo temporizador de 15 segundos
        progress_bar.start(15000)  # Ajustar la velocidad de la barra de progreso a 15 segundos (15000 milisegundos)
        time_left = 15  # Restablecer el tiempo límite a 15 segundos
        
        # Envía la respuesta al servidor
        # Ejecutar la función handle_user_input en un hilo separado
       
       
        #user_input_thread = threading.Thread(target=handle_user_input)
        #user_input_thread.start()
        
        while time_left > 0:
            if response:
                #print("nsjdn ")
                break
            time_left -= 1
            progress_bar['value'] = 15 - time_left  # Actualizar el valor de la barra de progreso
            root.update()  # Actualizar la interfaz gráfica para que se muestre el progreso
            
            # Esperar 1 segundo antes de actualizar nuevamente
            root.after(1000)

        
        # Si se agota el tiempo, marcar como incorrecta y pasar a la siguiente pregunta
        if response is None and time_left == 0 and j<=9 :
            response="6"
            client_socket.send(response.encode())
        
        
        #print(question_data)
        response=None
        j+=1

            
        

    
  

    # Recibe el número de respuestas correctas del servidor
    correct_answers = client_socket.recv(1024).decode()
    print(f"¡Juego terminado! Has acertado {correct_answers} preguntas.")
    
finally:
    # Cierre del socket del cliente
    
    client_socket.close()