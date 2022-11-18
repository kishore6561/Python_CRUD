from itertools import groupby
from tokenize import group
from unittest import result
from flask import Flask,request,jsonify,make_response
from flask_restful import Resource
import pymongo
import json
import config

class hello(Resource):
    def get(self):
        return make_response(jsonify({"result":"Hello"}),200)