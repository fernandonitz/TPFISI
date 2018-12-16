import time
#import zipcode
import miTiempo
import miCodigosPostales
import os.path
import shutil
import json

from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import perceptron

import pickle

hVend = {}
hCateg = {}
vendedores = []

RUTA = os.getcwd()
#RUTA = "e:\\fernandon\\Desktop\\ML"

def main ():
	hVendedores = {}
	print (time.strftime('%H:%M:%S')) 
	cp = miCodigosPostales.MiCodigoPostal()
	arch = open(RUTA + "\\trainSet.csv",'r')
	archNor = open(RUTA + "\\normalizado.txt",'w')
	#it = [0,0,0]
	i = 0
	j = 0
	for linea in arch:
		reg = linea.split(',')
		fechaHoraAprobacion     =reg[4]
		idVend                  =reg[6]
		categ 					=reg[8]
		zipCode  				=reg[9]
		fechaHoraDespacho       =reg[11]
		if i > 0:	 
			datos  = normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,fechaHoraDespacho,cp)
			k = len(datos)
			#it = datos[k-1]
			#datos = datos[:k-1]
			datos = datos[:k]
			aEsc = ""
			#for elem in range(k-1):
			for elem in range(k):
				if elem == 0:					
					aEsc = aEsc + str(datos[elem])
				else: 
					aEsc =  aEsc + "," + str(datos[elem])
		
			archNor.write( aEsc + "\n")
					
			#if not idVend in hVendedores:
			#	reg = []
			#	reg.append(datos)
			#	hVendedores[idVend] = reg
			#else:
			#	reg = hVendedores[idVend]
			#	reg.append(datos)
			#	hVendedores[idVend] = reg
		
		#if j == 15000:
		#	print ("se procesaron " + str(i) + " registros...")
		#	guardarHashEnJson(hVendedores)
		#	hVendedores = {}
		#	j = 0
		
		j = j + 1		
		i = i + 1
		
	#dump(hVend,"hVend")
	#dump(hCateg,"hCateg")	
	#guardarVendedores()	
	arch.close()
	archNor.close()
	print (time.strftime('%H:%M:%S'))

#def normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,fechaHoraDespacho,it,cp):
def normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,fechaHoraDespacho,cp):
	
	unTiempo = miTiempo.MiTiempo()
	unTiempo.definirTiempo(fechaHoraAprobacion)
	
	horaAprobacion = unTiempo.darHora()
	horaAprobacion = int(horaAprobacion)
	diaAprobacion = unTiempo.darDiaSemana()
	tTot = unTiempo.restarTiempos(fechaHoraDespacho,fechaHoraAprobacion)
	
	#if not idVend in hVend:
	#	hVend[idVend] = it[0]
	#	nVend = it[0]
	#	it[0] = it[0] + 1
	#else:
	#	nVend = hVend[idVend]
	#	
	#if not categ in hCateg:
	#	hCateg[categ] = it[1]
	#	nCateg = it[1]
	#	it[1] = it[1] + 1
	#else:
	#	nCateg = hCateg[categ]

	hTTot = 0
	if(tTot<24):hTTot = 1
	elif(24<= tTot < 48):hTTot = 2
	elif(48<= tTot < 72):hTTot = 3
	elif(72<= tTot < 96):hTTot = 4
	else:hTTot = 5

	nCodZip = cp.darProv(str(zipCode))
	#print (str(zipCode))
	#print (nCodZip)
	 
	#nit = [it[0],it[1],it[2]]
	#return  [horaAprobacion,diaAprobacion,nVend,nCateg,nCodZip,tTot,nit]
	#return  [horaAprobacion,diaAprobacion,nCateg,tTot,nit]
	return  [horaAprobacion,diaAprobacion,nCodZip,hTTot]
	
def recorrerNormalizado():
	res = []
	x = []
	y = []
	archivo = open(RUTA + "\\normalizado.txt",'r')
	registros = archivo.readlines()
	for registro in registros:
		registro = registro.rstrip('\n')
		registro = registro.split(',')
		l = len(registro)
		y1 = int(registro[l-1])
		x1 = []
		for i in range(l-1):
			x1.append(int(registro[i]))
		x.append(x1)
		y.append(y1)
	archivo.close()
	res.append(x)
	res.append(y)
	return res	

def promDistancia(vec1,vec2):
	if not len(vec1) == len(vec2):
		return 0
	suma = 0
	for i in range(len(vec1)):
		if vec1[i] < vec2[i]: suma = suma + vec2[i] - vec1[i]
		else: suma = suma + vec1[i] - vec2[i]
	return suma/len(vec2)
	
