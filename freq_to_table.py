import os

if os.name == "nt":         #testar se estamos no Windows ou no Linux porque conforme seja um ou outra, esta variÃ¡vel muda
    encondL = "cp1250" #encoding para o package do Latex
else:
    encondL = "utf8"

## Funçao que remove os elemntos reptidos de uma lista. Recebe uma lista e retorna a lista sem elemntos repetidos
def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

#Funçao que recebe uma lista de strings e retorna  uma string

def Lista_String(lista):
    s = ""
    s = ""  
    for pal in lista:
        s = s + pal + ", " 
    s = s[0:len(s)-2] # retirar a ultima virgula
    return s



'''
Funçao responsavel por converter os dados estatisticos obtidos na analise dos ficheiros JSON em duas tabelas recorrendo ao Latex.
A primeira tabela, aprsenta para cada comentario, as Keyword presentes, as variaveis sociolinguistas associadas e a frequencia 
de ocorrencia de hate speech no comentario (em fracionario e em percentagem).
A segunda tabela, faz uma sistese dos valores no post para cada variavel sociolinguista (Keywors, nº de occorencias, frequencias)
No final do documento é feita a classificaçao do tipo de hate speech presete no Post 
'''


def freq_to_table(variaveisSoc,ocorrencias,ficheiro_analizado,numeroPalavras,comentario_tabela,variveisPresentes,numeroPalavrasH,freqComentario):
    ficheiro = ficheiro_analizado.split(". ")
    fi = ficheiro[0].split('.')
    print("FIIIII",fi)
    texfilename ="TabelaFreq_" + fi[0] + ".tex"
    print(texfilename)   
    texfile = open(texfilename, 'w')
    
    texfile.write("\documentclass[11pt]{article}\n\\usepackage{graphicx}\n\\usepackage{multirow}\n\\usepackage[pdftex]{hyperref}\n\\usepackage{colortbl}")
    texfile.write("\n\\usepackage{longtable, array}\n\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\\newlength\mylength")
    texfile.write("\n\\usepackage[legalpaper, landscape, margin=1in]{geometry}\n\\newcommand{\MinNumber}{0}")
    texfile.write("\\begin{document}")
    texfile.write( "\n\n")
    
    texfile.write("\\textbf {\\huge In this file:}")
    texfile.write("\\newline")
    texfile.write(" {\\par\large --- Table  1: Summary of the results per comment; }\n\n")
    texfile.write(" {\\par\large --- \\hyperlink{Table 2}{Table 2}: Summary of the results per sociolinguistic variable;}")
    texfile.write("\\newline")
    texfile.write("\\newline")

    
    #Escreve no documento: "Tabela  1: Sintese dos resultados obtidos, em cada comentario"
    texfile.write("\n\n\\centering\\textbf{\\large Table  1: Summary of the results per comment \n}")

    texfile.write("\n\\newcommand{\MaxNumber}{0}%\n\\newcommand{\ApplyGradient}[1]{%\n\\pgfmathsetmacro{\PercentColor}{100.0*(#1-\MinNumber)/(\MaxNumber-\MinNumber)}\n\\xdef\PercentColor{\PercentColor}%\n\\cellcolor{LightSpringGreen!\PercentColor!LightRed}{#1}\n}")
    texfile.write("\n\\newcolumntype{C}[2]{>{\\centering\\arraybackslash}p{#1}}\n\\begin{center}\n\setlength")
    texfile.write("\mylength{\dimexpr\\textwidth - 1\\arrayrulewidth - 50\\tabcolsep}\n\\begin{longtable}{|C{.40\mylength}|C{.30\mylength}|C{.15\mylength}|C{.15\mylength}|C{.15\mylength}|}")
    texfile.write("\n\hline\n\\textbf{Comment} & \\textbf{KeyWords} & \\textbf{Sociolinguistic Variables}  & \\textbf{Hate Speech Frequency} & \\textbf{Hate Speech Frequency(\%)} \\\\\n\hline")

    #para alternar as cores das linhas
    color1 = "green!27" 			
    color2 = "green!5"
    color = color1
    
    for comentario in comentario_tabela:
        #Porque no latex nao reconhece de forma imediata os carateres especiais, por isso so queremos letras e numeros
        cons = [".","!","?","(",")" , ":", ",","'" ,"-",'/', "-","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","t","q","r","s","t","u","v","z","x","y","w","0","1","2","3","4","5","6","7","8","9","A","Q","W","S","Z","X","E","D","C","F","R","T","G","V","B","H","Y","U","J","N","M","K","I","O","L","P"]

        #para sabe o numero de palavras por comenatrio
        listaComentario = comentario.split()
        numeroPalavrasComentario=len(listaComentario)
        
        freq =  str(len(comentario_tabela[comentario][1])) + "/"+  str(numeroPalavrasComentario)
        freqPer = str(round(((len(comentario_tabela[comentario][1]))/numeroPalavrasComentario)*100,3))
        
        keywords = remove_repetidos (comentario_tabela[comentario][1])
        variavel = remove_repetidos (comentario_tabela[comentario][0])

        k,v = Lista_String (keywords), Lista_String(variavel)


        string =  ' & ' + '\cellcolor{' + color + '}' + k + ' & ' + '\cellcolor{' + color + '}' + v + ' & ' + '\cellcolor{' + color + '}' + freq + ' & ' + '\cellcolor{' + color + '}' + freqPer +  ' \\\\  \hline\n  '
        
        #para so escrever a parte do comentario que nao sao carateres espciais
        for j in comentario:
            if j not in cons:
                comentario = comentario.replace(j," ")
           


        s = "\cellcolor{" + color + "}" + comentario
        
        #alternar as cores
        if color == color1:
            color = color2
        else:
            color = color1
        
        #escrever as linhas da tabela
        texfile.write("%s %s" % (s, string))
     

    #termina a primeira tabela
    texfile.write("\n\end{longtable}\n\end{center}\n")

    #Inicia a 2 tabela
    texfile.write("\n\n\\centering\\textbf{\large \hypertarget{Table 2}{Table 2}: Summary of the results per sociolinguistic variable \n}")

    texfile.write("\n\\newcolumntype{C}[2]{>{\\centering\\arraybackslash}p{#1}}\n\\begin{center}\n\setlength")
    texfile.write("\mylength{\dimexpr\\textwidth - 1\\arrayrulewidth - 40\\tabcolsep}\n\\begin{longtable}{|C{.25\mylength}|C{.40\mylength}|C{.15\mylength}|C{.15\mylength}|C{.15\mylength}|}")
    texfile.write("\n\hline\n\\textbf{Variavel Sociolinguistica} & \\textbf{KeyWords} & \\textbf{N de ocorrencias} & \\textbf{Frequencia}  & \\textbf{Frequencia(\%)} \\\\\n\hline")

    
    color1 = "red!27" 			#para alternar as cores das linhas
    color2 = "red!5"
    color = color1

    sorted(variaveisSoc)
  
    for variavel in variaveisSoc:

        aux =  str(ocorrencias[variavel]) + "/"+  str(numeroPalavras) 
        v = Lista_String(variaveisSoc[variavel])
        string =  ' & ' + '\cellcolor{' + color + '}' + v + ' & ' + '\cellcolor{' + color + '}' + str(ocorrencias[variavel]) + ' & ' + '\cellcolor{' + color + '}' + aux +   '& ' + '\cellcolor{' + color + '}' +  str(round(ocorrencias[variavel] / numeroPalavras,4) * 100) + ' \\\\  \hline\n  '
        	
        s = "\cellcolor{" + color + "}" + variavel
        
        #alternar as cores
        if color in color1:
            color = color2
        else:
            color = color1

        #escrever as linhas da tabela
        texfile.write("\\multirow{1}{*}{%s} %s" % (s, string))
        
    
   
   #termina a segunda tabela 
    texfile.write("\n\end{longtable}\n\end{center}\n")

    #para saber qual a variavel com maior numero de ocorrencia
    maximo = 0
    for var in ocorrencias:
        if maximo < ocorrencias[var]:
            maximo = ocorrencias[var]
            varMax = var

    #Apresentar uma breve conclusao dos resultados obtidos

    texfile.write("\n\n\\textbf{\\Large Result analysis:}\n\n")
    texfile.write("\\begin{itemize}")
    texfile.write("\\item Taking into account the words that were detected, we can reach the conclusion these comments are associated with : : " + variveisPresentes + "%.\n\n")
   
    texfile.write("\\item The percentage of hate speech related words is " + str(round((numeroPalavrasH/numeroPalavras)*100,4))+ ".\n\n")
    texfile.write( "\\item Considering that the variable " + "\\textbf{" + varMax  + "} has the most occurences in the post, we can interpret that this is the predominant hate speech.\n\n")
    texfile.write("\\item Overall there were " + freqComentario + " occurences of hate speech related comments.")
    texfile.write("\\end{itemize}")
#terminar o docimento

    texfile.write("\end{document}")

    texfile.close()
    
    command = 'pdflatex ' + texfilename #gerar o ficheiro pdf a partir do .tex
    os.system(command)
    pdffilename = texfilename.split('.')[0] + ".pdf"
    return pdffilename