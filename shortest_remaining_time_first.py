from process import Process
from typing import List
from show_analysis import show_analysis
#----------------------------------------------------------------------------------------------------------------------------
def srtf(process_list: list[Process]):
    process_list.sort(key=lambda process: process.id)
    creation_queue:List[Process] = process_list[::]
    ready_queue:List[Process] = list()
    waiting_queue:List[Process] = list()
    finished_processes:List[Process] = list()
    process_duration = [process.process_duration.copy() for process in  process_list]
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
            for process in ready_queue[::]:
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
            elif current_process.process_duration[current_process._stage] <= 0:
                ready_queue.remove(current_process)
                current_process.update_stage(True)
                if current_process._stage == 1:
                    current_process.start_io = time_line
                    waiting_queue.append(current_process)
                elif current_process._stage == 3:
                    current_process.end = time_line
                    finished_processes.append(current_process)
                continue
        else:
            idle_time += 1
        time_line += 1
    finished_processes.sort(key=lambda process: process.id)
    for i in range(len(process_duration)):
        finished_processes[i].process_duration = process_duration[i]
    return (finished_processes, time_line, idle_time)
#----------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    process_list = Process.get_process_list('test.csv')
    result = srtf(process_list)
    show_analysis('srtf', result[0], result[1], result[2])