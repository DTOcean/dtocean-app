# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 11:21:12 2017

@author: Work
"""

import Tkinter as tk

def is_high_dpi(dpi_freshold=100.):
    
    root = tk.Tk()
    
    width_px = root.winfo_screenwidth()
    height_px = root.winfo_screenheight()
    width_mm = root.winfo_screenmmwidth()
    height_mm = root.winfo_screenmmheight()
    # 2.54 cm = in
    width_in = width_mm / 25.4
    height_in = height_mm / 25.4
    width_dpi = width_px/width_in
    height_dpi = height_px/height_in
    
    if (width_dpi + height_dpi) / 2. > dpi_freshold: return True
        
    return False
