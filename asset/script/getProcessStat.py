import os
import re


def getPID():
    stat_path = "/home/chengtong/auto-fuzz/fuzzing_platform/asset/target/output/fuzzer_stats"
    with open(stat_path, 'r') as rd:
        content = rd.readlines()
    line_posi = 2
    line = content[line_posi]
    pid = line.strip().split(':')[-1].strip()
    return pid


def getStat():
    regex = 'fuzz'
    cmd = 'ps aux | grep ' + regex
    output = os.popen(cmd)
    lines = output.read().split('\n')

    pid = getPID()
    target = None
    for line in lines:
        if re.search(pid, line) is not None:
            target = line
            break

    tokens = target.split()
    rst = {
        'cpu':  tokens[2],
        'mem': tokens[3],
        'virtual_mem': tokens[4],
        'residual_mem': tokens[5],
        'cpu_time': tokens[8],
    }
    return rst


def main():
    print(getStat())


if __name__ == "__main__":
    main()
