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


from Cheetah.Template import Template


from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import  MHocFileData, MHOCSections
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils








class MM_Neuron_GeneralisedRecord( NeuronRecordableOnLocation):
    def __init__(self, modvar, unit, tags, nrnsuffix, **kwargs):
        super( MM_Neuron_GeneralisedRecord, self).__init__( **kwargs)
        self.unit = unit
        self.tags = tags
        self.modvar=modvar
        self.nrnsuffix = nrnsuffix
    
    def getUnit(self):
        return self.unit
    
    def getStdTags(self):
        return self.tags
    
    def buildMOD(self, modFileSet):
        pass   
 
    def buildHOC(self, hocFile):
        HocModUtils.CreateRecordFromModFile( hocFile, 
                                             vecname="RecVec%s"%self.name, 
                                             celllocation=self.where, 
                                             modvariable=self.modvar, 
                                             mod_neuronsuffix=self.nrnsuffix, 
                                             recordobj=self)
        
        
        





chlHoc = """
    
$(cell_name).internalsections [ $section_index ] {
    // Eqnset Channels 
    insert $neuron_suffix         
    #for variable_name,variable_value_nounit, variable_value_with_unit,variable_unit in $variables:
    $(variable_name)_$(neuron_suffix) = $variable_value_nounit //( in $variable_unit, converted from $variable_value_with_unit)
    #end for
}
"""



def build_HOC_default( cell, section, hocFile, mta , units, nrnsuffix):
        
    cell_name = hocFile[MHocFileData.Cells][cell]['cell_name']
    section_index = hocFile[MHocFileData.Cells][cell]['section_indexer'][section]
    
    
    # Calculate the values of the variables for the section:
    variables = []
    for variable_name in mta.mechanism.getVariables():
        variable_value_with_unit = mta.applicator.getVariableValueForSection(variable_name=variable_name, section=section)
        variable_unit = units[variable_name]
        variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude 
        variables.append( [variable_name,variable_value_nounit, variable_value_with_unit,variable_unit] )
        
    tmplDict = {
                "cell_name":cell_name,
                "section_index":section_index,
                "neuron_suffix":nrnsuffix,
                "variables":variables
                }
    
    # Add the data to the HOC file
    hocFile.addToSection( MHOCSections.InitCellMembranes,  Template(chlHoc,tmplDict ).respond() )

        
