//  @author Merve Gulmez (merve.gulmez@ericsson.com)
//  @version 0.1
//  @date 2023-08-31
//  @copyright © Ericsson AB 2023
//  SPDX-License-Identifier: BSD 3-Clause 


#![feature(allocator_api)]
use libc::{c_int, c_void, clock_gettime, size_t, timespec, CLOCK_MONOTONIC};
use rand::distributions::Uniform;
use rand::Rng;
use rand_pcg::Lcg64Xsh32;


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

#[link(name = "snappy")]
extern "C" {
    fn snappy_compress(
        input: *const u8,
        input_length: size_t,
        compressed: *mut u8,
        compressed_length: *mut size_t,
    ) -> c_int;
    fn snappy_uncompress(
        compressed: *const u8,
        compressed_length: size_t,
        uncompressed: *mut u8,
        uncompressed_length: *mut size_t,
    ) -> c_int;
    fn snappy_max_compressed_length(source_length: size_t) -> size_t;
    fn snappy_uncompressed_length(
        compressed: *const u8,
        compressed_length: size_t,
        result: *mut size_t,
    ) -> c_int;
    fn snappy_validate_compressed_buffer(compressed: *const u8, compressed_length: size_t)
        -> c_int;
}

pub fn validate_compressed_buffer(src: &[u8]) -> bool {
    unsafe { snappy_validate_compressed_buffer(src.as_ptr(), src.len() as size_t) == 0 }
}

sandbox! {
    pub fn compress(src: &[u8]) -> Vec<u8> {
    unsafe {
        let srclen = src.len() as size_t;
        let psrc = src.as_ptr();

        let mut dstlen = snappy_max_compressed_length(srclen);
        let mut dst = Vec::with_capacity(dstlen as usize);
        let pdst = dst.as_mut_ptr();

        snappy_compress(psrc, srclen, pdst, &mut dstlen);
        dst.set_len(dstlen as usize);
        dst
        }
    }
}

sandbox! {
    pub fn uncompress(src: &[u8]) -> Option<Vec<u8>> {
            unsafe {
                let srclen = src.len() as size_t;
                let psrc = src.as_ptr();

                let mut dstlen: size_t = 0;
                snappy_uncompressed_length(psrc, srclen, &mut dstlen);

                let mut dst = Vec::with_capacity(dstlen as usize);
                let pdst = dst.as_mut_ptr();

                if snappy_uncompress(psrc, srclen, pdst, &mut dstlen) == 0 {
                    dst.set_len(dstlen as usize);
                    Some(dst)
                } else {
                    None // SNAPPY_INVALID_INPUT
                }
            }
        }
}

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

use std::hint::black_box;

fn main() {
    let n = 500000;
    let mut i = 0;
    let (mut start_time, mut end_time, mut execution_time);
    let x: Vec<u8> = vec![0; 256];
    let numbers = [
        1 << 0,
        1 << 3,
        1 << 6,
        1 << 8,
        1 << 9,
        1 << 10,
        1 << 12,
        1 << 14,
        1 << 15,
        1 << 16,
        1 << 18,
        1 << 21,
    ];

    /* just for warming */ 
    for _ in 0..100 {
        let _c: &[u8] = &black_box(compress(black_box(&x)));
    }

    for _ in 0..12 {
        let mut compress_execution_times = Vec::new();
        let mut decompress_execution_times = Vec::new();

        for _ in 0..n {
            const STATE: u64 = 3141592653;
            const STREAM: u64 = 5897932384;

            let mut rng = Lcg64Xsh32::new(STATE, STREAM);

            let range = Uniform::new(0, 255);
            let buf: Vec<u8> = (0..numbers[i]).map(|_| rng.sample(&range)).collect();
            start_time = get_time();
            let c: &[u8] = &black_box(compress(black_box(&buf)));
            end_time = get_time();
            execution_time = end_time - start_time;
            compress_execution_times.push(execution_time as f64);
            assert!(validate_compressed_buffer(&c));
            /**/
            start_time = get_time();
            let d: &[u8] = &black_box(uncompress(black_box(&c))).unwrap();
            end_time = get_time();
            execution_time = end_time - start_time;
            decompress_execution_times.push(execution_time as f64);
            assert!(d.to_vec() == buf.clone());
        }

        compress_execution_times.remove(0);
        let total_execution_time: f64 = compress_execution_times.iter().sum();
        let mean_execution_time = total_execution_time / compress_execution_times.len() as f64;
        let variance: f64 = compress_execution_times
            .iter()
            .map(|x| (x - mean_execution_time) * (x - mean_execution_time))
            .sum();
        let std_mean = ((variance / compress_execution_times.len() as f64).sqrt()) * 100.00
            / mean_execution_time;
        println!(
            "compress, {},{},{}",
            numbers[i], mean_execution_time, std_mean
        );

        decompress_execution_times.remove(0);
        let total_execution_time: f64 = decompress_execution_times.iter().sum();
        let mean_execution_time = total_execution_time / decompress_execution_times.len() as f64;
        let variance: f64 = decompress_execution_times
            .iter()
            .map(|x| (x - mean_execution_time) * (x - mean_execution_time))
            .sum();
        let std_mean = ((variance / decompress_execution_times.len() as f64).sqrt()) * 100.00
            / mean_execution_time;
        println!(
            "decompress, {},{},{}",
            numbers[i], mean_execution_time, std_mean
        );
        i = i + 1;
    }
}
