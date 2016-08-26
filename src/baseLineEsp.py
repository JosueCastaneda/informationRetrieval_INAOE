import nltk
import os
import csv
from glob import glob
from math import log
import re
import string
import unicodecsv
from cStringIO import StringIO

#Obtener todos los nombres de los documentos
texts = glob('conjuntoDatos/espanol/us*') 
from nltk.corpus.reader import XMLCorpusReader

#declaro el corpus de toda la coleccion 
terminos = [] #Lista de terminos
terminosUnicos = [] #Terminos unicos
terminosUnicos2 = [] #Terminos unicos  
terminosProhibidos = []
palabrasTotales = 0

#obtener el vocabulario de cada documnento
for item_path in texts:
    destino = os.path.basename(item_path)
    reader = XMLCorpusReader('conjuntoDatos/espanol', destino)
    palabras = reader.words() #obtengo las palabras
    palabrasTotales = palabrasTotales + len(palabras)
    palabrasUnicas = sorted(set(palabras)) #obtengo las palabras sin repeticion
    terminos.extend(palabrasUnicas)
    terminosUnicos.extend(sorted(set(terminos))) #obtengo las palabras sin repeticion
    terminosUnicos2 = sorted(set(terminosUnicos)) #Terminos unicos  
    reader = None #Hago null a el apuntador
    terminos = None
    terminos = []
    

a = "'";
for x in terminosUnicos2:
	if a in x:
		terminosProhibidos.append(x);
 
 

for x in terminosProhibidos:
    terminosUnicos2.remove(x);
    
frecuenciaInversa = None	
	
##Calcular frecuencia inversa, tengo el nombre del vocabulario
frecuenciaInversa = [[0 for x in range(2)] for x in range(len(terminosUnicos2))]	
k = 0
for vocabulario in terminosUnicos2:
	frecuenciaInversa[k][0] = vocabulario
	k = k + 1
    
#Frecuencia Inversa
for item_path in texts:
	destino = os.path.basename(item_path)
	readerDoc = XMLCorpusReader('conjuntoDatos/espanol', destino)
	palabrasDoc = readerDoc.words() #obtengo las palabras
	palabrasUnicasDoc = sorted(set(palabrasDoc)) #obtengo las palabras sin repeticion 
	a = "'";
	for x in palabrasUnicasDoc:
		if a in x:
			palabrasUnicasDoc.remove(x);	
	
        #Remover las palabras que no valen
        a = "'";
        terminosProhibidos = []
        for x in palabrasUnicasDoc:
            if a in x:
		    terminosProhibidos.append(x);
	for x in terminosProhibidos:
            palabrasUnicasDoc.remove(x);	
        
	i = 0 
	for termino in palabrasUnicasDoc:
		indexTermino = terminosUnicos2.index(termino) #obtengo la pos. en el vocabulario corpus
		frecuenciaInversa[indexTermino][1] = frecuenciaInversa[indexTermino][1] +1
		

#Obtener la clase de cada matriz M o Femenino
fname = 'conjuntoDatos/espanol/truth.txt'
with open(fname) as f:
   content = [x.strip('\n') for x in f.readlines()]

valoresVerdad = [[0 for x in range(3)] for x in range(len(texts))]

i=0

for valorVerdad in content:
	arregloV = valorVerdad.split(":::")
	valoresVerdad[i][0] = arregloV[0]
	valoresVerdad[i][1] = arregloV[1]
        valoresVerdad[i][2] = arregloV[2]
        i = i + 1

valoresVerdad.sort()

# Matriz del corpus vacia
matrizDocumento = [[0 for x in range(len(terminosUnicos2)+3)] for x in range(len(texts)+1)] 

#Crear los headers de la matriz
matrizDocumento[0][0] = 'idUsuario'
i = 1
for x in terminosUnicos2:
	matrizDocumento[0][i] = "'"+x+"'"
	#matrizDocumento[0][i] = x
	i = i+1

matrizDocumento[0][len(terminosUnicos2)+1] = 'claseUsuario'
matrizDocumento[0][len(terminosUnicos2)+2] = 'edadUsuario'

#Creacion matrix version 2 petit
j = 1 #Lleva el control del usuario
k = 0
for item_path in texts:
	destino = os.path.basename(item_path)
	readerDoc = XMLCorpusReader('conjuntoDatos/espanol', destino)
	palabrasDoc = readerDoc.words() #obtengo las palabras
	palabrasUnicasDoc = sorted(set(palabrasDoc)) #obtengo las palabras sin repeticion 
	
        #Remover las palabras que no valen
        a = "'";
        terminosProhibidos = []
        for x in palabrasUnicasDoc:
            if a in x:
		    terminosProhibidos.append(x);
	for x in terminosProhibidos:
            palabrasUnicasDoc.remove(x);
            
        
	for x in palabrasUnicasDoc:
		if a in x:
			palabrasUnicasDoc.remove(x);
	matrizTemporalDocumento = [[0 for x in range(2)] for x in range(len(palabrasUnicasDoc))] 
	i = 0
	matrizDocumento[j][0] = destino
	for termino in palabrasUnicasDoc:
		matrizTemporalDocumento[i][0] = termino
		matrizTemporalDocumento[i][1] = palabrasDoc.count(termino)
		i = i+1
		indiceTermino = terminosUnicos2.index(termino)+1 #obtengo la pos. en el vocabulario corpus
		indiceTemporal =  palabrasUnicasDoc.index(termino) #Posicion de documento local
		matrizDocumento[j][indiceTermino] = matrizTemporalDocumento[indiceTemporal][1]*log(len(texts)/frecuenciaInversa[indiceTermino-1][1])
		matrizDocumento[j][len(terminosUnicos2)+1] = valoresVerdad[k][1]
                matrizDocumento[j][len(terminosUnicos2)+2] = valoresVerdad[k][2]
		
	j = j +1        
	k = k +1


#Crear archivo arff para weka
myfile = open('archivoEs.arff', 'wb')
myfile.write( "@RELATION archivo\n\n")

stringID = ""
#Obtener los identificadores
for id in range(len(matrizDocumento)-1):
	#print matrizDocumento[id+1][0], id, len(matrizDocumento)-1
	if cmp(id+1, len(matrizDocumento)-1):
		stringID = stringID +  matrizDocumento[id+1][0] +","
	else:
		stringID = stringID +  matrizDocumento[id+1][0]

myfile.write( "@ATTRIBUTE idUsuario {"+stringID+"}\n")
#print (stringID)

#Obtener el nombre de las clases
for id in  range(len(matrizDocumento[0])-3):
	stringID = matrizDocumento[0][id+1]
	stringID = stringID.encode('utf8')
	#if( cmp(stringID, "'") != 0):
	myfile.write( "@ATTRIBUTE "+stringID+" REAL\n")

#Renglon de clase
myfile.write( "@ATTRIBUTE claseUsuario {M,F}\n")
myfile.write( "@ATTRIBUTE claseEdad {18-24,25-34,35-49,50-XX}\n\n")

#print id+2
#Datos
myfile.write( "@DATA\n\n")	
#Datos de la matriz
stringData = ""
stringID = ""
for id in range(len(matrizDocumento)-1):
	for idj in range(len(matrizDocumento[0])):
		stringData = str(matrizDocumento[id+1][idj])
		if cmp(idj+1, len(matrizDocumento[0])):
			stringID = stringID + stringData + ","
		else:
			stringID = stringID + stringData
		#stringID = stringID +"\n"#borrar despue
	#print idj	
	myfile.write( stringID+"\n")
	stringID = ""
	stringData = ""

# Close opend file
myfile.close()