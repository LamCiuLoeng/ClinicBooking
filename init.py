# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sys2do.model import connection, MONGODB_DB, Sequence, UploadFile, SystemLog
import sys2do.model.auth as auth
import sys2do.model.logic as logic
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def init():
    db = getattr(connection, MONGODB_DB)
    objects = [Sequence, UploadFile, SystemLog]
    objects.extend([getattr(auth, name) for name in auth.__all__])
    objects.extend([getattr(logic, name) for name in logic.__all__])

    print "*" * 20
    print "drop all collection"
    print "_" * 20
    #clear the DB
    for o in objects:
        print str(o)
        db.drop_collection(o.__collection__)

    print "*" * 20
    print "Init the sequence"
    print "_" * 20
    #init the seq
    for o in objects:
        seq = connection.Sequence()
        seq.name = unicode(o.__collection__)
        seq.save()


    print "*" * 20
    print "Adding the default data"
    print "_" * 20
    #init the permission
    permissions = ["ORDER_ADD", "ORDER_VIEW", "ORDER_CANCEL", "ORDER_UPDATE", "ORDER_VIEW_ALL",
                   "CLINIC_ADD", "CLINIC_VIEW", "CLINIC_VIEW_ALL", "CLINIC_UPDATE", "CLINIC_DELETE",
                   "DOCTOR_ADD", "DOCTOR_UPDATE", "DOCTOR_DELETE",
                   "NURSE_ADD", "NURSE_UPDATE", "NURSER_DELETE",
                   ]
    permissions_mapping = {}
    for p in permissions:
        obj = connection.Permission()
        obj.name = unicode(p)
        obj.id = obj.getID()
#        obj.save()
        permissions_mapping[p] = obj


    #add the HK holiday 
    for d in ["0101", "0203", "0204", "0205", "0405", "0423", "0425", "0502", "0510",
              "0606", "0701", "0913", "1001", "1005", "1226", "1227"]:
        day = connection.Holiday()
        day.id = day.getID()
        day.year = 2011
        day.month = int(d[:2])
        day.day = int(d[-2:])
        day.save()



    users = [
             ("aa@aa.com", "Admin", "Lam"),
             ("c1@aa.com", "Clinic Manager 1", "Lam"),
             ("c2@aa.com", "Clinic Manager 2", "Lam"),
             ("u1@aa.com", "User 1", "Lam"),
             ("u2@aa.com", "User 2", "Lam"),
             ("t1@aa.com", "Temp 1", "Lam"),
             ("t2@aa.com", "Temp 2", "Lam"),
             ]
    users_mapping = {}
    for (email, first_name, last_name) in users:
        u = connection.User()
        u.email = unicode(email)
        u.password = u"aa"
        u.first_name = unicode(first_name)
        u.last_name = unicode(last_name)
        u.id = u.getID()
#        u.save()
        users_mapping[email] = u

    roles = [
             ("ADMINISTRATOR", "Administrator"),
             ("CLINIC_MANAGER", "Clinic Manager"),
             ("DOCTOR", "Doctor"),
             ("NURSE", "Nurse"),
             ("NORMALUSER", "Normal User"),
             ("TEMPUSER", "Temp User")
             ]
    roles_mapping = {}
    for (name, display_name) in roles:
        r = connection.Role()
        r.name = unicode(name)
        r.display = unicode(display_name)
        r.id = r.getID()
