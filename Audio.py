#input: voice
#output: dictionary orders {order, quantity}

#uses pyaudio to record sound to current directory
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
# import Audio_record

#TODO PER RUN:
#TODO 1.    add keys
#TODO 2.    update job uri


class Audio:
    
    #get transcript of input
    @staticmethod
    def getTranscript():
        #Record audio
        # Audio_record.record_audio()
        #TODO credentials
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
        transfer.upload_file('Recording1.wav', 'sound-joelmussell', 'Recording.wav')
        #TODO 
        job_name = "Transcribe_1112"

        job_uri = "https://s3.us-east-2.amazonaws.com/sound-joelmussell/Recording.wav"

        #start transcription
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='wav',
            LanguageCode='en-US'
        )

        #wait for AWS to respond
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("AWS magicking...")
            time.sleep(5)

        #record transcribe output
        text = transcribe.get_transcription_job(TranscriptionJobName=job_name)

        #open json reults file  and extract information
        jsonText = urllib.request.urlopen(text['TranscriptionJob']['Transcript']['TranscriptFileUri']).read().decode('utf-8')
        jsonDict = json.loads(jsonText)
        #print(jsonDict['results'])
        transcript = jsonDict['results']['transcripts'][0]['transcript']
        #index = jsonDict.find('\"transcript\"') + 14
        #transcript = transcript[index:]
        #index = transcript.find('\"')
        #transcript = transcript[:index]
        #os.remove("Recording1.wav")
        transcribe.delete_transcription_job(TranscriptionJobName=job_name)
        '''
        print(transcript)
        '''
        return transcript

    #process transcript
    #returns dict() with order
    @staticmethod
    def getOrder(transcript):
        puctuation = {",", ".", "'", "?", "!"}
        lowercase = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

        #return value
        order = {}

        number_order_list = ["number one", "====", "====", 
            "number two", "number five", "number seven", "nugget", 
            "number four", "number eight", "number six", "===="]

        #potential input values searched by program stored in parellel arrays in reverse order of processing
        third_order_list = ["sandwich", "deluxe", "spicy chicken", 
            "spicy deluxe", "grilled chicken", "club", "number three", 
            "chicken strip", "wrap", "grilled nugget", "====", "mini", 
            "====", "bacon egg and cheese biscuit", "sausage egg and cheese biscuit", 
            "====", "multigrain bagel", "hash brown", "yogurt", 
            "fruit", "chicken egg and cheese bagel", "====", 
            "====", "muffin", "====", 
            "====", "====", "fries", "====", 
            "noodle", "tortilla", "super food", "apple sauce", 
            "====", "====", "slaw", "====", "chip", 
            "nugget kids", "kids chicken strip", "====", 
            "milkshake", "====","====", 
            "milk shake", "====", "====", "====",
            "ice cream", "key lime", "sweet", "lemonade", 
            "coca cola", "doctor pepper", "water", "====", 
            "====","chocolate milk",  "milk", "coffee", "====", 
            "====", "====", "iced tea",
            "====", "====", "====", "====",
            "====", "====", "===="]
        #
        alternative_order_list = ["====", "deluxe sandwich", "spicy chicken", 
            "spicy deluxe", "grilled chicken", "club", "====", 
            "====", "wrap", "====", "====", "mini", 
            "====", "bacon egg and cheese biscuit", "sausage egg and cheese biscuit", 
            "butter biscuit", "sunflower bagel", "====", "yogurt", 
            "fruit", "chicken egg and cheese bagel", "hash brown burrito", 
            "hash brown bowl", "====", "bacon egg and cheese muffin", 
            "sausage egg and cheese muffin", "====", "fries", "====", 
            "noodle soup", "tortilla soup", "superfood", "apple sauce", 
            "====", "====", "slaw", "cron bread", "chip", 
            "====", "chicken strip kids", "grilled nugget kids", 
            "chocolate milk shake", "cookies and cream milk shake", "strawberry milk shake", 
            "vanilla milk shake", "====", "====", "cookie",
            "ice-cream", "key lime", "====", "lemonade", 
            "coke", "doctor pepper", "water", "====", 
            "====","chocolate milk",  "====", "coffee", "====", 
            "====", "====", "non sweet",
            "chick-fil-a sauce", "====", "====", "====",
            "====", "barbeque", "===="]
        #
        order_list = ["chick fil one sandwich", "====", "spicy chicken sandwich", 
            "spicy deluxe sandwich", "grilled chicken sandwich", "grilled chicken club", "====", 
            "====", "grilled cool wrap", "grilled chicken nugget", "chicken biscuit", "chicken mini", 
            "egg white grill", "bacon, egg and cheese biscuit", "sausage, egg and cheese biscuit", 
            "buttered biscuit", "sunflower multigrain bagel", "====", "greek yogurt parfait", 
            "fruit cup", "chicken, egg and cheese bagel", "hash brown scramble burrito", 
            "hash brown scramble bowl", "english muffin", "bacon, egg and cheese muffin", 
            "sausage, egg and cheese muffin", "cobb salad", "waffle potato fries", "side salad", 
            "chicken noodle soup", "chicken tortilla soup", "superfood side", "apple sauce", 
            "carrot raisin salad", "chicken salad", "cole slaw", "cornbread", "potato chip", 
            "kids nugget", "kids chicken strip", "kids grilled nugget", 
            "chocolate milkshake", "cookies and cream milkshake", "strawberry milkshake", 
            "vanilla milkshake", "frosted coffee", "frosted lemonade", "chocolate chunk cookie",
            "ice dream cone", "key lime", "====", "====", 
            "coca-cola", "dr pepper", "bottled water", "apple juice", 
            "orange", "====", "white milk", "====", "iced coffee", 
            "gallon", "diet lemonade", "unsweet",
            "chick fil one sauce", "polynesian", "honey mustard", "ranch",
            "buffalo", "barbecue", "sriracha"]
        
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
        
        #tag values for drinks
        drinks = ["CHOCOLATE=MILKSHAKE", "COOKIES=&=CREAM=MILKSHAKE", "STRAWBERRY=MILKSHAKE", 
            "VANILLA=MILKSHAKE", "FROSTED=COFFEE", "FROSTED=LEMONADE", "CHOCOLATE=CHUNK=COOKIE",
            "ICEDREAM=CONE", "FROSTED=KEY=LIME", "FRESHLY-BREWED=ICED=TEA=SWEETENED", "LEMONADE", 
            "COCA-COLA", "DR=PEPPER", "DASANI=BOTTLED=WATER", "HONEST=KIDS=APPLE=JUICE", 
            "SIMPLY=ORANGE", "1%=CHOCOLATE=MILK", "1%=WHITE=MILK", "COFFEE", "ICED=COFFEE", 
            "GALLON=BEVERAGES", "CHICK-FIL-A=DIET=LEMONADE", "FRESHLY-BREWED=ICED=TEA=UNSWEETENED"] 
        
        side_output = ["Waffle Potato Fries", "Waffle Potato Fries", "Waffle Potato Fries", 
            "Waffle Potato Fries", "Waffle Potato Fries", "Waffle Potato Fries", "Waffle Potato Fries", 
            "Waffle Potato Fries", "Waffle Potato Fries", "Waffle Potato Fries", "Hash Browns", "Hash Browns", 
            "Hash Browns", "Hash Browns", "Hash Browns", 
            "Hash Browns", "Hash Browns", "====", "Hash Browns", 
            "Hash Browns", "Hash Browns", "Hash Brown", 
            "Hash Brown", "English Muffin", "Hash Browns", 
            "Hash Browns", "====", "====", "====", 
            "====", "====", "====", "====", 
            "====", "====", "====", "====", "====",
            "Waffle Potato Fries", "Waffle Potato Fries", "Waffle Potato Fries",
            "====", "====", "====",
            "====", "====", "====", "====",
            "====", "====", "====", "====",
            "====", "====", "====", "====", 
            "====", "====", "====", "====", "====",
            "====", "====", "====",
            "====", "====", "====", "====",
            "====", "====", "===="]
        
        #output array
        order_output = ["Chicken Sandwich", "Deluxe Sandwich", "Spicy Chicken Sandwich", 
            "Spicy Deluxe Sandwich", "Grilled Chicken Sandwich", "Grilled Chicken Club", "Nuggets", 
            "Chick-n-Strips", "Grilled Cool Wrap", "Grilled Nuggets", "Chicken Biscuit", "Chick-n-Minis", 
            "Egg White Grill", "Bacon, Egg & Cheese Biscuit", "Sausage, Egg & Cheese Biscuit", 
            "Buttered Biscuit", "Sunflower Multigrain Bagel", "Hash Browns", "Greek Yogurt Parfait", 
            "Fruit Cup", "Chicken, Egg & Cheese Bagel", "Hash Brown Scramble Burrito", 
            "Hash Brown Scramble Bowl", "English Muffin", "Bacon, Egg & Cheese Muffin", 
            "Sausage, Egg & Cheese Muffin", "Cobb Salad", "Waffle Potato Fries", "Side Salad", 
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
        #
        alt_quantities = [" a ", " to "]
        alt_quantities2 = [" the ", " too "]
        ALT_QUANTITIES = [" ONE ", " TWO "]

        operators = ["meal", "male", "combo"]
        OPERATORS = ["MEAL", "MEAL", "MEAL"]

        #preliminary translate
        translate = [" suraj a ", " suraj ", " sake ", " ship", " fry ", " grill ", " girl ", " rap ", " toe luck ", " multi green ", " multi grain ", " sun flower ", 
            " sunfire ", " flour ", " some ", " son ", " basil ", " babel ", " scrambled ", " browns ", " agon ", " to ", " too ", " ate ",
            " for ", " a ", " an ", " the ", " has ground ", " cara reason ", " nuggets ", " strips ", " kid ", "chicken nugget", 
            " ice ", "sweet iced tea ", " source ", " checking strap ", " the luck ", " com ", " Minnie", " uh ", " um ", " suite ", " no get "
            "chicken and", "chick and", "holland asian", "sarasota"]
        TRANSLATE = [" sriracha ", " sriracha ", " shake ", " chip", " fries ", " grilled ", " grilled ", " wrap ", " deluxe ", " multigrain ", " multigrain ", " sunflower ", 
            " sun flower ", " flower ", " sun ", " sun ", " bagel ", " bagel ", " scramble ", " brown ", " egg and ", " two ", " two ", " eight ",
            " four ", " one ", " one ", " one ", " hash browns ", " carrot raisin ", " nugget ", " strip ", " kids ", "nugget", 
            " iced ", "sweet ", " sauce ", " chicken strip ", " deluxe ", " corn ", " mini", " ", " ", " sweet ", "nugget"
            "chicken", "chicken", "polynesian", "sriracha"]
        #takes the transcription and converts to lowercase, then converts any word of interest to an uppercase tag indicating that it is
        #important. Then erases the remaining lowercase letters

        #convert to lowercase for processing: lowercase means unimportant
        transcript = transcript.lower() + ' '
        # print(transcript)
        #remove punctuation
        for char in puctuation:
            transcript = transcript.replace(char,'')
        # print(transcript)
        #preliminary translate
        for y in range(len(translate)):
            transcript = transcript.replace(translate[y],TRANSLATE[y])
        # print(transcript)
        #
        for y in range(len(translate)):
            transcript = transcript.replace(translate[y],TRANSLATE[y])
        # print(transcript)
        #replace words of interest with order tags
        for y in range(len(order_list)):
            transcript = transcript.replace(order_list[y],orders[y])
        # print(transcript)
        #
        for y in range(len(alternative_order_list)):
            transcript = transcript.replace(alternative_order_list[y],orders[y])
        # print(transcript)
        #
        for y in range(len(third_order_list)):
            transcript = transcript.replace(third_order_list[y],orders[y])
        # print(transcript)
        #
        for y in range(len(number_order_list)):
            transcript = transcript.replace(number_order_list[y],orders[y])
        # print(transcript)
        #replace words of interest with number tags #applied after number_order_list to avoid conflicts
        for y in range(len(quantities)):
            transcript = transcript.replace(quantities[y],QUANTITIES[y])
        # print(transcript)
        #
        for y in range(len(alt_quantities)):
            transcript = transcript.replace(alt_quantities[y],ALT_QUANTITIES[y])
        # print(transcript)
        #
        for y in range(len(alt_quantities2)):
            transcript = transcript.replace(alt_quantities2[y],ALT_QUANTITIES[y])
        # print(transcript)
        #finds the word 'to' in transcription to prevent confusion with two
        for y in range(len(operators)):
            transcript = transcript.replace(operators[y],OPERATORS[y])
        # print(transcript)
        #removes all lowercase letters that have not been converted to an order or number tag
        for char in lowercase:
            transcript = transcript.replace(char,'')
        # print(transcript)

        #take the filtered order data and convert to  dictionary orders{} containing {order, quantity}
        order_index = 1
        qu = 1
        last_qu = 1
        word = ""
        last_word = ""
        drinks_left = 0

        #for every order/quantity
        while True:
            #find next word
            index = transcript.find(' ')
            if index == -1:
                word = transcript
            elif index == 0:
                transcript = transcript[1:]
                continue
            else:
                word = transcript[:index]
            #count drinks
            if(word in drinks):
                if(last_word in OPERATORS):
                    qu = last_qu
                drinks_left = drinks_left - qu
            if(last_word in drinks):
                qu = 1
                last_qu = 1
            #compare word to list of all order tags and add to orders dict with quantity (if no quantity use 1)
            if(word in orders):
                order_index = orders.index(word)
                if order_output[order_index] in order:
                    order[order_output[order_index]] = order[order_output[order_index]] + qu
                else:
                    order[order_output[order_index]] = qu
                last_qu = qu
                qu = 1
            #compare word to list of all order tags and update qu to indicate most recent quantity
            elif(word in QUANTITIES or word in ALT_QUANTITIES):
                qu = QUANTITIES.index(word)+1
                last_qu = qu
            #deals with meals
            elif(word in OPERATORS and side_output[order_index] != "===="):
                drinks_left = drinks_left + last_qu
                if side_output[order_index] in order:
                    order[side_output[order_index]] = order[side_output[order_index]] + last_qu
                else:
                    order[side_output[order_index]] = last_qu
            
            #if no word left, end loop #if word left delete processed word
            if index == -1:
                break
            else:
                transcript = transcript[index+1:]
            last_word = word
        
        if drinks_left > 0:
            if "Coca-Cola" in order:
                order["Coca-Cola"] = order["Coca-Cola"] + drinks_left
            else:
                order["Coca-Cola"] = (drinks_left)

        return order

if __name__ == "__main__":
    # customerTest = Customer()
    order = Audio.getOrder(Audio.getTranscript())
    #order = Audio.getOrder("Hi. Can I have a kids? Nuggets meal?")
    print(order)