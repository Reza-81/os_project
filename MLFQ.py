from process import Process
from typing import List
from show_analysis import show_analysis
#----------------------------------------------------------------------------------------------------------------------------
def mlfq(process_list: list[Process]):
    process_list.sort(key=lambda process: process.id)
    creation_queue:List[Process] = process_list[::]
    ready_queue1:List[Process] = list()
    ready_queue2:List[Process] = list()
    ready_queue3:List[Process] = list()
    waiting_queue:List[Process] = list()
    finished_processes:List[Process] = list()
    process_duration = [process.process_duration.copy() for process in  process_list]
    time_line = 0
    idle_time = 0
    ctr1 = 0
    ctr2 = 0
    flag_ctr2 =0
    flag_ctr3 =0
    while(ready_queue1 or ready_queue2 or ready_queue3 or waiting_queue or creation_queue):
        # creation
        for process in creation_queue[::]:
            if process.arrival_time <= time_line:
                ready_queue1.append(process)
                creation_queue.remove(process)

        # from waiting to ready_queue1
        for process in waiting_queue[::]:
            if process.start_io + process.process_duration[process._stage] <= time_line:
                waiting_queue.remove(process)
                ready_queue1.append(process)
                process.update_stage(True)

        # select form ready_queue1

        if ready_queue1 and flag_ctr2 ==0 and flag_ctr3 ==0:
            current_process = ready_queue1[0]
            current_process.process_duration[current_process._stage] -= 1
            ctr1 += 1
            if ctr1 == 4 and current_process.process_duration[current_process._stage] != 0:
                ctr1 = 0
                ready_queue1.remove(current_process)
                ready_queue2.append(current_process)
            if current_process.start == None:
                current_process.start = time_line
            if current_process.process_duration[current_process._stage] == 0:
                ctr1 = 0
                ready_queue1.remove(current_process)
                current_process.update_stage(True)
                if current_process._stage == 1:
                    current_process.start_io = time_line + 1
                    waiting_queue.append(current_process)
                elif current_process._stage == 3:
                    current_process.end = time_line + 1
                    finished_processes.append(current_process)

        elif ready_queue2 and flag_ctr3 ==0:
            current_process = ready_queue2[0]
            current_process.process_duration[current_process._stage] -= 1
            ctr2 += 1
            if ctr2 != 16 and current_process.process_duration[current_process._stage] != 0:
                flag_ctr2 = 1
            if ctr2 == 16 and current_process.process_duration[current_process._stage] != 0:
                flag_ctr2 = 0
                ctr2 = 0
                ready_queue2.remove(current_process)
                ready_queue3.append(current_process)
            if current_process.start == None:
                current_process.start = time_line
            if current_process.process_duration[current_process._stage] == 0:
                flag_ctr2 = 0
                ctr2 = 0
                ready_queue2.remove(current_process)
                current_process.update_stage(True)
                if current_process._stage == 1:
                    current_process.start_io = time_line + 1
                    waiting_queue.append(current_process)
                elif current_process._stage == 3:
                    current_process.end = time_line + 1
                    finished_processes.append(current_process)

        elif ready_queue3:
            current_process = ready_queue3[0]
            flag_ctr3 = 1
            current_process.process_duration[current_process._stage] -= 1
            if current_process.start == None:
                current_process.start = time_line
            if current_process.process_duration[current_process._stage] == 0:
                flag_ctr3 =0
                ready_queue3.remove(current_process)
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
    finished_processes.sort(key=lambda process: process.id)
    print(finished_processes)
    for i in range(len(process_duration)):
        finished_processes[i].process_duration = process_duration[i]
    return (finished_processes, time_line, idle_time)
#----------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    process_list = Process.get_process_list('test.csv')
    result = mlfq(process_list)
    show_analysis('srtf', result[0], result[1], result[2])