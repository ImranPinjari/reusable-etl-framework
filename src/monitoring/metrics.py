from time import perf_counter


class PipelineMetrics:

    def __init__(self):
        self.start_time = None
        self.end_time = None

        self.total_records = 0
        self.valid_records = 0
        self.rejected_records = 0
        self.loaded_records = 0

    def start(self):
        """Start measuring pipeline execution time."""
        self.start_time = perf_counter()

    def finish(self):
        """Finish measuring pipeline execution time."""
        self.end_time = perf_counter()

    def record_counts(
        self,
        total: int,
        valid: int,
        rejected: int,
        loaded: int
    ):
        """Store pipeline record counts."""

        self.total_records = total
        self.valid_records = valid
        self.rejected_records = rejected
        self.loaded_records = loaded

    def get_execution_time(self) -> float:
        """Return execution time in seconds."""

        if self.start_time is None or self.end_time is None:
            return 0.0

        return round(self.end_time - self.start_time, 4)

    def get_summary(self) -> dict:
        """Return pipeline metrics as a dictionary."""

        return {
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "rejected_records": self.rejected_records,
            "loaded_records": self.loaded_records,
            "execution_time_seconds": self.get_execution_time()
        }