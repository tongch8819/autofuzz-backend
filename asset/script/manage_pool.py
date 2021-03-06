import os, argparse
import sys, psutil
from pathlib import Path


def get_base_dir():
    # works just fine
    # return os.fspath(BASE_DIR) + '/asset'
    # return "/home/chengtong/auto-fuzz/fuzzing_platform/asset"
    return os.fspath(Path(__file__).resolve().parent.parent.parent) + '/asset'

# utility function
def get_trgt_dir(project_id):
    base_dir = get_base_dir()
    return base_dir + '/pool/' + str(project_id)

def get_shell_path(shell_name):
    base_dir = get_base_dir()
    return base_dir + '/script/shell/' + shell_name


# feature function
def init_empty_project(project_id):
    trgt_dir = get_trgt_dir(project_id)
    if os.path.isdir(trgt_dir):
        os.system('rm -rf ' + trgt_dir)
    os.system('mkdir ' + trgt_dir)
    shell_path = get_shell_path('init_subdir.sh')
    os.system('bash ' + shell_path + ' ' + trgt_dir)


def clean_project_bin(project_id):
    trgt_dir = get_trgt_dir(project_id)
    os.system('rm -r ' + trgt_dir + '/bin/*')

def clean_project_input(project_id):
    trgt_dir = get_trgt_dir(project_id)
    os.system('rm -r ' + trgt_dir + '/input/*')

def clean_project_output(project_id):
    trgt_dir = get_trgt_dir(project_id)
    os.system('rm -r ' + trgt_dir + '/output/*')

def rm_project(project_id):
    trgt_dir = get_trgt_dir(project_id)
    if os.path.isdir(trgt_dir):
        os.system("rm -rf " + trgt_dir)

def compile_project(project_id, compiler_id, src_name='target.c', bin_name='demo'):
    shell_path = get_shell_path('compile.sh')
    tplt = "bash {0} {1} {2} {3} {4} {5}"
    cmd = tplt.format(shell_path, project_id, src_name, bin_name, compiler_id, get_base_dir())
    os.system(cmd)

def run_project(project_id, bin_name, kernel_id):
    shell_path = get_shell_path('run.sh')
    tplt = "bash {0} {1} {2} {3} {4}"
    cmd = tplt.format(shell_path, project_id, bin_name, kernel_id, get_base_dir())
    os.system(cmd)



# test function
def test_preprocess():
    init_empty_project(999)
    rm_project(999)

def test_compile():
    for i in range(1, 6):
        compile_project(1, i)
        clean_project_bin(1)

def test_run():
    # for i in range(1, 5):
        # run_project(1, 'demo', i)
    run_project(1, 'demo', 5)

def test_base_dir():
    print(get_base_dir())


# stop function

def stop_process(project_id):
    work_dir = get_base_dir() + '/pool/' + str(project_id)
    if not os.path.isdir(work_dir):
        print("Project does not exist.")
        return
    def get_pid(work_dir):
        possible_solus = [
            work_dir + '/output/fuzzer_stats', 
            work_dir + '/output/default/fuzzer_stats'  # AFLPlusPlus pid at 4-th line.
        ]
        trgt_path = None
        for item in possible_solus:
            if os.path.isfile(item):
                trgt_path = item
        if trgt_path is not None:
            with open(trgt_path, 'r') as rd:
                content = rd.readlines()
            if trgt_path == possible_solus[0]:
                return int(content[2].strip().split()[-1])
            else:
                return int(content[3].strip().split()[-1])
        else:
            print("fuzzer_stats NOT found.")
            return -1

    pid = get_pid(work_dir)
    try:
        psutil.Process(pid)
    except psutil.NoSuchProcess as e:
        print("Process does not exist.")
        return 
    except ValueError as e:
        print("fuzzer_stats NOT found.")
        return 

    cmd = "kill {}".format(pid)
    os.system(cmd)
    print("Kill PID {} with project id: {}".format(pid, project_id))

def stop_all_process():
    work_dir = get_base_dir() + '/pool'
    for name in os.listdir(work_dir):
        stop_process(int(name))
    print("Finished.")

# main
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', help="subparsers help")

    test_parser = subparsers.add_parser('test')
    # test_parser.add_argument('-v', '--verbose', action="count")
    test_parser.add_argument('subcommand', help='preprocess, compile, run, base_dir')


    preprocess_parser = subparsers.add_parser('preprocess')
    preprocess_parser.add_argument("cmd", type=str, help="init, clean, clean_i, clean_o, clean_b")
    preprocess_parser.add_argument("project_id", type=int)

    compile_parser = subparsers.add_parser('compile')
    compile_parser.add_argument("project_id", type=int)
    compile_parser.add_argument("compiler_id", type=int)
    compile_parser.add_argument("src_name", type=str)
    compile_parser.add_argument("bin_name", type=str)

    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('project_id', type=int)
    run_parser.add_argument('bin_name', type=str)
    run_parser.add_argument('kernel_id', type=int)

    postprocess_parser = subparsers.add_parser('stop')
    postprocess_parser.add_argument('--all', '-a', action='store_true', help="stop all fuzzing process")
    postprocess_parser.add_argument('--project_id', '-p', action='store', help="stop fuzzing process with pid")

    args = parser.parse_args()
    # print(vars(args))

    if args.subparser_name == 'test':
        assert args.subcommand in ('preprocess', 'compile', 'run', 'base_dir'), "subcommand error!!!"
        if args.subcommand == 'preprocess':
            test_func = test_preprocess
        elif args.subcommand == 'compile':
            test_func = test_compile
        elif args.subcommand == 'run':
            test_func = test_run
        elif args.subcommand == 'base_dir':
            test_func = test_base_dir
        try:
            test_func()
            print("\n\n\033[1;32m+\033[0m Test Passed;")
        except:
            print("\n\n\033[1;31mx\033[0m Test failed;")
    elif args.subparser_name == 'preprocess':
        if args.cmd == "init":
            init_empty_project(args.project_id)
        elif args.cmd == 'clean':
            rm_project(args.project_id)
        elif args.cmd == 'clean_i':
            clean_project_input(args.project_id)
        elif args.cmd == 'clean_o':
            clean_project_output(args.project_id)
        elif args.cmd == 'clean_b':
            clean_project_bin(args.project_id)
        else:
            print("Nothing to be done!!!")
    elif args.subparser_name == 'compile':
        args_dict = vars(args)
        args_dict.pop('subparser_name')
        compile_project(**args_dict)
    elif args.subparser_name == 'run':
        args_dict = vars(args)
        args_dict.pop('subparser_name')
        run_project(**args_dict)
    elif args.subparser_name == 'stop':
        if args.all:
            stop_all_process()
        elif args.project_id is not None:
            stop_process(args.project_id)
    else:
        print("Nothing to be done!!!")

    



if __name__ == "__main__":
    main()
