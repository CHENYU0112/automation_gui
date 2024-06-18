import cv2 as cv
from pygrabber.dshow_graph import FilterGraph
from guiFiles.configmgr import ConfigMgr
import threading as th

class FlirCam:
    '''
    Simple class to access a connected camera, using opencv library, and be able to capture an image or do a live
    stream from that camera
    '''

    def __init__(self):
        '''
        Initialize the camera object
        '''
        graph = FilterGraph()
        try:
            device = graph.get_input_devices().index(ConfigMgr.instr['flirCam'])
        except ValueError as e:
            try:
                print('Flir Camera failed to initialize.')
                device = graph.get_input_devices().index("Integrated Camera")
            except:
                print('Complete failure on initializing camera')
                device = None
        self.vid = cv.VideoCapture(device)

    def get_image(self, fileName='output_img.png', *args, **kwargs):
        '''
        :param fileName: (str) File name for the image to be saved PNG format. Ex. "output_img.png"
        :return: None
        '''
        ret, frame = self.vid.read()
        cv.imwrite(fileName, frame)

    def live_image(self):
        '''
        Creates a small window that shows a live stream of what the camera is capturing. To exit this window press "q"
        :return: None
        '''
        while(True):
            ret, frame = self.vid.read()
            cv.imshow('frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    def close(self, *args, **kwargs):
        '''
        Closes the connection to camera
        :return: None
        '''
        self.vid.release()


if __name__ == '__main__':
    mycam = FlirCam()
    mycam.get_image('test1.png')