#        r.save()
        roles_mapping[name] = r


    users_mapping["aa@aa.com"].roles = [roles_mapping["ADMINISTRATOR"].id, ]
    users_mapping["c1@aa.com"].roles = [roles_mapping["CLINIC_MANAGER"].id, ]
    users_mapping["c2@aa.com"].roles = [roles_mapping["CLINIC_MANAGER"].id, ]
    users_mapping["u1@aa.com"].roles = [roles_mapping["NORMALUSER"].id, ]
    users_mapping["u2@aa.com"].roles = [roles_mapping["NORMALUSER"].id, ]
    users_mapping["t1@aa.com"].roles = [roles_mapping["TEMPUSER"].id, ]
    users_mapping["t2@aa.com"].roles = [roles_mapping["TEMPUSER"].id, ]

    roles_mapping["ADMINISTRATOR"].permissions = [v.id for k, v in permissions_mapping.items()]
    roles_mapping["ADMINISTRATOR"].users = [users_mapping["aa@aa.com"].id, ]
    roles_mapping["CLINIC_MANAGER"].permissions = [
                                                   permissions_mapping["CLINIC_VIEW"].id,
                                                   permissions_mapping["CLINIC_UPDATE"].id,
                                                   permissions_mapping["DOCTOR_ADD"].id,
                                                   permissions_mapping["DOCTOR_UPDATE"].id,
                                                   permissions_mapping["DOCTOR_DELETE"].id,
                                                   permissions_mapping["NURSE_ADD"].id,
                                                   permissions_mapping["NURSE_UPDATE"].id,
                                                   permissions_mapping["NURSER_DELETE"].id,
                                                   permissions_mapping["ORDER_VIEW"].id,
                                                   permissions_mapping["ORDER_CANCEL"].id,
                                                   permissions_mapping["ORDER_UPDATE"].id,
                                                   ]
    roles_mapping["CLINIC_MANAGER"].users = [users_mapping["c1@aa.com"].id, users_mapping["c2@aa.com"].id]
    roles_mapping["DOCTOR"].permissions = [
                                           permissions_mapping["ORDER_VIEW"].id,
                                           permissions_mapping["ORDER_CANCEL"].id,
                                           permissions_mapping["ORDER_UPDATE"].id,
                                           ]
    roles_mapping["DOCTOR"].users = []
    roles_mapping["NURSE"].permissions = [
                                           permissions_mapping["ORDER_VIEW"].id,
                                           permissions_mapping["ORDER_CANCEL"].id,
                                           permissions_mapping["ORDER_UPDATE"].id,
                                          ]
    roles_mapping["NURSE"].users = []
    roles_mapping["NORMALUSER"].permissions = [
                                               permissions_mapping["ORDER_ADD"].id,
                                               permissions_mapping["ORDER_VIEW"].id,
                                               permissions_mapping["ORDER_CANCEL"].id,
                                               ]
    roles_mapping["NORMALUSER"].users = [users_mapping["u1@aa.com"].id, users_mapping["u2@aa.com"].id]
    roles_mapping["TEMPUSER"].permissions = []
    roles_mapping["TEMPUSER"].users = [users_mapping["t1@aa.com"].id, users_mapping["t2@aa.com"].id]


    permissions_mapping["ORDER_ADD"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["NORMALUSER"].id, ]
    permissions_mapping["ORDER_VIEW"].roles = [
                                               roles_mapping["ADMINISTRATOR"].id,
                                               roles_mapping["CLINIC_MANAGER"].id,
                                               roles_mapping["DOCTOR"].id,
                                               roles_mapping["NURSE"].id,
                                               ]
    permissions_mapping["ORDER_CANCEL"].roles = [
                                                 roles_mapping["ADMINISTRATOR"].id,
                                                 roles_mapping["NORMALUSER"].id,
                                                 roles_mapping["DOCTOR"].id,
                                                 roles_mapping["NURSE"].id,
                                                 ]
    permissions_mapping["ORDER_UPDATE"].roles = [
                                                 roles_mapping["ADMINISTRATOR"].id,
                                                 roles_mapping["CLINIC_MANAGER"].id,
                                                 roles_mapping["DOCTOR"].id,
                                                 roles_mapping["NURSE"].id,
                                                 ]
    permissions_mapping["ORDER_VIEW_ALL"].roles = [roles_mapping["ADMINISTRATOR"].id, ]
    permissions_mapping["CLINIC_ADD"].roles = [roles_mapping["ADMINISTRATOR"].id, ]
    permissions_mapping["CLINIC_VIEW"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id ]
    permissions_mapping["CLINIC_VIEW_ALL"].roles = [roles_mapping["ADMINISTRATOR"].id, ]
    permissions_mapping["CLINIC_UPDATE"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id ]
    permissions_mapping["CLINIC_DELETE"].roles = [roles_mapping["ADMINISTRATOR"].id, ]
    permissions_mapping["DOCTOR_ADD"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id ]
    permissions_mapping["DOCTOR_UPDATE"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id, ]
    permissions_mapping["DOCTOR_DELETE"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id ]
    permissions_mapping["NURSE_ADD"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id ]
    permissions_mapping["NURSE_UPDATE"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id, ]
    permissions_mapping["NURSER_DELETE"].roles = [roles_mapping["ADMINISTRATOR"].id, roles_mapping["CLINIC_MANAGER"].id ]


    from clinic_list import clinics
    clinics_mapping = {}

    for (code, name, address, tel) in clinics:
        c = connection.Clinic()
        c.id = c.getID()
        c.code = unicode(code)
        c.name = unicode(name)
        c.address = unicode(address)
        c.tel = unicode(tel)

        u = connection.User()
        u.id = u.getID()
        u.email = unicode("%sNUR@ieasybooking.com" % code)
        u.password = u"aa"
        u.first_name = unicode(code)
        u.last_name = unicode("Nurse")

        n = connection.NurseProfile()
        n.id = n.getID()
        n.uid = u.id
        n.desc = u"I'm nurse."
        n.clinic = [c.id]

        c.nurses = [n.id]
        c.doctors = []
        roles_mapping["NURSE"].users.append(n.id)

        u.save()
        c.save()
        n.save()

        clinics_mapping[code] = c


    from doctors_list import doctors
    doctors_count = {}
    default_worktime = {
                          "MONDAY" : [ ],
                          "TUESDAY" : [],
                          "WEDNESDAY" : [],
                          "THURSDAY" : [],
                          "FRIDAY" : [],
                          "SATURDAY" : [],
                          "SUNDAY" : [],
                          "HOLIDAY" : [],
                          "SPECIAL" : [],
                          }
    for (code, first_name, last_name, worktime) in doctors:
        u = connection.User()
        u.id = u.getID()

        if code in doctors_count : doctors_count[code] += 1
        else : doctors_count[code] = 1

        u.email = unicode("%sDOC_%d@ieasybooking.com" % (code, doctors_count[code]))
        u.password = u"aa"
        u.first_name = unicode(first_name)
        u.last_name = unicode(last_name)
        u.roles = [roles_mapping["DOCTOR"].id, ]
        roles_mapping["DOCTOR"].users.append(u.id)

        tempWorkTime = default_worktime.copy()
        tempWorkTime.update(worktime)
        for k, v in tempWorkTime.items():
            tempWorkTime[k] = map(lambda o:{"times" : o, "seats" : 4}, v)
        c = clinics_mapping[code]
        d = connection.DoctorProfile()
        d.id = d.getID()
        d.uid = u.id
        d.clinic = [c.id]
        d.worktime_setting = tempWorkTime
        c.doctors.append(d.id)
        c.save()
        u.save()
        d.save()


    for m in [users_mapping, roles_mapping, permissions_mapping]:
        for k, v in m.items():
            v.save()


    print "*" * 20
    print "finish"
    print "_" * 20

if __name__ == '__main__':
    init()
