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

# @title LLM
async def get_chat_response_openai(
    system_message: str, user_request: str, GPT_MODEL: str = "gpt-4o-2024-05-13", seed: int = None, temperature: float = 0.7
):
    try:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_request},
        ]

        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            seed=seed,
            max_tokens=4000,
            temperature=temperature,
        )

        response_content = response.choices[0].message.content
        system_fingerprint = response.system_fingerprint
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.total_tokens - response.usage.prompt_tokens

        return response_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# @title LLM
async def get_chat_response_openai_json(
    system_message: str, user_request: str, GPT_MODEL: str = "gpt-4o-2024-05-13", seed: int = None, temperature: float = 0.7
):
    try:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_request},
        ]

        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            response_format={ "type": "json_object" },
            seed=seed,
            max_tokens=4000,
            temperature=temperature,
        )

        response_content = response.choices[0].message.content
        system_fingerprint = response.system_fingerprint
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.total_tokens - response.usage.prompt_tokens

        return response_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



# @title Write prompt openai
from IPython.display import display, HTML, Image, Audio
import base64
import markdown2
import asyncio
import json
async def main():
    # @markdown Prompt for making plot
    model = 'gpt-4o-2024-05-13' # @param ["gpt-3.5-turbo-0125", "gpt-4-turbo-2024-04-09", "gpt-4o-2024-05-13"]
    system_message = "Outline Détaillé de l'Histoire  Introduction du Personnage: {characters}, {age} ans, caractérisé(e) par les émotions {emotions} et motivé(e) par les valeurs {positive_values}. Contexte initial soulignant comment {characters} est impliqué(e) dans le scénario {scenario}. Situation Initiale et Cadre: Description détaillée de l'environnement où {characters} commence son aventure. Présentation des acteurs secondaires clés et leur relation initiale avec {characters}. Développement du Conflit et Obstacles: Obstacle 1: Description d'un défi physique ou mental que {characters} doit surmonter. Inclure les détails de l'obstacle et comment il est directement lié à {scenario}. Énigme 1: Présentation d'une énigme complexe qui doit être résolue pour progresser. Détail des indices disponibles et processus de réflexion de {characters} pour la résoudre. Interactions Dynamiques: Exploration approfondie des relations entre {characters} et les autres personnages, montrant comment ces interactions sont influencées par {emotions} et comment elles évoluent tout au long de l'histoire. Chaque interaction importante doit refléter ou tester les valeurs {positive_values} de {characters}. Apogée: Description du moment le plus intense du conflit, où {characters} est confronté(e) à un choix crucial ou à un ultime défi. Détails sur la manière dont {characters} utilise ses émotions {emotions} et ses valeurs {positive_values} pour naviguer dans cette situation. Résolution: Comment {characters} résout le conflit principal, détaillant les étapes spécifiques et les décisions prises. Impact de la résolution sur {characters} et les autres personnages principaux. Conclusion: Synthèse de ce que {characters} a appris à travers cette aventure. Effets à long terme des actions de {characters} sur l'environnement et le contexte initial." #@param {type:"string"}
    prompt_input1 = "HISTOIRE POUR MAYANA 3ANS LHISTOIRE DU LOUP ET DU CHAPERON ROUGE, EMOTION PEUR ET JOIE, VALEUR PARTAGE ET PERSEVERANCE" #@param {type:"string"}
    expected_response = """
    {
        "type": "object",
        "properties": {
            "story": {"type": "string"}
            "title": {"type": "string"},
        },
        "required": ["title", "story"]
    }
    """

    user_input = prompt_input1 + " You return output in JSON format"+ expected_response
    plot_with_title = await get_chat_response_openai_json(system_message, user_input,model)
    # plot_with_title = get_chat_response(system_message, user_input)
    plot_with_title = plot_with_title.strip().strip('`').strip('json').strip('').replace('\n', '')

    print("plot_with_title")
    print(repr(plot_with_title))


    response_json = json.loads(plot_with_title)
    plot = response_json['story']
    title = response_json['title']
    # print(plot)
    # print(title)
    # Update system message for the continuation

    # @markdown Prompt for making story using the plot
    system_message = "You are an expert at generating long stories based on a given synopsis" #@param {type:"string"}

    # Construct user input for story expansion

    prompt_input_2 = "Prompt pour Générer une Histoire de 2000 Mots  En utilisant l'outline généré, créez-moi une histoire de 2000 mots qui plonge le lecteur dans un univers captivant et unique. Débutez par décrire le cadre de l'histoire de manière vivante et détaillée, en faisant appel à l'imagination des jeunes lecteurs. Introduisez les personnages principaux en soulignant leurs traits de caractère distinctifs, leurs motivations profondes, et la manière dont ils se rapportent à leur monde.  Faites démarrer l'aventure avec un événement qui pousse les personnages hors de leur zone de confort, les lançant sur le chemin de la découverte et du défi. Tissez le récit autour d'une série de péripéties qui testent leurs limites, les font grandir et révèlent progressivement les émotions et les valeurs clés que vous souhaitez explorer, telles que le courage, l'amitié, la persévérance, et la curiosité.  Pour chaque quête donnée par l'outline, développez-la en décrivant comment les personnages gèrent et surmontent ces défis en détail. Ne traversez pas ces quêtes rapidement; plongez profondément dans chaque action, décrivant comment ils ont fait face à chaque situation, enrichissant ainsi le récit avec des descriptions vivantes et des réflexions approfondies sur leurs expériences.  Construisez l'histoire en veillant à ce que chaque scène contribue à l'avancement du récit vers son apogée, un moment de tension dramatique où les personnages font face à leur plus grand défi, mettant en jeu les leçons apprises au cours de leur voyage. Assurez-vous que la résolution de l'histoire est à la fois satisfaisante et porteuse de sens, reflétant les valeurs positives et offrant une conclusion qui encourage à la réflexion personnelle.  Intégrez des éléments narratifs enrichissants comme des jeux de langage, des dialogues, un rythme engageant, et des interactions imaginatives avec le lecteur pour rendre la lecture ou l'écoute de l'histoire plus dynamique et immersive. L'histoire devrait non seulement divertir mais aussi éduquer et inspirer les jeunes lecteurs, en les invitant à voir le monde sous un jour nouveau.  Tout au long du récit, maintenez un langage adapté à l'âge cible, en évitant toute vulgarité ou violence explicite, pour assurer que l'histoire soit appropriée et agréable pour un public enfantin. Finalement, concluez l'histoire de manière à laisser une impression durable, encourager l'imagination, et inspirer les jeunes esprits à rêver grand.  Instructions Supplémentaires:  Assurez-vous que le récit atteint un minimum de 2000 mots pour une expérience de lecture complète. L'histoire doit être fluide et cohérente, avec une transition naturelle entre les scènes et les événements. Le titre de l'histoire doit capturer l'essence du récit et intriguer le lecteur dès le début. Je souhaite que l'histoire soit générée sans commentaire supplémentaire et qu'elle se termine par 'Fin.'" #@param {type:"string"}
    user_input = plot + prompt_input_2

    # Call the get_chat_response function to expand on plot
    long_story = await get_chat_response_openai(system_message, user_input, model)
    # long_story = get_chat_response(system_message, user_input)

    # print("long_story")
    # print(long_story)


    # Update system message for generating image prompts
    system_message = "You are an expert at generating prompts for image generation models"

    # Construct user input for image prompt generation
    user_input = plot[:250] + " please make a single prompt using the given details"

    audio_file_path = generate_speech(title,long_story)

    # Call the get_chat_response function to generate image prompt
    image_prompt = await get_chat_response_openai(system_message, user_input,model)
    # image_prompt = get_chat_response(system_message, user_input)
    print("Image_prompt")
    print(image_prompt)

    image_location = generate_image(image_prompt)



    text_content=f"## {title}\n\n"+long_story

    