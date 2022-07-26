from models.tables import db, Mapping

## lock and unlock data based on geotype and region filters
def lock_unlock_data(lockStatus, geotype, region):

    ## SELECT * FROM MAPPING
    rows = db.session.query(Mapping)

    ## if geotype filters present
    if len(geotype) > 0:
        ## WHERE MAPPING.GEO_TYPE IN GEOTYPE
        rows.filter(Mapping.geo_type.in_(geotype))

    ## if region filters present
    if len(region) > 0:
        ## WHERE MAPPING.REGION IN REGION
        rows.filter(Mapping.region.in_(region))

    ## if user wants to lock the data
    if lockStatus == "lock":
        print("Locking rows..")

        ## SET LOCK_STATUS = TRUE
        rows.update({"lock_status": 1})

    ## if user wants to unlock the data
    else:
        print("Unlocking rows..")

        ## SET LOCK_STATUS = FALSE
        rows.update({"lock_status": 0})

    db.session.commit()
    db.session.close()
