from nipype import Workflow, IdentityInterface, Node, Merge, MapNode, Function
from nipype.interfaces.fsl import Split as FslSplit

def get_dwi_target():
    """ create a nipype workflow to get dwi target 

    Parameters
    ----------
    
    Returns
    -------

    nipype workflow

    """

    def _get_target(in_files):
        """ DWI with highest FA is Target """
        return in_files[0]


    inputnode = Node(IdentityInterface(fields=['in_file']), name='inputnode')
    
    split_dwi = Node(FslSplit(dimension='t'), name="split_dwi")
    
    get_target = Node(Function(input_names=['in_files'],
                               output_names=['out_file'],
                               function=_get_target),
                      name='get_target')
    
    outputnode = Node(IdentityInterface(fields=['dwi_target']), name='outputnode')

    wf = Workflow(name="dwi_target")
    wf.connect([(inputnode, split_dwi, [('in_file', 'in_file')]),
                (split_dwi, get_target, [('out_files', 'in_files')]),
                (get_target, outputnode, [('out_file', 'dwi_target')]),

               ])

    return wf
    
def get_mwf_target():
    """ create a nipype workflow to get mwf target= spgrfa18 

    Parameters
    ----------
    
    Returns
    -------

    nipype workflow

    """

    def _get_target(in_files):
        """ spgr with highest kontrast is Target """
        return in_files[-1]


    inputnode = Node(IdentityInterface(fields=['in_file']), name='inputnode')
    
    split_spgr = Node(FslSplit(dimension='t'), name="split_spgr")
    
    get_target = Node(Function(input_names=['in_files'],
                               output_names=['out_file'],
                               function=_get_target),
                      name='get_target')
    
    outputnode = Node(IdentityInterface(fields=['spgr_target']), name='outputnode')

    wf = Workflow(name="spgr_target")
    wf.connect([(inputnode, split_spgr, [('in_file', 'in_file')]),
                (split_spgr, get_target, [('out_files', 'in_files')]),
                (get_target, outputnode, [('out_file', 'spgr_target')]),

               ])   
    return wf            