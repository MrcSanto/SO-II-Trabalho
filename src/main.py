import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

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

        # Variável para armazenar o status dos blocos
        self.block_status = []

        # Variável para armazenar as setas entre os blocos alocados (apenas para alocação encadeada)
        self.arrows = []

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
        tk.Button(sidebar, text="Criar Arquivo", command=self.allocate_file).pack(side=tk.BOTTOM, pady=10, anchor="s")
        tk.Button(sidebar, text="Limpar", command=self.clear_canvas).pack(side=tk.BOTTOM, pady=10, anchor="s")

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
            self.block_size = 80
            self.margin = 100
            self.blocks_per_row = 5
        elif num_blocks >= 50 and num_blocks < 100:
            self.block_size = 70
            self.margin = 80
            self.blocks_per_row = 6
        elif num_blocks >= 100 and num_blocks < 200:
            self.block_size = 60
            self.margin = 60
            self.blocks_per_row = 8
        elif num_blocks >= 200 and num_blocks < 400:
            self.block_size = 50
            self.margin = 50
            self.blocks_per_row = 10
        elif num_blocks >= 400 and num_blocks < 650:
            self.block_size = 40
            self.margin = 40
            self.blocks_per_row = 12
        else:
            self.block_size = 30
            self.margin = 30
            self.blocks_per_row = 15

        try:
            rows = (num_blocks + self.blocks_per_row - 1) // self.blocks_per_row
            width = self.blocks_per_row * (self.block_size + self.margin) + self.margin  # Largura total
            height = rows * (self.block_size + self.margin) + self.margin  # Altura total

            # Criar a imagem
            image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(image)

            # Configurar fonte para os números e o texto
            try:
                font = ImageFont.truetype("arial.ttf", size=14)
            except IOError:
                font = ImageFont.load_default()

            # Lista para guardar o status de cada bloco
            self.block_status = [False] * num_blocks  # Inicialmente, todos os blocos estão livres

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
                    if current_block % self.blocks_per_row < start_block % self.blocks_per_row:
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
                        self.block_status[block] = True  # Marcar os blocos como ocupados

            # Desenhar os blocos na imagem
            for i in range(num_blocks):
                row, col = divmod(i, self.blocks_per_row)
                x0 = col * (self.block_size + self.margin) + self.margin
                y0 = row * (self.block_size + self.margin) + self.margin
                x1 = x0 + self.block_size
                y1 = y0 + self.block_size

                # Cor do bloco
                fill_color = "firebrick" if self.block_status[i] else "skyblue"
                text = "Alocado" if self.block_status[i] else "Livre"

                # Desenhar o bloco
                draw.rectangle([x0, y0, x1, y1], fill=fill_color, outline="black")

                # Adicionar número identificador no topo do bloco
                block_id_text = str(i + 1)  # Número identificador (i + 1 para começar de 1)
                block_id_bbox = draw.textbbox((0, 0), block_id_text, font=font)  # Pega a caixa delimitadora do texto
                block_id_width = block_id_bbox[2] - block_id_bbox[0]
                block_id_x = x0 + (self.block_size - block_id_width) // 2  # Centralizar horizontalmente
                block_id_y = y0 + 5  # Colocar no topo do bloco

                draw.text((block_id_x, block_id_y), block_id_text, fill="black", font=font)

                # Adicionar o status (Livre ou Alocado) centralizado
                text_bbox = draw.textbbox((0, 0), text, font=font)  # Pega a caixa delimitadora do texto
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = x0 + (self.block_size - text_width) // 2  # Centralizar horizontalmente
                text_y = y0 + (self.block_size - text_height) // 2  # Centralizar verticalmente

                draw.text((text_x, text_y), text, fill="black", font=font)

            # Salvar a imagem no atributo para exibir no Canvas
            self.tk_image = ImageTk.PhotoImage(image)

            # Limpar o Canvas antes de desenhar
            self.canvas.delete("all")

            # Calcular a posição para centralizar a imagem no Canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

            # Atualizar a barra de rolagem
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # Desenhar as setas armazenadas
            for arrow in self.arrows:
                self.desenhar_seta(*arrow)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar a imagem: {e}")

    def show_disk(self):
        self.clear_canvas()
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

    def allocate_file(self):
        if self.file_size_entry.get() == '':
            messagebox.showwarning("Atenção", "Informe o tamanho do arquivo.")
            return

        try:
            file_size = int(self.file_size_entry.get())
            if file_size <= 0:
                raise ValueError("O tamanho do arquivo deve ser maior que zero.")

            self.current_allocation_color = "#%06x" % random.randint(0x000000, 0xFFFFFF)

            if self.allocation_type.get() == "Contígua":
                self.allocate_contiguous(file_size)
            elif self.allocation_type.get() == "Encadeada":
                self.allocate_linked(file_size)
            elif self.allocation_type.get() == "Indexada":
                self.allocate_indexed(file_size)
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    def allocate_contiguous(self, file_size):
        # Verifica os blocos livres e tenta alocar um segmento contíguo
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]

        for i in range(len(free_blocks) - file_size + 1):
            if all(free_blocks[j] == free_blocks[i] + j for j in range(file_size)):
                # Alocar os blocos contíguos encontrados
                for j in range(file_size):
                    self.block_status[free_blocks[i] + j] = self.current_allocation_color
                self.update_disk_image()
                return

        messagebox.showerror("Erro", "Não há blocos contíguos suficientes disponíveis para alocar o arquivo.")

    def allocate_linked(self, file_size):
        # Aloca blocos livres aleatoriamente e cria uma cadeia entre eles
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]

        if len(free_blocks) < file_size:
            messagebox.showerror("Erro", "Não há blocos suficientes disponíveis para alocar o arquivo.")
            return

        allocated_blocks = random.sample(free_blocks, file_size)
        self.arrows = []  # Limpar setas anteriores

        for i in range(len(allocated_blocks) - 1):
            self.block_status[allocated_blocks[i]] = self.current_allocation_color
            # Armazenar seta para ser desenhada posteriormente
            self.arrows.append((allocated_blocks[i], allocated_blocks[i + 1], self.block_size, self.block_size, self.margin, self.blocks_per_row, self.current_allocation_color))

        # Marcar o último bloco
        self.block_status[allocated_blocks[-1]] = self.current_allocation_color

        self.update_disk_image()

    def desenhar_seta(self, bloco_origem, bloco_destino, largura_bloco, altura_bloco, espaco, blocos_por_linha, cor):
        linha_origem = bloco_origem // blocos_por_linha
        coluna_origem = bloco_origem % blocos_por_linha
        x1 = coluna_origem * (largura_bloco + espaco) + espaco + largura_bloco / 2
        y1 = linha_origem * (altura_bloco + espaco) + espaco + altura_bloco / 2

        linha_destino = bloco_destino // blocos_por_linha
        coluna_destino = bloco_destino % blocos_por_linha
        x2 = coluna_destino * (largura_bloco + espaco) + espaco + largura_bloco / 2
        y2 = linha_destino * (altura_bloco + espaco) + espaco + altura_bloco / 2

        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=cor, width=4)

    def allocate_indexed(self, file_size):
        # Utiliza um bloco índice que aponta para outros blocos livres
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]

        if len(free_blocks) < file_size + 1:
            messagebox.showerror("Erro", "Não há blocos suficientes disponíveis para alocar o arquivo.")
            return

        index_block = free_blocks.pop(0)  # Primeiro bloco será o índice
        allocated_blocks = random.sample(free_blocks, file_size)

        self.block_status[index_block] = self.current_allocation_color
        for block in allocated_blocks:
            self.block_status[block] = self.current_allocation_color

        self.update_disk_image()

    def update_disk_image(self):
        # Atualiza a imagem do disco com o novo status dos blocos
        num_blocks = len(self.block_status)
        rows = (num_blocks + self.blocks_per_row - 1) // self.blocks_per_row
        width = self.blocks_per_row * (self.block_size + self.margin) + self.margin  # Largura total
        height = rows * (self.block_size + self.margin) + self.margin  # Altura total

        # Criar a imagem
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Configurar fonte para os números e o texto
        try:
            font = ImageFont.truetype("arial.ttf", size=14)
        except IOError:
            font = ImageFont.load_default()

        # Desenhar os blocos na imagem
        for i in range(num_blocks):
            row, col = divmod(i, self.blocks_per_row)
            x0 = col * (self.block_size + self.margin) + self.margin
            y0 = row * (self.block_size + self.margin) + self.margin
            x1 = x0 + self.block_size
            y1 = y0 + self.block_size

            if isinstance(self.block_status[i], str):  # Bloco alocado com cor especificada
                fill_color = self.block_status[i]
                text = "Alocado"
            else:
                fill_color = "firebrick" if self.block_status[i] else "skyblue"
                text = "Alocado" if self.block_status[i] else "Livre"

            # Desenhar o bloco
            draw.rectangle([x0, y0, x1, y1], fill=fill_color, outline="black")

            # Adicionar número identificador no topo do bloco
            block_id_text = str(i + 1)  # Número identificador (i + 1 para começar de 1)
            block_id_bbox = draw.textbbox((0, 0), block_id_text, font=font)  # Pega a caixa delimitadora do texto
            block_id_width = block_id_bbox[2] - block_id_bbox[0]
            block_id_x = x0 + (self.block_size - block_id_width) // 2  # Centralizar horizontalmente
            block_id_y = y0 + 5  # Colocar no topo do bloco

            draw.text((block_id_x, block_id_y), block_id_text, fill="black", font=font)

            # Adicionar o status (Livre ou Alocado) centralizado
            text_bbox = draw.textbbox((0, 0), text, font=font)  # Pega a caixa delimitadora do texto
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = x0 + (self.block_size - text_width) // 2  # Centralizar horizontalmente
            text_y = y0 + (self.block_size - text_height) // 2  # Centralizar verticalmente

            draw.text((text_x, text_y), text, fill="black", font=font)

        # Salvar a imagem no atributo para exibir no Canvas
        self.tk_image = ImageTk.PhotoImage(image)

        # Limpar o Canvas antes de desenhar
        self.canvas.delete("all")

        # Calcular a posição para centralizar a imagem no Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Atualizar a barra de rolagem
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Desenhar as setas armazenadas
        for arrow in self.arrows:
            self.desenhar_seta(*arrow)

    def clear_canvas(self):
        # Limpa o canvas e reseta o estado
        self.canvas.delete("all")
        self.tk_image = None
        self.block_status = []
        self.arrows = []

if __name__ == "__main__":
    root = tk.Tk()  
    app = SimulatorApp(root)    
    root.mainloop()
