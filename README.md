# hypomyelinating leukodystrophies


## Description
The repository stores the datasets and code used for the paper: Atlas-based quantitative MRI assessment in hypomyelinating Pelizaeus Merzbacher disease. 

The repository contains example MRI data of 5 pediatric Pelizaeus-Merzbacher disease (PMD) patients. Example data is organized in BIDS structure (brain imaging data structure, https://bids.neuroimaging.io/). 

The developed pipeline registers the PMD data within the session, than in a pediatric template (JHU18m) space and finally it warps the atlas from the template space back into the individual patient space.   

Because of hypomyelination (profound lack of myelin) the MRI tissue contrast of T1-weighted images can be severey altered hampering registration accuracy. Therefore, 3 registration approaches were developed and compared using nipype.

## Register PMD MRI data
Choose a registration pipeline.   

1. 1_run_coreg_pmd_T1w.py
2. 1_run_coreg_pmd_fa.py
3. 1_run_coreg_pmd_multimodal.py

## evaluate quantitative MRI within pediatric atlas ROIs
read out quantitative MRI metrics  
2_get_atlas_values_mwf.py

## Installation
- Python 
- ANTS registration Package \
You can use the following link to install the ANTS Package.
https://anaconda.org/aramislab/ants \
conda install -c aramislab ants \
You can find more information on ants on the following website: https://stnava.github.io/ANTs/
- install dependencies pybids, nipype... --> requirements.txt 

## Prerequisites
Dataset needs to be in BIDS structure.  \
The dataset must contain the following files\
see also queries
* T1w: T1-weighted image .nii.gz 
* T2w: T2-weighted image .nii.gz 
* spgr: SPGR Flipangle 18 image from mcdespot .nii.gz 
* mwf: Myelin water fraction (MWF) map from mcdespot
* mrt: Myelin water residence time (MRT) map from mcdespot
* qt1: quantitative T1 map from mcdespot
* qt2: quantitative T2 map from mcdespot
* fa: Fractional anisotropy (FA) image from DTI processing
* mt: Magnetisation Transfer image (MT)
* mtr: Magentisation transfer ratio image (MTR)  
* bval: b-value from dwi image
* dwi: diffusion weighted image



## Usage
Download the repository. Install dependencies and ants registration.

will register all avaliable BIDS datasets
python3 1_run_coreg_pmd_fa.py

python3 1_run_coreg_pmd_fa.py –s subject_id –S session_id \
-s : provide a subject_id \
-S : provide a session_id \
-p: path to the projectdir, default patent directory of the code folder \
example: \
python3 1_run_coreg_pmd_fa.py –s V7744 –S 16126 \

After registration run get_atlas_values. \
python3 2_get_atlas_values_mwf.py

## Outputs
Following processed files will be generated from the script in the derivatives folder.
 * coreg_session : contains co-registered files within the session (reference image is T1w image) for every subject\
 * coreg_jhu_fa : contains registered files in tempalte space using FA-based registration \
 * jhu18m_to_pmd_fa : contains atlas mask for every patient in patient space \
 * segment_pmd : contains WM/GM segmentation masks using Fsl FAST \ 
 * statistik : a .tsv file is generated for every subject and session  containing the quantitative metrics for every atlas ROI


## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
This project was developed as part of a grant from the German Leukodystrophie association. The development status of the project has slowed down.
