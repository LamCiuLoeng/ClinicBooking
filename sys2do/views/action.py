# -*- coding: utf-8 -*-
'''
Created on 2011-5-4

@author: cl.lam
'''
from datetime import datetime as dt, timedelta
import calendar, traceback
from webhelpers.paginate import Page
import pymongo
from flask import g, render_template, flash, session, redirect, url_for, request
from flask import current_app as app
from flask.helpers import jsonify

from sys2do.model import connection
from sys2do.util.decorator import templated


@templated("list_clinic.html")
def list_clinic():
    cs = list(connection.Clinic.find({'active':0}).sort('name'))
    return {"clinics" :cs}


@templated("list_doctors.html")
def list_doctors():
    id = request.values.get("id", None)
    if not id:
        dps = connection.DoctorProfile.find({'active':0})
        data = [dp.populate() for dp in dps]
    else:
        c = connection.Clinic.one({'active':0, 'id':int(id)})
        data = [connection.DoctorProfile.one({'id':i}).populate() for i in c.doctors]
    return {"doctors" : data}



def list_doctors_by_clinic():
    id = request.values.get("id", None)
    if not id:
        flash("No clinic supplied !")
        return redirect(url_for("index"))
    else:
        c = connection.Clinic.one({'active':0, 'id':int(id)})
        data = [connection.DoctorProfile.one({'id':i})for i in c.doctors]

    return render_template("list_doctors_by_clinic.html", doctors = data, clinic = c)


def schedule():
    id = request.values.get("id", None)
    if not id :
        flash("No doctor id is supplied!", "WARNING")
        return redirect("/index")

    dp = connection.DoctorProfile.one({'id':int(id)})
    year = int(request.values.get("y", dt.now().year))
    month = int(request.values.get("m", dt.now().month))
    current = dt(year, month, 15)
    pre = current - timedelta(days = 30)
    next = current + timedelta(days = 30)
    calendar.setfirstweekday(6)

    es = connection.Events.find({'active':0,
                                  'did':int(id),
                                  'date':{'$gt':current.strftime('%Y%m'), '$lt':next.strftime('%Y%m')}
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

            for e in info['events']:
                if e.uid == session['user_profile']['id']:
                    info['is_booked'] = True
                    app.logger.debug('It booked')
                    break
            else:
                info['is_booked'] = False


            if len(info['events']) >= dp.qty:
                info['avaiable'] = False
                if len(info['events']) == dp.qty : info['full'] = True
            elif d.weekday() not in dp.avaiable_day:
                info['avaiable'] = False
            elif d < dt.today().date():
                info['avaiable'] = False
            else:
                info['avaiable'] = True
        s.append(info)
    return render_template("/schedule.html", schedule = s, doctor = dp, current = current, pre = pre, next = next)



def save_events():
    uid = request.values.get("uid", None)
    did = request.values.get("did", None)
    d = request.values.get("d", None)

    if not uid or not did or not d:
        return jsonify({
                        "success" : False,
                        "message" : "The required info is not supplied !"
                        })
    try:
        e = connection.Events()
        e.id = e.getID()
        e.uid = int(uid)
        e.did = int(did)
        e.date = d
        e.remark = request.values.get("remark", None)
        e.save()

        doctor = connection.DoctorProfile.one({'id':int(did)}).populate()
        m = connection.Message()
        m.id = m.getID()
        m.subject = u'Booking request submit'
        m.uid = session['user_profile']['id']
        m.content = u'%s make a booking with doctor %s on %s' % (session['user_profile']['name'], doctor['name'], d)
        m.save()

        return jsonify({
                        "success" : True,
                        "message" : "Save your request successfully !"
                        })
    except:
        app.logger.error(traceback.format_exc())
        return jsonify({
                        "success" : False,
                        "message" : "Error occur when submiting the request !"
                        })



def my_booking():
    try:
        page = request.values.get("page", 1)
    except:
        page = 1
    id = session['user_profile']['id']

    events = list(connection.Events.find({'active':0, 'uid':id}).sort("date"))
    paginate_events = Page(events, page = page, items_per_page = 10, url = lambda page:"%s?page=%d" % (url_for("my_booking"), page))
    return render_template("/my_booking.html", events = paginate_events)


def my_message():
    try:
        page = request.values.get("page", 1)
    except:
        page = 1
    id = session['user_profile']['id']

    msgs = list(connection.Message.find({'active':0, 'uid':id}).sort("create_time", pymongo.DESCENDING))
    paginate_msgs = Page(msgs, page = page, items_per_page = 10, url = lambda page:"%s?page=%d" % (url_for("my_message"), page))
    return render_template("/my_message.html", messages = paginate_msgs)
