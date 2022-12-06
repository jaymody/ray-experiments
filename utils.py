from time import perf_counter


class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.time = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.time
        self.readout = f"Time to execute {self.name}: {self.time:.3f} seconds"
        print(self.readout)
