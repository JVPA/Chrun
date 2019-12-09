class API:

	def elTiempo_api(self):
		from elTiempo import keys
		API = keys.Configuracion()
	

		Token = API.Token
		Url = API.Url + 'appid=' + API.Token + '&zip=' + API.Zip_Code + ',' + API.Country 

		return Url
	
	def refresh(self):
		import requests, json, datetime
		import pandas as pd
				
		Url = self.elTiempo_api()
		
		response = requests.get(Url) 
		datos = response.json() 
		
		df = pd.DataFrame(columns=['Fecha', 'DiaSem', 'Hora', 'Temp.', 'Tiempo','Lluvia','Presion','Icono'])	
		i = 0
		if datos['cod'] != '404': 
			weather = datos['list']
			for dt in weather:
				lluvia = None
				fecha = datetime.datetime.fromtimestamp(dt['dt']).strftime('%Y-%m-%d')
				hora = datetime.datetime.fromtimestamp(dt['dt']).strftime('%H:%M')
				DiaSem = (datetime.datetime.fromtimestamp(dt['dt']) ).weekday()
				temperatura = round(dt['main']['temp'] - 273.15,2)
				presion = dt['main']['pressure']
				icono = dt['weather'][0]['icon']
				tiempo = dt['weather'][0]['description']
				if 'rain' in dt:
					if '3h' in dt['rain']:
						lluvia = dt['rain']['3h']
					
				df.loc[i] = [fecha, DiaSem, hora, temperatura, tiempo, lluvia, presion, icono]
				i += 1
				
		df = df[(df['Lluvia'] > 0.1)
			& (df['DiaSem'] < 5) 
			& (df['Fecha'] <= str(datetime.date.today() + datetime.timedelta(days = 1)))  # en el día y día + 1
			& (df['Hora'] > '0' + str( datetime.timedelta(hours = 7)))   # La hora de las lluvias después de las 08:00
			& (df['Hora'] < str( datetime.timedelta(hours = 20)))  ]   # La hora de las lluvias antes de las 19:00 

		return df
