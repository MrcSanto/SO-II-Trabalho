from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import random

class SimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Alocação de Blocos Lógicos")
        
        # Obter as dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Criação da barra lateral
        self.setup_sidebar()

        # Área principal para exibir o estado do disco (imagem)
        self.setup_canvas()

    def setup_sidebar(self):
        # Frame para a barra lateral
        sidebar = tk.Frame(self.root, width=300, bg="lightgray")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Widgets na barra lateral
        tk.Label(sidebar, text="Tamanho do Disco (blocos):", bg="lightgray").pack(pady=5, anchor="w", padx=10)
        self.disk_size_entry = tk.Entry(sidebar)
        self.disk_size_entry.pack(pady=5, anchor="w", padx=10)
        tk.Label(sidebar, text="Máximo de blocos: 512", bg="lightgray", fg="red").pack(pady=(0, 5), anchor="w", padx=10)
                
        tk.Label(sidebar, text="Tamanho do Arquivo (blocos):", bg="lightgray").pack(pady=5, anchor="w", padx=10)
        self.file_size_entry = tk.Entry(sidebar)
        self.file_size_entry.pack(pady=5, anchor="w", padx=10)


        tk.Label(sidebar, text="Métodos de Alocação:", bg="lightgray").pack(pady=5, anchor="w", padx=10)            
        self.allocation_type = tk.StringVar(value="Contígua")
        tk.Radiobutton(sidebar, text="Contígua", variable=self.allocation_type, value="Contígua", bg="lightgray").pack(pady=5, anchor="w", padx=10)
        tk.Radiobutton(sidebar, text="Encadeada", variable=self.allocation_type, value="Encadeada", bg="lightgray").pack(pady=5, anchor="w", padx=10)
        tk.Radiobutton(sidebar, text="Indexada", variable=self.allocation_type, value="Indexada", bg="lightgray").pack(pady=5, anchor="w", padx=10)

        # Botão único para criar o disco e visualizar
        tk.Button(sidebar, text="Criar Disco", command=self.show_disk).pack(side=tk.BOTTOM, pady=10, anchor="s")

    def setup_canvas(self):
        # Frame para o Canvas que vai receber a barra de rolagem
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Canvas para exibir a imagem
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de rolagem vertical
        self.scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Vincular o canvas à barra de rolagem
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Inicialmente, o canvas estará vazio, sem nenhuma imagem
        self.tk_image = None

    def generate_disk_image(self, num_blocks):
        # Definir tamanho dos blocos, margens e blocos por linha dependendo do número de blocos
        if num_blocks < 50:
            block_size = 80
            margin = 100
            blocks_per_row = 5
        elif num_blocks >= 50 and num_blocks < 100:
            block_size = 70
            margin = 80
            blocks_per_row = 6
        elif num_blocks >= 100 and num_blocks < 200:
            block_size = 60
            margin = 60
            blocks_per_row = 8
        elif num_blocks >= 200 and num_blocks < 400:
            block_size = 50
            margin = 50
            blocks_per_row = 10
        elif num_blocks >= 400 and num_blocks < 650:
            block_size = 40
            margin = 40
            blocks_per_row = 12
        else:
            block_size = 30
            margin = 30
            blocks_per_row = 15

        try:
            rows = (num_blocks + blocks_per_row - 1) // blocks_per_row
            width = blocks_per_row * (block_size + margin) + margin  # Largura total
            height = rows * (block_size + margin) + margin  # Altura total

            # Criar a imagem
            image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(image)

            # Configurar fonte para os números (ajustar tamanho conforme necessário)
            try:
                font = ImageFont.truetype("arial.ttf", size=14)  # Tente usar uma fonte específica
            except IOError:
                font = ImageFont.load_default()  # Fallback para fonte padrão

            # Gerar uma lista de índices aleatórios para pintar de preto
            num_black_blocks = max(1, num_blocks // 10)  # 10% dos blocos serão pretos
            black_blocks = random.sample(range(num_blocks), num_black_blocks)

            # Desenhar os blocos e adicionar os números de identificação
            for i in range(num_blocks):
                row, col = divmod(i, blocks_per_row)
                x0 = col * (block_size + margin) + margin
                y0 = row * (block_size + margin) + margin
                x1 = x0 + block_size
                y1 = y0 + block_size

                # Definir a cor do bloco
                fill_color = "black" if i in black_blocks else "skyblue"

                # Desenhar o bloco
                draw.rectangle([x0, y0, x1, y1], fill=fill_color, outline="black")

                # Adicionar o número de identificação ao lado direito do bloco
                text_x = x1 + 10  # Posição x (10 pixels à direita do bloco)
                text_y = y0 + (block_size // 2) - 7  # Centralizar o texto verticalmente
                draw.text((text_x, text_y), str(i), fill="black", font=font)

            # Salvar a imagem no atributo para exibir no Canvas
            self.tk_image = ImageTk.PhotoImage(image)

            # Limpar o Canvas antes de desenhar
            self.canvas.delete("all")

            # Calcular a posição para centralizar a imagem no Canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            x_center = (canvas_width - width) // 2
            y_center = (canvas_height - height) // 2

            # Exibir a imagem centralizada no Canvas
            self.canvas.create_image(x_center, y_center, anchor=tk.NW, image=self.tk_image)

            # Atualizar a barra de rolagem
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar a imagem: {e}")
            
    def show_disk(self):
        if self.disk_size_entry.get() == '':
            return

        try:
            num_blocks = int(self.disk_size_entry.get())
            if num_blocks <= 0 or num_blocks >= 512:
                raise ValueError("O número de blocos deve ser maior que zero e menor que 512.")
            self.generate_disk_image(num_blocks)
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

if __name__ == "__main__":
    root = tk.Tk()  
    app = SimulatorApp(root)    
    root.mainloop() 
