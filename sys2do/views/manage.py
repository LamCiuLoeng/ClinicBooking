# -*- coding: utf-8 -*-
from datetime import datetime as dt, timedelta
import calendar, traceback
from webhelpers.paginate import Page
import pymongo
from flask import g, render_template, flash, session, redirect, url_for, request
from flask import current_app as app
from flask.helpers import jsonify

from sys2do.model import connection
from sys2do.util.common import MESSAGE_INFO, MESSAGE_ERROR, _g


def m_clinic_list():
    try:
        page = request.values.get("page", 1)
    except:
        page = 1

    cs = list(connection.Clinic.find({'active':0}).sort('name'))
    paginate_clinics = Page(cs, page = page, items_per_page = 10, url = lambda page:"%s?page=%d" % (url_for("m_clinic"), page))
    return render_template("m_clinic.html", paginate_clinics = paginate_clinics)


def m_clinic_update():
    type = request.values.get("type", None)
    if not type:
        flash("No such action type !", MESSAGE_ERROR)
        return redirect(url_for("m_clinic_list"))

    if type == "n":
        return render_template("m_clinic_new.html")
    elif type in ["m", "d"]:
        id = request.values.get("id", None)
        if not id:
            flash("No clinic id supply", MESSAGE_ERROR)
            return redirect(url_for("m_clinic_list"))
        c = connection.Clinic.one({'id' : int(id)})
        if type == "m":
            return render_template("m_clinic_update.html", clinic = c)
        elif type == "d":
            c.active = 1
            c.save()
            l = connection.SystemLog()
            l.uid = session['user_profile']['id']
            l.type = u'DELETE CLINIC'
            l.content = u'%s delete the clinic [name : %s, id : %d]' % (session['user_profile']['name'], c.name, c.id)
            flash("The clinic [%s] has been deleted successfully !" % c.name, MESSAGE_INFO)
            return redirect(url_for("m_clinic_list"))
    else:
        flash("No such action type !", MESSAGE_ERROR)
        return redirect(url_for("m_clinic_list"))

def m_clinic_save():
    name = _g("name")
    if not name :
        flash("The clinic's name is not supplied!", MESSAGE_ERROR)
        return redirect(url_for("m_clinic_list"))

    type = _g("type")
    if type == "NEW":
        c = connection.Clinic()
        c.id = c.getID()
        c.name = name
        c.website = _g("website")
        c.address = _g("address")
        c.desc = _g("desc")
        lat = float(_g("lat")) if _g("lat") else None
        lng = float(_g("lng")) if _g("lng") else None
        c.location = (lat, lng)
        c.save()
        flash("Save the new clinic successfully!", MESSAGE_INFO)
        return redirect(url_for("m_clinic_list"))
    elif type == 'UPDATE':
        id = _g("id")
        if not id:
            flash("No clinic id supplied!", MESSAGE_ERROR)
            return redirect(url_for("m_clinic_list"))
        c = connection.Clinic.one({'id':int(id)})
        c.name = _g("name")
        c.website = _g("website")
        c.address = _g("address")
        c.desc = _g("desc")
        if _g("lat") : c.location[0] = float(_g("lat"))
        if _g("lng") : c.location[1] = float(_g("lng"))
        c.save()
        flash("Save the update successfully !", MESSAGE_INFO)
        return redirect(url_for("m_clinic_list"))
    else:
        flash("No such action type !", MESSAGE_ERROR)
        return redirect(url_for("m_clinic_list"))




def m_doctor_list():
    pass

def m_doctor_update():
    pass


def m_nurse_list():
    pass

def m_nurse_update():
    pass



def m_user_list():
    pass

def m_user_update():
    pass
