# AI modules
import openai
import langchain

# System Utils
import os
import re
import json
import time
import uuid
import requests
from datetime import datetime


# Python - MongoDB Connection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse     # Mongo Authentication Link Join
import pymongo, uuid

# Audio time calculator 
from pydub import AudioSegment

# API Serve
from flask import Flask, request, jsonify


# Loding of .env File
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------------------------------------------------------


# --------------   Story Generation -----------------------

def title_storyOutline_imgPrompt_generation(age, characters, scenario, positive_values, emotions, lang):
    
    # -------  Prompt for FRENCH Story generation -----------------
    
    if lang=="french":

        # Prompt To be added Later
        vulgar_prompt_for_french = f"""If these words : \" {characters}, {scenario}, {positive_values}, {emotions} \" are vulger for a kid, then only return : {{"title": "error"}} and nothing else."""
        
        prompt_template = f"""

Prompt de Plan d'Histoire : Concevez un titre et un plan intéressants et uniques pour une histoire captivante de 2000 mots adaptée aux enfants âgés de {age}. Orientez le récit autour des personnages {characters}, qui peuvent être seuls ou plusieurs, confrontés à un événement déterminant dans {scenario}, éveillant une émotion profonde de {emotions}. Cet événement les incite à viser un but qui incarne la valeur de {positive_values}. Décrivez en détail les défis et péripéties de l'aventure, en mettant en lumière comment {characters} affrontent et tirent des leçons de ces épreuves, reflétant ainsi subtilement {emotions} et {positive_values}. Veillez à ce que le plan soit sans vulgarité ni violence explicite, et qu'il soit soigneusement conçu pour captiver et éduquer le groupe d'âge visé.

Rule (Don't Ignore) : Use this python dictionary format for output and make the response to escape special characters, so that i can directly use the response, and keep the "title" and "story" ; the keys of the json in english...

{{"title": "<title_here_in_string_format>", "story": "<story_here_in_string_format>"}}
"""
    
    else:
        
        # --------------------  Prompt for other (ENGLISH) language  -----------------------------

        # Prompt To be added Later
        vulgar_prompt_for_english = f"""
If these words : \" {characters}, {scenario}, {positive_values}, {emotions} \" are vulger for a kid, then only return : {{"title": "error"}} and nothing else."""
        
        
        prompt_template = f"""

Craft an outline and an interesting and unique title for a captivating 2000-word story suitable for children aged {age}. Center the narrative around {characters}, a protagonist(s) who encounters a pivotal event in {scenario}, sparking a profound sense of {emotions}. This event leads {characters} to pursue a goal that represents {positive_values}. Detail each challenge or twist in the adventure, making sure to vividly depict how {characters} confronts and learns from these moments, thereby subtly illustrating {emotions} and {positive_values}. Ensure the outline is free from vulgarity and explicit violence, and is thoughtfully tailored to engage and inspire the target age group.

Rule (Don't Ignore) : Use this python dictionary format for output and make the response to escape special characters, so that i can directly use the response.

{{"title": <title_here_in_string_format>, "story": <story_here_in_string_format>}}

"""

    # ----------------  OPENAI Generation Code LLM ----------------------

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4o-2024-05-13",
      max_tokens=2000,
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": "You are a very lengthy elaborative story teller, with a lot of twist and turn and morals. Give the output in json."},
        {"role": "user", "content": f"{prompt_template}"}
      ]
    )
    
    print("Title + Story Outine --- Direct Response :\n",response,"\n-----------------------------------------------\n")

    return response.choices[0].message.content


# ------------------------  Story Outline --> Lengthy Story --------------------------

