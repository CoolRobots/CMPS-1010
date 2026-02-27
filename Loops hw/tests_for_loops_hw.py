from unittest.mock import patch, call   
from unittest import TestCase
from loops_hw import *
import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility

class CreateTests(TestCase):
    @weight(10)
    @number('1')
    @visibility('visible')
    @patch('builtins.print')
    def test_diamond(self,mocked_print):
        diamond_of_stars(3)
        assert mocked_print.mock_calls== [call("  *"), call(" * *"), call("* * *"), call(" * *"), call("  *")]
        mocked_print.mock_calls = []
        diamond_of_stars(5)
        assert mocked_print.mock_calls== [call("    *"), call("   * *"), call("  * * *"), call(" * * * *"), call("* * * * *"),
                                          call(" * * * *"), call("  * * *"), call("   * *"), call("    *")]
    @weight(10)
    @number('2')
    @visibility('visible')
    def test_weird_sequence(self):
        assert weird_sequence(1)==[1,2,3,4,5,6,7,8,9]
        assert weird_sequence(2)==[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90]
        assert weird_sequence(3)==[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900]
        assert len(weird_sequence(8))==8*9

    @weight(10)
    @number(3)
    @visibility('visibile')
    def test_repeated_letters(self):
        assert count_double_letters("raccoons appear, skiing weekly.")==5
        assert count_double_letters("hmmm...?")==4
        assert count_double_letters("double  spaced  words")==2
if __name__=="__main__":
    unittest.main()
