#input: audio file 'Recording1.mp3' in current directory
#output: dictionary orders {order, quantity}

#uses AWS to move file to s3 storage
#uses AWS to transcribe audio stored in AWS s3 storage to text
#converts transcription to order
from __future__ import print_function
import time
import boto3
from boto3.s3.transfer import S3Transfer
import urllib
import json
import os

class Audio:
    
    #get transcript of input
    @staticmethod
    def getTranscript():
        #credentials
        access_key = ''
        key_id = ''
        #set up AWS transcribe
        transcribe = boto3.client('transcribe',
            region_name='us-east-2',
            aws_secret_access_key =access_key,
            aws_access_key_id = key_id)
        client = boto3.client('s3', 'us-west-2',
            aws_secret_access_key =access_key,
            aws_access_key_id = key_id)
        transfer = S3Transfer(client)
        transfer.upload_file('Recording1.mp3', 'sound-joelmussell', 'Recording.mp3')
        job_name = "Transcribe63"
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
        os.remove("Recording1.mp3")
        transcribe.delete_transcription_job(TranscriptionJobName=job_name)
        print(transcript)
        return transcript

    #process transcript
    #returns dict() with order
    @staticmethod
    def getOrder(transcript):
        puctuation = {",", ".", "?", "!"}
        lowercase = {"'s", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

        #return value
        order = {}

        number_order_list = ["number one", "====", "====", 
            "number two", "number five", "number seven", "number three", 
            "number four", "number eight", "number six", "===="]

        #potential input values searched by program stored in parellel arrays in reverse order of processing
        third_order_list = ["sandwich", "deluxe", "spicy chicken", 
            "====", "grilled chicken", "club", "====", 
            "strip", "wrap", "====", "====", "mini", 
            "====", "bacon egg and cheese biscuit", "sausage egg and cheese biscuit", 
            "====", "sunflower bagel", "====", "yogurt", 
            "fruit", "chicken egg and cheese bagel", "hash brown burrito", 
            "hash brown bowl", "muffin", "bacon egg and cheese muffin", 
            "sausage egg and cheese muffin", "====", "fries", "====", 
            "noodle", "tortilla", "superfood", "apple sauce", 
            "====", "====", "slaw", "====", "chip", 
            "kid's nugget", "kid's chicken strip", "kid's grilled nugget", 
            "chocolate milk shake", "cookies and cream milk shake", "strawberry milk shake", 
            "milk shake", "====", "====", "====",
            "ice-cream", "key lime", "sweet", "lemonade", 
            "coke", "doctor pepper", "water", "====", 
            "====","chocolate milk",  "milk", "coffee", "====", 
            "====", "====", "unsweet",
            "====", "====", "====", "====",
            "====", "====", "===="]
        #
        alternative_order_list = ["sandwich", "deluxe", "spicy chicken", 
            "====", "grilled chicken", "club", "nugget", 
            "strip", "wrap", "grilled nugget", "====", "mini", 
            "====", "bacon egg and cheese biscuit", "sausage egg and cheese biscuit", 
            "====", "sunflower bagel", "====", "yogurt", 
            "fruit", "chicken egg and cheese bagel", "hash brown burrito", 
            "hash brown bowl", "muffin", "bacon egg and cheese muffin", 
            "sausage egg and cheese muffin", "====", "fries", "====", 
            "noodle soup", "tortilla soup", "superfood", "apple sauce", 
            "====", "====", "slaw", "====", "chip", 
            "kid's nugget", "kid's chicken strip", "kid's grilled nugget", 
            "chocolate milk shake", "cookies and cream milk shake", "strawberry milk shake", 
            "vanilla milk shake", "====", "====", "cookie",
            "ice-cream", "key lime", "sweet tea", "lemonade", 
            "coke", "doctor pepper", "water", "====", 
            "====","chocolate milk",  "milk", "coffee", "====", 
            "====", "====", "unsweet tea",
            "====", "====", "====", "====",
            "====", "====", "===="]
        #
        order_list = ["====", "====", "spicy chicken sandwich", 
            "spicy deluxe", "grilled chicken sandwich", "grilled chicken club", "chicken nugget", 
            "chicken strip", "grilled cool wrap", "grilled chicken nugget", "chicken biscuit", "chicken mini", 
            "egg white grill", "bacon, egg and cheese biscuit", "sausage, egg and cheese biscuit", 
            "buttered biscuit", "sunflower multigrain bagel", "hash brown", "greek yogurt parfait", 
            "fruit cup", "chicken, egg and cheese bagel", "hash brown scramble burrito", 
            "hash brown scramble bowl", "english muffin", "bacon, egg and cheese muffin", 
            "sausage, egg and cheese muffin", "cobb salad", "waffle potato fries", "side salad", 
            "chicken noodle soup", "chicken tortilla soup", "superfood side", "buddy's apple sauce", 
            "carrot raisin salad", "chicken salad", "cole slaw", "cornbread", "potato chip", 
            "nuggets kid's", "chicken strips kid's", "grilled nuggets kid's", 
            "chocolate milkshake", "cookies and cream milkshake", "strawberry milkshake", 
            "vanilla milkshake", "frosted coffee", "frosted lemonade", "chocolate chunk cookie",
            "ice dream cone", "key lime", "iced tea sweetened", "====", 
            "coca-cola", "dr pepper", "bottled water", "apple juice", 
            "orange", "====", "white milk", "====", "iced coffee", 
            "gallon", "diet lemonade", "iced tea unsweetened",
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
        operators = ["to"]#"with", "without", "and", "no", "not", "meal"}
        OPERATORS = ["TO"]#"with", "without", "and", "no", "not", "meal"}

        #takes the transcription and converts to lowercase, then converts any wword of interest to an uppercase tag indicating that it is
        #important. Then erases the remaining ;lowercase letters

        #convert to lowercase for processing: lowercase means unimportant
        transcript = transcript.lower() + ' '
        print(transcript)
        #remove punctuation
        for char in puctuation:
            transcript = transcript.replace(char,'')
        print(transcript)
        #replace words of interest with order tags
        for y in range(len(order_list)):
            transcript = transcript.replace(order_list[y],orders[y])
        print(transcript)
        #
        for y in range(len(alternative_order_list)):
            transcript = transcript.replace(alternative_order_list[y],orders[y])
        print(transcript)
        #
        for y in range(len(third_order_list)):
            transcript = transcript.replace(third_order_list[y],orders[y])
        print(transcript)
        #
        for y in range(len(number_order_list)):
            transcript = transcript.replace(number_order_list[y],orders[y])
        print(transcript)
        #replace words of interest with number tags #applied after number_order_list to avoid conflicts
        for y in range(len(quantities)):
            transcript = transcript.replace(quantities[y],QUANTITIES[y])
        print(transcript)
        #finds the word 'to' in transcription to prevent confusion with two
        for y in range(len(operators)):
            transcript = transcript.replace(operators[y],OPERATORS[y])
        print(transcript)
        #removes all lowercase letters that have not been converted to an order or number tag
        for char in lowercase:
            transcript = transcript.replace(char,'')
        print(transcript)

        #take the filtered order data and convert to  dictionary orders{} containing {order, quantity}
        q = False
        qu = 1

        #for every order/quantity
        while True:
            #find next word
            index = transcript.find(' ')
            if index == -1:
                word = transcript
            else:
                word = transcript[:index]
            #compare word to list of all order tags and add to orders dict with quantity (if no quantity use 1)
            if(word in orders):
                if(q == False):
                    qu = 1
                order[order_output[orders.index(word)]] = qu
                q = False
            #compare word to list of all order tags and update qu to indicate most recent quantity
            elif(word in QUANTITIES):
                qu = QUANTITIES.index(word)+1
                q = True
            #if no qunatity but 'to' is found assume it is 2
            elif(word == 'TO' and q == False):
                qu = 2
                q = True
            
            #if no word left, end loop #if word left delete processed word
            if index == -1:
                break
            else:
                transcript = transcript[index+1:]

        return order

if __name__ == "__main__":
    # customerTest = Customer()
    order = Audio.getOrder(Audio.getTranscript())
    #order = Audio.getOrder("Can I get three chicken strips")
    print(order)
"""
    elif(word == "meal"):
        order = order + '**'
    elif(word == "with"):
        order = order + '-'
    elif(word == "without"):
        order = order + '-/-'
    elif(word == "no"):
        order = order + '/-'
    elif(word == "and"):
        order = order + '    '
    elif(word in operators):
        order = order + '-' + word + '-'
"""