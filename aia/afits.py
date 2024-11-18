#!/home/snehil/miniforge3/envs/data-work/bin/python

import subprocess as sp
from sunpy.net import Fido, attrs as a
import astropy.units as u
import sunpy.map
import sunpy.data.sample
import matplotlib.pyplot as plt
import matplotlib.colors
import argparse
from glob import glob
from astropy.coordinates import SkyCoord
from astropy.visualization import ImageNormalize, SqrtStretch
from copy import deepcopy

def custom_plot(sequence_list, axes=None, resample=None, annotate=True, interval=200,
             plot_function=None, clip_interval=None, **kwargs):
    for ax, sequence in zip(axes, sequence_list):
        if not ax:
            ax = wcsaxes_compat.gca_wcs(sequence.maps[0].wcs)
    fig = axes.ravel()[0].get_figure()
     
    if not plot_function:
        def plot_function(fig, ax, smap):
            return []
    removes = []

    # Normal plot
    def annotate_frame(i):
        for ax, sequence in zip(axes, sequence_list):
            ax.set_title(f"{sequence.name}")
            axes.set_xlabel(axis_labels_from_ctype(sequence[i].coordinate_system[0],
                                                   sequence[i].spatial_units[0]))
            axes.set_ylabel(axis_labels_from_ctype(sequence[i].coordinate_system[1],
                                                   sequence[i].spatial_units[1]))

    ani_data_list = []
    if resample:
        for sequence in sequence_list:
            if sequence.all_maps_same_shape():
                resample = u.Quantity(sequence.maps[0].dimensions) * np.array(resample)
                ani_data_list.append([amap.resample(resample) for amap in sequence.maps])
            else:
                raise ValueError('Maps in mapsequence do not all have the same shape.')
    else:
        for sequence in sequence_list:
            ani_data_list.append(sequence.maps)
    im_list = []
    for ani_data, ax in zip(ani_data_list, axes):
        im_list.append(ani_data[0].plot(axes=ax, **kwargs))

    def updatefig(i, im, annotate, ani_data_list, removes, axes):
        while removes:
            removes.pop(0).remove()

        norm_list = []
        for im, ani_data, ax in zip(im_list, ani_data_list, axes):
            im = ani_data[i].plot(axes=ax, **kwargs)
            im.set_cmap(kwargs.get('cmap', ani_data[i].plot_settings.get('cmap')) or "grey")
            norm_list.append(deepcopy(kwargs.get('norm',
                                            ani_data[i].plot_settings.get('norm'))))
        # fix the below for list thingy
        # if clip_interval is not None:
        #     vmin, vmax = _clip_interval(ani_data[i].data, clip_interval)
        #     if norm is None:
        #         norm = ImageNormalize()
        #     norm.vmin=vmin
        #     norm.vmax=vmax
        # if norm:
        #     _handle_norm(norm, kwargs)
        #     im.set_norm(norm)
        # if wcsaxes_compat.is_wcsaxes(axes):
        #     im.axes.reset_wcs(ani_data[i].wcs)
        #     wcsaxes_compat.default_wcs_grid(axes)
        # else:
        #     bl = ani_data[i]._get_lon_lat(ani_data[i].bottom_left_coord)
        #     tr = ani_data[i]._get_lon_lat(ani_data[i].top_right_coord)
        #     x_range = list(u.Quantity([bl[0], tr[0]]).to(ani_data[i].spatial_units[0]).value)
        #     y_range = list(u.Quantity([bl[1], tr[1]]).to(ani_data[i].spatial_units[1]).value)

        #     im.set_extent(np.concatenate((x_range.value, y_range.value)))   


        # if annotate:
        #     annotate_frame(i)
        # removes += list(plot_function(fig, ax, ani_data[i]))

    ani = matplotlib.animation.FuncAnimation(fig, updatefig,
                                             frames=list(range(0, len(ani_data_list[0]))),
                                             fargs=[im_list, annotate, ani_data_list,
                                                    removes, axes],
                                             interval=interval,
                                             blit=False)

    return ani


