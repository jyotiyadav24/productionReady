import re
import os
import requests
from PIL import Image
import gradio as gr
import warnings
import logging
import io
import base64
from io import StringIO
from fastapi import UploadFile
warnings.filterwarnings("ignore")
from transformers import pipeline
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.router import MultiPromptChain
from dotenv import load_dotenv, find_dotenv
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

# Load environment variables
config = find_dotenv(".env")
load_dotenv()

groq_api = os.getenv("GROQ_API_KEY")


def image_to_prompt(image_path):
    captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    result = captioner(image_path)
    
    # Extract and return the text part
    text_parts = [item['generated_text'] for item in result]
    return text_parts


def initialize_zero_shot_agent(prompt,temp,max_tokens,top_p,frequency_penalty,presence_penalty):
    llm = ChatGroq(temperature=temp,
                   groq_api_key=groq_api,
                   model_name="mixtral-8x7b-32768",
                   max_tokens=max_tokens,
                   top_p=top_p,
                   frequency_penalty=frequency_penalty,
                   presence_penalty=presence_penalty)
    
    wikipedia = WikipediaAPIWrapper()
    search = DuckDuckGoSearchRun()
    #google_search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)

    wikipedia_tool = Tool(
        name='wikipedia',
        func=wikipedia.run,
        description="Useful for when you need to look up a topic, country or person on Wikipedia, the best website for fact-checking and finding details on any subject."
    )

    duckduckgo_tool = Tool(
        name='DuckDuckGo Search',
        func=search.run,
        description="Useful for when you need to do a search on the internet to find information that another tool can't find. Always be specific with your input."
    )


    #google_search=(
    #Tool(
    #    name="Google Search",
    #    func=google_search.run,
    #    description="Useful to search in Google. Use by default.",
    #    )
    #  )
    
    tools = [
        Tool(
            name="Wikipedia Search",
            func=wikipedia.run,
            description="Useful for when you need to answer questions from the internet."
        )
    ]

    zero_shot_agent = initialize_agent(
        agent="zero-shot-react-description",
        tools=tools,
        llm=llm,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
    )

    return zero_shot_agent.run(prompt)


def menu_prompt(input):
    prompt_menu = f"""
    As a restaurant menu manager, your role is to gather below informations based on input data {input} (Name of the dish).
    generate the output
    ### information to be extracted :
    <Ingredients>: Only Ingredients included in the dish.
    <Description>: Briefly describe the dish.
    <Allergens>: Only Choose relevant options from this list - [Cereals, Crustaceans, Egg, Fish, Peanuts, SOYBEAN, Latte, Nuts, Celery, Mustard, Sesame seeds, Sulfur dioxide and sulphites, Shell, Clams].
    <Additional Information>: Only Choose relevant options from this list - [Spicy, Vegan, Gluten free, Vegetarian].
    ### Output Format
    {{
    ingredients: All Ingredients in a List,
    description: Description in a string,
    allergen: All allergen in a List,
    Additional_information: All Additional_information in a List
    }}
    ### Input data:
     {input}
    ### Output:
    """
    return prompt_menu


def social_media_prompt(input,image):
    prompt_social_media = f'''
    As the social media manager of the restaurant, your task is to craft four Social Media Posts for Restaurant for their Facebook and Instagram pages based on the Input data [which contains a goal for the posts and Image description which is an additonal information for helping to write a posts] .
    
    ### Guidelines:
    * Craft the post with the goal of highlighting Input data.
    * Incorporate 3-5 emojis, ensuring no more than one emoji is used every two sentences.
    * Mention a maximum of 1 or 2 products from the menu.
    * Remember that social media posts are part of a content plan, not sponsored content.
    * Focus on showcasing the restaurant's strengths rather than directly promoting sales.
    * Include a Call to Action mentioning information such as opening hours, restaurant address, telephone number, or WhatsApp number, if available.
    * Direct audience attention to the online menu available at www.restaurants.menu.
    * Utilize hashtags at the end of the description, relevant to the content and objectives. Use the # symbol to add hashtags.
    
    ### Information to be Extracted:
    Generate four posts based on the above guidelines.
    
    ### Output Format:
    {{
    "Post1": "This is the content of Post 1.",
    "Post2": "This is the content of Post 2.",
    "Post3": "This is the content of Post 3.",
    "Post4": "This is the content of Post 4."
    }}
    
    ### Input data:
    {input}{image}
    
    ### Output:
    '''
    return prompt_social_media



