# coding=utf-8
from flask import redirect, url_for
from flask_restful import Resource


class Index(Resource):
    def get(self):
        return redirect(url_for('index'))

    def post(self):
        pass
