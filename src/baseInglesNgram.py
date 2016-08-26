import nltk
import os
import csv
from glob import glob
import math 
import re
import string
import unicodecsv
from cStringIO import StringIO
from nltk.corpus.reader import XMLCorpusReader
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#Obtener todos los nombres de los documentos
texts = glob('conjuntoDatos/ingles/sexo/us*') 

#declaro el corpus de toda la coleccion 
terminos = [] #Lista de terminos
terminosUnicos = [] #Terminos unicos
terminosUnicos2 = [] #Terminos unicos 
terminosProhibidos = []

# Seleccion de valores aleatorios:
datos = range(len(texts));
random.shuffle(datos);
print datos;

n=4; #Cuatrigramas
# Corpus de entrenamiento
for id in range(0,122):
    item_path = texts[datos[id]]; #Obtengo un documento aleatorio
    destino = os.path.basename(item_path);
    with open("conjuntoDatos/ingles/sexo/"+destino,'r') as f:
        for line in f:
            for word in line.split():
                word = word.translate(None, '"')
                for i in range(len(word)-n+1):
                    #b[i:i+n]
                    ngrama = word[i:i+n];
                    try:
                        ngrama2 = ngrama.encode('utf8','replace')
                        terminos.append(ngrama)
                    except UnicodeError as e:
                        print ngrama,str(e)
                #terminos.append(word);
                #terminos.append(word); 
            terminosUnicos.extend(sorted(set(terminos)))
        terminosUnicos2 = sorted(set(terminosUnicos)) 
    terminos = None
    terminos = []    

#contadorPalabrasTotales = 0;
#terminosUnicos2

print len(terminosUnicos2);
a=["\xe2","\x80","\x9d","\x9c","\xa3","\xc2","\xa0","0xb6","\xc3","0x81","0x82","0x85","0x89","0x8d","0x91"
   ,"0x93","0x94"," 0x96","0x98","0x99","0x9f","0xa1"," 0xb1","0xa4","0xa5"," 0xa6","0xa7"," 0xa8","0xa9",
   "0xab","0xad","0xae","”","'"]
for i in a:
    for x in terminosUnicos2:
        if i in x:
            terminosProhibidos.append(x);
            print x

print x
for x in terminosProhibidos:
    #print x
    try:
        terminosUnicos2.remove(x);
    except ValueError as e:
            print x, str(e);

print  len(terminosUnicos2);       
#Terminos prohibidos.....
#a = "'";
#for x in terminosUnicos2:
#    if a in x:
#        terminosProhibidos.append(x);
#didsd

#for x in terminosProhibidos:
#    terminosUnicos2.remove(x);

#terminosProhibidos = []
#a = "?";
#for x in terminosUnicos2:
#    if a in x:
#        terminosProhibidos.append(x);
#didsd

#for x in terminosProhibidos:
#    terminosUnicos2.remove(x);
#Calculo frecuencia inversa
frecuenciaInversa = None
frecuenciaInversa = [[0 for x in range(2)] for x in range(len(terminosUnicos2))]	
k = 0
for vocabulario in terminosUnicos2:
	frecuenciaInversa[k][0] = vocabulario
	k = k + 1

#f1=open('testfile2.txt', 'w+')
numeroDatos = 0;

terminosUnicos = [] # Vaciar el buffer
terminos = [] # Vaciar el buffer

for id in range(0,122):
    item_path = texts[datos[id]]; #Obtengo un documento aleatorio
    destino = os.path.basename(item_path);
    with open("conjuntoDatos/ingles/sexo/"+destino,'r') as f:
        for line in f:
            for word in line.split():
                word = word.translate(None, '"')
                for i in range(len(word)-n+1):
                    #b[i:i+n]
                    ngrama = word[i:i+n];
                    try:
                        ngrama2 = ngrama.encode('utf8','replace')
                        terminos.append(ngrama)
                    except UnicodeError as e:
                        print ngrama,str(e)
                    #terminos.append(word[i:i+n])
                #terminos.append(word); 
            terminosUnicos.extend(sorted(set(terminos)))
    #Terminos prohibidos.....
    #a=["\xe2","\x80","\x9d","\x9c","\xa3","\xc2","\xa0","0xb6","\xc3","'"]
    for i in a:
        for x in terminosUnicos2:
            if i in x:
                terminosProhibidos.append(x);
    #a = "'";
    #terminosProhibidos = []
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
            
    for x in terminosProhibidos: 
        try:  
            terminosUnicos.remove(x); 
        except ValueError as e:
            print str(e),x; 
    for i in a:        
        for x in  terminosUnicos:
            if i in x:
                try:
                    terminosUnicos.remove(x);
                except ValueError as e:
                    print str(e),x;
    #a = "?";
    #terminosProhibidos = []
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
            
    #for x in terminosProhibidos:   
    #    terminosUnicos.remove(x); 
        
    #for x in  terminosUnicos:
    #    if a in x:
    #         terminosUnicos.remove(x);  
        
    for t in terminosUnicos:
        indexTermino = terminosUnicos2.index(t);
        frecuenciaInversa[indexTermino][1] = frecuenciaInversa[indexTermino][1] +1;
        #f1.write(t+"\n");
        #print t;
    print item_path;
    numeroDatos = numeroDatos + 1
    #f1.write(item_path);
    terminosUnicos = [] # Vaciar el buffer
    terminos = [] # Vaciar el buffer