def story_length_increaser(story, age, characters, scenario, positive_values, emotions, lang):
    
    prompt_template = f"""
    
    Using previously crafted story outline : \"{story}\", write a detailed atleast 2000-word story in {lang}. Feature {characters}, whether solo or as a group, in {scenario}. Provide in-depth descriptions for each twist and turn they encounter, outlining the events, the characters\' responses, and how each situation is resolved. Provide climax and thriller in the story. Emphasize how {characters} embodies {positive_values} and experiences {emotions} throughout these challenges. The story should be age-appropriate for {age}, rich in engaging details, and free from any vulgarity or violence.

    Rule (Don't Ignore) : Just Provide Only the Story body as string, with no title or anything extra like chapters.

"""

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4o-2024-05-13",
      max_tokens=2000,
    #   response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": f"You are a {lang} chatbot that provides a long lengthy response."},
        {"role": "user", "content": f"{prompt_template}"}
      ]
    )
    
    print("Story Increase --- Direct Response :\n",response,"\n-----------------------------------------------\n")

    return response.choices[0].message.content


# ------------------------- Image Prompt & Image File ---------------------------

def image_prompt_generator(story):
    prompt_template = f""" Generate a descriptive image prompt for the story and in the prompt give a detailed description about everything in 100 words. This is the Story :  \"{story}\"."""

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4o-2024-05-13",
      max_tokens=2000,
    #   response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": f"You are a image prompt generator for an AI Image Generator."},
        {"role": "user", "content": f"{prompt_template}"}
      ]
    )
    
    print("Image Prompt :\n",response.choices[0].message.content,"\n-----------------------------------------------\n")

    return response.choices[0].message.content

def create_image(prompt):

    from openai import OpenAI
    client = OpenAI()

    prompt_template = f"{prompt}; 8k, ray tracing, photorealism, Without ever writing any text, or having inappropriate imagery for children, peaceful nighttime landscape with vibrant colors of purple, blue, and white. The starry sky is adorned with a bright crescent moon."

    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt_template,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    image_url = response.data[0].url

    return image_url

# Fix the Function for image generation --> add another extra image_compressed.jpg to check image is compressed or not

# def compress_image(image_path):
#     import os
#     from PIL import Image

#     quality=35
    
#     try:
#         img = Image.open(image_path)
#         img.save(image_path, quality=quality, optimize=True)
#         print(f"Compressed: {image_path}")
#         return image_path
#     except Exception as e:
#         print(f"Error compressing {image_path}: {e}")




# -------------------------  Download Image from Link ----------------------

def save_img___from_link_to_local(image_url, index):
    directory = f'content/{index}'
    # Check if the directory exists, and if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = f'content/{index}/image.png'
    # Send an HTTP GET request to the URL
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary write mode and write the image content to it
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {file_path}")
    else:
        print("Failed to download the image")

    return file_path

# -----------------------  Audio Section - Audio Generation ----------------------

# Helper function to split text into chunks
def split_text(text, chunk_size=4000):
    chunks = []
    words = text.split()
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += " " + word
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Helper function to merge audio files
def merge_audio_files(audio_files, output_file):
    combined = None
    for file in audio_files:
        sound = AudioSegment.from_wav(file)
        if combined is None:
            combined = sound
        else:
            combined += sound
    print("Output File : ",output_file)
    combined.export(output_file, format="wav")

def convert_wav_to_mp3(wav_file, mp3_file):

    # Load the WAV file
    audio = AudioSegment.from_wav(wav_file)
    
    # Export as MP3
    audio.export(mp3_file, format="mp3")

# Modified generate_speech function
def generate_speech(title, story, index):
    # Initialize OpenAI client
    from openai import OpenAI
    client = OpenAI()

    # Split story into chunks
    story_chunks = split_text(story)
    # Define image directory
    audio_dir = os.path.join(os.curdir, f"content/{index}/")

    # Create the directory if it doesn't yet exist
    if not os.path.isdir(audio_dir):
        os.mkdir(audio_dir)
    # Generate speech for each chunk
    audio_files = []
    response = None  # Initialize response variable outside the loop
    for i, chunk in enumerate(story_chunks):
        if i==0:
          input_text = title + "                " + chunk
        else:
          input_text=chunk
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=input_text
        )
        file_path = os.path.join(f"content/{index}/", f"audio_{i}.wav")
        response.stream_to_file(file_path)
        audio_files.append(file_path)

    # Convert audio files to WAV format
    for i, file_path in enumerate(audio_files):
        audio = AudioSegment.from_file(file_path)
        audio.export(file_path, format="wav")

    # Merge audio files
    merged_file_path = os.path.join(f"content/{index}/", f"audio.wav")
    mp3_file_path = os.path.join(f"content/{index}/", f"audio.mp3")
    merge_audio_files(audio_files, merged_file_path)
    convert_wav_to_mp3(merged_file_path, mp3_file_path)

    return mp3_file_path


