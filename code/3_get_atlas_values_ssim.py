#! env python3

# -*- coding: utf-8 -*-

__author__ = "Caroline Köhlere"
__email__ = "caroline.koehler@uniklinikum-dresden.de"
__license__ = "BSD 3 Clause"
__version__ = "0.1"


import bids
import os
from tqdm import tqdm
from os.path import join, isfile
from nipype import Workflow
from nipype.interfaces.utility import Split, Merge
from nipype.interfaces.utility import Rename
from nipype.interfaces.io import BIDSDataGrabber, DataSink
#from wmi_nipype_workflows import prepare_mcdespot, run_classic_mcdespot, register_to_mni
from nipype import Node, MapNode, Workflow, IdentityInterface, Function


def run_wf(layout, subjects=None, sessions=None, tmp=None):
    """
    Start the Workflow

    Additionally you may select the `subject` and `session`. If none is
    selected all available will be used.  If set you may additionally set the
    `tmpdir` for the nipype scripts. If not set the `tmp` defaults to  `tmp` in
    `bids.root`.

    Graphs of the workflow will be generated inside the `tmp`-directory:
        - graph_orig
        - graph_colored


    Parameters
    ----------

    layout: BIDSLayout
        layout to use for bids-dataset
    subjects: list of str
        select the subjects to run these workflow (default: None)
    session: list of str
        select the Sessions to use (default:None)
    tmp: str
        choose a dir for tmp
        
    Usage:
    -------
    python3 3_get_atlas_values_ssim.py -s PMD1 
    """
    



    # if no subjects are selected: use all from layout
    if subjects is None:
        subjects = layout.get_subjects()

    # filter all subjects that have T1w and belong to pmd cohort
    subjects = list(
            set(layout.get_subjects(subject=subjects, suffix='T1w', extension='nii.gz')) &
            set(['PMD1', 'PMD2', 'PMD3', 'PMD4', 'PMD5'])
            )

    for subject in tqdm(subjects):
        """ Now go through all subjects """
        
        if sessions == None:
            sessions = layout.get_session(subject=subject)
        if type(sessions) is str:
            sessions = [sessions] 
        # filter sessions with ssim    
        sessions = list(
            set(layout.get_sessions(subject=subject)) &
                set(layout.get_sessions(subject=subject, suffix='ssimmap', extension='nii.gz', scope='derivatives')) & 
                set(sessions)
            
            )
        print('print the sessionS', sessions)   
        # grab input files (jhu atlas)
        jhu18 = Node(IdentityInterface(fields=['in_file']), name='jhu18')
        #jhu18.inputs.in_file= join(layout.root + '/code/templates/JHU_pediatric/18month/JHU_pediatric18_SS_159parcellation_lps.nii.gz')
        jhu18.inputs.in_file= join(layout.root + '/code/templates/JHU_pediatric/18month/dil_ventricle_atlas18m_edCK_desc-relable_atlas.nii.gz')
        
        for session in tqdm(sessions):

            queries = {
                        'ssim_fa': dict(suffix='ssimmap', session=session, extension='nii.gz', desc='fa', scope='derivatives'),
                        'ssim_multimod': dict(suffix='ssimmap', session=session, extension='nii.gz', desc='multimod', scope='derivatives'),
                        'ssim_t1w': dict(suffix='ssimmap', session=session, extension='nii.gz', desc='t1w', scope='derivatives'),

                        }

            in_files = {}
            inputnode = Node(IdentityInterface(list(queries.keys())), name='inputnode')
            for key in queries.keys():
                in_files[key] = layout.get(**queries[key], return_type='file', subject=subject, invalid_filters='allow')
                inputnode.set_input(key, in_files[key])
                #squeeze= remove list 
            print('found files for inputnode.inputs:' ,inputnode.inputs)
            
            ssim_fa_squeezer = Node(Split(splits=[1], squeeze=True), name='ssim_fa_squeezer')
            ssim_multimod_squeezer = Node(Split(splits=[1], squeeze=True), name='ssim_multimod_squeezer')
            ssim_t1w_squeezer = Node(Split(splits=[1], squeeze=True), name='ssim_t1w_squeezer')

                
            print(' load files')
            merge_maps = Node(Merge(3), name= 'merge_maps')
            
            ##NODES
            # read out lesion values via function get_roi_means
            from wmi_nipype_workflows.wmi_nipype_workflows.image_statistik import get_roi_means
            roi_means = MapNode(Function(function=get_roi_means, 
                                        input_names=['mapfile', 'roifile'], 
                                        output_names=['output', 'stats_array']),
                                        name='roi_means', iterfield=['mapfile'])
                                        
            split_maps = Node (Split(), name= 'split_maps')
            split_maps.inputs.splits= [1,1,1]
            split_maps.inputs.squeeze= True
                
            #import ipdb
            #ipdb.set_trace()
            # save and rename quantitative values in statistics sink
 
            ssim_sink= Node(DataSink(base_directory=join(layout.root,'derivatives', 'ssim_rlblatlas_sink'),
                                remove_dest_dir=True,
                                parameterization=False),
                        name='ssim_sink')
            ssim_sink.inputs.container=join('sub-'+subject, 'ses-'+session)
            
            # create a dataset_description.json for derivatives 'jhu18m_to_pmd_t1w'
            import time
            import json
            __version__ = "0.2"
            with open(join(layout.root, 'derivatives', 'ssim_rlblatlas_sink', 'dataset_description.json'), 'w') as f:
                f.write(json.dumps({
                            'Name': 'means ssim within tract',
                            'BIDSVersion': '1.4.0',
                            'DatasetType': 'derivative',
                            'GeneratedBy': [{'caroline.koehler@ukdd.de': '3_get_atlas_values_ssim.py'}],
                }))

            with open(join(layout.root, 'derivatives', 'ssim_rlblatlas_sink', 'CHANGELOG'), 'a') as f:
                f.write('\n')
                f.write(time.strftime("%Y-%m-%d:"))
                f.write('\t-Running get mean ssim within tract')
            # update layout otherwise jhu18m_to_pmd_t1w files are not found)
            try:
                layout.add_derivatives(path= join(layout.root, 'derivatives', 'ssim_rlblatlas_sink'))
                print ('writing dataset_description for derivatives ssim_rlblatlas_sink')

            except:
                print('dataset_description exists ')

            rename_ssim_fa = Node(Rename(format_string=("sub-%(subject_id)s_ses-%(session_id)s_space-%(session_id)s_roimean-rlbljhu18m_desc-tractssim_label-fa_means"),
                               keep_ext=True),
                               name='rename_ssim_fa')
            rename_ssim_fa.inputs.subject_id= subject
            rename_ssim_fa.inputs.session_id= session 
                
            rename_ssim_multimod = Node(Rename(format_string=("sub-%(subject_id)s_ses-%(session_id)s_space-%(session_id)s_roimean-rlbljhu18m_desc-tractssim_label-multimod_means"),
                               keep_ext=True),
                               name='rename_ssim_multimod')
            rename_ssim_multimod.inputs.subject_id= subject
            rename_ssim_multimod.inputs.session_id= session
                
            rename_ssim_t1w= Node(Rename(format_string=("sub-%(subject_id)s_ses-%(session_id)s_space-%(session_id)s_roimean-rlbljhu18m_desc-tractssim_label-t1w_means"),
                            keep_ext=True),
                            name='rename_ssim_t1w')
            rename_ssim_t1w.inputs.subject_id= subject
            rename_ssim_t1w.inputs.session_id= session
                
                   
                
            tmp = join(layout.root, 'tmp', f'sub-{subject}', f'ses-{session}')
            wf = Workflow(name='get_values_ssim', base_dir=tmp)
            wf.connect([
                        (inputnode, ssim_fa_squeezer, [('ssim_fa','inlist')]),
                        (inputnode, ssim_multimod_squeezer, [('ssim_multimod','inlist')]),
                        (inputnode, ssim_t1w_squeezer, [('ssim_t1w','inlist')]),

                        
                        (ssim_fa_squeezer, merge_maps, [('out1','in1')]),
                        (ssim_multimod_squeezer, merge_maps,[('out1','in2')]),
                        (ssim_t1w_squeezer, merge_maps,[('out1','in3')]),
                        
                        (merge_maps, roi_means, [('out', 'mapfile')]),
                        (jhu18, roi_means, [('in_file', 'roifile')]),
                        (roi_means, split_maps, [('output', 'inlist')]),
                        
                        (split_maps, rename_ssim_fa, [('out1', 'in_file')]),
                        (rename_ssim_fa, ssim_sink, [('out_file', '@fa')]),
                        
                        (split_maps, rename_ssim_multimod, [('out2', 'in_file')]),
                        (rename_ssim_multimod, ssim_sink, [('out_file', '@multimod')]),
                        
                        (split_maps, rename_ssim_t1w, [('out3', 'in_file')]),
                        (rename_ssim_t1w, ssim_sink, [('out_file', '@t1w')]),

                       ])
                            
            #wf.write_graph(graph2use='orig', dotfilename=join(layout.get, 'tmp', './graph_orig.dot'))
            #wf.write_graph(graph2use='colored', dotfilename=join(layout.get, 'tmp', './graph_colored.dot'))
            wf.run(plugin='MultiProc')
                

   
         
def main():
    """
    main function that is run when started as standalone commandline program
    """

    import argparse
    parser = argparse.ArgumentParser(description='run coreg to session T1w ')
    parser.add_argument('-s' ,'--subject', type=str, nargs='*', default=None, help='subjects to perform registration on, if none is given, all valid will be taken')
    parser.add_argument('-S' ,'--session', type=str, nargs='*', default=None, help='session to perform registration on, if none is given, all valid will be taken')
    parser.add_argument('-p' ,'--path', type=str, default=os.path.dirname(os.getcwd()), help='path to study folder')
    parser.add_argument('-t', '--tmp', type=str, default=None, help='Tempdir, defaults to tmp')

    args = parser.parse_args()
    subjects = args.subject
    session = args.session

    
    indexer=bids.layout.index.BIDSLayoutIndexer(validate=False, ignore=['code','tmp'])
    layout = bids.BIDSLayout(os.path.dirname(os.getcwd()), derivatives=True, validate=False, indexer=indexer)
    print(layout.get_subjects())
    run_wf(layout, subjects, session, tmp=args.tmp)



if __name__ == '__main__':
    main()
