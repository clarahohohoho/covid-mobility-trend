from sqlalchemy import case

from models.tables import db, Mobility, Mapping

## update rows based on uploaded file
def updated_rows(df):

    payload_mobilityrate = {}
    payload_date = {}
    payload_mappingid = {}

    ## SELECT ID FROM MAPPING WHERE LOCK_STATUS = FALSE
    unlocked = db.session.query(Mapping.id).filter(Mapping.lock_status == 0)

    ## store all unlocked mapping_id in list
    unlocked_ids = [unlocked_id[0] for unlocked_id in unlocked]

    ## filter out only rows in upload file that contains unlocked mapping_id
    df = df[df["mapping_id"].isin(unlocked_ids)]

    ## if there are data to be uploaded from resultant df
    if len(df) > 0:
        ## iterate through df
        for i, row in df.iterrows():
            print("inserting row")

            ## set mobility_id: mobility_rate in payload_mobilityrate dict
            payload_mobilityrate[row["mobility_id"]] = row["mobility_rate"]
            ## set mobility_id: date in payload_date dict
            payload_date[row["mobility_id"]] = row["date"]

            ## find out id from mapping table with region, geo_type and transportation_type
            ids = db.session.query(Mapping.id).filter(
                Mapping.region == row["region"],
                Mapping.geo_type == row["geo_type"],
                Mapping.transportation_type == row["transportation_type"],
            )
            ## set resultant id as id, as expected 1-1 matching, there should only be 1 query result
            id = [id[0] for id in ids][0]

            ## set mobility_id: id in payload_mappingid dict
            payload_mappingid[row["mobility_id"]] = id


        ## update mapping_id to mobility_id based on payload_mappingid dict
        db.session.query(Mobility).filter(
            Mobility.mobility_id.in_(payload_mappingid)
        ).update(
            {
                Mobility.mapping_id: case(
                    payload_mappingid,
                    value=Mobility.mobility_id,
                )
            },
            synchronize_session=False,
        )

        db.session.commit()
        
        ## update mobility_rate to mobility_id based on payload_mobilityrate dict
        print("updating mobility rate..")
        db.session.query(Mobility).filter(
            Mobility.mobility_id.in_(payload_mobilityrate)
        ).update(
            {
                Mobility.mobility_rate: case(
                    payload_mobilityrate,
                    value=Mobility.mobility_id,
                )
            },
            synchronize_session=False,
        )

        db.session.commit()

        ## update date to mobility_id based on payload_mobilitydate dict
        print("updating date..")
        db.session.query(Mobility).filter(
            Mobility.mobility_id.in_(payload_date)
        ).update(
            {
                Mobility.date: case(
                    payload_date,
                    value=Mobility.mobility_id,
                )
            },
            synchronize_session=False,
        )

        db.session.commit()

    db.session.close()
