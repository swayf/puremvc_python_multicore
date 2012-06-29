import unittest

import puremvc_multicore.patterns.mediator as mediator

class MediatorTest(unittest.TestCase):
    """MediatorTest: Test Mediator Pattern"""

    def testNameAccessor(self):
        """MediatorTest: Test get_mediator_name()"""
        mdiatr = mediator.Mediator();
        self.assertEqual(True, mdiatr.get_mediator_name() == mediator.Mediator.NAME );

    def testViewAccessor(self):
        """MediatorTest: Test get_view_component()"""

        view = object()
        mdiatr = mediator.Mediator(mediator.Mediator.NAME, view);
        self.assertEqual(True, mdiatr.get_view_component() is not None)
