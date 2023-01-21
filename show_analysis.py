from process import Process
import math

def show_analysis(algorithm_name: str, process_list: list[Process], total_time: int, idle_time: int) -> None:
    print('+==================+==================+==================+==================+==================+')
    print(f'|' + (47-math.floor(len(str(algorithm_name))/2))*' ' + str(algorithm_name) + (47-math.ceil(len(str(algorithm_name))/2))*' '  + '|')
    print('+==================+==================+==================+==================+==================+')
    print('|    Process ID    |     Start-End    | Turn Around Time |  Responce Time   |   Waiting Time   |')
    print('+------------------+------------------+------------------+------------------+------------------|')
    a_t_t = 0
    a_r_t = 0
    a_w_t = 0
    for process in process_list:
        a_t_t += process.end - process.arrival_time
        a_r_t += process.start_io
        a_w_t += process.end - process.arrival_time - sum(process.process_duration.values())
        id = str(process.id)
        start_end = str(process.start) + ' - ' + str(process.end)
        turn_around_time = str(process.end - process.arrival_time)
        response_time = str(process.start_io)
        waiting_time = str(process.end - process.arrival_time - sum(process.process_duration.values()))
        print('|p' + id + (17-len(id))*' ' + '|' + start_end + (18-len(start_end))*' ' + '|' + turn_around_time + (18-len(turn_around_time))*' ' + '|' + response_time + (18-len(response_time))*' ' + '|' + waiting_time + (18-len(waiting_time))*' ' + '|')
    a_t_t = a_t_t/len(process_list)
    a_r_t = a_r_t/len(process_list)
    a_w_t = a_w_t/len(process_list)
    print('+------------------+------------------+------------------+------------------+------------------|')
    print('|Average                              |' + str(a_t_t) + (18-len(str(a_t_t)))*' ' + '|' + str(a_r_t) + (18-len(str(a_r_t)))*' ' + '|' + str(a_w_t) + (18-len(str(a_w_t)))*' ' + '|')
    print('+------------------+------------------+------------------+------------------+------------------|')
    print('\nTotal Time:', total_time)
    print('Idle Time:', idle_time)
    print('CPU Utilization:', 1-(idle_time/total_time))
    print('Throughput:', len(process_list)/total_time)