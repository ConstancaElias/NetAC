# Projeto_NetLang

## Para correr o site em Windows:

1) instalar flask

Em Windows:

2) executar: py -m venv env

3) env\Scripts\activate

4) set FLASK_APP = "app.py"

5) flask run

6) abrir o browser e escrever o endereço "localhost:5000"

Para sair do _env_, executar o comando _deactivate_.

## Para correr o site no servidor:

1) executar: source env/bin/activate

2) set FLASK_APP = "app.py"

3) export FLASK_RUN_PORT=10400

4) flask run --host=193.136.19.129
