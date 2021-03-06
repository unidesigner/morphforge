#! /usr/bin/env python

import time 
tStart = time.time()

import sys
from morphforge.core import LogMgr, mfrandom
from morphforge.simulation.simulationmetadatabundle import SimMetaDataBundle




def main():
    
    bundleFilename = sys.argv[1]
    print "Loading Bundle from ", bundleFilename
    bundle = SimMetaDataBundle.loadFromFile(bundleFilename)
    
    # Load the random number seed
    if bundle.random_seed is not None:
        mfrandom.MFRandom.seed(bundle.random_seed) # = morphforge.core.mfrandom.MFRandom._seed
    
    
    result = bundle.getSimulation().Run(doSpawn=False)
    result.setSimulationTime(tStart, time.time())

    LogMgr.info("Simulation Ran OK. Post Processing:")
    
    bundle.doPostProcessingActions()
    LogMgr.info("Bundle Completed OK")
    
    
    
    
    
try:
    tStart = time.time()    
    main()
    tEnd = time.time()
    print "Simulation Time Elapsed: ", tEnd - tStart
except:
    import traceback
    traceback.print_exc()
    print "Simulation Failled"
    sys.exit(0)



print "Suceeded"
sys.exit(1)
