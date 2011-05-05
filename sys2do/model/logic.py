'''
Created on 2011-4-21

@author: cl.lam
'''
import datetime
from mongokit import Document
from sys2do.model import connection, Abstract

__all__ = ['Clinic', 'Category', 'DoctorProfile', 'NurseProfile', 'Events', 'Message']

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
        'image_url' : unicode,
        'desc':unicode,
        'doctors':[int],
        'nurse':[int],
        'category':[int],
    }

    required_fields = ['name']
    default_values = {'create_time':datetime.datetime.now(),
                      'doctors' : [],
                      'nurse' : [],
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
                      'avaiable_day' : range(0, 7),
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



@connection.register
class Events(Abstract):
    __collection__ = 'EVENTS'
    structure = {
        'id': int,
        'uid': int,
        'did': int,
        'date' : unicode,
        'status' : unicode,
        'remark':unicode,
    }

    equired_fields = ['uid', 'did', 'start', 'end']
    default_values = {'create_time':datetime.datetime.now()}

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.title


@connection.register
class Message(Abstract):
    __collection__ = 'MESSAGE'
    structure = {
        'id': int,
        'uid': int,
        'title':unicode,
        'content':unicode,
        'date' : unicode,
        'status' : unicode,
    }

    equired_fields = ['uid', 'start', 'end']
    default_values = {'create_time':datetime.datetime.now()}

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.title
