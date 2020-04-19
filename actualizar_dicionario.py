# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#Considerando que o ficheiro recebido com novas palavras tem em cada linha o formato:
# 
#  tipo * variavel Sociolonguista * keyword
#from app import app
import os
import sys
import ast
import pickle
import codecs
from dict_to_table import dict_to_table #para atualizar a tabela LATEX

## Palavras que se oretende adicionar deverao estar no ficheiro novas_palavras.txt
## ao invocar o comando devera ser passado o dicionario : Portugues ou ingles, que se prentende atualizar 
# Formato do Comando: python3 actualizar_dicionario.py <DICIONARIO_A_ATUALIZAR>.txt


def actualizar_dicionario(fileDicionario):

    with open(fileDicionario, encoding="utf8") as f:      #por ser windows tive de por encoding = 'cp1252' em vez de enconding = "utf-8"
        gene_data = f.read()
        print("GEN_DATA", gene_data)

    keywordTabEN = ast.literal_eval(gene_data)

    #keywordTabEN = sorted(keywordTabEN.items(), key = lambda x : x[0])
    print("PRIMEIRO", keywordTabEN)
    #para abrir o ficheiro com palavras a adicionar ao diconario

    conteudo_ficheiro = open("novas_palavras.txt", "r", encoding = "utf8")
    #le as linhas do ficheiro com as palavras novas
    output = "abrir"
    for linha in conteudo_ficheiro:
        palavras = linha.split('*')
        tipo = palavras[0].strip()
        variavel =  palavras[1].strip()
        keyword = palavras[2].strip()
        print((tipo,variavel,keyword)) #para saber que a palavra foi lida corretamente e acrescentada
        #vê se o par já existe no dicionario
        if (tipo,variavel) in keywordTabEN:
            #se a keyword ainda nao estiver na lista do respetivo par vai adiciona-la
            if keyword not in keywordTabEN[(tipo,variavel)]:
                keywordTabEN[(tipo,variavel)].append(keyword)
                output = keyword + str(keywordTabEN)
                keywordTabEN[(tipo,variavel)].sort()
            else:
                #print("A palavra ja se encontra no dicionario")
                output = "The word you are trying to introduce in the dictionary is already there."
        #se o par nao existir, adicionamos ao dicionario com uma lista vazia
        else:
            keywordTabEN[(tipo,variavel)] = []
            keywordTabEN[(tipo,variavel)].append(keyword)
            output = keyword + str(keywordTabEN)
    conteudo_ficheiro.close()

    arquivo = open(fileDicionario, 'w') # Abre novamente o ficheiro com o dicionario mas desta vez em mod escrita
    print("SEGUNDO", keywordTabEN)
    #constroi o dicionario ja atualizado no ficheiro
    arquivo.write("{\n")
    n_tipos_preconceito = len(keywordTabEN) - 1

    for i in keywordTabEN:
        si = str(i)
        print("si", si)
        arquivo.write(si)
        arquivo.write(":")
        arquivo.write("[")
        comprimento = len(keywordTabEN[i])-1
        for j in keywordTabEN[i]:
            j = "'" + j +  "'"
            print("keyword", str(j))
            arquivo.write(str(j))
            if comprimento != 0:
                arquivo.write(",")
            comprimento -=1
        if n_tipos_preconceito == 0:
            arquivo.write("]\n")
        else:
            arquivo.write("],\n")
        n_tipos_preconceito -= 1


    arquivo.write("}")
    arquivo.close()

    open('novas_palavras.txt', 'w').close()

    dict_to_table(fileDicionario)
    return output