def get_audio_duration(file_path):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Get the duration in seconds
    duration_in_seconds = len(audio) / 1000.0

    return duration_in_seconds


# ----------------- Master Database - Every Story to be Added ------------------

def mongo_add(json_data):
    # Replace 'username' and 'password' with your actual values
    username = "ddhara"
    password = "Admin@123"

    # Escape the username and password
    escaped_username = urllib.parse.quote_plus(username)
    escaped_password = urllib.parse.quote_plus(password)

    # Giving URL Parsed string, or else error
    uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.uzwjz4i.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    mongo_client = client
    db = mongo_client["ver1"]
    collection = db["collection"]
    collection.insert_one(json_data)
    mongo_client.close()


# ----------------- Story Word Counter ------------

def count_words(text):
    words = text.split()  # Split the text into words
    return len(words)     # Return the number of words


# -----------------  Driver Code here -----------------

def start_main_process(age, characters, scenario, positive_values, emotions, userId, story_lang):
    print("\n\nGenerating Story and Titles and Img Prompt...\n\n")
    openai_json_output = title_storyOutline_imgPrompt_generation(age, characters, scenario, positive_values, emotions, story_lang)
    
    try:
        title_storyOutline = json.loads(openai_json_output)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return jsonify({"title": "Story Generation Error - Please re-check your Parameters - Error Code : 402"})

    # unique story id generation
    index = str(uuid.uuid4())
    print("\n\nUUID generated !! --> ", index)

    try:
        story_with_slash_n = story_length_increaser(title_storyOutline['story'], age, characters, scenario, positive_values, emotions, story_lang)
        story = re.sub(r'\\n', '<br>', story_with_slash_n)   # \n\n to <br><br>
        title = title_storyOutline['title']
        # Handling of Vulgar Prompts
        if title.lower() == "error":
            return jsonify({"title": "Story Generation Error - Please re-check your Parameters - Error Code : 401"})
        img_prompt = image_prompt_generator(story)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"title": "Story Generation Error - Please re-check your Parameters - Error Code : 502"})
    
    thumb_img_path = save_img___from_link_to_local(create_image(img_prompt), index)
    timestamp = datetime.utcnow()
    audio_path = generate_speech(title, story, index)
    audio_duration = get_audio_duration(audio_path)
    story_length = count_words(story)

    json_data = {
        "_id": index,
        "story_word_count": story_length,
        "lang": story_lang,
        "timestamp": timestamp,
        "userId": userId,
        "title" : title,
        "story": story,
        "thumb_img_path": f"https://storyia.app/{thumb_img_path}",
        "audio_path": f"https://storyia.app/{audio_path}",
        "audio_duration": audio_duration,
    }

    mongo_add(json_data)

    return json_data


# ------------------- Flask API Here ---------------------
app = Flask(__name__)

# Check Health
@app.route('/api/', methods=['GET'])
def index():
    return "Hello World !!!"

# Generate Story
@app.route('/api/generate_story', methods=['POST'])
def storia_story_responce():
    try:
        age = request.args.get('age')
        characters = request.args.get('characters')
        scenario = request.args.get('scenario')
        positive_values = request.args.get('values')
        emotions = request.args.get('emotions')
        userId = request.args.get('userId')
        lang = request.args.get('lang')
        print(characters)
        response = start_main_process(age, characters, scenario, positive_values, emotions, userId, lang)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"title": "Story Generation Error - Please re-check your Parameters - Error Code : 501"})

# Run the Flask app
if __name__ == '__main__':
    app.run()
