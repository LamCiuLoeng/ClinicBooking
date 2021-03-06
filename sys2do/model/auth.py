'''
Created on 2011-4-21

@author: cl.lam
'''
import datetime, traceback
from mongokit import Document

from sys2do.model import connection, Abstract, MONGODB_DB
from sys2do.util.validator import *



__all__ = ['User', 'Role', 'Permission']




@connection.register
class User(Abstract):
    __database__ = MONGODB_DB
    __collection__ = 'USER'
    structure = {
        'email': unicode,
        'password':unicode,
        'first_name': unicode,
        'last_name': unicode,
        'phone': unicode,
        'birthday': unicode,
        'image_url':int,
        'roles':[int],
    }

    required_fields = ['email', 'password']
    default_values = {'create_time':datetime.datetime.now()}

    validators = {
        'email': max_length(120)
    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return '%s%s' % (self.first_name, self.last_name)

    def name(self):
        return '%s%s' % (self.first_name, self.last_name)

    def populate(self):
        return {
                'id' : self.id,
                'email' : self.email,
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'image_url' : self.image_url,
                'phone' : self.phone,
                'name' : unicode(self)
                }

    def getImage(self):
        try:
            return connection.UploadFile.one({"id" : self.image_url})
        except:
            app.logger.error(traceback.format_exc())
            return None



@connection.register
class Role(Abstract):
    __collection__ = 'ROLE'
    structure = {
        'name': unicode,
        'displayname' : unicode,
        'desc':unicode,
        'users':[int],
        'permissions':[int],
    }

    required_fields = ['name']
    default_values = {'create_time':datetime.datetime.now()}

    validators = {
        'name': max_length(50),
    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.name


@connection.register
class Permission(Abstract):
    __collection__ = 'PERMISSION'
    structure = {
        'name': unicode,
        'desc':unicode,
        'roles':[int],
    }

    required_fields = ['name']
    default_values = {'create_time':datetime.datetime.now()}

    validators = {

    }
    use_dot_notation = True
    use_autorefs = True
    def __repr__(self):
        return self.name
