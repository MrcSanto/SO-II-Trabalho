# Simulador de Alocação de Blocos Lógicos

Este é um aplicativo em Python que simula diferentes métodos de alocação de blocos em sistemas de arquivos. Ele fornece uma interface gráfica para visualizar como arquivos são alocados em um disco virtual utilizando métodos de alocação contígua, encadeada e indexada.

## Características
- Interface Gráfica.
- Métodos de Alocação:
    - Contígua: Aloca blocos adjacentes.
    - Encadeada: Aloca blocos não adjacentes, mantendo referências para o próximo bloco.
    - Indexada: Utiliza um bloco índice que aponta para todos os blocos alocados.
- Configuração de Dificuldade: Três níveis de dificuldade (Fácil, Médio, Difícil) que afetam a fragmentação do disco.
- Visualização de Setas: Exibe setas indicando a sequência de alocação dos blocos.
- Legenda de Cores: Ajuda a identificar os diferentes tipos de alocação e estados dos blocos.


## Pré-requisitos
- SO Linux
- Python 3.9
- Gerenciador de pacotes PIP
- Tkinter *para interface gráfica*
- Pillow *para manipular as imagens*

## Instalação
Siga os passos abaixo para configurar o ambiente e executar o aplicativo:

1. Instalar o Python 3.9
    - Antes de tudo, verifique se você já tem o Python instalado:

    ```bash
    $ which python3
    /usr/bin/python3
    ```
    - Se a versão não for 3.9, siga os passos abaixo:

    - Atualize o gerenciador de pacotes:

    ```bash
    sudo apt update
    sudo apt upgrade
    ```