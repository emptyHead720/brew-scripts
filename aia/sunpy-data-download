#!/home/snehil/miniforge3/envs/data-work/bin/python

import subprocess as sp
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

def convert_date(date):
    months = {'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07',
              'aug':'08', 'sep':'09', 'oct':'10', 'nov':'11', 'dec':'12'}
    tmp = date.split('-')
    date = tmp[2] + '/' + months[tmp[0]] + '/' + tmp[1]
    return(date)

def download_data(start_date, end_date, instrument, wavelength_arr, no_sampling,
                  sampling_time, download):
    for wavelength in wavelength_arr:
        print("Searching...")

        if not no_sampling:
            if instrument == 'aia':
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.aia,
                                    a.Sample(sampling_time), a.Wavelength(wavelength*u.angstrom))
            else:
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.hmi,
                                    a.Sample(sampling_time), a.Physobs.los_magnetic_field)
        else:
            if instrument == 'aia':
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.aia,
                                    a.Wavelength(wavelength*u.angstrom))
            else:
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.hmi,
                                    a.Physobs.los_magnetic_field)
         
        print(result)
        if not download:
            download_choice = input("Do you want to download the data (y/n): ")
            if download_choice == 'y':
                print("downloading")
                download_data = Fido.fetch(result, path=f'./{wavelength}' + '/{file}')
                print('\n\n\n')

        else:
            print("auto downloading")
            download_data = Fido.fetch(result, path=f'./{wavelength}' + '/{file}')
            print('\n\n\n')


if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', "--no_sampling", action="store_true",
                        help="if sampling is not to be provided")
    parser.add_argument('-i', "--instrument", nargs='?', default='aia', const='aia',
                        help="instrument name to download data from")
    parser.add_argument('-d', '--download', action='store_true',
                        help='to auto download data')
    args = parser.parse_args()

    dates = [
            'dec-30-2023',
            'add_new_date'
            ]

    process = sp.Popen(['fzf'], stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT)    
    date = process.communicate(input='\n'.join(dates).encode())[0].decode().strip()


    if date == 'add_new_date':
        date = input("enter date (mth-dd-yyyy): ")
        with open(__file__, 'r') as file:
            filedata = file.read()
    
        filedata = filedata.replace('\'add_new_date\'', '\'' + date + '\',' +
                                    '\n    \'add_new_date\'')
    
        with open(__file__, 'w') as file:
            file.write(filedata)

    date = convert_date(date)

    start_time = input("enter start time (hh:mm): ")
    end_time = input("enter end time (hh:mm): ")

    start_date = date + ' ' + start_time
    end_date = date + ' ' + end_time

    allowed_wavelengths = ['171 (gold)', '193 (bronze)', '304 (red)', '211 (purple)',
                           '131 (teal)', '335 (blue)', '094 (green)', '1600 (yellow/green)',
                           '1700 (pink)']

    process = sp.Popen(['fzf -m | awk \'{print $1}\''], shell=True, stdout=sp.PIPE,
                    stdin=sp.PIPE, stderr=sp.STDOUT)    
    wavelength = process.communicate(input='\n'.join(allowed_wavelengths).encode())[0].decode()
    wavelength = wavelength.strip().split('\n')
    wavelength = list(map(int, wavelength))

    if not args.no_sampling:
        sampling_time = input("Enter sampling time in minutes or 'default': ")
        if sampling_time == 'default':
            no_sampling = True
        else:
            sampling_time = int(sampling_time) * u.min

    download_data(start_date, end_date, args.instrument, wavelength, args.no_sampling,
                  sampling_time, args.download)
