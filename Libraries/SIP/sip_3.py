#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" SIP Libraries """
import i18n

import subprocess
import json
import ast
import time
import thread
from calendar import timegm
import sys
import RPi.GPIO as GPIO
sys.path.append('./plugins')

import web  # the Web.py module. See webpy.org (Enables the Python SIP web interface)

import gv
from helpers import (
                     report_station_completed,
                     plugin_adjustment,
                     prog_match,
                     schedule_stations,
                     log_run,
                     stop_onrain,
                     check_rain,
                     jsave,
                     station_names,
                     get_rpi_revision
                     )
from urls import urls  # Provides access to URLs for UI pages
from gpio_pins import set_output
from ReverseProxied import ReverseProxied

# do not call set output until plugins are loaded because it should NOT be called
# if gv.use_gpio_pins is False (which is set in relay board plugin.
# set_output()

""" GPIO setup """
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
global chan_list
# Channel list for setting up all GPIO at the same time
chan_list_BCM = (16, 5, 6, 18, 14, 17, 27, 22, 25) #BCM numbering
chan_list_BOARD = (36, 29, 31, 12, 8, 11, 13, 15) #BOARD numbering

# Set pins as output and input Mechanical Relays (1-8)
for i in range(8):
    GPIO.setup(chan_list_BOARD[i], GPIO.OUT)  # 9 Relays
    # Set trigger to False (Low)
    GPIO.output(chan_list_BOARD[i], True)

#GPIO setup for SSR (Optic relay -> Fan Control)
sid = 8
frequency = 5 #List for testing different frequencies (the lower the frequency, the higher the speed)
dc = (50, 70, 100) #List for testing different duty cycles (the higher the duty cycle, the higher the speed)
GPIO.setup(32, GPIO.OUT)
p = GPIO.PWM(32, frequency)  # GPIO.PWM(channel, frequency (in Hz)

""" SIP variables """
gv.restarted = 1

"""FAN_THREAD FUNCTION (SSR/PWM) """
def fan_speed(sid):
    try:
        time_on = gv.rs[sid][2] #gv.rs[sid][2] is the duration given in the UI (see rd from gv.py)
        while 1:
            p.start(dc[sid-8])
            print "IN SIP_3.PY -> STATION ", sid, " --> ","frequency =", frequency, "// dc =", dc[sid-8]
            time_on = time_on-0.1
            time.sleep(0.1)
            if time_on <= 0.1:
                try:
                    p.ChangeDutyCycle(0)
                    time.sleep(0.1)
                    p.stop()
                    print "p.ChangeDutyCycle(0) EXECUTED"
                    print "p.stop EXECUTED"
                    time.sleep(0.1)
                    break
                except:
                    print ValueError
            print "time_on = ", time_on

    except:
        print "ERROR: FAN COULDN'T START"
        print ValueError
        pass

""" ON/OFF DEVICES - MECHANICAL RELAYS """
def device_on(sid):
    try:
        if sid in range(0,7):
            GPIO.output(chan_list_BOARD[sid], False)
            print "RELAY ", sid, " IS ON"
            time.sleep(0.1)
        elif sid in range(8,11): # FAN_LOW
            try:
                thread.start_new_thread(fan_speed, (sid, ))
            except ValueError as valerr:
                print valerr
                pass
                time.sleep(0.1)
        else:
            print "NO DEVICES WERE TURNED ON"
    except ValueError as valerr:
        print "Problem turning ON station ", sid, "BECAUSE OF", valerr
        time.sleep(0.1)

def device_off(sid):
    try:
        if sid in range(0,7):
            GPIO.output(chan_list_BOARD[sid], True)
            print "RELAY ", sid, "IS OFF"
            time.sleep(0.1)
        else:
            print "NO DEVICES WERE TURNED OFF"
    except ValueError as valerr:
        print "Problem turning OFF station  ---> ", sid, "BECAUSE OF", valerr
        pass
        time.sleep(0.1)


