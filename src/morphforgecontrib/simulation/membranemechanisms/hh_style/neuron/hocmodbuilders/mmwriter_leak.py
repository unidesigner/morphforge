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
from morphforge.simulation.neuron import ModFile
from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections, MHocFileData
from morphforge.simulation.neuron.hocmodbuilders import MM_ModFileWriterBase





class MM_WriterLeak(object):
    
    
    
    lkChlHoc = """
    
$(cell_name).internalsections [ $section_index ] {
    // Leak Channels
    insert $neuron_suffix         
    #for variable_name,variable_value_nounit, variable_value_with_unit,variable_unit in $variables:
    $(variable_name)_$(neuron_suffix) = $variable_value_nounit //( in $variable_unit, converted from $variable_value_with_unit)
    #end for
}
"""

    Units = { 
        "gLk": "S/cm2",
        "eLk": "mV",
        "gScale":"",
            }


    @classmethod
    def build_HOC_Section(cls, cell, section, hocFile, mta ):
        
        cell_name = hocFile[MHocFileData.Cells][cell]['cell_name']
        section_index = hocFile[MHocFileData.Cells][cell]['section_indexer'][section]
        
        neuronSuffix = mta.mechanism.getNeuronSuffix()
        
        
        # Calculate the values of the variables for the section:
        variables = []
        for variable_name in mta.mechanism.getVariables():
            variable_value_with_unit = mta.applicator.getVariableValueForSection(variable_name=variable_name, section=section)
            variable_unit = MM_WriterLeak.Units[variable_name]
            variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude 
            variables.append( [variable_name,variable_value_nounit, variable_value_with_unit,variable_unit] )
            
        tmplDict = {
                    "cell_name":cell_name,
                    "section_index":section_index,
                    "neuron_suffix":neuronSuffix,
                    "variables":variables
                    }
        
        # Add the data to the HOC file
        hocFile.addToSection( MHOCSections.InitCellMembranes,  Template(MM_WriterLeak.lkChlHoc,tmplDict ).respond() )
    


    @classmethod
    def build_Mod(cls, leakChl, modFileSet):
        
        baseWriter = MM_ModFileWriterBase(suffix=leakChl.getNeuronSuffix())
        
        gbarName = "gLk" 
        eRevName = "eLk"
        gScaleName = "gScale"  
        
        gbarUnits = MM_WriterLeak.Units[gbarName]
        eRevUnits = MM_WriterLeak.Units[eRevName]
        
        # Parameters:
        # {name: (value, unit,range)}
        baseWriter.parameters = { 
          gbarName:   (leakChl.conductance.rescale( gbarUnits ).magnitude, (gbarUnits), None),
          eRevName:   (leakChl.reversalpotential.rescale(eRevUnits).magnitude, (eRevUnits), None),
          gScaleName: (1.0, None, None)
                      }
        
        baseWriter.currentequation = "(v-%s) * %s * %s" % (eRevName, gbarName, gScaleName)
        baseWriter.conductanceequation =  "%s * %s" % (gbarName, gScaleName)
         
        modtxt = baseWriter.GenerateModFile() 
        modFile = ModFile(name=leakChl.name, modtxt=modtxt)
        modFileSet.append(modFile)
