#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import quantities as pq

import operator
from morphforge.traces.tracetypes  import Trace_FixedDT

from morphforge.traces.trace_operators_ctrl import TraceOperatorCtrl



class TraceOperator_TraceFixedDT_Quantity(object):
    @classmethod
    def do_add(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == pq.Quantity ) or \
               ( type(rhs) == Trace_FixedDT and type(lhs) == pq.Quantity )
        
        if type(lhs) == Trace_FixedDT:
            return Trace_FixedDT( lhs._time,  lhs._data + rhs)
        else:
            return Trace_FixedDT( rhs._time,  rhs._data + lhs)
    
    @classmethod
    def do_sub(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == pq.Quantity ) or \
             ( type(rhs) == Trace_FixedDT and type(lhs) == pq.Quantity )
        
        if type(lhs) == Trace_FixedDT:
            return Trace_FixedDT( lhs._time,  lhs._data - rhs)
        else:
            return Trace_FixedDT( rhs._time,  rhs._data - lhs)
    @classmethod
    def do_mul(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == pq.Quantity ) or \
               ( type(rhs) == Trace_FixedDT and type(lhs) == pq.Quantity )
        
        if type(lhs) == Trace_FixedDT:
            return Trace_FixedDT( lhs._time,  lhs._data * rhs)
        else:
            return Trace_FixedDT( rhs._time,  rhs._data * lhs)
    
    @classmethod
    def do_div(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == pq.Quantity ) or \
               ( type(rhs) == Trace_FixedDT and type(lhs) == pq.Quantity )
        
        if type(lhs) == Trace_FixedDT:
            return Trace_FixedDT( lhs._time,  lhs._data / rhs)
        else:
            return Trace_FixedDT( rhs._time,  rhs._data / lhs)





class TraceOperator_TraceFixedDT_Scalar(object):
    @classmethod
    def do_add(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == float ) or \
               ( type(rhs) == Trace_FixedDT and type(lhs) == float )
        
        if type(lhs) == Trace_FixedDT:
            assert isinstance(lhs._data, pq.Dimensionless)
            return Trace_FixedDT( lhs._time,  lhs._data + rhs)
        else:
            assert isinstance(rhs._data, pq.Dimensionless)
            return Trace_FixedDT( rhs._time,  rhs._data + lhs)

    @classmethod
    def do_sub(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == float ) or \
             ( type(rhs) == Trace_FixedDT and type(lhs) == float )
        
        if type(lhs) == Trace_FixedDT:
            assert isinstance(lhs._data, pq.Dimensionless)
            return Trace_FixedDT( lhs._time,  lhs._data - rhs)
        else:
            assert isinstance(rhs._data, pq.Dimensionless)
            return Trace_FixedDT( rhs._time,  rhs._data - lhs)
        
    @classmethod
    def do_mul(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == float ) or \
               ( type(rhs) == Trace_FixedDT and type(lhs) == float )
        
        if type(lhs) == Trace_FixedDT:
            return Trace_FixedDT( lhs._time,  lhs._data * rhs)
        else:
            return Trace_FixedDT( rhs._time,  rhs._data * lhs)

    @classmethod
    def do_div(self, lhs, rhs):
        assert ( type(lhs) == Trace_FixedDT and type(rhs) == float ) or \
               ( type(rhs) == Trace_FixedDT and type(lhs) == float )
        
        if type(lhs) == Trace_FixedDT:
            assert isinstance(lhs._data, pq.Dimensionless)
            return Trace_FixedDT( lhs._time,  lhs._data / rhs)
        else:
            assert isinstance(rhs._data, pq.Dimensionless)
            return Trace_FixedDT( rhs._time,  rhs._data / lhs)

TraceOperatorCtrl.add_trace_operator( operator_type = operator.__add__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TraceFixedDT_Quantity.do_add,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__sub__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TraceFixedDT_Quantity.do_sub,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__mul__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TraceFixedDT_Quantity.do_mul,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__div__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TraceFixedDT_Quantity.do_div,
                                      flag='default' )


TraceOperatorCtrl.add_trace_operator( operator_type = operator.__add__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = float,
                                      operator_func = TraceOperator_TraceFixedDT_Scalar.do_add,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__sub__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = float,
                                      operator_func = TraceOperator_TraceFixedDT_Scalar.do_sub,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__mul__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = float,
                                      operator_func = TraceOperator_TraceFixedDT_Scalar.do_mul,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__div__, 
                                      lhs_type = Trace_FixedDT,
                                      rhs_type = float,
                                      operator_func = TraceOperator_TraceFixedDT_Scalar.do_div,
                                      flag='default' )
