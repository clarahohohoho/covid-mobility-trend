from models.tables import db, Mobility, Mapping
from flask import jsonify, request
from modules.repository.filter import filter_mobility, filter_covid

## fetch all data points to plot on graph
def fetch_all_data():

    result = {}
    ## run common mobility filter with no geotype, region and transportation filtered
    dates, overall, driving, walking, transit = filter_mobility([], [], [], [])

    ## format response json
    result["mobility"] = {"label": dates, "values": overall}
    result["mobility_driving"] = {"label": dates, "values": driving}
    result["mobility_walking"] = {"label": dates, "values": walking}
    result["mobility_transit"] = {"label": dates, "values": transit}

    ## run common covid filter with no region filtered
    dates, new_cases = filter_covid([])

    result["covid"] = {"label": dates, "values": new_cases}

    return jsonify(result)


## fetch all values in multiselect filters
def fetch_filter_values():

    res = {}
    geotype = []
    transportation = []
    region = []

    ## SELECT DISTINCT GEO_TYPE FROM MAPPING
    rows = db.session.query(Mapping.geo_type).distinct()
    for row in rows:
        geotype.append(row[0])
    res["geotype"] = geotype

    ## SELECT DISTINCT TRANSPORTATION_TYPE FROM MAPPING
    rows = db.session.query(Mapping.transportation_type).distinct()
    for row in rows:
        transportation.append(row[0])
    res["transportation"] = transportation

    ## SELECT DISTINCT REGION FROM MAPPING
    rows = db.session.query(Mapping.region).distinct()
    for row in rows:
        region.append(row[0])
    res["region"] = region

    db.session.close()

    return jsonify(res)


## fetch filtered data points based on multiselect filters to plot on graph
def fetch_filtered():

    result = {}

    ## get selected multiselect filter values
    data = request.get_json()
    geotype = data["geotype"]
    region = data["region"]
    transportation = data["transportation"]

    ## run common mobility data filter with selected filter values
    dates, overall, driving, walking, transit = filter_mobility(
        geotype, region, transportation, []
    )

    ## format response json
    result["mobility"] = {"label": dates, "values": overall}
    result["mobility_driving"] = {"label": dates, "values": driving}
    result["mobility_walking"] = {"label": dates, "values": walking}
    result["mobility_transit"] = {"label": dates, "values": transit}

    ## run common covid data filter with selected region
    dates, new_cases = filter_covid(region)

    ## format response json
    result["covid"] = {"label": dates, "values": new_cases}

    return jsonify(result)


## get filtered region data points based on provided traffic number, regions considered if have any data point in mobility_rate > x
def filter_traffic_number():

    result = {}

    mapping_ids = []
    region = []

    ## get traffic number
    data = request.get_json()
    traffic_number = data["trafficNumber"]

    ## SELECT DISTINCT (MAPPING.ID, MAPPING.REGION) FROM (MAPPING JOIN MOBILITY ON MAPPING.ID = MOBILITY.MAPPING_ID) WHERE MOBILITY.MOBILITY_RATE > x
    rows = (
        db.session.query(Mapping.id, Mapping.region)
        .join(Mobility, Mapping.id == Mobility.mapping_id)
        .filter(Mobility.mobility_rate > traffic_number)
        .distinct()
    )
    for row in rows:
        mapping_ids.append(row[0])
        region.append(row[1])

    ## if there are regions within traffic number limit
    if len(region) > 0:

        ## use generic mobility filter and filter by mapping ids
        dates, overall, driving, walking, transit = filter_mobility(
            [], [], [], mapping_ids
        )

        ## format response json
        result["mobility"] = {"label": dates, "values": overall}
        result["mobility_driving"] = {"label": dates, "values": driving}
        result["mobility_walking"] = {"label": dates, "values": walking}
        result["mobility_transit"] = {"label": dates, "values": transit}

        ## use generic covid filter and filter by region
        dates, new_cases = filter_covid(region)

        ## format response json
        result["covid"] = {"label": dates, "values": new_cases}
        result["region"] = region

    ## else if no regions within traffic number limit, return no data points
    else:
        result["mobility"] = {"label": [], "values": []}
        result["mobility_driving"] = {"label": [], "values": []}
        result["mobility_walking"] = {"label": [], "values": []}
        result["mobility_transit"] = {"label": [], "values": []}
        result["covid"] = {"label": [], "values": []}
        result["region"] = region

    return jsonify(result)
