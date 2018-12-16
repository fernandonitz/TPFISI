import time
import datetime
   
FERIADOS = [20170227,20170324,20170414,20170501,20170525,20170620,20170817,20171012,20171120,20171208,20171225]
   
class MiTiempo:
	
	def definirTiempo(self,tiempo):
		res = self.desglozarTiempo(tiempo)
		self.año = res[0]
		self.mes = res[1]
		self.dia = res[2]
		self.hora = res[3]
		self.min = res[4]
		self.seg = res[5]
		
	def desglozarTiempo(self,tiempo):
		reg = tiempo.split(' ')
		date = reg[0]
		time = reg[1]
		reg = date.split('-')
		año = reg[0]
		mes = reg[1]
		dia = reg[2]
		reg = time.split('.')
		reg = reg[0]
		reg = reg.split(':')
		hora = reg[0]
		min = reg[1]
		seg = reg[2]
		return [año,mes,dia,hora,min,seg]
		
	def darHora(self):
		return self.hora

	def darDiaSemana(self):
		#L = 0, Ma = 1, Mi = 2, J = 3, V = 4, S = 5, D = 6
		return datetime.date(int(self.año),int(self.mes),int(self.dia)).weekday()
		
	def restarTiempos(self,tiempo2,tiempo1):
		#resta tiempo2 menos tiempo1
		formato_fecha = "%Y-%m-%d %H:%M:%S.%f"
		fechaInicial = time.mktime(time.strptime(tiempo1,formato_fecha))
		fechaFinal = time.mktime(time.strptime(tiempo2,formato_fecha))	
		dif = datetime.timedelta(seconds=fechaFinal-fechaInicial)
		hs = int(dif.seconds/3600)
		dias = dif.days
		horas = dias * 24 + hs
		#-----hasta aca comun
		regt1 = self.desglozarTiempo(tiempo1)
		regt2 = self.desglozarTiempo(tiempo2)
		w1 = datetime.date(int(regt1[0]),int(regt1[1]),int(regt1[2])).weekday()
		w2 = datetime.date(int(regt2[0]),int(regt2[1]),int(regt2[2])).weekday()
		
		aRestar = 0
		
		it = dif.days
		cantFinde = 0
		while it >= 7:	
			cantFinde = cantFinde + 2
			it = it - 7
		if w2 < w1:
			if w2 in [0,1,2,3,4] and w1 in [0,1,2,3,4]: 
				cantFinde = cantFinde + 2	
		
		reg1 = tiempo1.split(" ")
		
		if w1 == 5:
			if w2 in [5,6] : 
				return dif.days * 24 - self.cantDiasFeriados(tiempo2,tiempo1) * 24 - cantFinde * 24
			else: 
				fechaAux = time.mktime(time.strptime(reg1[0] + " " + "23:59:59.9",formato_fecha)) 
				dif = datetime.timedelta(seconds=fechaAux-fechaInicial)
				aRestar = 24 + int((dif.seconds+1)/3600)	
		
		if w1 == 6:
			if w2 in [5,6] : 
				return dif.days * 24 - self.cantDiasFeriados(tiempo2,tiempo1) * 24 - cantFinde * 24
			else:
				fechaAux = time.mktime(time.strptime(reg1[0] + " " + "23:59:59.9",formato_fecha)) 
				dif = datetime.timedelta(seconds=fechaAux-fechaInicial)
				aRestar = int((dif.seconds+1)/3600)
				
				
		#print (str(horas) + " " + str(aRestar) + " " + str(cantFinde))		
		return horas - aRestar - cantFinde * 24 - self.cantDiasFeriados(tiempo2,tiempo1) * 24
		
	def cantDiasFeriados(self,fecha2,fecha1):
		regt1 = self.desglozarTiempo(fecha1)
		regt2 = self.desglozarTiempo(fecha2)
		fec1 = regt1[0] + regt1[1] + regt1[2]
		fec2 = regt2[0] + regt2[1] + regt2[2]
		fec1 = int(fec1)
		fec2 = int(fec2)
		#print (str(fec2) + " " + str(fec1))
		cant = 0
		for feriado in FERIADOS:
			if feriado > fec1 and feriado < fec2:
				cant = cant + 1
		return cant


#asd = MiTiempo()
#asd.definirTiempo("2017-12-11 15:57:17.0")
#print(asd.darDiaSemana())
#print(asd.darHora())
#print (asd.restarTiempos("2017-12-13 16:00:00.0","2017-12-09 15:00:00.0"))
#print (asd.cantDiasFeriados("2017-12-13 16:00:00.0","2017-12-07 15:00:00.0"))
