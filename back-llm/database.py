from datetime import date

from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Date, ForeignKey, insert, delete
)

# ---------- Bootstrap: create DB and data dummy -----------------
def bootstrap_db():
    engine = create_engine("postgresql://postgres:password@localhost:5432/sales_db")
    meta = MetaData()

    meta.drop_all(engine)

    attendants = Table(
        "attendants", meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String, unique=True, nullable=False),
    )
    sales = Table(
        "sales", meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("attendant_id", Integer, ForeignKey("attendants.id")),
        Column("sale_date", Date),
        Column("amount", Integer),
    )
    meta.create_all(engine)

    today = date.today()
    with engine.begin() as conn:
        conn.execute(delete(sales))
        conn.execute(delete(attendants))

    with engine.begin() as conn:   
        conn.execute(insert(attendants), [
            {"name": "João"}, {"name": "Maria"}, {"name": "Carlos"},
        ])
        conn.execute(insert(sales), [
            {"attendant_id": 1, "sale_date": today, "amount": 200},
            {"attendant_id": 2, "sale_date": today, "amount": 300},
            {"attendant_id": 3, "sale_date": today, "amount": 50},
        ])