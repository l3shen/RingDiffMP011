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

        # For now, load up




def main():

    # Here is the main code.
    scanDirectory = "E:\\Exp\\2019-03-28\\scans\\scan5"
    tetraceneData = DataSet('tetracene polycrystalline')
    tetraceneData.loadData(scanDirectory)
    print(tetraceneData.tp)
    print(tetraceneData.scanMetadata['scan number'])


if __name__ == "__main__":
    main()