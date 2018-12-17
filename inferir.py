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
	arch = open(RUTA + "\\testSet.csv",'r')
	#it = [0,0,0]
	cp = miCodigosPostales.MiCodigoPostal()

	cant = 0
	aciertos = 0

	for linea in arch:
		reg = linea.split(',')
		fechaHoraDespacho		=reg[11]
		fechaHoraAprobacion     =reg[4]
		idVend                  =reg[6]
		categ 					=reg[8]
		zipCode  				=reg[9]	
		#datos  = normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,it,cp)
		datos  = normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,cp, fechaHoraDespacho)
		k = len(datos)
		#it = datos[k-1]
		#datos = datos[:k-1]
		cantEstimada = adivinar(datos[:k-1],adivinadores)#,idVend,vendedores)
		#print ("dias estimadas: " + str(cantEstimada) + " ,dias reales: " + str(datos[k-1]))
		if round(cantEstimada) == int(datos[k-1]) :
			aciertos = aciertos + 1
		cant = cant + 1
		#print(cantEstimada)
	print("Se predijieron " + str(cant) + " registos.")
	print("Se acertaron " + str (aciertos) + " registros.")
	print("El porcentaje de aciertos es: " + str(aciertos/cant) + "%.")

	arch.close()

#def normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,it,cp):
def normalizarDatos(fechaHoraAprobacion,idVend,categ,zipCode,cp,fechaHoraDespacho):
	unTiempo = miTiempo.MiTiempo()
	unTiempo.definirTiempo(fechaHoraAprobacion)
	
	horaAprobacion = unTiempo.darHora()
	horaAprobacion = int(horaAprobacion)
	diaAprobacion = unTiempo.darDiaSemana()
	tTot = unTiempo.restarTiempos(fechaHoraDespacho,fechaHoraAprobacion)
	#hTTot = 0
	#if(tTot<24):hTTot = 1
	#elif(24<= tTot < 48):hTTot = 2
	#elif(48<= tTot < 72):hTTot = 3
	#else:hTTot = 4

	hTTot = 0
	if(0 <= tTot < 48):hTTot = 1
	elif(48 <= tTot < 96):hTTot = 2
	elif(96 <= tTot < 144):hTTot = 3
	else: hTTot = 4
	
	nVend = -1
	if idVend in hVend:
		nVend = hVend[idVend]

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
	return  [horaAprobacion,diaAprobacion,nCodZip,nVend,hTTot]	
	
def promediar(resultados):
	l = len(resultados)	
	res = 0
	for elem in resultados:
		res = res + elem
	return res/l
	
hVend = upload("hVend")
#hCateg = upload("hCateg")

oKnn = upload("knn")
oPerc = upload("perceptron")
#oKmeans = upload("kmeans")
oRF = upload("randomForest")

#vendedores = levantarVendedores()
adivinadores = [oKnn,oPerc,oRF]
#adivinadores = [oKmeans]	
#main(adivinadores,vendedores)	
main(adivinadores)#,vendedores)
	
	
	
	
	
	