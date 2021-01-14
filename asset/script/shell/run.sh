#!/bin/bash

if test $# != 4; then
    echo "Usage: $0 <ID> <BIN Name> <KID> <BASE_DIR>"
    cat<<EOF

KID      Name
1        AFL
2        Memlock
3        MOpt
4        Triforce
5        AFLplusplus
default  AFL
EOF
    exit 1
fi

# BASE_DIR="/home/chengtong/auto-fuzz/fuzzing_platform/asset"
BASE_DIR=$4
if test ! -d $BASE_DIR; then 
    echo "Base directory error"
    exit 2
fi
# kernel path
AFL_FUZZ_BIN=$BASE_DIR"/kernel/afl/afl-fuzz"
Memlock_heap_FUZZ_BIN=$BASE_DIR"/kernel/MemLock/tool/MemLock/memlock-heap-fuzz"
Memlock_stack_FUZZ_BIN=$BASE_DIR"/kernel/MemLock/tool/MemLock/memlock-stack-fuzz"
MOpt_FUZZ_BIN=$BASE_DIR"/kernel/MOpt-AFL/MOpt/afl-fuzz"
Triforce_FUZZ_BIN=$BASE_DIR"/kernel/TriforceAFL/afl-fuzz"
AFLplusplus_FUZZ_BIN=$BASE_DIR"/kernel/AFLplusplus/afl-fuzz"

# select kernel
case $3 in 
    1) FUZZ_BIN=$AFL_FUZZ_BIN
    ;;
    2) FUZZ_BIN=$Memlock_heap_FUZZ_BIN
    ;;
    3) FUZZ_BIN=$MOpt_FUZZ_BIN
    ;;
    4) FUZZ_BIN=$Triforce_FUZZ_BIN 
    ;;
    5) FUZZ_BIN=$AFLplusplus_FUZZ_BIN 
    ;;
    *) FUZZ_BIN=$AFL_FUZZ_BIN
    ;;
esac

# target bin path
ID=$1
BIN_NAME=$2
if test "$BIN_NAME" == ""; then
    BIN_NAME="demo"
fi
TRGT_BIN=$BASE_DIR"/pool/"$ID"/bin/"$BIN_NAME
INPUT_DIR=$BASE_DIR"/pool/"$ID"/input"
OUTPUT_DIR=$BASE_DIR"/pool/"$ID"/output"


# run
cmd="$FUZZ_BIN -i $INPUT_DIR -o $OUTPUT_DIR -- $TRGT_BIN &"
# echo -e "Command to run: \n"$cmd
$cmd



# asn1c run
# AFL_FUZZ_BIN="/home/chengtong/auto-fuzz/dev/afl/afl-fuzz"
# TRGT_BIN="/home/chengtong/auto-fuzz/dev/target/bin/asn1c"
# mkdir -p "target/input"
# mv "target/"*.txt "target/input/"
# mkdir -p "target/output"
# $AFL_FUZZ_BIN -i "target/input" -o "target/output" -- $TRGT_BIN @@