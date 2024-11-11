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
import json
import psycopg2

from pdf_generator import PdfGenerator

# Função para converter datetime para string
def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%d / %m / %Y') if isinstance(recipe[4], datetime) else recipe[4]  # Converte para o formato 'YYYY-MM-DDTHH:MM:SS'
    raise TypeError("Type not serializable")

# Conexão ao banco de dados PostgreSQL
try:
    conn = psycopg2.connect(
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

cur = conn.cursor()

# Consulta SQL para buscar os dados da receita, usuário e categoria
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

print(recipes_data)

book_data = []

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
# Cria o PDF
pdf = PdfGenerator()
pdf.add_page()

for recipe in book_data:
    pdf.add_recipe(recipe)
    
pdf.output('receitas.pdf')

cur.close()
conn.close()
