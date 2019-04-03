#uses AWS to transcribe audio stored in AWS s3 storage to text
#to do: add voice input and analyze output
#change job name for each run
from __future__ import print_function
import time
import boto3
import urllib
import json

class Audio:
    
    #get transcript of input
    @staticmethod
    def getTranscript():
        #set up AWS transcribe
        transcribe = boto3.client('transcribe',
            region_name='us-east-2',
            aws_secret_access_key ='key',
            aws_access_key_id = 'id')
        job_name = "Transcribe53"
        job_uri = "https://s3.us-east-2.amazonaws.com/sound-joelmussell/Recording.mp3"

        #start transcription
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp3',
            LanguageCode='en-US'
        )

        #wait for AWS to respond
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)

        #record transcribe output
        text = transcribe.get_transcription_job(TranscriptionJobName=job_name)

        #open json reults file  and extract information
        jsonText = urllib.urlopen(text['TranscriptionJob']['Transcript']['TranscriptFileUri']).read()
        index = jsonText.find('\"transcript\"') + 14
        transcript = jsonText[index:]
        index = transcript.find('\"')
        transcript = transcript[:index]
        return transcript

    #process transcript
    #returns dict() with order
    @staticmethod
    def getOrder(transcript):
        puctuation = {",", "."}

        #return value
        order = {}

        number_order_list = ["number one", "====", "====", 
            "number two", "number five", "numbrer seven", "number three", 
            "number four", "number eight", "number six", "===="]

        #potential input values searched by program stored in parellel arrays in reverse order of processing
        alternative_order_list = ["sandwich", "deluxe", "spicy chicken", 
            "====", "grilled chicken", "club", "nuggets", 
            "strips", "wrap", "grilled nuggets", "====", "minis", 
            "====", "bacon egg and cheese biscuit", "sausage egg and cheese biscuit", 
            "====", "sunflower bagel", "====", "yogurt", 
            "fruit", "chicken egg and cheese bagel", "hash brown burrito", 
            "hash brown bowl", "muffin", "bacon egg and cheese muffin", 
            "sausage egg and cheese muffin", "====", "fries", "====", 
            "noodle soup", "tortilla soup", "superfood", "apple sauce", 
            "====", "====", "slaw", "====", "chips", 
            "kid's nuggets", "kid's chicken strips", "kid's grilled nuggets", 
            "====", "====", "====", 
            "====", "====", "====", "cookie",
            "ice-cream", "frosted key lime", "sweet tea", "lemonade", 
            "coke", "doctor pepper", "water", "====", 
            "orange juice","====",  "milk", "coffee", "====", 
            "gallon beverages", "====", "unsweet tea",
            "====", "====", "====", "====",
            "====", "====", "===="]
        #
        order_list = ["====", "====", "spicy chicken sandwich", 
            "spicy deluxe", "grilled chicken sandwich", "grilled chicken club", "chicken nuggets", 
            "chicken strips", "grilled cool wrap", "grilled chicken nuggets", "chicken biscuit", "chicken minis", 
            "egg white grill", "bacon, egg and cheese biscuit", "sausage, egg and cheese biscuit", 
            "buttered biscuit", "sunflower multigrain bagel", "hash browns", "greek yogurt parfait", 
            "fruit cup", "chicken, egg and cheese bagel", "hash brown scramble burrito", 
            "hash brown scramble bowl", "english muffin", "bacon, egg and cheese muffin", 
            "sausage, egg and cheese muffin", "cobb salad", "waffle potato fries", "side salad", 
            "chicken noodle soup", "chicken tortilla soup", "superfood side", "buddy's apple sauce", 
            "carrot raisin salad", "chicken salad", "cole slaw", "cornbread", "potato chips", 
            "nuggets kid's", "chicken strips kid's", "grilled nuggets kid's", 
            "chocolate milkshake", "cookies and cream milkshake", "strawberry milkshake", 
            "vanilla milkshake", "frosted coffee", "frosted lemonade", "chocolate chunk cookie",
            "icedream cone", "frosted key lime", "iced tea sweetened", "====", 
            "coca-cola", "dr pepper", "bottled water", "apple juice", 
            "simply orange", "chocolate milk", "white milk", "====", "iced coffee", 
            "gallon beverages", "diet lemonade", "iced tea unsweetened",
            "chick-fil-a sauce", "polynesian", "honey mustard", "ranch sauce",
            "buffalo", "barbeque", "sriracha"]
        
        #tag values to replace serched values
        orders = ["CHICKEN=SANDWICH", "DELUXE=SANDWICH", "SPICY=CHICKEN=SANDWICH", 
            "SPICY=DELUXE=SANDWICH", "GRILLED=CHICKEN=SANDWICH", "GRILLED=CHICKEN=CLUB", "NUGGETS", 
            "CHICK-N-STRIPS", "GRILLED=COOL=WRAP", "GRILLED=NUGGETS", "CHICKEN=BISCUIT", "CHICK-N-MINIS", 
            "EGG=WHITE=GRILL", "BACON=EGG=&=CHEESE=BISCUIT", "SAUSAGE=EGG=&=CHEESE=BISCUIT", 
            "BUTTERED=BISCUIT", "SUNFLOWER=MULTIGRAIN=BAGEL", "HASH=BROWNS", "GREEK=YOGURT=PARFAIT", 
            "FRUIT=CUP", "CHICKEN=EGG=&=CHEESE=BAGEL", "HASH=BROWN=SCRAMBLE=BURRITO", 
            "HASH=BROWN=SCRAMBLE=BOWL", "ENGLISH=MUFFIN", "BACON=EGG=&=CHEESE=MUFFIN", 
            "SAUSAGE, EGG=&=CHEESE=MUFFIN", "COBB=SALAD", "WAFFLE=POTATO=FRIES", "SIDE=SALAD", 
            "CHICKEN=NOODLE=SOUP", "CHICKEN=TORTILLA=SOUP", "SUPERFOOD=SIDE", "BUDDY'S=APPLE=SAUCE", 
            "CARROT=RAISIN=SALAD", "CHICKEN=SALAD", "COLE=SLAW", "CORNBREAD", "WAFFLE=POTATO=CHIPS", 
            "NUGGET=KID'S=MEAL", "CHICK-N-STRIPS=KID'S=MEAL", "GRILLED=NUGGETS=KID'S=MEAL", 
            "CHOCOLATE=MILKSHAKE", "COOKIES=&=CREAM=MILKSHAKE", "STRAWBERRY=MILKSHAKE", 
            "VANILLA=MILKSHAKE", "FROSTED=COFFEE", "FROSTED=LEMONADE", "CHOCOLATE=CHUNK=COOKIE",
            "ICEDREAM=CONE", "FROSTED=KEY=LIME", "FRESHLY-BREWED=ICED=TEA=SWEETENED", "LEMONADE", 
            "COCA-COLA", "DR=PEPPER", "DASANI=BOTTLED=WATER", "HONEST=KIDS=APPLE=JUICE", 
            "SIMPLY=ORANGE", "1%=CHOCOLATE=MILK", "1%=WHITE=MILK", "COFFEE", "ICED=COFFEE", 
            "GALLON=BEVERAGES", "CHICK-FIL-A=DIET=LEMONADE", "FRESHLY-BREWED=ICED=TEA=UNSWEETENED",
            "CHICK-FIL-A=SAUCE", "POLYNESIAN=SAUCE", "HONEY=MUSTARD=SAUCE", "GARDEN=HERB=RANCH=SAUCE",
            "ZESTY=BUFFALO=SAUCE", "BARBEQUE=SAUCE", "SRIRACHA=SAUCE"] 
        
        #output array
        order_output = ["Chicken Sandwich", "Deluxe Sandwich", "Spicy Chicken Sandwich", 
            "Spicy Deluxe Sandwich", "Grilled Chicken Sandwich", "Grilled Chicken Club", "Nuggets", 
            "Chick-n-Strips", "Grilled Cool Wrap", "Grilled Nuggets", "Chicken Biscuit", "Chick-n-Minis", 
            "Egg White Grill", "Bacon, Egg & Cheese Biscuit", "Sausage, Egg & Cheese Biscuit", 
            "Buttered Biscuit", "Sunflower Multigrain Bagel", "Hash Browns", "Greek Yogurt Parfait", 
            "Fruit Cup", "Chicken, Egg & Cheese Bagel", "Hash Brown Scramble Burrito", 
            "Hash Brown Scramble Bowl", "English Muffin", "Bacon, Egg & Cheese Muffin", 
            "Sausage, Egg & Cheese Muffin", "Cobb Salad", "Waffel Potato Fries", "Side Salad", 
            "Chicken Noodle Soup", "Chicken Tortilla Soup", "Superfood Side", "Buddy's Apple Sauce", 
            "Carrot Raisin Salad", "Chicken Salad", "Cole Slaw", "Cornbread", "Waffle Potato Chips", 
            "Nugget Kid's Meal", "Chick-n-Strips Kid's Meal", "Grilled Nuggets Kid's Meal", 
            "Chocolate Milkshake", "Cookies & Cream Milkshake", "Strawberry Milkshake", 
            "Vanilla Milkshake", "Frosted Coffee", "Frosted Lemonade", "Chocolate Chunk Cookie",
            "Icedream Cone", "Frosted Key Lime", "Freshly-Brewed Iced Tea Sweetened", "Lemonade", 
            "Coca-Cola", "Dr Pepper", "DASANI Bottled Water", "Honest Kids Apple Juice", 
            "Simply Orange", "1% Chocolate Milk", "1% White Milk", "Coffee", "Iced Coffee", 
            "Gallon Beverages", "Chick-fil-A Diet Lemonade", "Freshly-Brewed Iced Tea Unsweetened",
            "Chick-fil-A Sauce", "Polynesian Sauce", "Honey Mustard Sauce", "Garden Herb Ranch Sauce",
            "Zesty Buffalo Sauce", "Barbeque Sauce", "Sriracha Sauce"]

        #quantities array
        quantities = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        QUANTITIES = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN"]

        #operators array
        operators = {"with", "without", "and", "no", "not", "meal"}

        for y in range(len(order_list)):
            transcript = transcript.replace(order_list[y],orders[y])
        for y in range(len(alternative_order_list)):
            transcript = transcript.replace(alternative_order_list[y],orders[y])
        for y in range(len(number_order_list)):
            transcript = transcript.replace(number_order_list[y],orders[y])
        for y in range(len(quantities)):
            transcript = transcript.replace(quantities[y],QUANTITIES[y])
        for char in puctuation:
            transcript = transcript.replace(char,'')

        q = False
        qu = 1

        while True:
            index = transcript.find(' ')
            if index == -1:
                word = transcript
            else:
                word = transcript[:index]
            if(word in orders):
                if(q == False):
                    qu = 1
                order[order_output[orders.index(word)]] = qu
                q = False
            elif(word in QUANTITIES):
                qu = QUANTITIES.index(word)+1
                q = True

            if index == -1:
                break
            else:
                transcript = transcript[index+1:]
        return order

if __name__ == "__main__":
    # customerTest = Customer()
    #Audio.getOrder(Audio.getTranscript())
    order = Audio.getOrder('Can I get three number two meal with four cookies and cream milkshake and a chicken biscuit please')
    print(order)