import os
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


def access_data(download):
    print("Searching...")
    start_date = "2023/12/30"
    end_date = "2023/12/31"
    sampling_time = 15*u.min

    Instrument = 'aia'
    
    if Instrument == 'aia':
        result = Fido.search(a.Time(start_date, end_date), a.Instrument.aia,
                             a.Sample(sampling_time), a.Wavelength(171*u.angstrom))
    else:
        result = Fido.search(a.Time(start_date, end_date), a.Instrument.hmi,
                             a.Sample(sampling_time), a.Physobs.los_magnetic_field)
    
    if download:
        print("Downloading...")
        download = Fido.fetch(result, path='./data/{file}')
    else:
        print(result)

def cropped():
    start_date = "2023/12/31 20:55"
    end_date = "2024/01/01 01:55"
    
    bottom_left_x = -1200
    bottom_left_y = -500
    top_right_x = -700
    top_right_y = 400
    bottom_left = SkyCoord(bottom_left_x*u.arcsec, bottom_left_y*u.arcsec,
                               obstime=start_date, observer="earth",
                               frame="helioprojective")
    top_right = SkyCoord(top_right_x*u.arcsec, top_right_y*u.arcsec,
                             obstime=start_date, observer="earth",
                             frame="helioprojective")
    cutout = a.jsoc.Cutout(bottom_left, top_right=top_right, tracking=True)

    jsoc_email = "pandey.snehil720@gmail.com"
    
    result = Fido.search(a.Time(start_date, end_date), a.Wavelength(171*u.angstrom),
                         a.jsoc.Series.aia_lev1_euv_12s, a.jsoc.Notify(jsoc_email),
                         cutout)

    download = Fido.fetch(result, path='./cropped/{file}')
    # print(result)
    # sub_seq = []
    # top_right_x = -800
    # top_right_y = 400
    # for i in range(len(files)):
    #     roi_bottom_left = SkyCoord(Tx=bottom_left_x*u.arcsec, Ty=bottom_left_y*u.arcsec,
    #                                frame=sequence.maps[i].coordinate_frame)
    #     roi_top_right = SkyCoord(Tx=top_right_x*u.arcsec, Ty=top_right_y*u.arcsec,
    #                              frame=sequence.maps[i].coordinate_frame)
    #     item = sequence.maps[i].submap(roi_bottom_left, top_right=roi_top_right)
    #     sub_seq.append(item)
    # sub_seq = sunpy.map.Map(sub_seq, sequence=True)

    # fig = plt.figure()
    # ax = fig.add_subplot(projection=sub_seq.maps[0])
    # ani = sub_seq.plot(axes=ax, clip_interval=(1, 99.5)*u.percent)
    #                     # norm=ImageNormalize(vmin=0, vmax=5e3, stretch=SqrtStretch()))
    # plt.colorbar()
    # ani.save('./cropped-ani.mp4')
    # plt.show()

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', "--no_sampling", action="store_true",
                        help="if sampling is not to be provided")
    args = parser.parse_args()

    start_date = input("start date-time (yyyy/mm/dd hh:mm)")
    end_date = input("end date-time (yyyy/mm/dd hh:mm)")

    allowed_wavelengths = ['171 (gold)', '193 (bronze)', '304 (red)', '211 (purple)',
                           '131 (teal)', '335 (blue)', '094 (green)', '1600 (yellow/green)',
                           '1700 (pink)']

    wavelength = sp.run('find . -type f -name "*.fits" |fzf',
                    shell=True, capture_output=True, text=True)
    if not args.no_sampling:
        sampling_time = input("Enter sampling time ( #h|m|s )")

    