def timing_loop():
    """ ***** Main timing algorithm. Runs in a separate thread.***** """
    try:
        print _('Starting timing loop') + '\n'
    except Exception:
        pass
    last_min = 0
    while True:  # infinite loop
        gv.nowt = time.localtime()   # Current time as time struct.  Updated once per second.
        gv.now = timegm(gv.nowt)   # Current time as timestamp based on local time from the Pi. Updated once per second.
        if gv.sd['en'] and not gv.sd['mm'] and (not gv.sd['bsy'] or not gv.sd['seq']):
            if gv.now / 60 != last_min:  # only check programs once a minute
                last_min = gv.now / 60
                extra_adjustment = plugin_adjustment()
                for i, p in enumerate(gv.pd):  # get both index and prog item
                    # check if program time matches current time, is active, and has a duration
                    if prog_match(p) and p[0] and p[6]:
                        # check each station for boards listed in program up to number of boards in Options
                        for b in range(len(p[7:7 + gv.sd['nbrd']])):
                            for s in range(8):
                                sid = b * 8 + s  # station index
                                if sid + 1 == gv.sd['mas']:
                                    continue  # skip if this is master station
                                if gv.srvals[sid]:  # skip if currently on
                                    continue

            				# station duration condionally scaled by "water level"
                                if gv.sd['iw'][b] & 1 << s:
                                    duration_adj = 1.0
                                    if gv.sd['idd'] == 1:
                                        duration = p[-1][sid]
                                    else:
                                        duration = p[6]
                                else:
                                    duration_adj = (float(gv.sd['wl']) / 100) * extra_adjustment
                                    if gv.sd['idd'] == 1:
                                        duration = p[-1][sid] * duration_adj
                                    else:
                                        duration = p[6] * duration_adj
                                    duration = int(round(duration)) # convert to int
                                if p[7 + b] & 1 << s:  # if this station is scheduled in this program
                                    if gv.sd['seq']:  # sequential mode
                                        gv.rs[sid][2] = duration
                                        gv.rs[sid][3] = i + 1  # store program number for scheduling
                                        gv.ps[sid][0] = i + 1  # store program number for display
                                        gv.ps[sid][1] = duration
                                    else:  # concurrent mode
                                        # If duration is shortter than any already set for this station
                                        if duration < gv.rs[sid][2]:
                                            continue
                                        else:
                                            gv.rs[sid][2] = duration
                                            gv.rs[sid][3] = i + 1  # store program number
                                            gv.ps[sid][0] = i + 1  # store program number for display
                                            gv.ps[sid][1] = duration
                        return duration
                        schedule_stations(p[7:7 + gv.sd['nbrd']])  # turns on gv.sd['bsy']

        if gv.sd['bsy']:
            for b in range(gv.sd['nbrd']):  # Check each station once a second
                for s in range(8):
                    sid = b * 8 + s  # station index
                    if gv.srvals[sid]:  # if this station is on
                        if gv.now >= gv.rs[sid][1]:  # check if time is up
                            gv.srvals[sid] = 0
                            set_output()
                            gv.sbits[b] &= ~(1 << s)
                            device_off(sid)
                            if gv.sd['mas'] - 1 != sid:  # if not master, fill out log
                                gv.ps[sid] = [0, 0]
                                gv.lrun[0] = sid
                                gv.lrun[1] = gv.rs[sid][3]
                                gv.lrun[2] = int(gv.now - gv.rs[sid][0])
                                gv.lrun[3] = gv.now
                                log_run()
                                report_station_completed(sid + 1)
                                gv.pon = None  # Program has ended
                            gv.rs[sid] = [0, 0, 0, 0]
                    else:  # if this station is not yet on
                        if gv.rs[sid][0] <= gv.now < gv.rs[sid][1]:
                            if gv.sd['mas'] - 1 != sid:  # if not master
                                gv.srvals[sid] = 1  # station is turned on
                                set_output()
                                gv.sbits[b] |= 1 << s  # Set display to on
                                gv.ps[sid][0] = gv.rs[sid][3]
                                gv.ps[sid][1] = gv.rs[sid][2]
                                if gv.sd['mas'] and gv.sd['mo'][b] & 1 << (s - (s / 8) * 80):  # Master settings
                                    masid = gv.sd['mas'] - 1  # master index
                                    gv.rs[masid][0] = gv.rs[sid][0] + gv.sd['mton']
                                    gv.rs[masid][1] = gv.rs[sid][1] + gv.sd['mtoff']
                                    gv.rs[masid][3] = gv.rs[sid][3]
                                device_on(sid)
                            elif gv.sd['mas'] == sid + 1:
                                gv.sbits[b] |= 1 << sid
                                gv.srvals[masid] = 1
                                set_output()
                                device_on(sid)

            for s in range(gv.sd['nst']):
                if gv.rs[s][1]:  # if any station is scheduled
                    program_running = True
                    gv.pon = gv.rs[s][3]  # Store number of running program
                    break
                program_running = False
                set_output()
                device_off(sid)
                gv.pon = None

            if program_running:
                if gv.sd['urs'] and gv.sd['rs']:  #  Stop stations if use rain sensor and rain detected.
                    stop_onrain()  # Clear schedule for stations that do not ignore rain.
                for idx in range(len(gv.rs)):  # loop through program schedule (gv.ps)
                    if gv.rs[idx][2] == 0:  # skip stations with no duration
                        continue
                    if gv.srvals[idx]:  # If station is on, decrement time remaining display
                        gv.ps[idx][1] -= 1

            if not program_running:
                gv.srvals = [0] * (gv.sd['nst'])
                device_off(sid)
                set_output()
                gv.sbits = [0] * (gv.sd['nbrd'] + 1)
                gv.ps = []
                for i in range(gv.sd['nst']):
                    gv.ps.append([0, 0])
                gv.rs = []
                for i in range(gv.sd['nst']):
                    gv.rs.append([0, 0, 0, 0])
                gv.sd['bsy'] = 0

            if (gv.sd['mas'] #  master is defined
                and (gv.sd['mm'] or not gv.sd['seq']) #  manual or concurrent mode.
                ):
                stayon = 0
                for octet in xrange(gv.sd['nbrd']):
                    base = octet * 8
                    for s in xrange(8):
                        stn = base + s
                        if (gv.srvals[stn] #  station is on
                            and gv.rs[stn][1] >= gv.now #  station has a stop time >= now
                            and gv.sd['mo'][octet] & 1 << s #  station activates master
                            ):
                            stayon = 1
                            break
                if not stayon:
                    gv.rs[gv.sd['mas'] - 1][1] = gv.now  # set master to turn off next cycle

        if gv.sd['urs']:
            check_rain()  # in helpers.py

        if gv.sd['rd'] and gv.now >= gv.sd['rdst']:  # Check if rain delay time is up
            gv.sd['rd'] = 0
            gv.sd['rdst'] = 0  # Rain delay stop time
            jsave(gv.sd, 'sd')

        time.sleep(1)
        #### End of timing loop ####


