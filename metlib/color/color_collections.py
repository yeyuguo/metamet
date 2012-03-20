#!/usr/bin/env python
import numpy as np
from matplotlib import colors

def n_colors_towards_somecolor(basecolor, tocolor, N=5, max_ratio=0.7, use_basecolor_alpha=True):
    """Generate a list of N colors from basecolor to tocolor
    basecolor: starting color
    tocolor: to this color
    N: number of result colors
    max_ratio: 0-1, the degree of tranformation. if max_ratio == 0.0, all colors will be the same as the first color. if max_ratio == 1.0, the last color will be tocolor
    use_basecolor_alpha: use basecolor's alpha as all color's alpha
    """
    w_ratios = np.linspace(0.0, max_ratio, N)
    b_ratios = 1.0 - w_ratios
    converter = colors.ColorConverter()
    bcolor_rgba = np.array(converter.to_rgba(basecolor))
    tocolor_rgba = np.array(converter.to_rgba(tocolor))
    if use_basecolor_alpha:
        tocolor_rgba[-1] = bcolor_rgba[-1]
    res = []
    for i in range(N):
        res.append(tuple(bcolor_rgba*b_ratios[i] + tocolor_rgba*w_ratios[i]))
    return res

def n_colors_towards_white(basecolor, N=5, max_ratio=0.7):
    """Generate a list of N colors from basecolor to white
    basecolor: starting color
    N: number of result colors
    max_ratio: 0-1, the degree of tranformation. if max_ratio == 0.0, all colors will be the same as the first color. if max_ratio == 1.0, the last color will be tocolor
    """
    return n_colors_towards_somecolor(basecolor, 'white', N=N, max_ratio=max_ratio, use_basecolor_alpha=True)

reds = ['red', 'darkred', 'lightcoral', 'crimson', 'lightsalmon']
oranges = ['orange', 'orangered', 'sandybrown', 'goldenrod', 'wheat']
yellows = ['yellow', 'goldenrod', 'khaki', 'darkkhaki', 'moccasin']
greens = ['green', 'darkgreen', 'yellowgreen', 'olive', 'lightgreen', 'lime']
blues = ['blue', 'navy', 'royalblue', 'steelblue', 'skyblue', 'aqua']
grays = ['gray', 'dimgray', 'lightgrey', 'darkslategray', 'slategray', 'black']
greys = grays
whites = ['white', 'mistyrose', 'honeydew', 'antiquewhite', 'beige']
purples = ['purple', 'indigo', 'plum', 'blueviolet', 'mediumpurple']
pinks = ['hotpink', 'mediumvioletred', 'pink', 'magenta', 'lightcoral']
browns = ['sienna', 'saddlebrown', 'burlywood', 'brown', 'chocolate']

seasons1 = []
seasons2 = ['darkgreen', 'red', 'goldenrod', 'blue']
seasons3 = ['lightgreen', 'salmon',  'khaki', 'deepskyblue']

months1 = []
months2 = []
for c in seasons2:
    months2.extend(n_colors_towards_white(c, 3, max_ratio=0.6))
months3 = []
for c in seasons3:
    months3.extend(n_colors_towards_somecolor(c, 'black', 3, max_ratio=0.5))

crayon = ['#EE204D', '#FFAACC', '#926EAE', '#1F75FE', '#1A4876', '#1CAC78', '#9FE2BF', '#BACF6C', '#FCE883', '#E7C697', '#FF7538', '#B4674D', '#EA7E5D', '#CB4154', '#95918C', 'black']
crayon_dark = ['#EE204D', '#926EAE', '#1F75FE', '#1A4876', '#1CAC78', '#BACF6C', '#FF7538', '#B4674D', '#EA7E5D', '#CB4154', '#95918C', '#202020']
crayon_dark_random = ['#1F75FE', '#CB4154', '#1CAC78', '#FF7538', '#926EAE', '#EA7E5D', '#202020', '#1A4876', '#EE204D', '#BACF6C', '#B4674D', '#95918C']

pop_poster = ['#861D2B', '#CA3226', '#E66B1E', '#E9B64B', '#FBD21A', '#BCC03E', '#69A646', '#318266', '#34A883', '#1F6597', '#273F61', '#8B4AA0', '#95879E', '#6E5248']
pop_poster_random = ['#1F6597', '#CA3226', '#69A646', '#E66B1E', '#8B4AA0', '#6E5248', '#34A883', '#273F61', '#861D2B', '#318266', '#E9B64B', '#95879E', '#FBD21A', '#BCC03E']





    

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    def plot_color_list(clist):
        plt.figure()
        cmap = ListedColormap(clist, name='tmp_cmap')
        data = np.arange(len(clist)).reshape((1,len(clist)))
        plt.pcolor(data, cmap=cmap)
        plt.show()
