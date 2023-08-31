##  @author Merve Gulmez (merve.gulmez@ericsson.com)
##  @version 0.1
##  @date 2023-08-31
##  @copyright © Ericsson AB 2023
##  SPDX-License-Identifier: BSD 3-Clause 


#!/bin/bash
set -x
datetime=$(date '+%Y-%m-%d_%H-%M-%S')
mkdir "../log/${datetime}_snappy"


###Figure 1######
cd ../snappy

cargo run --release --bin snappy  --features "bincode_v1 sdradrustffi"  >> ../log/"${datetime}_snappy"/sdrob_bincode_output.txt
cargo run --release --bin snappy  --features "bincode_v2 sdradrustffi" >> ../log/"${datetime}_snappy"/sdrob_bincodev2_output.txt
cargo run --release --bin snappy  --features "abomonation_v1 sdradrustffi" >> ../log/"${datetime}_snappy"/sdrob_abon_v1_output.txt
cargo run --release --bin snappy  --features "empty_sandbox" >> ../log/"${datetime}_snappy"/empty_output.txt
cargo run --release --bin snappy  --features "sandcrust"  >> ../log/"${datetime}_snappy"/sandcrust_output.txt

cd ../benchmark_scripts
python rb_snappy.py "../log/${datetime}_snappy"