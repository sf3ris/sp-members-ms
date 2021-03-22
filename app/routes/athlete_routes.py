import flask
import pyexcel as p
import bson
from models.athlete import Athlete
from services.import_document_service import import_document

athlete_routes = flask.Blueprint('athlete_route', __name__)


@athlete_routes.route('/athletes', methods=['GET'])
def athletes() -> flask.Response:
    athletes = Athlete.objects().all()
    athletes = [athlete.jsonify() for athlete in athletes]

    return flask.jsonify(athletes)


@athlete_routes.route('/athletes/<athlete_id>', methods=['GET'])
def athlete(athlete_id: str = 0) -> flask.Response:
    if not bson.ObjectId.is_valid(athlete_id):
        flask.abort(400)

    athlete = Athlete.objects(id=athlete_id).first()
    if not athlete:
        flask.abort(404)

    return flask.jsonify(athlete.jsonify())


@athlete_routes.route('/athletes', methods=['POST'])
def create_athlete() -> flask.Response:
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

    athlete = Athlete(
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

    athlete.save()

    return athlete.jsonify()


@athlete_routes.route('/athletes/<athlete_id>', methods=["PUT"])
def update_athlete(athlete_id: str) -> flask.Response:
    if not bson.ObjectId.is_valid(athlete_id):
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

    athlete: Athlete = Athlete.objects(id=athlete_id).first()
    if not athlete:
        flask.abort(400)

    if name is not None:
        athlete.name = name
    if last_name is not None:
        athlete.last_name = last_name
    if birth_date is not None:
        athlete.birth_date = birth_date
    if birth_place is not None:
        athlete.birth_place = birth_place
    if fiscal_code is not None:
        athlete.fiscal_code = fiscal_code
    if address is not None:
        athlete.address = address
    if zip_code is not None:
        athlete.zip_code = zip_code
    if city is not None:
        athlete.city = city
    if province is not None:
        athlete.province = province
    if gender is not None:
        athlete.gender = gender
    if phone is not None:
        athlete.phone = phone
    if email is not None:
        athlete.email = email

    athlete.save()

    return athlete.jsonify()


@athlete_routes.route('/athletes/<athlete_id>', methods=["DELETE"])
def delete_athlete(athlete_id: str = 0) -> flask.Response:
    if not bson.ObjectId.is_valid(athlete_id):
        flask.abort(400)

    athlete: Athlete = Athlete.objects(id=athlete_id).first()
    if not athlete:
        flask.abort(404)

    athlete.delete()

    return ('', 200)


@athlete_routes.route('/bulk/athletes', methods=['POST'])
def import_athletes():
    upload_file = flask.request.files['athletes']
    header_row = flask.request.form.get('header_row') or '0'

    rows = p.get_records(
        file_content=upload_file.read(),
        file_type='xlsx',
        start_row=int(header_row)
    )

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

    athletes = import_document(
        Athlete,
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

    return flask.jsonify(athletes)
