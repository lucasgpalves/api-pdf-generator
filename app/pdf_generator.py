from fpdf import FPDF

class PdfGenerator(FPDF):
    
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Receitas', 0, 1, 'C')
        self.ln(10)

    def add_recipe(self, recipe):
        (userName, name, categoryName, createdAt, preparationMethod, ingredients, portions, 
         description) = recipe
        
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, f"Receita: - {recipe['name']}", 0, 1)
        
        self.set_font('Arial', '', 9)
        self.cell(0, 8, f'Autor: {recipe['userName']} | Categoria: {recipe['categoryName']}', 0, 1)
        self.cell(0, 8, f'Criada em: {recipe['createdAt']}', 0, 1)
        self.cell(0, 8, f'Porções: {recipe['portions']}', 0, 1)
        self.cell(0, 8, f'Descrição: {recipe['description']}', 0, 1)
        self.cell(0, 8, f'Método de Preparo: {recipe['preparationMethod']}', 0, 1)
        
        self.cell(0, 8, "Ingredientes:", 0, 1)
        for ingredient in recipe['ingredients']:
            self.cell(0, 8, f" - {ingredient['amount']} {ingredient['measurementName']} de {ingredient['ingredientName']}", 0, 1)
        
        self.ln(10)  # Espaço entre receitas

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
