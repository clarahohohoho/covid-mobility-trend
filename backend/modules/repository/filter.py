from models.tables import db, Mobility, Mapping, Covid
from sqlalchemy import func

## generic filter for mobility data
def filter_mobility(geotype, region, transportation, mapping_ids):

    ## SELECT (YEAR(MOBILITY.DATE), MONTH(MOBILITY.DATE), SUM(MOBILITY.MOBILITY_RATE), MAPPING.TRANSPORTATION_TYPE) FROM MOBILITY JOIN MAPPING ON MOBILITY.MAPPING_ID = MAPPING.ID
    rows = db.session.query(
        func.month(Mobility.date),
        func.year(Mobility.date),
        func.sum(Mobility.mobility_rate),
        Mapping.transportation_type,
    ).join(Mapping, Mapping.id == Mobility.mapping_id)

    ## if geotype filter present
    if len(geotype) > 0:
        ## WHERE MAPPING.GEO_TYPE IN GEOTYPE
        rows = rows.filter(Mapping.geo_type.in_(geotype))

    ## if region filter present
    if len(region) > 0:
        ## WHERE MAPPING.REGION IN REGION
        rows = rows.filter(Mapping.region.in_(region))

    ## if transportation filter present
    if len(transportation) > 0:
        ## WHERE MAPPING.TRANSPORTATION_TYPE IN TRANSPORTATION
        rows = rows.filter(Mapping.transportation_type.in_(transportation))

    ## if mapping ids filters present (only for traffic number filter)
    if len(mapping_ids) > 0:
        ## WHERE MOBILITY.MAPPING_ID IN MAPPING_IDS
        rows = rows.filter(Mobility.mapping_id.in_(mapping_ids))

    ## GROUP BY (YEAR(MOBILITY.DATE), MONTH(MOBILITY.DATE), MAPPING.TRANSPORTATION_TYPE) ORDER BY (YEAR(MOBILITY.DATE), MONTH(MOBILITY.DATE))
    rows = rows.group_by(
        func.year(Mobility.date), func.month(Mobility.date), Mapping.transportation_type
    ).order_by(func.year(Mobility.date), func.month(Mobility.date))

    ## format output lists from query result
    dates = []
    mobility_rate_overall = []
    mobility_rate_driving = []
    mobility_rate_walking = []
    mobility_rate_transit = []

    for row in rows:
        ## if current date of query is not already in output dates list
        if str(row[0]) + "-" + str(row[1]) not in dates:
            ## take MM-YYYY
            dates.append(str(row[0]) + "-" + str(row[1]))

        ## if transportation_type = DRIVING, add it to driving output values list
        if row[3] == "driving":
            mobility_rate_driving.append(row[2])

        ## if transportation_type = WALKING, add it to walking output values list
        elif row[3] == "walking":
            mobility_rate_walking.append(row[2])

        ## if transportation_type = TRANSIT, add it to transit output values list
        elif row[3] == "transit":
            mobility_rate_transit.append(row[2])

    ## getting numbers for overall mobility values by adding up all transportation types values
    for i in range(len(dates)):
        number = 0
        if len(mobility_rate_driving) > 0:
            number += mobility_rate_driving[i]
        if len(mobility_rate_transit) > 0:
            number += mobility_rate_transit[i]
        if len(mobility_rate_walking) > 0:
            number += mobility_rate_walking[i]
        mobility_rate_overall.append(number)

    db.session.close()

    return (
        dates,
        mobility_rate_overall,
        mobility_rate_driving,
        mobility_rate_walking,
        mobility_rate_transit,
    )

## generic filter for covid data
def filter_covid(region):

    ## SELECT YEAR(DATE), MONTH(DATE), SUM(NEW_CASES) WHERE "2020-01-13" <= DATE <= "2021-07-27"
    rows = db.session.query(
        func.year(Covid.date),
        func.month(Covid.date),
        func.sum(Covid.new_cases),
    ).filter(Covid.date >= "2020-01-13", Covid.date <= "2021-07-27")

    ## if region filter is present
    if len(region) > 0:
        ## WHERE LOCATION IN REGION
        rows = rows.filter(Covid.location.in_(region))

    ## GROUP BY YEAR(DATE), MONTH(DATE) ORDER BY YEAR(DATE), MONTH(DATE)
    rows = rows.group_by(func.year(Covid.date), func.month(Covid.date)).order_by(
        func.year(Covid.date), func.month(Covid.date)
    )

    ## format output values lists
    dates = []
    new_cases = []

    for row in rows:
        ## format dates to MM-YY
        dates.append(str(row[0]) + "-" + str(row[1]))
        new_cases.append(row[2])

    return dates, new_cases
