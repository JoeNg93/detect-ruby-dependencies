import unittest
import parse_ruby_project as parse

class MyTest(unittest.TestCase):

    def test_is_valid_git_link(self):
        self.assertTrue(parse.is_valid_git_link('https://github.com/JoeNg93/Fitsmind_Test_Backend.git'))
        self.assertTrue(parse.is_valid_git_link('git@github.com:JoeNg93/Fitsmind_Test_Backend.git'))
        self.assertFalse(parse.is_valid_git_link('https'))
        self.assertFalse(parse.is_valid_git_link('https://www.google.com'))
        self.assertFalse(parse.is_valid_git_link('/Volumes/Data/ruby_project'))

    def test_is_ruby_file(self):
        self.assertTrue(parse.is_ruby_file('test.rb'))
        self.assertFalse(parse.is_ruby_file('test.html'))
        self.assertFalse(parse.is_ruby_file('asbas'))

    def test_get_ruby_files_from_list(self):
        ruby_files = parse.get_ruby_files_from_list(['test1.rb', 'test2.rb', 'test.html', 'test.ex'])
        self.assertEqual(len(ruby_files), 2)

        ruby_files = parse.get_ruby_files_from_list(['test.html', 'test.java'])
        self.assertEqual(len(ruby_files), 0)
    

if __name__ == '__main__':
    unittest.main()
    