#f1.close();

#Obtener la clase de cada matriz M o Femenino
fname = 'conjuntoDatos/ingles/sexo/truth.txt'
with open(fname) as f:
   content = [x.strip('\n') for x in f.readlines()]

valoresVerdad = [[0 for x in range(3)] for x in range(numeroDatos)]

i=0

# Crear arreglo que contenga solo los seleccionados aleatoriamente
usuariosAleatorios = [];
for id in range(numeroDatos):
    #print id;
    indiceTexto = datos[id];
    stringTexto = texts[indiceTexto];
    stringTexto = stringTexto.replace("conjuntoDatos/ingles/sexo/", "");
    stringTexto = stringTexto.replace(".xml", "");
    stringTexto = stringTexto.strip();
    usuariosAleatorios.append(stringTexto);
#print id;

usuariosAleatorios.sort();
print usuariosAleatorios;

i = 0;
j=0; #indice de los usuarioAleatorios
for valorVerdad in content:
    arregloV = valorVerdad.split(":::");
    for x in usuariosAleatorios:
        if cmp(arregloV[0], x) == 0:
            #print arregloV[0],x
            valoresVerdad[i][0] = arregloV[0]
            valoresVerdad[i][1] = arregloV[1]
            valoresVerdad[i][2] = arregloV[2]
            i = i + 1

valoresVerdad.sort()

# Matriz del corpus vacia       
matrizDocumento = [[0 for x in range(len(terminosUnicos2)+3)] for x in range(numeroDatos+1)] 

#Crear los headers de la matriz
matrizDocumento[0][0] = 'idUsuario'

i = 1
for x in terminosUnicos2:
	matrizDocumento[0][i] = "'"+x+"'"
	#matrizDocumento[0][i] = x
	i = i+1
#sdsdds

matrizDocumento[0][len(terminosUnicos2)+1] = 'claseUsuario'
matrizDocumento[0][len(terminosUnicos2)+2] = 'edadUsuario'

#Creacion matrix version 2 petit
j = 1 #Lleva el control del usuario
#k = 0
terminosUnicos = [] # Vaciar el buffer
terminos = [] # Vaciar el buffer

for id in range(0,122):
    item_path = texts[datos[id]]; #Obtengo un documento aleatorio
    destino = os.path.basename(item_path);
    #print destino;
    with open("conjuntoDatos/ingles/sexo/"+destino,'r') as f:
        for line in f:
            for word in line.split():
                word = word.translate(None, '"')
                for i in range(len(word)-n+1):
                    ngrama = word[i:i+n];
                    try:
                        ngrama2 = ngrama.encode('utf8','replace')
                        terminos.append(ngrama)
                    except UnicodeError as e:
                        print ngrama,str(e)
                    #terminos.append(word[i:i+n])
                #terminos.append(word); 
            terminosUnicos.extend(sorted(set(terminos)))
    #Terminos prohibidos.....
    #a=["\xe2","\x80","\x9d","\x9c","\xa3","\xc2","\xa0","0xb6","\xc3","'"]
    for i in a:
        for x in terminosUnicos2:
            if i in x:
                terminosProhibidos.append(x);
    #a = "'";
    #terminosProhibidos = []
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
            
    for x in terminosProhibidos: 
        try:  
            terminosUnicos.remove(x); 
        except ValueError as e:
            print str(e),x; 
    for i in a:        
        for x in  terminosUnicos:
            if i in x:
                try:
                    terminosUnicos.remove(x);
                except ValueError as e:
                    print str(e),x;
    #a = "'";
    #terminosProhibidos = []
    
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
    #        
    #for x in terminosProhibidos:   
    #    terminosUnicos.remove(x); 
        
    #for x in  terminosUnicos:
    #    if a in x:
    #         terminosUnicos.remove(x);       
    
    #a = "?";
    #terminosProhibidos = []
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
            
    #for x in terminosProhibidos:   
    #    terminosUnicos.remove(x); 
        
    #for x in  terminosUnicos:
    #    if a in x:
    #         terminosUnicos.remove(x);  
     
    matrizTemporalDocumento = [[0 for x in range(2)] for x in range(len(terminosUnicos))] 
    i = 0
    matrizDocumento[j][0] = destino
   
    for termino in terminosUnicos:
        matrizTemporalDocumento[i][0] = termino
        matrizTemporalDocumento[i][1] = terminos.count(termino)
        i = i+1
        indiceTermino = terminosUnicos2.index(termino)+1 #obtengo la pos. en el vocabulario corpus
        indiceTemporal =  terminosUnicos.index(termino) #Posicion de documento local
        matrizDocumento[j][indiceTermino] = matrizTemporalDocumento[indiceTemporal][1]*math.log(numeroDatos/frecuenciaInversa[indiceTermino-1][1])
        destino = destino.replace(".xml", "");
        destino = destino.strip();
        for x in valoresVerdad:
            if cmp(destino, x[0]) == 0:
                matrizDocumento[j][len(terminosUnicos2)+1] = x[1]
                matrizDocumento[j][len(terminosUnicos2)+2] = x[2]
    j = j +1
    #k = k +1
    terminosUnicos = [] # Vaciar el buffer
    terminos = [] # Vaciar el buffer

