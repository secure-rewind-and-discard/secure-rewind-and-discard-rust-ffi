//  @author Merve Gulmez (merve.gulmez@ericsson.com)
//  @version 0.1
//  @date 2023-08-31
//  @copyright © Ericsson AB 2023
//  SPDX-License-Identifier: BSD 3-Clause

extern crate libc;

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

#[cfg(feature = "empty_sandbox")]
use empty_sandbox::*;

use libc::{clock_gettime, timespec, CLOCK_MONOTONIC};
use std::hint::black_box;

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

sandbox! {
    fn empty() {}
}

fn main() {
    let mut execution_times = Vec::new();
    for _ in 0..100 {
        empty();
    }

    for _ in 0..100000000 {
        let start_time = get_time();
        black_box(empty());
        let end_time = get_time();
        let execution_time = end_time - start_time;
        execution_times.push(execution_time as f64);
    }
    let total_execution_time: f64 = execution_times.iter().sum();
    let mean_execution_time = total_execution_time / execution_times.len() as f64;
    let variance: f64 = execution_times
        .iter()
        .map(|x| (x - mean_execution_time) * (x - mean_execution_time))
        .sum();
    println!(
        "{},{}",
        mean_execution_time,
        (variance / execution_times.len() as f64).sqrt()
    );
}
