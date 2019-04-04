# protein-DNA scoring

```/data/old-users/zeynep/Protein-Nucleic-ClustENM/Protein-DNA/Scoring-Alex

For each protein-DNA complex (6 cases), I created a directory with "structures" directory in it. "structures" contains the end models, together with target pdb, named as "target.pdb" with same residue numbering.
I just need the haddock scores and no need for clustering since in Marc's paper the statistics for top 10 best scoring models were given. And I already have i-RMSD, l-RMSD and fnat values.
The only failing case is 1AZP and I think the problem is the quality of restraints (or the docking settings) because DNA structures that I generated seem quite similar to the target.```

* 1A74 - dimer
* 1AZP - dimer
* 1JJ4 - dimer
* 1ZME - dimer

* 1BYA - trimer
* 3CRO - trimer


# protocol

1. chain-segid
2. create pdb.list

dna-rna-allatom-hj-opls-1.3.param/dna-rna-allatom-hj-opls.param