def src_plot(sequence, axes=None, resample=None, annotate=True, interval=200,
             plot_function=None, clip_interval=None, **kwargs):
    if not axes:
        axes = wcsaxes_compat.gca_wcs(sequence.maps[0].wcs)
    fig = axes[1][0].get_figure()
     
    if not plot_function:
        def plot_function(fig, ax, smap):
            return []
    removes = []

    # Normal plot
    def annotate_frame(i):
        for axe in axes:
            for ax in axe:
                ax.set_title("this")
                ax.set_xlabel("that")
                ax.set_ylabel("that")

    if resample:
        if sequence.all_maps_same_shape():
            resample = u.Quantity(sequence.maps[0].dimensions) * np.array(resample)
            ani_data = [amap.resample(resample) for amap in sequence.maps]
        else:
            raise ValueError('Maps in mapsequence do not all have the same shape.')
    else:
        ani_data = sequence.maps
    im = [[0] * 3] * 2
    for k in range(2):
        for j in range(3):
            im[k][j] = ani_data[0].plot(axes=axes[k][j], **kwargs)

    def updatefig(i, im, annotate, ani_data, removes):
        while removes:
            removes.pop(0).remove()
        for imm in im:
            for j in imm:
                j.set_array(ani_data[i].data)
                j.set_cmap(kwargs.get('cmap', ani_data[i].plot_settings.get('cmap')) or "grey")
        norm = deepcopy(kwargs.get('norm', ani_data[i].plot_settings.get('norm')))
        if clip_interval is not None:
            vmin, vmax = _clip_interval(ani_data[i].data, clip_interval)
            if norm is None:
                norm = ImageNormalize()
            norm.vmin=vmin
            norm.vmax=vmax
        if norm:
            _handle_norm(norm, kwargs)
            for imm in im:
                for j in imm:
                    j.set_norm(norm)
        for axe in axes:
            for ax in axe:
                if wcsaxes_compat.is_wcsaxes(axes):
                    im.axes.reset_wcs(ani_data[i].wcs)
                    wcsaxes_compat.default_wcs_grid(ax)
        else:
            bl = ani_data[i]._get_lon_lat(ani_data[i].bottom_left_coord)
            tr = ani_data[i]._get_lon_lat(ani_data[i].top_right_coord)
            x_range = list(u.Quantity([bl[0], tr[0]]).to(ani_data[i].spatial_units[0]).value)
            y_range = list(u.Quantity([bl[1], tr[1]]).to(ani_data[i].spatial_units[1]).value)

            for imm in im:
                for j in imm:
                    im.set_extent(np.concatenate((x_range.value, y_range.value)))

        if annotate:
            annotate_frame(i)
        for axe in axes:
            for ax in axe:
                removes += list(plot_function(fig, ax, ani_data[i]))

    ani = matplotlib.animation.FuncAnimation(fig, updatefig,
                                             frames=list(range(0, len(ani_data))),
                                             fargs=[im, annotate, ani_data, removes],
                                             interval=interval,
                                             blit=False)

    return ani


def plot(files, dir_back):
    sequence = sunpy.map.Map(files, sequence=True)

    fig = plt.figure()
    ax = fig.add_subplot(projection=sequence.maps[0])
    # ani = sequence.plot(axes=ax, clip_interval=(1, 99.5)*u.percent) # clip & norm read

    # kw passed to all subplots, passing different read loosely that was impossible and
    # thus see if ever need to pass different, especially when plotting different
    # wavelengths and said you might need to create your own wrapper.

    # fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True,
    #                                subplot_kw={'projection':sequence.maps[0]})

    # print(f'{axes = }\n{ax = }\n{type(axes) = }\n{type(ax) = }\n{ax[0][0] = }\n{type(ax[0][0]) = }')
    # ani = sequence.plot(axes=ax[0][0], clip_interval=(1, 99.5)*u.percent) # , norm=matplotlib.colors.LogNorm()
    ani = sequence.plot(axes=ax, clip_interval=(1, 99.5)*u.percent) # , norm=matplotlib.colors.LogNorm()
    # plt.axis('off')

    # ani = sequence.plot(axes=ax[0][0], clip_interval=(1, 99.5)*u.percent) # , norm=matplotlib.colors.LogNorm()
 

    # map.draw_contours([1,5,10,50,90]*u.percent)
    # plt.colorbar() # need to fix how to have global colorbar and not only on the last

    # plt.ion()
    plt.show(block=False)
    save = input("want to save file?(y/n) : ")
    if save == 'y':
        filename = input("enter file name: ")
        ani.save(f'./{dir_back*"../"}animations/{filename}.mp4')

