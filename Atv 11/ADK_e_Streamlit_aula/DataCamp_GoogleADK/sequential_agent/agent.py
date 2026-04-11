import os

from dotenv import load_dotenv

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

print("DEBUG KEY:", os.getenv("GOOGLE_API_KEY"))
#model = LiteLlm(
#    model="openrouter/google/gemini-2.5-flash",
#    api_key=os.getenv("OPENROUTER_API_KEY")
#)

# Recipe Research Agent - encontra  os ingredientes e os metodos de preparo
recipe_research_agent = Agent(
    name="RecipeResearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search], # ferramenta dele é a busca no google
    description="An agent that researches recipe ideas and ingredients for a given dish concept",
    instruction="""
    You are a culinary researcher. You will be given a dish concept and you will research:
    - Best ingredients and their combinations
    - Popular cooking methods for this dish
    - Key flavor profiles and techniques
    Provide a summary that will help create a complete recipe.
    """,
    output_key="recipe_research",
)

# Recipe Creator Agent - Cria de fato a receita com o que foi passado pelo RecipeResearchAgent no contexto (output_key="recipe_research")
recipe_creator_agent = Agent(
    model="gemini-2.0-flash",
    name="RecipeCreatorAgent",
    description="An agent that creates complete recipes with ingredients and cooking instructions",
    instruction="""
    You are a professional chef. Using the research from "recipe_research" output, create a complete recipe that includes:
    - Recipe title and brief description
    - Ingredient list with measurements
    - Step-by-step cooking instructions
    - Cooking time and servings
    - Basic nutritional highlights
    Make it clear and easy to follow for home cooks.
    """,
    output_key="final_recipe", #Guarda em context o output
)

# Recipe Enhancement Agent - Insere dicas e orientações para a receita enviada pelo recipe_creator_agent
recipe_enhancement_agent = Agent(
    model="gemini-2.0-flash",
    name="RecipeEnhancementAgent",
    description="An agent that adds cooking tips and recipe variations",
    instruction="""
    You are a cooking instructor. Using the recipe from "final_recipe" output, enhance it by adding:
    - 3-4 helpful cooking tips
    - 2-3 recipe variations or substitutions
    - Storage and serving suggestions
    
    Format the final output as:
    
    RECIPE: {final_recipe}
    
    COOKING TIPS: [your tips here]
    
    VARIATIONS: [your variations here]
    """,
)

# Esse é o agente raiz, que irá orquestrar os demais, Além disso o criamos como SequentialAgent 
# pois os subagentes que estabelecermos na lista serão chamados em ordem, sequencialmente
root_agent = SequentialAgent(
    name="RecipeDevelopmentSystem",
    description="A simple system that researches, creates, and enhances recipes",
    sub_agents=[recipe_research_agent, recipe_creator_agent, recipe_enhancement_agent],
)
