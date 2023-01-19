from process import Process
from typing import List
import csv
#----------------------------------------------------------------------------------------------------------------------------
def srtf(process_list : list[Process]):
    creation_queue:List[Process] = process_list[::]
    ready_queue:List[Process] = list()
    waiting_queue:List[Process] = list()
    finished_processes:List[process] = list()
    time_line = 0
    idle_time = 0

    while(ready_queue or waiting_queue or creation_queue):
        # creation
        for process in creation_queue[::]:
            if process.arrival_time <= time_line:
                ready_queue.append(process)
                creation_queue.remove(process)
        
        # from waiting to ready_queue
        for process in waiting_queue[::]:
            if process.start_io + process.process_duration[process._stage] <= time_line:
                waiting_queue.remove(process)
                ready_queue.append(process)
                process.update_stage(True)
        
        # select form ready_queue
        if ready_queue:
            current_process = ready_queue[0]
            for process in ready_queue:
                if current_process.process_duration[current_process._stage] > process.process_duration[process._stage]:
                    current_process = process
            if current_process.start == None:
                current_process.start = time_line
            current_process.process_duration[current_process._stage] -= 1
            if current_process.process_duration[current_process._stage] == 0:
                ready_queue.remove(current_process)
                current_process.update_stage(True)
                if current_process._stage == 1:
                    current_process.start_io = time_line + 1
                    waiting_queue.append(current_process)
                elif current_process._stage == 3:
                    current_process.end = time_line + 1
                    finished_processes.append(current_process)
        else:
            idle_time += 1
        time_line += 1
    return (finished_processes, time_line, idle_time)
#----------------------------------------------------------------------------------------------------------------------------
def get_process_list(file_name: str):
    process_list:List[Process] = list()
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                process_list.append(Process(int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4])))
    return process_list
#----------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    process_list = get_process_list('test.csv')
    result = srtf(process_list)
    process_list = result[0]