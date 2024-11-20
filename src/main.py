import random
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from typing import Optional

class SimuladorAlocacao:
    """Classe principal contendo todos os atributos e métodos para simular a alocação de blocos."""
    COLOR_CONTIGUOUS = "#722F37"   # Cor vinho
    COLOR_LINKED = "#90EE90"       # Verde claro
    COLOR_INDEXED = "#E6E6FA"      # Lilás claro
    COLOR_INDEX_BLOCK = "#FFFF00"  # Amarelo para o bloco índice

    def __init__(self, raiz) -> None:
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
        self.file_name_entry = None
        self.allocation_type = None
        self.difficulty_level = None
        self.canvas = None
        self.scrollbar = None
        self.files = {}
        self.selected_file = None

        self.configurar_barra_lateral()
        self.configurar_canvas()

        # configuração da Scroll Bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "TScrollbar",
            gripcount=0,
            background="#5A5A5A",  # Cor do fundo da barra
            darkcolor="#3C3C3C",   # Cor escura (bordas internas)
            lightcolor="#E0E0E0",  # Cor clara (bordas externas)
            troughcolor="#D3D3D3",  # Cor do trilho
            bordercolor="#2E2E2E",  # Cor da borda
            arrowcolor="#FFFFFF"    # Cor das setas
        )

    def configurar_barra_lateral(self) -> None:
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

        # Entrada para o nome do arquivo
        tk.Label(
            sidebar,
            text="Nome do Arquivo:",
            bg="lightgray"
        ).pack(pady=5, anchor="w", padx=10)
        self.file_name_entry = tk.Entry(sidebar)
        self.file_name_entry.pack(pady=5, anchor="w", padx=10)

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
            text="Contígua (first-fit)",
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
            text="Excluir Arquivo",
            command=self.excluir_arquivo
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

    def configurar_canvas(self) -> None:
        """Configura o canvas onde as imagens dos blocos 
        serão exibidas e posiciona a tabela à direita."""
        # Frame para o canvas
        canvas_frame = tk.Frame(self.raiz)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de rolagem vertical para o canvas
        self.scrollbar = ttk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=self.canvas.yview,
            style="TScrollbar"
        )
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.tk_image = None

        # Frame para a tabela de alocação à direita
        self.tabela_frame = tk.Frame(self.raiz, width=350, bg="lightgray")  # Aumentar a largura
        self.tabela_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuração da tabela de alocação
        self.tree = ttk.Treeview(
            self.tabela_frame,
            columns=("arquivo", "tamanho", "blocos"),
            show='headings',
            height=18
        )

        # Estilo para ajustar a altura das linhas
        style = ttk.Style()
        style.configure(
            "Treeview",
            rowheight=40
        )
        self.tree.heading("arquivo", text="Arquivo")
        self.tree.heading("tamanho", text="Tamanho")
        self.tree.heading("blocos", text="Blocos Alocados")
        self.tree.column("arquivo", width=120, anchor='center')
        self.tree.column("tamanho", width=80, anchor='center')
        self.tree.column("blocos", width=200, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Barra de rolagem para a tabela
        scrollbar = tk.Scrollbar(self.tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.config(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")

    def gerar_imagem_disco(self, num_blocks) -> None:
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
            self.block_status = [False] * num_blocks
            used_blocks = set()
            self.files = {}
            self.arrows = []

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
            self.atualizar_imagem_disco()
        except Exception as e:  # pylint: disable=W0718
            messagebox.showerror("Erro", f"Erro ao gerar a imagem: {e}")

    def exibir_disco(self) -> None:
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

    def criar_arquivo(self) -> None:
        """
        Cria um arquivo com o tamanho especificado e método de alocação selecionado.
        """
        if self.file_size_entry.get() == '':
            messagebox.showwarning("Atenção", "Informe o tamanho do arquivo.")
            return

        if self.file_name_entry.get() == '':
            messagebox.showwarning("Atenção", "Informe o nome do arquivo.")
            return

        file_name = self.file_name_entry.get()

        if file_name in self.files:
            messagebox.showwarning("Atenção", "Já existe um arquivo com este nome.")
            return

        try:
            file_size = int(self.file_size_entry.get())
            if file_size <= 0:
                raise ValueError("O tamanho do arquivo deve ser maior que zero.")
            allocation_method = self.allocation_type.get()
            allocated_blocks = None
            if allocation_method == "Contígua":
                self.current_allocation_color = self.COLOR_CONTIGUOUS
                allocated_blocks = self.alocar_contiguo(file_size)

            elif allocation_method == "Encadeada":
                self.current_allocation_color = self.COLOR_LINKED
                allocated_blocks = self.alocar_encadeado(file_size)

            elif allocation_method == "Indexada":
                self.current_allocation_color = self.COLOR_INDEXED
                allocated_blocks = self.alocar_indexado(file_size)

            if allocated_blocks:
                self.files[file_name] = {
                    "tamanho": file_size,
                    "blocos": allocated_blocks,
                    "metodo": allocation_method
                }

                self.atualizar_tabela_alocacao()
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    def alocar_contiguo(self, file_size) -> Optional[list[int]]:
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
                return contiguous_blocks
            start_index += 1
        messagebox.showerror(
            "Erro",
            "Não há blocos contíguos suficientes disponíveis para alocar o arquivo."
        )
        return None

    def alocar_encadeado(self, file_size) -> Optional[list[int]]:
        """Aloca um arquivo de forma encadeada."""
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]
        if len(free_blocks) < file_size:
            messagebox.showerror(
                "Erro",
                "Não há blocos suficientes disponíveis para alocar o arquivo."
            )
            return None
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
        return allocated_blocks

    def alocar_indexado(self, file_size) -> Optional[list[int]]:
        """Aloca um arquivo de forma indexada."""
        free_blocks = [i for i, status in enumerate(self.block_status) if not status]
        if len(free_blocks) < file_size + 1:
            messagebox.showerror(
                "Erro",
                "Não há blocos suficientes disponíveis para alocar o arquivo."
            )
            return None
        
        # Seleciona o bloco índice e os blocos de dados
        index_block = free_blocks.pop(0)  # Primeiro bloco é o índice
        allocated_blocks = random.sample(free_blocks, file_size)  # Seleciona blocos para alocar

        # Marca o bloco índice
        self.block_status[index_block] = self.COLOR_INDEX_BLOCK

        # Marca os blocos alocados e cria as setas do bloco índice para cada bloco
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

        # Atualiza o canvas para refletir a alocação
        self.atualizar_imagem_disco()
        return [index_block] + allocated_blocks

    def desenhar_seta(
        self,
        bloco_origem,
        bloco_destino,
        largura_bloco,
        altura_bloco,
        espaco,
        blocos_por_linha
    ) -> None:
        """Desenha uma seta apontando do bloco de origem para o bloco de destino."""
        # Calcula as coordenadas do bloco de origem
        linha_origem = bloco_origem // blocos_por_linha
        coluna_origem = bloco_origem % blocos_por_linha
        x1 = coluna_origem * (largura_bloco + espaco) + espaco + largura_bloco / 2
        y1 = linha_origem * (altura_bloco + espaco) + espaco + altura_bloco / 2

        # Calcula as coordenadas do bloco de destino
        linha_destino = bloco_destino // blocos_por_linha
        coluna_destino = bloco_destino % blocos_por_linha
        x2 = coluna_destino * (largura_bloco + espaco) + espaco + largura_bloco / 2
        y2 = linha_destino * (altura_bloco + espaco) + espaco + altura_bloco / 2

        # Ajusta as coordenadas para evitar sobreposição com as bordas
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

        # Desenha a linha no canvas com uma seta no final
        self.canvas.create_line(
            x1, y1, x2, y2,
            arrow=tk.LAST,
            fill='black',
            width=3
        )

    def atualizar_imagem_disco(self) -> None:
        """Atualiza a imagem do disco no canvas com os novos blocos alocados e exibe setas do arquivo selecionado."""
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
        
        # Desenha os blocos
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

            outline_color = "black"
            border_width = 1
            if (
                self.selected_file
                and i in self.files[self.selected_file]["blocos"]
            ):
                outline_color = "yellow"  # Cor de destaque
                border_width = 3
            
            draw.rectangle(
                [x0, y0, x1, y1],
                fill=fill_color,
                outline=outline_color,
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
        
        # Exibe as setas de acordo com o método de alocação
        if self.selected_file and self.selected_file in self.files:
            selected_blocks = self.files[self.selected_file]["blocos"]
            allocation_method = self.files[self.selected_file]["metodo"]
            if allocation_method in ["Contígua", "Encadeada"]:
                for i in range(len(selected_blocks) - 1):
                    self.desenhar_seta(
                        selected_blocks[i],
                        selected_blocks[i + 1],
                        self.block_size,
                        self.block_size,
                        self.margin,
                        self.blocks_per_row
                    )
            elif allocation_method == "Indexada":
                index_block = selected_blocks[0]
                data_blocks = selected_blocks[1:]
                for block in data_blocks:
                    self.desenhar_seta(
                        index_block,
                        block,
                        self.block_size,
                        self.block_size,
                        self.margin,
                        self.blocks_per_row
                    )

    def atualizar_tabela_alocacao(self) -> None:
        """Atualiza a tabela de alocação com os arquivos atuais."""
        # Limpar a tabela antes de atualizar
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Inserir os arquivos na tabela
        for file_name, info in self.files.items():
            # Limitar o número de blocos exibidos diretamente na tabela
            num_blocos_exibir = 10  # Número de blocos a serem exibidos na tabela
            blocos_str = ', '.join(str(b + 1) for b in info["blocos"][:num_blocos_exibir])
            if len(info["blocos"]) > num_blocos_exibir:
                blocos_str += ", ... (clique para ver mais)"

            self.tree.insert(
                '',
                'end',
                iid=file_name,
                values=(
                    file_name,
                    info["tamanho"],
                    blocos_str
                )  # Inclui o nome do arquivo e os primeiros blocos
            )

        # Adicionar evento de clique para visualizar todos os blocos
        self.tree.bind("<Double-1>", self.mostrar_blocos_completos)
        self.tree.bind("<ButtonRelease-1>", self.selecionar_arquivo)

    def mostrar_blocos_completos(self, event) -> None:
        """Mostra todos os blocos alocados em uma janela popup."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        file_info = self.files.get(selected_item)
        if not file_info:
            return

        # Cria uma nova janela para exibir os blocos completos
        popup = tk.Toplevel(self.raiz)
        popup.title(f"Blocos Alocados - {selected_item}")
        popup.geometry("400x400")

        blocos_str = ', '.join(str(b + 1) for b in file_info["blocos"])
        text_widget = tk.Text(popup, wrap=tk.WORD)
        text_widget.insert(tk.END, blocos_str)
        text_widget.config(state=tk.DISABLED)  # Tornar o texto não editável
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def selecionar_arquivo(self, event) -> None:
        """Destaca os blocos do arquivo selecionado na tabela e preenche os campos de entrada."""
        selected_item = self.tree.focus()
        if selected_item:
            self.selected_file = selected_item  
            file_info = self.files.get(self.selected_file) 

            if file_info:
                self.file_name_entry.delete(0, tk.END)
                self.file_name_entry.insert(0, self.selected_file)

                self.file_size_entry.delete(0, tk.END)
                self.file_size_entry.insert(0, str(file_info["tamanho"]))

            self.atualizar_imagem_disco()

    def excluir_arquivo(self) -> None:
        """Exclui um arquivo pelo nome e atualiza o disco."""
        if not self.files:
            messagebox.showwarning("Atenção", "Não há arquivos para excluir.")
            return
        file_name = self.file_name_entry.get()
        if file_name == '':
            messagebox.showwarning("Atenção", "Informe o nome do arquivo a ser excluído.")
            return
        if file_name not in self.files:
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return
        # Liberar os blocos alocados pelo arquivo
        for block in self.files[file_name]["blocos"]:
            self.block_status[block] = False
        # Remover as setas associadas ao arquivo
        self.arrows = [
            arrow for arrow in self.arrows
            if arrow[0] not in self.files[file_name]["blocos"]
            and arrow[1] not in self.files[file_name]["blocos"]
        ]
        # Remover o arquivo da lista
        del self.files[file_name]
        self.selected_file = None
        self.atualizar_imagem_disco()
        self.atualizar_tabela_alocacao()
        messagebox.showinfo("Sucesso", f"Arquivo '{file_name}' excluído com sucesso.")

    def limpar_canvas(self) -> None:
        """Limpa o canvas, removendo todos os blocos e setas."""
        self.canvas.delete("all")
        self.tk_image = None
        self.block_status = []
        self.arrows = []
        self.files = {}
        self.selected_file = None
        self.tree.delete(*self.tree.get_children())

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorAlocacao(root)
    root.mainloop()
