from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import random

class AlocationAlgorithms:
    def __init__(self, list_blocks: list[bool]):
        self.list_blocks = list_blocks
    
    def contigua(self, file_size : int) -> bool:
        for i in range(len(self.list_blocks) - file_size + 1):
            # Verifica se há espaço contíguo suficiente
            if all(not self.list_blocks[j] for j in range(i, i + file_size)):
                # Marca os blocos como ocupados
                for j in range(i, i + file_size):
                    self.list_blocks[j] = True
            return True
        return False
    
    def encadeada(self, file_size: int) -> list[int]:
        allocated_blocks = []
        for i, block in enumerate(self.list_blocks):
            if not block:  # Bloco livre
                allocated_blocks.append(i)
                self.list_blocks[i] = True  # Marca o bloco como ocupado
                if len(allocated_blocks) == file_size:
                    return allocated_blocks
        # Não foi possível alocar o arquivo
        for i in allocated_blocks:  # Reverte a alocação parcial
            self.list_blocks[i] = False
        return []

    def indexada(self, file_size: int) -> tuple[int, list[int]]:
        index_block = -1
        data_blocks = []
        
        # Encontrar o bloco de índice
        for i, block in enumerate(self.list_blocks):
            if not block:
                index_block = i
                self.list_blocks[i] = True  # Marca o bloco de índice como ocupado
                break

        if index_block == -1:
            return ()  # Não há bloco de índice disponível

        # Alocar blocos para os dados
        for i, block in enumerate(self.list_blocks):
            if not block and len(data_blocks) < file_size:
                data_blocks.append(i)
                self.list_blocks[i] = True

        if len(data_blocks) < file_size:
            # Reverter alocações se não houver blocos suficientes
            self.list_blocks[index_block] = False
            for i in data_blocks:
                self.list_blocks[i] = False
            return ()

        return index_block, data_blocks

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
        tk.Button(sidebar, text="Criar Arquivo", command='').pack(side=tk.BOTTOM, pady=10, anchor="s")
        tk.Button(sidebar, text="Limpar", command='').pack(side=tk.BOTTOM, pady=10, anchor="s")

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

            # Configurar fonte para os números e o texto
            try:
                font = ImageFont.truetype("arial.ttf", size=14)
            except IOError:
                font = ImageFont.load_default()

            # Lista para guardar o status de cada bloco
            block_status = [False] * num_blocks  # Inicialmente, todos os blocos estão livres

            # Inicializar lista para acompanhar os blocos usados
            used_blocks = set()

            # Aumentar o número de blocos alocados para 30% ou mais
            total_files = num_blocks // 5  # Alocar aproximadamente 20% a 30% dos blocos para arquivos

            for _ in range(total_files):
                start_block = random.randint(0, num_blocks - 1)

                # Ignorar se o bloco inicial já está ocupado
                if start_block in used_blocks:
                    continue

                # Determinar tamanho do arquivo (3 a 10 blocos)
                file_size = random.randint(3, 10)

                # Verificar se o arquivo pode ser alocado sem ultrapassar os limites
                allocated_blocks = []
                for i in range(file_size):
                    current_block = start_block + i

                    # Quebrar a linha caso ultrapasse o limite da linha atual
                    if current_block % blocks_per_row < start_block % blocks_per_row:
                        break

                    # Adicionar o bloco se ainda não estiver ocupado
                    if current_block < num_blocks and current_block not in used_blocks:
                        allocated_blocks.append(current_block)
                    else:
                        break

                # Se o arquivo couber nos blocos selecionados
                if len(allocated_blocks) == file_size:
                    used_blocks.update(allocated_blocks)
                    for block in allocated_blocks:
                        block_status[block] = True  # Marcar os blocos como ocupados

            # Desenhar os blocos na imagem
            for i in range(num_blocks):
                row, col = divmod(i, blocks_per_row)
                x0 = col * (block_size + margin) + margin
                y0 = row * (block_size + margin) + margin
                x1 = x0 + block_size
                y1 = y0 + block_size

                # Cor do bloco
                fill_color = "firebrick" if block_status[i] else "skyblue"
                text = "Alocado" if block_status[i] else "Livre"

                # Desenhar o bloco
                draw.rectangle([x0, y0, x1, y1], fill=fill_color, outline="black")

                # Adicionar número identificador no topo do bloco
                block_id_text = str(i + 1)  # Número identificador (i + 1 para começar de 1)
                block_id_bbox = draw.textbbox((0, 0), block_id_text, font=font)  # Pega a caixa delimitadora do texto
                block_id_width = block_id_bbox[2] - block_id_bbox[0]
                block_id_x = x0 + (block_size - block_id_width) // 2  # Centralizar horizontalmente
                block_id_y = y0 + 5  # Colocar no topo do bloco

                draw.text((block_id_x, block_id_y), block_id_text, fill="black", font=font)

                # Adicionar o status (Livre ou Alocado) centralizado
                text_bbox = draw.textbbox((0, 0), text, font=font)  # Pega a caixa delimitadora do texto
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = x0 + (block_size - text_width) // 2  # Centralizar horizontalmente
                text_y = y0 + (block_size - text_height) // 2  # Centralizar verticalmente

                draw.text((text_x, text_y), text, fill="black", font=font)

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

            # Retornar a lista com o status dos blocos
            return block_status

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar a imagem: {e}")

    def show_disk(self):
        if self.disk_size_entry.get() == '':
            messagebox.showwarning("Atenção", "Informe o tamanho do disco.")
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
