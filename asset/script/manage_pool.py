import os, argparse

# utility function
def get_trgt_dir(project_id):
    base_dir = "/home/chengtong/auto-fuzz/fuzzing_platform/asset"
    return base_dir + '/pool/' + str(project_id)

def get_shell_path(shell_name):
    base_dir = "/home/chengtong/auto-fuzz/fuzzing_platform/asset"
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
    tplt = "bash {0} {1} {2} {3} {4}"
    cmd = tplt.format(shell_path, project_id, src_name, bin_name, compiler_id)
    os.system(cmd)

def run_project(project_id, bin_name, kernel_id):
    shell_path = get_shell_path('run.sh')
    tplt = "bash {0} {1} {2} {3}"
    cmd = tplt.format(shell_path, project_id, bin_name, kernel_id)
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


# main
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', help="subparsers help")

    test_parser = subparsers.add_parser('test')
    # test_parser.add_argument('-v', '--verbose', action="count")
    test_parser.add_argument('subcommand', help='preprocess, compile, run')


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

    args = parser.parse_args()
    # print(vars(args))

    if args.subparser_name == 'test':
        assert args.subcommand in ('preprocess', 'compile', 'run'), "subcommand error!!!"
        if args.subcommand == 'preprocess':
            test_func = test_preprocess
        elif args.subcommand == 'compile':
            test_func = test_compile
        elif args.subcommand == 'run':
            test_func = test_run
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
    else:
        print("Nothing to be done!!!")

    



if __name__ == "__main__":
    main()
