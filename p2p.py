import tkinter as tk
from tkinter import ttk
from tkinter import font
import time

global message
message = "Olá"

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Node:
    def __init__(self, host):
        self.host = host
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def send_message(self, dest_node, file):
        global message
        if(self.host != dest_node.host):
            message.set(f"Compartilhando '{file.name}' com {dest_node.host}.") 
            print(f"Enviando pedaço do arquivo '{file.name}' do nó {self.host} para o nó {dest_node.host}.")
            dest_node.receive_file(file)
            

    def receive_file(self, file):
        self.files.append(file)


class P2PNetworkGUI:
    global message
    def __init__(self, window):
        self.window = window
        self.nodes = []
        self.node_coords = {}
        self.node_radius = 20
        self.canvas_width = 600
        self.canvas_height = 300

        # Criar o Nó 1 com o arquivo inicial
        node1 = Node("Nó 1")
        file1 = File("Arquivo Inicial", 300)
        node1.add_file(file1)
        self.nodes.append(node1)

        # Criar os outros nós
        node2 = Node("Nó 2")
        node3 = Node("Nó 3")
        node4 = Node("Nó 4")
        node5 = Node("Nó 5")
        self.nodes.extend([node2, node3, node4, node5])

        # Adicionar arquivos aos nós restantes
        file2 = File("Arquivo 2", 200)
        file3 = File("Arquivo 3", 150)
        file4 = File("Arquivo 4", 250)
        file5 = File("Arquivo 5", 180)
        node2.add_file(file2)
        node3.add_file(file3)
        node4.add_file(file4)
        node5.add_file(file5)

        self.create_gui()

    def create_gui(self):
        self.window.title("Rede P2P")
        self.window.geometry("800x600")

        # Frame para seleção de nós
        node_frame = tk.Frame(self.window)
        node_frame.pack(pady=10)

        # Seleção de nó de destino
        dest_label = tk.Label(node_frame, text="Solicita:")
        dest_label.grid(row=0, column=0, padx=5)

        self.dest_combobox = ttk.Combobox(node_frame, values=[node.host for node in self.nodes])
        self.dest_combobox.grid(row=0, column=1, padx=5)
        self.dest_combobox.bind("<<ComboboxSelected>>", self.handle_dest_selection)

        # Frame para seleção de arquivo
        file_frame = tk.Frame(self.window)
        file_frame.pack(pady=10)

        file_label = tk.Label(file_frame, text="Arquivo:")
        file_label.grid(row=0, column=0, padx=4)

        self.file_combobox = ttk.Combobox(file_frame, values=[file.name for file in self.nodes[0].files])
        self.file_combobox.grid(row=0, column=1, padx=5)

        # Botão de envio de pedaço de arquivo
        send_button = tk.Button(self.window, text="Solicitar Arquivo na Rede", command=self.send_piece)
        send_button.pack(anchor="center", pady=20)

        # Frame para visualização dos nós
        canvas_frame = tk.Frame(self.window, width=self.canvas_width, height=self.canvas_height)
        canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Posicionamento dos nós na tela
        self.node_coords[self.nodes[0]] = (100, 200)
        self.node_coords[self.nodes[1]] = (200, 100)
        self.node_coords[self.nodes[2]] = (300, 150)
        self.node_coords[self.nodes[3]] = (400, 100)
        self.node_coords[self.nodes[4]] = (500, 200)

        # Mensagem de nós enviando pedaços do arquivo
        global message
        message = tk.StringVar()
        fonte = font.Font(family="Arial", size=15)
        label_msg = tk.Label(self.window, textvariable=message, font=fonte)
        label_msg.pack(pady=10)

        # Executar a janela principal
        self.update_node_display_green()
        # self.update_node_display_blue()
        self.window.mainloop()

    def handle_dest_selection(self, event):
        self.selected_dest_node = self.dest_combobox.get()

    def send_piece(self):
        dest_host = self.selected_dest_node
        file_name = self.file_combobox.get()

        dest_node = None
        file = None

        # Encontrar o nó de destino
        for node in self.nodes:
            if node.host == dest_host:
                dest_node = node
                break

        # Encontrar o arquivo
        for file_obj in self.nodes[0].files:
            if file_obj.name == file_name:
                file = file_obj
                break

        # Verificar se o nó de destino e o arquivo foram encontrados
        if dest_node is None or file is None:
            return

        # Verificar se o nó de destino já possui o arquivo
        if file not in dest_node.files:
            # Realizar a transferência do arquivo completo
            dest_node.receive_file(file)
        else:
            # O nó de destino já possui o arquivo
            print(f"O nó {dest_node.host} já possui o arquivo '{file.name}'.")

        # Realizar a transferência do pedaço do arquivo por todos os nós que possuem o arquivo
        for node in self.nodes:
            if file in node.files:
                node.send_message(dest_node, file)

        # Desenhar as setas
        self.draw_arrows(dest_node)

    def update_node_display_green(self):
        self.canvas.delete("all")

        for node, coords in self.node_coords.items():
            x, y = coords
            color = "green" if any(file in node.files for file in self.nodes[0].files) else "red"
            self.canvas.create_oval(x, y, x + self.node_radius * 2, y + self.node_radius * 2, fill=color)
            self.canvas.create_text(x + self.node_radius, y + self.node_radius, text=node.host, tags="node_text")

        self.window.update()

    # def update_node_display_blue(self):
    #     self.canvas.delete("all")

    #     for node, coords in self.node_coords.items():
    #         x, y = coords
    #         color = "blue" 
    #         self.canvas.create_oval(x, y, x + self.node_radius * 2, y + self.node_radius * 2, fill=color)
    #         self.canvas.create_text(x + self.node_radius, y + self.node_radius, text=node.host, tags="node_text")

    #     self.window.update()

    def draw_arrows(self, dest_node):
        dest_coords = self.node_coords[dest_node]

        for node, coords in self.node_coords.items():
            if node != dest_node and any(file in node.files for file in dest_node.files):
                origin_coords = coords
                self.draw_arrow(origin_coords, dest_coords)
        
        self.update_node_display_green()

    def draw_arrow(self, origin_coords, dest_coords):
        x1, y1 = origin_coords[0] + self.node_radius, origin_coords[1] + self.node_radius
        x2, y2 = dest_coords[0] + self.node_radius, dest_coords[1] + self.node_radius
        arrow = self.canvas.create_line(x1, y1, x2, y2, arrow="last", tags="arrow")

        step = 0
        while step <= 1:
            x = x1 + (x2 - x1) * step
            y = y1 + (y2 - y1) * step
            self.canvas.coords(arrow, x1, y1, x, y)
            self.window.update()
            time.sleep(0.04) 
            step += 0.05

        self.canvas.delete(arrow)


if __name__ == "__main__":
    window = tk.Tk()
    p2p_network = P2PNetworkGUI(window)
