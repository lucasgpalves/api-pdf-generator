from typing import List

# Consulta SQL para buscar os dados da receita, usuário e categoria
def query_recipes( cur ) -> List[tuple]:
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

# Consulta SQL para buscar os dados da receita, usuário e categoria
def query_recipe_by_id( cur, recipe_id: int) -> tuple:
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
    WHERE 
        r.id = %s
    """

    cur.execute(recipes_query, (recipe_id, ))
    recipe_data = cur.fetchall()
    return recipe_data