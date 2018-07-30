import os
import random
import shutil
import tempfile
from struct import calcsize, unpack

import pandas as pd
import six
from pytdx.crawler.base_crawler import BaseCralwer

if six.PY2:
    import zipfile


class HistoryFinancialListCrawler(BaseCralwer):
    '''
    u'获取通达信list'
    '''

    def get_url(self, *args, **kwargs):
        return "http://down.tdx.com.cn:8001/fin/gpcw.txt"

    def parse(self, download_file, *args, **kwargs):
        content = download_file.read()
        content = content.decode("utf-8")

        def list_to_dict(l):
            return {'filename': l[0], 'hash': l[1], 'filesize': int(l[2])}

        result = [
            list_to_dict(l) for l in
            [line.strip().split(",") for line in content.strip().split('\n')]
        ]
        return result


class HistoryFinancialCrawler(BaseCralwer):
    def get_url(self, *args, **kwargs):
        if 'filename' in kwargs:
            filename = kwargs['filename']
        else:
            raise Exception("Param filename is not set")

        return "http://down.tdx.com.cn:8001/fin/{}".format(filename)

    def parse(self, download_file, *args, **kwargs):

        header_pack_format = '<1hI1H3L'

        if download_file.name.endswith('.zip'):
            tmpdir_root = tempfile.gettempdir()
            subdir_name = "pytdx_" + str(random.randint(0, 1000000))
            tmpdir = os.path.join(tmpdir_root, subdir_name)
            shutil.rmtree(tmpdir, ignore_errors=True)
            os.makedirs(tmpdir)
            if six.PY2:
                with zipfile.ZipFile(download_file.name, 'r') as zf:
                    zf.extractall(tmpdir)
            else:
                shutil.unpack_archive(download_file.name, extract_dir=tmpdir)
            # only one file endswith .dat should be in zip archives
            datfile = None
            for _file in os.listdir(tmpdir):
                if _file.endswith(".dat"):
                    datfile = open(os.path.join(tmpdir, _file), "rb")

            if datfile is None:
                raise Exception("no dat file found in zip archive")
        else:
            datfile = download_file
        header_size = calcsize(header_pack_format)
        stock_item_size = calcsize("<6s1c1L")
        data_header = datfile.read(header_size)
        stock_header = unpack(header_pack_format, data_header)
        max_count = stock_header[2]
        report_date = stock_header[1]
        report_size = stock_header[4]
        report_fields_count = int(report_size / 4)
        report_pack_format = '<{}f'.format(report_fields_count)

        results = []
        for stock_idx in range(0, max_count):
            datfile.seek(header_size + stock_idx * calcsize("<6s1c1L"))
            si = datfile.read(stock_item_size)
            stock_item = unpack("<6s1c1L", si)
            code = stock_item[0].decode("utf-8")
            foa = stock_item[2]
            datfile.seek(foa)

            info_data = datfile.read(calcsize(report_pack_format))
            cw_info = unpack(report_pack_format, info_data)
            one_record = (code, report_date) + cw_info
            results.append(one_record)

        if download_file.name.endswith('.zip'):
            datfile.close()
            shutil.rmtree(tmpdir, ignore_errors=True)
        return results

    def to_df(self, data):
        if len(data) == 0:
            return None

        total_lengh = len(data[0])
        col = ['code', 'report_date']

        length = total_lengh - 2
        for i in range(0, length):
            col.append("col" + str(i + 1))

        df = pd.DataFrame(data=data, columns=col)
        df.set_index('code', inplace=True)
        return df


if __name__ == "__main__":
    import pandas as pd
    from pytdx.crawler.base_crawler import demo_reporthook
    crawler = HistoryFinancialListCrawler()

    list_data = crawler.fetch_and_parse(reporthook=demo_reporthook)
    print(pd.DataFrame(data=list_data))
    filename = list_data[3]['filename']
    #

    datacrawler = HistoryFinancialCrawler()
    pd.set_option('display.max_columns', None)
    # result = datacrawler.fetch_and_parse(reporthook=demo_reporthook, filename=filename, path_to_download="/tmp.zip")
    with open(r"/tmp.zip", "rb") as fp:
        result = datacrawler.parse(download_file=fp)
        x = datacrawler.to_df(data=result)
        x.to_csv('11.csv')
