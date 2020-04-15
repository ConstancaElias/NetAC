#coding: utf-8

import os

if os.name == "nt":         #testar se estamos no Windows ou no Linux porque conforme seja um ou outra, esta variável muda
    encondL = "cp1250" #encoding para o package do Latex
else:
    encondL = "utf8"

#funcao que recebe o ficheiro com o dicionario e cria a tabela
def dict_to_table(filename):

	file = open(filename)
	d = {}

	#percorre as linhas do dic
	for l in file:
		if "{" not in l and  "}" not in l:
			k, v = l.rsplit(':', 1) #obtem a última separação por ':' apenas. rsplit começa a o split pela direita e não pela esquerda
			tp, slv = k.split(',', 1) #obtem a primeira separação ':' apenas
			tp = tp[2:-1]
			slv = slv[2:-2]
			value = ""
			if "[]" in v:
				d[(tp, slv)] = value
			else:
				v = v[1:-2]

				conj = v.split(',')

				value = conj[0][1:-1]
				for i in range(1, len(conj)-1):
					w = conj[i]
					w = w[1:-1]
					value += ', ' + w
		
				w = conj[len(conj)-1]
				w = w[1:-2]
				value += ', ' + w

				d[(tp, slv)] = value

	file.close()
	
	texfilename = filename.split('.')[0][7:] + '.tex'
	texfile = open("static/Dicionarios/" + texfilename, 'w')
	texfile.write("\documentclass[11pt]{article}\n\\usepackage{graphicx}\n\\usepackage{multirow}\n\\usepackage[T1]{fontenc}\n\\usepackage[utf8]{inputenc}\n\\usepackage[portuguese]{babel}\n\\usepackage{lmodern}\n\\usepackage{colortbl}")
	texfile.write("\n\\usepackage{longtable, array}\n\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\\newlength\mylength")
	texfile.write("\n\\usepackage[legalpaper, landscape, margin=1in]{geometry}\n\\newcommand{\MinNumber}{0}")
	texfile.write("\n\\newcommand{\MaxNumber}{0}%\n\\newcommand{\ApplyGradient}[1]{%\n\\pgfmathsetmacro{\PercentColor}{100.0*(#1-\MinNumber)/(\MaxNumber-\MinNumber)}\n\\xdef\PercentColor{\PercentColor}%\n\\cellcolor{LightSpringGreen!\PercentColor!LightRed}{#1}\n}")
	texfile.write("\n\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n\\begin{document}\n\\begin{center}\n\setlength")
	texfile.write("\mylength{\dimexpr\\textwidth-5\\arrayrulewidth-8\\tabcolsep}\n\\begin{longtable}{|C{.30\mylength}|C{.30\mylength}|C{.45\mylength}|C{.45\mylength}|}")
	texfile.write("\n\hline\n\\textbf{Types of Prejudice} & \\textbf{Sociolinguist variables} & \\textbf{Keywords} \\\\\n\hline")
	c = -1
	string = ""
	n = 1
	tant = "" 		
	#type of prejudice anterior
	inicio = 1
	color1 = "cyan!20" 			#para alternar as cores das linhas
	color2 = "cyan!5"
	color = color1

	#percorre o dicionario d
	for key in sorted(d.keys()):
		t, s = key

		if inicio == 1:
			c = 1
			tant = t
			string += ' & ' + '\cellcolor{' + color + '}' + s + ' & ' + '\cellcolor{' + color + '}' + d[key] + ' \\\\ '
			color = color2
		else:
			if t in tant: 		#se type of prejudice é o mesmo
				c += 1
				string += ' & ' + '\cellcolor{' + color + '}' + s + ' & ' + '\cellcolor{' + color + '}' + d[key] + ' \\\\  '
				if color in color1:
					color = color2
				else:
					color = color1

			if t not in tant: 	# se mudou o type of prejudice.   Só depois de sabermos todas as var sociolinguisticas do type of prejudice é que podemos escrever a multirow no ficheiro
				string += ' & ' + '\cellcolor{' + color + '}' + s + ' & ' + '\cellcolor{' + color + '}' + d[key] + ' \\\\  '
				string += '\hline\n'
				texfile.write("\\multirow{%d}*{%s} %s" % (c,tant, string))
				c = 0			#contador de var sociolonguisticas volta a zero
				string = ""

		tant = t
		inicio += 1

	texfile.write("\n\end{longtable}\n\end{center}\n\end{document}")

	texfile.close()
	dire =  os.getcwd() 
	path = dire+"/static/Dicionarios"
	os.chdir(path)
	command = 'pdflatex ' + texfilename #gerar o ficheiro pdf a partir do .tex
	os.system(command)