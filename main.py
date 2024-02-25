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
        prompt_template = f"""
If these words : \" {characters}, {scenario}, {positive_values}, {emotions} \" are vulger for a kid, then only return : {{"title": "error"}} and nothing else.

Generate a very lengthy children's story in french of about atleast 1000 words for story only and a title for :

Titre : [Titre personnalisé lié au scénario et aux personnages]

Tranche d'Âge Cible : {age} Créez des histoires adaptées à la tranche d'âge spécifiée, en veillant à ce que les émotions et les valeurs positives soient intégrales à l'histoire.

Style et Ton : Adapté au scénario choisi.

Personnages Principaux : {characters} [Nom et genre. Utilisez les émotions et les valeurs pour façonner leur personnalité et leur rôle.]

Cadre et Scénario : {scenario} Développez un monde autour du scénario fourni.

Valeurs Positives : {positive_values}

Émotions à Explorer : {emotions}

Développement de l'Histoire :
1. Introduction des Personnages et du Monde : Description captivante et détaillée.
2. Profondeur des Personnages : Explorez leurs antécédents, {emotions}, et {positive_values}.
3. Introduction d'un Problème ou Défi : Un défi unique dans leur monde, décrit en profondeur.
4. Descriptions Riches : Environnements, situations et interactions détaillés.
5. Plusieurs Tentatives de Résolution : Différentes méthodes pour résoudre le problème, chacune décrite en détail.
6. Introduction de Personnages Secondaires : Personnages supplémentaires qui enrichissent l'intrigue, avec des antécédents et des rôles détaillés.
7. Plus de Rebondissements : Chaque nouveau rebondissement, tournant et développement doit être minutieusement détaillé, pas juste mentionné superficiellement.
8. Conflits Internes et Externes : Conflits émotionnels et physiques, explorés de manière élaborée.
9. Détails du Voyage : Si applicable, décrivez le voyage en détail.
10. Sous-intrigues : Histoires secondaires liées à la narrative principale, chacune développée de manière approfondie.
11. Nouveau Rebondissement ou Obstacle : Un élément inattendu ou un nouveau défi, décrit en détail.
12. Résolution et Conclusion : Résolvez le problème, changements et apprentissages des personnages, tout décrit en profondeur.
13. Conclusion Étendue : Réfléchissez sur les leçons apprises et l'évolution des personnages, en tenant compte de tous les événements détaillés de l'histoire.

Directives Supplémentaires :
- Évitez la violence explicite, les thèmes effrayants ou le contenu inapproprié.
- Adaptez les scènes, dialogues et descriptions à la tranche d'âge.
- Rendez l'histoire immersive et captivante.

Exigence de Longueur :
- L'histoire doit être longue et continue, avec un minimum de 1000 mots, fournissant une expérience narrative complète et engageante.

Fournissez également une description détaillée de l'image pour le générateur d'images IA, avec chaque petit détail (max 100 mots).

Utilisez ce format de liste python pour la sortie et échappez les caractères spéciaux, afin que je puisse utiliser directement la réponse.

Use this python list format for output and make the response to escape special characters, so that i can directly use the response, and keep the "title", "story" and the "image_prompt" ; the keys of the json in english...

{{"title": "<title_here_in_string_format>", "story": "<story_here_in_string_format>", "image_prompt": "<image_prompt_here_in_string_format>"}}
"""
    
    else:
        
        # --------------------  Prompt for other (ENGLISH) language  -----------------------------
        
        prompt_template = f"""

If these words : \" {characters}, {scenario}, {positive_values}, {emotions} \" are vulger for a kid, then only return : {{"title": "error"}} and nothing else.

Generate a very lengthy children's story of about atleast 1000 words for story only and a title for :

Title: [Custom title related to the scenario and characters]

Target Age Range: {age} Create stories tailored to the specified age range.

Style and Tone: Adapted to the chosen scenario.

Main Characters: {characters} [Name and gender. Use the emotions and values to shape their personality and role.]

Setting and Scenario: {scenario} Develop a world around the provided scenario.

Positive Values: {positive_values}

Emotions to Explore: {emotions}

Story Development:
1. Introduction of Characters and World: Captivating and detailed description.
2. Character Depth: Explore their backgrounds, dreams, fears, and motivations.
3. Introduction of a Problem or Challenge: A unique challenge in their world.
4. Rich Descriptions: Detailed environments, situations, and interactions.
5. Multiple Resolution Attempts: Different methods to solve the problem.
6. Introduction of Secondary Characters: Additional characters that enrich the plot.
7. More Twists and Turns: Unexpected obstacles and developments.
8. Internal and External Conflicts: Emotional and physical conflicts.
9. Journey Details: If applicable, describe the journey in detail.
10. Subplots: Secondary stories related to the main narrative.
11. New Twist or Obstacle: An unexpected element or new challenge.
12. Resolution and Conclusion: Solve the problem, changes and learnings of the characters.
13. Extended Conclusion: Reflect on the lessons learned and the evolution of the characters.

Additional Guidelines:
- Avoid explicit violence, frightening themes, or inappropriate content.
- Adapt scenes, dialogues, and descriptions to the age range.
- Make the story immersive and captivating.

Length Requirement:
- The story should be long and continuous, with a minimum of 1000 words, providing a comprehensive and engaging narrative experience.

Also provide a descriptive image prompt (max 100 words) for ai image generator, with every small details.

Use this python list format for output and make the response to escape special characters, so that i can directly use the response.

{{"title": <title_here_in_string_format>, "story": <story_here_in_string_format>, "image_prompt": <image_prompt_here_in_string_format>}}
"""

    # ----------------  OPENAI Generation Code LLM ----------------------

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      max_tokens=2000,
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": "You are a very lengthy elaborative story teller, with a lot of twist and turn and morals. Give the output in json."},
        {"role": "user", "content": f"{prompt_template}"}
      ]
    )
    
    print("Title + Story Outine + Img Prompt --- Direct Response :\n",response,"\n-----------------------------------------------\n")

    return response.choices[0].message.content


