from adapters import getAllJobs, jobClass
class JobRunner:
    def __init__(self,ActionClass, ResultsClasses):
        self.ActionClass = ActionClass
        self.ResultsClasses = ResultsClasses
        self._idle_log_counter = 0

    
    def run_loop(self):
        import time
        while True:
            cases = self.get_cases()
            if len(cases) == 0:
                # Avoid log spam while idle; emit a heartbeat occasionally.
                self._idle_log_counter += 1
                if self._idle_log_counter % 60 == 0:
                    print("JobRunner: Idle (no queued cases)")
                time.sleep(5)
                continue
            self._idle_log_counter = 0
            queued_cases = [case for case in cases if case.get_status() == "Queued"]
            if len(queued_cases) > 0:
                print(f"JobRunner: Processing {len(queued_cases)} queued case(s)")
            for case in queued_cases:
                case.runCase()
            # Small delay to avoid tight loop
            time.sleep(1)

    def get_cases(self):
        jobs = getAllJobs(self.ActionClass, self.ResultsClasses)
        all_cases = []
        for job in jobs:
            if( not job.isCompleted() ):
                all_cases.extend(job.get_cases())
        return all_cases