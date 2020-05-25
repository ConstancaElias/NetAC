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

## Para as alterações feitas no site do servidor serem refletidas no browser:

1) ps fax | grep -i flask

2) kill -9 PID_DO_PROCESSO_OBTIDO_NO_COMANDO_ANTERIOR

3) export FLASK_RUN_PORT=10400

4) nohup flask run --host 127.0.0.1 &
