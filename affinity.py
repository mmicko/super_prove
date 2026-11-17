"""
Portable CPU affinity helpers.

On Linux these use os.sched_getaffinity()/os.sched_setaffinity(). Other
platforms (e.g. macOS) have no API to pin a process to specific cores, so
sched_getaffinity() reports all online CPUs and sched_setaffinity() does
nothing; the OS scheduler is left to place the processes.
"""

import os

_number_of_cores = os.cpu_count() or 1

_has_affinity = hasattr(os, 'sched_getaffinity') and hasattr(os, 'sched_setaffinity')


def sched_getaffinity(pid):

    if _has_affinity:
        return sorted(os.sched_getaffinity(pid))

    return list(range(_number_of_cores))


def sched_setaffinity(pid, cpus):

    cpus = list(cpus)

    if _has_affinity and cpus:
        os.sched_setaffinity(pid, cpus)

    mask = 0
    for c in cpus:
        mask |= 1 << c

    return mask


if __name__=='__main__':
    print(sched_getaffinity(os.getpid()))
    sched_setaffinity(os.getpid(), [0,1])
    print(sched_getaffinity(os.getpid()))
