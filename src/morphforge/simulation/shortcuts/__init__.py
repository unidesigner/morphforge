#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
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


from morphforge.simulation.core.biophysics import * 

def ApplyMechanismUniform( cell, mechanism, targetter, parameter_multipliers={}, parameter_overrides= {}):
    vals = mechanism.getDefaults()
        
    # Make it easy to scale values
    for k,v in parameter_multipliers.iteritems():
        if not k in vals:
            print 'Invalid Parameter:',k
            print 'Available Params:', vals
            assert False
        vals[k] = vals[k] * v
    
     # Make it easy to over-ride
    for k,v in parameter_overrides.iteritems():
        assert k in vals
        vals[k] = v
    
    cell.getBiophysics().addMechanism(mechanism=mechanism, 
                                        targetter= targetter, 
                                        applicator=MembraneMechanismApplicator_Uniform(vals) )




def ApplyMechanismEverywhereUniform( cell, mechanism, parameter_multipliers={}, parameter_overrides= {}):
    return ApplyMechanismUniform( cell=cell, 
                                     mechanism=mechanism, 
                                     targetter=MembraneMechanismTargeter_Everywhere(), 
                                     parameter_multipliers=parameter_multipliers, 
                                     parameter_overrides= parameter_overrides)

def ApplyMechanismRegionUniform( cell, mechanism, region, parameter_multipliers={}, parameter_overrides= {}):
    return ApplyMechanismUniform( cell=cell, 
                                  mechanism=mechanism, 
                                  targetter=MembraneMechanismTargeter_Region(region), 
                                  parameter_multipliers=parameter_multipliers, 
                                  parameter_overrides= parameter_overrides)



def ApplyPassiveEverywhereUniform( cell, passiveproperty, value):
    assert passiveproperty in PassiveProperty.all
    cell.getBiophysics().addPassive(passiveproperty=passiveproperty, 
                                        targetter= PassiveTargeter_Everywhere(), 
                                        value = value)

