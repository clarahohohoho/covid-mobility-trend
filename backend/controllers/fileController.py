from models.tables import db, Mobility, Mapping
from flask import jsonify, request, send_file
import json
import csv
from modules.repository.update_rows import updated_rows
from modules.repository.lock_unlock_data import lock_unlock_data

import pandas as pd


## function to create download file and send to user for download
def download_file():

    ## get geotype and region filter values
    geotype = json.loads(request.args.get("geotype"))
    region = json.loads(request.args.get("region"))

    ## SELECT (MOBILITY.*, MAPPING.*[~~everything except id~~]) FROM MAPPING JOIN MOBILITY ON MAPPING.ID = MOBILITY.MAPPING_ID
    rows = db.session.query(
        Mobility.mobility_id,
        Mobility.mapping_id,
        Mobility.date,
        Mobility.mobility_rate,
        Mapping.region,
        Mapping.alternative_name,
        Mapping.country,
        Mapping.geo_type,
        Mapping.sub_region,
        Mapping.transportation_type,
    ).join(Mapping, Mapping.id == Mobility.mapping_id)

    ## if provided geotype filter
    if len(geotype) > 0:
        ## WHERE MAPPING.GEO_TYPE IN GEOTYPE
        rows = rows.filter(Mapping.geo_type.in_(geotype))

    ## if provided region filter
    if len(region) > 0:
        ## WHERE MAPPING.REGION IN REGION
        rows = rows.filter(Mapping.region.in_(region))

    ## ORDER BY MOBLITY.DATE
    rows = rows.order_by(Mobility.date)

    ## create csv file in temporary file location within server
    with open("../data/download.csv", "w") as s_key:
        ## write output to csv
        csv_out = csv.writer(s_key)
        csv_out.writerow(rows.statement.columns.keys())
        for i in rows:
            csv_out.writerow(i)

    db.session.close()

    return send_file(
        "../data/download.csv",
        mimetype="text/csv",
        download_name="download.csv",
        as_attachment=True,
    )


## receive and ingest upload file
def upload_file():

    ## get geotype, region, traffic upload limit filter values from UI
    upFile = request.files["file"]
    geotype = json.loads(request.form.get("geotype"))
    region = json.loads(request.form.get("region"))
    trafficLimit = request.form.get("trafficLimit")

    ## flag to use if user indicates continue upload after warning traffic upload limit has crossed
    override = request.form.get("override")

    ## read upload csv file into pandas
    df = pd.read_csv(upFile)

    ## if this is user's first time going through upload function, check in df if any mobility_rate > trafficLimit
    if override == "false":
        aboveTrafficLimit = (df["mobility_rate"] > int(trafficLimit)).any()

        ## if df contains any data point of moblity_rate > x
        if aboveTrafficLimit:
            ## return false response for frontend to ingest and reroute
            response = {"response": "false"}
            return jsonify(response)

    ## if data does not cross traffic limit or if user indicated to proceed with upload
    try:
        ## run update function
        updated_rows(df)
    except:
        ## if update fails, it is due to invalid mapping combination due to edits made by user
        return jsonify(
            {
                "response": "Error: geotype, region and transportation type combination is not valid. Please try again."
            }
        )

    response = {"response": "true"}
    return jsonify(response)


## lock and unlock filtered data
def lock_filter_data():

    ## get filter values from multiselect filters and if user wants to lock/unlock
    data = request.get_json()
    lockStatus = data["lockStatus"]
    geotype = data["geotype"]
    region = data["region"]

    ## run lock/unlock function based on filtered values from multiselect
    lock_unlock_data(lockStatus, geotype, region)

    return jsonify({"lockStatus": lockStatus})

