#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.core.mgrs.settingsmgr import SettingsMgr 
import morphforge.core.quantities.unit_string_parser
import morphforge.core.quantities.unit_string_lexer  
import quantities as pq
from morphforge.core.misc import isFloat, isInt


# Required to initialise the unit definitions
import common_neuroscience_defs
from quantities.quantity import Quantity




def quantity_unit_to_string(pquantity):
    return str( pquantity )
    



def FactoriseUnitsFromList( seq ):
    assert len(seq) > 0
    
    for o in seq:
        assert isinstance( o, Quantity)
    
    s0unit = seq[0].units    
    newList = [ o.rescale(s0unit).magnitude for o in seq] * s0unit 
    return newList


    
     






def convertToUnit(o, defaultUnit):
    assert not isinstance( defaultUnit, (pq.quantity.Quantity,) )

    if isinstance(o, pq.quantity.Quantity):
        return o.rescale(defaultUnit)
    elif isFloat(o) or isInt(o):
        return o * morphforge.core.quantities.unit_string_parser.parse( defaultUnit ).rescale(defaultUnit)
    elif isinstance(o, (str, unicode)) and ":" in o:
        return unit(o).rescale(defaultUnit)
    else:
        raise ValueError()
    



definedUnitStrings = {
                      "J/K/mol": pq.J / pq.K / pq.mol
                      }


def unit(s):
    if isinstance(s, pq.quantity.Quantity):
        return s
    
    if isFloat(s): 
        return float(s) * pq.dimensionless
    
    if isinstance(s, list):
        return [ unit(x) for x in s]
    if isinstance(s, dict):
        return dict([ (k, unit(v)) for k, v in s.iteritems()])
    
    if ":" in s:
        valueStr, unitStr = s.split(":")
        
        if SettingsMgr.allowEvalInLoading: 
            v = float(eval(valueStr)) 
        else: 
            v = float(valueStr)
        
        
        if unitStr in definedUnitStrings:
            unt = definedUnitStrings[unitStr]
        else: 
            unt = morphforge.core.quantities.unit_string_parser.parse( unitStr )
        
        return v * unt
        
    if " " in s:
        t = s.split(" ")
        
        if len(t) == 2:
            
            valueStr, unitStr = t
            if SettingsMgr.allowEvalInLoading: 
                v = float(eval(valueStr)) 
            else: 
                v = float(valueStr)
            
            unt = morphforge.core.quantities.unit_string_parser.parse( unitStr )
            
            return v * unt
                    
    
     
    return  morphforge.core.quantities.unit_string_parser.parse( s )





def get_constant(k):
    assert False, 'Deprecated'
    if k in pq.__dict__:
        v = pq.__dict__[k]
        
