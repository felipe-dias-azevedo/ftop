import psutil, time, sys, os

def convert(tipoDado):
	if tipoDado >= 1000 and tipoDado < 1000000:
		tipoDado = round((tipoDado / (2**10)))
		Metrica = "KiB/s"
		#print(infoSaida, tipoDado, "KiB/s")
	elif tipoDado >= 1000000:
		tipoDado = round((tipoDado / (2**20)),2)
		Metrica = "MiB/s"
		#print(infoSaida, tipoDado, "MiB/s")		
	else:
		Metrica = "Bytes/s"
		#print(infoSaida, tipoDado, "Bytes/s")
	return [tipoDado, Metrica]

def clearShellCommand():
	if sys.platform == 'linux' or sys.platform == 'darwin':
		limpar = 'clear'
	elif sys.platform == 'win32':
		limpar = 'cls'
	return limpar

def verificarWSL():
	if sys.platform == 'linux':
		if 'Microsoft' in os.uname()[2]:
			return True
		else:
			return False
	else:
		return False

def condHorario(hora):
	if 5 <= hora <= 12:
		condicao_hora = 'manhã'
	elif 13 <= hora <= 18:
		condicao_hora = 'tarde'
	else:
		condicao_hora = 'noite'
	return condicao_hora

def barraUso(uso, valorUso, tamanho = 2, limite = 100, tipo = "%"):
	carga = ''
	for i in range((tamanho - 1),int(uso),tamanho):
		carga += "#"
	for j in range(int(uso), limite, tamanho):
		carga += "."
	barra = "[" + carga + " " + str(valorUso) + " " + tipo + "]"
	return barra

