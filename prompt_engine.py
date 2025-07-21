import os
import glob
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Old version of call_model function
# def call_model(prompt: str) -> str:
#     return f"[SIMULATED INSIGHT] {prompt}"

# New version of call_model function
def call_model(prompt: str, use_real_model: bool = False) -> str:
    """Call model with option to use real LLM or simulation."""
    
    if not use_real_model:
        return f"[SIMULATED INSIGHT] {prompt}"
    
    # Check for API key
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        print("Warning: No COHERE_API_KEY found in environment. Falling back to simulation.")
        return f"[SIMULATED INSIGHT] {prompt}"
    
    try:
        # Initialize Cohere client
        co = cohere.Client(api_key)
        
        # Make API call
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        
        return response.generations[0].text.strip()
        
    except Exception as e:
        print(f"Error calling Cohere API: {e}")
        print("Falling back to simulation...")
        return f"[SIMULATED INSIGHT] {prompt}"

def load_facts():
    """Load facts from data/raw/facts_*.txt files."""
    facts = []
    
    # Find all facts files
    fact_files = glob.glob("data/raw/facts_*.txt")
    
    for file in fact_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse facts from file
        blocks = content.split("-" * 60)
        for block in blocks:
            lines = block.strip().split('\n')
            for line in lines:
                if line.startswith("Text: "):
                    facts.append(line[6:])  # Remove "Text: " prefix
    
    return facts
# Old version of process_facts function
# def process_facts():
#     """Load facts and process each with a prompt."""
#     facts = load_facts()
#     results = []
    
#     for fact in facts:
#         # Generate prompt for each fact
#         prompt = f"Explain why this fun fact is interesting to humans: {fact}"
        
#         # Get response from model
#         insight = call_model(prompt)
        
#         results.append({
#             'fact': fact,
#             'insight': insight
#         })
    
#     return results

# New version of process_facts function
def process_facts(use_real_model=False):
    """Load facts and process each with a prompt."""
    facts = load_facts()
    results = []
    
    for fact in facts:
        # Generate prompt for each fact
        prompt = f"Explain why this fun fact is interesting to humans: {fact}"
        
        # Get response from model
        insight = call_model(prompt, use_real_model)
        
        results.append({
            'fact': fact,
            'insight': insight
        })
    
    return results

if __name__ == '__main__':
    # results = process_facts()
    results = process_facts(use_real_model=True)  # Use real model by default when run directly
    for result in results:
        print(f"Fact: {result['fact']}")
        print(f"Insight: {result['insight']}")
        print("-" * 50)