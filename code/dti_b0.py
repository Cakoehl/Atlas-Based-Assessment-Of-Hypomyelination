#! env python
# -*- coding: utf-8 -*-

def b0_average(in_dwi, in_bval, max_b=10.0, out_file=None):
    """
    A function that averages the *b0* volumes from a DWI dataset.
    As current dMRI data are being acquired with all b-values > 0.0,
    the *lowb* volumes are selected by specifying the parameter max_b.
    .. warning:: *b0* should be already registered (head motion artifact should
      be corrected).
    """
    import numpy as np
    import nibabel as nb
    import os.path as op

    if out_file is None:
        fname, ext = op.splitext(op.basename(in_dwi))
        if ext == ".gz":
            fname, ext2 = op.splitext(fname)
            ext = ext2 + ext
        out_file = op.abspath("%s_avg_b0%s" % (fname, ext))

    imgs = np.array(nb.four_to_three(nb.load(in_dwi)))
    bval = np.loadtxt(in_bval)
    index = np.argwhere(bval <= max_b).flatten().tolist()

    b0s = [im.get_fdata().astype(np.float32)
           for im in imgs[index]]
    b0 = np.average(np.array(b0s), axis=0)

    hdr = imgs[0].header.copy()
    hdr.set_data_shape(b0.shape)
    hdr.set_xyzt_units('mm')
    hdr.set_data_dtype(np.float32)
    nb.Nifti1Image(b0, imgs[0].affine, hdr).to_filename(out_file)
    return out_file