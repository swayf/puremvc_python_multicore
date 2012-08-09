from nose.tools import ok_, eq_
from puremvc_multicore.patterns.mediator import Mediator

def testNameAccessor():
    """MediatorTest: Test get_mediator_name()"""
    mediator = Mediator()
    eq_(mediator.get_mediator_name(), 'Mediator' )


def testViewAccessor():
    """MediatorTest: Test get_view_component()"""
    mediator = Mediator(view_component=object)
    ok_(mediator.get_view_component() is not None)
