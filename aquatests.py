import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from aquatech_maintask import run_calculations

class DFTests(unittest.TestCase):

    def setUp(self):
        TEST_INPUT_DIR = './'
        self.records_file_name = 'records.csv'
        self.sensors_file_name = 'sensors.csv'
        results_file = 'results.csv'
        try:
            df = pd.read_csv(TEST_INPUT_DIR + results_file,
                sep = ',',
                header = 0)
        except IOError:
            print('cannot open file')
        df.columns = ['sensor_addr', 'totals', 'leaks']
        df['sensor_addr'] = df['sensor_addr'].astype('string')
        df['totals'] = df['totals'].astype('int64')
        df['leaks'] = df['leaks'].astype('int64')
        self.fixture = df

    def test_dataFrame_constructedAsExpected(self):
        foo = run_calculations(self.sensors_file_name, self.records_file_name)
        assert_frame_equal(self.fixture, foo)