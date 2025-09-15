import cv2 as cv
import requests
import m3u8
import time
import io
import tempfile
import uuid
from urllib.parse import urljoin
from datetime import datetime

import ultralytics
import numpy as np

from ultralytics import solutions
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from db import engine, Polygon, DetectedPolygon, CountPolygon
from repository import get_all_polygon, insert_detected

model = ultralytics.RTDETR("rtdetr-x.pt")  # load an official model

url = "https://pelindung.bandung.go.id:3443/video/DAHUA/BUB.m3u8"
continue_stream = True

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

while continue_stream == True:
    playlist = m3u8.load(url)
    for segment in playlist.segments:
        segment_url = urljoin(url, segment.uri)
        try:
            response = requests.get(segment_url, stream=True, timeout=10)
            if response.status_code == 200:
                video_buffer = io.BytesIO()

                for chunk in response.iter_content(chunk_size=8192):
                    video_buffer.write(chunk)

                video_buffer.seek(0)

                with tempfile.NamedTemporaryFile(suffix='.ts', delete=False) as temp_file:
                    temp_file.write(video_buffer.getvalue())
                    temp_file_path = temp_file.name

                cap = cv.VideoCapture(temp_file_path)
                frame_count = 0
                while cap.isOpened():
                    status, frame = cap.read()
                    prediction = model.track(frame, stream_buffer = True, classes = [0], persist=True, tracker="bytetrack.yaml")

                    frame = prediction[0].plot()

                    cv.polylines(frame,polygon,True,(0,255,255))

                    #Check for lost or missing track, if the lost track previously inside the polygon area, remove it from tracked states
                    if frame_count % 30 == 0:
                        lost_tracker = model.predictor.trackers[0].lost_stracks
                        for lost in lost_tracker:
                            # print(lost.track_id)
                            lost_id = lost.track_id
                            if lost_id in track_states:
                                insert_detected(id_polygon=track_states[lost_id][1]+1, uuid_object=track_states[lost_id][0], time_in=track_states[lost_id][-1], time_out=datetime.now())
                                # print("test")
                                count_out[track_states[lost_id][-1]] += 1
                                del track_states[lost_id]

                        session = Session(engine)
                        for i, pts in enumerate(polygon):
                            # print("===========")
                            # print(polygon_metadata[i]["id_polygon"])
                            # print(count_in[i])
                            # print(count_out[i])
                            # print("=====+=====")
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

                    for ii, pts in enumerate(polygon):
                        print(ii)
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
                                    if track_states[track_id][1] == (polygon_metadata[ii]["id_polygon"]-1):
                                        insert_detected(id_polygon=track_states[track_id][1]+1, uuid_object=track_states[track_id][0], time_in=track_states[track_id][-2], time_out=datetime.now())
                                        # print("test")
                                        del track_states[track_id]
                                        count_out[ii] += 1
                                        # print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
                                        # print(ii)
                                        # print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
                                continue

                            if box.id is None:
                                continue

                            #If new object enter the area, assign a tracker status
                            if track_id not in track_states:
                                # print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                # print(ii)
                                # print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                track_states[track_id] = [uuid.uuid4(), polygon_metadata[ii]["id_polygon"]-1, datetime.now(), ii]
                                count_in[ii] += 1

                            cv.putText(frame, "Alert", (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                            # print(count_in)
                            # print(count_out)
                    if status:
                        cv.imshow("Frame", frame)
                        if cv.waitKey(1) & 0xFF == ord('w'):
                            continue_stream=False
                            break
                    else:
                        break
                if continue_stream == False:
                    break
        except Exception as e:
            print("Error while streaming:", e)
            continue
        if continue_stream == False:
            break
    if continue_stream == False:
        break