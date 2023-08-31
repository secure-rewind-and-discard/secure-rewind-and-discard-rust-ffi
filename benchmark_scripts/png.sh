##  @author Merve Gulmez (merve.gulmez@ericsson.com)
##  @version 0.1
##  @date 2023-08-31
##  @copyright © Ericsson AB 2023
##  SPDX-License-Identifier: BSD 3-Clause 

#!/bin/bash
set -x
datetime=$(date '+%Y-%m-%d_%H-%M-%S')
mkdir "../log/${datetime}_png"


## png performance 

cd ../png

cargo run --release  --features "sandcrust" -- ../benchmark_images/myblood.png >> ../log/"${datetime}_png"/my_blood.txt 
cargo run --release  --features "abomonation_v1 sdradrustffi" -- ../benchmark_images/myblood.png >> ../log/"${datetime}_png"/my_blood.txt
cargo run --release  --features "empty_sandbox" -- ../benchmark_images/myblood.png >> ../log/"${datetime}_png"/my_blood.txt

cargo run --release  --features "sandcrust" -- ../benchmark_images/rust-logo.png >> ../log/"${datetime}_png"/rust_logo.txt 
cargo run --release  --features "abomonation_v1 sdradrustffi" -- ../benchmark_images/rust-logo.png >> ../log/"${datetime}_png"/rust_logo.txt
cargo run --release  --features "empty_sandbox" -- ../benchmark_images/rust-logo.png >> ../log/"${datetime}_png"/rust_logo.txt

cargo run --release  --features "sandcrust" -- ../benchmark_images/arithmetic28x11.png >> ../log/"${datetime}_png"/arithmetic.txt 
cargo run --release  --features "abomonation_v1 sdradrustffi" -- ../benchmark_images/arithmetic28x11.png >> ../log/"${datetime}_png"/arithmetic.txt
cargo run --release  --features "empty_sandbox" -- ../benchmark_images/arithmetic28x11.png >> ../log/"${datetime}_png"/arithmetic.txt

cargo run --release  --features "sandcrust" -- ../benchmark_images/objects.png >> ../log/"${datetime}_png"/objects.txt 
cargo run --release  --features "abomonation_v1 sdradrustffi" -- ../benchmark_images/objects.png >> ../log/"${datetime}_png"/objects.txt
cargo run --release  --features "empty_sandbox" -- ../benchmark_images/objects.png >> ../log/"${datetime}_png"/objects.txt



