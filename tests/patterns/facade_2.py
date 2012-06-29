from nose.tools import *
from puremvc.patterns.facade import Facade


class CustomFacade(Facade):
    pass


def testCustomFacade():
    f1 = CustomFacade('test_1')
    f2 = Facade('test_1')
    f3 = CustomFacade('test_2')

    ok_(f1 is f2)
    ok_(f2 is not f3)

