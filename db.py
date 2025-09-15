import sqlalchemy
import yaml

from sqlalchemy.orm import Session, declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Integer, Double, Text, select

with open("config.yaml", 'r') as config_file:
    config = yaml.safe_load(config_file)

print(config)
engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{config['DB_USERNAME']}:{config['DB_PASS']}@{config['DB_URL']}:{config['DB_PORT']}/{config['DB_NAME']}?charset=utf8mb4"
)

Base = declarative_base()

class Polygon(Base):
    __tablename__ = "polygon"

    id_polygon: Mapped[int] = mapped_column(primary_key=True)
    name_polygon: Mapped[str] = mapped_column(String(255))
    pts1_x: Mapped[int] = mapped_column(Integer(), default=0)
    pts1_y: Mapped[int] = mapped_column(Integer(), default=0)
    pts2_x: Mapped[int] = mapped_column(Integer(), default=0)
    pts2_y: Mapped[int] = mapped_column(Integer(), default=0)
    pts3_x: Mapped[int] = mapped_column(Integer(), default=0)
    pts3_y: Mapped[int] = mapped_column(Integer(), default=0)
    pts4_x: Mapped[int] = mapped_column(Integer(), default=0)
    pts4_y: Mapped[int] = mapped_column(Integer(), default=0)

class CountPolygon(Base):
    __tablename__ = "count_polygon"

    id_count: Mapped[int] = mapped_column(primary_key=True)
    id_polygon: Mapped[str] = mapped_column(
        ForeignKey("polygon.id_polygon"))
    count_in: Mapped[int] = mapped_column(Integer(), default=0)
    count_out: Mapped[int] = mapped_column(Integer(), default=0)

class DetectedPolygon(Base):
    __tablename__ = "detected_polygon"

    id_detected: Mapped[int] = mapped_column(primary_key=True)
    id_polygon: Mapped[str] = mapped_column(
        ForeignKey("polygon.id_polygon"))
    uuid_object: Mapped[str] = mapped_column(String(50))
    time_in: Mapped[DateTime] = mapped_column(DateTime)
    time_out: Mapped[DateTime] = mapped_column(DateTime)

if __name__ == "__main__":
    session = Session(engine)
    ress = select(Polygon)

    out = [res for res in session.scalars(ress)]
    session.close()

    print(out[0].name_polygon)