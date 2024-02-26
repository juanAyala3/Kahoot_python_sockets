import tkinter as tk
from tkinter import ttk

# Assuming jugadores is your dictionary
jugadores = {"Player1": 5, "Player2": 3, "Player3": 7}

root = tk.Tk()
root.title("Jugadores Scores")

tree = ttk.Treeview(root, columns=('Player', 'Score'), show='headings')
tree.heading('Player', text='Player')
tree.heading('Score', text='Score')

for player, score in jugadores.items():
    tree.insert('', 'end', values=(player, score))

tree.pack()

root.mainloop()