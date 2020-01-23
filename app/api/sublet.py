from flask import request
from flask import abort
from flask import jsonify

from app.api import bp
from app import db
from app.models import User, Sublet, Review, Reply
from app.auth.oauth import requires_auth, get_current_user


@bp.route('/v0/sublet/<int:sublet_id>', methods=['GET'])
def get_sublets(sublet_id):

    if request.json and 'level' in request.json:
        level = request.json['level']
    else:
        level = 0

    sublet = db.session.query(Sublet).get(sublet_id)
    if sublet is None:
        abort(404)

    if level == 0:
        return jsonify({'sublet': sublet.serialize})
    elif level == 1:
        sublet_data = sublet.serialize
        author = db.session.query(User).get(sublet.creatorid)
        sublet_data['creator'] = author.serialize
        return jsonify({'sublet': sublet_data})
    else:
        abort(400)


@requires_auth
@bp.route('/v0/sublet', methods=['POST'])
def post_sublets():
    creatorid = get_current_user()
    if not request.json:
        abort(400)
    if 'title' not in request.json:
        abort(400)
    if 'latitude' not in request.json:
        abort(400)
    if 'longitude' not in request.json:
        abort(400)

    lat = request.json['latitude']
    lon = request.json['longitude']
    title = request.json['title']

    if len(title) > 100:
        abort(400)
    if not (-90 <= lat <= 90):
        abort(400)
    if not (-180 <= lon <= 180):
        abort(400)

    sublet = Sublet(
        creatorid=creatorid, latitude=lat, longitude=lon, title=title
    )

    sync_sublet_json(sublet, request.json)
    db.session.add(sublet)
    db.session.commit()
    return jsonify({'sublet': sublet.serialize}), 201


@requires_auth
@bp.route('/v0/sublet/<int:sublet_id>', methods=['PUT'])
def update_sublet(sublet_id):

    sublet = db.session.query(Sublet).get(sublet_id)
    req_id = get_current_user()
    if sublet is None:
        abort(404)
    if sublet.creatorid != req_id:
        abort(403)

    if 'title' in request.json:
        title = request.json['title']
        if len(title) > 100:
            abort(400)
        sublet.set_title(title)

    if 'latitude' in request.json and 'longitude' in request.json:
        lat = request.json['latitude']
        lon = request.json['longitude']
        if not (-90 <= lat <= 90):
            abort(400)
        if not (-180 <= lon <= 180):
            abort(400)
        sublet.set_position(lat, lon)

    sync_sublet_json(sublet, request.json)
    db.session.commit()
    return jsonify({'sublet': sublet.serialize}), 201


@requires_auth
@bp.route('/v0/sublet/<int:sublet_id>', methods=['DELETE'])
def delete_sublet(sublet_id):

    sublet = db.session.query(Sublet).get(sublet_id)
    req_id = get_current_user()
    if sublet is None:
        abort(404)
    if sublet.creatorid != req_id:
        abort(403)
    db.session.delete(sublet)
    db.session.commit()
    return jsonify({'delete': True})


def sync_sublet_json(sublet, s_data):
    if 'description' in request.json:
        des = request.json['description']
        if len(des) > 200:
            abort(400)
        sublet.set_description(des)

    if 'address' in request.json:
        address = request.json['address']
        if len(address) > 100:
            abort(400)
        sublet.set_address(address)

    if 'postalcode' in request.json:
        pcode = request.json['postalcode']
        if len(pcode) > 6:
            abort(400)
        sublet.set_postalcode(pcode)

    if 'management' in request.json:
        manag = request.json['management']
        if len(manag) > 30:
            abort(400)
        sublet.set_management(manag)

    if 'profileimg' in request.json:
        plink = request.json['profileimg']
        if len(plink) > 200:
            abort(400)
        sublet.set_profileimg(plink)
