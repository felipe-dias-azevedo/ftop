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
	sistema = sys.platform
	limparTela = clearShellCommand()
	os.system(limparTela)
	lidaAntiga = psutil.disk_io_counters()
	netAntiga = psutil.net_io_counters()
	loop = True
	print("\nIniciando as leituras do Hardware no Sistema Operacional", sistema.capitalize(), "\n")
	while loop:
		time.sleep(1) # EXECUTA A CADA 1 SEGUNDO
		horario = time.localtime()
		os.system(limparTela)
		#usoAtual = psutil.cpu_percent()
		#print("Uso atual de CPU: ", usoAtual, "%")
		
		print(('0' if horario[3] < 10 else '') + str(horario[3]) + (':0' if horario[4] < 10 else ':') + str(horario[4]), "da", condHorario(horario[3]), "em", sistema.capitalize())

		qtdTarefas = len(psutil.pids())
		print(qtdTarefas, "em execução no momento\n")

		if sistema == 'linux':
			tempCPU = psutil.sensors_temperatures(fahrenheit=False)
			tempCPU = tempCPU.get('coretemp')
			print("Temperatura do CPU:", int(tempCPU[0][1]), "ºC")
			
		freqCPU = psutil.cpu_freq()
		print("Frequência do CPU:", int(freqCPU[0]), "MHz de", int(freqCPU[2]), "MHz")

		usoCPUs = psutil.cpu_percent(percpu=True)
		usoAtual = psutil.cpu_percent()
		#print("\nUso de CPU:  "+barraUso(usoAtual, 3))
		for nucleo in range(len(usoCPUs)):
			#print("Núcleo", nucleo, ":",  usoCPUs[nucleo], "%")
			print("Núcleo " + str(int(nucleo)+1) + ": " + barraUso(usoCPUs[nucleo], usoCPUs[nucleo], 4))
			
		usoRAM = psutil.virtual_memory()
		totalGBram = round(usoRAM[0] / (2**30),2)
		usoGBram = round(((totalGBram) - usoRAM[1] / (2**30)),2)
		print("\nUso da Memória RAM:", usoGBram, "GB de", totalGBram, "GB")
		print(barraUso(usoRAM[2], usoRAM[2]))

		swapRAM = psutil.swap_memory()
		totalGBswap = round(swapRAM[0] / (2**30),2)
		usoGBswap = round(((swapRAM[0] / (2**30)) - swapRAM[2] / (2**30)),2)
		print("Uso do SWAP:", usoGBswap, "GB de", totalGBswap, "GB")
		print(barraUso(swapRAM[3], swapRAM[3]))

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

		infoHD = psutil.disk_partitions()
		for part in range(len(infoHD)):
			if ('snap' not in infoHD[part][1] and 'cdrom' not in infoHD[part][3]):
				usoHD = psutil.disk_usage(infoHD[part][1])
				print("Ocupação de", infoHD[part][1], "em", infoHD[part][0], ":", usoHD[3], "%")
			
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

		print("-" * 80)
	
main()