#print "es";

#Crear archivo arff para weka
myfile = open('archivoWekaEntrenamiento.arff', 'wb')
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
	#stringID = stringID.encode('utf8','ignore')
        try:
            stringID = stringID.encode('utf8','replace')
            myfile.write( "@ATTRIBUTE "+stringID+" REAL\n")
        except UnicodeError as e:
            print stringID,str(e)
	#if( cmp(stringID, "'") != 0):
	#myfile.write( "@ATTRIBUTE "+stringID+" REAL\n")

#Renglon de clase
myfile.write( "@ATTRIBUTE claseUsuario {M,F}\n\n")
myfile.write( "@ATTRIBUTE claseEdad {18-24,25-34,35-49,50-XX}\n\n")

#print id+2
#Datos
myfile.write( "@DATA\n\n")	
#Datos de la matriz
stringData = ""
stringID = ""
for id in range(len(matrizDocumento)-1):
#for id in range(1,91):
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

# ========================================================================================================

#Prueba

valoresVerdad2 = [[0 for x in range(3)] for x in range(len(texts))]

i=0
for valorVerdad in content:
	arregloV = valorVerdad.split(":::")
	valoresVerdad2[i][0] = arregloV[0]
	valoresVerdad2[i][1] = arregloV[1]
        valoresVerdad2[i][2] = arregloV[2]
        i = i + 1

valoresVerdad2.sort()


sizePrueba = len(texts) - numeroDatos; 
# Matriz del corpus vacia       
matrizDocumentoPrueba = [[0 for x in range(len(terminosUnicos2)+3)] for x in range(sizePrueba+1)] 

#Crear los headers de la matriz
matrizDocumentoPrueba[0][0] = 'idUsuario'

i = 1
for x in terminosUnicos2:
	matrizDocumentoPrueba[0][i] = "'"+x+"'"
	#matrizDocumento[0][i] = x
	i = i+1
#sdsdds

matrizDocumentoPrueba[0][len(terminosUnicos2)+1] = 'claseUsuario'
matrizDocumentoPrueba[0][len(terminosUnicos2)+2] = 'edadUsuario'

#Creacion matrix version 2 petit
j = 1 #Lleva el control del usuario
#k = 0
terminosUnicos = [] # Vaciar el buffer
terminos = [] # Vaciar el buffer
z = 0

