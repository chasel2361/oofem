# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from math import isclose

class Clock:
    """
    Clock object to coordinate time integration.

    Parameters
    ----------
    increment : {time increment, float}
    input_time : {input time series, list}
    start_time : {start time stamp, float}

    Returns
    -------
    out : Clock obj

    """
    def __init__(self, increment, input_time, start_time = 0.0):
        self._inc = increment
        self._input_time = input_time
        self._time = start_time
    
    @property
    def current_time(self):
        return self._time
    
    @property
    def inc(self):
        return self._inc
    
    @property
    def input_time(self):
        return self._input_time
    
    @property
    def is_end(self):
        inp = self.input_time
        if isclose(self.current_time, inp[len(inp)-1]):
            return True
        else:
            return False
    
    @current_time.setter
    def current_time(self, value):
        self._time = value
    
    def forward(self):
        self.current_time += self.inc


