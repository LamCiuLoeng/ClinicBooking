'''
Created on 2011-4-21

@author: cl.lam
'''
import datetime, traceback
from mongokit import Document
from flask import current_app as app
from sys2do.model import connection, Abstract

__all__ = ['Clinic', 'Category', 'DoctorProfile', 'NurseProfile', 'Events', 'Message', ]

@connection.register
class Clinic(Abstract):
    __collection__ = 'CLINIC'
    structure = {
        'name': unicode,
        'location' : (float, float),
        'address':unicode,
        'district':unicode,
        'street':unicode,
        'website' : unicode,
        'image_url' : int,
        'desc':unicode,
        'doctors':[int],
        'nurses':[int],
        'category':[int],
        'admin' : [int]
    }

    required_fields = ['name']
    default_values = {'create_time':datetime.datetime.now(),
                      'doctors' : [],
                      'nurses' : [],
                      'category' : []}

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.name

    def populate(self):
        return {
                'id' : self.id,
                'name' : self.name,
                'desc' : self.desc,
                }

    def getImage(self):
        try:
            return connection.UploadFile.one({"id" : self.image_url})
        except:
            app.logger.error(traceback.format_exc())
            return None


@connection.register
class Category(Abstract):
    __collection__ = 'CATEGORY'
    structure = {
        'cid':int,
        'name': unicode,
        'desc':unicode,
        'doctors':[int],
    }

    required_fields = ['cid', 'name']
    default_values = {'create_time':datetime.datetime.now(),
                      'doctors' :[]}

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.name

    def populate(self):
        return {
                'id' :self.id,
                'name' : self.name,
                'desc' : self.desc,
                }


@connection.register
class DoctorProfile(Abstract):
    __collection__ = 'DOCTORPROFILE'
    structure = {
        'uid': int,
        'desc':unicode,
        'category':[int],
        'clinic':[int],
        'avaiable_day' : [int],
        'qty' : int
    }

    required_fields = ['uid']
    default_values = {'create_time':datetime.datetime.now(),
                      'qty' : 10,
                      'avaiable_day' : range(1, 6),
                      'clinic' : []}

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.name

    def populate(self):
        u = connection.User.one({'id':self.uid})
        user_info = u.populate()
        doctor_info = {
                       'id' : self.id,
                       'uid' : u.id,
                       'desc' : self.desc,
                       'qty' : self.qty,
                       'avaiable_day' : self.avaiable_day
                       }
        user_info.update(doctor_info)
        return user_info

    def getUserProfile(self):
        return connection.User.one({"id" : self.uid})

    @property
    def name(self):
        return str(connection.User.one({"id" : self.uid}))

@connection.register
class NurseProfile(Abstract):
    __collection__ = 'NURSEPROFILE'
    structure = {
        'uid': int,
        'desc':unicode,
        'clinic':[int],
    }

    required_fields = ['uid']
    default_values = {'create_time':datetime.datetime.now(),
                      'clinic' : []}

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.name

    def getUserProfile(self):
        return connection.User.one({"id" : self.uid})

@connection.register
class Events(Abstract):
    __collection__ = 'EVENTS'
    structure = {
        'id': int,
        'uid': int,
        'did': int,
        'date' : unicode,
        'status' : int,
        'remark':unicode,
    }

    equired_fields = ['uid', 'did', 'start', 'end']
    default_values = {
                      'create_time':datetime.datetime.now(),
                      'status' : 0 #0 is new ,1 is confirmed , 2 is cancel
                      }

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.title

    def showStatus(self):
        return {
                0 : "NEW",
                1 : "CONFIRMED",
                2 : "CANCEL"
                }[self.status]

@connection.register
class Message(Abstract):
    __collection__ = 'MESSAGE'
    structure = {
        'id': int,
        'uid': int,
        'subject':unicode,
        'content':unicode,
        'type' : unicode,
        'time' : datetime.datetime,
        'status' : unicode,
    }

    equired_fields = ['uid', 'title']
    default_values = {
                      'create_time':datetime.datetime.now(),
                      'type' : u'NORMAL',
                      'time':datetime.datetime.now(),
                     }

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.subject


