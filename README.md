# sharearray
Have you worried about creating large identical numpy arrays across processes due to RAM wastage, e.g. datasets that are big enough to fit in RAM but large enough to cause concern when running multiple jobs using the same data?

`sharearray` efficiently caches numpy arrays in RAM (using shared memory in `/dev/shm`, no root needed) locally on a machine.

