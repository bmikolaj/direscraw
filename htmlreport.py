#!/usr/bin/env python
#HTML Report Generator, htmlreport v1.0
#Copyright (c) 2014 by Brian Mikolajczyk, brianm12@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import os.path
import re
import time

def pretty(input_time):
    if float(input_time).is_integer():
        input_time = float(str(input_time) + '.0')
#Pretty time formatting
    #Month time
    if input_time > 2628000:
        month_time = str(input_time / 2628000)
        months = re.split('\.', month_time)[0]
        days = str(float(str('.') + re.split('\.', month_time)[1]) * 30.42)
        hours = str(float(str('.') + re.split('\.', days)[1]) * 24)
        minutes = str(float(str('.') + re.split('\.', hours)[1]) * 60)
        seconds = float(str('.') + re.split('\.', minutes)[1]) * 60
        days = re.split('\.', days)[0]
        hours = re.split('\.', hours)[0]
        minutes = re.split('\.', minutes)[0]
        seconds = format(seconds, '.2f').rstrip('0').rstrip('.')
        if days == '0':
            pretty_time = months + ' months'
            
        elif hours == '0':
            pretty_time = months + ' months, ' + days + ' days'
            
        elif minutes == '0':
            pretty_time = months + ' months, ' + days + ' days, ' + hours +\
                  ' hours'
        
        elif seconds == '0':
            pretty_time = months + ' months, ' + days + ' days, ' + hours +\
                  ' hours, ' + minutes + ' minutes'

        else:
            pretty_time = months + ' months, ' + days + ' days, ' + hours +\
                  ' hours, ' + minutes + ' minutes, ' + seconds + ' seconds'
    #Day time
    elif input_time > 86400:
        day_time = str(input_time / 86400)
        days = re.split('\.', day_time)[0]
        hours = str(float(str('.') + re.split('\.', day_time)[1]) * 24)
        minutes = str(float(str('.') + re.split('\.', hours)[1]) * 60)
        seconds = float(str('.') + re.split('\.', minutes)[1]) * 60
        hours = re.split('\.', hours)[0]
        minutes = re.split('\.', minutes)[0]
        seconds = format(seconds, '.2f').rstrip('0').rstrip('.')
        if hours == '0':
            pretty_time = days + ' days'
            
        elif minutes == '0':
            pretty_time = days + ' days, ' + hours +\
                  ' hours'
        
        elif seconds == '0':
            pretty_time = days + ' days, ' + hours +\
                  ' hours, ' + minutes + ' minutes'

        else:
            pretty_time = days + ' days, ' + hours +\
                  ' hours, ' + minutes + ' minutes, ' + seconds + ' seconds'
    #Hour time
    elif input_time > 3600:
        hour_time = str(input_time / 3600)
        hours = re.split('\.', hour_time)[0]
        minutes = str(float(str('.') + re.split('\.', hour_time)[1]) * 60)
        seconds = float(str('.') + re.split('\.', minutes)[1]) * 60
        minutes = re.split('\.', minutes)[0]
        seconds = format(seconds, '.2f').rstrip('0').rstrip('.')
        if minutes == '0':
            pretty_time = hours + ' hours'
        
        elif seconds == '0':
            pretty_time = hours + ' hours, ' + minutes + ' minutes'

        else:
            pretty_time = hours + ' hours, ' + minutes + ' minutes, ' +\
                                                    seconds + ' seconds'
    #Minute time
    elif input_time > 60:
        min_time = str(input_time / 60)
        minutes = re.split('\.', min_time)[0]
        seconds = float(str('.') + re.split('\.', min_time)[1]) * 60
        seconds = format(seconds, '.2f').rstrip('0').rstrip('.')
        if seconds == '0':
            pretty_time = minutes + ' minutes'

        else:
            pretty_time = minutes + ' minutes, ' + seconds + ' seconds'
    
    else:
        seconds = format(input_time, '.2f').rstrip('0').rstrip('.')
        pretty_time = seconds + ' seconds'
    
    return pretty_time

def main(input=None):
    input = os.path.abspath(input)
    file = open(input, 'r')
    lines = file.readlines()
    file.close()
    tfmt = '%Y-%m-%d %H:%M:%S'
##Time summation/average
    timelist = []
    for i, line in enumerate(lines):
        if not line.startswith('/') and not i == 0 and not\
               line.endswith(';\n') and not line.endswith('RunTime\n') and not\
               line.startswith('\n'):
            timelist.append(re.split('%', line)[1].strip())
    ####For Testing###
    timelist = ['2.3 days', '5 s', '42.34 mins', '52 hrs', '96 days']
    ##################
    timelist_num = []
    timelist_unit = []
    for el in timelist:
        timelist_num.append(float(re.split(' ', el)[0].strip()))
        timelist_unit.append(re.split(' ', el)[1].strip())
    
    time_s = []
    for i, _ in enumerate(timelist):
        if timelist_unit[i].startswith('day'):
            time_s.append(timelist_num[i] * 86400)
            
        elif timelist_unit[i].startswith('hr'):
            time_s.append(timelist_num[i] * 3600)
            
        elif timelist_unit[i].startswith('min'):
            time_s.append(timelist_num[i] * 60)
            
        else:
            time_s.append(timelist_num[i])

    total_time = 0
    for i, _ in enumerate(time_s):
        total_time = total_time + time_s[i]
    
    average_time = pretty(total_time / len(time_s))
    total_time = pretty(total_time)
##Errors to list
    errlist = []
    errnums = []
    for i, line in enumerate(lines):
        if not line.startswith('/') and not i == 0 and not\
               line.endswith(';\n') and not line.endswith('RunTime\n') and not\
               line.startswith('\n'):
            errlist.append(re.split('%', line)[0].rsplit(' ', 1)[1] + '%')
            errnums.append(re.split('%', line)[0].rsplit(' ', 1)[1])
    
    total_error = 0
    for i, _ in enumerate(errnums):
        total_error = total_error + float(errnums[i])
    
	average_error = format(total_error / len(errnums),
                    '.2f').rstrip('0').rstrip('.') + '%'

#Build HTML
    with(os.path.join(os.path.split(input)[0], 'ErrorReport.html'), 'w') as\
                                                              htmlfile:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--version', action='version',
                        version='htmlreport v1.0')

    main(**vars(parser.parse_args()))
