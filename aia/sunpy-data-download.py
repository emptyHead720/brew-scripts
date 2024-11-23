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


def download_data(start_date, end_date, instrument, iterable_arr, no_sampling,
                  sampling_time, auto_download):
    for iterable in iterable_arr:
        print("Searching...")
        if not no_sampling:
            if instrument == 'aia':
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.aia,
                                    a.Sample(sampling_time),
                                     a.Wavelength(iterable*u.angstrom), a.Resolution(1))
            elif instrument == 'hmi':
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.hmi,
                                     a.Sample(sampling_time),
                                     getattr(a.Physobs, iterable), a.Resolution(1))
        else:
            if instrument == 'aia':
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.aia,
                                    a.Wavelength(iterable*u.angstrom), a.Resolution(1))
            elif instrument == 'hmi':
                result = Fido.search(a.Time(start_date, end_date), a.Instrument.hmi,
                                    getattr(a.Physobs, iterable), a.Resolution(1))
         
        print(result)
        if not auto_download:
            download_choice = input("Do you want to download the data (y/n): ")
            if download_choice == 'y':
                print("downloading")
                download_data = Fido.fetch(result, path=f'./{iterable}' + '/{file}')
                print('\n\n\n')

        else:
            print("auto downloading")
            download_data = Fido.fetch(result, path=f'./{iterable}' + '/{file}')
            print('\n\n\n')


def get_date(date):
    def convert_date(date):
        months = {'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07',
                  'aug':'08', 'sep':'09', 'oct':'10', 'nov':'11', 'dec':'12'}
        tmp = date.split('-')
        date = tmp[2] + '/' + months[tmp[0]] + '/' + tmp[1]
        return(date)


    def write_date(date):
        with open(__file__, 'r') as file:
            filedata = file.read()

        filedata = filedata.replace('\'add_new_date\'\n            ]', '\'' + date + '\',' +
                                    '\n            \'add_new_date\'\n            ]')

        with open(__file__, 'w') as file:
            file.write(filedata)


    dates = [
            'dec-30-2023',
            'add_new_date'
            ]

    if not date:
        process = sp.Popen(['fzf'], stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT)    
        date = process.communicate(input='\n'.join(dates).encode())[0].decode().strip()
        if date == 'add_new_date':
            date = input("enter date (mth-dd-yyyy): ")
            write_date(date)
    else:
        if date not in dates:
            write_date(date)

    date = convert_date(date)
    return date


def get_time_range(tr):
    if not tr:
        start_time = input("enter start time (hhmm): ")
        end_time = input("enter end time (hhmm): ")
    else:
        start_time = tr[:4]
        end_time = tr[-4:]
        
    start_time = start_time[:2] + ':' + start_time[2:]
    end_time = end_time[:2] + ':' + end_time[2:]
    return start_time, end_time


def get_instrument_iterable(instrument):
    allowed_wavelengths = ['171 (gold)', '193 (bronze)', '304 (red)', '211 (purple)',
                           '131 (teal)', '335 (blue)', '094 (green)', '1600 (yellow/green)',
                           '1700 (pink)']
    
    hmi_phy_obs = ['hmi los_magnetic_field', 'him los_velocity', 'hmi intensity']

    if instrument == 'aia':
        process = sp.Popen(['fzf -m | awk \'{print $1}\''], shell=True, stdout=sp.PIPE,
                           stdin=sp.PIPE, stderr=sp.STDOUT)    
        wavelength = process.communicate(input='\n'.join(allowed_wavelengths).encode())[0].decode()
        wavelength = wavelength.strip().split('\n')
        wavelength = list(map(int, wavelength))
        iterable = wavelength

    elif instrument == 'hmi':
        process = sp.Popen(['fzf -m | awk \'{print $2}\''], shell=True, stdout=sp.PIPE,
                           stdin=sp.PIPE, stderr=sp.STDOUT)    
        phy_obs = process.communicate(input='\n'.join(hmi_phy_obs).encode())[0].decode()
        phy_obs = phy_obs.strip().split('\n')
        iterable = phy_obs

    return iterable


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', "--sampling", nargs='?', const='',
                        help="sampling time in minutes")
    parser.add_argument('-i', "--instrument", nargs='?', default='aia', const='aia',
                        help="instrument name to download data from")
    parser.add_argument('-ad', '--auto_download', action='store_true',
                        help='to auto download data')
    parser.add_argument('-d', '--date', nargs='?', const='',
                        help='date of observation (mth-dd-yyyy)')
    parser.add_argument('-tr', '--time-range', nargs='?', const='',
                        help='time range (hhmm-hhmm)')
    args = parser.parse_args()


    date = get_date(args.date)
    start_time, end_time = get_time_range(args.time_range)

    start_date = date + ' ' + start_time
    end_date = date + ' ' + end_time

    iterable = get_instrument_iterable(args.instrument)

    if not args.sampling:
        sampling_time = input("Enter sampling time in minutes or 'default': ")
        if sampling_time == 'default':
            no_sampling = True
        else:
            sampling_time = int(sampling_time) * u.min

    else:
        sampling_time = args.sampling

    download_data(start_date, end_date, args.instrument, iterable, args.sampling,
                  sampling_time, args.auto_download)


if __name__=="__main__":
    main()
