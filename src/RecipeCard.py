### Code to generate a recipe card PDF from google sheets recipe template ###

from fpdf import FPDF
from Recipe import Recipe


class RecipeCard(FPDF):

    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        recipe = Recipe(self.spreadsheeet_id)

        super().__init__(orientation = 'P',
                        format = 'Letter',
                        unit = 'mm')
        self.header()

    def header(self):
        """header function is automatically called when class instance is instantiated"""
        self.image(recipe.photo, )


pdf = RecipeCard(spreadsheet_id = "14d17GFFmJWBle__sCoo7CGIoEJf7OXdgBcynSv7bBVE")
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')
pdf.output('recipes/sample.pdf', 'F')