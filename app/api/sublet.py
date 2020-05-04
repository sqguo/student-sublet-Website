from flask import request
from flask import abort
from flask import jsonify
from flask import session

from app.api import bp
from app import db
from app.models import User, Sublet, Review, Reply

from functools import wraps


def requires_auth_api(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_profile' not in session:
            abort(401)
        return f(*args, **kwargs)
    return decorated


# retrieves a single sublet post of matching ID
@bp.route('/v0/sublet/<int:sublet_id>', methods=['GET'])
def get_sublets_by_id(sublet_id):

    if 'level' in request.args:
        try:
            level = int(request.args['level'])
        except Exception:
            abort(400)
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


# retrieves multiple sublet posts, currently ordered by ID
@bp.route('/v0/sublet', methods=['GET'])
def get_sublets():

    if 'size' in request.args:
        size = request.args['size']
    else:
        size = 10

    if 'page' in request.args:
        page = request.args['page']
    else:
        page = 1
    data = []
    sublets = db.session.query(Sublet).order_by(Sublet.id).paginate(int(page), int(size), True).items
    for sublet in sublets:
        data.append(sublet.serialize)
    return jsonify(data)


# adds a new sublet post into the database
@bp.route('/v0/sublet', methods=['POST'])
@requires_auth_api
def post_sublets():
    creatorid = session['user_profile']['user_id']
    if not request.json:
        print("missing json")
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


# enbles creator to update a single sublet post of matching ID
@bp.route('/v0/sublet/<int:sublet_id>', methods=['PUT'])
@requires_auth_api
def update_sublet(sublet_id):

    sublet = db.session.query(Sublet).get(sublet_id)
    req_id = session['user_profile']['user_id']
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


# enbles creator to update a single sublet post of matching ID
@bp.route('/v0/sublet/<int:sublet_id>', methods=['DELETE'])
@requires_auth_api
def delete_sublet(sublet_id):

    sublet = db.session.query(Sublet).get(sublet_id)
    req_id = session['user_profile']['user_id']
    if sublet is None:
        abort(404)
    if sublet.creatorid != req_id:
        abort(403)
    db.session.delete(sublet)
    db.session.commit()
    return jsonify({'delete': True})


# helper function for validating json request
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
