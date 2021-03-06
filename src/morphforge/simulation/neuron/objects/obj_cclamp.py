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
from morphforge.simulation.core import CurrentClamp
from neuronobject import NeuronObject
from morphforge.simulation.neuron.simulationdatacontainers import MHocFileData
from morphforge.core.quantities import unit
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforge.simulation.neuron.hocmodbuilders import HocBuilder
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.core.stimulation.currentclamps import CurrentClampStepChange
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment






class CurrentClampCurrentRecord(NeuronRecordable):
    def __init__(self, cclamp, **kwargs):
        super(CurrentClampCurrentRecord,self).__init__(**kwargs)
        self.cclamp = cclamp    

    def getUnit(self):
        return unit("nA")
    def getStdTags(self):
        return [StandardTags.Current] 


    def buildHOC(self, hocFile):
        nameHoc = hocFile[MHocFileData.CurrentClamps][self.cclamp]["stimname"]
        HocModUtils.CreateRecordFromObject( hocFile=hocFile, vecname="RecVec%s"%self.name, objname=nameHoc, objvar="i", recordobj=self )

    def buildMOD(self, modFileSet):
        pass
    



class MNeuronCurrentClampStepChange(CurrentClampStepChange,NeuronObject):
    def __init__( self, simulation, amp, dur, delay, celllocation, name=None):
        CurrentClampStepChange.__init__(self, name=name, amp=amp, dur=dur, delay=delay, celllocation=celllocation )
        NeuronObject.__init__(self, name=name, simulation=simulation )
        

    def buildHOC(self, hocFile):
        HocBuilder.CurrentClamp( hocFile=hocFile, currentClamp=self)
        
    def buildMOD(self, modFileSet):
        pass

    def getRecordable(self, what, name=None, **kwargs):
        recorders = {
              CurrentClamp.Recordables.Current : CurrentClampCurrentRecord 
        }
        
        return recorders[what]( cclamp=self, name=name, **kwargs )
    

NeuronSimulationEnvironment.currentclamps.registerPlugin(CurrentClampStepChange, MNeuronCurrentClampStepChange)
