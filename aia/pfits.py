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

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-p', "--path", nargs='?', default='./*.fits', const='./*.fits',
                        help="path to file") 
    parser.add_argument('-m', '--multi_plot', action='store_true')
    args = parser.parse_args()
    
    # files = glob(f"{args.path}")
     
    output = sp.run('readlink -f $(find . -type f -name "*.fits" |fzf)',
                    shell=True, capture_output=True, text=True)

    if output.stderr.split('\n', 1)[0] == 'readlink: missing operand':
        print('No file selected')
        # print(output.stderr)
        import sys; sys.exit(0)


    if not args.multi_plot:
        file = output.stdout.strip()
        map = sunpy.map.Map(file)
        fig, axes = plt.subplots(nrows=1, ncols=1, constrained_layout=True,
                                       subplot_kw={'projection':map})
        map.plot(axes=axes, clip_interval=(1, 99.5)*u.percent) # , norm=matplotlib.colors.LogNorm()

    else:
        print("Not setup yet")
        import sys; sys.exit(0)
        
        process = sp.Popen(['ls .. | fzf -m '], shell=True, stdout=sp.PIPE,
                            stderr=sp.STDOUT)    
        wavelengths = process.communicate()[0].decode()
        wavelengths = wavelengths.strip().split('\n')
        path = output.stdout.strip().split('/')
        files = [f"{'/'.join(path[:-2])}/{wavelength}/{re.sub(r'\.[\d]+A',
                 f'.{wavelength}A', path[-1])}" for wavelength in wavelengths]

        maps = sunpy.map.Map(files)
        fig, axes = plt.subplots(nrows=2, ncols=4, constrained_layout=True,
                                       subplot_kw={'projection':map,'projection':map })
        for ax, map in zip(axes.ravel(), maps):
            map.plot(axes=ax, clip_interval=(1, 99.5)*u.percent) # , norm=matplotlib.colors.LogNorm()

        plt.axis('off')


    # map.draw_contours([1,5,10,50,90]*u.percent)
    # plt.colorbar() # need to fix how to have global colorbar and not only on the last

    plt.show()
