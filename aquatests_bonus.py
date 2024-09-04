import unittest
from unittest.mock import patch

import pandas as pd
from pandas.testing import assert_frame_equal

#import os
#cwd = os.getcwd()
#print(cwd)

#import sys
#sys.path.append('../')
import aquatech_bonus
def args_based_return(t):
    if t == 1640991600:
        return '1-1-2024'
    return '2-1-2024'

class DFTests(unittest.TestCase):

    def setUp(self):
        TEST_INPUT_DIR = './'
        self.records_file_name = 'records.csv'
        self.sensors_file_name = 'sensors.csv'
        results_file2 = 'results2.csv'
        results_file3 = 'results3.csv'
        try:
            df = pd.read_csv(TEST_INPUT_DIR + results_file2,
                sep = ',',
                header = 0)
        except IOError:
            print('cannot open file')
        df.columns = ['timestamp', 'leaks']
        df['timestamp'] = df['timestamp'].astype('string')
        df['leaks'] = df['leaks'].astype('int64')
        self.fixture2 = self.read_file(TEST_INPUT_DIR + results_file2)
        self.fixture3 = self.read_file(TEST_INPUT_DIR + results_file3)
    
    def read_file(self, fpath):
        try:
            df = pd.read_csv(fpath,
                sep = ',',
                header = 0)
        except IOError:
            print('cannot open file')
        df.columns = ['timestamp', 'leaks']
        df['timestamp'] = df['timestamp'].astype('string')
        df['leaks'] = df['leaks'].astype('int64')
        return df

    def test_dataFrame_onesingleday(self):
        foo = aquatech_bonus.run_calculations(self.sensors_file_name, self.records_file_name)
        assert_frame_equal(self.fixture2, foo)

    def test_dataFrame_twodays(self):
        aquatech_bonus.ATUtils = unittest.mock.Mock()
        aquatech_bonus.ATUtils.print_day.side_effect = args_based_return
        foo = aquatech_bonus.run_calculations(self.sensors_file_name, self.records_file_name)
        assert_frame_equal(self.fixture3, foo)