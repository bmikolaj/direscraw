#!/usr/bin/env python
#Error and Runtime HTML Report Generator, htmlrepgen v1.0
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
import numpy
import os.path
import plotly.plotly as plotly
from plotly.graph_objs import *
import re
import time

def pretty(input_time):
    if float(input_time).is_integer() and not re.search('\.',
                                                        str(input_time)):
        input_time = float(str(input_time) + '.0')
    else:
        input_time = float(input_time)

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
        if not seconds == '0':
            seconds = format(seconds, '.2f').rstrip('0').rstrip('.')

        if days == '0':
            pretty_time = str(months) + ' months'
            
        elif hours == '0':
            pretty_time = str(months) + ' months, ' + str(days) + ' days'
            
        elif minutes == '0':
            pretty_time = str(months) + ' months, ' + str(days) + ' days, ' +\
                          str(hours) + ' hours'
        
        elif seconds == '0':
            pretty_time = str(months) + ' months, ' + str(days) + ' days, ' +\
                          str(hours) + ' hours, ' + str(minutes) + ' minutes'

        else:
            pretty_time = str(months) + ' months, ' + str(days) + ' days, ' +\
                          str(hours) + ' hours, ' + str(minutes) +\
                          ' minutes, ' + str(seconds) + ' seconds'
    #Day time
    elif input_time > 86400:
        day_time = str(input_time / 86400)
        days = re.split('\.', day_time)[0]
        hours = str(float(str('.') + re.split('\.', day_time)[1]) * 24)
        minutes = str(float(str('.') + re.split('\.', hours)[1]) * 60)
        seconds = float(str('.') + re.split('\.', minutes)[1]) * 60
        hours = re.split('\.', hours)[0]
        minutes = re.split('\.', minutes)[0]
        if not seconds == '0':
            seconds = format(seconds, '.2f').rstrip('0').rstrip('.')

        if hours == '0':
            pretty_time = str(days) + ' days'
            
        elif minutes == '0':
            pretty_time = str(days) + ' days, ' + str(hours) +\
                          ' hours'
        
        elif seconds == '0':
            pretty_time = str(days) + ' days, ' + str(hours) +\
                          ' hours, ' + str(minutes) + ' minutes'

        else:
            pretty_time = str(days) + ' days, ' + str(hours) +\
                          ' hours, ' + str(minutes) + ' minutes, ' +\
                          str(seconds) + ' seconds'
    #Hour time
    elif input_time > 3600:
        hour_time = str(input_time / 3600)
        hours = re.split('\.', hour_time)[0]
        minutes = str(float(str('.') + re.split('\.', hour_time)[1]) * 60)
        seconds = float(str('.') + re.split('\.', minutes)[1]) * 60
        minutes = re.split('\.', minutes)[0]
        if not seconds == '0':
            seconds = format(seconds, '.2f').rstrip('0').rstrip('.')

        if minutes == '0':
            pretty_time = str(hours) + ' hours'
        
        elif seconds == '0':
            pretty_time = str(hours) + ' hours, ' + str(minutes) + ' minutes'

        else:
            pretty_time = str(hours) + ' hours, ' + str(minutes) +\
                          ' minutes, ' + str(seconds) + ' seconds'
    #Minute time
    elif input_time > 60:
        min_time = str(input_time / 60)
        minutes = re.split('\.', min_time)[0]
        seconds = float(str('.') + re.split('\.', min_time)[1]) * 60
        if not seconds == '0':
            seconds = format(seconds, '.2f').rstrip('0').rstrip('.')

        if seconds == '0':
            pretty_time = str(minutes) + ' minutes'

        else:
            pretty_time = str(minutes) + ' minutes, ' + str(seconds) +\
                          ' seconds'
    
    else:
        seconds = format(input_time, '.2f').rstrip('0').rstrip('.')
        pretty_time = str(seconds) + ' seconds'
    
    return pretty_time

def main(input=None, full=False):
    input = os.path.abspath(input)
    output_dir = os.path.split(input)[0]
    output_images = os.path.join(output_dir, 'html_report_images')
    try:
        os.makedirs(output_images)
    except OSError:
        pass
    
    file = open(input, 'r')
    lines = file.readlines()
    file.close()
    tfmt = '%Y-%m-%d %H:%M:%S'
    timelist = []
    errlist = []
    errnums = []
    for i, line in enumerate(lines):
        if not i == 0 and not line.startswith('/') and not\
               line.endswith(';\n') and not line.endswith('RunTime\n') and not\
               line.startswith('\n'):
            timelist.append(re.split('%', line)[1].strip())
            errlist.append(re.split('%', line)[0].rsplit(' ', 1)[1] + '%')
            errnums.append(re.split('%', line)[0].rsplit(' ', 1)[1])
##Time summation/average
    ####For Testing###
    timelist = ['2.3 days', '5 s', '42.34 mins', '52 hrs', '96 days']
    ##################
    timelist_num = []
    timelist_unit = []
    for el in timelist:
        timelist_num.append(float(re.split(' ', el)[0].strip()))
        timelist_unit.append(re.split(' ', el)[1].strip())
    #Time normalized to seconds
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
    time_h = []
    for i, _ in enumerate(time_s):
        total_time = total_time + time_s[i]
    #Time normalized to hours
        time_h.append(format(time_s[i] / 3600, '.2f').rstrip('0').rstrip('.'))
    
    average_time = pretty(numpy.mean(time_s))
    total_time = pretty(total_time)
