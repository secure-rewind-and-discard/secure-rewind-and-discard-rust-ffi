##  @author Merve Gulmez (merve.gulmez@ericsson.com)
##  @version 0.1
##  @date 2023-08-31
##  @copyright © Ericsson AB 2023
##  SPDX-License-Identifier: BSD 3-Clause 

#!/bin/bash

set -x

datetime=$(date '+%Y-%m-%d_%H-%M-%S')
mkdir ../log/"${datetime}_snappy_abon"

SDRAD_PATH=${DEPLOY_ENV:-/home/merve/sdrad_repo/secure-rewind-and-discard/src/}

###Figure 1######
cd ../snappy


`CARGO_PROFILE_RELEASE_OPT_LEVEL=3 cargo build --release --bin snappy --features "abomonation_v1 sdradrustffi"`
`LD_LIBRARY_PATH=$SDRAD_PATH ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v1_output_03.txt`
`CARGO_PROFILE_RELEASE_OPT_LEVEL=3 cargo build  --bin snappy --features "abomonation_v2 sdradrustffi"`
`LD_LIBRARY_PATH=$SDRAD_PATH ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v2_output_03.txt`

`CARGO_PROFILE_RELEASE_OPT_LEVEL=2 cargo build --release --bin snappy --features "abomonation_v1 sdradrustffi"`
`LD_LIBRARY_PATH=$SDRAD_PATH  ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v1_output_02.txt`
`CARGO_PROFILE_RELEASE_OPT_LEVEL=2 cargo build --release --bin snappy  --features "abomonation_v2 sdradrustffi"`
`LD_LIBRARY_PATH=$SDRAD_PATH ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v2_output_02.txt`

`CARGO_PROFILE_RELEASE_OPT_LEVEL=1 cargo build --release  --bin snappy --features "abomonation_v1 sdradrustffi"` 
`LD_LIBRARY_PATH=$SDRAD_PATH  ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v1_output_01.txt`
`CARGO_PROFILE_RELEASE_OPT_LEVEL=1 cargo build --release  --bin snappy --features "abomonation_v2 sdradrustffi" `
`LD_LIBRARY_PATH=$SDRAD_PATH ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v2_output_01.txt`

`CARGO_PROFILE_RELEASE_OPT_LEVEL=0 cargo build --release --bin snappy --features "abomonation_v1 sdradrustffi"` 
`LD_LIBRARY_PATH=$SDRAD_PATH ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v1_output_00.txt`
`CARGO_PROFILE_RELEASE_OPT_LEVEL=0 cargo build --release --bin snappy --features "abomonation_v2 sdradrustffi" `
`LD_LIBRARY_PATH=$SDRAD_PATH ./target/release/snappy >> ../log/"${datetime}_snappy_abon"/abon_v2_output_00.txt`



cd ../benchmark_scripts
python rb_abon_opt.py ../log/"${datetime}_snappy_abon"