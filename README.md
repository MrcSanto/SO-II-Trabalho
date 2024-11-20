# Como Configurar e Rodar a Aplicação

Siga os passos abaixo para configurar e executar o projeto:

## 1. Abra o projeto e acesse sua pasta
```bash
$ cd caminho/para/o/projeto
```

## 2. Verifique se o Python 3 está instalado
Certifique-se de que o Python 3 está disponível no sistema:
```bash
$ which python3
```
O comando deve retornar:
```
/usr/bin/python3
```

## 3. Instale os pacotes necessários
Instale os seguintes módulos para preparar o ambiente:

### Módulo para criar ambientes virtuais
```bash
$ sudo apt-get install python3-venv
```

### Gerenciador de pacotes Python (pip)
```bash
$ sudo apt-get install python3-pip
```

### Tkinter - Biblioteca de interface gráfica para Python
```bash
$ sudo apt-get install python3-tk
```

## 4. Crie o ambiente virtual
No diretório do projeto, crie o ambiente virtual:
```bash
$ python3 -m venv .venv
```

## 5. Ative o ambiente virtual
Ative o ambiente virtual criado:
```bash
$ source ./.venv/bin/activate
```

## 6. Instale as dependências
Com o ambiente virtual ativado, instale os pacotes listados no arquivo `requirements.txt`:
```bash
$ pip install -r ./requirements.txt
```

## 7. Execute a aplicação
Rode o aplicativo principal:
```bash
$ python3 ./src/main.py
```
