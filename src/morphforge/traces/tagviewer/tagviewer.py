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
from morphforge.core import Flatten, isIterable
from morphforge.simulation.core import SimulationResult, SimulationResultSet
#from morphforge.constants.standardtags import StandardTags
from morphforge.core.quantities import mV, ms, Quantity
from mhlibs.quantities_plot import QuantitiesFigure
#from plotspecs import PlotSpec_Default 
from plotspecs import PlotSpec_DefaultNew
from morphforge.core.mgrs.settingsmgr import SettingsMgr
from morphforge.traces import  Trace_FixedDT, Trace_VariableDT, Trace_Piecewise
from morphforge.traces.eventset import EventSet
from morphforge.core import quantities as pq
from mhlibs.scripttools import PM
#from morphforge.traces.tracePiecewise import TracePieceFunctionLinear, Trace_Piecewise



        

def resolveTimeRange(timeRange):
    # Sort out the timeRange:
    if timeRange is not None:
        if  isinstance(timeRange, (tuple, list, Quantity) ):
            if len(timeRange) == 2:
                if isinstance(timeRange[0], Quantity ):
                    pass
                else:
                    assert False
                    timeRange = timeRange * ms
        else:
            assert False    
    return timeRange


class TagViewer(object):
    
    defaultPlotSpecs = (   
                PlotSpec_DefaultNew( s="Voltage", ylabel='Voltage', yrange=(-60*mV,40*mV)  ),
                PlotSpec_DefaultNew( s="CurrentDensity", ylabel='CurrentDensity', yunit=pq.milliamp/pq.cm2  ),
                PlotSpec_DefaultNew( s="Current", ylabel='Current',yunit=pq.picoamp ), 
                PlotSpec_DefaultNew( s="Conductance", ylabel="Conductance" ),
                PlotSpec_DefaultNew( s="ConductanceDensity", ylabel="ConductanceDensity", yunit=pq.milli * pq.siemens / pq.cm2  ),
                PlotSpec_DefaultNew( s="StateVariable", ylabel="StateVariable" ), 
                PlotSpec_DefaultNew( s="StateTimeConstant",yunit=pq.millisecond, ylabel="Time Constant"  ),
                PlotSpec_DefaultNew( s="StateSteadyState", ylabel="Steady State" ),                 
                PlotSpec_DefaultNew( s="Event", ylabel="Events" ),

                )
    


    
    def __init__(self, 
                 input, 
                 tags=None, 
                 fig_kwargs = {'figsize': (12, 8)},
                 timeranges=(None,), 
                 plotspecs = None,
                 post_ax_functors= None,
                 figtitle = None,
                 show=True,
                 linkage = None, 
                 timerange=None,
                 additional_plotspecs = None,
                 ):
        
        self.linkage = linkage
        
        
        if timerange is not None:
            timeranges = [timerange,]
        
        
        if not isIterable( input ):
            input = [input]
            
        
        
        # For each type of input; this should return a list of traces:
        self.allTraceObjs = []
        self.allEventSetObjs = []
        trace_extractors = {
            SimulationResult:       lambda i: self.allTraceObjs.extend( i.traces ),  
            SimulationResultSet:    lambda i: self.allTraceObjs.extend( Flatten( [s.traces for s in i] ) ),
            Trace_FixedDT:          lambda i: self.allTraceObjs.append( i ),           
            Trace_VariableDT:       lambda i: self.allTraceObjs.append( i ),
            Trace_Piecewise:        lambda i: self.allTraceObjs.append( i ),
            EventSet:               lambda i: self.allEventSetObjs.append(i) 
                            }    
        
        for i in input:
            print i
            tr_extractor = trace_extractors[ type(i) ]
            tr_extractor(i) 
            
        
         
        
        # Work Around: if tags are supplied, then lets convert them into a PlotSpec:
        if tags:
            assert False
            assert not plotspecs
            plotspecs = [ PlotSpec_Default(tags=t) for t in tags ]
            
        
        
        
        # Use the new PlotSpec architecture:
        # Filter out which plotspecs are actually going to display something,
        # and filter out the rest:
        plotspecs = plotspecs or TagViewer.defaultPlotSpecs 
        
        if additional_plotspecs:
            plotspecs = tuple( list(plotspecs) + list(additional_plotspecs) ) 
        
        self.plot_specs = [ sp for sp in plotspecs if 
                            [ tr for tr in self.allTraceObjs if sp.addtrace_predicate(tr)] or  \
                            [ evset for evset in self.allEventSetObjs if sp.addeventset_predicate(evset)] \
                           ]
        
        
        self.fig_kwargs = fig_kwargs
        self.figtitle = figtitle
        
        self.post_ax_functors = post_ax_functors
        
        self.timeranges = timeranges 
        
        
        self.fig = None
        self.subaxes = []
        self.Render()
        
        
        
        # Save the figure:
        PM.SaveFigure( figtitle )
        
        
        if SettingsMgr.tagViewerAutoShow() and show:
            import pylab
            pylab.show()
        
        
    
    def Render(self):
        self.fig = QuantitiesFigure(**self.fig_kwargs)
        
        
        # Add a title to the plot:
        if self.figtitle:
            self.fig.suptitle(self.figtitle)
        

        # Work out what traces are on what graphs:
        ps_to_traces = dict([ (ps,[tr for tr in self.allTraceObjs if ps.addtrace_predicate(tr) ]) for ps in self.plot_specs  ])
        #print ps_to_traces
        if self.linkage:
            self.linkage.process(ps_to_traces)

        
        nTimeRanges = len(self.timeranges)
        nPlots = len(self.plot_specs)
        
        
        #time_axis = None
        
        for i, plot_spec in enumerate( self.plot_specs ):
            
            print 'Plotting For PlotSpec:', plot_spec
            
            for iT, timeRange in enumerate(self.timeranges):
                
                
                timeRange = resolveTimeRange(timeRange) 
                
                # Create the axis:
                #if not time_axis:
                ax = self.fig.add_subplot(nPlots, nTimeRanges, i*nTimeRanges + iT  + 1 )
                
                
                # Leave the plotting to the PlotSpecification
                plot_spec.plot( ax=ax, all_traces=self.allTraceObjs, all_eventsets=self.allEventSetObjs, time_range=timeRange, linkage=self.linkage )
                
                # Save the Axis:
                self.subaxes.append(ax)
                
        
        if self.post_ax_functors:
            for ax in self.subaxes:
                for func in self.post_ax_functors:
                    func(ax)
    
    
        
