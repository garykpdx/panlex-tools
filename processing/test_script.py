#!/usr/bin/python3

import types
import unittest

import processing

@processing.trace
def foo(n):
    for x in range(n):
        yield x
                                 

class DLFNETester(unittest.TestCase):
    def setUp(self):
        pass


    def test_trace_generator_type(self):
        gen = foo(5)
        self.assertTrue(isinstance(gen, types.GeneratorType), 'generator type returned')


    def test_trace_generator_results(self):
        gen = foo(5)
        ls = [x for x in gen]
        self.assertListEqual(ls, [0,1,2,3,4], 'should give results from generator')


        
if __name__ == '__main__':
    unittest.main()
