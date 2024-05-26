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

Outline Détaillé de l'Histoire  Introduction du Personnage: {characters}, {age} ans, caractérisé(e) par les émotions {emotions} et motivé(e) par les valeurs {positive_values}. Contexte initial soulignant comment {characters} est impliqué(e) dans le scénario {scenario}. Situation Initiale et Cadre: Description détaillée de l'environnement où {characters} commence son aventure. Présentation des acteurs secondaires clés et leur relation initiale avec {characters}. Développement du Conflit et Obstacles: Obstacle 1: Description d'un défi physique ou mental que {characters} doit surmonter. Inclure les détails de l'obstacle et comment il est directement lié à {scenario}. Énigme 1: Présentation d'une énigme complexe qui doit être résolue pour progresser. Détail des indices disponibles et processus de réflexion de {characters} pour la résoudre. Interactions Dynamiques: Exploration approfondie des relations entre {characters} et les autres personnages, montrant comment ces interactions sont influencées par {emotions} et comment elles évoluent tout au long de l'histoire. Chaque interaction importante doit refléter ou tester les valeurs {positive_values} de {characters}. Apogée: Description du moment le plus intense du conflit, où {characters} est confronté(e) à un choix crucial ou à un ultime défi. Détails sur la manière dont {characters} utilise ses émotions {emotions} et ses valeurs {positive_values} pour naviguer dans cette situation. Résolution: Comment {characters} résout le conflit principal, détaillant les étapes spécifiques et les décisions prises. Impact de la résolution sur {characters} et les autres personnages principaux. Conclusion: Synthèse de ce que {characters} a appris à travers cette aventure. Effets à long terme des actions de {characters} sur l'environnement et le contexte initial.

Generate a Captivating, and Interesting title (not a generic one) , based on this outline in french.

