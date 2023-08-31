//  @author Merve Gulmez (merve.gulmez@ericsson.com)
//  @version 0.1
//  @date 2023-08-31
//  @copyright © Ericsson AB 2023
//  SPDX-License-Identifier: BSD 3-Clause 


#[macro_export]
macro_rules! sandbox {
    (fn $f:ident($($x:tt)*) $(->$rettype:ty)? $body:block) => { 
        fn $f($($x)*) $(->$rettype)? {
            $body 
        }
    };

    (pub fn $f:ident($($x:tt)*) $(->$rettype:ty)? $body:block) => { 
        pub fn $f($($x)*) $(->$rettype)? {
            $body
        }
    };
}