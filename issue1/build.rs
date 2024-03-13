//  @author Merve Gulmez (merve.gulmez@ericsson.com) Thomas Nyman (thomas.nyman@ericsson.com)
//  @version 0.1
//  @date 2023-10-14
//  @copyright © Ericsson AB 2023
//  SPDX-License-Identifier: BSD 3-Clause

use std::process::Command;
use std::path::Path;
use std::ffi::OsString;
use std::os::unix::ffi::OsStringExt;

fn main() {
    if let Ok(output) = Command::new("find")
            .args([".", "-iname", "libsdrad.so", "-print", "-quit"])
            .output() {
        let stdout = OsString::from_vec(output.stdout);
        let libsdrad_file = Path::new(&stdout);

        if let Some(libsdrad_path) = libsdrad_file.parent() {
            println!(r"cargo:rustc-link-search={}", 
            &libsdrad_path.display());
        
            println!(r"cargo:rustc-env=LD_LIBRARY_PATH={}",
            &libsdrad_path.display());
        } else {
            panic!("Unable to find libsdrad.so");       
        }
    } else {
        panic!("Unable to find libsdrad.so");
    } 
}
