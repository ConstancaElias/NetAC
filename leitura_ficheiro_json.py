# -*- coding: utf-8 -*-


# o argumento passado é o nome do ficheiro a converter: 
# Formato do Comando: python3 leitura_ficheiro_json.py <NOME_DO_FICHEIRO_JSON>.json

import os
import json
import ast
import sys
from freq_to_table import freq_to_table #para atualizar a tabela LATEX

#limpa os carateres indesejados e acrescenta 1 espaço no início e 1 espaço no fim (tokenizer)
def clean_str(string): 
    carateres_indesejados = [',', '!', '?', '.', '"', '@', '+', '^', '(', ')']

    for c in carateres_indesejados:
        string = string.replace(c, ' ')     #substituir o carater por um espaço
    
    string = " ".join(string.split())

    string = ' ' + string + ' '
    return string


def leitura_ficheiro_json(fileDicionario,ficheiroJson):
#Para guardar os comentarios, que vao ser usados para construir  a tabela
    comentario_Tabela = {}  # comentario : ([variaveisSocio], [keywords] )

    ocorrencias={}       #numero de ococorrencias por variavel sociolinguistica no post
    variaveisSoc={}      #keywords por variavel sociolinguistica no post 
    numeroPalavras=0     #numero total de todas as palavras de todos os comentarios do post
    numeroPalavrasH=0    #numero de palavras no post que sao hate speech
    quantidadeHate=0
    numeroComentarios = 0
    encondF = "utf8"

    #abrir o ficheiro json a ler
    with open(ficheiroJson, encoding=encondF) as myfile:
        data=myfile.read()
        myfile.close()
    # parse file
    obj = json.loads(data)



    #Abrir e ler o dicionario
    with open(fileDicionario, encoding=encondF) as f:
        gene_data = f.read()
        f.close()
    keywordTabEN = ast.literal_eval(gene_data)
    


    #ciclo que vai percorrer todos os comentarios do post
    for comentarios in obj["commentThread"]:
            # vai ver se é um comentario principal ou um reply a um dos comentarios principais
            if "commentText" in comentarios:
                comentario = comentarios["commentText"]
                numeroComentarios +=1
                ## necessario porque queremos guardar no dicionario para  a tabela o comentario com pontua�ao 
                coment = comentario
                comentario = clean_str(comentario)
                listaComentario = comentario.split()
                
                #print("Lista Comentario", listaComentario)
                #print("len: ", len(listaComentario))
                numeroPalavras+=len(listaComentario)
                #ciclo que percorre o tipo de preconceito e as variaveis socialinguisticas
                for (t,v) in keywordTabEN:
                    tp = t
                    slv = v
                    #ciclo que percorre o dicionario das palavras
                    for j in keywordTabEN[(t,v)]: 
                        #Comparacao das palavras do dicionario com as dos comentarios
                        if (' ' + j.lower() + ' ') in comentario.lower():
                            tp = t
                            slv = v
                            #if tp_ant != tp or slv_ant != slv:
                                #print("    ", "Type of Prejudice: ", tp, " || Socioling variable: ", slv)
                            #print("        ", j)

                            quantidadeHate+=1

                            #criar o dicionario que vai ser usado na construção da tabela
                            if comentario not in  comentario_Tabela:
                                    comentario_Tabela [coment] = ([],[])
                            #junta a lista, mesmo que ja exista para depois ao contar ser so fazer len(comentario_Tabela[comentario][1])
                            comentario_Tabela[coment][0].append(slv)
                            comentario_Tabela[coment][1].append(j)

                            #ve se o dicionario variaveisSoc ja tem a variavel sociolinguistica identificada
                            #se nao tiver adicionamos ao dicionario, com uma lista vazia
                            if slv not in variaveisSoc:
                                variaveisSoc[slv]=[]
                            #verifica se a keyword ja esta na respetiva lista
                            #se nao estiver, adicionamos
                            if j not in variaveisSoc[slv]:
                                variaveisSoc[slv].append(j)
                            #dicionario que guarda o numero de ocorrencias de uma variavel sociolinguistica
                            #se a variavel ainda nao estiver presente no dicionario, metemos o contador a um
                            if slv not in ocorrencias:
                                ocorrencias[slv]=1
                            #se ja estiver presente no dicionario, incrementamos o contador
                            else:
                                ocorrencias[slv]+=1

                    tp_ant = tp
                    slv_ant = slv
            
            #vai ver se é reply a um dos comentarios principais ou um um comentario principal 
            if "replies" in comentarios:
                #ciclo que vai percorrer todas as replies do comentario principal
                for subComentarios in comentarios["replies"]:
                    #serve para identificar o campo do texto
                    if "commentText" in subComentarios :

                        numeroComentarios +=1

                        comentario = subComentarios["commentText"]
                        coment = comentario
                        comentario = clean_str(comentario)
                    #  print("comentario S: ", comentario)
                        listaComentario = comentario.split()
                        
                        numeroPalavras+=len(listaComentario)
                        #ciclo que percorre o tipo de preconceito e as variaveis socialinguisticas
                        for (t,v) in keywordTabEN:

                            #ciclo que percorre o dicionario das palavras
                            for j in keywordTabEN[(t,v)]:
                                #Comparacao das palavras do dicionario com as dos comentarios
                                if (' ' + j.lower() + ' ') in comentario.lower():
                                    tp = t
                                    slv = v
                                    #if tp_ant != tp or slv_ant != slv:
                                        #print("    ", "Type of Prejudice: ", tp, " || Socioling variable: ", slv)
                                    #print("        ", j)

                                    quantidadeHate+=1

                                    #criar o dicionario que vai ser usado na construção da tabela
                                    if comentario not in  comentario_Tabela:
                                        comentario_Tabela [coment] = ([],[])
                                    
                                    #junta a lista, mesmo que ja exista para depois ao contar ser so fazer len(comentario_Tabela[comentario][1])
                                    comentario_Tabela[coment][0].append(slv)
                                    comentario_Tabela[coment][1].append(j)

                                    #vê se o dicionario variaveisSoc já tem a variavel sociolinguistica identificada
                                    #se não tiver adicionamos ao dicionario, com uma lista vazia
                                    if slv not in variaveisSoc:
                                        variaveisSoc[slv]=[]
                                    #verifica se a keyword ja esta na respetiva lista
                                    #se nao estiver, adicionamos
                                    if j not in variaveisSoc[slv]:
                                        variaveisSoc[slv].append(j)
                                    #dicionario que guarda o numero de ocorrencias de uma variavel sociolinguistica
                                    #se a variavel ainda nao estiver presente no dicionario, metemos o contador a um
                                    if slv not in ocorrencias:
                                        ocorrencias[slv]=1
                                    #se ja estiver presente no dicionario, incrementamos o contador
                                    else:
                                        ocorrencias[slv]+=1
                            tp_ant = tp
                            slv_ant = slv                
                                        
                            
 


    # a string s contem todas as variaveis sociolinguisticas presentes no post
    s = ""  
    for variavel in ocorrencias:
        s = s + variavel + ";\n " 
        s = s[0:len(s)-2] # retirar a ultima virgula


    for pal in ocorrencias:
        numeroPalavrasH+=ocorrencias[pal]

    freqComentario = str(quantidadeHate) + "/" + str (numeroComentarios)

    # Construçao da tabela de frequencia e dos comentarios
    out4 = freq_to_table(variaveisSoc,ocorrencias,ficheiroJson,numeroPalavras,comentario_Tabela,s,numeroPalavrasH,freqComentario)

    #Informaçao no terminal
    print("\n")

    out = []
    for variavel in variaveisSoc:
        print("For the sociolinguistic variables " + variavel + " the keywords used were :")
        print(variaveisSoc[variavel])
        print("and the percentage of its occurence is :" + str(round(( (ocorrencias[variavel])/numeroPalavras)*100,3)) + "%.")
        print("\n")

    print("The percentage of hate speech related words is " + str(round(( (ocorrencias[variavel])/numeroPalavras)*100,3)) + "%.")

    print("\n")

    print("---> Taking into account what was detected, we can reach the conclusion these comments are associated with : ", s[0:len(s)-1] + ".")
    print("\n")
    print("Overall there were " + freqComentario + " occurences of hate speech related comments.")

    out= "The percentage of hate speech related words is " + str(round((numeroPalavrasH/numeroPalavras)*100,4))+ "%"
    out1 = "Taking into account what was detected, we can reach the conclusion these comments are associated with : " + s[0:len(s)-1] + "."
    out2 = "Overall there were " + freqComentario + " occurences of hate speech related comments."
    
    return  out, out1, out2, out4