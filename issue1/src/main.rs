// testing for issue https://github.com/EricssonResearch/sdradrustffi/issues/1

#![feature(allocator_api)]
use sdradrustffi::*;
use std::os::raw::c_void;


sandbox!(
    fn f(a: &[i32]) {
    }
);

fn main() {
    f(&[3]);
}