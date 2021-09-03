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


def leitura_ficheiro_json(fileDicionario,ficheiroJson,variavelSociolinguistica):
#Para guardar os comentarios, que vao ser usados para construir  a tabela
    comentario_Tabela = {}  # comentario : ([variaveisSocio], [keywords] )
    listaVariavelSoc={}
    ocorrencias={}       #numero de ococorrencias por keywords no post
    numeroPalavras=0     #numero total de todas as palavras de todos os comentarios do post
    numeroPalavrasH=0    #numero de palavras no post que sao hate speech
    encondF = "utf8"

    ficheiroJson2 = "static/Ficheiros_Json/" + ficheiroJson
    #abrir o ficheiro json a ler
    with open(ficheiroJson2, encoding=encondF) as myfile:
        data=myfile.read()

    # parse file
    obj = json.loads(data)

    myfile.close()


    #Abrir e ler o dicionario
    with open(fileDicionario, encoding=encondF) as f:
        gene_data = f.read()
    keywordTabEN = ast.literal_eval(gene_data)
    

    doc_title = obj["header"]["title"]


    for (t,v) in keywordTabEN:
        if v==variavelSociolinguistica:
            listaVariavelSoc=keywordTabEN[(t,v)]
            break

    #ciclo que vai percorrer todos os comentarios do post
    for comentarios in obj["commentThread"]:
            # vai ver se é um comentario principal ou um reply a um dos comentarios principais
            if "commentText" in comentarios:
                comentario = comentarios["commentText"]
                ## necessario porque queremos guardar no dicionario para  a tabela o comentario com pontua�ao 
                coment = comentario
                comentario = clean_str(comentario)
                listaComentario = comentario.split()
                
                #print("Lista Comentario", listaComentario)
                #print("len: ", len(listaComentario))
                numeroPalavras+=len(listaComentario)
                #ciclo que percorre o tipo de preconceito e as variaveis socialinguisticas
                for word in listaVariavelSoc:
                    #Comparacao das palavras do dicionario com as dos comentarios
                    if (' ' + word.lower() + ' ') in comentario.lower():
                        #if tp_ant != tp or slv_ant != slv:
                            #print("    ", "Type of Prejudice: ", tp, " || Socioling variable: ", slv)
                        #print("        ", j)
                        print(word)
                        numeroPalavrasH+=1

                        if word not in ocorrencias:
                            ocorrencias[word]=1
                        else:
                            ocorrencias[word]+=1



            #vai ver se é reply a um dos comentarios principais ou um um comentario principal 
            if "replies" in comentarios:
                #ciclo que vai percorrer todas as replies do comentario principal
                for subComentarios in comentarios["replies"]:
                    #serve para identificar o campo do texto
                    if "commentText" in subComentarios :

                        comentario = subComentarios["commentText"]
                        coment = comentario
                        comentario = clean_str(comentario)
                    #  print("comentario S: ", comentario)
                        listaComentario = comentario.split()
                        
                        numeroPalavras+=len(listaComentario)
                        #ciclo que percorre o tipo de preconceito e as variaveis socialinguisticas
                        for word in listaVariavelSoc:
                                #Comparacao das palavras do dicionario com as dos comentarios
                            if (' ' + word.lower() + ' ') in comentario.lower():
                                #if tp_ant != tp or slv_ant != slv:
                                    #print("    ", "Type of Prejudice: ", tp, " || Socioling variable: ", slv)
                                #print("        ", j)
                                print(word)
                                numeroPalavrasH+=1
                                if word not in ocorrencias:
                                    ocorrencias[word]=1
                                else:
                                    ocorrencias[word]+=1                       
    f.close()
    #Se existir hate
    if numeroPalavrasH>0:
        #numero total (numPalavrasH) de ocorrencia de hate
        print("The occurence of words related to the sociolinguistic variable given is: ",numeroPalavrasH)
        #frequencia palavras de hate
        print("And the percentage of its occurence is :" + str(round(( (numeroPalavrasH)/numeroPalavras)*100,3)) + "%.")
        #hate por keyword
        for word in ocorrencias:
            print("The keyword " + word + " occurred " + str(ocorrencias[word]) + " times.")
    else:
        print("No keywords related to the sociolinguistic variable given were found.")