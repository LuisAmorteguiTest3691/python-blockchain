import tkinter as tk
from tkinter import messagebox
import requests
import networkx as nx
import matplotlib.pyplot as plt


class SupplyChainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de la Cadena de Suministro")
        self.root.geometry("400x300")  # Tamaño de la ventana (más amplio)
        self.root.configure(bg="#f0f0f0")  # Color de fondo

        # Marco para el formulario
        frame = tk.Frame(root, bg="#ffffff", bd=2, relief="raised")
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Título
        title = tk.Label(frame, text="Gestión de Blockchain", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333")
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiquetas y campos de entrada
        tk.Label(frame, text="Remitente:", bg="#ffffff", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5)
        self.sender = tk.Entry(frame, font=("Arial", 12))
        self.sender.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Destinatario:", bg="#ffffff", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5)
        self.recipient = tk.Entry(frame, font=("Arial", 12))
        self.recipient.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame, text="Producto:", bg="#ffffff", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=5)
        self.product = tk.Entry(frame, font=("Arial", 12))
        self.product.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame, text="Cantidad:", bg="#ffffff", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=5)
        self.quantity = tk.Entry(frame, font=("Arial", 12))
        self.quantity.grid(row=4, column=1, padx=10, pady=5)

        # Botones con estilos
        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "activebackground": "#367c39"}

        tk.Button(frame, text="Agregar Transacción", command=self.add_transaction, **button_style).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Minar Bloque", command=self.mine_block, **button_style).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Ver Cadena", command=self.view_chain, **button_style).grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Visualizar Grafo", command=self.visualize_graph, **button_style).grid(row=8, column=0, columnspan=2, pady=5)

    def add_transaction(self):
        data = {
            'sender': self.sender.get(),
            'recipient': self.recipient.get(),
            'product': self.product.get(),
            'quantity': self.quantity.get(),
        }
        response = requests.post("http://127.0.0.1:5000/transactions/new", json=data)
        messagebox.showinfo("Respuesta", response.json().get("message", "Error"))

    def mine_block(self):
        response = requests.get("http://127.0.0.1:5000/mine")
        messagebox.showinfo("Respuesta", response.json().get("message", "Error"))

    def view_chain(self):
        response = requests.get("http://127.0.0.1:5000/chain")
        chain = response.json().get("chain", [])
        messagebox.showinfo("Cadena de Bloques", str(chain))

    def visualize_graph(self):
        response = requests.get("http://127.0.0.1:5000/chain")
        chain = response.json().get("chain", [])

        G = nx.DiGraph()
        for block in chain:
            for txn in block['transactions']:
                G.add_edge(txn['sender'], txn['recipient'], label=f"{txn['product']} ({txn['quantity']})")

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="#77dd77", font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)})
        plt.title("Visualización de la Cadena de Suministro")
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = SupplyChainApp(root)
    root.mainloop()