Rule (Don't Ignore) : Use this python dictionary format for output and make the response to escape special characters, so that i can directly use the response, and keep the "title" and "story" ; the keys of the json in english...

{{"title": "<title_here_in_string_format>", "story": "<story_here_in_string_format>"}}
"""
    
    else:
        
        # --------------------  Prompt for other (ENGLISH) language  -----------------------------

        # Prompt To be added Later
        vulgar_prompt_for_english = f"""
If these words : \" {characters}, {scenario}, {positive_values}, {emotions} \" are vulger for a kid, then only return : {{"title": "error"}} and nothing else."""
        
        
        prompt_template = f"""

Detailed Story Outline:

Character Introduction: {characters}, {age} years old, characterized by the emotions {emotions} and motivated by the values {positive_values}. Initial context highlighting how {characters} is involved in the scenario {scenario}.

Initial Situation and Setting: Detailed description of the environment where {characters} begins their adventure. Introduction of key secondary characters and their initial relationship with {characters}.

Conflict Development and Obstacles:

- Obstacle 1: Description of a physical or mental challenge that {characters} must overcome. Include details of the obstacle and how it is directly related to {scenario}.
- Puzzle 1: Introduction of a complex puzzle that must be solved to progress. Detail the available clues and the thought process of {characters} to solve it.

Dynamic Interactions: In-depth exploration of the relationships between {characters} and other characters, showing how these interactions are influenced by {emotions} and how they evolve throughout the story. Each important interaction should reflect or test the {positive_values} of {characters}.

Climax: Description of the most intense moment of the conflict, where {characters} faces a crucial choice or an ultimate challenge. Details on how {characters} uses their {emotions} and {positive_values} to navigate this situation.

Resolution: How {characters} resolves the main conflict, detailing the specific steps and decisions taken. Impact of the resolution on {characters} and the other main characters.

Conclusion: Synthesis of what {characters} has learned through this adventure. Long-term effects of {characters}' actions on the environment and initial context.

Generate a Captivating, and Interesting title (not a generic one) , based on this outline.

Rule (Don't Ignore) : Use this python dictionary format for output and make the response to escape special characters, so that i can directly use the response.

{{"title": <title_here_in_string_format>, "story": <story_here_in_string_format>}}

"""

    # ----------------  OPENAI Generation Code LLM ----------------------

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4o-2024-05-13",
      max_tokens=4000,
      seed = None,
      temperature = 0.7,
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

    if lang == "french":
    
        prompt_template = f"""
    
    Prompt pour Générer une Histoire de 2000 Mots  En utilisant l'outline généré, créez-moi une histoire de 2000 mots qui plonge le lecteur dans un univers captivant et unique. Débutez par décrire le cadre de l'histoire de manière vivante et détaillée, en faisant appel à l'imagination des jeunes lecteurs. Introduisez les personnages principaux en soulignant leurs traits de caractère distinctifs, leurs motivations profondes, et la manière dont ils se rapportent à leur monde.  Faites démarrer l'aventure avec un événement qui pousse les personnages hors de leur zone de confort, les lançant sur le chemin de la découverte et du défi. Tissez le récit autour d'une série de péripéties qui testent leurs limites, les font grandir et révèlent progressivement les émotions et les valeurs clés que vous souhaitez explorer, telles que le courage, l'amitié, la persévérance, et la curiosité.  Pour chaque quête donnée par l'outline, développez-la en décrivant comment les personnages gèrent et surmontent ces défis en détail. Ne traversez pas ces quêtes rapidement; plongez profondément dans chaque action, décrivant comment ils ont fait face à chaque situation, enrichissant ainsi le récit avec des descriptions vivantes et des réflexions approfondies sur leurs expériences.  Construisez l'histoire en veillant à ce que chaque scène contribue à l'avancement du récit vers son apogée, un moment de tension dramatique où les personnages font face à leur plus grand défi, mettant en jeu les leçons apprises au cours de leur voyage. Assurez-vous que la résolution de l'histoire est à la fois satisfaisante et porteuse de sens, reflétant les valeurs positives et offrant une conclusion qui encourage à la réflexion personnelle.  Intégrez des éléments narratifs enrichissants comme des jeux de langage, des dialogues, un rythme engageant, et des interactions imaginatives avec le lecteur pour rendre la lecture ou l'écoute de l'histoire plus dynamique et immersive. L'histoire devrait non seulement divertir mais aussi éduquer et inspirer les jeunes lecteurs, en les invitant à voir le monde sous un jour nouveau.  Tout au long du récit, maintenez un langage adapté à l'âge cible, en évitant toute vulgarité ou violence explicite, pour assurer que l'histoire soit appropriée et agréable pour un public enfantin. Finalement, concluez l'histoire de manière à laisser une impression durable, encourager l'imagination, et inspirer les jeunes esprits à rêver grand.  Instructions Supplémentaires:  Assurez-vous que le récit atteint un minimum de 2000 mots pour une expérience de lecture complète. L'histoire doit être fluide et cohérente, avec une transition naturelle entre les scènes et les événements. Le titre de l'histoire doit capturer l'essence du récit et intriguer le lecteur dès le début. Je souhaite que l'histoire soit générée sans commentaire supplémentaire , sans titre a l'histoire et qu'elle se termine par 'Fin.' . Voici le plan de l'histoire : \"{story}\"

    Rule (Don't Ignore) : Just Provide Only the Story body as string, with no title or anything extra like chapters.

"""

    else:

        prompt_template = f"""

Prompt for Generating a 2000-Word Story

Using the generated outline, create a 2000-word story that immerses the reader in a captivating and unique universe. Start by vividly and detailedly describing the story's setting, appealing to the imagination of young readers. Introduce the main characters by highlighting their distinctive traits, deep motivations, and how they relate to their world.

Begin the adventure with an event that pushes the characters out of their comfort zone, launching them on a path of discovery and challenge. Weave the narrative around a series of events that test their limits, make them grow, and gradually reveal the key emotions and values you wish to explore, such as courage, friendship, perseverance, and curiosity.

For each quest given by the outline, develop it by describing in detail how the characters handle and overcome these challenges. Do not rush through these quests; delve deeply into each action, describing how they faced each situation, thus enriching the narrative with vivid descriptions and in-depth reflections on their experiences.

Build the story ensuring that each scene contributes to advancing the narrative towards its climax, a moment of dramatic tension where the characters face their greatest challenge, putting into play the lessons learned during their journey. Ensure that the story's resolution is both satisfying and meaningful, reflecting positive values and offering a conclusion that encourages personal reflection.

Integrate enriching narrative elements such as wordplay, dialogues, engaging rhythm, and imaginative interactions with the reader to make the reading or listening experience more dynamic and immersive. The story should not only entertain but also educate and inspire young readers, inviting them to see the world in a new light.

Throughout the narrative, maintain language appropriate to the target age, avoiding any vulgarity or explicit violence, to ensure the story is suitable and enjoyable for a child audience. Finally, conclude the story in a way that leaves a lasting impression, encourages imagination, and inspires young minds to dream big.

Additional Instructions:

Ensure that the narrative reaches a minimum of 2000 words for a complete reading experience. The story should be fluid and coherent, with natural transitions between scenes and events. The title of the story should capture the essence of the narrative and intrigue the reader from the start. I want the story to be generated without additional commentary, without a title, and to end with 'The End.'

This is the story outline : \"{story}\"




"""

    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4o-2024-05-13",
      max_tokens=4000,
      seed = None,
      temperature = 0.7,
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
      max_tokens=4000,
      seed = None,
      temperature = 0.7,
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