for id in range(0,sizePrueba):
    item_path = texts[datos[id+numeroDatos]]; #Obtengo un documento aleatorio
    destino = os.path.basename(item_path);
    print destino;
    with open("conjuntoDatos/ingles/sexo/"+destino,'r') as f:
        for line in f:
            for word in line.split():
                word = word.translate(None, '"')
                for i in range(len(word)-n+1):
                    ngrama = word[i:i+n];
                    try:
                        ngrama2 = ngrama.encode('utf8','replace')
                        terminos.append(ngrama)
                    except UnicodeError as e:
                        print ngrama,str(e)
                    #terminos.append(word[i:i+n])
                #terminos.append(word); 
            terminosUnicos.extend(sorted(set(terminos)))
    #Terminos prohibidos.....
    #a=["\xe2","\x80","\x9d","\x9c","\xa3","\xc2","\xa0","0xb6","\xc3","'"]
    terminosProhibidos = []
    for i in a:
        for x in terminosUnicos2:
            if i in x:
                terminosProhibidos.append(x);
    #a = "'";
    #terminosProhibidos = []
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
            
    for x in terminosProhibidos: 
        try:  
            terminosUnicos.remove(x); 
        except ValueError as e:
            print str(e),x; 
    for i in a:        
        for x in  terminosUnicos:
            if i in x:
                try:
                    terminosUnicos.remove(x);
                except ValueError as e:
                    print str(e),x;
    #a = "'";
    #terminosProhibidos = []
    
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
    #        
    #for x in terminosProhibidos:   
    #    terminosUnicos.remove(x); 
        
    #for x in  terminosUnicos:
    #    if a in x:
    #         terminosUnicos.remove(x); 
    
    #a = "?";
    #terminosProhibidos = []
    #for x in terminosUnicos:
    #    if a in x:
    #        terminosProhibidos.append(x);
            
    #for x in terminosProhibidos:   
    #    terminosUnicos.remove(x); 
        
    #for x in  terminosUnicos:
    #    if a in x:
    #         terminosUnicos.remove(x);
                   
    matrizTemporalDocumento = [[0 for x in range(2)] for x in range(len(terminosUnicos))] 
    i = 0
    matrizDocumentoPrueba[j][0] = destino
   
    for termino in terminosUnicos:
        matrizTemporalDocumento[i][0] = termino
        matrizTemporalDocumento[i][1] = terminos.count(termino)
        i = i+1
    #print matrizTemporalDocumento    
        #Try del terminos
        try:
            indiceTermino = terminosUnicos2.index(termino)+1 #obtengo la pos. en el vocabulario corpus
            indiceTemporal =  terminosUnicos.index(termino) #Posicion de documento local
            #matrizDocumentoPrueba[j][indiceTermino] = matrizTemporalDocumento[indiceTemporal][1]*math.log(numeroDatos/frecuenciaInversa[indiceTermino-1][1])
            matrizDocumentoPrueba[j][indiceTermino] = z
            z = z+1
            #print termino,indiceTermino,indiceTemporal,matrizDocumentoPrueba
            destino = destino.replace(".xml", "");
            destino = destino.strip();
            for x in valoresVerdad2:
                if cmp(destino, x[0]) == 0:
                    matrizDocumentoPrueba[j][len(terminosUnicos2)+1] = x[1]
                    matrizDocumentoPrueba[j][len(terminosUnicos2)+2] = x[2]
            
        except ValueError as e:
            print str(e)
    j = j+1
    terminosUnicos = [] # Vaciar el buffer
    terminos = [] # Vaciar el buffer       
#print "Ded";

#Crear archivo arff para weka
myfile = open('archivoWekaPrueba.arff', 'wb')
myfile.write( "@RELATION archivo\n\n")

stringID = ""
#Obtener los identificadores
for id in range(len(matrizDocumentoPrueba)-1):
	#print matrizDocumento[id+1][0], id, len(matrizDocumento)-1
	if cmp(id+1, len(matrizDocumentoPrueba)-1):
		stringID = stringID +  matrizDocumentoPrueba[id+1][0] +","
	else:
		stringID = stringID +  matrizDocumentoPrueba[id+1][0]

myfile.write( "@ATTRIBUTE idUsuario {"+stringID+"}\n")
#print (stringID)

#Obtener el nombre de las clases
for id in  range(len(matrizDocumentoPrueba[0])-3):
	stringID = matrizDocumentoPrueba[0][id+1]
	try:
            stringID = stringID.encode('utf8','replace')
            myfile.write( "@ATTRIBUTE "+stringID+" REAL\n")
        except UnicodeError as e:
            print stringID,str(e)

#Renglon de clase
myfile.write( "@ATTRIBUTE claseUsuario {M,F}\n\n")
myfile.write( "@ATTRIBUTE claseEdad {18-24,25-34,35-49,50-XX}\n\n")

#print id+2
#Datos
myfile.write( "@DATA\n\n")	
#Datos de la matriz
stringData = ""
stringID = ""
for id in range(len(matrizDocumentoPrueba)-1):
#for id in range(1,91):
	for idj in range(len(matrizDocumentoPrueba[0])):
		stringData = str(matrizDocumentoPrueba[id+1][idj])
		if cmp(idj+1, len(matrizDocumentoPrueba[0])):
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