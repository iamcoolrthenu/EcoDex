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

    if (not species):
        prompt = f"""Give a give sources for what this object is"""
        response = model.generate_content([prompt, file])
        sources = response.text
        realSpecies = False
        desc = "N/A"
        type = "N/A"
        help = "N/A"
        typeDesc = "N/A"
        return realSpecies, desc, type, help, sources, typeDesc
    
    prompt = "Give a short description of this species. Don't add any unnessary spaces or newlines."
    response = model.generate_content([prompt, file])
    desc = response.text

    prompt = f"""Only respond With these descriptions based on this location of the animal, {location} : Native Species, Non-Harmful Invasive Species, Beneficial Invasive Species, Harmful Invasive Species (Control Required), Critical Invasive Species (Immediate Action), Endangered Species. Don't add any unnessary spaces or newlines."""
    response = model.generate_content([prompt, file])
    type = response.text

    prompt = f"""Give a short explanation of how we can help this species based on location {location}. Don't add any unnessary spaces or newlines."""
    response = model.generate_content([prompt, file])
    help = response.text

    prompt = f"""Give a give sources for ways to help this species, descriptions of it, whether it being native or endangered or invasive based on the location: {location}"""
    response = model.generate_content([prompt, file])
    sources = response.text

    typeDesc = species_info[type]

    return realSpecies, desc, type, help, sources, typeDesc
print(getDex("girl.png","Kanto"))
