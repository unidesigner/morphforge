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
from morphforge.simulation.neuron.biophysics.mm_neuron import MM_Neuron_Base
#from mhlibs.eqnset.equationset.nmodl_writer import NMODLWriter
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment


#import quantities as pq



#from core import EqnSetChl
from morphforgecontrib.simulation.membranemechanisms.common.neuron import  build_HOC_default #MM_Neuron_GeneralisedRecord, 
from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel

import re
    



class MM_Neuron_SimulatorSpecificChannel(MM_Neuron_Base, SimulatorSpecificChannel):

    def __init__(self, modfilename=None, modtxt=None,mechanism_id=None):
        self.mechanism_id = mechanism_id
        MM_Neuron_Base.__init__(self)
        SimulatorSpecificChannel.__init__(self)
        
        assert mechanism_id
        if modfilename:
            assert not modtxt
            self.mod_text = open(modfilename).read()
        if modtxt:
            assert not modfilename
            self.mod_text = modtxt
        
        
        #SUFFIX exampleChannels3a
        
        
        r = re.compile(r"""^[^:]* SUFFIX \s* (?P<suffix>[a-zA-Z0-9_]+) (\s+:.*)? $ """, re.VERBOSE | re.MULTILINE |re.DOTALL)
        
        m = r.match(self.mod_text)
        assert m 
        nrnsuffix = m.groupdict()['suffix'] 
        
        
        
        self.name = nrnsuffix
        self.nrnsuffix = nrnsuffix
        
                
        

    def build_HOC_Section(self, cell, section, hocFile, mta ):
        #Units = dict( [ (p.symbol, pq.Quantity(1., p.get_dimension().simplified ) ) for p in self.eqnset.parameters] )
        build_HOC_default( cell=cell, section=section, hocFile=hocFile, mta=mta , units={}, nrnsuffix=self.nrnsuffix )
        
    def createModFile(self, modFileSet):
        modFile =  ModFile(name='EqnSetModfile', modtxt=self.mod_text )
        modFileSet.append(modFile)
        
    
    
    
    
    # No Internal recording or adjusting of parameters for now:
    class Recordables:
        all = []
    
    
    def getVariables(self):
        return []
        
    def getDefaults(self):
        return {}
        
    def getRecordable(self, what,  **kwargs):
        raise ValueError( "Can't find Recordable: %s"%what)
    
    
NeuronSimulationEnvironment.membranemechanisms.registerPlugin(SimulatorSpecificChannel, MM_Neuron_SimulatorSpecificChannel)

