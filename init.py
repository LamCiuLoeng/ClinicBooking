# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sys2do.model import connection, MONGODB_DB, Sequence, UploadFile, SystemLog
import sys2do.model.auth as auth
import sys2do.model.logic as logic

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

    users = [
             ("aa@aa.com", "Admin", "Lam"),
             ("c1@aa.com", "Clinic Manager 1", "Lam"),
             ("c2@aa.com", "Clinic Manager 2", "Lam"),
             ("d1@aa.com", "Doctor 1", "Lam"),
             ("d2@aa.com", "Doctor 2", "Lam"),
             ("n1@aa.com", "Nurse 1", "Lam"),
             ("n2@aa.com", "Nurse 2", "Lam"),
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
    users_mapping["d1@aa.com"].roles = [roles_mapping["DOCTOR"].id, ]
    users_mapping["d2@aa.com"].roles = [roles_mapping["DOCTOR"].id, ]
    users_mapping["n1@aa.com"].roles = [roles_mapping["NURSE"].id, ]
    users_mapping["n2@aa.com"].roles = [roles_mapping["NURSE"].id, ]
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
    roles_mapping["DOCTOR"].users = [users_mapping["d1@aa.com"].id, users_mapping["d2@aa.com"].id]
    roles_mapping["NURSE"].permissions = [
                                           permissions_mapping["ORDER_VIEW"].id,
                                           permissions_mapping["ORDER_CANCEL"].id,
                                           permissions_mapping["ORDER_UPDATE"].id,
                                          ]
    roles_mapping["NURSE"].users = [users_mapping["n1@aa.com"].id, users_mapping["n2@aa.com"].id]
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


    clinic = [
              ("C1 Address", "Clinic 1", "This is C1 Clinic.", (22.396428, 114.1094970)),
              ("C2 Address", "Clinic 2", "This is C2 Clinic.", (22.396428, 114.0094970)),
              ("C3 Address", "Clinic 3", "This is C3 Clinic.", (22.296428, 114.0094970)),
              ("C4 Address", "Clinic 4", "This is C4 Clinic.", (22.286428, 114.1094970)),
              ("C5 Address", "Clinic 5", "This is C5 Clinic.", (22.284428, 114.1094970)),
              ]
    clinic_mapping = {}
    for address, name, desc, (lat, lng) in clinic:
        c = connection.Clinic()
        c.id = c.getID()
        c.address = unicode(address)
        c.name = unicode(name)
        c.desc = unicode(desc)
        c.location = (lat, lng)
        c.save()
        clinic_mapping[name] = c


    d1 = connection.DoctorProfile()
    d1.id = d1.getID()
    d1.uid = users_mapping["d1@aa.com"].id
    d1.desc = u"I'm temp 1 doctor."
    d1.clinic = [clinic_mapping["Clinic 1"].id]
    d1.worktime_setting = {
                              "MONDAY" : [[u"09:00", u"12:00"], [u"13:00", u"18:00"] ],
                              "TUESDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "WEDNESDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "THURSDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "FRIDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "SATURDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "SUNDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "HOLIDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "SPECIAL" : [],
                              }
    d1.save()

    d2 = connection.DoctorProfile()
    d2.id = d2.getID()
    d2.uid = users_mapping["d2@aa.com"].id
    d2.desc = u"I'm temp 2 doctor."
    d2.clinic = [clinic_mapping["Clinic 2"].id]
    d2.worktime_setting = {
                              "MONDAY" : [[u"09:00", u"12:00"], [u"13:00", u"18:00"] ],
                              "TUESDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "WEDNESDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "THURSDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "FRIDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "SATURDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "SUNDAY" : [],
                              "HOLIDAY" : [[u"09:00", u"18:00"], [u"13:00", u"18:00"] ],
                              "SPECIAL" : [],
                              }
    d2.save()

    n1 = connection.NurseProfile()
    n1.id = n1.getID()
    n1.uid = users_mapping["n1@aa.com"].id
    n1.desc = u"I'm temp 1 nurse."
    n1.clinic = [clinic_mapping["Clinic 1"].id]
    n1.save()

    n2 = connection.NurseProfile()
    n2.id = n1.getID()
    n2.uid = users_mapping["n2@aa.com"].id
    n2.desc = u"I'm temp 2 nurse."
    n2.clinic = [clinic_mapping["Clinic 2"].id]
    n2.save()

    clinic_mapping["Clinic 1"].doctors = [d1.id]
    clinic_mapping["Clinic 1"].nurses = [n1.id]
    clinic_mapping["Clinic 2"].doctors = [d2.id]
    clinic_mapping["Clinic 2"].nurses = [n2.id]

    for m in [users_mapping, roles_mapping, permissions_mapping, clinic_mapping]:
        for k, v in m.items():
            v.save()


    print "*" * 20
    print "finish"
    print "_" * 20

if __name__ == '__main__':
    init()
