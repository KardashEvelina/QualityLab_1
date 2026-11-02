import multiprocessing
import os
import time


DURATION_SECONDS = 30


def create_cpu_load():
    end_time = time.time() + DURATION_SECONDS

    value = 1

    while time.time() < end_time:
        value = (
            value * 1664525 + 1013904223
        ) % 4294967296


def main():
    workers = os.cpu_count() or 4

    print(
        f"CPU noise: {workers} workers, "
        f"{DURATION_SECONDS} seconds"
    )

    processes = []

    for _ in range(workers):
        process = multiprocessing.Process(
            target=create_cpu_load
        )
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    print("CPU noise completed")


if __name__ == "__main__":
    main()