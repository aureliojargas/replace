import unittest
import replace


class TestReplace(unittest.TestCase):

    def test_examples_in_docstring(self):
        # Those examples are inserted in the --help message
        self.assertTrue(replace.__doc__.startswith('\nExamples:'))

    def test_read_file(self):
        self.assertTrue(
            replace.read_file(__file__).startswith('import unittest'))


class TestConfigValidation(unittest.TestCase):

    def setUp(self):
        import argparse
        self.config = argparse.Namespace()
        self.config.from_file = None
        self.config.to_file = None
        self.config.from_ = None
        self.config.to = None

    def test_validate_config_from_to(self):
        self.config.from_ = 'f'
        self.config.to = 't'
        replace.validate_config(self.config)
        self.assertEqual('f', self.config.from_value)
        self.assertEqual('t', self.config.to_value)


if __name__ == '__main__':
    unittest.main()
