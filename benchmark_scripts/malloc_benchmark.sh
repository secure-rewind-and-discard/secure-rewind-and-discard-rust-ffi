##  @author Merve Gulmez (merve.gulmez@ericsson.com)
##  @version 0.1
##  @date 2023-08-31
##  @copyright © Ericsson AB 2023
##  SPDX-License-Identifier: BSD 3-Clause 

#!/bin/bash
set -x
## Micro benchmark Result 
datetime=$(date '+%Y-%m-%d_%H-%M-%S')
mkdir "../log/${datetime}_micro_malloc"

cd ../microbenchmark_malloc/ 

cargo run --release --features "sdradrustffi abomonation_v1"  >> ../log/"${datetime}_micro_malloc"/sdrad_output.txt
cargo run --release --features "empty_sandbox"  >> ../log/"${datetime}_micro_malloc"/empty_output.txt