def sub_select_files(files):
    # have selection work with multi select in one fzf window itself
    # try to not use shell = True
    file1 = sp.run('find . -type f -name "*.fits" |fzf',
                    shell=True, capture_output=True, text=True)

    file2 = sp.run('find . -type f -name "*.fits" |fzf',
                    shell=True, capture_output=True, text=True)

    # file1 = sp.run('readlink -f $(find . -type f -name "*.fits" |fzf)',
    #                 shell=True, capture_output=True, text=True)

    # file2 = sp.run('readlink -f $(find . -type f -name "*.fits" |fzf)',
    #                 shell=True, capture_output=True, text=True)

    # fix the error as readlink is not being used
    if (file1.stderr.split('\n', 1)[0] == 'readlink: missing operand' or
    file2.stderr.split('\n', 1)[0] == 'readlink: missing operand'):
        print('Either start or end file wasn\'t selected')
        import sys; sys.exit(0)

    file1 = file1.stdout.strip()
    file2 = file2.stdout.strip()

    file1_index = files.index(file1)
    file2_index = files.index(file2)

    if file1_index > file2_index:
        # dont use this if multidimensional array or if second element depend on first
        file1_index, file2_index = file2_index, file1_index
        print("order of files chosen was swapped")

    files = files[file1_index:file2_index]

    return(files)


def plot_on_dense(files, dense, dir_back):
    length = len(files)
    if dense == 0:
        if length > 25:
            plot(files[::length//25], dir_back)
        else:
            plot(files, dir_back)

    elif dense == 1:
        if length > 50:
            plot(files[::length//50], dir_back)
        else:
            plot(files, dir_back)

    elif dense == 2:
        if length > 100:
            plot(files[::length//100], dir_back)
        else:
            plot(files, dir_back)
            

def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-p', "--path", nargs='?', default='.', const='.',
                        help="path to files' directory") 
    parser.add_argument('-d', "--dense", action='count', default=0, 
                        help='density of file to be used')
    parser.add_argument('-c', "--choice", action='store_true',
                        help="to choose two files to plot between")
    # parser.add_argument(gcc)
    # parser.add_argument('-t', "--time", action='store_true', help="give two time inputs")
    
    # make -d and -c mutually exclusive

    args = parser.parse_args()
    
    files = glob("./*.fits")
    dir_back = True
    
    if not files:
        process = sp.Popen(['ls | fzf'], shell=True, stdout=sp.PIPE,
                        stdin=sp.PIPE, stderr=sp.STDOUT)    
        wavelength = process.communicate()[0].decode()
        wavelength = wavelength.strip()

        files = glob(f'./{wavelength}/*.fits')
        dir_back = False
    # fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True,
    #                                subplot_kw={'projection':sequence.maps[1]})
    
    # im = sequence[0].plot(axes=ax.ravel()[0])
    # im = sequence[1].plot(axes=tt.ravel()[0])

    # ani = custom_plot(sequence_list=sequence_list, axes=ax.ravel()) # clip & norm read

    # ani.save('./ani.mp4')
    # ani = src_plot(sequence=sequence, axes=axes, clip_interval=(1, 99.5)*u.percent)


    # see if sorting set would be faster # sets are not ordered so useless for this code
    files.sort()
    
    if args.choice:
        files = sub_select_files(files, dir_back)

    if args.dense > 2:
        # print("will take too long")
        plot(files, dir_back)

    else:
        plot_on_dense(files, args.dense, dir_back)


if __name__=="__main__":
    main()
