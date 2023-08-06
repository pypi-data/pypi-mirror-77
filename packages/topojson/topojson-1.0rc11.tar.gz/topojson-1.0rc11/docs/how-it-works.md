---
layout: default
title: How it works
nav_order: 4
---

# How it works

With topojson it is possible to reduce the file size of your geographical data. This is often useful if you are aiming for browser-based visualizations (eg. visualizations in JupyterLab or on the Web).

As explained before we can do so through:

1. Eliminating redundancy through computation of a topology
2. Fixed-precision integer encoding of coordinates and
3. Simplification and quantization of arcs

## Topology computation

While the 2nd and 3rd bullets from above list have a significant impact on the filesize reduction, we will describe here the 1st bullet -the computation of the Topology- since it is basically the core of this library.

The computation of the Topology consists of the following sequence:

1. `extract`:
   - Detection of geometrical type of the object
   - Extraction of linestrings from the object
2. `join`:
   - Quantization of input linestrings if necessary
   - Identifies junctions of shared paths
3. `cut`:
   - Split linestrings given the junctions of shared paths
   - Identifies indexes of linestrings that are duplicates
4. `dedup`:
   - Deduplication of linestrings that contain duplicates
   - Merge contiguous arcs
5. `hashmap`:
   - Resolves bookkeeping results to object arcs.

The names are borrowed from the JavaScript variant of TopoJSON, to establish a certain synergy between the packages, even though the code differs significant (and sometimes even the TopoJSON output).

The addopted approach involves secure bookkeeping on multiple levels in order to succesfully pass all steps.