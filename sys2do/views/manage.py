# -*- coding: utf-8 -*-
from datetime import datetime as dt, timedelta
import calendar, traceback
from webhelpers.paginate import Page
import pymongo
from flask import g, render_template, flash, session, redirect, url_for, request
from flask import current_app as app
from flask.helpers import jsonify

from sys2do.model import connection
from sys2do.util.common import MESSAGE_INFO, MESSAGE_ERROR, _g, _gList


def m_clinic_list():
    try:
        page = request.values.get("page", 1)
    except:
        page = 1

    cs = list(connection.Clinic.find({'active':0}).sort('name'))
    paginate_clinics = Page(cs, page = page, items_per_page = 10, url = lambda page:"%s?page=%d" % (url_for("m_clinic"), page))
    return render_template("m_clinic_list.html", paginate_clinics = paginate_clinics)


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

    action_type = _g("type")
    if action_type == "NEW":
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
    elif action_type == 'UPDATE':
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
    ds = connection.DoctorProfile.find({'active':0})
    try:
        page = request.values.get("page", 1)
    except:
        page = 1

    ds = list(connection.DoctorProfile.find({'active':0}))
    paginate_docotrs = Page(ds, page = page, items_per_page = 10, url = lambda page:"%s?page=%d" % (url_for("m_doctor_list"), page))
    return render_template("m_doctor_list.html", paginate_docotrs = paginate_docotrs)

def m_doctor_update():
    type = request.values.get("type", None)
    if not type:
        flash("No such action type !", MESSAGE_ERROR)
        return redirect(url_for("m_doctor_list"))

    if type == "n":
        cs = connection.Clinic.find({'active':0}).sort('name')
        cats = connection.Category.find({'active':0}).sort('name')
        return render_template("m_doctor_new.html", clinics = cs, categories = cats)
    elif type in ["m", "d"]:
        id = request.values.get("id", None)
        if not id:
            flash("No doctor id supply", MESSAGE_ERROR)
            return redirect(url_for("m_doctor_list"))
        d = connection.DoctorProfile.one({'id' : int(id)})
        if type == "m":
            return render_template("m_doctor_update.html", doctor = d)
        elif type == "d":
            info = d.populate()
            d.active = 1
            d.save()
            l = connection.SystemLog()
            l.uid = session['user_profile']['id']
            l.type = u'DELETE DOCTOR'
            l.content = u'%s delete the doctor profile [name : %s, id : %d]' % (session['user_profile']['name'], info['name'], d.id)
            flash("The doctor profile [%s] has been deleted successfully !" % info['name'], MESSAGE_INFO)
            return redirect(url_for("m_doctor_list"))
    else:
        flash("No such action type !", MESSAGE_ERROR)
        return redirect(url_for("m_clinic_list"))



def m_doctor_save():
    required_fields = ["email", "password", "repassword", "first_name", "last_name"]
    for f in required_fields:
        if not _g(f) :
            flash("The required field is not supplied !", MESSAGE_ERROR)
            return redirect(url_for("m_doctor_list"))

    if _g("password") != _g("repassword"):
        flash("The password and the confirmed password are not the same !", MESSAGE_ERROR)
        return redirect(url_for("m_doctor_list"))

    action_type = _g("type")
    if action_type == "NEW":
        u = connection.User()
        u.id = u.getID()
        u.email = _g("email")
        u.password = _g("password")
        u.first_name = _g("first_name")
        u.last_name = _g("last_name")
        u.phone = _g("phone")
        u.birthday = _g("birthday")
        r = connection.Role.one({'active':0, 'name' : 'DOCTOR'})
        r.users.append(u.id)
        u.roles = [r.id]
        r.save()
        u.save()

        d = connection.DoctorProfile()
        d.id = d.getID()
        d.uid = u.id
        d.desc = _g("desc")
        d.qty = int(_g("qty"))  if _g("qty") else 10

        d.category = map(int, _gList("category"))
        d.clinic = map(int, _gList("clinic"))
        d.avaiable_day = map(int, _gList("avaiable_day"))
        d.save()
        flash("Save the new doctor successfully!", MESSAGE_INFO)
        return redirect(url_for("m_doctor_list"))

    elif action_type == 'UPDATE':
        id = _g("id")
        if not id:
            flash("No doctor id supplied!", MESSAGE_ERROR)
            return redirect(url_for("m_doctor_list"))
        d = connection.DoctorProfile.one({'id':int(id)})
        d.desc = _g("desc")
        d.category = map(int, _gList("category"))
        d.clinic = map(int, _gList("clinic"))
        d.avaiable_day = map(int, _gList("avaiable_day"))


        app.logger.info(_gList("avaiable_day"))

        d.save()

        u = connection.User.one({'id' : d.uid})
        u.email = _g("email")
        u.first_name = _g("first_name")
        u.last_name = _g("last_name")
        u.phone = _g("phone")
        u.birthday = _g("birthday")
        u.save()

        flash("Save the update successfully !", MESSAGE_INFO)
        return redirect(url_for("m_doctor_list"))
    else:
        flash("No such action type !", MESSAGE_ERROR)
        return redirect(url_for("m_doctor_list"))


def m_nurse_list():
    pass

def m_nurse_update():
    pass



def m_user_list():
    pass

def m_user_update():
    pass
