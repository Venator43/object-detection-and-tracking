from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from db import engine, Polygon, DetectedPolygon, CountPolygon
from datetime import datetime

def get_all_polygon():
    session = Session(engine)
    select_statment = select(Polygon)
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def insert_polygon(name_polygon, pts1_x, pts1_y, pts2_x, pts2_y, pts3_x, pts3_y, pts4_x, pts4_y):
    try:
        session = Session(engine)
        insert_statment = insert(Polygon).values(
            name_polygon = name_polygon,
            pts1_x = pts1_x,
            pts1_y = pts1_y,
            pts2_x = pts2_x,
            pts2_y = pts2_y,
            pts3_x = pts3_x,
            pts3_y = pts3_y,
            pts4_x = pts4_x,
            pts4_y = pts4_y
        )
        results = session.execute(insert_statment)
        inserted_id = results.lastrowid
        session.commit()

        session.close()

        return inserted_id
    except Exception as e:
        print("Error while executing query ", e)
        return False

def update_polygon(id_polygon, **kwargs):
    try:
        session = Session(engine)
        
        values = {rows: value for rows, value in kwargs.items() if value is not None}
        update_statment = update(Polygon).where(Polygon.id_polygon == id_polygon).values(
            values
        )
        results = session.execute(update_statement)
        session.commit()

        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False

def delete_polygon(id_polygon):
    session = Session(engine)

    try:
        delete_statment = delete(Polygon).where(Polygon.id_polygon.__eq__(id_polygon))

        session.execute(delete_statment)
        session.commit()
        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False

def get_all_count():
    session = Session(engine)
    select_statment = select(CountPolygon)
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def get_area_count(id_polygon):
    session = Session(engine)
    select_statment = select(CountPolygon).where(CountPolygon.id_polygon.__eq__(id_polygon))
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def insert_count(id_polygon, count_in, count_out):
    try:
        session = Session(engine)
        insert_statment = insert(CountPolygon).values(
            id_polygon = id_polygon,
            count_in = count_in,
            count_out = count_out
        )
        results = session.execute(insert_statment)
        session.commit()

        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False

def update_count(id_count, **kwargs):
    try:
        session = Session(engine)
        
        values = {rows: value for rows, value in kwargs.items() if value is not None}
        update_statment = update(CountPolygon).where(CountPolygon.id_count == id_count).values(
            values
        )
        results = session.execute(update_statement)
        session.commit()

        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False

def delete_count(id_count):
    session = Session(engine)

    try:
        delete_statment = delete(CountPolygon).where(CountPolygon.id_count.__eq__(id_count))

        session.execute(delete_statment)
        session.commit()
        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False

def get_all_detected():
    session = Session(engine)
    select_statment = select(DetectedPolygon)
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def get_area_detected(id_polygon):
    session = Session(engine)
    select_statment = select(DetectedPolygon).where(DetectedPolygon.id_polygon == id_polygon)
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def get_latest_detected(limit=5):
    session = Session(engine)
    select_statment = select(DetectedPolygon).order_by(DetectedPolygon.id_detected.desc()).limit(5)
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def get_latest_detected_area(id_polygon, limit=5):
    session = Session(engine)
    select_statment = select(DetectedPolygon).where(DetectedPolygon.id_polygon == id_polygon).order_by(DetectedPolygon.id_detected.desc()).limit(5)
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def get_range_detected(from_date: datetime, to_date: datetime):
    session = Session(engine)
    select_statment = select(DetectedPolygon).where(DetectedPolygon.time_in >= from_date, DetectedPolygon.time_in <= to_date)
    out = [res for res in session.scalars(select_statment)]
    session.close()

    return out

def insert_detected(id_polygon, uuid_object, time_in, time_out):
    try:
        session = Session(engine)
        insert_statment = insert(DetectedPolygon).values(
            id_polygon = id_polygon,
            uuid_object = uuid_object,
            time_in = time_in,
            time_out = time_out
        )
        results = session.execute(insert_statment)
        session.commit()

        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False

def update_detected(id_detected, **kwargs):
    try:
        session = Session(engine)
        
        values = {rows: value for rows, value in kwargs.items() if value is not None}
        update_statment = update(DetectedPolygon).where(DetectedPolygon.id_detected == id_detected).values(
            values
        )
        results = session.execute(update_statement)
        session.commit()

        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False

def delete_detected(id_detected):
    session = Session(engine)

    try:
        delete_statment = delete(DetectedPolygon).where(DetectedPolygon.id_detected.__eq__(id_detected))

        session.execute(delete_statment)
        session.commit()
        session.close()

        return True
    except Exception as e:
        print("Error while executing query ", e)
        return False