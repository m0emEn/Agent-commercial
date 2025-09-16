# server_openrouter.py
from flask import Flask, request, jsonify
import requests
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})  

OPENROUTER_API_KEY = "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"

def load_products_profiles():
    """Load the products profiles from JSON file"""
    try:
        with open('products_profiles.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: products_profiles.json not found. Product filtering will be disabled.")
        return {}
    except Exception as e:
        print(f"Error loading products_profiles.json: {e}")
        return {}

PRODUCTS_PROFILES = load_products_profiles()

def filter_valid_products(age, job, recommended_products):
    """Filter products based on client profile and products database"""
    if not PRODUCTS_PROFILES:
        return recommended_products  # Return all if no filtering data available
    
    valid_products = []
    job_lower = job.lower() if job else ""
    
    for product in recommended_products:
        if product not in PRODUCTS_PROFILES:
            continue  # Skip unknown products
        
        target_profiles = PRODUCTS_PROFILES[product].lower()
        is_valid = False
        
        # Check for specific job matches
        job_matches = {
            'médecin': ['médecins', 'professions libérales', 'cabinets médicaux'],
            'docteur': ['médecins', 'professions libérales', 'cabinets médicaux'],
            'pharmacien': ['pharmaciens', 'professions libérales'],
            'infirmier': ['auxiliaires médicaux', 'professions libérales'],
            'chef': ['restaurants', 'chefs', 'traiteurs', 'profession culinaire'],
            'coiffeur': ['coiffeurs', 'salons de beauté'],
            'commerçant': ['commerçants', 'artisans', 'petites entreprises'],
            'agriculteur': ['agriculteurs', 'exploitants agricoles'],
            'entrepreneur': ['dirigeants', 'entreprises', 'pme']
        }
        
        # Check job-specific matches
        for job_key, target_list in job_matches.items():
            if job_key in job_lower:
                if any(target in target_profiles for target in target_list):
                    is_valid = True
                    break
        
        # Check age-based matches
        if age and age >= 60:
            if any(keyword in target_profiles for keyword in ['seniors', 'retraités', 'personnes âgées']):
                is_valid = True
        
        # Check generic matches
        generic_profiles = ['particuliers', 'familles', 'adultes', 'chefs de famille', 'personnes']
        if any(profile in target_profiles for profile in generic_profiles):
            is_valid = True
        
        # Exclude highly specialized products that don't match
        exclude_keywords = [
            'propriétaires de bateaux', 'plaisanciers', 'armateurs', 'pêcheurs',
            'importateurs/exportateurs', 'entreprises expédiant', 'chantiers navals',
            "exploitants d'aviation", "propriétaires d'aéronefs"
        ]
        
        if any(keyword in target_profiles for keyword in exclude_keywords):
            is_valid = False
        
        # Special case: credit insurance only for actual borrowers
        if 'capital décroissant' in product.lower():
            # This should only be offered to actual borrowers, not as general recommendation
            is_valid = False
        
        if is_valid:
            valid_products.append(product)
    
    return valid_products

def create_enhanced_prompt(age, job,etaFam, recommended_products, client_type):
    """Create enhanced prompt with product information"""
    
    if client_type != 'MORALE':
        
            
        prompt = f"""Vous êtes un employé de BH Assurance.

PROFIL CLIENT: {job} de {age} ans ,etat familial:{etaFam}

MAPPING DES PRODUITS ET LES PROFILES CIBLES:{PRODUCTS_PROFILES}

INSTRUCTIONS:
- Le Client n'est pas une entreprise!
- Créez un pitch commercial professionnel en français
- Utilisez uniquement les produits listés ci-dessus 
- Si la proffession du client n'est pas dans LES PROFILES CIBLES utilise ses recommandation :{recommended_products} 
- Expliquez pourquoi chaque produit correspond à ce profil client
- donnez-moi seulement les 5 meilleurs produits qui correspondent vraiment au client. S'il n'y en a pas 5, vous pouvez en choisir moins.
- le pitch doit être un paragraphe complet sans liste de produits
- Ton professionnel, pas de salutations
- Pitch personnalisé et convaincant


RÉPONSE: Pitch commercial uniquement."""

    

    else:
        # For MORALE (business) clients
        prompt = f"""Vous êtes un employé de BH Assurance.

Créez un pitch commercial pour une entreprise du secteur: {job}

MAPPING DES PRODUITS ET LES PROFILES CIBLES:{PRODUCTS_PROFILES}


INSTRUCTIONS:
- Créez un pitch commercial professionnel en français
- Utilisez uniquement les produits listés ci-dessus 
- Si le secteur du entreprise est 'AUCUN' utilise ses recommandation :{recommended_products} 
- Expliquez pourquoi chaque produit correspond à ce profil client
- le pitch doit être un paragraphe complet sans liste de produits
- Ton professionnel, pas de salutations
- Pitch personnalisé et convaincant


RÉPONSE: Pitch commercial uniquement."""
    return prompt

@app.route("/generate_pitch", methods=["POST"])
def generate_pitch():
    """
    Expects JSON:
    {
        "client_id": 47836,
        "age": 35,
        "job": "Médecin",
        "type": "PHYSIQUE",
        "etatFam"
        "recommended_products": ["Product A", "Product B"]
    }
    Returns a JSON with the pitch.
    """
    data = request.json
    
    client_id = data.get("client_id")
    age = data.get("age")
    job = data.get("job")
    etaFam=data.get("etaFam")
    client_type = data.get("type")
    recommended_products = data.get("recommended_products")
    
    if not client_id or not recommended_products:
        return jsonify({"error": "Missing client_id or recommended_products"}), 400
    
    # Create enhanced prompt with product validation
    prompt = create_enhanced_prompt(age, job,etaFam, recommended_products, client_type)
    print("\n\n\n\n",prompt)
    # OpenRouter API request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat-v3.1:free",  # You can choose another model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        pitch = result["choices"][0]["message"]["content"].strip().replace("**", "")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Debug info (optional)
    debug_info = {}
    if client_type != 'MORALE':
        valid_products = filter_valid_products(age, job, recommended_products)
        debug_info = {
            "original_products": recommended_products,
            "filtered_products": valid_products,
            "products_database_loaded": len(PRODUCTS_PROFILES) > 0
        }
    
    return jsonify({
        "client_id": client_id,
        "pitch": pitch,
        "debug": debug_info
    })

@app.route("/reload_products", methods=["POST"])
def reload_products():
    """Reload products profiles from JSON file"""
    global PRODUCTS_PROFILES
    PRODUCTS_PROFILES = load_products_profiles()
    return jsonify({
        "message": "Products profiles reloaded",
        "products_count": len(PRODUCTS_PROFILES)
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "products_loaded": len(PRODUCTS_PROFILES),
        "api_key_configured": bool(OPENROUTER_API_KEY)
    })

if __name__ == "__main__":
    print(f"Server starting... Products loaded: {len(PRODUCTS_PROFILES)}")
    app.run(debug=True)