def main():
	sistema = "windows" if sys.platform == 'win32' else sys.platform # TODO: FAZER ISTO PARA TODAS AS PLATAFORMAS
	limparTela = clearShellCommand()
	isWsl = verificarWSL() # TODO: REDIRECIONAR PARA VARIAVEL SISTEMA
	os.system(limparTela)
	lidaAntiga = psutil.disk_io_counters()
	netAntiga = psutil.net_io_counters()
	TempoBoot = psutil.boot_time()
	loop = True
	porCPU = input("\nVer percentual de uso de CPUs por núcleo? [Y/n] ")
	porCPU = True if porCPU.lower() == 'y' else False
	print("\n", end="")
	print("\nIniciando as leituras do Hardware no Sistema Operacional", sistema.capitalize(), "\n")
	while loop:
		time.sleep(1) # EXECUTA A CADA 1 SEGUNDO
		horario = time.localtime()
		os.system(limparTela)
		#usoAtual = psutil.cpu_percent()
		#print("Uso atual de CPU: ", usoAtual, "%")
		
		#print(('0' if horario[3] < 10 else '') + str(horario[3]) + (':0' if horario[4] < 10 else ':') + str(horario[4]), "da", condHorario(horario[3]), "em", sistema.capitalize())
		
		DifTempo = (time.time()) - TempoBoot
		HorasLigado = int(DifTempo // 3600)
		MinutosLigado = int((DifTempo // 60)) if HorasLigado < 1 else int((DifTempo - (HorasLigado * 3600)) / 60)
		SegundosLigado = int((DifTempo)) if MinutosLigado < 1 else int((DifTempo - ((MinutosLigado * 60) + (HorasLigado * 3600))))
		print("Uptime em " + sistema.capitalize() + (': 0' if HorasLigado < 10 else ': ') + (str(HorasLigado) + (':0' if MinutosLigado < 10 else ':') + str(MinutosLigado) + (':0' if SegundosLigado < 10 else ':') + str(SegundosLigado)))

		qtdTarefas = len(psutil.pids())
		print(qtdTarefas, "processos em execução no momento\n")

		if sistema == 'linux' and not isWsl:
			tempCPU = psutil.sensors_temperatures(fahrenheit=False)
			tempCPU = tempCPU.get('coretemp')
			print("Temperatura do CPU:", int(tempCPU[0][1]), "ºC")
	
		if not isWsl:
			freqCPU = psutil.cpu_freq()
			print("Frequência do CPU:", int(freqCPU[0]), "MHz de", int(freqCPU[2]), "MHz")

		if porCPU:
			usoCPUs = psutil.cpu_percent(percpu=True)
			for nucleo in range(len(usoCPUs)):
				print("Núcleo " + str(int(nucleo)+1) + ": " + barraUso(usoCPUs[nucleo], usoCPUs[nucleo], 4))
		else:
			usoAtual = psutil.cpu_percent(percpu=False)
			print("Uso de CPU: " + barraUso(usoAtual, usoAtual, 4))

		usoRAM = psutil.virtual_memory()
		totalram = usoRAM[0]
		usoGBram = round(((totalram - usoRAM[1]) / (2**30)),2)
		print("\nUso da Memória RAM:", usoGBram, "GB de", round(totalram / (2**30),2), "GB")
		print(barraUso(usoRAM[2], usoRAM[2]))

		swapRAM = psutil.swap_memory()
		totalswap = swapRAM[0]
		usoGBswap = round(((swapRAM[0] - swapRAM[2]) / (2**30)),2)
		print("Uso do SWAP:", usoGBswap, "GB de", round((totalswap / (2**30)),2), "GB")
		print(barraUso(swapRAM[3], swapRAM[3]))

		if not isWsl:

			lidaAtual = psutil.disk_io_counters()

			BytesLidos = round((lidaAtual[2] - lidaAntiga[2]))
			#convert("\nLeitura do HD:", BytesLidos)
			conversaoMetricas = convert(BytesLidos)
			print("\nLeitura do HD:", conversaoMetricas[0], conversaoMetricas[1])

			BytesEscritos = round((lidaAtual[3] - lidaAntiga[3]))
			#convert("Escritura do HD:", BytesEscritos)
			conversaoMetricas = convert(BytesEscritos)
			print("Escritura do HD:", conversaoMetricas[0], conversaoMetricas[1])
			print("")
			
			lidaAntiga = lidaAtual

			sdaLido = False
			infoHD = psutil.disk_partitions()
			for part in range(len(infoHD)):
				ordemNum = 97
				if ('snap' not in infoHD[part][1] and 'cdrom' not in infoHD[part][3]):
					usoHD = psutil.disk_usage(infoHD[part][1]) # uso de 'sda1'
					sdTot = [0]

					if sys.platform == 'linux':
						for i in range(len(infoHD)):
							if ('sd' + chr(ordemNum)) in infoHD[i][0]:
								sdTot[0] += usoHD[1]
								if 'sda' in infoHD[i][0] and not sdaLido:
									sdTot[0] += swapRAM[0]
									sdaLido = True
									print("Ocupação de", infoHD[part][1], (("em " + infoHD[part][0]) + " :"), round((sdTot[0] - swapRAM[0]) / (2**30),2), "GB de", round(usoHD[0] / (2**30),2), "GB")
								else:
									print("Ocupação de", infoHD[part][1], (("em " + infoHD[part][0]) + " :"), round(sdTot[0] / (2**30),2), "GB de", round(usoHD[0] / (2**30),2), "GB")
						usoPercent = round(((1 - ((usoHD[0] - sdTot[0]) / usoHD[0])) * 100),1) #TODO: ARRUMAR QUANDO FOR PARTIÇÃO '/' ADICIONAR O SWAP QUE USA DO DISCO.
						print(barraUso(usoPercent, usoPercent))
						ordemNum += 1
					else:
						print("Ocupação de", infoHD[part][1], (("em " + infoHD[part][0]) if not sistema == 'windows' else '') + ":", round(usoHD[1] / (2**30),2), "GB de", round(usoHD[0] / (2**30),2), "GB")
						print(barraUso(usoHD[3], usoHD[3]))
					
					

			netAtual = psutil.net_io_counters()

			BytesRecebidos = round((netAtual[1] - netAntiga[1]))
			conversaoMetricas = convert(BytesRecebidos)
			#convert("\nTaxa Download:", BytesRecebidos)
			print("\nTaxa Download:", conversaoMetricas[0], conversaoMetricas[1])

			BytesEnviados = round((netAtual[0] - netAntiga[0]))
			conversaoMetricas = convert(BytesEnviados)
			#convert("Taxa Upload:", BytesEnviados)
			print("Taxa Upload:", conversaoMetricas[0], conversaoMetricas[1])
			
			netAntiga = netAtual

		print("-" * os.get_terminal_size()[0])
	
main()
