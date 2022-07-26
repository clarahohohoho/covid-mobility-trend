from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Mobility(db.Model):
    __tablename__ = "mobility"

    mobility_id = db.Column(db.Integer, primary_key=True)
    mapping_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    mobility_rate = db.Column(db.Float)

    @property
    def serialize(self):
        return {
            "mobility_id": self.mobility_id,
            "mapping_id": self.mapping_id,
            "date": self.date,
            "mobility_rate": self.mobility_rate,
        }


class Mapping(db.Model):
    __tablename__ = "mapping"
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(120))
    alternative_name = db.Column(db.String(120))
    country = db.Column(db.String(120))
    geo_type = db.Column(db.String(120))
    sub_region = db.Column(db.String(120))
    transportation_type = db.Column(db.String(120))
    lock_status = db.Column(db.Boolean)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "region": self.region,
            "alternative_name": self.alternative_name,
            "country": self.country,
            "geo_type": self.geo_type,
            "sub_region": self.sub_region,
            "transportation_type": self.transportation_type,
            "lock_status": self.lock_status,
        }


class Covid(db.Model):
    __tablename__ = "covid"

    id = db.Column(db.Integer, primary_key=True)
    iso_code = db.Column(db.String(120))
    continent = db.Column(db.String(120))
    location = db.Column(db.String(120))
    date = db.Column(db.Date)
    total_cases = db.Column(db.Float)
    new_cases = db.Column(db.Float)

    @property
    def serialize(self):
        return {
            "iso_code": self.iso_code,
            "continent": self.continent,
            "location": self.location,
            "date": self.date,
            "total_cases": self.total_cases,
            "new_cases": self.new_cases,
        }
