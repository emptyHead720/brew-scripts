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

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-p', "--path", nargs='?', default='./*.fits', const='./*.fits',
                        help="path to file") 
    args = parser.parse_args()
    
    files = glob(f"{args.path}")
     
    output = sp.run('readlink -f $(find . -type f -name "*.fits" |fzf)',
                    shell=True, capture_output=True, text=True)

    if output.stderr.split('\n', 1)[0] == 'readlink: missing operand':
        print('No file selected')
        # print(output.stderr)
        import sys; sys.exit(0)

    file = output.stdout.strip()
    map = sunpy.map.Map(file)

    fig, ax = plt.subplots(nrows=2, ncols=4, constrained_layout=True,
                                   subplot_kw={'projection':map,'projection':map })

    for axe in ax:
        for axes in axe:
            map.plot(axes=axes, clip_interval=(1, 99.5)*u.percent) # , norm=matplotlib.colors.LogNorm()
            plt.axis('off')


    # map.draw_contours([1,5,10,50,90]*u.percent)
    # plt.colorbar() # need to fix how to have global colorbar and not only on the last

    plt.show()
