import psutil, time, sys, os

def convert(infoSaida, tipoDado):
	if tipoDado >= 1000 and tipoDado < 1000000:
		KB = round((tipoDado / (2**10)))
		print(infoSaida, KB, "KB/s")
	elif tipoDado >= 1000000:
		MB = round((tipoDado / (2**20)),2)
		print(infoSaida, MB, "MB/s")		
	else:
		print(infoSaida, tipoDado, "Bytes/s")

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
		convert("\nLeitura do HD:", BytesLidos)

		BytesEscritos = round((lidaAtual[3] - lidaAntiga[3]))
		convert("Escritura do HD:", BytesEscritos)
		
		lidaAntiga = lidaAtual

		infoHD = psutil.disk_partitions()
		for part in range(len(infoHD)):
			if ('snap' not in infoHD[part][1]):
				usoHD = psutil.disk_usage(infoHD[part][1])
				print("Ocupação de", infoHD[part][1], "em", infoHD[part][0], ":", usoHD[3], "%")
			
		netAtual = psutil.net_io_counters()

		BytesRecebidos = round((netAtual[0] - netAntiga[0]))
		convert("\nTaxa Download:", BytesRecebidos)

		BytesEnviados = round((netAtual[1] - netAntiga[1]))
		convert("Taxa Upload:", BytesEnviados)
		
		netAntiga = netAtual

		print("----------------------------------------------------------------------")
	
main()
