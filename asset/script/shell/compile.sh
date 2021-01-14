#!/bin/bash

if test $# != 5; then
    echo "Usage: $0 <ID> <SRC Name> <Output Name> <CID> <BASE_DIR>"
    cat<<EOF

CID      Name
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
BASE_DIR=$5
if test ! -d $BASE_DIR; then 
    echo "Base directory error"
    exit 2
fi
# compiler path
AFL_CC=$BASE_DIR"/kernel/afl/afl-gcc"
Memlock_CC=$BASE_DIR"/kernel/MemLock/tool/MemLock/afl-gcc"
MOpt_CC=$BASE_DIR"/kernel/MOpt-AFL/MOpt/afl-gcc"
Triforce_CC=$BASE_DIR"/kernel/TriforceAFL/afl-gcc"
AFLplusplus_CC=$BASE_DIR"/kernel/AFLplusplus/afl-cc"

# select compiler
case $4 in 
    1) FUZZ_CC=$AFL_CC
    ;;
    2) FUZZ_CC=$Memlock_CC
    ;;
    3) FUZZ_CC=$MOpt_CC
    ;;
    4) FUZZ_CC=$Triforce_CC 
    ;;
    5) FUZZ_CC=$AFLplusplus_CC 
    ;;
    *) FUZZ_CC=$AFL_CC
    ;;
esac

# target src path
ID=$1
TRGT_DIR=$BASE_DIR"/pool/"$ID
SRC_PATH=$TRGT_DIR"/src/"$2
OUTPUT_PATH=$TRGT_DIR"/bin/"$3

# compile
cmd="$FUZZ_CC -o $OUTPUT_PATH $SRC_PATH"
# echo -e "Command to run: \n"$cmd
$cmd









