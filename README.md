# 2020_s_fm_7zip-bzip2
This repository contains scripts for experiment automation and experiment results for a 'toy'-scientific paper created during my studies.

## experiments_on_samples.sh
Runs the experiment on all sample data.
This is the main entry point of the experiment automation. Basic information about the system and tools are displayed (versions, system performance specs, ...)

## experiment.sh
Runs the experiment for a specified compression method with a specified
number of repetitions on sample data. Measures, among others, CPU time, maximum
memory usage and compression ratio and saves the results as semi-colon separated
csv-file.

## 7z_lzma_comp.sh
Compresses data with 7-Zip using 7z/LZMA.

## 7z_lzma_decomp.sh
Decompresses data with 7-Zip using 7z/LZMA.

## 7z_bzip2_comp.sh
Compresses data with 7-Zip using tar/bzip.

## 7z_bzip2_decomp.sh
Decompresses data with 7-Zip using tar/bzip.
