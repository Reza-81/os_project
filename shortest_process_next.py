from process import Process
from typing import List
from show_analysis import show_analysis
#----------------------------------------------------------------------------------------------------------------------------
def spn(process_list : list[Process]) -> tuple[list[Process], int, int]:
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
            ready_queue.remove(current_process)
            if current_process._stage == 0:
                current_process.start = time_line
            time_line += current_process.process_duration[current_process._stage]
            current_process.update_stage(True)
            if current_process._stage == 1:
                current_process.start_io = time_line
                waiting_queue.append(current_process)
            elif current_process._stage == 3:
                current_process.end = time_line
                finished_processes.append(current_process)
        else:
            idle_time += 1
            time_line += 1
    finished_processes.sort(key=lambda process: process.id)
    return (finished_processes, time_line, idle_time)
#----------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    process_list = Process.get_process_list('test.csv')
    result = spn(process_list)
    show_analysis('spn', result[0], result[1], result[2])