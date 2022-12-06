import time

import ray

from utils import Timer


def f(x):
    # simulate work
    time.sleep(1)
    return x**2


def main():
    ray.init()
    data = range(10)

    with Timer("Ray"):
        f_ray_remote = ray.remote(f)
        result_ids = [f_ray_remote.remote(i) for i in data]
        results = ray.get(result_ids)
        print(results)

    with Timer("Vanilla"):
        results = [f(i) for i in data]
        print(results)


if __name__ == "__main__":
    main()
