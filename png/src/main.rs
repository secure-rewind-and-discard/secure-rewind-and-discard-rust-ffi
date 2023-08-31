// @author Merve Gulmez (merve.gulmez@ericsson.com)
// @version 0.1
// @date 2023-08-31
// @copyright © Ericsson AB 2023
// SPDX-License-Identifier: BSD 3-Clause

#![feature(allocator_api)]

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

use libc::{c_char, c_int, c_void};
use libc::{clock_gettime, size_t, timespec, CLOCK_MONOTONIC};
use std::mem::size_of;
use std::ptr::null_mut;

use std::fs::File;
use std::io::Read;
use std::os::unix::fs::MetadataExt;
use std::ptr;
type PngStruct = c_void;
type PngInfo = c_void;
type PngSizeT = size_t;

#[link(name = "png")]
extern "C" {
    fn png_create_read_struct(
        user_png_ver: *const c_char,
        error_ptr: *mut c_void,
        error_fn: *mut u8,
        warn_fn: *mut u8,
    ) -> *mut PngStruct;
    fn png_create_info_struct(png_ptr: *mut PngStruct) -> *mut PngInfo;
    fn png_sig_cmp(sig: *const u8, start: size_t, num_to_check: size_t) -> c_int;
    fn png_destroy_read_struct(
        png_ptr_ptr: *mut *mut PngStruct,
        info_ptr_ptr: *mut *mut PngInfo,
        end_info_ptr_ptr: *mut *mut PngInfo,
    );
    fn png_set_read_fn(
        png_ptr: *mut PngStruct,
        io_ptr: *mut c_void,
        read_data_fn: extern "C" fn(*mut PngStruct, *mut u8, size_t),
    );
    fn png_get_io_ptr(png_ptr: *mut PngStruct) -> *mut c_void;

    fn png_read_info(png_ptr: *mut PngStruct, info_ptr: *mut PngInfo);
    fn png_get_image_height(png_ptr: *mut PngStruct, info_ptr: *mut PngInfo) -> u32;
    fn png_get_rowbytes(png_ptr: *mut PngStruct, info_ptr: *mut PngInfo) -> u32;
    fn png_read_image(png_ptr: *mut PngStruct, row_pointers: *mut *mut u8);
    fn setjmp(env: *mut c_void) -> c_int;
    fn longjmp(env: *mut c_void, val: c_int);
    fn png_set_longjmp_fn(
        png_ptr: *mut PngStruct,
        longjmp_fn: unsafe extern "C" fn(*mut c_void, c_int),
        jmp_buf_size: size_t,
    ) -> *mut c_void;
}

fn read_file(path: &str) -> Vec<u8> {
    let mut file = File::open(path).unwrap();
    let size = file.metadata().unwrap().size() as usize;
    let mut buf = vec![0u8; size];
    file.read_exact(&mut buf).unwrap();
    buf
}

/// Custom read function for libpng.
extern "C" fn callback(callback_png_ptr: *mut PngStruct, buf_ptr: *mut u8, count: PngSizeT) {
    unsafe {
        let mut buf = std::slice::from_raw_parts_mut(buf_ptr, count as usize);
        let image_ptr = png_get_io_ptr(callback_png_ptr);
        let image: &mut &[u8] = ::std::mem::transmute(image_ptr);
        image.read_exact(&mut buf).unwrap();
    }
}

//Read png image into a vector of row byte vectors.
sandbox! {
    fn decode_png(png_image: &[u8]) -> Result<Vec<Vec<u8>>, String> {
        let mut png_ptr: *mut PngStruct = 0 as *mut PngStruct;
        let mut info_ptr: *mut PngInfo = 0 as *mut PngStruct;
        unsafe {
            let ver = std::ffi::CString::new("1.6.28").unwrap();
            let ver_ptr = ver.as_ptr();

            png_ptr = png_create_read_struct(ver_ptr as *const  i8, null_mut(), null_mut(), null_mut());
            if png_ptr.is_null() {
                return Err("failed to create png_ptr".to_owned());
            }
            info_ptr = png_create_info_struct(png_ptr);
            if info_ptr.is_null() {
                png_destroy_read_struct(&mut png_ptr, null_mut(),null_mut());
                return Err("failed to create info_ptr".to_owned());
            }
            let jmp_buf_size: size_t = 200;

            if 0 != setjmp(png_set_longjmp_fn(png_ptr, longjmp, jmp_buf_size)) {
                return Err("read failed in libpng".to_owned());
            }

            let image_ptr: *mut c_void = ::std::mem::transmute(&png_image);
            png_set_read_fn(png_ptr, image_ptr, callback);

            png_read_info(png_ptr, info_ptr);
            let height = png_get_image_height(png_ptr, info_ptr) as usize;

            let mut result = Vec::with_capacity(height);
            let rowbytes = png_get_rowbytes(png_ptr,info_ptr) as usize;

            let mut rows = vec![ptr::null_mut() as *mut u8; height];

            for i in 0..height {
               let mut row = vec![0u8; rowbytes];
               rows[i] = row.as_mut_ptr();
               result.push(row);
            }
            png_read_image(png_ptr, rows.as_mut_ptr());
            Ok(result)
        }
    }
}

sandbox! {
    fn is_png(buf: &[u8]) -> bool {
        let buf_ptr = buf.as_ptr();
        let size = buf.len() as size_t;
        unsafe {
            if png_sig_cmp(buf_ptr, 0, size) != 0 {
                return false;
            }
        }

        return true;
    }
}

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
    let n = 1000000;

    if let Some(arg1) = std::env::args().nth(1) {
        let mut execution_times = Vec::new();
        for _ in 0..n {
            let file_buf = read_file(&arg1.as_str());
            if !is_png(&file_buf[0..8]) {
                panic!("no PNG!");
            }
            let start_time = get_time();
            let _vec = decode_png(&file_buf).unwrap();
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
        let std_mean =
            ((variance / execution_times.len() as f64).sqrt()) * 100.00 / mean_execution_time;
        println!("{},{}", mean_execution_time / 1000.00, std_mean);
    } else {
        println!("usage: png <png file>");
    }
}