class SIPApp(web.application):
    """Allow program to select HTTP port."""

    def run(self, port=gv.sd['htp'], *middleware):  # get port number from options settings
        func = self.wsgifunc(*middleware)
        func = ReverseProxied(func)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


app = SIPApp(urls, globals())
#  disableShiftRegisterOutput()
web.config.debug = False  # Improves page load speed
if web.config.get('_session') is None:
    web.config._session = web.session.Session(app, web.session.DiskStore('sessions'),
                                              initializer={'user': 'anonymous'})
template_globals = {
    'gv': gv,
    'str': str,
    'eval': eval,
    'session': web.config._session,
    'json': json,
    'ast': ast,
    '_': _,
    'i18n': i18n,
    'app_path': lambda p: web.ctx.homepath + p,
    'web': web,
}

template_render = web.template.render('templates', globals=template_globals, base='base')

if __name__ == '__main__':

    #########################################################
    #### Code to import all webpages and plugin webpages ####

    import plugins

    try:
        print _('plugins loaded:')
    except Exception:
        pass
    for name in plugins.__all__:
        print ' ', name

    gv.plugin_menu.sort(key=lambda entry: entry[0])

    #  Keep plugin manager at top of menu
    try:
        gv.plugin_menu.pop(gv.plugin_menu.index(['Manage Plugins', '/plugins']))
    except Exception:
        pass

    thread.start_new_thread(timing_loop, ())

    if gv.use_gpio_pins:
        set_output()


    app.notfound = lambda: web.seeother('/')

    app.run()
