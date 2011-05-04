# -*- coding: utf-8 -*-
'''
Created on 2011-5-4

@author: cl.lam
'''
from datetime import datetime as dt, timedelta
import calendar

from flask import g, render_template, flash, session, redirect, url_for, request
from flask import current_app as app
from sys2do.model import connection
from flask.helpers import jsonify


def list_clinic():
    cs = connection.Clinic.find({'active':0})
    return render_template("list_clinic.html", clinics = cs)


def list_doctor():
    id = request.values.get("id", None)
    if not id:
        dps = connection.DoctorProfile.find({'active':0})
        data = [dp.populate() for dp in dps]
    else:
        c = connection.Clinic.one({'active':0, 'id':int(id)})
        data = [connection.DoctorProfile.one({'id':i}).populate() for i in c.doctors]

    return render_template("list_doctors.html", doctors = data)



def schedule():
    id = request.values.get("id", None)
    if not id :
        flash("No doctor id is supplied!", "WARNING")
        return redirect("/index")

    dp = connection.DoctorProfile.one({'id':int(id)}).populate()
    app.logger.debug(dp)
    year = int(request.values.get("y", dt.now().year))
    month = int(request.values.get("m", dt.now().month))
    current = dt(year, month, 15)
    pre = current - timedelta(days = 30)
    next = current + timedelta(days = 30)
    calendar.setfirstweekday(6)

    es = connection.Events.find({'active':0,
                                  'did':int(id),
                                  'date':{'$lt':current.strftime('%Y%m'), '$gt':next.strftime('%Y%m')}
                                  }).sort("date")

    events = {}
    for b in es:
        if b.date in events:
            events[b.date].append(b)
        else:
            events[b.date] = [b]

    s = []
    for d in calendar.Calendar().itermonthdates(year, month):
        info = {
                "date" : d,
                }
        if d.month != month:
            info['this_month'] = False
        else:
            info['this_month'] = True
            info['events'] = events[d.strftime("%Y%m%d")] if d.strftime("%Y%m%d") in events else []

            if len(info['events']) >= dp['qty']:
                info['avaiable'] = False
                if len(info['events']) == dp['qty'] : info['full'] = True
            elif d.weekday() not in dp['avaiable_day']:
                info['avaiable'] = False
            else:
                info['avaiable'] = True
        s.append(info)
    return render_template("/schedule.html", schedule = s, doctor_profile = dp, current = current, pre = pre, next = next)



def save_events():
    uid = request.values.get("uid", None)
    did = request.values.get("did", None)
    d = request.values.get("d", None)

    if not uid or not did or not d:
        return jsonify({
                        "success" : False,
                        "message" : "The required info is not supplied !"
                        })
    e = connection.Events()
    e.id = e.getID()
    e.uid = int(uid)
    e.did = int(did)
    e.date = d
    e.remark = request.values.get("remark", None)
    e.save()
    return jsonify({
                    "success" : True,
                    "message" : "Save your request successfully !"
                    })
