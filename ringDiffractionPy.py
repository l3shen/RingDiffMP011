'''
Ring diffraction analysis tool for MP011
Kamil Krawczyk, 2019
'''

import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import ndimage as ndi
from skimage.restoration import denoise_bilateral, denoise_wavelet
from skimage import feature, filters
import cv2
from skued import diff_register, shift_image, diffread, baseline_dwt, align


class DataSet:

    tp = []
    scanMetadata = {'scan number' : 0,
                    'grand loop number' : 0,
                    'timepoint units' : ''
                    }

    # Temp variable for images; need to resize later and figure out how to deal with grand loops?
    # TODO: Use 4th dimension as grand loop index.
    imagesOn = np.zeros([1,1,1,1])
    imagesOff = np.zeros([1,1,1,1])
    beamBlockMask = np.zeros([1,1])

    def __init__(self, id):
        self.idName = id

    def loadData(self, direc):

        # List all entries in directory.
        cwd = os.listdir(direc)
        images = []
        for file in cwd:
            if file.endswith((".tiff", ".tif")):
                images.append(file)

        # Begin parsing metadata for images.
        # Overall metadata parse.
        for i in range(0, len(images) - 1):

            if images[i] == 'dexp.tiff' or images[i] == 'pscatt.tiff':
                print("Bypassing blank images for metadata search.")

            elif images[i].endswith(("md_.tiff")):

                tempMD = images[i].split("_")

                self.scanMetadata['scan number'] = tempMD[0][-1]
                self.scanMetadata['timepoint units'] = tempMD[4]

                # Load beam block mask data.
                # dataDirec = direc + "\\" + images[i]
                # img = plt.imread(dataDirec)
                # edges = feature.canny(img, sigma=3)
                # fig = plt.figure()
                # plt.imshow(edges)
                # plt.show(block=True)

                del tempMD

        # Parse time point array.
        for i in range(2, len(images) - 3):
        # for file in images:

            # Create temporary array to store split string data.
            tempMD = images[i].split("_")

            # Append time point data if not already existing in array.
            if int(tempMD[3]) not in self.tp:
                self.tp.append(int(tempMD[3]))

            # Check number of grand loops, append to metadata.
            if int(tempMD[2][-1]) > self.scanMetadata['grand loop number']:
                self.scanMetadata['grand loop number'] = int(tempMD[2][-1])

            # Clear array from memory.
            del tempMD

        # TODO: Get this shit to work.
        # Load beam block mask.
        # for i in range(0, len(images) - 1):
        #         #     if images[i].endswith(("md_.tiff")):
        #         #
        #         #         # Select data directory and load.
        #         #         dataDirec = direc + "\\" + images[i]
        #         #         img = plt.imread(dataDirec)
        #         #         imgMedian = np.median(img)
        #         #         sigma = 0.33
        #         #         lowerT = int(max(0, (1.0 - sigma) * imgMedian))
        #         #         upperT = int(min(255, (1.0 + sigma) * imgMedian))
        #         #
        #         #         # Perform Canny edge detection.
        #         #         img = denoise_wavelet(img)
        #         #         img = filters.gaussian(img, sigma=3)
        #         #         edges = cv2.Canny(img, lowerT, upperT)
        #         #
        #         #         fig = plt.figure()
        #         #         plt.imshow(edges)
        #         #         plt.show(block=True)
        #         #         break

        # For now, load up beam block rectangle (general shape) and convert to mask.
        # TODO: Make this a user defined path.
        showMask = True
        beamBlockFileDirec = "C:\\Users\\MP011 User\\PycharmProjects\\RingDiffMP011\\beamBlockMask7.png"
        beamBlock = plt.imread(beamBlockFileDirec)
        # TODO: Figure out why imported PNG forms a 3D array?
        # The below temporary fix seems to work and forms a True/False mask.
        beamBlock = beamBlock[:,:,0] == 0
        print(beamBlock)
        print(beamBlock.shape)
        # np.ma.make_mask(beamBlock)

        if showMask:
            plt.imshow(beamBlock)
            plt.show(block=True)

        # Load in first image as a reference, assuming first two images are the background images.
        # TODO: Add separate folder for storing background substraction images to simplify file IO.
        firstImage = direc + "\\" + images[3]
        print(firstImage)
        ref = diffread(firstImage)
        ref = baseline_dwt(ref, max_iter = 250, level = 1, wavelet = 'sym2', axis = (0, 1))
        mask = np.zeros_like(ref, dtype=np.bool)
        print(mask)
        print(ref.shape)

        # Using a test image.
        print(len(images) - 2)
        testImage = diffread(direc + "\\" + images[158])
        testImage = baseline_dwt(testImage, max_iter = 250, level = 1, wavelet = 'sym2', axis = (0, 1))
        print(testImage.shape)

        # Do the shift thing and check difference.
        shift = diff_register(testImage, reference=ref, mask=beamBlock)
        im = shift_image(testImage, shift)
        plt.imshow(im)
        print(shift)
        plt.show(block=True)
        plt.imshow(testImage - ref, cmap='jet')
        plt.show(block=True)
        plt.imshow(im - ref, cmap='jet')
        plt.show(block=True)

        # Test of Hough circles method on first image.
        # circles = cv2.HoughCircles(cv2.imread(firstImage), cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)






def main():

    # Here is the main code.
    scanDirectory = "E:\\Exp\\2019-03-28\\scans\\scan5"
    tetraceneData = DataSet('tetracene polycrystalline')
    tetraceneData.loadData(scanDirectory)


if __name__ == "__main__":
    main()