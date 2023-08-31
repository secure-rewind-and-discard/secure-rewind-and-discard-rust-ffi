//  @author Merve Gulmez (merve.gulmez@ericsson.com)
//  @version 0.1
//  @date 2023-08-31
//  @copyright © Ericsson AB 2023
//  SPDX-License-Identifier: BSD 3-Clause

extern crate libc;

use rand::Rng;
use rand_pcg::Lcg64Xsh32;
use std::hint::black_box;

#[allow(unused_imports)]
#[cfg(feature = "sdradrustffi")]
extern crate sdradrustffi;

#[cfg(feature = "sdradrustffi")]
use sdradrustffi::*;

#[cfg(feature = "sandcrust")]
extern crate sandcrust;

#[cfg(feature = "sandcrust")]
use sandcrust::*;

#[cfg(feature = "empty_sandbox")]
extern crate empty_sandbox;

use libc::{clock_gettime, free, malloc, timespec, CLOCK_MONOTONIC};

#[inline]
fn get_time() -> u64 {
    let mut ts = timespec {
        tv_sec: 0,
        tv_nsec: 0,
    };
    unsafe {
        clock_gettime(CLOCK_MONOTONIC, &mut ts);
    }

    (ts.tv_sec as u64) * 1_000_000_000 + (ts.tv_nsec as u64)
}

fn main() {
    let mut a;
    let mut buf_size;
    let n = 100000000;
    unsafe {
        a = malloc(24);
        free(a);
    }
    buf_size = 1;
    const STATE: u64 = 3141592653;
    const STREAM: u64 = 5897932384;
    //let mut rng = rand::thread_rng(); //sometimes, it doesn't work hard to detect
    let mut rng = Lcg64Xsh32::new(STATE, STREAM);
    let mut execution_malloc_times = Vec::with_capacity(100000001);
    let mut execution_free_times = Vec::with_capacity(100000001);
    for _ in 0..n {
        buf_size = rng.gen_range(0..4096);
        let start_time = get_time();
        unsafe {
            a = black_box(malloc(black_box(buf_size)));
        }
        let end_time = get_time();
        let execution_time = end_time - start_time;

        execution_malloc_times.push(execution_time as f64);

        let start_time = get_time();

        unsafe {
            black_box(free(black_box(a)));
        }
        let end_time = get_time();
        let execution_time = end_time - start_time;

        execution_free_times.push(execution_time as f64);
    }
    let total_execution_time: f64 = execution_malloc_times.iter().sum();
    let mean_execution_time = total_execution_time / execution_malloc_times.len() as f64;
    let variance: f64 = execution_malloc_times
        .iter()
        .map(|x| (x - mean_execution_time) * (x - mean_execution_time))
        .sum();
    println!(
        "malloc, {},{}, {}",
        buf_size,
        mean_execution_time,
        (variance / execution_malloc_times.len() as f64).sqrt()
    );

    let total_execution_time: f64 = execution_free_times.iter().sum();
    let mean_execution_time = total_execution_time / execution_free_times.len() as f64;
    let variance: f64 = execution_free_times
        .iter()
        .map(|x| (x - mean_execution_time) * (x - mean_execution_time))
        .sum();
    println!(
        "free, {},{}, {}",
        buf_size,
        mean_execution_time,
        (variance / execution_free_times.len() as f64).sqrt()
    );
}
