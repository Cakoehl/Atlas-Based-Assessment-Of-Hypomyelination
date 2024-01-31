# hypomyelinating leukodystrophies


## Description
The repository stores the datasets and code used for the paper: Atlas-based quantitative MRI assessment in hypomyelinating Pelizaeus Merzbacher disease. 

The repository contains example MRI data of 5 pediatric Pelizaeus-Merzbacher disease (PMD) patients. Example data is organized in BIDS structure (brain imaging data structure, https://bids.neuroimaging.io/). 

The developed pipeline registers the PMD data within the session, than in a pediatric template (JHU18m) space and finally it warps the atlas from the template space back into the individual patient space.   

Because of hypomyelination (profound lack of myelin) the MRI tissue contrast of T1-weighted images can be severey altered hampering registration accuracy. Therefore, 3 registration approaches were developed and compared.

## Register PMD MRI data within the session and to a pediatric template 
Choose a registration pipeline.   

1. 1_run_coreg_pmd_t1w.ipynb
2. 1_run_coreg_pmd_fa.ipynb
3. 1_run_coreg_pmd_multimodal.ipynb

## Evaluate best registration method for hypomyelinating leukodystrophies using structural similarity index (SSIM maps) 
4. 2_calculate_SSIM.ipybn
5. 3_get_atlas_values_ssim.py
6. 4_ssim_statistic.ipybn

## Installation
- Python 
- FSL6 
- ANTS registration Package \
You can use the following link to install the ANTS Package.
https://anaconda.org/aramislab/ants \
conda install -c aramislab ants \
You can find more information on ants on the following website: https://stnava.github.io/ANTs/
- install dependencies pybids, nipype... --> requirements.txt 

## Prerequisites
To run registration workflows: 
Dataset needs to be in BIDS structure.  \
The dataset must contain the following files\
see also queries
* T1w: T1-weighted image .nii.gz 
* fa: Fractional anisotropy (FA) image from DTI processing
* dwi: diffusion weighted image
* bval: b-value from dwi image

optional inputs:
* T2w: T2-weighted image .nii.gz 
* spgr: SPGR Flipangle 18 image from mcdespot .nii.gz 
* mwf: Myelin water fraction (MWF) map from mcdespot
* mrt: Myelin water residence time (MRT) map from mcdespot
* qt1: quantitative T1 map from mcdespot
* qt2: quantitative T2 map from mcdespot
* mt: Magnetisation Transfer image (MT)
* mtr: Magentisation transfer ratio image (MTR)  


## Usage
Download the repository. Install dependencies and FSL6 and ants registration.

will register all avaliable BIDS datasets
# set path for FSL, and ANTS package in the jupyter notebook
os.environ["FSLDIR"] = "/opt/fsl/"
os.environ['ANTSPATH']='/opt/conda/bin/'

# set a subject-id and a session-id in the jupyter notebook
subject='PMD1'
session='0m'

# set optional input queries if other qMRI data should be registered
'ad': dict(suffix='AD', session=session, extension='nii.gz', scope='derivatives', desc=None),
'rd': dict(suffix='RD', session=session, extension='nii.gz', scope='derivatives', desc=None),
'md': dict(suffix='MD', session=session, extension='nii.gz', scope='derivatives', desc=None),
'spgr': dict(suffix='T1w', session=session, extension='nii.gz', acquisition='SPGR'),
'mwf': dict(suffix='mwfmap', session=session, extension='nii.gz', scope='derivatives'),
'mrt': dict(suffix='mrtmap', session=session, extension='nii.gz', scope='derivatives'),
'qt1': dict(suffix='T1map', session=session, extension='nii.gz', scope='derivatives'),
'qt2': dict(suffix='T2map', session=session, extension='nii.gz', scope='derivatives'),

# set ref_image_matcher providing the registration target as key and the corresponding maps as value or list of values
ref_image_matcher={'b0': ['fa', 'ad','rd',md],
                  'spgr': ['mwf', 'qt1','qt2','mrt']
}

# run the jupyter notebook

## Outputs
Following processed files will be generated from the script in the derivatives folder.
 * coreg_session : contains co-registered files within the session (reference image is T1w image) for every subject\
 * coreg_jhu_fa : contains registered files in tempalte space using FA-based registration \
 * coreg_jhu_t1w : contains registered files in tempalte space using T1w-based registration \
 * coreg_jhu_multimodal : contains registered files in tempalte space using multimodal registration \
 * jhu18m_to_pmd_fa : contains atlas mask for every patient in patient space \



## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.


## Project status
This project was developed as part of a grant from the German Leukodystrophie association. The development status of the project has slowed down.
