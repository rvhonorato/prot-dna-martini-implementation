

# DNA
- All with restraints from Marc
* run1: CG default values
* run2: AA default values
* run3: AA epsilon = 78, 
* run4: CG epsilon = 78, w_desol = 0.0

# RNA
- Variations of parameters with same restraints 
* run1: act-pass - epsilon=78
* run2: act-pass-nodesol - epsilon=78, w_desol = 0.0
* run3: CM
* run4: CM-nodesol

# Pipeline
1. create patch-cg-runX.sh with run specific parameters

2. go to the root folder of the benchmark and run submit-analyze-dna-cg-benchmark.sh run_number
3. proceed to analysis