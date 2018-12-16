import pickle
import json
import os
import miTiempo
import miCodigosPostales
RUTA = os.getcwd()

def upload(nombre):
	with open(nombre + ".pickle", 'rb') as f:
		return pickle.load(f)
		
def levantarVendedores():
	ruta = RUTA + "\\vendedores\\Vendedores.json"
	with open(ruta, 'r') as file:
		data = json.load(file)	
	return data["vendedores"]			

def traerHis(usuario):
	ruta = RUTA + "\\vendedores\\" + usuario + ".json"
	with open(ruta, 'r') as file:
		data = json.load(file)
	cReg = data["cantReg"]	
	compras = data["compras"]	
	vCompras = []
	for elem in compras:
		reg = []
		reg.append(elem["cantHs"])
		reg.append(elem["weekday"])
		reg.append(elem["hora"])
		reg.append(elem["categ"])
		vCompras.append(reg)
	return vCompras
	
def adivinar(reg,adivinadores):#,idVend,vendedores):
	resultado = []
	for adivinador in adivinadores:
		aAdivinar = []
		aAdivinar.append(reg)
		res = adivinador.predict(aAdivinar)
		resultado.append(res[0])
	promedio = promediar(resultado)
	
	#if idVend in vendedores:
	#	reg = traerHis(idVend)
	#	Ehis = sacarEsperanzaHis(reg)
	#	Vhis = sacarVarianzaHis(reg,Ehis)
	#	l = len(reg)
	#	n = ponderar(Ehis,Vhis,l)
	#	return Ehis * n + promedio * (1 - n)	
	#else:
	return promedio
	
	
def ponderar(E,V,l):
	#cantHs,weekday,hora,categ
	pond = 0
	if l < 10:
		if E < V:
			pond = 0.3
		else:
			pond = 0.5
	else:
		if l < 50:
			if E < V:
				pond = 0.6
			else:
				pond = 0.8
		else:
			if E < V:
				pond = 0.9
			else:
				pond = 1
	return pond
	
def sacarEsperanzaHis(reg):		
	#cantHs,weekday,hora,categ
	E = 0
	l = len(reg)
	for elem in reg:
		E = E + elem[0]
	return E/l
	
def sacarVarianzaHis(reg,E):
	#cantHs,weekday,hora,categ
	V = 0
	l = len(reg)
	for elem in reg:
		V = V + ((elem[0] - E) * (elem[0] - E))
	return V/l

#def main(adivinadores,vendedores):
def main(adivinadores):#,vendedores):
	arch = open(RUTA + "\\aAdivinar.csv",'r')
	#it = [0,0,0]
	cp = miCodigosPostales.MiCodigoPostal()
	for linea in arch:
		reg = linea.split(',')
		fechaHoraAprobacion     =reg[4]
		idVend                  =reg[6]
		categ 					=reg[8]
		zipCode  				=reg[9]	
		#datos  = normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,it,cp)
		datos  = normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,cp)
		#k = len(datos)
		#it = datos[k-1]
		#datos = datos[:k-1]
		cantEstimada = adivinar(datos,adivinadores)#,idVend,vendedores)
		print (cantEstimada)
		
	arch.close()

#def normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,it,cp):
def normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,cp):
	unTiempo = miTiempo.MiTiempo()
	unTiempo.definirTiempo(fechaHoraAprobacion)
	
	horaAprobacion = unTiempo.darHora()
	horaAprobacion = int(horaAprobacion)
	diaAprobacion = unTiempo.darDiaSemana()
	
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

	nCodZip = cp.darProv(str(zipCode))
	#print (str(zipCode))
	#print (nCodZip)
	
	#nit = [it[0],it[1],it[2]]
	#return  [horaAprobacion,diaAprobacion,nVend,nCateg,nCodZip,tTot,nit]
	#return  [horaAprobacion,diaAprobacion,nCateg,nit]	
	return  [horaAprobacion,diaAprobacion,nCodZip]	
	
def promediar(resultados):
	l = len(resultados)	
	res = 0
	for elem in resultados:
		res = res + elem
	return res/l
	
#hVend = upload("hVend")
#hCateg = upload("hCateg")
oKnn = upload("knn")
oPerc = upload("perceptron")
oKmeans = upload("kmeans")

#vendedores = levantarVendedores()
adivinadores = [oKnn,oPerc,oKmeans]
	
#main(adivinadores,vendedores)	
main(adivinadores)#,vendedores)
	
	
	
	
	
	