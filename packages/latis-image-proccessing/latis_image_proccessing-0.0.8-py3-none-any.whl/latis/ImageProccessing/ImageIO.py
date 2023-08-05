from . import Image
import numpy as np

import pydicom
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000, RLELossless, ImplicitVRLittleEndian



class ImageIO:

    # private
    def ensure_even(self, stream):
        # Very important for some viewers
        if len(stream) % 2:
            return stream + b"\x00"
        return stream

    def loadImage(self, file):
        ds = pydicom.dcmread(file)
        pixel_array = np.uint16(ds.pixel_array)
        cols = ds.Columns
        rows = ds.Rows
        return Image(pixel_array, cols, rows, ds)

    def buildFile(self, image, saveName):
        # TODO : edit height and width elements
        dataset = ImageIO.buildDataSetImplicitVRLittleEndian(image)
        dataset.save_as(saveName)
        return saveName

    def buildDataSetJPEG2000(self, image):
        from io import BytesIO
        from PIL import Image as PImage
        dataset = image.dataset
        pixels = image.pixelData
        frame_data = []
        with BytesIO() as output:
            image = PImage.fromarray(pixels)
            image.save(output, format="JPEG2000")
            frame_data.append(output.getvalue())
        dataset.PixelData = encapsulate(frame_data)
        dataset.file_meta.TransferSyntaxUID = JPEG2000
        dataset.is_implicit_VR = False
        return dataset

    def buildDataSetImplicitVRLittleEndian(self, image):
        dataset = image.dataset
        pixels = image.pixelData
        dataset.PixelData = pixels.tobytes()
        dataset.file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
        dataset.is_implicit_VR = True
        return dataset
