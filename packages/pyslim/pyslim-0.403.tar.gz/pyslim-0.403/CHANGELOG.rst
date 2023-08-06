***************************
[UPCOMING.X.X] - XXXX-XX-XX
***************************

********************
[0.403] - 2020-08-27
********************

BUGFIX: if a tree had all first generation individuals removed
   (e.g., if it had been simplified) then individuals_alive_at( ) failed.

********************
[0.402] - 2020-08-27
********************


This is a compatibility release, for the tskit 0.3.0 release.

**New features**:

- Provenance handling:
   * added the `.slim_provenances` property to return all SLiM provenance entries
   * added the `slim_provenance_version` and `parse_provenance` methods to tell if
      provenance entries come from SLiM and to parse them

- documentation for recapitation with a nonuniform map by :user:@TeresaPegan

**Bug fixes**:

- fixed differential time offset for tree sequences saved out in early versus late:
   prior to this, mutation_at and nucleotides_at would have been sometimes wrong if the tree sequence
   was saved out during late

- initialises correctly to work with tskit 0.3.0

********************
[0.401] - 2020-03-27
********************

**Bug fixes**:

- checks for the ability to simulate with a discrete recombination map
   in the available version of msprime, and sets the default flat
   recombination map in recapitate appropriately

********************
[0.400] - 2020-03-24
********************

**New features**:

- updated to take and output SLiM file version 0.4, which only differs from 0.3
   in minor aspects of provenance

********************
[0.314] - 2019-10-31
********************

**New features**:

- allows passing in of a recombination map to recapitate (:user:`mufernando`)
- added first_generation_individuals() function
- defined individual ages for WF ages
- added mutation_at() and fixed up nucleotide_at() functions

