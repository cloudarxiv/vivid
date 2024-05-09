
# default imports
import json
import os
import time

# third-party imports
import psutil

# variables for the amdgpu_top profile
# total values
total_gpu_util = 0
total_vram_util = 0
total_gpu_temp = 0
total_gpu_power = 0
# max values
max_gpu_util = 0
max_vram_util = 0
max_gpu_temp = 0
max_gpu_power = 0
# average values
avg_gpu_util = 0
avg_vram_util = 0
avg_gpu_temp = 0
avg_gpu_power = 0
# current values
gpu_util = 0
vram_util = 0
gpu_temp = 0
gpu_power = 0
# min values
min_gpu_util = 0
min_vram_util = 0
# min cpu and mem values
min_cpu_util = 0
min_virt_mem_util = 0
min_swap_mem_util = 0
# max cpu and mem values
max_cpu_util = 0
max_virt_mem_util = 0
max_swap_mem_util = 0
# total cpu and mem values
total_cpu_util = 0
total_virt_mem_util = 0
total_swap_mem_util = 0
# average cpu and mem values
avg_cpu_util = 0
avg_virt_mem_util = 0
avg_swap_mem_util = 0
# current cpu and mem values
cpu_util = 0
virt_mem_util = 0
swap_mem_util = 0

# count of samples
count = 0
# flag to start sampling
flag = 0

# main function
if __name__ == '__main__':

    while True:
        try:
            # run the amdgpu_top command in JSON mode and parse the output
            os.system('amdgpu_top -n 1 --json > amdgpu_top_profile.json')

            # increment the count of samples
            count += 1

            # open the JSON file and load the data
            with open('amdgpu_top_profile.json') as f:
                data = json.load(f)

            if flag == 0:
                start_sampling = input('Start sampling? (y/n): ')
                if start_sampling == 'y':
                    flag = 1

                # get the CPU and memory utilization in %
                min_cpu_util = psutil.cpu_percent()
                min_virt_mem_util = psutil.virtual_memory().percent
                min_swap_mem_util = psutil.swap_memory().percent

                # parse the minimum values for the amdgpu_top profile

                # GPU utilization in %
                min_gpu_util = data['devices'][0]['gpu_activity']['GFX']['value']

                # VRAM utilization in MiB
                min_vram_util = ( (data['devices'][0]['VRAM']['Total VRAM Usage']['value']) / (data['devices'][0]['VRAM']['Total VRAM']['value']) ) * 100

            if flag == 1:
                # calculate the total, max and average values for the amdgpu_top profile

                # GPU utilization in %
                gpu_util = data['devices'][0]['gpu_activity']['GFX']['value'] - min_gpu_util
                total_gpu_util += gpu_util
                if gpu_util > max_gpu_util:
                    max_gpu_util = gpu_util
                avg_gpu_util = total_gpu_util / count

                # VRAM utilization in %
                vram_util = ( ( (data['devices'][0]['VRAM']['Total VRAM Usage']['value']) / (data['devices'][0]['VRAM']['Total VRAM']['value']) ) * 100 ) - min_vram_util
                total_vram_util += vram_util
                if vram_util > max_vram_util:
                    max_vram_util = vram_util
                avg_vram_util = total_vram_util / count

                # GPU temperature in °C
                gpu_temp = data['devices'][0]['Sensors']['Edge Temperature']['value']
                total_gpu_temp += gpu_temp
                if gpu_temp > max_gpu_temp:
                    max_gpu_temp = gpu_temp
                avg_gpu_temp = total_gpu_temp / count

                # GPU power in W
                gpu_power = data['devices'][0]['Sensors']['GFX Power']['value']
                total_gpu_power += gpu_power
                if gpu_power > max_gpu_power:
                    max_gpu_power = gpu_power
                avg_gpu_power = total_gpu_power / count

                # CPU utilization in %
                cpu_util = psutil.cpu_percent() - min_cpu_util
                total_cpu_util += cpu_util
                if cpu_util > max_cpu_util:
                    max_cpu_util = cpu_util
                avg_cpu_util = total_cpu_util / count

                # virtual memory utilization in %
                virt_mem_util = psutil.virtual_memory().percent - min_virt_mem_util
                total_virt_mem_util += virt_mem_util
                if virt_mem_util > max_virt_mem_util:
                    max_virt_mem_util = virt_mem_util
                avg_virt_mem_util = total_virt_mem_util / count

                # swap memory utilization in %
                swap_mem_util = psutil.swap_memory().percent - min_swap_mem_util
                total_swap_mem_util += swap_mem_util
                if swap_mem_util > max_swap_mem_util:
                    max_swap_mem_util = swap_mem_util
                avg_swap_mem_util = total_swap_mem_util / count

            # print the max and average values for the amdgpu_top profile
            print(f'Max GPU utilization: {round(max_gpu_util, 2)}%', f'Average GPU utilization: {round(avg_gpu_util, 2)}%', sep='\t')
            print(f'Max VRAM utilization: {round(max_vram_util, 2)} %', f'Average VRAM utilization: {round(avg_vram_util, 2)} %', sep='\t')
            print(f'Max GPU temperature: {round(max_gpu_temp, 2)}°C', f'Average GPU temperature: {round(avg_gpu_temp, 2)}°C', sep='\t')
            print(f'Max GPU power: {round(max_gpu_power, 2)} W', f'Average GPU power: {round(avg_gpu_power, 2)} W', sep='\t')
            print(f'Max CPU utilization: {round(max_cpu_util, 2)}%', f'Average CPU utilization: {round(avg_cpu_util, 2)}%', sep='\t')
            print(f'Max virtual memory utilization: {round(max_virt_mem_util, 2)}%', f'Average virtual memory utilization: {round(avg_virt_mem_util, 2)}%', sep='\t')
            print(f'Max swap memory utilization: {round(max_swap_mem_util, 2)}%', f'Average swap memory utilization: {round(avg_swap_mem_util, 2)}%', sep='\t')
            print()

            time.sleep(1)

        except KeyboardInterrupt:
            print('Exiting the GPU monitoring program...')

            break

