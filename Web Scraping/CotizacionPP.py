
from BbDd import conexion

def getdata(Plan):
	from bs4 import BeautifulSoup
	from datetime import datetime
	import urllib3
	import re
	
	url = 'https://www.bankia.es/es/particulares/ahorro-e-inversion/planes-de-pensiones/buscador-planes/bankia-' + Plan[0]
	urllib3.disable_warnings()
	http = urllib3.PoolManager()
	response = http.request('GET', url)
	
	soup = BeautifulSoup(response.data, 'html.parser')
	links = soup.find_all(True, {'class':['lst-item-text last data-value'],'data-value':['€']})
	for tag in links:
		for i in tag:
			cotizacion = i
			
	links = soup.find_all(True, {'class':['lst-item-text']})
	for tag in links:
		for i in tag:
			if 'Valor liquidativo del fondo a' in i:
				fecha = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", i)
				
	return Plan[1], cotizacion, datetime.strptime(fecha[0], '%d/%m/%Y')	
					
Planes = [['flexible','FuturPension'],['moderado','Bcj. R. Fija Mixta']]
bd = conexion.PythonDb()
for Plan in Planes:
	PP, Valor, Fecha = getdata(Plan)
	
	StrQuery =  'UPDATE bbdd.tabla SET Cotizacion = ' +  str(Valor).replace(',','.') + ' , UltActu = "' + str(Fecha) + '" where Plan = "' + PP + '"'
	Recordset = bd.ejecutaSql(StrQuery)
