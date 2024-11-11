"""
    id = recipe[0]
    creator = recipe[1]
    name = recipe[2]
    category = recipe[3]
    created_at = recipe[4]
    ingredients = 
    preparation_method = recipe[5]
    portions = recipe[6]
    description = recipe[7]
"""

from datetime import datetime
from typing import List
import json
import psycopg2

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from pdf_generator import PdfGenerator

app = FastAPI()

# Função para converter datetime para string
def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%d / %m / %Y') if isinstance(obj, datetime) else obj  # Converte para o formato 'YYYY-MM-DDTHH:MM:SS'
    raise TypeError("Type not serializable")

# ==== QUERIES ====
# Retorna as receitas relacionadas ao livro que sera gerado
def query_book(cur, id: int) -> tuple:
    book_query = """
    SELECT r.id
    FROM publications p
    JOIN recipes r ON p.recipe_id = r.id
    WHERE p.book_id = %s
    """
    
    cur.execute(book_query, (id, ))
    book_data = cur.fetchall()
    
    print(book_data)
    return [record[0] for record in book_data]

# Consulta SQL para buscar os dados da receita, usuário e categoria
def query_recipes( cur, ids: List[int]) -> List[tuple]:
    recipes_query = """
    SELECT 
        r.id AS id,
        u.name AS userName,
        r.name AS name,
        c.name AS categoryName,
        r.created_at AS createdAt,
        r.preparation_method AS preparationMethod,
        (SELECT 
            json_agg(
                json_build_object(
                    'amount', ir.amount,
                    'ingredientName', i.name,
                    'measurementName', m.name
                )
            )
            FROM 
                ingredients_recipe ir
            JOIN 
                ingredients i ON ir.ingredient_id = i.id
            JOIN 
                measurements m ON ir.measurement_id = m.id
            WHERE 
                ir.recipe_id = r.id
        ) AS ingredients,
        r.portions,
        r.description,
        r.is_published AS isPublished,
        r.is_rated AS isRated
    FROM 
        recipes r
    JOIN 
        users u ON r.user_id = u.id
    JOIN 
        categories c ON r.category_id = c.id
    """

    cur.execute(recipes_query)
    recipes_data = cur.fetchall()
    return recipes_data

# ==== DATABASE CONNECTION ====
# Conexão ao banco de dados PostgreSQL
def init_connection():
    try:
        return psycopg2.connect(
            database="recipes_collection",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
            client_encoding="UTF8"
        )
        print("Connection established")
    except Exception as e:
        print(f"Connection cannot be established: {e}")
        exit(1)  # Encerra o programa se a conexão falhar



@app.get("/book/{id_book}/download", response_class=FileResponse)
def get_book(id_book: int):
    conn = init_connection()
    with conn.cursor() as cur:
        # Pegando as receitas do livro que sera gerado
        ids_recipes = query_book(cur, id_book)
        print(ids_recipes)
        if not ids_recipes:
            raise HTTPException(status_code=404, detail="Not found any recipes for this book")
        
        # Armazenando as receitas relacionadas ao livro
        recipes_data = query_recipes(cur, ids_recipes)

        # Iniciando uma lista para armazenar as receitas
        book_data = []

        # Lopping para formatar as receitas para um gerar o pdf
        for recipe in recipes_data:

            recipe_data = {
                "userName": recipe[1],
                "name": recipe[2],
                "categoryName": recipe[3],
                "createdAt": convert_datetime(recipe[4]),
                "preparationMethod": recipe[5],
                "ingredients": recipe[6],  # Já está em formato JSON da consulta SQL
                "portions": recipe[7],
                "description": recipe[8],
            }
            
            book_data.append(recipe_data)
            
        print(book_data)


        # ==== PDF ====
        # Cria o PDF
        pdf = PdfGenerator()
        pdf.add_page()

        for recipe in book_data:
            pdf.add_recipe(recipe)
            
        pdf_output_path = 'receitas.pdf'
        pdf.output(pdf_output_path)

    headers = {'Content-Disposition': 'attachment; filename="receitas.pdf"'}
    return FileResponse(pdf_output_path, media_type="application/pdf", headers=headers)
