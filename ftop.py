import GPUtil
import psutil
import time
from performance.sysos import OsSys, WSL
from performance.console_utils import get_usage_bar
from performance.byte_utils import get_byte_type


def main():
    system = OsSys(boot_time=psutil.boot_time())
    system.os_clear()

    old_disk_read = psutil.disk_io_counters()
    old_net = psutil.net_io_counters()

    per_cpu = input("\nVer percentual de uso de CPUs por núcleo? [Y/n] ")
    per_cpu = True if per_cpu.lower() == 'y' else False

    print()
    print("\nIniciando as leituras do Hardware no Sistema Operacional", system.systype, "\n")

    while True:
        time.sleep(1)  # EXECUTA A CADA 1 SEGUNDO
        system.os_clear()

        print(system.get_uptime())

        pids_count = len(psutil.pids())
        print(pids_count, "processos em execução no momento\n")

        if psutil.LINUX and system.systype != WSL:
            cpu_temperature = psutil.sensors_temperatures(fahrenheit=False)
            cpu_temperature = cpu_temperature.get('coretemp')
            if bool(cpu_temperature):
                print("Temperatura do CPU:", int(cpu_temperature[0][1]), "ºC")

        if system.systype != WSL:
            cpu_frequency = psutil.cpu_freq()  # TODO: colocar frequencia por CPU (se tiver no psutil)
            print("Frequência do CPU:", int(cpu_frequency[0]), "MHz de", int(cpu_frequency[2]), "MHz")

        if per_cpu:
            cpu_usage = psutil.cpu_percent(percpu=True)
            for nucleo in range(len(cpu_usage)):
                print("Núcleo " + str(int(nucleo) + 1) + ": " + get_usage_bar(cpu_usage[nucleo], cpu_usage[nucleo], 4))
        else:
            cpu_usage = psutil.cpu_percent(percpu=False)
            print("Uso de CPU: " + get_usage_bar(cpu_usage, cpu_usage, 4))

        ram_usage = psutil.virtual_memory()
        totalram = ram_usage[0]
        usage = round(((totalram - ram_usage[1]) / (2 ** 30)), 2)
        print("\nUso da Memória RAM:", usage, "GB de", round(totalram / (2 ** 30), 2), "GB")
        print(get_usage_bar(ram_usage[2], ram_usage[2]))

        swap_usage = psutil.swap_memory()
        totalswap = swap_usage[0]
        usage = round(((swap_usage[0] - swap_usage[2]) / (2 ** 30)), 2)
        print("Uso do SWAP:", usage, "GB de", round((totalswap / (2 ** 30)), 2), "GB")
        print(get_usage_bar(swap_usage[3], swap_usage[3]))
        print()

        if system.systype != WSL:

            disk_read = psutil.disk_io_counters()

            disk_bytes_read = round((disk_read[2] - old_disk_read[2]))
            metric = get_byte_type(disk_bytes_read)
            print("Leitura do HD:", metric['value'], metric['metric'])

            disk_bytes_write = round((disk_read[3] - old_disk_read[3]))
            metric = get_byte_type(disk_bytes_write)
            print("Escritura do HD:", metric['value'], metric['metric'])
            print()

            old_disk_read = disk_read

            disk_partitions = psutil.disk_partitions()
            for part in range(len(disk_partitions)):
                if 'snap' not in disk_partitions[part][1] and 'cdrom' not in disk_partitions[part][3]:
                    disk_usage = psutil.disk_usage(disk_partitions[part][1])  # uso de 'sda1'

                    print("Ocupação de", disk_partitions[part][1],
                          (("em " + disk_partitions[part][0]) if not psutil.WINDOWS else '') + ":",
                          round(disk_usage[1] / (2 ** 30), 2), "GB de", round(disk_usage[0] / (2 ** 30), 2), "GB")
                    print(get_usage_bar(disk_usage[3], disk_usage[3]))

            net_read = psutil.net_io_counters()

            net_bytes_download = round((net_read[1] - old_net[1]))
            metric = get_byte_type(net_bytes_download)
            print()
            print("Taxa Download:", metric['value'], metric['metric'])

            net_bytes_upload = round((net_read[0] - old_net[0]))
            metric = get_byte_type(net_bytes_upload)
            print("Taxa Upload:", metric['value'], metric['metric'])

            old_net = net_read

            gpus = GPUtil.getGPUs()
            if bool(gpus):
                for gpu in gpus:
                    print("\nTemperatura da GPU:", gpu.temperature, "ºC")
                    print("Uso de GPU: " + get_usage_bar(round(gpu.load * 100), round(gpu.load * 100), 4))
                    print("Uso de VRAM:", round((gpu.memoryUsed / 2 ** 10), 2), "GB de",
                          round((gpu.memoryTotal / 2 ** 10), 2), "GB")
                    print(get_usage_bar(round(gpu.memoryUtil * 100), round(gpu.memoryUtil * 100), 4))

            print("-" * system.get_terminal_size()['width'])


if __name__ == '__main__':
    main()
