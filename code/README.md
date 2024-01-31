# Atlas-based quantitative MRI assessment in hypomyelinating Pelizaeus Merzbacher Disease 

### Background: 
Pelizaeus-Merzbacher disease (PMD) is a rare childhood hypomyelinating leukodystrophy. Quantification of the pronounced myelin deficit and delineation of subtle myelination processes will be of clinical interest. Quantitative magnetic resonance imaging (qMRI) techniques can provide in vivo insights into myelination status, its spatial distribution and dynamics during brain maturation. They could be potential biomarkers for assessing the effect of myelin-modulating therapies. However, registration techniques for image quantification and statistical comparison of diseased pediatric brains, such as those with low or deviant image contrast, with healthy controls are scarce.

### Objective: 
This study aimed to develop a post-processing pipeline for atlas-based qMRI image quantification of pediatric PMD and comparison with healthy controls, and to demonstrate its feasibility by evaluating myelin water imaging (MWI) data.

<br/>
Ths repository summarizes the code which have been developed for atlas-based qMRI assessments in hypomyelinating leukodystrophies. Additionaly, the raw and processed imaging files used in this study are provided under the data folder.

<br/>
The jupyter notebook __paper_results.ipynb__ summarizes the main outputs of the study and visualizes also the registration dataset and the structural similarity index method (SSIM) in more detail. 
<br/>
<br/>
The jupyter notebook register_PMD1_to_JHU18m.ipynb shows the registration workflow (step2) for example patient PMD1 in short by also warping the atlas segmentation in the patient space. 
<br/>
<br/>
The jupyter notebook relbl_atlas_to_tract.ipynb shows the original atlas segmentation of the JHU18m template and the relabeld segmentation resulting in four main white matter tracts for the analysis used in this paper.
<br/>
<br/>
1_run_coreg_pmd_fa.py, 1_run_coreg_pmd_T1w.py and 1_run_coreg_pmd_multimodal.py reflect the workflow for the three individual registation workflows including step 1 and 2. 
<br/>
<br/>
2_get_atlas_values.py is code to assess mean values of MWF and other qMRI parameter within main four white matter atlas tracts. To do so the atlas was warped in the patient session space in 1_run_cored_pmd. 
<br/>
<br/>
3_get atlas_values_ssim.py is code to assess mean ssim values within the four white matter tracts of the atlas. 
