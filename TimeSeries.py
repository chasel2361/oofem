class TimeSeries:
    """
    TimeSeries object to control FEM timing.

    Parameters
    ----------
    init : {initial time, float}
    interval : {time interval, float}
    record_in : {input series, list}

    """
    def __init__(self, init, interval, record_in):
        self.init = init
        self.interval = interval
        self.record_in = record_in
        
    
    def at(self, t):
        """
        Return value at specific time stamp by linear interploation.
        
        Parameters
        ----------
        t : {time stamp, float}

        Returns
        -------
        out : float
        
        """
        t0 = self.init
        dt = self.interval
        rec = self.record_in
        i = int((t - t0) // dt)
        increment = (rec[i+1] - rec[i])/dt * (t - (t0 + dt * i))
        result = rec[i] + increment
        return result