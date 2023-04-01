import os
import nrrd
import pydicom
import numpy as np

def loadDicom(filepath):
    images = os.listdir(filepath)

    # load the DICOM files
    files = []
    for fname in images:
        #print("loading: {}".format(fname))
        files.append(pydicom.dcmread(filepath + fname))

    print("file count: {}".format(len(files)))

    # skip files with no SliceLocation (eg scout views)
    slices = []
    skipcount = 0
    for f in files:
        if hasattr(f, 'SliceLocation'):
            slices.append(f)
        else:
            skipcount = skipcount + 1

    print("skipped, no SliceLocation: {}".format(skipcount))

    # ensure they are in the correct order
    slices = sorted(slices, key=lambda s: s.SliceLocation)

    # pixel aspects, assuming all slices are the same
    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    ax_aspect = ps[1]/ps[0]
    sag_aspect = ps[1]/ss
    cor_aspect = ss/ps[0]

    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)
    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d

    # plot 3 orthogonal slices
    # a1 = plt.subplot(2, 2, 1)
    # plt.imshow(img3d[:, :, img_shape[2]//2])
    # a1.set_aspect(ax_aspect)

    # a2 = plt.subplot(2, 2, 2)
    # plt.imshow(img3d[:, img_shape[1]//2, :].T)
    # a2.set_aspect(sag_aspect)

    # a3 = plt.subplot(2, 2, 3)
    # plt.imshow(img3d[img_shape[0]//2, :, :].T)
    # a3.set_aspect(cor_aspect)

    # plt.show()
    #img3d -= 1024
    #img3d*=255/np.max(img3d)
    diff = 954
    img3d[img3d < diff+1] = 0
    img3d[img3d > diff] -= diff
    img3d[img3d > 255] = 255
    #img3d *= 255/2000
    #img3d -= 1024
    #img3d *= 255/1024
    return img3d, img_shape

def loadSaveData(save_path):

    # Write to a NRRD file
    # Read the data back from file
    readdata, header = nrrd.read(save_path)
    segmentnr = 0
    segment_names = []
    segment_values = []
    while 1:
        try:
            segment_names.append(header["Segment" + str(segmentnr) + "_Name"])
            segment_values.append(int(header["Segment" + str(segmentnr) + "_LabelValue"]))
            #print(segment_names[segmentnr]+":",segment_values[segmentnr])
            segmentnr+=1
        except:
            break
    return readdata, segment_names, segment_values