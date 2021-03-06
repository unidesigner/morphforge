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


class SummariserLibrary():
    
    summarisers = { }
    
    @classmethod
    def registerSummariser(cls, channelBaseClass, summariserClass ):
        # Check it has a toReportLab Method:
        # Todo: Replace this with 'hasattr'
        assert "toReportLab" in summariserClass.__dict__
        
        # Add it to the dictionary of summarisers:
        cls.summarisers[channelBaseClass] = summariserClass 
        
        
        
         
                   
    @classmethod
    def getSummarisier(cls, obj):
        possibleSummarisers = []
        for ChlType, summarisier in SummariserLibrary.summarisers.iteritems():
            if issubclass(type(obj), ChlType ):
                possibleSummarisers.append( summarisier )
        
        if len(possibleSummarisers) == 0:
            return None
        if len(possibleSummarisers) == 1:
            return possibleSummarisers[0]
        else:
            assert False, "I have to many options for summarising: " + str(obj)
        
