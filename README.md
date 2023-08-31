# Secure Rewind & Discard of Isolated Domains for Foreign Function Interface in Rust

This repository contains the benchmark source code for [sdradrustffi](https://github.com/secure-rewind-and-discard/sdradrustffi) crate. Please read the paper for more info [Friend or Foe Inside? Exploring In-Process Isolation to Maintain Memory Safety for Unsafe Rust](https://arxiv.org/pdf/2306.08127.pdf)

Accepted at [IEEE-SECDEV 2023](https://secdev.ieee.org/2023/home). 

## Abstract

Rust is a popular memory-safe systems programming language. In order to interact with hardware or call into non- Rust libraries, Rust provides unsafe language features that shift responsibility for ensuring memory safety to the developer. Failing to do so, may lead to memory safety violations in unsafe code which can violate safety of the entire application. In this work we explore in-process isolation with Memory Protection Keys as a mechanism to shield safe program sections from safety violations that may happen in unsafe sections. Our approach is easy to use and comprehensive as it prevents heap and stack-based violations. We further compare process-based and in-process isolation mechanisms and the necessary requirements for data serialization, communication, and context switching. Our results show that in-process isolation can be effective and efficient, permits for a high degree of automation, and also enables a notion of application rewinding where the safe program section may detect and safely handle violations in unsafe code.


### How to get started

* Check the requirements for the [sdradrustffi](https://github.com/secure-rewind-and-discard/sdradrustffi.git) crate

This repository can be cloned using the following commands:
```
git clone https://github.com/secure-rewind-and-discard/secure-rewind-and-discard-ffi.git
```

### Benchmarks
The [benchmark_scripts](./benchmark_scripts/) folder contains the related benchmarking scripts. All benchmark data will be located under [log](./log) folder.  Here's an overview of the available scripts:

- [bench_all.sh](./benchmark_scripts/bench_all.sh) runs all following benchmarks
    - [micro_benchmark.sh](./benchmark_scripts/micro_benchmark.sh) reproduces Figure 2. 
    - [malloc_benchmark.sh](./benchmark_scripts/malloc_benchmark.sh) reproduces Section V-A result. 
    - [png.sh](./benchmark_scripts/png.sh) reproduces Table I. 
    - [snappy_opt.sh](./benchmark_scripts/snappy_opt.sh) reproduces Figure 3-a.
    - [snappy.sh](./benchmark_scripts/snappy.sh) reproduces Figure 3-b.


We used [empty_sandbox](./empty_sandbox/) as the baseline. 

We ran all experiments with the "release" build option on Dell PowerEdge R540 machines with 24-core MPK-enabled Intel(R) Xeon(R) Silver 4116 CPU (2.10GHz) having 128 GB RAM and using Ubuntu 18.04, Linux Kernel 4.15.0.

## License 

© Ericsson AB 2023

BSD 3-Clause License

