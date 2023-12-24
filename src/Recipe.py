### Recipe Card Data ###

# Test/default spreadsheet ID
SPREADSHEET_ID = "14d17GFFmJWBle__sCoo7CGIoEJf7OXdgBcynSv7bBVE"

# Libraries
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import credentials
from google.auth.transport.requests import AuthorizedSession
import requests
import io
from PIL import Image
from copy import deepcopy


class Recipe():
    """stores data on a recipe, 
    based on the structure of a google sheets template file"""

    def __init__(self, creds, spreadsheet_id = SPREADSHEET_ID):

        # attributes for internal  use
        self._creds = creds
        self._spreadsheet_id = spreadsheet_id

        # metadata fields
        self.title = None
        self.sheet_metadata = None
        self.component_count = 0

        # data fields
        self.servings = None
        self.time = None
        self.source = None
        self.notes = None
        self.to_serve = None
        self.photo = None
        self.recipe = []

        # get raw metadata from google sheet
        self._metadata = self.get_metadata()

        # update metadata fields as long as http request for metada worked
        if self._metadata is not None:
            self.update_metadata_fields()
            self._data = self.get_data()
        
        # if http request to retrieve data worked, update data fields 
        if self._data is not None:
            self.update_data_fields()



    def get_metadata(self):
        """Retrieves metadata on the recipe spreadsheet"""
        try:
            service = build("sheets", "v4", credentials = self._creds)
            res = service.spreadsheets().get(spreadsheetId = self._spreadsheet_id).execute()
            #with open('metadata.json', 'w') as f:
            #    json.dump(res, f, indent = 2)
            return res
        
        except HttpError as err:
            print(err)
            return None 


    def extract_title(self):
        """Looks in self._metadata and returns the recipe title"""
        return self._metadata["properties"]["title"]


    def extract_sheet_metadata(self):
        """ 
        Looks in self._metadata 
        Retrieves sheet ID and sheet name for each sheet in the spreadsheet
        Returns sheet info in dictionary format
        """
        # sets up outer dictionary
        sheet_info = {}
        sheet_info['components'] = []
        
        # loops through sheets in the metadata field
        for sheet in self._metadata['sheets']:
            # creates a subdictionary with info on each sheet's id and name
            temp_dict = {}
            temp_dict['sheet_id'] = sheet['properties']['sheetId']
            temp_dict['name'] = sheet['properties']['title']
            
            # if appropriate, adds that subdict as the value for a key summary in the outer dict
            if temp_dict['name'] == 'Summary':
                sheet_info['summary'] = temp_dict
            # otherwise, adds subdict to a list of all the components in the recipe
            # a recipe may have multiple components, for example a pie has the crust and filling
            else:
                sheet_info['components'].append(temp_dict)

        return sheet_info


    def update_metadata_fields(self):
        """updates title, sheet_metadata, and component count attributes
        based on self._metadata"""
        self.title = self.extract_title()
        self.sheet_metadata = self.extract_sheet_metadata()
        self.component_count = len(self.sheet_metadata['components'])


    def get_data(self):
        """Retrieves values from the recipe spreadsheet"""
        try:
            range_list = ['Summary!A1:B6']
            for sheet in self.sheet_metadata['components']:
                ingredients = sheet['name'] + '!A2:B100'
                method = sheet['name'] + '!C2:C100'
                range_list.append(ingredients)
                range_list.append(method)

            service = build("sheets", "v4", credentials = self._creds)
            res = service.spreadsheets().values().batchGet(spreadsheetId = self._spreadsheet_id, ranges = range_list).execute()
            #with open('data.json', 'w') as f:
            #    json.dump(res, f, indent = 2)
            return res

        except HttpError as err:
            print(err)
            return None 


    def extract_servings(self):
        """gets serving info from self._data"""
        return self._data['valueRanges'][0]['values'][0][1]


    def extract_time(self):
        """gets time info from self._data"""
        return self._data['valueRanges'][0]['values'][1][1]

    
    def extract_source(self):
        """extracts source info from self._data"""
        return self._data['valueRanges'][0]['values'][2][1]

    
    def extract_notes(self):
        """extracts notes info from self._data"""
        return self._data['valueRanges'][0]['values'][3][1]


    def extract_to_serve(self):
        """extracts to serve info from self._data"""
        return self._data['valueRanges'][0]['values'][4][1]


    def extract_photo(self):
        """retrieves photo from specified url"""
        photo_name = self._data['valueRanges'][0]['values'][5][1]
        filetype = photo_name.split('.')[-1]
        filename = 'resources/raw_images' + str(self.title).replace(" ", "_") + '.' + str(filetype)
            
        # checks if url is a regular url or the name of an image stored in google photos
        if photo_name[0:4] == 'http':
            # uses requests library to get photo from url
            image_response = requests.get(photo_name, stream=True)
            try:
                Image.open(io.BytesIO(image_response.content))
                with open(filename, 'wb') as f:
                    f.write(image_response.content)
            except OSError:
                print("Image download request did not return valid data. The site you are downloading from may be blocking your request.")  
                return None                
        else:
            # to use the google api client to download a photo, we need the base url 
            # which is a temp url valid for 60 mins
            # there is no direct way to get base url from the user interface online
            # so we get data on all the food photos in the users library
            # and look for one where the filename field matches our specified photo variable
            # then retrieve the temporary baseUrl associated with that photo
            service = build("photoslibrary", "v1", credentials = self._creds, static_discovery=False)
            food_pics = service.mediaItems().search(
                body={"filters": 
                    {
                    "contentFilter": {"includedContentCategories": ["FOOD"]},
                    "mediaTypeFilter": {"mediaTypes":["PHOTO"]}
                    }}).execute()    
            base_url = None  
            for photo in food_pics['mediaItems']:
                if photo['filename'] == photo_name:
                    base_url = photo['baseUrl'] 
                    break   
            if base_url is None:
                return None

            # now we can use the requests https library to download the image file
            authed_session = AuthorizedSession(self._creds)
            image_response = authed_session.get(f'{base_url}=w800-h800').content
            with open(filename, 'wb') as f:
                f.write(image_response)

        return filename

    def extract_recipe(self):
        """extracts recipe ingredients and method from self._data"""
        components = deepcopy(self.sheet_metadata['components'])
        recipe = []
        idx = 1
        content = self._data['valueRanges']

        while idx < len(content) - 1:
            temp_dict = {}
            temp_dict['name'] = components[0]['name']
            components.pop(0)

            ingredients = []
            for amount, ingredient in content[idx]['values']:
                ingredients.append(amount + ' ' + ingredient)
            temp_dict['ingredients'] = ingredients

            method = []
            for step in content[idx + 1]['values']:
                method.append(step[0])
            temp_dict['method'] = method

            recipe.append(temp_dict)
            idx += 2
            
        return recipe

    
    def update_data_fields(self):
        """extracts data from self._data and updates all the data fields"""
        self.servings = self.extract_servings()
        self.time = self.extract_time()
        self.source = self.extract_source()
        self.notes = self.extract_notes()
        self.to_serve = self.extract_to_serve()
        self.photo = self.extract_photo()
        self.recipe = self.extract_recipe()


if __name__ == "__main__":
    creds = credentials.get_creds()
    my_recipe = Recipe(creds)