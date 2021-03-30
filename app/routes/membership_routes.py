import flask
import bson
from mongoengine import Document

from models.athlete import Athlete
from models.member import Member

membership_routes = flask.Blueprint('membership_routes', __name__)


@membership_routes.route('/members/<member_id>/memberships', methods=["POST"])
def create_member_membership(member_id: str = 0) -> flask.Response:
    return _create_membership(Member, member_id)


@membership_routes.route('/athletes/<athlete_id>/memberships', methods=["POST"])
def create_athlete_membership(athlete_id: str = 0) -> flask.Response:
    return _create_membership(Athlete, athlete_id)


@membership_routes.route(
    '/members/<member_id>/memberships/<membership_id>',
    methods=["DELETE"]
)
def delete_member_membership(
        member_id: str = 0,
        membership_id: str = 0
) -> flask.Response:
    return _delete_membership(Member, member_id, membership_id)


@membership_routes.route(
    '/athletes/<athlete_id>/memberships/<membership_id>',
    methods=["DELETE"]
)
def delete_athlete_membership(
        athlete_id: str = 0,
        membership_id: str = 0
) -> flask.Response:
    return _delete_membership(Athlete, athlete_id, membership_id)


def _create_membership(document: Document, id: str):
    if not bson.ObjectId.is_valid(id):
        flask.abort(400)

    start_date = flask.request.form.get('start_date')
    end_date = flask.request.form.get('end_date')

    if start_date is None or end_date is None:
        flask.abort(400)

    document: Document = document.objects(id=id).first()
    if not document:
        flask.abort(404)

    document.memberships.create(start_date=start_date, end_date=end_date)

    document.save()

    return flask.jsonify(document.jsonify())


def _delete_membership(document: Document, id: str, membership_id: str):
    if not bson.ObjectId.is_valid(id):
        flask.abort(400)

    document: Document = document.objects(id=id).first()
    if not document:
        flask.abort(404)
    document.update(pull__memberships___id=membership_id)
    document.reload()

    return flask.jsonify(document.jsonify())