# ------------------------  Story Outline --> Lengthy Story --------------------------

def story_length_increaser(story):
    prompt_template = f""" This is a outline of a story : \"{story}\" . Please make sure the story is expanded to atleast 1000 words. Expand this story with no title for 10 paragraph. Each paragraph containing 120 words. Please make it lengthy. 
"""

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      max_tokens=2000,
    #   response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": "You are a chatbot that provides a long lengthy response."},
        {"role": "user", "content": f"{prompt_template}"}
      ]
    )
    
    print("Story Increase --- Direct Response :\n",response,"\n-----------------------------------------------\n")

    return response.choices[0].message.content


# ------------------------- Image Prompt --> Image File ---------------------------

def create_image(prompt):

    from openai import OpenAI
    client = OpenAI()

    prompt_template = f"{prompt}; cartoon, 8k, rtx, photorealism, without ever writing any text, or having inappropriate imagery for children, with vibrant colors of purple, blue, and white"

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

# def text_to_audio_generate(input, index):

#     from openai import OpenAI
#     client = OpenAI()

#     response = client.audio.speech.create(
#       model="tts-1",
#       voice="nova",
#       input=input
#     )

#     audio_output_path = f"content/{index}/audio.mp3"

#     response.stream_to_file(audio_output_path)

#     return audio_output_path

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
        input_text = title + "\n\n\n\n\n\n\n\n" + chunk
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
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
    merge_audio_files(audio_files, merged_file_path)

    return merged_file_path



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
        title_storyOutline_imgPrompt = json.loads(openai_json_output)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return jsonify({"title": "Story Generation Error - Please re-check your Parameters - Error Code : 402"})

    # unique story id generation
    index = str(uuid.uuid4())
    print("\n\nUUID generated !! --> ", index)

    try:
        story_with_slash_n = story_length_increaser(title_storyOutline_imgPrompt['image_prompt'])
        story = re.sub(r'\\n', '<br>', story_with_slash_n)   # \n\n to <br><br>
        title = title_storyOutline_imgPrompt['title']
        # Handling of Vulgar Prompts
        if title.lower() == "error":
            return jsonify({"title": "Story Generation Error - Please re-check your Parameters - Error Code : 401"})
        img_prompt = title_storyOutline_imgPrompt['image_prompt']
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"title": "Story Generation Error - Please re-check your Parameters - Error Code : 502"})
    
    thumb_img_path = save_img___from_link_to_local(create_image(img_prompt), index)
    timestamp = datetime.utcnow()
    # audio_path = text_to_audio_generate(story, index)
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
