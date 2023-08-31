##  @author Merve Gulmez (merve.gulmez@ericsson.com)
##  @version 0.1
##  @date 2023-08-31
##  @copyright © Ericsson AB 2023
##  SPDX-License-Identifier: BSD 3-Clause 


#!/bin/bash
set -x

./micro_benchmark.sh 

./malloc_benchmark.sh 

./snappy.sh 

./snappy_opt.sh

./png.sh
