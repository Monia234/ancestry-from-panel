# Local ancestry analyses used in the TCGA ancestry paper. 

## Usage example

### Local ancestry enrichment by gene. 
##### Download TCGA MC3 mutation calls http://firebrowse.org/api-docs/#!/Analyses
```
python find_local_ancestry_by_gene.py samplelist.txt PIK3CA 3:178864311-178959881
```
##### Input file: samplelist.txt   (prepare a list of local ancestry output file per sample in bed format.)
```
TCGA-D8-A1JP_A.bed
TCGA-D8-A1JP_B.bed
TCGA-E2-A1L9_A.bed
TCGA-E2-A1L9_B.bed
...
```
##### Output file: admixture_blocks.txt 
```
1:721290
1:5879772
1:5902050
1:13354121
1:13703662
1:17554853
1:17559676
...
```
### Genome-wide local ancestry enricment. 

#### Step 1: read in local ancestry breakpoints identified in the cohort.
```
python local_ancestry_count_blocks.py samplelist.txt
```
##### Input file: samplelist.txt   (prepare a list of local ancestry output file per sample in bed format.)
##### Output file: admixture_blocks.txt
#### Step 2: for each region with unique local ancestry across samples in the cohort identified from step 1, generate the zscore relative to the genome.
```
python local_ancestry_enrichment.py admixture_blocks.txt
```
