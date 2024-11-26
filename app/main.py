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

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import psycopg2
import os

from connection import Connection
from queries import query_recipes, query_recipe_by_id
from pdf_generator import PdfGenerator

app = FastAPI()

# Função para converter datetime para string
def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%d/%m/%Y')
    raise TypeError("Type not serializable")

@app.get("/recipes/download/{recipe_id}", response_class=FileResponse)
def download_single_recipe(recipe_id: int):
    conn = Connection.init_connection()
    try:
        with conn.cursor() as cur:
            # Obtém os detalhes de uma única receita
            recipes_data = query_recipe_by_id(cur, recipe_id)
            if not recipes_data:
                raise HTTPException(status_code=404, detail="Recipe not found")

            # Formata os dados da receita
            book_data = format_recipes_data(recipes_data)

        # Gera o PDF
        pdf_output_path = generate_pdf(book_data)
        return FileResponse(pdf_output_path, media_type="application/pdf",
                            headers={'Content-Disposition': f'attachment; filename="{os.path.basename(pdf_output_path)}"'})
    finally:
        conn.close()


@app.get("/recipes/download/", response_class=FileResponse)
def download_multiple_recipes():
    conn = Connection.init_connection()
    try:
        with conn.cursor() as cur:
            # Obtém os detalhes das receitas
            recipes_data = query_recipes(cur)
            if not recipes_data:
                raise HTTPException(status_code=404, detail="Recipes not found")

            # Formata os dados das receitas
            book_data = format_recipes_data(recipes_data)

        # Gera o PDF
        pdf_output_path = generate_pdf(book_data)
        return FileResponse(pdf_output_path, media_type="application/pdf",
                            headers={'Content-Disposition': 'attachment; filename="receitas.pdf"'})
    finally:
        conn.close()


# Função para gerar o PDF
def generate_pdf(recipe_data):
    pdf = PdfGenerator()
    pdf.add_page()
    
    if len(recipe_data) == 1:
        pdf_title = recipe_data[0]['name']
    else:
        # Combine os nomes das receitas (limite o tamanho para evitar nomes muito longos)
        pdf_title = "_".join(recipe['name'] for recipe in recipe_data[:3])  # Exemplo: usa os 3 primeiros nomes

    for recipe in recipe_data:
        pdf.add_recipe(recipe)

    # Define o caminho com o título dinâmico
    pdf_output_path = f"{pdf_title}.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path

def format_recipes_data(recipes_data):
    return [
        {
            "userName": recipe[1],
            "name": recipe[2],
            "categoryName": recipe[3],
            "createdAt": convert_datetime(recipe[4]),
            "preparationMethod": recipe[5],
            "ingredients": recipe[6],
            "portions": recipe[7],
            "description": recipe[8],
        }
        for recipe in recipes_data
    ]
