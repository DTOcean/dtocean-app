# -*- coding: utf-8 -*-

#    Copyright (C) 2016-2018 Mathew Topper
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import matplotlib.pyplot as plt

from dtocean_app.widgets.display import get_current_figure_size


def test_get_current_figure_size_no_figure():
        
    test = get_current_figure_size()
    
    assert test is None


def test_get_current_figure_size():
        
    plt.figure()
    test = get_current_figure_size()
    plt.close('all')
    
    assert (test == [8., 6.]).all()
