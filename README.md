# AutoFuzz

This is a platform for automated fuzzing task.



## Dependency

+ django
+ pdfkit
+ psycopg2
+ django_ftpserver


## Usage

```bash
cd asset/script
python manage_pool.py --help

# development test
python manage_pool.py test --help
# E.x.: test the functionality of subcommand preprocess
python manage_pool.py test preprocess


# init a project directory
python manage_pool.py preprocess --help
# E.x.: init the directory with project id 500
python manage_pool.py preprocess init 500
# E.x.: clean the directory with project id 500
python manage_pool.py preprocess clean 500


# compile a project
python manage_pool.py compile --help
# E.x.: compile the src file target.c into binary demo in project 500 
#       using AFL (id: 1) compiler
python manage_pool.py compile 500 1 target.c demo


# start a project
python manage_pool.py run --help
# E.x.: start the fuzzing process of project id 500 using AFL fuzzer
python manage_pool.py run 500 demo 1 


# stop a project
python manage_pool.py stop --help
# E.x.: stop all fuzzing process
python manage_pool.py stop --all
# E.x.: stop fuzzing process with project id 500
python manage_pool.py stop 500
```


## Kernel ID
| Kernel | ID | URL |
| :--: | :--: | :--: |
| AFL | 1 | https://lcamtuf.coredump.cx/afl/ |
| Memlock | 2 | https://github.com/ICSE2020-MemLock/MemLock |
| MOpt | 3 | https://github.com/puppet-meteor/MOpt-AFL |
| Triforce | 4 | https://github.com/nccgroup/TriforceAFL |
| AFLplusplus | 5 | https://github.com/AFLplusplus/AFLplusplus |


## Deployment
Start from an empty ubuntu
1. Install python 3.x (anaconda recommended);
2. Install python packages: [django], [pdfkit], [psutil], [psycopg2];
3. Install postgresql and start service using default port `5432`;
4. Install [wkhtmltopdf]: https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
4. Clone 'autofuzz-backend' project;
5. Execute SQL 'init.sql' in directory sql/;
6. Start backend using port `8001`: `python manage.py runserver 8001`

[pdfkit]: https://pypi.org/project/pdfkit/
[psutil]: https://github.com/giampaolo/psutil/blob/master/INSTALL.rst
[psycopg2]: https://pypi.org/project/psycopg2/
[django]: https://www.djangoproject.com/download/
[wkhtmltopdf]: https://wkhtmltopdf.org/



