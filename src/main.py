import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

class SimuladorAlocacao:
    """Classe principal contendo todos os atributos e métodos para simular a alocação de blocos."""

    COLOR_CONTIGUOUS = "#722F37"   # Cor vinho
    COLOR_LINKED = "#90EE90"       # Verde claro
    COLOR_INDEXED = "#E6E6FA"      # Lilás claro
    COLOR_INDEX_BLOCK = "#FFFF00"  # Amarelo para o bloco índice

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador de Alocação de Blocos Lógicos")
        self.raiz.geometry("1366x768")

        # Inicialização de atributos
        self.block_status = []
        self.arrows = []
        self.block_size = None
        self.margin = None
        self.blocks_per_row = None
        self.current_allocation_color = None
        self.tk_image = None
        self.disk_size_entry = None
        self.file_size_entry = None
        self.allocation_type = None
        self.difficulty_level = None
        self.canvas = None
        self.scrollbar = None

        self.configurar_barra_lateral()
        self.configurar_canvas()

    def configurar_barra_lateral(self):
        """Configura a barra lateral com os campos de entrada e opções."""
        sidebar = tk.Frame(self.raiz, width=300, bg="lightgray")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Entrada para o tamanho do disco
        tk.Label(
            sidebar,
            text="Tamanho do Disco (blocos):",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)
        self.disk_size_entry = tk.Entry(sidebar)
        self.disk_size_entry.pack(pady=5, anchor="w", padx=10)
        tk.Label(
            sidebar,
            text="Máximo de blocos: 512",
            bg="lightgray",
            fg="red"
        ).pack(pady=(0, 5), anchor="w", padx=10)

        # Entrada para o tamanho do arquivo
        tk.Label(
            sidebar,
            text="Tamanho do Arquivo (blocos):",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)
        self.file_size_entry = tk.Entry(sidebar)
        self.file_size_entry.pack(pady=5, anchor="w", padx=10)

        # Seleção do método de alocação
        tk.Label(
            sidebar,
            text="Métodos de Alocação:",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)
        self.allocation_type = tk.StringVar(value="Contígua")
        tk.Radiobutton(
            sidebar,
            text="Contígua",
            variable=self.allocation_type,
            value="Contígua",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)
        tk.Radiobutton(
            sidebar,
            text="Encadeada",
            variable=self.allocation_type,
            value="Encadeada",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)
        tk.Radiobutton(
            sidebar,
            text="Indexada",
            variable=self.allocation_type,
            value="Indexada",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)

        # Seleção do nível de dificuldade
        tk.Label(
            sidebar,
            text="Dificuldade:",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)
        self.difficulty_level = tk.StringVar(value="Fácil")
        tk.Radiobutton(
            sidebar,
            text="Fácil",
            variable=self.difficulty_level,
            value="Fácil",
            bg="lightgray"
        ).pack(pady=2, anchor="w", padx=10)
        tk.Radiobutton(
            sidebar,
            text="Médio",
            variable=self.difficulty_level,
            value="Médio",
            bg="lightgray"
        ).pack(pady=2, anchor="w", padx=10)
        tk.Radiobutton(
            sidebar,
            text="Difícil",
            variable=self.difficulty_level,
            value="Difícil",
            bg="lightgray"
        ).pack(pady=2, anchor="w", padx=10)

        # Tabela de cores (Legenda)
        tk.Label(
            sidebar,
            text="Legenda:",
            bg="lightgray",
            font=("Arial", 12, "bold")
        ).pack(pady=10, anchor="w", padx=10)

        # Frame para a legenda
        legend_frame = tk.Frame(sidebar, bg="lightgray")
        legend_frame.pack(pady=5, padx=10, anchor="w")

        # Método Contíguo
        contig_color = tk.Label(
            legend_frame,
            bg=self.COLOR_CONTIGUOUS,
            width=2,
            height=1
        )
        contig_color.grid(row=0, column=0, padx=5, pady=2)
        tk.Label(
            legend_frame,
            text="Contígua",
            bg="lightgray"
        ).grid(row=0, column=1, sticky="w")

        # Método Encadeado
        linked_color = tk.Label(
            legend_frame,
            bg=self.COLOR_LINKED,
            width=2,
            height=1
        )
        linked_color.grid(row=1, column=0, padx=5, pady=2)
        tk.Label(
            legend_frame,
            text="Encadeada",
            bg="lightgray"
        ).grid(row=1, column=1, sticky="w")

        # Método Indexado - Blocos de dados
        indexed_data_color = tk.Label(
            legend_frame,
            bg=self.COLOR_INDEXED,
            width=2,
            height=1
        )
        indexed_data_color.grid(row=2, column=0, padx=5, pady=2)
        tk.Label(
            legend_frame,
            text="Indexada (Blocos de Dados)",
            bg="lightgray"
        ).grid(row=2, column=1, sticky="w")

        # Método Indexado - Bloco índice
        index_block_color = tk.Label(
            legend_frame,
            bg=self.COLOR_INDEX_BLOCK,
            width=2,
            height=1
        )
        index_block_color.grid(row=3, column=0, padx=5, pady=2)
        tk.Label(
            legend_frame,
            text="Indexada (Bloco Índice)",
            bg="lightgray"
        ).grid(row=3, column=1, sticky="w")

        # Botões de ação
        tk.Button(
            sidebar,
            text="Criar Disco",
            command=self.exibir_disco
        ).pack(side=tk.BOTTOM, pady=10, anchor="s")
        tk.Button(
            sidebar,
            text="Criar Arquivo",
            command=self.criar_arquivo
        ).pack(side=tk.BOTTOM, pady=10, anchor="s")
        tk.Button(
            sidebar,
            text="Limpar",
            command=self.limpar_canvas
        ).pack(side=tk.BOTTOM, pady=10, anchor="s")

    def configurar_canvas(self):
        """Configura o canvas onde as imagens dos blocos serão exibidas."""
        canvas_frame = tk.Frame(self.raiz)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.tk_image = None

    def gerar_imagem_disco(self, num_blocks):
        """Gera a imagem do disco com os blocos livres e alocados."""
        # Configurações de tamanho dos blocos e margens
        if num_blocks < 50:
            self.block_size = 80
            self.margin = 100
            self.blocks_per_row = 5
        elif 50 <= num_blocks < 100:
            self.block_size = 70
            self.margin = 80
            self.blocks_per_row = 6
        elif 100 <= num_blocks < 200:
            self.block_size = 60
            self.margin = 60
            self.blocks_per_row = 8
        elif 200 <= num_blocks < 400:
            self.block_size = 50
            self.margin = 50
            self.blocks_per_row = 10
        elif 400 <= num_blocks < 650:
            self.block_size = 40
            self.margin = 40
            self.blocks_per_row = 12
        else:
            self.block_size = 30
            self.margin = 30
            self.blocks_per_row = 15
        try:
            # Calcula o tamanho da imagem
            rows = (num_blocks + self.blocks_per_row - 1) // self.blocks_per_row
            width = self.blocks_per_row * (self.block_size + self.margin) + self.margin
            height = rows * (self.block_size + self.margin) + self.margin
            image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", size=14)
            except IOError:
                font = ImageFont.load_default()
            self.block_status = [False] * num_blocks
            used_blocks = set()

            # Mapeia níveis de dificuldade para divisores
            difficulty_mapping = {
                "Fácil": 5,
                "Médio": 3,
                "Difícil": 1
            }
            divisor = difficulty_mapping.get(self.difficulty_level.get(), 5)
            total_files = num_blocks // divisor

            # Gera blocos já alocados para simular uso do disco
            for _ in range(total_files):
                start_block = random.randint(0, num_blocks - 1)
                if start_block in used_blocks:
                    continue
                file_size = random.randint(3, 10)
                allocated_blocks = []
                for i in range(file_size):
                    current_block = start_block + i
                    if current_block % self.blocks_per_row < start_block % self.blocks_per_row:
                        break
                    if current_block < num_blocks and current_block not in used_blocks:
                        allocated_blocks.append(current_block)
                    else:
                        break
                if len(allocated_blocks) == file_size:
                    used_blocks.update(allocated_blocks)
                    for block in allocated_blocks:
                        self.block_status[block] = True
            # Desenha os blocos
            for i in range(num_blocks):
                row, col = divmod(i, self.blocks_per_row)
                x0 = col * (self.block_size + self.margin) + self.margin
                y0 = row * (self.block_size + self.margin) + self.margin
                x1 = x0 + self.block_size
                y1 = y0 + self.block_size
                fill_color = "firebrick" if self.block_status[i] else "skyblue"
                text = "Alocado" if self.block_status[i] else "Livre"
                if self.block_status[i]:
                    draw.rectangle(
                        [x0, y0, x1, y1],
                        fill=fill_color,
                        outline="black",
                        width=3
                    )
                else:
                    draw.rectangle(
                        [x0, y0, x1, y1],
                        fill=fill_color,
                        outline="black"
                    )
                # Escreve o ID do bloco
                block_id_text = str(i + 1)
                block_id_bbox = draw.textbbox((0, 0), block_id_text, font=font)
                block_id_width = block_id_bbox[2] - block_id_bbox[0]
                block_id_x = x0 + (self.block_size - block_id_width) // 2
                block_id_y = y0 + 5
                draw.text(
                    (block_id_x, block_id_y),
                    block_id_text,
                    fill="black",
                    font=font
                )
                # Escreve o status do bloco
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = x0 + (self.block_size - text_width) // 2
                text_y = y0 + (self.block_size - text_height) // 2
                draw.text(
                    (text_x, text_y),
                    text,
                    fill="black",
                    font=font
                )
            self.tk_image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            for arrow in self.arrows:
                self.desenhar_seta(*arrow)
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Erro", f"Erro ao gerar a imagem: {e}")

    def exibir_disco(self):
        """Exibe a imagem do disco no canvas."""
        self.limpar_canvas()
        if self.disk_size_entry.get() == '':
            messagebox.showwarning("Atenção", "Informe o tamanho do disco.")
            return
        try:
            num_blocks = int(self.disk_size_entry.get())
            if num_blocks <= 0 or num_blocks >= 512:
                raise ValueError(
                    "O número de blocos deve ser maior que zero e menor que 512."
                )
            self.gerar_imagem_disco(num_blocks)
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    def criar_arquivo(self):
        """
        Cria um arquivo com o tamanho especificado e método de alocação selecionado.
        """
        if self.file_size_entry.get() == '':
            messagebox.showwarning("Atenção", "Informe o tamanho do arquivo.")
            return
        try:
            file_size = int(self.file_size_entry.get())
            if file_size <= 0:
                raise ValueError("O tamanho do arquivo deve ser maior que zero.")
            allocation_method = self.allocation_type.get()
            if allocation_method == "Contígua":
                self.current_allocation_color = self.COLOR_CONTIGUOUS
                self.alocar_contiguo(file_size)
            elif allocation_method == "Encadeada":
                self.current_allocation_color = self.COLOR_LINKED
                self.alocar_encadeado(file_size)
            elif allocation_method == "Indexada":
                self.current_allocation_color = self.COLOR_INDEXED
                self.alocar_indexado(file_size)
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    def alocar_contiguo(self, file_size):
        """Aloca um arquivo de forma contígua na memória."""
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]
        start_index = 0
        while start_index <= len(free_blocks) - file_size:
            contiguous_blocks = free_blocks[start_index:start_index + file_size]
            if all(
                contiguous_blocks[i] == contiguous_blocks[0] + i
                for i in range(file_size)
            ):
                for block in contiguous_blocks:
                    self.block_status[block] = self.current_allocation_color

                # Adicionar setas entre os blocos contíguos
                for i in range(len(contiguous_blocks) - 1):
                    self.arrows.append(
                        (
                            contiguous_blocks[i],
                            contiguous_blocks[i + 1],
                            self.block_size,
                            self.block_size,
                            self.margin,
                            self.blocks_per_row
                        )
                    )
                self.atualizar_imagem_disco()
                return
            start_index += 1
        messagebox.showerror(
            "Erro",
            "Não há blocos contíguos suficientes disponíveis para alocar o arquivo."
        )

    def alocar_encadeado(self, file_size):
        """Aloca um arquivo de forma encadeada."""
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]
        if len(free_blocks) < file_size:
            messagebox.showerror(
                "Erro",
                "Não há blocos suficientes disponíveis para alocar o arquivo."
            )
            return
        allocated_blocks = random.sample(free_blocks, file_size)
        for i in range(len(allocated_blocks) - 1):
            self.block_status[allocated_blocks[i]] = self.current_allocation_color
            self.arrows.append(
                (
                    allocated_blocks[i],
                    allocated_blocks[i + 1],
                    self.block_size,
                    self.block_size,
                    self.margin,
                    self.blocks_per_row
                )
            )
        self.block_status[allocated_blocks[-1]] = self.current_allocation_color
        self.atualizar_imagem_disco()

    def alocar_indexado(self, file_size):
        """Aloca um arquivo de forma indexada."""
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]
        if len(free_blocks) < file_size + 1:
            messagebox.showerror(
                "Erro",
                "Não há blocos suficientes disponíveis para alocar o arquivo."
            )
            return
        index_block = free_blocks.pop(0)
        allocated_blocks = random.sample(free_blocks, file_size)
        self.block_status[index_block] = self.COLOR_INDEX_BLOCK
        for block in allocated_blocks:
            self.block_status[block] = self.current_allocation_color
            self.arrows.append(
                (
                    index_block,
                    block,
                    self.block_size,
                    self.block_size,
                    self.margin,
                    self.blocks_per_row
                )
            )
        self.atualizar_imagem_disco()

    def desenhar_seta(
        self,
        bloco_origem,
        bloco_destino,
        largura_bloco,
        altura_bloco,
        espaco,
        blocos_por_linha
    ):
        """Desenha uma seta apontando para o próximo bloco de memória."""
        linha_origem = bloco_origem // blocos_por_linha
        coluna_origem = bloco_origem % blocos_por_linha
        x1 = coluna_origem * (largura_bloco + espaco) + espaco + largura_bloco / 2
        y1 = linha_origem * (altura_bloco + espaco) + espaco + altura_bloco / 2
        linha_destino = bloco_destino // blocos_por_linha
        coluna_destino = bloco_destino % blocos_por_linha
        x2 = coluna_destino * (largura_bloco + espaco) + espaco + largura_bloco / 2
        y2 = linha_destino * (altura_bloco + espaco) + espaco + altura_bloco / 2
        ajuste_x = largura_bloco / 4
        ajuste_y = altura_bloco / 4
        if x1 < x2:
            x1 += ajuste_x
            x2 -= ajuste_x
        elif x1 > x2:
            x1 -= ajuste_x
            x2 += ajuste_x
        if y1 < y2:
            y1 += ajuste_y
            y2 -= ajuste_y
        elif y1 > y2:
            y1 -= ajuste_y
            y2 += ajuste_y
        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            arrow=tk.LAST,
            fill='black',
            width=4
        )

    def atualizar_imagem_disco(self):
        """Atualiza a imagem do disco no canvas com os novos blocos alocados."""
        num_blocks = len(self.block_status)
        rows = (num_blocks + self.blocks_per_row - 1) // self.blocks_per_row
        width = self.blocks_per_row * (self.block_size + self.margin) + self.margin
        height = rows * (self.block_size + self.margin) + self.margin
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", size=14)
        except IOError:
            font = ImageFont.load_default()
        for i in range(num_blocks):
            row, col = divmod(i, self.blocks_per_row)
            x0 = col * (self.block_size + self.margin) + self.margin
            y0 = row * (self.block_size + self.margin) + self.margin
            x1 = x0 + self.block_size
            y1 = y0 + self.block_size
            if isinstance(self.block_status[i], str):
                fill_color = self.block_status[i]
                text = "Alocado"
                border_width = 4
            else:
                fill_color = "firebrick" if self.block_status[i] else "skyblue"
                text = "Alocado" if self.block_status[i] else "Livre"
                border_width = 3 if self.block_status[i] else 1
            draw.rectangle(
                [x0, y0, x1, y1],
                fill=fill_color,
                outline="black",
                width=border_width
            )
            block_id_text = str(i + 1)
            block_id_bbox = draw.textbbox((0, 0), block_id_text, font=font)
            block_id_width = block_id_bbox[2] - block_id_bbox[0]
            block_id_x = x0 + (self.block_size - block_id_width) // 2
            block_id_y = y0 + 5
            draw.text(
                (block_id_x, block_id_y),
                block_id_text,
                fill="black",
                font=font
            )
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = x0 + (self.block_size - text_width) // 2
            text_y = y0 + (self.block_size - text_height) // 2
            draw.text(
                (text_x, text_y),
                text,
                fill="black",
                font=font
            )
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        for arrow in self.arrows:
            self.desenhar_seta(*arrow)

    def limpar_canvas(self):
        """Limpa o canvas, removendo todos os blocos e setas."""
        self.canvas.delete("all")
        self.tk_image = None
        self.block_status = []
        self.arrows = []

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorAlocacao(root)
    root.mainloop()
