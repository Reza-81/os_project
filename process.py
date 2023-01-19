class Process():
    def __init__(self, id: int, arrival_time: int, cpu_burst_1: int = 0, io_burst: int = 0, cpu_burst_2: int = 0) -> None:
        self.id = id
        self.arrival_time = arrival_time
        #stage = 0 -> cpu burst 1, 1 -> io burst, 2 -> cpu burst 2, 3 -> finished
        self._stage = 0
        self.process_duration = {0: cpu_burst_1, 1: io_burst, 2: cpu_burst_2}
        self.start = None
        self.end = None
        self.start_io = None
    
    def update_stage(self, next: bool = True):
        if next:
            if self._stage < 3:
                self._stage += 1
        elif self._stage > 0:
            self._stage -= 1