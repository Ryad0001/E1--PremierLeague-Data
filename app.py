import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict
from pydantic import BaseModel
from sqlalchemy import create_engine, text

# Configuration de l'application FastAPI
app = FastAPI(title="API Premier League 2023-2024")

# Configuration de la base de données MySQL
host = "localhost"
user = "root"
password = "root"
database = "premierleague_db"

database_url=f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
engine=create_engine(database_url)


# Modèle pour représenter une équipe
class Team(BaseModel):
    position: str
    club: str
    total_played: int
    total_wins: int
    total_draws: int
    total_losses: int
    goals_for: int
    goals_against: int
    points: int

    class Config:
        orm_mode = True

@app.get("/test")
async def test():
    try:
        with engine.connect() as connexion:

            query =text( "SELECT * FROM premierleague2023_2024")
            result = connexion.execute(query)  # Récupérer toutes les équipes sous forme de dictionnaires
            df=pd.DataFrame(result.fetchall(), columns=result.keys())
            return df.to_dict(orient="records")  # Renvoie les équipes au format JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/top-teams")
async def get_top_teams():
    try:
        with engine.connect() as connexion:
            query = text("SELECT * FROM premierleague2023_2024 WHERE Points > 80")
            result = connexion.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            # Si aucune équipe ne correspond, renvoyer un message
            if df.empty:
                return {"message": "No teams found with more than 80 points."}
            
            return df.to_dict(orient="records")  # Renvoie les données au format JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-value/{club_name}")
async def get_market_value(club_name: str):
    """
    Récupère la valeur marchande d'un club spécifique.
    """
    try:
        with engine.connect() as connexion:
            query = text("""
                SELECT Club, Market_Value 
                FROM premierleague_market_values 
                WHERE Club = :club_name
            """)
            result = connexion.execute(query, {"club_name": club_name})
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            # Vérification si le club existe
            if df.empty:
                raise HTTPException(status_code=404, detail=f"Club '{club_name}' not found.")
            
            # Retourner la valeur marchande au format JSON
            return df.to_dict(orient="records")[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





