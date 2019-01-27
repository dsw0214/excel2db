# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 下午4:11
# @Author  : shiwei-Du
# @Email   : dusw0214@126.com
# @File    : Excel2db.py
# @Software: PyCharm

import sys
import pandas as pd
from sqlalchemy import create_engine
import configparser
import threading
import argparse
import os
from lib.Log import Log

config = configparser.ConfigParser()
config.read('config/define.ini')
dbconfig = config['MYSQL']

handle = "%s+%s://%s:%s@%s:%s/%s?charset=%s" % (dbconfig['DIALECT'], dbconfig['DRIVER'], dbconfig['USER'],
                                                dbconfig['PASSWORD'], dbconfig['HOST'], dbconfig['PORT'],
                                                dbconfig['DBNAME'], dbconfig['CHARSET'])
engine = create_engine(handle)


class Excel2db(Log):
    def __init__(self):
        Log.__init__(self)
        self.path = config.get('EXCEL_CONFIG', 'SOURCE_PATH')
        self.back_path = config.get('EXCEL_CONFIG', 'BACKUPS_PATH')

    def load_in_by_table(self, table:str):
        try:
            df = pd.read_excel(self.path + table + '.xls', index_col=None)
        except Exception as e:
            msg = 'Read %s Error, Error is:%s' % (table, str(e))
            self.error(msg)
            return

        try:
            chunksize = dbconfig['CHUNKSIZE']
            if chunksize != 'None':
                chunksize = int(dbconfig['CHUNKSIZE'])
            else:
                chunksize = None

            df.to_sql(table, engine, if_exists=dbconfig['IF_EXISTS'], index=0, chunksize=chunksize)
        except Exception as e:
            msg = 'import %s Error, Error is:%s' % (table, str(e))
            self.error(msg)
            return

        self.info('Table：% s Success load In' % table)

        return True

    def load_out_by_table(self, table:str):
        try:
            df = pd.read_sql_table(table, engine)
        except Exception as e:
            self.info('Select %s Error, Error is:%s' % (table, str(e)))
            return

        try:
            df.to_excel(self.back_path + table + ".xls")
        except Exception as e:
            self.error('import %s Error, Error is:%s' % (table, str(e)))
            return

        self.info('Table：% s Success load out' % table)
        return True

    def get_all_table_names(self):
        try:
            sql = "select table_name from information_schema.TABLES where TABLE_SCHEMA='%s' ;" % dbconfig['DBNAME']
            df = pd.read_sql(sql, engine)
        except Exception as e:
            self.error('Error is:%s' % (str(e)))
            return

        return [table[0] for table in df.values]

    def get_all_files_name(self):
        try:
            tables = []
            if not os.path.exists(self.path):
                self.error('Source Path Not Exists!!!')
                pass

            for file in os.listdir(self.path):
                if file.endswith(".xls"):
                    table=file[:-4]
                    tables.append(table)

        except Exception as e:
            self.error('Scan %s Error, Error is: %s' % (self.path, str(e)))
            return

        return tables

    def load_out_all(self):
        all_tables = self.get_all_table_names()
        if all_tables:
            self.create_thread(all_tables, self.load_out_by_table)

    def load_in_all(self):
        all_tables = self.get_all_files_name()
        # print(all_tables)
        if all_tables:
            self.create_thread(all_tables, self.load_in_by_table)
        else:
            self.error('No File Match')

    def create_thread(self, all_tables, func):
        for tb in all_tables:
            t = threading.Thread(target=func, args=(tb,))  # 创建线程
            t.start()

    def check_dir(self):
        try:
            if not os.path.isdir(self.back_path):
                os.makedirs(self.back_path, mode=755)
        except Exception as e:
            self.error('Mkdirs %s error, error is:%s' % (self.back_path, str(e)))
            exit()


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print('Python Version is too low')
        exit()

    '''
        The description parameter can be used to insert information describing script usage, which can be empty.
        Notice: formatter_class ，The purpose is to describe parameters too long without field newlines
    '''
    parser = argparse.ArgumentParser(description="Database and Excel Interoperate", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', '-v', action='version', version="%(prog)s " + config['VERSION']['version'])
    parser.add_argument('--operation', '-opt', type=int, help="Operation Detail:\n"
                                                              "    1:Load In Single Table By Table Excel Name\n"
                                                              "    2:Load Out Single Table By Table Name\n"
                                                              "    3:Load In All Files By Configure Source Path\n"
                                                              "    4:Load Out All Tables By Configure Dbname\n"
                        , choices=[1, 2, 3, 4], required=True)
    parser.add_argument('--table', '-t', default=None, help="Table Params Details\n"
                                                            "   1.The name of the Excel to be operated:\n"
                                                            "   2.There must be corresponding table names \n"
                                                            "       in the configured database.\n"
                                                            "   (When the name of the input table is empty, \n"
                                                            "    all tables in the configuration database \n"
                                                            "    are operated by default. )")
    args = parser.parse_args()

    if not args.operation:
        print("Please Select Operation number....")
        exit()

    obj = Excel2db()
    operation = args.operation
    if operation == 1:
        table = args.table
        if table:
            obj.check_dir()
            obj.load_in_by_table(table)
        else:
            pass
    elif operation == 2:
        table = args.table
        if table:
            obj.load_out_by_table(table)
        else:
            pass
    elif operation == 3:
        obj.load_in_all()
    elif operation == 4:
        obj.check_dir()
        obj.load_out_all()
    else:
        print('Operation Failed！！！')