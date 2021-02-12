from operator import itemgetter as item_getter
from resource.base import Base_Resource

from docstring import docstring
from lib.http import HTTP_Method
from lib.polycube import Polycube
from lib.response import *
from schema.code import *
from schema.response import *
from utils.datetime import datetime_to_str
from utils.sequence import is_list, wrap

__all__ = [
    'FooThing'
]


class FooThing(Base_Resource):
    tag = {'name': 'FooThing', 'description': 'Does Nothing but allows me learn.'}
    routes = '/foothing', '/foothing/{id}',

    def __init__(self):
        pass

    @docstring(source='foothing/get.yaml')
    def on_get(self, req, resp, id=None):
        print("Estoy en la funcion sin parametros")
        return

