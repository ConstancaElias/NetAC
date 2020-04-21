#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, redirect, flash
import os
import subprocess
import os.path
from werkzeug.utils import secure_filename
app = Flask(__name__)

from actualizar_dicionario import actualizar_dicionario
from leitura_ficheiro_json import leitura_ficheiro_json
dire =  os.getcwd() 

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/Uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
		with open("novas_palavras2.txt", "w") as f: 
			f.write("%s*%s*%s" % (typeP, sociolinguistic, keyword))
		f.close()
		print("SUBPROCESS")
		output = actualizar_dicionario('static/dicionario_Ingles.txt')
		
		return redirect(url_for("novapalavra", output = output))
	else:
		return render_template("words.html")

@app.route('/novapalavra')
def novapalavra():
	output = request.args['output']
	return render_template("novapalavra.html", output = output)

ALLOWED_EXTENSIONS = set(['json'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		if request.file:
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
			leitura_ficheiro_json('static/dicionario_Ingles.txt', f)
			return redirect(url_for("resultados_analise", filen = f))
	else:
		return render_template('upload.html')

@app.route('/resultados_analise',  methods=['GET','POST'])
def resultados_analise():
	#output = request.args['output']
	f = request.args['filena']
	return render_template("resultados_analise.html", file = f)




'''
@app.route('/dicionario')
def dicionario():
	path = "C:/Users/Constança Elias/Documents/Projeto_LCC/dicionario_Ingles.pdf"
	return send_file(path, as_attachment=True)
'''

if __name__ == "__main__":
	app.run()

