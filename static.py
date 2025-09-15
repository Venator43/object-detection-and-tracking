import cv2 as cv
import requests
import m3u8
import time
import io
import tempfile
from datetime import datetime
import uuid
from urllib.parse import urljoin

import ultralytics
import numpy as np

from ultralytics import solutions
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from db import engine, Polygon, DetectedPolygon, CountPolygon
from repository import get_all_polygon, insert_detected

model = ultralytics.RTDETR("rtdetr-x.pt")  # load an official model

video_path = "background video _ people _ walking _.mp4"

out = get_all_polygon()

polygon = []
polygon_metadata = []

count_in = []
count_out = []

for poly in out:
    region = [(poly.pts1_x, poly.pts1_y), (poly.pts2_x, poly.pts2_y), (poly.pts3_x, poly.pts3_y), (poly.pts4_x, poly.pts4_y),]
    
    polygon.append(np.array(region, np.int32))
    polygon_metadata.append({
        "id_polygon": poly.id_polygon,
        "name_polygon": poly.name_polygon
    })
    count_in.append(0)
    count_out.append(0)
# region1 = [(590, 490), (580, 680), (950, 640), (930, 470)]
# region2 = [(120, 430), (350, 430), (300, 630), (50, 590)]

# polygon = [np.array(region1, np.int32), np.array(region2, np.int32)]

track_states = {}

cap = cv.VideoCapture(video_path)
frame_count = 0
while cap.isOpened():
    status, frame = cap.read()
    prediction = model.track(frame, stream_buffer = True, classes = [0], persist=True, device='cuda', tracker="bytetrack.yaml")
    
    frame = prediction[0].plot()
    
    cv.polylines(frame,polygon,True,(0,255,255))

    #Check for lost or missing track, if the lost track previously inside the polygon area, remove it from tracked states
    if frame_count % 30 == 0:
        lost_tracker = model.predictor.trackers[0].lost_stracks
        for lost in lost_tracker:
            print(lost.track_id)
            lost_id = lost.track_id
            if lost_id in track_states:
                insert_detected(id_polygon=track_states[lost_id][1]+1, uuid_object=track_states[lost_id][0], time_in=track_states[lost_id][-1], time_out=datetime.now())            
                print("test")
                count_out[i] += 1
                del track_states[lost_id]
        
        session = Session(engine)
        for i, pts in enumerate(polygon):
            update_statement = update(CountPolygon).where(CountPolygon.id_polygon == polygon_metadata[i]["id_polygon"]).values(
                count_in = CountPolygon.count_in + count_in[i],
                count_out = CountPolygon.count_out + count_out[i]
            )
            results = session.execute(update_statement)
            session.commit()

            count_in[i] = 0
            count_out[i] = 0

        session.close()
    if frame_count % 60 == 0:
        out = get_all_polygon()

        polygon = []
        polygon_metadata = []
        
        count_in = []
        count_out = []
        
        for poly in out:
            region = [(poly.pts1_x, poly.pts1_y), (poly.pts2_x, poly.pts2_y), (poly.pts3_x, poly.pts3_y), (poly.pts4_x, poly.pts4_y),]
            
            polygon.append(np.array(region, np.int32))
            polygon_metadata.append({
                "id_polygon": poly.id_polygon,
                "name_polygon": poly.name_polygon
            })
            count_in.append(0)
            count_out.append(0)

                        
    for i, pts in enumerate(polygon):
        for box in prediction[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            centerX, centerY = (x1 + x2) // 2, (y1 + y2) // 2

            cv.circle(frame, (centerX, centerY), 5, (0, 0, 255), -1)
            
            #Check if object inside the polygon area
            is_inside = cv.pointPolygonTest(pts, (centerX, centerY), False) >= 0

            try:
                track_id = int(box.id.item())
            except:
                continue
            
            if not is_inside:
                #Check if previous tracked object has exit polygon area
                if track_id in track_states:
                    if track_states[track_id][1] == (polygon_metadata[i]["id_polygon"]-1):
                        insert_detected(id_polygon=track_states[track_id][1]+1, uuid_object=track_states[track_id][0], time_in=track_states[track_id][-2], time_out=datetime.now())
                        print("test")
                        del track_states[track_id]
                        count_out[i] += 1
                continue

            if box.id is None:
                continue
            
            #If new object enter the area, assign a tracker status
            if track_id not in track_states:
                track_states[track_id] = [uuid.uuid4(), polygon_metadata[i]["id_polygon"]-1, datetime.now()]
                count_in[i] += 1

            cv.putText(frame, "Alert", (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            print(track_states)
    if status:
        cv.imshow("Frame", frame)
        frame_count += 1
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        if cv.waitKey(1) & 0xFF == ord('w'):
            print("test")
            polygon[1] = np.array([(220, 150), (320, 170), (250, 250), (120, 230)], np.int32)
    else:
        break