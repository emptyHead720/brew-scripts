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

def access_data(start_date, end_date, instrument, wavelength, no_sampling, sampling_time ):
    print("Searching...")
    
    if not no_sampling:
        sampling_time = int(sampling_time) * u.min
        if Instrument == 'aia':
            result = Fido.search(a.Time(start_date, end_date), a.Instrument.aia,
                                 a.Sample(sampling_time), a.Wavelength(wavelength*u.angstrom))
        else:
            result = Fido.search(a.Time(start_date, end_date), a.Instrument.hmi,
                                 a.Sample(sampling_time), a.Physobs.los_magnetic_field)
    else:
        if Instrument == 'aia':
            result = Fido.search(a.Time(start_date, end_date), a.Instrument.aia,
                                 a.Wavelength(wavelength*u.angstrom))
        else:
            result = Fido.search(a.Time(start_date, end_date), a.Instrument.hmi,
                                 a.Physobs.los_magnetic_field)
        
        print(result)

        download = input("Do you want to downlaod the data (y/n): ")
        if download == 'y':
            print("Downloading...")
            download = Fido.fetch(result, path='./data/{file}')


if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', "--no_sampling", action="store_true",
                        help="if sampling is not to be provided")
    args = parser.parse_args()

    dates = [
            'dec-30-2023',
            'add_new_date'
            ]

    process = Popen(['fzf'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
    date = p.communicate(input='\n'.join(dates).encode())[0].decode().strip()


    if write == 'y':
        date = input("enter date (mth-dd-yyyy): ")
        with open(__file__, 'r') as file:
            filedata = file.read()
    
        filedata = filedata.replace('\'add_new_date\'', '\'' + date + '\',' +
                                    '\n    \'add_new_date\'')
    
        with open(__file__, 'w') as file:
            file.write(filedata)

    date = convert(date)

    start_time = input("start time (hh:mm)")
    end_time = input("end time (hh:mm)")

    start_date = date + ' ' + start_time
    end_date = date + ' ' + end_time

    allowed_wavelengths = ['171 (gold)', '193 (bronze)', '304 (red)', '211 (purple)',
                           '131 (teal)', '335 (blue)', '094 (green)', '1600 (yellow/green)',
                           '1700 (pink)']

    process = Popen(['fzf | awk \'{print $1}\''], shell=True, stdout=PIPE,
                    stdin=PIPE, stderr=STDOUT)    
    wavelength = process.communicate(input='\n'.join(allowed_wavelengths).encode())[0].decode()
    wavelength = wavelength.strip()

    if not args.no_sampling:
        sampling_time = input("Enter sampling time in minutes or 'default': ")
        if samplint_time = 'default':
            no_sampling = True

