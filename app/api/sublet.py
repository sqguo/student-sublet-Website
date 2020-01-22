from flask import request
from flask import abort
from flask import jsonify

from app.api import bp
from app import db
from app.models import User, Sublet, Review, Reply
from app.auth.oauth import requires_auth, get_current_user


@bp.route('/v0/sublet/<int:sublet_id>/<int:level>', methods=['GET'])
def get_sublets(sublet_id, level=0):
    sublet = db.session.query(Sublet).get(sublet_id)
    if sublet is None:
        abort(404)
    else:
        if level == 0:
            return jsonify({'sublet': sublet.serialize})
        elif level == 1:
            sublet_data = sublet.serialize
            author = db.session.query(User).get(sublet.creatorid)
            sublet_data['author'] = author.serialize
            return jsonify({'sublet': sublet_data})
        else:
            abort(400)


@requires_auth
@bp.route('/v0/sublet', methods=['POST'])
def post_sublets():
    creatorid = get_current_user()
    if request.json and 'latitude' in request.json and 'longitude' in request.json:
        lat = request.json['latitude']
        lon = request.json['longitude']
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            sublet = Sublet(
                creatorid=creatorid, latitude=lat, longitude=lon
            )
            if 'description' in request.json:
                sublet.set_description(request.json['description'])
            if 'profileimg' in request.json:
                sublet.set_profileimg(request.json['profileimg'])
            db.session.add(sublet)
            db.session.commit()
            return jsonify({'sublet': sublet.serialize}), 201
        else:
            abort(400)
    else:
        abort(400)
