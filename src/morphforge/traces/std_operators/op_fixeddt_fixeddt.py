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
import operator
from morphforge.traces.tracetypes  import Trace_FixedDT
from morphforge.traces.traceGenerator import NpPqWrappers

from morphforge.traces.trace_operators_ctrl import TraceOperatorCtrl



class TraceOperator_TraceFixedDT_TraceFixedDT(object):

    @classmethod
    def get_new_time_axis(cls, lhs, rhs):
        assert type(lhs) == Trace_FixedDT
        assert type(rhs) == Trace_FixedDT

        minTime = max( lhs.getMinTime(), rhs.getMinTime()  )
        maxTime = min( lhs.getMaxTime(), rhs.getMaxTime()  )
        
        newDT = min( lhs.getDTNew(), rhs.getDTNew() )
        assert maxTime - minTime > newDT * 2, 'The new trace will only have a single point'
        return NpPqWrappers.arange( minTime, maxTime, newDT )
  
    @classmethod
    def do_add(cls, lhs, rhs):
        timeAxis = cls.get_new_time_axis(lhs,rhs)
        return Trace_FixedDT(timeAxis, lhs.getValues(timeAxis) + rhs.getValues(timeAxis) )

    @classmethod
    def do_sub(cls, lhs, rhs):
        timeAxis = cls.get_new_time_axis(lhs,rhs)
        return Trace_FixedDT(timeAxis, lhs.getValues(timeAxis) - rhs.getValues(timeAxis) )

    @classmethod
    def do_mul(cls, lhs, rhs):
        timeAxis = cls.get_new_time_axis(lhs,rhs)
        return Trace_FixedDT(timeAxis, lhs.getValues(timeAxis) * rhs.getValues(timeAxis) )
    @classmethod
    def do_div(cls, lhs, rhs):
        timeAxis = cls.get_new_time_axis(lhs,rhs)
        return Trace_FixedDT(timeAxis, lhs.getValues(timeAxis) / rhs.getValues(timeAxis) )

# FixedDT (+-*/) FixedDT
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__add__, 
                                      lhs_type = Trace_FixedDT, rhs_type = Trace_FixedDT,
                                      operator_func = TraceOperator_TraceFixedDT_TraceFixedDT.do_add,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__sub__, 
                                      lhs_type = Trace_FixedDT, rhs_type = Trace_FixedDT,
                                      operator_func = TraceOperator_TraceFixedDT_TraceFixedDT.do_sub,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__mul__, 
                                      lhs_type = Trace_FixedDT, rhs_type = Trace_FixedDT,
                                      operator_func = TraceOperator_TraceFixedDT_TraceFixedDT.do_mul,
                                      flag='default' )
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__div__, 
                                      lhs_type = Trace_FixedDT, rhs_type = Trace_FixedDT,
                                      operator_func = TraceOperator_TraceFixedDT_TraceFixedDT.do_div,
                                      flag='default' )