def crearEscritorio(ruta):
	if not os.path.exists(ruta):
		os.mkdir(ruta)
	else:
		shutil.rmtree(ruta)
		time.sleep(2)
		os.mkdir(ruta)		
	
#Almacenado de datos

def guardarVendedores():
	ruta = RUTA + "\\vendedores\\Vendedores.json"
	data = {
		'vendedores' : vendedores
	}
	with open(ruta, 'w') as file:
		json.dump(data, file)

def guardarEnJson(vendedor,datos):
	
	ruta = RUTA + "\\vendedores\\" + vendedor + ".json"
	#horaAprobacion,diaAprobacion,nCateg,tTot cliente
	#print (datos)
	if os.path.isfile(ruta):
		with open(ruta, 'r') as file:
			data = json.load(file)
			compras = data["compras"]
			cantReg = data["cantReg"]
			for dato in datos:
				nuevoMov = {
					'cantHs': dato[3],
					'weekday': dato[1],
					'hora': dato[0],
					'categ': dato[2]
					
				}
				compras.append(nuevoMov)
			cantReg = cantReg + len(datos)	
			data["cantReg"] = cantReg
			data["compras"] = compras			
			
	else:
		#data = """{'idVend' : '""" + cliente + """','cantReg' : 1,'compras' : [{'cantHs': """ + str(datos[0]) + """,'weekday':""" + str(datos[1]) + """,'hora':' """+ str(datos[2]) + """'}]}"""
		vendedores.append(vendedor)
		movs = []
		for dato in datos:
			nuevoMov = {
				'cantHs': dato[3],
				'weekday': dato[1],
				'hora': dato[0],
				'categ': dato[2]
			}
			movs.append(nuevoMov)
		data = {
			'idVend' : vendedor,
			'cantReg' : len(datos),
			'compras' : movs
		}
		
	with open(ruta, 'w') as file:
		json.dump(data, file)
	
def guardarHashEnJson(hashVend):
	vends = hashVend.keys()
	for vend in vends:
		guardarEnJson(vend, hashVend[vend])

def dump(obj,nombre):
	with open(nombre + ".pickle", 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def upload(nombre):
	with open(nombre + ".pickle", 'rb') as f:
		return pickle.load(f)
	
#Metodos de Inferencia
	
def Svc(x,y,r):
	C = 1.0  # parametro de regulacion SVM 
	
	if r == 1:svc = svm.SVC(kernel='linear', C=C).fit(x, y)
	if r == 2:svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(x, y)
	if r == 3:svc = svm.SVC(kernel='poly', degree=3, C=C).fit(x, y)
	if r == 4:svc = svm.LinearSVC(C=C).fit(x, y)

	#print("precisión del modelo: {0: .2f}".format((y == svc.predict(x)).mean()))

	return svc

def randomForest(x,y):
	rf = RandomForestClassifier() # Creando el modelo
	rf.fit(x,y) # Ajustando el modelo
	#print("precisión del modelo: {0: .2f}".format((y == rf.predict(x)).mean()))
	return rf	

def kmeans(x,y):
	k = 7
	for i in range(k):
		p = x[y == i]
		#print (p)
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(x) # Ajustando el modelo
	return kmeans

def knn(x,y):
	knnr = KNeighborsRegressor(n_neighbors=100) # Creando el modelo con 10 vecinos
	knnr.fit(x, y) # Ajustando el modelo
	#print("El error medio del modelo es: {:.2f}".format(np.power(y - knnr.predict(x),2).mean()))
	return knnr
	
def fperceptron(x,y):	
	#perc = perceptron.Perceptron(None,0.00001,True,None,0.01,True,0,1.0,1,0,None,False,None)
	perc = perceptron.Perceptron()
	perc.fit(x,y)
	#print('accuracy:', clf.score(train_data, train_answers))
	return perc
		
#crearEscritorio(RUTA + "\\vendedores")
	
main()	
xy = recorrerNormalizado()
x = xy[0]
y = xy[1]

print ("Entrenando al perceptron...")
objInferencia = fperceptron(x,y)
dump(objInferencia,"perceptron")

print ("Entrenando al kmeans...")
objInferencia = kmeans(x,y)
dump(objInferencia,"kmeans")

print ("Entrenando al knn...")
objInferencia = knn(x,y)
dump(objInferencia,"knn")



	