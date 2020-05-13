#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, redirect, flash
import os
import subprocess
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)

## evita que se tenha de fazer ctrl + f5 para recarregar os pdfs
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CACHE_TYPE = "null"
dire =  os.getcwd() 

from actualizar_dicionario import actualizar_dicionario
from leitura_ficheiro_json import leitura_ficheiro_json

'''
def execute(cmd, files):
    subp_ret = ""
    cmd_list = [cmd]
    cmd_list.extend(files)
    try:
        subp_ret = subprocess.check_output(cmd_list)
        """ at this point you have the output of the command in subp_ret in case you need it """
    except Exception as e:
        print("Failed to run subprocess. Details: " + str(e))
    back =dict()
    for file in files:
        with open(file, 'r') as f:
            info = f.read()
            back[file] = info
    return back
'''


@app.route("/home")
@app.route("/")
def home():
	return render_template('home.html')

@app.route('/words', methods=['POST', 'GET'])
def words():
	if request.method == 'POST':
		typeP = request.form['type']
		sociolinguistic = request.form.get('sociolinguistic')
		keyword = request.form['keyword']
		if os.name == "nt":       
		    encondF = "cp1252" 
		else:
		    encondF = "utf8"
		with open("novas_palavras.txt", "w") as f: 
			f.write("%s*%s*%s" % (typeP, sociolinguistic, keyword))
		f.close()
		os.chdir(dire)
		output = actualizar_dicionario('dicionario_Ingles.txt')
		os.chdir(dire)
		return redirect(url_for("novapalavra", output = output))
	else:
		return render_template("words.html")

@app.route('/novapalavra')
def novapalavra():
	output = request.args['output']
	output = output.split(':')
	out1 = output[0]
	if len(output) == 1:
		out2 = ""
	else:
		out2 = output[1]
	return render_template("novapalavra.html", out1 = out1, out2 = out2)

ALLOWED_EXTENSIONS = set(['json'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		if request.files:
			f = request.files['file']
			f.save(secure_filename(f.filename))
			print("FILE", f.filename)
			os.chdir(dire)
			out1, out2, out3, out4 = leitura_ficheiro_json('dicionario_Ingles.txt', f.filename)
			#print(out1, out2, out3
			return redirect(url_for("resultados_analise", f = f.filename, out1 = out1, out2 = out2, out3 = out3, out4 = out4))
	else:
		return render_template('upload.html')

@app.route('/resultados_analise',  methods=['GET','POST'])
def resultados_analise():
	#output = request.args['output']
	f = request.args['f']
	out1 = request.args['out1']
	out2 = request.args['out2']
	out3 = request.args['out3']
	out4 = request.args['out4']
	print(out4)
	return render_template("resultados_analise.html", file = f, out1 = out1, out2 = out2, out3 = out3, out4 = out4)
'''
@app.route('/dicionario')
def dicionario():
	path = "C:/Users/Constança Elias/Documents/Projeto_LCC/dicionario_Ingles.pdf"
	return send_file(path, as_attachment=True)
'''

if __name__ == "__main__":
	app.run()
	
