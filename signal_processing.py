import numpy as np
from scipy import signal


class Signal_processing():
    def __init__(self):
        self.a = 1
        
    def extract_color(self, ROIs):
        '''
        从ROIS中提取绿色平均值
        '''
        output_val = np.mean(ROIs)
        return output_val


