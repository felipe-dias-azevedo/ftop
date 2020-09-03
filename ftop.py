import psutil, time, sys, os
def main():
	sistema = sys.platform
	lidaAntiga = psutil.disk_io_counters()
	netAntiga = psutil.net_io_counters()
	loop = True
	print("\nIniciando as leituras do Hardware no Sistema Operacional", sistema.capitalize(), "\n")
	while loop:
		time.sleep(1) # EXECUTA A CADA 1 SEGUNDO
		if sistema == 'linux':
			os.system('clear')
		elif sistema == 'win32':
			os.system('cls')
		#usoAtual = psutil.cpu_percent()
		#print("Uso atual de CPU: ", usoAtual, "%")
			
		freqCPU = psutil.cpu_freq()
		print("Frequência do CPU:", int(freqCPU[0]), "MHz de", int(freqCPU[2]), "MHz")

		if sistema == 'linux':
			tempCPU = psutil.sensors_temperatures(fahrenheit=False)
			tempCPU = tempCPU.get('coretemp')
			print("Temperatura do CPU:", int(tempCPU[0][1]), "ºC")
			
		usoCPUs = psutil.cpu_percent(percpu=True)
		print("\nUso de CPU")
		for nucleo in range(len(usoCPUs)):
			print("Núcleo", nucleo, ":",  usoCPUs[nucleo], "%")
			
		usoRAM = psutil.virtual_memory()
		totalGBram = round(usoRAM[0] / (2**30),2)
		usoGBram = round(((totalGBram) - usoRAM[1] / (2**30)),2)
		print("\nUso da Memória RAM:", usoRAM[2], "% (", usoGBram, "GB de", totalGBram, "GB )")

		swapRAM = psutil.swap_memory()
		totalGBswap = round(swapRAM[0] / (2**30),2)
		usoGBswap = round(((swapRAM[0] / (2**30)) - swapRAM[2] / (2**30)),2)
		print("Uso do SWAP:", swapRAM[3], "% (", usoGBswap, "GB de", totalGBswap, "GB )")

		lidaAtual = psutil.disk_io_counters()

		BytesLidos = round((lidaAtual[2] - lidaAntiga[2]))
		if BytesLidos >= 1000 and BytesLidos < 1000000:
			KBlidos = round((BytesLidos / (2**10)))
			print("\nLeitura do HD:", KBlidos, "KB/s")
		elif BytesLidos >= 1000000:
			MBlidos = round((BytesLidos / (2**20)),2)
			print("\nLeitura do HD:", MBlidos, "MB/s")		
		else:
			print("\nLeitura do HD:", BytesLidos, "Bytes/s")

		BytesEscritos = round((lidaAtual[3] - lidaAntiga[3]))
		if BytesEscritos >= 1000 and BytesEscritos < 1000000:
			KBescritos = round((BytesEscritos / (2**10)))
			print("Escritura do HD:", KBescritos, "KB/s")
		elif BytesEscritos >= 1000000:
			MBescritos = round((BytesEscritos / (2**20)),2)
			print("Escritura do HD:", MBescritos, "MB/s")
		else:
			print("Escritura do HD:", BytesEscritos, "Bytes/s")
		
		lidaAntiga = lidaAtual

		infoHD = psutil.disk_partitions()
		for part in range(len(infoHD)):
			if ('snap' not in infoHD[part][1]):
				usoHD = psutil.disk_usage(infoHD[part][1])
				print("Ocupação de", infoHD[part][1], "em", infoHD[part][0], ":", usoHD[3], "%")
			
		netAtual = psutil.net_io_counters()

		BytesRecebidos = round((netAtual[0] - netAntiga[0]))
		if BytesRecebidos >= 1000 and BytesRecebidos < 1000000:
			KBRecebidos = round((BytesRecebidos / (2**10)))
			print("\nTaxa Download:", KBRecebidos, "KB/s")
		elif BytesRecebidos >= 1000000:
			MBRecebidos = round((BytesRecebidos / (2**20)),2)
			print("\nTaxa Download:", MBRecebidos, "MB/s")		
		else:
			print("\nTaxa Download:", BytesRecebidos, "Bytes/s")

		BytesEnviados = round((netAtual[1] - netAntiga[1]))
		if BytesEnviados >= 1000 and BytesEnviados < 1000000:
			KBEnviados = round((BytesEnviados / (2**10)))
			print("Taxa Upload:", KBEnviados, "KB/s")
		elif BytesEnviados >= 1000000:
			MBEnviados = round((BytesEnviados / (2**20)),2)
			print("Taxa Upload:", MBEnviados, "MB/s")		
		else:
			print("Taxa Upload:", BytesEnviados, "Bytes/s")
		
		netAntiga = netAtual

		print("----------------------------------------------------------------------")
			
main()
