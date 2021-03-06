#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
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


from morphforge.morphology.importer.morphologyimporter import MorphologyImporter
from morphforge.core.misc import MergeDictionaries, Flatten, CheckValidName
from morphforge.morphology.core.region import Region
from morphforge.morphology.core.section import Section
import math
from morphforge.morphology.core.morphologytree import MorphologyTree


class DictionaryLoader(object):
    @classmethod
    def Load(cls,  morphDict, name=None, metaData=None):
        """ Load a morphology from a recursive dictionary such as:
        {'root': {'length': 20, 'diam': 20, 'sections': 
            [
                {'absangle': 120, 'length': 40, 'diam': 5, 'region': 'dendrite'}, 
                {'absangle': 240, 'length': 40, 'diam': 5, 'sections': 
                    [
                        {'region': 'dendrite', 'diam': 5, 'relangle': 240, 'length': 40}
                    ], 'region': 'dendrite'},
                {'absangle': 5, 'length': 500, 'diam': 0.29999999999999999, 'region': 'axon'}], 
            'region': 'soma'}}
            
            If addRootSection is true, then we make the root section, by adding in a fake section:
            
        """

        
        if not morphDict or not morphDict.has_key("root"): raise ValueError()
        validKeywords = ["length", "diam", "id", "sections", "region", 'regions', "relangle", "absangle", "xyz"]
        requiredKeywords = ["diam"]



        # Does the root has a length variable? if it does, then lets add an intermediate node and remove it.
        rootNode = morphDict["root"]
        if rootNode.has_key('length'):
          # Lets assume it extends backwards on the X-axis. This isn't great, but will work, although 
          # visualisations are likely to look a bit screwy:
          
          assert not rootNode.has_key('xyz')
          
          #print rootNode
          
          
          #del rootNode['length'] 
          newRootNode =  {'region': 'soma', 'diam': rootNode['diam'], 'xyz':(0.0,0.0,0.0), 'sections': [rootNode]}
           
          #print newRootNode
           
          rootNode = newRootNode
          
          #assert False
              
          #sectionDict[None] = Section(x=0.0, y=0.0, z=0.0, r=rootYamlSect['diam'] / 2.0, region=None, parent=None)

      

            


        
        #First flatten the recursion, by copy 
        #the dictionary and adding a parent tag:
        yamlSectionDict = {} # id to paramDict
        def recursivelyAddSectionToList(sectionNode, sectionNodeParentID, sectionDictInt):
            for k in sectionNode.keys(): 
                if not k in validKeywords: raise ValueError("Invalid Keyword: " + k)
            for rK in requiredKeywords: 
                if not rK in sectionNode.keys(): raise ValueError("Required Key: %s not found." % rK)
                
            children = sectionNode.get("sections", []) 
            if sectionNode.has_key("sections"): del sectionNode["sections"]  
            sectionID = len(sectionDictInt)
            sectionDictInt[sectionID] = MergeDictionaries([{"parent": sectionNodeParentID}, sectionNode])
            for c in children:  recursivelyAddSectionToList(c, sectionID, sectionDictInt)     
        
        #rootNode = morphDict["root"]
       
        recursivelyAddSectionToList(rootNode, None, yamlSectionDict) 
        
        
        #We now have a dictionary similar to:
        """ 0 {'length': 20, 'diam': 20, 'region': 'soma', 'parent': None}
            1 {'absangle': 120, 'length': 40, 'diam': 5, 'region': 'dendrite', 'parent': 0}
            2 {'absangle': 240, 'length': 40, 'diam': 5, 'region': 'dendrite', 'parent': 0}
            3 {'length': 40, 'region': 'dendrite', 'diam': 5, 'relangle': 240, 'parent': 2}
            4 {'absangle': 5, 'length': 500, 'diam': 0.29999999999999999, 'region': 'axon', 'parent': 0} 
        """
        
        #Map a lack of region to region:"NoRegionGiven"
        for yml in yamlSectionDict.values():
            if not ("region" in yml or "regions" in yml):
                yml["region"] = "NoRegionGiven"
        
        regionNames1 = [ yml["region"] for yml in yamlSectionDict.values() if yml.has_key("region") ]
        regionNames2 = Flatten([ yml["regions"] for yml in yamlSectionDict.values() if yml.has_key("regions") ])
        
        regionNames = list(set( regionNames1 + regionNames2) )
        regionDict = dict([ (n, Region(n)) for n in regionNames])
        sectionAnglesDict = {}
        sectionIdTags = []
        
        
        
        
        # We create a 'dummy' root node, and then the real root node.
        # This will be at index '0'
        
        # Do we need to create a dummy node explicity? This depends on whether the root node has a length:
        sectionDict = {}
        rootYamlSect = yamlSectionDict[0]
        
        
        if 'length' in rootYamlSect.keys():
            assert False
            #sectionDict[None] = Section(x=0.0, y=0.0, z=0.0, r=rootYamlSect['diam'] / 2.0, region=None, parent=None)
        else:
            pass 
            #sectionDict[None] = Section(x=0.0, y=0.0, z=0.0, r=rootYamlSect['diam'] / 2.0, region=None, parent=None)
            #assert False
        
        
        
        
        xyz = rootYamlSect['xyz']
        sectionDict[0] = Section(x=xyz[0], y=xyz[1], z=xyz[2], r=rootYamlSect['diam'] / 2.0, region=None, parent=None)
        
        # Add the remaining nodes:
        for yamlID, yamlSect in yamlSectionDict.iteritems():
            
            if yamlSect['parent'] == None:
                continue
            
            #print yamlID, yamlSect
            
            parentSection = sectionDict[ yamlSect["parent"] ]
            
            #Region:
            rgNames1 = [ yamlSect["region"] ] if yamlSect.has_key("region") else [] 
            rgNames2 = yamlSect["regions"] if yamlSect.has_key("regions") else []
            rgs = [ regionDict[rgName] for rgName in rgNames1 + rgNames2   ]  
            # Since December 2010 each section is only allowed to have one
            # region.
            assert len(rgs) <= 1

            #Diameter & length:
            if not yamlSect.has_key("diam") or not (yamlSect["diam"] > 0): raise ValueError("indvalid radius")   
            rad = yamlSect["diam"] / 2.0
            
            
            
            
            
            # End Point:
            def getYamlLength(yamlSect):
                if not yamlSect.has_key("length"): raise ValueError("No Length given")
                length = yamlSect["length"]
                if not length > 0: raise ValueError("Invalid Length")
                return length
             
            #We only specify end points by using angles or by xyz cooridinates:
            if int(yamlSect.has_key("absangle")) + int(yamlSect.has_key("relangle")) + int(yamlSect.has_key("xyz")) >= 2:
                raise ValueError("Too many ways for specifying endpoint")
            
            if yamlSect.has_key("xyz"):
                if not parentSection: angle = 0 
                xyz = yamlSect["xyz"] 
                
                
            elif yamlSect.has_key("absangle"):
                length = getYamlLength(yamlSect)
                angle = yamlSect["absangle"]
                xyz = (parentSection.d_x + length * math.cos(math.radians(angle)), parentSection.d_y + length * math.sin(math.radians(angle)), 0.0)
                
            elif yamlSect.has_key("relangle"):
                length = getYamlLength(yamlSect)
                angle = sectionAnglesDict[parentSection] + yamlSect["relangle"]
                xyz = (parentSection.d_x + length * math.cos(math.radians(angle)), parentSection.d_y + length * math.sin(math.radians(angle)), 0.0)
                
            else: # Default to 'abs'-angle to 0
                length = getYamlLength(yamlSect)
                angle = 0
                xyz = (parentSection.d_x + length * math.cos(math.radians(angle)), parentSection.d_y + length * math.sin(math.radians(angle)), 0.0)
                

            
            #Possible ID's:
            sectionIdTag = yamlSect["id"] if yamlSect.has_key("id") else None  
            if sectionIdTag:
                CheckValidName(sectionIdTag)
            if sectionIdTag in sectionIdTags: 
                raise ValueError("Duplicate Section ID: %s" % sectionIdTag)
            if sectionIdTag:  sectionIdTags.append(sectionIdTag)
            
            
            # Create the new section:
            if parentSection:
                newSection = parentSection.extrudeChildSection(x=xyz[0], y=xyz[1], z=xyz[2], r=rad, region=rgs[0], idTag=sectionIdTag)
            else:
                newSection = Section(x=xyz[0], y=xyz[1], z=xyz[2], r=rad, region=None, idTag=sectionIdTag)
                sectionDict[None] = newSection
            
            
            
                
            # Calculate the angle of the current section:
            if parentSection:
                joiningVec = newSection.getDistalNPA3() - parentSection.getDistalNPA3()
                angle = math.radians(math.atan2(joiningVec[1], joiningVec[0]))
            sectionAnglesDict[newSection] = angle
            
            
            #Save the section:
            sectionDict[yamlID] = newSection   
            
            
        ## TODO: THIS IS A HACK! Ensure the dummy node has no attached regions:
        #sectionDict[None].regions = []
        assert sectionDict[0].region == None 
    
        if sectionDict[0].children == []: raise ValueError("No segments found")
        c = MorphologyTree(name=name, dummysection=sectionDict[0], metadata=metaData)
        if len(c) < 1: raise ValueError
        return c
    
    

MorphologyImporter.register("fromDictionary", DictionaryLoader.Load, allow_override=False, as_type=MorphologyTree) 
