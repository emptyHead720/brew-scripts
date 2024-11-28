#!/home/snehil/miniforge3/envs/data-work/bin/python

# plots fits files

import subprocess as sp
import astropy.units as u
import sunpy.map
# import sunpy.data.sample
import matplotlib.pyplot as plt
import matplotlib.colors
import argparse
from glob import glob
# from astropy.coordinates import SkyCoord
from astropy.visualization import ImageNormalize, SqrtStretch
import re
from astropy.visualization import AsymmetricPercentileInterval
import numpy as np


class plot_functions:
    vmin = 1
    vmax = 99.5
    def plot_aia(map):
        obj = plot_functions()

        def onkey(event, data):
            if event.key == 'ctrl+j':
                obj.vmin -= 0.1
            if event.key == 'ctrl+k':
                obj.vmin += 0.1
            if event.key == 'ctrl+J':
                obj.vmax -= 0.1
            if event.key == 'ctrl+K':
                obj.vmax += 0.1
            clip_percentages = ((obj.vmin, obj.vmax)*u.percent).to('%').value
            vmin, vmax = AsymmetricPercentileInterval(*clip_percentages).get_limits(data)
            im.set_clim(vmin, vmax)
            text_vmin.set_text(f'{vmin = :.2f}\nvmin%={obj.vmin:.2f}%')
            text_vmax.set_text(f'{vmax = :.2f}\nvmax%={obj.vmax:.2f}%')
            fig.canvas.draw()


        fig, axes = plt.subplots(constrained_layout=False,
                                 subplot_kw={'projection':map})
        im = map.plot(axes=axes, clip_interval=(obj.vmin, obj.vmax)*u.percent)
        clip_percentages = ((obj.vmin, obj.vmax)*u.percent).to('%').value
        data = map.data
        vmin, vmax = AsymmetricPercentileInterval(*clip_percentages).get_limits(data)
        plt.colorbar()
        np.set_printoptions(legacy='1.25')
        text_vmin = plt.figtext(0.1, 0.1, f'{vmin = :.2f}\nvmin%={obj.vmin:.2f}%',
                                horizontalalignment='center', wrap=True, 
                                bbox={ 'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})
        text_vmax = plt.figtext(0.1, 0.4, f'{vmax = :.2f}\nvmax%={obj.vmax:.2f}%',
                                horizontalalignment='center', wrap=True, 
                                bbox={ 'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})
        key_press = fig.canvas.mpl_connect('key_press_event', lambda event: onkey(event,
                                                                                  data))
        plt.show()


    def plot_hmi(map):
        fig, axes = plt.subplots(nrows=1, ncols=1, constrained_layout=True,
                                 subplot_kw={'projection':map})
        value = 1500
        map.plot(axes=axes, norm=plt.Normalize(-value, value), cmap='hmimag')
        plt.colorbar()
        plt.show()
    

def get_file():
    output = sp.run('find . -type f -name "*.fits" |fzf',
                    shell=True, capture_output=True, text=True)

    if output.stderr.split('\n', 1)[0] == 'readlink: missing operand':
        print('No file selected')
        # print(output.stderr)
        import sys; sys.exit(0)

    file = output.stdout.strip()
    return file


def get_plot_func(file):
    filename = file.split('/')[-1].lower()
    if 'aia' in filename:
        return "plot_aia"
    elif 'hmi' in filename:
        return "plot_hmi"
        

def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    # parser.add_argument('-p', "--path", nargs='?', default='./*.fits', const='./*.fits',
    #                     help="path to file") 
    parser.add_argument('-p', "--path", nargs = '?', const = "", help="path to file")
    parser.add_argument('-m', '--multi_plot', action='store_true')
    args = parser.parse_args()
    
    # files = glob(f"{args.path}")

    if not args.multi_plot:
        if not args.path:
            file = get_file()
        else:
            file = args.path
        map = sunpy.map.Map(file)
        plot_func_name = get_plot_func(file)
        plot_func = getattr(plot_functions, plot_func_name)
        plot_func(map)

    # if not args.path:
    #     if args.multi_plot:
    #         print("Not setup yet")
    #         import sys; sys.exit(0)
            
    #         process = sp.Popen(['ls .. | fzf -m '], shell=True, stdout=sp.PIPE,
    #                             stderr=sp.STDOUT)    
    #         wavelengths = process.communicate()[0].decode()
    #         wavelengths = wavelengths.strip().split('\n')
    #         path = output.stdout.strip().split('/')
    #         files = [f"{'/'.join(path[:-2])}/{wavelength}/{re.sub(r'\.[\d]+A',
    #                  f'.{wavelength}A', path[-1])}" for wavelength in wavelengths]

    #         maps = sunpy.map.Map(files)
    #         fig, axes = plt.subplots(nrows=2, ncols=4, constrained_layout=True,
    #                                        subplot_kw={'projection':map,'projection':map })
    #         for ax, map in zip(axes.ravel(), maps):
    #             map.plot(axes=ax, clip_interval=(1, 99.5)*u.percent)

    #         plt.axis('off')


    # map.draw_contours([1,5,10,50,90]*u.percent)
    # plt.colorbar() # need to fix how to have global colorbar and not only on the last


if __name__=="__main__":
    main()
