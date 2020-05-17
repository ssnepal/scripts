import unittest
from click.testing import CliRunner
import test

class TestTest(unittest.TestCase):
    def test_main(self):
        runner = CliRunner()
        result = runner.invoke(test.main, ['hi'])
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(test.main, ['config', '-k', 'ram'])
        self.assertEqual(result.exit_code,0)
        self.assertEqual(result.output,'Input the key to store [ram]: \n')

 
if __name__ == '__main__':
    unittest.main()