def advertising_prompt(input,buyersPersonas):
    advertising_menu = f'''
    As the advertising manager of the restaurant, your task is to create compelling ad copy for a restaurant's based on the Input data [which contains a goal for the descriptions and Buyers Personas which is an additonal information for helping to write a descriptions] .
    The restaurant aim to attract a specific target audience described as the Buyers Personas.
    
    ### Guidelines:
    * The Call to Action should target the Buyer Personas.
    * Use emojis in the ad copy only if necessary.
    * Mention 2 products from menu.
    * Generated ad copy should be in only English language.
    * Create content related hashtags at the end of the ad copy.
    * Do not use restaurant info directly, use inside the generated ad text.
    ### Information to be Extracted:
    Generate four descriptions based on the above guidelines.
    
    ### Output Format:
    {{
    "Description1": "This is the content of Description 1.",
    "Description2": "This is the content of Description 2.",
    "Description3": "This is the content of Description 3.",
    "Description4": "This is the content of Description 4."
    }}
    
    ### Input data:
    {input}{buyersPersonas}
    ### Output:
    '''

    return advertising_menu


def menu_extract_dictionary(text):
    pattern = r'\{[^{}]*\}'  # Regular expression pattern to match text within flower brackets
    matches = re.findall(pattern, text)
    result = ""
    for match in matches:
        if any(key in match for key in ['ingredients', 'description', 'allergen', 'Additional_information']):
            result += match + "\n"
    return result


def social_extract_dictionary(text):
    pattern = r'\{[^{}]*\}'  # Regular expression pattern to match text within flower brackets
    matches = re.findall(pattern, text)
    result = ""
    for match in matches:
        if any(key in match for key in ['Post1', 'Post2', 'Post3','Post4']):
            result += match + "\n"
    return result

def advertising_extract_dictionary(text):
    pattern = r'\{[^{}]*\}'  # Regular expression pattern to match text within flower brackets
    matches = re.findall(pattern, text)
    result = ""
    for match in matches:
        if any(key in match for key in ['Description1', 'Description2', 'Description3', 'Description4']):
            result += match + "\n"
    return result

def newsletter_extract_dictionary(text):
    pattern = r'\{[^{}]*\}'  # Regular expression pattern to match text within flower brackets
    matches = re.findall(pattern, text)
    result = ""
    for match in matches:
        if any(key in match for key in ['campaignName', 'campaignObject', 'campaignEmail']):
            result += match + "\n"
    return result

def newsletter_prompt(input):
    prompt_newsletter = f'''
    As a Newsletter Manager, your task is to extract informations based on the input data {input}.
    ### information to be extracted :
    <campaign Name>: Identifies a marketing initiative
    <campaign Object>: Defines the primary goal of a marketing campaign
    <campaign Email>: Communication sent via email as part of a marketing campaign.
    ### Output Format
    {{
      "campaignName": [Suggest some good campaign Name]
      "campaignObject": [Suggest some good campaign Object],
      "campaignEmail": [Write a sample campaign Email based on Campaign Name and campaign Object],
    }}
    ### Input data:
     {input}
    ### Output:
    '''
    return prompt_newsletter


def agent_menu(goal):
    print('Triggering Menu')
    prompt_menu=menu_prompt(goal)
    response_agent = initialize_zero_shot_agent(prompt_menu, 0.1, 32000, 0.1, 0.1, 0.1)
    response_agent=menu_extract_dictionary(response_agent)
    print('Finish Triggering Menu')
    return response_agent


def agent_socialMedia(goal, image):
    print('Triggering Social Media')
    image_description = image_to_prompt(image)
    prompt_social_media = social_media_prompt(goal, image_description)
    response_agent = initialize_zero_shot_agent(prompt_social_media, 0.8, 32000, 0.7, 0.4, 0.4)
    response_agent = social_extract_dictionary(response_agent)
    return response_agent


def agent_advertising(goal,buyersPersonas):
    print('Triggering Advertising')
    prompt_advertising=advertising_prompt(goal,buyersPersonas)
    response_agent = initialize_zero_shot_agent(prompt_advertising, 0.8, 32000, 0.7, 0.4, 0.4)
    response_agent=advertising_extract_dictionary(response_agent)
    return response_agent


def agent_newsletter(goal):
    print('Triggering Newsletter')
    prompt_newsletter=newsletter_prompt(goal)
    response_agent = initialize_zero_shot_agent(prompt_newsletter, 0.8, 32000, 0.7, 0.4, 0.4)
    response_agent=newsletter_extract_dictionary(response_agent)
    return response_agent
