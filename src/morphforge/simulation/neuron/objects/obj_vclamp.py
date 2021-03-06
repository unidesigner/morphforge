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
from neuronobject import NeuronObject
from morphforge.simulation.core import VoltageClamp, VoltageClampStepChange#, CurrentClamp
from morphforge.simulation.neuron.simulationdatacontainers import MHocFileData
from morphforge.core.quantities import unit
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforge.simulation.neuron.hocmodbuilders import HocBuilder
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment




class VoltageClampCurrentRecord(NeuronRecordable):
    def __init__(self, vclamp,  **kwargs):
        super(VoltageClampCurrentRecord,self).__init__(**kwargs)
        self.vclamp = vclamp    
      
    def getUnit(self):
        return unit("nA")
    def getStdTags(self):
        return [StandardTags.Current]


    def buildHOC(self, hocFile):
        objNameHoc = hocFile[MHocFileData.VoltageClamps][self.vclamp]["stimname"]
        HocModUtils.CreateRecordFromObject( hocFile=hocFile, vecname="RecVec%s"%self.name, objname=objNameHoc, objvar="i", recordobj=self )
                
    def buildMOD(self, modFileSet):
        pass
    



class MNeuronVoltageClampStepChange(VoltageClampStepChange ,NeuronObject):
    
    def __init__( self, name, simulation, **kwargs):
        VoltageClampStepChange.__init__(self, name=name, **kwargs )
        NeuronObject.__init__(self, name=name, simulation=simulation )
      
    def buildHOC(self, hocFile):
        HocBuilder.VoltageClamp( hocFile=hocFile, voltageclamp=self)
        
    def buildMOD(self, modFileSet):
        pass
    
 
    def getRecordable(self, what, name, **kwargs):
        recorders = {
              VoltageClamp.Recordables.Current : VoltageClampCurrentRecord 
        }
        
        return recorders[what]( vclamp=self, name=name, **kwargs )
        
NeuronSimulationEnvironment.voltageclamps.registerPlugin(VoltageClampStepChange, MNeuronVoltageClampStepChange)        
