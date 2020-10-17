import flask
import bson

from models.member import Member
from models.membership import Membership

membership_routes = flask.Blueprint('membership_routes',__name__)

@membership_routes.route('/members/<member_id>/memberships', methods=["POST"])
def create_membership( member_id : str = 0 ) -> flask.Response:

    if not bson.ObjectId.is_valid(member_id):
        flask.abort(400)

    start_date  = flask.request.form.get('start_date')
    end_date    = flask.request.form.get('end_date')

    if(start_date is None or end_date is None):
        flask.abort(400)

    member : Member = Member.objects(id=member_id).first()
    if not member : 
        flask.abort(404)

    membership = Membership(
        start_date=start_date,
        end_date=end_date
    )

    member.memberships.create(start_date=start_date, end_date=end_date)

    member.save()

    return flask.jsonify(member.jsonify())

    