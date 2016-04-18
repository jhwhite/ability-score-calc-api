from flask import Flask, jsonify, abort, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from marshmallow import Schema, fields, ValidationError, pre_load
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jwhite@localhost/ability_score_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class AbilityScorePoint(db.Model):
    abilityscorepointid = db.Column(db.Integer, primary_key=True)
    campaigntype = db.Column(db.String(20), unique=True)
    points = db.Column(db.Integer)

    
class BonusSpell(db.Model):
    bonusspellid = db.Column(db.Integer, primary_key=True)
    abilitymodifier = db.Column(db.Integer, unique=True)
    firstlevel = db.Column(db.Integer)
    secondlevel = db.Column(db.Integer)
    thirdlevel = db.Column(db.Integer)
    fourthlevel = db.Column(db.Integer)
    fifthlevel = db.Column(db.Integer)
    sixthlevel = db.Column(db.Integer)
    seventhlevel = db.Column(db.Integer)
    eighthlevel = db.Column(db.Integer)
    ninthlevel = db.Column(db.Integer)


class CarryingCapacity(db.Model):
    carrying_capacity_id = db.Column(db.Integer, primary_key=True)
    strength_score = db.Column(db.Integer)
    light_load = db.Column(db.String(20))
    medium_load = db.Column(db.String(20))
    heavy_load = db.Column(db.String(20))


class Races(db.Model):
    race_id = db.Column(db.Integer, primary_key=True)
    race = db.Column(db.String(20))
    description = db.Column(db.String(1000))
    points = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

    
class AbilityScorePointSchema(Schema):
    abilityscorepointid = fields.Int(dump_only=True)
    campaigntype = fields.Str()
    points = fields.Int(dump_only=True)

    
class BonusSpellSchema(Schema):
    bonusspellid = fields.Int(dump_only=True)
    abilitymodifier = fields.Int(dump_only=True)
    firstlevel = fields.Int(dump_only=True)
    secondlevel = fields.Int(dump_only=True)
    thirdlevel = fields.Int(dump_only=True)
    fourthlevel = fields.Int(dump_only=True)
    fifthlevel = fields.Int(dump_only=True)
    sixthlevel = fields.Int(dump_only=True)
    seventhlevel = fields.Int(dump_only=True)
    eighthlevel = fields.Int(dump_only=True)
    ninthlevel = fields.Int(dump_only=True)


class CarryingCapacitySchema(Schema):
    carrying_capacity_id = fields.Int(dump_only=True)
    strength_score = fields.Int(dump_only=True)
    light_load = fields.Str()
    medium_load = fields.Str()
    heavy_load = fields.Str()


class RaceSchema(Schema):
    race_id = fields.Int(dump_only=True)
    race = fields.Str()
    description = fields.String()
    points = fields.Int(dump_only=True)
    strength = fields.Int(dump_only=True)
    dexterity = fields.Int(dump_only=True)
    constitution = fields.Int(dump_only=True)
    intelligence = fields.Int(dump_only=True)
    wisdom = fields.Int(dump_only=True)
    charisma = fields.Int(dump_only=True)

    
ability_score_points_schema = AbilityScorePointSchema(many=True)
bonus_spells_schema = BonusSpellSchema(many=True)
bonus_spell_schema = BonusSpellSchema()
carrying_capacities_schema = CarryingCapacitySchema(many=True)
carrying_capacity_schema = CarryingCapacitySchema()
races_schema = RaceSchema(many=True)
race_schema = RaceSchema()

    # def __init__(self, campaigntype, points):
    #     self.campaigntype = campaigntype
    #     self.points = points


def calculate_ability_mod(ability_score):
    return math.floor((ability_score - 10) / 2)


def calculate_points(ability_score):
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45].index(ability_score)
    point_array = [0, 0, 0, 0, 0, 0, -4, -2, -1, 0, 1, 2, 3, 5, 7, 10, 13, 17, 0, 0]

    return point_array[index]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/ability-score-points', methods=['GET'])
def get_ability_score_points():
    ability_score_points = AbilityScorePoint.query.all()
    result = ability_score_points_schema.dump(ability_score_points)
    return jsonify({'ability_score_points': result.data})


@app.route('/bonus-spells', methods=['GET'])
def get_bonus_spells():
    bonus_spells = BonusSpell.query.all()
    result = bonus_spells_schema.dump(bonus_spells)
    return jsonify({'bonus_spells': result.data})


@app.route('/bonus-spell/<int:ability_modifier>', methods=['GET'])
def get_bonus_spell(ability_modifier):
    min_mod = db.session.query(func.min(BonusSpell.abilitymodifier)).scalar()
    max_mod = db.session.query(func.max(BonusSpell.abilitymodifier)).scalar()

    if ability_modifier < min_mod or ability_modifier > max_mod:
        abort(404)

    bonus_spell = BonusSpell.query.filter_by(abilitymodifier=ability_modifier).first()
    result = bonus_spell_schema.dump(bonus_spell)
    return jsonify({'bonus_spell': result.data})


@app.route('/carrying-capacity/<int:ability_score>', methods=['GET'])
def get_carrying_capacity(ability_score):
    min_strength_score = db.session.query(func.min(CarryingCapacity.strength_score)).scalar()
    max_strength_score = db.session.query(func.max(CarryingCapacity.strength_score)).scalar()
    if ability_score < min_strength_score or ability_score > max_strength_score:
        abort(404)

    carrying_capacity = CarryingCapacity.query.filter_by(strength_score=ability_score).first()
    result = carrying_capacity_schema.dump(carrying_capacity)
    return jsonify({'carrying_capacity': result.data})


@app.route('/carrying-capacities', methods=['GET'])
def get_carrying_capacities():
    carrying_capacities = CarryingCapacity.query.all()
    result = carrying_capacities_schema.dump(carrying_capacities)
    return jsonify({'carrying_capacities': result.data})


@app.route('/calculate-ability-mod/<int:ability_score>', methods=['GET'])
def calculate_ability_score(ability_score):
    mod = calculate_ability_mod(ability_score)
    points = calculate_points(ability_score)

    carrying_capacity = CarryingCapacity.query.filter_by(strength_score=ability_score).first()
    result = carrying_capacity_schema.dump(carrying_capacity)

    bonus_spell = BonusSpell.query.filter_by(abilitymodifier=mod).first()
    bs = bonus_spell_schema.dump(bonus_spell)

    return jsonify({'mod': mod, 'points': points, 'carrying_capacity': result.data, 'bonus_spells': bs})


@app.route('/races', methods=['GET'])
def get_races():
    races = Races.query.all()
    result = races_schema.dump(races)

    return jsonify({'races': result.data})


@app.route('/race/<string:race>', methods=['GET'])
def get_race(race):
    r = Races.query.filter(func.lower(Races.race) == race.lower()).first()
    result = race_schema.dump(r)

    return jsonify({'race': result.data})

    
if __name__ == '__main__':
    app.run(debug=True)
