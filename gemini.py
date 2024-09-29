import google.generativeai as genai
import os
from dotenv import load_dotenv
import PIL.Image

load_dotenv()
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)



species_info = {
    "Native Species": "Species naturally found in the region, crucial for local biodiversity.",
    "Non-Harmful Invasive Species": "Invasive species that have minimal or no negative impact on the local environment.",
    "Beneficial Invasive Species": "Non-native species that contribute positively to the ecosystem or provide economic benefits.",
    "Harmful Invasive Species (Control Required)": "Species that cause harm to the ecosystem or economy and should be actively managed or removed.",
    "Critical Invasive Species (Immediate Action)": "Highly destructive invasive species that need to be reported and controlled immediately to prevent further damage.",
    "Endangered Species": "Species at risk of extinction that require urgent protection and conservation efforts."
}

def getDex(image, location):
    model = genai.GenerativeModel('gemini-1.5-pro')
    file = PIL.Image.open(image)
    prompt = "Only respond True or False to this image being a real plant or animal? Don't add any spaces or newlines."
    response = model.generate_content([prompt, file])
    realSpecies = response.text == "True"
    
    prompt = "Only respond True or False to there being a species in this image, it does not have to be real. ? Don't add any spaces or newlines."
    response = model.generate_content([prompt, file])
    species = response.text == "True"

    #if (not species):
#        prompt = f"""Give a give sources for what this object is"""
#        response = model.generate_content([prompt, file])
#        sources = response.text
#        realSpecies = False
#        desc = "N/A"
#        type = "N/A"
#        help = "N/A"
#        typeDesc = "N/A"
#        return realSpecies, desc, type, help, sources, typeDesc
    
    prompt = f"""
    I will give you multiple prompts, answer them and separate them with newlines. Here are the prompts: 
    1. Only respond True or False to this image being a real plant or animal. Don't add any unnessary newlines.
    2. Only respond True or False to there being a species in this image, it does not have to be real. Don't add any unnessary newlines.
    3. Give a 3 sentence description of this species. Don't add any unnessary newlines.
    4. Only respond with these descriptions based on this location of the animal, {location}: Native Species, Non-Harmful Invasive Species, Beneficial Invasive Species, Harmful Invasive Species (Control Required), Critical Invasive Species (Immediate Action), Endangered Species. Don't add any unnecessary newlines.
    5. Give a 3 sentence explanation of how we can help this species based on location {location}. Don't add any unnecessary spaces or newlines.
    """
    response = model.generate_content([prompt, file])

    responses = response.text.split("\n")

# Map the responses to specific variables
    realSpecies = "True" in responses[0]  # Real plant or animal
    species = "True" in responses[1]  # Species in image (real or not)
    desc = responses[2]  # 3-sentence description
    type = ""
    for word in species_info:
        if word in responses[3]:
            type = word
            break
    help = responses[4]  # 3-sentence help explanation based on location

# Print or manipulate the answers as needed
    return realSpecies, species, desc, type, help
