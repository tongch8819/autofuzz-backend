import pdfkit
# 将wkhtmltopdf.exe程序绝对路径传入config对象
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

'''将网页url生成pdf文件'''


def url_to_pdf(url, to_file):
    # 生成pdf文件，to_file为文件路径
    pdfkit.from_url(url, to_file, configuration=config)
    print('完成')


'''将html文件生成pdf文件'''
def html_to_pdf(html, output_path=None):
    options = {
        'page-size': 'Letter',
        'quiet': '',
        'enable-local-file-access': '',
        'no-collate': '',
        'margin-top': '0.50in',
        'margin-right': '0.50in',
        'margin-bottom': '0.50in',
        'margin-left': '0.50in',
        'encoding': 'UTF-8',
                    'custom-header': [
                        ('Accept-Encoding', 'gzip'),
                    ],
        'no-outline': None,
    }
    # 生成pdf文件，to_file为文件路径
    # pdfkit.from_file(html, output, configuration=config)
    if output_path is None:
        pdf_data = pdfkit.from_string(html, False, options=options)
        # pdf_data = pdfkit.from_file(html, False, options=options)
        return pdf_data
    else:
        pdfkit.from_string(html, output_path, options=options)
        print('完成')


'''将字符串生成pdf文件'''


def str_to_pdf(string, to_file):
    # 生成pdf文件，to_file为文件路径
    pdfkit.from_string(string, to_file, configuration=config)
    print('完成')


def main():
    # 这里传入我知乎专栏文章url，转换为pdf
    # url_to_pdf(r'https://zhuanlan.zhihu.com/p/69869004',
    #            '/home/chengtong/auto-fuzz/fuzzing_platform/asset/report/test.pdf')
    pdfkit.from_file('./echart.html', '/home/chengtong/auto-fuzz/fuzzing_platform/asset/report/echart.pdf')


if __name__ == "__main__":
    main()
