from fastapi import FastAPI
import os 
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Tomamos las variables de entorno y le damos un valor por defecto de respaldo
user = os.getenv("POSTGRES_USER", "admin")
password = os.getenv("POSTGRES_PASSWORD", "password")
host = os.getenv("POSTGRES_HOST", "postgres")
db_name = os.getenv("POSTGRES_DB", "my_db")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
engine = create_engine(DATABASE_URL)

class Moto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    brand: str = Field(index=True)
    model: str
    stock: bool = True

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.on_event("startup")
def on_startup():
    # un print para verificar la base de datos
    print(f"--- CONECTANDO A: {host} | DB: {db_name} ---")
    SQLModel.metadata.create_all(engine)

    # Comprobamos si ya existe para no duplicar en cada inicio
    with Session(engine) as session:
        busqueda = select(Moto)
        resultado = session.exec(busqueda).first() 
        
        if not resultado:
            moto1 = Moto(brand="Yamaha", model="MT-07", stock=True)
            moto2 = Moto(brand="Honda", model="CBR500R", stock=False)
            
            session.add(moto1)
            session.add(moto2)
            session.commit()
            print("Lista de ejemplo creada")
@app.get("/motos", response_model=List[Moto]) 
def get_motos(): 
    with Session(engine) as session:
        vista = select(Moto)
        motos = session.exec(vista).all()
    return motos

@app.post("/motos", response_model=Moto)
def crear_moto(moto: Moto):
    with Session(engine) as session:
        session.add(moto)
        session.commit()
        session.refresh(moto)
        return moto