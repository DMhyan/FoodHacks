import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import RoundedRectangle, Color
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
import os
import openai
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import re
from google.cloud import vision
import cv2
import requests
import base64


class RoundedButton(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.text = kwargs.get('text', 'Button')
        self.color = kwargs.get('color', [0, 0, 0, 1])
        self.text_color = kwargs.get('text_color', [1,1,1,1])
        self.markup = True
        self.font_size = 20
        with self.canvas.before:
            Color(*self.color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[50,])
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MyApp(App):
    def build(self):
        self.food_name = ["1","1","1"]
        self.ingredient = ["1","1","1"]
        self.preparation_time = ["1","1","1"]
   
        self.listOfIngredients = ""
        Window.size = (410,640)
        Window.clearcolor = get_color_from_hex('#a4c4e3')

        self.screen_manager = ScreenManager()
        self.main_screen = Screen(name='main')
        self.second_screen = Screen(name='second')
        self.third_screen = Screen(name='third')
        self.fourth_screen = Screen(name='type_ingredients')
        self.fifth_screen = Screen(name='sumbit_ingredients')
        self.upload_screen = Screen(name='upload')
        self.recipe_screen = Screen(name='recipe')
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.second_screen)
        self.screen_manager.add_widget(self.third_screen)
        self.screen_manager.add_widget(self.fourth_screen)
        self.screen_manager.add_widget(self.fifth_screen)
        self.screen_manager.add_widget(self.upload_screen)
        self.screen_manager.add_widget(self.recipe_screen)

        main_layout = BoxLayout(orientation='vertical', spacing = 120, size_hint=(1,0.7),padding=[0, 0, 0, 20])
        recipe = RoundedButton(text='[color=FFFFFF]Create Recipes[/color]',
                                color=get_color_from_hex('#0000FF'),
                                size_hint=(0.7, 0.05), pos_hint={'center_x': 0.5})
        recipe.bind(on_press=self.go_to_second_screen)
        main_layout.add_widget(recipe)
        about = RoundedButton(text='[color=FFFFFF]About[/color]',
                                color=get_color_from_hex('#0000FF'),
                                size_hint=(0.7, 0.05), pos_hint={'center_x': 0.5})
        about.bind(on_press=self.go_to_third_screen)
        main_layout.add_widget(about)
        exit1 = RoundedButton(text='[color=FFFFFF]Exit[/color]',
                                color=get_color_from_hex('#0000FF'),
                                size_hint=(0.7, 0.05), pos_hint={'center_x': 0.5}, on_press=self.stop)
        main_layout.add_widget(exit1)
        self.main_screen.add_widget(main_layout)

        second_layout = BoxLayout(orientation='vertical', spacing = 75, size_hint=(1,1),padding=[20, 0, 0, 10])
        takepic = RoundedButton(text='[color=FFFFFF]Take Picture[/color]',
                                        color=get_color_from_hex('#0000FF'),
                                size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        second_layout.add_widget(takepic)
        uploadpic = RoundedButton(text='[color=FFFFFF]Upload Picture[/color]',
                                color=get_color_from_hex('#0000FF'),
                                size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        uploadpic.bind(on_press = self.go_to_sixth_screen)
        second_layout.add_widget(uploadpic)
        type_ing = RoundedButton(text='[color=FFFFFF]Type Ingredients[/color]',
                                color=get_color_from_hex('#0000FF'),
                                size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        type_ing.bind(on_press = self.go_to_text_ingredients_screen)
        second_layout.add_widget(type_ing)
       
        goback = RoundedButton(text='[color=FFFFFF]Go Back[/color]',
                                color=get_color_from_hex('#0000FF'),
                                size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        goback.bind(on_press=self.go_to_first_screen)
        second_layout.add_widget(goback)
        self.second_screen.add_widget(second_layout)
       
       
        third_layout = BoxLayout(orientation='vertical',size_hint=(1,1), padding=[0, 0, 0, 5])
        about_text = Label(text='Welcome to my Computer Vision based Recipe Generator! I am a student who has come up with this idea to create a cutting-edge technology that generates delicious recipes from your leftover ingredients.\n\nMy app uses the latest in computer vision and machine learning techniques to identify the ingredients in your fridge or pantry, and then suggests recipes that use those ingredients in creative and delicious ways. With my app, you\'ll never have to worry about food going to waste again.\n\nI am dedicated to providing you with the highest quality recipes and user experience possible. I work closely with professional chefs to ensure that my recipes are not only delicious but also easy to follow.\n\nI believe that technology can play a vital role in reducing food waste and promoting sustainability. With my app, I hope to make a positive impact on both the environment and your taste buds.\n\nI am constantly working to improve my app and add new features, so stay tuned for updates and new recipes. Thank you for choosing my Computer Vision based Recipe Generator, and happy cooking!', font_size=15, bold=True, text_size=(300, None), color=[0,0,0,1], pos_hint={'center_x': 0.5, 'center_y':0.8})
       
        third_layout.add_widget(about_text)
        gobackabt = RoundedButton(text='[color=FFFFFF]Go Back[/color]', color=get_color_from_hex('#0000FF'), size_hint=(0.7, 0.05), pos_hint={'center_x': 0.5})
        third_layout.add_widget(gobackabt)
        gobackabt.bind(on_press=self.go_to_first_screen)
        self.third_screen.add_widget(third_layout)
       
       
       
        add_ingre_layout = BoxLayout(orientation = 'vertical', padding=[20, 20, 20, 30], spacing = 55)
       

        self.list_ing = Label(text = "Please enter the ingredients you have ",  font_size=15, text_size=(300, None), bold=True, color=[0,0,0,1], pos_hint={'center_x': 0.5})
        self.ingredient_input = TextInput(multiline=False)
        add_ingre_layout.add_widget(self.ingredient_input)
       
   
        add_ingre_layout.add_widget(self.list_ing)
       
        button3 = RoundedButton(text='[color=FFFFFF]Generate Recipe[/color]', color=get_color_from_hex('#0000FF'), size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        button3.bind(on_press = self.go_to_fifth_screen)
        add_ingre_layout.add_widget(button3)
        button1 = RoundedButton(text='[color=FFFFFF]Add[/color]', color=get_color_from_hex('#0000FF'), size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        button1.bind(on_press=self.on_add)
        add_ingre_layout.add_widget(button1)
       
        button2 = RoundedButton(text='[color=FFFFFF]Delete[/color]', color=get_color_from_hex('#0000FF'), size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        button2.bind(on_press=self.on_del)
        add_ingre_layout.add_widget(button2)
        button4 = RoundedButton(text='[color=FFFFFF]Go Back[/color]', color=get_color_from_hex('#0000FF'), size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
        button4.bind(on_press = self.go_to_second_screen)
        add_ingre_layout.add_widget(button4)
       
        self.fourth_screen.add_widget(add_ingre_layout)
       
       
        show_recipes_layout = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=1)
        grid.bind(minimum_height=grid.setter('height'))
        show_recipes_layout.add_widget(grid)
       
        self.food_names = []
        self.ingredients = []
        self.preparation_times = []


        for i in range(3):
           
            food_box = BoxLayout(orientation='vertical', spacing=10)
            food_name = Label(text=self.food_name[i].format(i+1), font_size=20, bold=True, color=[0,0,0,1])
            self.food_names.append(food_name)
            ingredients = Label(text='Ingredients: ' + self.ingredient[i], font_size=15, color=[0,0,0,1])
            self.ingredients.append(ingredients)

            time = Label(text = self.preparation_time[i] + ' minutes is the Prep Time' , font_size=17, color=[0,0,0,1])
            self.preparation_times.append(time)
           
            recipes_button = RoundedButton(text='[color=FFFFFF]Recipes {}[/color]'.format(i+1), color=get_color_from_hex('#0000FF'), size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
           
           
            food_box.add_widget(recipes_button)
            food_box.add_widget(food_name)
            food_box.add_widget(ingredients)
            food_box.add_widget(time)
            grid.add_widget(food_box)
           
           
           
        self.fifth_screen.add_widget(show_recipes_layout)
           

        upload_layout = BoxLayout(orientation='vertical', padding = (0,20,0,100), spacing = 100)

        # Create the label
        file_name_label = Label(text='Enter your file name', font_size = 40, bold = True)

        # Create the text input widget
        self.file_name_input = TextInput()
       
        file_name_button = RoundedButton(text='[color=FFFFFF]Upload Image[/color]', color=get_color_from_hex('#0000FF'), size_hint=(0.7, 0.5), pos_hint={'center_x': 0.5})
       
        file_name_button.bind(on_press = self.extract_Ing)

        # Add the label and text input to the upload_layout
        upload_layout.add_widget(file_name_label)
        upload_layout.add_widget(self.file_name_input)
        upload_layout.add_widget(file_name_button)

        # Add the upload_layout to the upload_screen
        self.upload_screen.add_widget(upload_layout)
       

       
        return self.screen_manager
   
    def go_to_recipes(self,num,*args):
        print(num)
   
    def extract_Ing(self, *args):
        file_path = self.file_name_input.text
        model_id = "food-item-v1-recognition"
        CLARIFAI_API_KEY = ""
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Lenovo Yoga 9SIN\Desktop\Apps\Food_Recipes\corded-forge-385305-abbd3de5d0f5.json"

        # create a client for the Google Cloud Vision API
        client = vision.ImageAnnotatorClient()

        # read the image file into a binary string
        with open(str(file_path), "rb") as image_file:
            content = image_file.read()

        # create a vision.Image object from the binary string
        image = vision.Image(content=content)

        # perform object detection on the image
        objects = client.object_localization(
                image=image).localized_object_annotations

        # read the image file into a numpy array
        image = cv2.imread(str(file_path))


        print(image.shape)

        count=0
        x = []
        for obj in objects:
            # convert the bounding_poly property to a list of tuples
            count = count+1
            print(count)
            bounding_poly = [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices]
           
           
           
            if len(bounding_poly) != 4:
                print(f"Error: bounding_poly has length {len(bounding_poly)}, expected 4")
                continue
           
            height, width, _ = image.shape
           
            top_left = int(bounding_poly[0][0] * width)
            top_right = int(bounding_poly[0][1] * height)
            bottom_left= int(bounding_poly[2][0] * width)
            bottom_right = int(bounding_poly[2][1] * height)
            cv2.rectangle(image, (top_left, top_right), (bottom_left, bottom_right), (255, 0, 0), 2)
           
            cropped_image = image[top_right:bottom_right, top_left:bottom_left]
            cropped_image = cv2.resize(cropped_image, (200, 200))
           
            # Encode the cropped image to base64
            _, image_jpeg = cv2.imencode('.jpg', cropped_image)
            image_base64 = base64.b64encode(image_jpeg.tobytes()).decode("utf-8")

            # Make a request to the Clarifai API with the cropped image
            response = requests.post(
                "https://api.clarifai.com/v2/models/{}/outputs".format(model_id),
                headers={
                    "Authorization": "Key {}".format(CLARIFAI_API_KEY),
                    "Content-Type": "application/json",
                },
                json={
                    "inputs": [
                        {
                            "data": {
                                "image": {
                                    "base64": image_base64
                                },
                            },
                        },
                    ],
                },
            )

    # Get the list of food predictions
            predictions = response.json()['outputs'][0]['data']['concepts']
            # Initialize variables to store the highest score and the corresponding ingredient
            highest_scores = []
            highest_score = 0
            highest_score_ingredient = ""
            # Loop through the list of predictions
            for prediction in predictions:
                if prediction['value'] > highest_score:
                    highest_score = prediction['value']
                    highest_score_ingredient = prediction['name']
                    highest_scores.append(highest_score)
                    x.append(highest_score_ingredient)
        cv2.imshow('image',image)
        x=', '.join(x)
        self.listOfIngredients = x
        self.go_to_fifth_screen()
       
       
       
       
           
           
                   
       
                   
   
    def on_add(self, instance):
        if self.listOfIngredients == '':
            self.listOfIngredients = self.ingredient_input.text
            self.list_ing.text = self.listOfIngredients
        else:
            self.listOfIngredients = self.listOfIngredients + ", " + self.ingredient_input.text
            self.list_ing.text = self.listOfIngredients
        self.ingredient_input.text = ''
   
    def on_del(self, instance):
        li = self.listOfIngredients.split(", ")
        li.pop()
        self.listOfIngredients = ", ".join(li)
        self.list_ing.text = self.listOfIngredients
       
    def go_to_sixth_screen(self, *args):
        self.screen_manager.current = 'upload'
       
       
    def go_to_fifth_screen(self, *args):
        openai.api_key = ("")
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt="I have the ingredients:" + self.listOfIngredients + "Only tell me 3 foods I can make using all ingredients. Tell me the food name, the ingredients I need to make them and the preparation time in this format:   1.<food_name> : Ingredients: '<ingredients>'. Preparation Time: <preparation_time>",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        string = response.choices[0].text
        print(string)
        self.food_name = re.findall(r'\d+\.([A-Za-z\s]+)', string)
        # Extract the ingredients
        self.ingredient = re.findall(r'Ingredients:\s(.*?)[\.|-]\sPreparation', string, re.MULTILINE)
        # Extract the preparation time
        self.preparation_time = re.findall(r'Preparation\sTime:\s([\w\s]*)', string, re.MULTILINE)

        # Print the extracted information
        print("Food Name: ", self.food_name)
        print("Ingredients: ", self.ingredient)
        print("Preparation Time: ", self.preparation_time)
       
        for i in range(3):
            self.food_names[i].text = self.food_name[i]
            self.ingredients[i].text = self.ingredient[i]
            self.preparation_times[i].text = self.preparation_time[i]
       
       
        self.screen_manager.current = 'sumbit_ingredients'
                                   

    def go_to_second_screen(self, *args):
        self.screen_manager.current = 'second'
    def go_to_first_screen(self, *args):
        self.screen_manager.current = 'main'
    def go_to_third_screen(self, *args):
        print("hello")
        self.screen_manager.current = 'third'
    def go_to_text_ingredients_screen(self, *args):
        self.screen_manager.current = 'type_ingredients'
   
   

if __name__ == '__main__':
    MyApp().run()
