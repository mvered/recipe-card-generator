### Code to generate a recipe card PDF from google sheets recipe template ###

from fpdf import FPDF
from Recipe import Recipe
import setup_credentials
import image_resize

class RecipeCard(FPDF):

    def __init__(self, creds, spreadsheet_id):
        """initializes instance of FPDF class, 
        creates self.recipe object as instance of Recipe class"""
        self.creds = creds
        self.spreadsheet_id = spreadsheet_id
        self.recipe = Recipe(self.creds, self.spreadsheet_id)
        self.process_image()

        super().__init__(orientation = 'P',
                        format = 'Letter',
                        unit = 'mm')


    def header(self):
        """header function is automatically called when class instance is instantiated"""
        if self.page_no() == 1:
            self.image(self.recipe.photo, 0, 0)
        elif self.page_no() != 1:
            pass


    def process_image(self):
        """converts image to proper size and aspect ratio, 
        saves file path in self.recipe.photo"""
        if self.recipe.photo is not None:
            filetype = self.recipe.photo.split('.')[-1]
            new_filename = '../resources/processed_images/' + str(self.recipe.title).replace(" ", "_") + '.' + str(filetype)
            image_resize.main(source_filename = self.recipe.photo, 
                                destination_filename = new_filename, 
                                desired_ratio = (5, 4), 
                                desired_width = 250)
            self.recipe.photo = new_filename


### build RecipeCard pdf
def main(spreadsheet_id):
    """builds recipe card pdf"""
    creds = setup_credentials.get_creds()
    pdf = RecipeCard(creds = creds, spreadsheet_id = spreadsheet_id)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.output('../recipes/sample.pdf', 'F')


if __name__ == '__main__':
    main(spreadsheet_id = "14d17GFFmJWBle__sCoo7CGIoEJf7OXdgBcynSv7bBVE")