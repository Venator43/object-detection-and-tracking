from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from repository import get_all_detected, get_range_detected, get_latest_detected, get_area_detected, get_area_detected, insert_polygon, delete_polygon, update_polygon, insert_count, get_latest_detected_area, get_all_count, get_area_count

app = FastAPI(
    title="Your API Name",
    description="Your API Description",
    version="0.1.0"
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["content-disposition"]
) 


@app.get("/api/count/")
async def get_count_for_all_area():
    rows = get_all_count()
    return {"data": rows}

@app.get("/api/count/area")
async def get_count_for_all_area(id_polygon):
    rows = get_area_count(id_polygon)
    return {"data": rows}

@app.get("/api/stats/")
async def get_stats_for_all_area():
    rows = get_all_detected()
    return {"data": rows}

@app.get("/api/stats/area")
async def get_stats_area(id_polygon):
    rows = get_area_detected(id_polygon)
    return {"data": rows}

@app.get("/api/stats/range")
async def get_stats_for_all_area_in_range(from_date: datetime, to_date: datetime):
    rows = get_range_detected(from_date, to_date)
    return {"data": rows}

@app.get("/api/stats/live")
async def get_top_n_live_stats(limit: int = 5):
    rows = get_latest_detected(limit)
    return {"data": rows}

@app.get("/api/stats/live/area")
async def get_top_n_live_stats_for_area(id_polygon, limit: int = 5):
    rows = get_latest_detected_area(id_polygon, limit)
    return {"data": rows}

@app.put("/api/config/area")
async def update_polygon_area(id_polygon, name_polygon, pts1_x, pts1_y, pts2_x, pts2_y, pts3_x, pts3_y, pts4_x, pts4_y):
    update_status = update_polygon(id_polygon, name_polygon, pts1_x, pts1_y, pts2_x, pts2_y, pts3_x, pts3_y, pts4_x, pts4_y)
    return {"status": update_status}

@app.post("/api/config/area")
async def create_new_polygon_area(name_polygon, pts1_x, pts1_y, pts2_x, pts2_y, pts3_x, pts3_y, pts4_x, pts4_y):
    insert_status = insert_polygon(name_polygon, pts1_x, pts1_y, pts2_x, pts2_y, pts3_x, pts3_y, pts4_x, pts4_y)
    
    insert_status = insert_count(insert_status, 0, 0)
    
    return {"status": insert_status}

@app.delete("/api/config/area")
async def delete_polygon_area(id_polygon):
    delete_status = delete_polygon(id_polygon)
    return {"status": delete_status}

if __name__ ==  "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8002, reload=True)