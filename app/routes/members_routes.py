import flask
from models.member import Member
import sys, os
import mongoengine
from typing import List, Dict

member_routes = flask.Blueprint('member_routes',__name__)

@member_routes.route('/members/<member_id>',methods=["GET"])
def member(member_id : str = 0) -> flask.Response:

    member = Member.objects(id=member_id).first()

    return flask.jsonify(member.to_mongo())

@member_routes.route('/members',methods=["GET"])
def members() -> flask.Response:

    members = Member.objects().load()

    return flask.jsonify(members)

@member_routes.route('/members',methods=["POST"])
def create_member() -> flask.Response:

    name        = flask.request.form.get('name')
    last_name   = flask.request.form.get('last_name')
    birth_date  = flask.request.form.get('birth_date')
    birth_place = flask.request.form.get('birth_place')
    fiscal_code = flask.request.form.get('fiscal_code')
    address     = flask.request.form.get('address')
    zip_code    = flask.request.form.get('zip_code')
    city        = flask.request.form.get('city')
    province    = flask.request.form.get('province')
    gender      = flask.request.form.get('gender')
    phone       = flask.request.form.get('phone')
    email       = flask.request.form.get('email')

    member = Member(
            name=name,
            last_name=last_name,
            birth_date=birth_date,
            birth_place=birth_place,
            fiscal_code=fiscal_code,
            address=address,
            zip_code=zip_code,
            city=city,
            province=province,
            gender=gender,
            phone=phone,
            email=email
        )

    member.save()
        
    document = member.to_mongo()
    document['_id'] = str(document['_id'])

    return document