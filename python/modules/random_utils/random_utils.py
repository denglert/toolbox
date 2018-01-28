#!/usr/bin/env python

class lcg:
	"""A very simple implementation of a linear congruential generator."""
    
    def __init__(self, multiplier=40692, increment=0, modulo=2147483399, seed=42):
        self.rand = seed
        self.multiplier = multiplier
        self.increment = increment
        self.modulo = modulo
        
    def getRand(self):
        self.rand = (self.rand * self.multiplier) % self.modulo
        return self.rand
    
    def getRandUni(self):
        self.getRand()
        return self.rand / self.modulo
