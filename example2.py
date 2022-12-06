import time

import ray

from utils import Timer


def f(x, y):
    # simulate work
    time.sleep(1)
    return x + y


def linear_reduce(f, l):
    if len(l) == 0:
        raise ValueError("len(l) must be > 0")

    def recurse(l):
        return l[0] if len(l) == 1 else f(l[-1], recurse(l[:-1]))

    return recurse(l)


def divide_and_conquer_reduce(f, l):
    if len(l) == 0:
        raise ValueError("len(l) must be > 0")

    def recurse(l):
        m = len(l) // 2
        return l[0] if len(l) == 1 else f(recurse(l[:m]), recurse(l[m:]))

    return recurse(l)


def main():
    ray.init()
    data = list(range(10))

    with Timer("Ray Linear"):
        f_ray_remote = ray.remote(f)
        result_ids = linear_reduce(f_ray_remote.remote, data)
        results = ray.get(result_ids)
        print(results)

    with Timer("Ray Divide and Conquer"):
        f_ray_remote = ray.remote(f)
        result_ids = divide_and_conquer_reduce(f_ray_remote.remote, data)
        results = ray.get(result_ids)
        print(results)

    with Timer("Vanilla Linear"):
        results = linear_reduce(f, data)
        print(results)

    with Timer("Vanilla Divide and Conquer"):
        results = divide_and_conquer_reduce(f, data)
        print(results)


if __name__ == "__main__":
    main()
