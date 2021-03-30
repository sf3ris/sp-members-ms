import flask
from flask_cors import cross_origin
from models.member import Member
import mongoengine
from mongoengine.queryset.visitor import Q
import bson
from core.pdf.members_pdf import MembersPDF
from base64 import b64encode
import json
from services.import_document_service import import_document
import pyexcel as p

member_routes = flask.Blueprint('member_routes', __name__)


@member_routes.route('/members/<member_id>', methods=["GET"])
def get_member(member_id: str = 0) -> flask.Response:
    if not bson.ObjectId.is_valid(member_id):
        flask.abort(400)

    member = Member.objects(id=member_id).first()
    if not member:
        flask.abort(404)

    return flask.jsonify(member.jsonify())


@member_routes.route('/members', methods=["GET"])
def get_members() -> flask.Response:
    format = flask.request.args.get('format', '')
    name = flask.request.args.get('name', '')
    last_name = flask.request.args.get('lastName', '')
    fiscal_code = flask.request.args.get('fiscalCode', '')
    status = flask.request.args.get('status', '')

    members = Member.objects(
        Q(name__contains=name) &
        Q(last_name__contains=last_name) &
        Q(fiscal_code__contains=fiscal_code)
    )

    if status != '':
        if status == 'true':
            members = list(filter(lambda member: member.is_enabled(), members))
        else:
            members = list(filter(
                lambda member: not member.is_enabled(),
                members
            ))

    if format == 'pdf':
        columns: str = (flask.request.args.get('columns'))
        cols = columns.split(',')
        if len(cols) < 1:
            flask.abort(400)

        data = MembersPDF().generate_members_pdf(members, cols)
        return {'data': str(b64encode(data).decode("utf-8"))}

    return flask.jsonify([member.jsonify() for member in members])


@member_routes.route('/members', methods=["POST"])
@cross_origin(supports_credentials=True)
def create_member() -> flask.Response:
    name = flask.request.form.get('name')
    last_name = flask.request.form.get('last_name')
    birth_date = flask.request.form.get('birth_date')
    birth_place = flask.request.form.get('birth_place')
    fiscal_code = flask.request.form.get('fiscal_code')
    address = flask.request.form.get('address')
    zip_code = flask.request.form.get('zip_code')
    city = flask.request.form.get('city')
    province = flask.request.form.get('province')
    gender = flask.request.form.get('gender')
    phone = flask.request.form.get('phone')
    email = flask.request.form.get('email')
    memberships = json.loads(flask.request.form.get('temporaryMemberships'))

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
        email=email,
        memberships=memberships
    )

    member.save()

    return member.jsonify()


@member_routes.route('/members/<member_id>', methods=["PUT"])
@cross_origin(supports_credentials=True)
def update_member(member_id: str) -> flask.Response:
    if not bson.ObjectId.is_valid(member_id):
        flask.abort(400)

    name = flask.request.form.get('name')
    last_name = flask.request.form.get('last_name')
    birth_date = flask.request.form.get('birth_date')
    birth_place = flask.request.form.get('birth_place')
    fiscal_code = flask.request.form.get('fiscal_code')
    address = flask.request.form.get('address')
    zip_code = flask.request.form.get('zip_code')
    city = flask.request.form.get('city')
    province = flask.request.form.get('province')
    gender = flask.request.form.get('gender')
    phone = flask.request.form.get('phone')
    email = flask.request.form.get('email')

    member: mongoengine.Document = Member.objects(id=member_id).first()
    if not member:
        flask.abort(404)

    if name is not None:
        member.name = name
    if last_name is not None:
        member.last_name = last_name
    if birth_date is not None:
        member.birth_date = birth_date
    if birth_place is not None:
        member.birth_place = birth_place
    if fiscal_code is not None:
        member.fiscal_code = fiscal_code
    if address is not None:
        member.address = address
    if zip_code is not None:
        member.zip_code = zip_code
    if city is not None:
        member.city = city
    if province is not None:
        member.province = province
    if gender is not None:
        member.gender = gender
    if phone is not None:
        member.phone = phone
    if email is not None:
        member.email = email

    member.save()

    return member.jsonify()


@member_routes.route('/members/<member_id>', methods=["DELETE"])
def delete_member(member_id: str) -> flask.Response:
    if not bson.ObjectId.is_valid(member_id):
        flask.abort(400)

    member: mongoengine.Document = Member.objects(id=member_id).first()
    if not member:
        flask.abort(404)

    member.delete()

    return ('', 200)


@member_routes.route('/bulk/members', methods=['POST'])
def import_athletes():
    upload_file = flask.request.files['members']
    file_path = "./tmp/bulk_members_upload.xlsx"
    upload_file.save(file_path)

    rows = p.get_records(file_name=file_path, start_row=1)

    # Retrieves header name for the excel file
    name_field = flask.request.form.get('name')
    last_name_field = flask.request.form.get('last_name')
    birth_date_field = flask.request.form.get('birth_date')
    birth_place_field = flask.request.form.get('birth_place')
    fiscal_code_field = flask.request.form.get('fiscal_code')
    address_field = flask.request.form.get('address')
    zip_code_field = flask.request.form.get('zip_code')
    city_field = flask.request.form.get('city')
    province_field = flask.request.form.get('province')
    gender_field = flask.request.form.get('gender')
    phone_field = flask.request.form.get('phone')
    email_field = flask.request.form.get('email')

    members = import_document(
        Member,
        rows,
        name_field,
        last_name_field,
        birth_date_field,
        birth_place_field,
        fiscal_code_field,
        address_field,
        zip_code_field,
        city_field,
        province_field,
        gender_field,
        phone_field,
        email_field
    )

    return flask.jsonify(members)