##Number of files
    n_files = len(timelist)
    for line in lines:
        if re.search('Files Skipped', line):
            n_skip = int(re.split(':', line)[1].strip().replace(';',''))
##Number of directories
    n_dir = 0 - n_skip
    for line in lines:
        if line.startswith('/'):
            n_dir += 1
##Average Errors
    total_error = 0
    for i, _ in enumerate(errnums):
        total_error += float(errnums[i])
    
	average_error = format(numpy.mean(total_error),
                    '.2f').rstrip('0').rstrip('.') + '%'
##Charts
#List of usables#
#
#total_time - pretty Total Time
#average_time - pretty Average Time
#time_s - List of time normalized to seconds
#time_h - List of time normalized to hours
#
#errlist - List of errors with %
#errnums - List of errors sans %
#average_error - Average Error
#
#n_files - File count
#n_dir - Directory Count
#n_skip - Skipped Count

    n_val = 1000
#Error Distribution
    errnums = numpy.random.randint(0,100,n_val)
    x = errnums
    err_dist = Histogram(
        x=x,
        histnorm='count',
        autobinx=False,
        xbins=XBins(start=0, end=100, size=1),
        marker=Marker(color='red')
    )
    layout = Layout(
        title='Error Percent Distribution',
        xaxis=XAxis(title='Error (%)'),
        yaxis=YAxis(title='Count'),
    )
    fig = Figure(data=Data([err_dist]), layout=layout)
    plotly.image.save_as(fig, os.path.join(output_images, 'err_dist.png'))
#Time Distribution
    time_h = numpy.random.randint(0,750,n_val)
    min_time = numpy.amin(time_h)
    max_time = numpy.amax(time_h)
    time_diff = (max_time - min_time) / 10
    print(time_diff)
    x = time_h
    time_dist = Histogram(
        x=x,
        histnorm='count',
        autobinx=False,
        xbins=XBins(start=min_time, end=max_time, size=time_diff),
        marker=Marker(color='green')
    )
    layout = Layout(
        title='RunTime Distribution',
        xaxis=XAxis(title='Duration (hours)'),
        yaxis=YAxis(title='Count'),
    )
    fig = Figure(data=Data([time_dist]), layout=layout)
    plotly.image.save_as(fig, os.path.join(output_images, 'time_dist.png'))
#Error Box Chart
    y = errnums
    q1_err = format(numpy.percentile(errnums, 25), '.2f')
    q2_err = format(numpy.percentile(errnums, 50), '.2f')
    q3_err = format(numpy.percentile(errnums, 75), '.2f')
    min_err = format(numpy.amin(errnums), '.2f')
    max_err = format(numpy.amax(errnums), '.2f')
    err_box = Box(
        y=y,
        name='Error Percent',
        boxmean=True,
        marker=Marker(color='red'),
        boxpoints='outliers',
        jitter=0.5
    )
    layout = Layout(
        title='Error Percent BoxPlot',
        yaxis=YAxis(title='Error (%)'),
        boxgap=0.65,
        height=500,
        width=500,
	annotations=Annotations([
            Annotation(
                x=0.25,
                y=min_err,
                text=str(min_err) + '%',
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=q1_err,
                text=str(q1_err) + '%',
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=q2_err,
                text=str(q2_err) + '%',
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=q3_err,
                text=str(q3_err) + '%',
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=max_err,
                text=str(max_err) + '%',
                showarrow=False
            )
        ])
    )
    fig = Figure(data=Data([err_box]), layout=layout)
    plotly.image.save_as(fig, os.path.join(output_images, 'err_box.png'))
#Time Box Chart
    y = time_h
    q1_time = format(numpy.percentile(time_h, 25), '.1f')
    q2_time = format(numpy.percentile(time_h, 50), '.1f')
    q3_time = format(numpy.percentile(time_h, 75), '.1f')
    #Already calculated above
    min_time = format(min_time, '.1f')
    max_time = format(max_time, '.1f')
    time_box = Box(
        y=y,
        name='RunTime',
        boxmean=True,
        marker=Marker(color='green'),
        boxpoints='outliers',
        jitter=0.5
    )
    layout = Layout(
        title='RunTime BoxPlot',
        yaxis=YAxis(title='Duration (hours)'),
        boxgap=0.65,
        height=500,
        width=500,
	annotations=Annotations([
            Annotation(
                x=0.25,
                y=min_time,
                text=str(min_time),
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=q1_time,
                text=str(q1_time),
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=q2_time,
                text=str(q2_time),
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=q3_time,
                text=str(q3_time),
                showarrow=False
            ),
            Annotation(
                x=0.25,
                y=max_time,
                text=str(max_time),
                showarrow=False
            )
        ])
    )
    fig = Figure(data=Data([time_box]), layout=layout)
    plotly.image.save_as(fig, os.path.join(output_images, 'time_box.png'))
    
    ##Write HTML
    q1_time = pretty(numpy.percentile(time_s, 25))
    q3_time = pretty(numpy.percentile(time_s, 75))
    min_time = pretty(numpy.amin(time_s))
    max_time = pretty(numpy.amax(time_s))

    output = 'direscraw_HTMLReport.html' if full else 'HTMLReport.html'

    #with open(os.path.join(output_dir, output), 'w') as htmlfile:
    #if nskip == 0:


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--version', action='version',
                        version='htmlrepgen v1.0')
    parser.add_argument('-f', '--full', action='store_true')

    main(**vars(parser.parse_args()))
