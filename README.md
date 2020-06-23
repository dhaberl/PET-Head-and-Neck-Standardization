# PET-Head-and-Neck-Standardization
 Standardization of multicentric PET data.

## Info
This repo intends to evaluate the impact of multicentric data on Radiomics studies and is currently in progress.

For now, only preprocessing of the data has been done.  

## Dataset
The dataset is an open dataset from *The Cancer Imaging Archive (TCIA)* and consists of 298 Head and Neck PET/CT scans from four different centers [1] [2].

The dataset can be downloaded from:
 
https://wiki.cancerimagingarchive.net/display/Public/Head-Neck-PET-CT

### Note:
In order to extract the masks (contours) from the Dicom-RT structure file, the dataset provides an Excel-sheet 
with the roi-names (region of interest) of the tumour region. 
The tumour region is defined by the names of the GTV primary and GTV lymph nodes [2].

The masks of the tumour are stored in the Dicom-RT structure file under this name. However, I recognized that some 
names in the Excel-sheet were wrong (typo).

The corrected Excel-sheet 
- INFO_GTVcontours_HN_edit.xlsx

and the original

- INFO_GTVcontours_HN_original.xlsx

can be found in the data folder of this repo.

## Acknowledgement
- [1] [The Cancer Imaging Archive](https://www.cancerimagingarchive.net/)
- [2] Vallières, M. et al. Radiomics strategies for risk assessment of tumour failure in head-and-neck cancer. Sci Rep 7, 10117 (2017). doi: [10.1038/s41598-017-10371-5](https://www.nature.com/articles/s41598-017-10371-5)
