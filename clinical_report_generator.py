"""
Clinical Report Generator for AyurAI Veda
Generates detailed Ayurvedic clinical reports using Groq LLM
"""

import os
from datetime import datetime

def generate_clinical_report(user_data, assessment_results):
    """
    Generate comprehensive Ayurvedic clinical report
    
    Args:
        user_data: dict with name, age, gender, location
        assessment_results: dict with dosha scores, dominant dosha, etc.
    
    Returns:
        dict with structured clinical report
    """
    
    # Try to use Groq LLM for intelligent report generation
    try:
        from groq import Groq
        groq_api_key = os.getenv('GROQ_API_KEY')
        
        if groq_api_key:
            return generate_llm_report(user_data, assessment_results, groq_api_key)
    except Exception as e:
        print(f"LLM generation failed: {e}")
    
    # Fallback to rule-based report
    return generate_rule_based_report(user_data, assessment_results)

def generate_llm_report(user_data, assessment_results, api_key):
    """Generate report using Groq LLM"""
    from groq import Groq
    
    client = Groq(api_key=api_key)
    
    # Prepare assessment data
    answers_summary = format_assessment_answers(assessment_results.get('raw_answers', {}))
    
    prompt = f"""You are an advanced Ayurveda Clinical Intelligence System powered by Tridosha Logic (Vata, Pitta, Kapha).

Your task is to:
1. Analyze user responses from Prakriti + Vikriti assessment
2. Identify dominant dosha imbalance
3. Generate a structured, personalized Ayurvedic Clinical Report

-----------------------------------
🔶 INPUT DATA:
- Name: {user_data.get('name', 'User')}
- Age: {user_data.get('age', 'N/A')}
- Gender: {user_data.get('gender', 'N/A')}
- Location: {user_data.get('location', 'N/A')}
- Dominant Dosha: {assessment_results.get('dominant', 'N/A')}
- Dosha Scores: Vata {assessment_results['scores']['vata']}%, Pitta {assessment_results['scores']['pitta']}%, Kapha {assessment_results['scores']['kapha']}%
- Assessment Answers: {answers_summary}
-----------------------------------

⚠️ IMPORTANT RULES:
- Follow pure Ayurvedic principles only (Charaka Samhita, Ashtanga Hridaya based logic)
- Do NOT give modern medical diagnosis
- Keep suggestions natural, preventive, and lifestyle-based
- Use simple but professional language
- Avoid generic advice — make it dosha-specific

-----------------------------------
🔷 OUTPUT FORMAT:

🧾 AYURVEDIC CLINICAL ASSESSMENT REPORT

👤 Personal Details:
- Name: {user_data.get('name', 'User')}
- Age: {user_data.get('age', 'N/A')}
- Gender: {user_data.get('gender', 'N/A')}
- Location: {user_data.get('location', 'N/A')}

-----------------------------------

🧠 Dosha Analysis:
- Dominant Dosha: {assessment_results.get('dominant', 'N/A')}
- Secondary Dosha: [Identify from scores]
- Current Imbalance (Vikriti): [Describe]
- Brief Explanation (2-3 lines)

-----------------------------------

🥗 DIET RECOMMENDATIONS:

✅ Foods to Take:
- [List 5-7 foods balancing dominant dosha]
- Include grains, fruits, vegetables, spices

❌ Foods to Avoid:
- [List 5-7 aggravating foods clearly]

💡 Eating Guidelines:
- [Timing, habits, digestion tips - 3-4 points]

-----------------------------------

🧘 LIFESTYLE RECOMMENDATIONS:

🌿 Daily Routine (Dinacharya):
- Wake-up time
- Sleep time
- Activity suggestions (3-4 points)

🧘♂️ Practices:
- Yoga (dosha-specific poses - 3-4)
- Pranayama (specific techniques)
- Meditation (type and duration)

⚠️ Habits to Avoid:
- [List 3-4 harmful lifestyle patterns]

-----------------------------------

🌱 HERBAL SUPPORT:

🌿 Recommended Herbs:
- [Herb Name] — [Benefit in 1 line] (4-5 herbs)

💊 Usage Guidance:
- Simple form (powder, tea, decoction)
- General timing suggestion

⚠️ Avoid:
- [Herbs that may worsen condition if applicable]

-----------------------------------

🧭 ADDITIONAL WELLNESS ADVICE:
- Seasonal tips (Ritucharya) - 2-3 points
- Stress management suggestions - 2-3 points
- Digestive care - 2-3 points

-----------------------------------

⚠️ DISCLAIMER:
This is an Ayurvedic wellness assessment for educational and preventive purposes only. It is not a medical diagnosis. Consult a qualified Ayurvedic practitioner for treatment.

-----------------------------------

🔶 STYLE REQUIREMENTS:
- Use bullet points (clean formatting)
- Keep it structured and readable
- Avoid long paragraphs
- Make it feel like a professional clinical report

Generate the complete report now."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2500
    )
    
    report_text = response.choices[0].message.content
    
    # Parse the report into structured format
    return parse_llm_report(report_text, user_data, assessment_results)

def generate_rule_based_report(user_data, assessment_results):
    """Generate report using rule-based logic"""
    
    dominant = assessment_results.get('dominant', 'Vata').lower()
    scores = assessment_results.get('scores', {})
    
    # Determine secondary dosha
    sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    secondary = sorted_doshas[1][0].capitalize() if len(sorted_doshas) > 1 else "Balanced"
    
    # Dosha analysis
    dosha_analysis = {
        'dominant_dosha': assessment_results.get('dominant', 'Vata'),
        'secondary_dosha': secondary,
        'vikriti': f"{assessment_results.get('dominant', 'Vata')} imbalance detected",
        'explanation': get_dosha_explanation(dominant, scores)
    }
    
    # Diet recommendations
    diet_recs = get_diet_recommendations(dominant)
    
    # Lifestyle recommendations
    lifestyle_recs = get_lifestyle_recommendations(dominant)
    
    # Herbal support
    herbal_support = get_herbal_recommendations(dominant)
    
    # Additional wellness advice
    wellness_advice = get_wellness_advice(dominant)
    
    return {
        'personal_details': {
            'name': user_data.get('name', 'User'),
            'age': user_data.get('age', 'N/A'),
            'gender': user_data.get('gender', 'N/A'),
            'location': user_data.get('location', 'N/A')
        },
        'dosha_analysis': dosha_analysis,
        'diet_recommendations': diet_recs,
        'lifestyle_recommendations': lifestyle_recs,
        'herbal_support': herbal_support,
        'wellness_advice': wellness_advice,
        'disclaimer': "This is an Ayurvedic wellness assessment for educational and preventive purposes only. It is not a medical diagnosis. Consult a qualified Ayurvedic practitioner for treatment.",
        'timestamp': datetime.now().strftime('%d %B %Y at %I:%M %p')
    }

def get_dosha_explanation(dominant, scores):
    """Get explanation for dominant dosha"""
    explanations = {
        'vata': f"Your assessment shows Vata dominance ({scores.get('vata', 0)}%). Vata governs movement and nervous system. Current imbalance may manifest as anxiety, irregular digestion, or sleep disturbances. Focus on grounding, warming practices.",
        'pitta': f"Your assessment shows Pitta dominance ({scores.get('pitta', 0)}%). Pitta governs metabolism and transformation. Current imbalance may manifest as acidity, inflammation, or irritability. Focus on cooling, calming practices.",
        'kapha': f"Your assessment shows Kapha dominance ({scores.get('kapha', 0)}%). Kapha governs structure and stability. Current imbalance may manifest as lethargy, weight gain, or congestion. Focus on energizing, lightening practices."
    }
    return explanations.get(dominant, "Balanced constitution detected.")

def get_diet_recommendations(dominant):
    """Get diet recommendations for dosha"""
    diets = {
        'vata': {
            'foods_to_take': [
                "Warm, cooked grains: Rice, oats, quinoa",
                "Sweet fruits: Bananas, mangoes, berries, dates",
                "Cooked vegetables: Sweet potato, carrots, beets, squash",
                "Healthy fats: Ghee, sesame oil, avocado, nuts",
                "Warming spices: Ginger, cinnamon, cumin, cardamom",
                "Dairy: Warm milk, ghee, fresh yogurt",
                "Proteins: Mung dal, chicken, fish, eggs"
            ],
            'foods_to_avoid': [
                "Cold, raw foods and salads",
                "Dry, light foods like crackers and chips",
                "Bitter vegetables: Kale, broccoli, cauliflower",
                "Stimulants: Coffee, black tea, energy drinks",
                "Processed and frozen foods",
                "Carbonated beverages",
                "Excessive beans and legumes"
            ],
            'eating_guidelines': [
                "Eat at regular times - breakfast 7-8 AM, lunch 12-1 PM, dinner 6-7 PM",
                "Favor warm, moist, grounding foods with healthy fats",
                "Eat in calm, peaceful environment without distractions",
                "Sip warm water or herbal tea throughout the day",
                "Avoid eating when anxious or stressed"
            ]
        },
        'pitta': {
            'foods_to_take': [
                "Cooling grains: Basmati rice, barley, oats, wheat",
                "Sweet fruits: Melons, grapes, coconut, pomegranate",
                "Cooling vegetables: Cucumber, zucchini, leafy greens, asparagus",
                "Cooling oils: Coconut oil, ghee, olive oil",
                "Cooling spices: Coriander, fennel, cardamom, mint",
                "Dairy: Milk, ghee, butter (in moderation)",
                "Proteins: Mung dal, chickpeas, tofu, white meat"
            ],
            'foods_to_avoid': [
                "Spicy, hot, pungent foods",
                "Sour foods: Citrus, vinegar, fermented foods",
                "Salty and fried foods",
                "Red meat and seafood",
                "Alcohol and caffeine",
                "Tomatoes, garlic, onions (in excess)",
                "Processed and fast foods"
            ],
            'eating_guidelines': [
                "Never skip meals - eat at regular intervals",
                "Favor cool or room temperature foods and drinks",
                "Eat in cool, calm environment",
                "Avoid eating when angry or stressed",
                "Include sweet, bitter, and astringent tastes"
            ]
        },
        'kapha': {
            'foods_to_take': [
                "Light grains: Barley, millet, buckwheat, quinoa",
                "Astringent fruits: Apples, pears, pomegranate, berries",
                "Light vegetables: Leafy greens, broccoli, cauliflower, peppers",
                "Minimal oils: Mustard oil, sunflower oil (small amounts)",
                "Warming spices: Ginger, black pepper, turmeric, cayenne",
                "Legumes: Mung dal, red lentils, chickpeas",
                "Proteins: Chicken, turkey, fish, eggs"
            ],
            'foods_to_avoid': [
                "Heavy, oily, fried foods",
                "Sweet foods: Sugar, desserts, pastries",
                "Dairy products: Milk, cheese, yogurt, ice cream",
                "Cold foods and drinks",
                "Wheat and rice (in excess)",
                "Salty and sour foods",
                "Red meat and pork"
            ],
            'eating_guidelines': [
                "Eat light breakfast or skip it - main meal at lunch",
                "Favor warm, light, dry foods with pungent spices",
                "Avoid eating after 7 PM",
                "Eat only when truly hungry",
                "Include bitter, pungent, and astringent tastes"
            ]
        }
    }
    return diets.get(dominant, diets['vata'])

def get_lifestyle_recommendations(dominant):
    """Get lifestyle recommendations for dosha"""
    lifestyles = {
        'vata': {
            'daily_routine': [
                "Wake up: 6:00-6:30 AM",
                "Sleep: 10:00-10:30 PM (7-8 hours)",
                "Oil massage (Abhyanga) with warm sesame oil before bath",
                "Maintain regular schedule for all activities"
            ],
            'practices': {
                'yoga': [
                    "Grounding poses: Mountain pose, Tree pose, Warrior poses",
                    "Forward bends: Child's pose, Seated forward bend",
                    "Gentle twists and hip openers",
                    "Avoid excessive jumping or fast-paced sequences"
                ],
                'pranayama': [
                    "Nadi Shodhana (Alternate Nostril Breathing) - 10 minutes",
                    "Ujjayi (Ocean Breath) - calming and warming",
                    "Bhramari (Bee Breath) - for anxiety relief"
                ],
                'meditation': [
                    "Grounding meditation - 15-20 minutes daily",
                    "Body scan or yoga nidra before sleep",
                    "Focus on stability and calmness"
                ]
            },
            'habits_to_avoid': [
                "Irregular sleep schedule and staying up late",
                "Excessive travel and constant movement",
                "Overstimulation from screens and noise",
                "Skipping meals or eating irregularly"
            ]
        },
        'pitta': {
            'daily_routine': [
                "Wake up: 5:30-6:00 AM",
                "Sleep: 10:30-11:00 PM (6-7 hours)",
                "Cool shower or bath in the morning",
                "Avoid midday sun (10 AM - 2 PM)"
            ],
            'practices': {
                'yoga': [
                    "Cooling poses: Moon salutation, Forward bends",
                    "Gentle backbends: Cobra, Bridge pose",
                    "Restorative poses: Shavasana, Legs-up-the-wall",
                    "Avoid hot yoga and competitive practices"
                ],
                'pranayama': [
                    "Sheetali (Cooling Breath) - 10 minutes",
                    "Sheetkari (Hissing Breath) - cooling effect",
                    "Chandra Bhedana (Left Nostril Breathing)"
                ],
                'meditation': [
                    "Calming meditation - 15-20 minutes daily",
                    "Loving-kindness meditation",
                    "Focus on patience and compassion"
                ]
            },
            'habits_to_avoid': [
                "Overworking and perfectionism",
                "Competitive and aggressive activities",
                "Excessive sun exposure and heat",
                "Skipping meals or fasting excessively"
            ]
        },
        'kapha': {
            'daily_routine': [
                "Wake up: 5:00-5:30 AM (before sunrise)",
                "Sleep: 10:00 PM (6-7 hours, avoid oversleeping)",
                "Vigorous dry brushing before shower",
                "Stay active throughout the day"
            ],
            'practices': {
                'yoga': [
                    "Energizing poses: Sun salutation, Warrior sequences",
                    "Backbends: Camel, Bow, Wheel pose",
                    "Inversions: Headstand, Shoulder stand",
                    "Fast-paced vinyasa or power yoga"
                ],
                'pranayama': [
                    "Kapalabhati (Skull Shining Breath) - 5-10 minutes",
                    "Bhastrika (Bellows Breath) - energizing",
                    "Surya Bhedana (Right Nostril Breathing)"
                ],
                'meditation': [
                    "Energizing meditation - 10-15 minutes",
                    "Walking meditation",
                    "Focus on motivation and action"
                ]
            },
            'habits_to_avoid': [
                "Oversleeping and daytime napping",
                "Sedentary lifestyle and lack of exercise",
                "Overeating and emotional eating",
                "Excessive sitting and inactivity"
            ]
        }
    }
    return lifestyles.get(dominant, lifestyles['vata'])

def get_herbal_recommendations(dominant):
    """Get herbal recommendations for dosha"""
    herbs = {
        'vata': {
            'recommended_herbs': [
                "Ashwagandha — Reduces stress, anxiety, and promotes restful sleep",
                "Brahmi — Enhances memory, focus, and calms nervous system",
                "Shatavari — Nourishes tissues and supports reproductive health",
                "Triphala — Gentle detoxification and regulates digestion",
                "Bala — Strengthens muscles, nerves, and increases stamina"
            ],
            'usage_guidance': [
                "Take as powder (churna) mixed with warm milk or water",
                "Herbal teas: Ginger, cinnamon, cardamom tea",
                "Best time: Morning and evening with meals"
            ],
            'avoid': [
                "Avoid excessive bitter and astringent herbs",
                "Limit stimulating herbs like guarana"
            ]
        },
        'pitta': {
            'recommended_herbs': [
                "Amla — Rich in Vitamin C, cools body, and supports immunity",
                "Neem — Purifies blood and reduces inflammation",
                "Aloe Vera — Cooling, soothes digestive tract and skin",
                "Brahmi — Calms mind and reduces mental heat",
                "Shatavari — Cooling tonic for reproductive and digestive systems"
            ],
            'usage_guidance': [
                "Take as powder with cool water or coconut water",
                "Herbal teas: Coriander, fennel, mint tea",
                "Best time: Morning on empty stomach or between meals"
            ],
            'avoid': [
                "Avoid heating herbs like ginger, garlic in excess",
                "Limit pungent and spicy herbal formulations"
            ]
        },
        'kapha': {
            'recommended_herbs': [
                "Trikatu — Stimulates digestion and metabolism (ginger, black pepper, long pepper)",
                "Guggulu — Supports weight management and cholesterol balance",
                "Turmeric — Anti-inflammatory, improves circulation and metabolism",
                "Tulsi — Boosts immunity and clears respiratory congestion",
                "Punarnava — Reduces water retention and supports kidney function"
            ],
            'usage_guidance': [
                "Take as powder with warm water or honey",
                "Herbal teas: Ginger, tulsi, cinnamon tea",
                "Best time: Morning on empty stomach"
            ],
            'avoid': [
                "Avoid heavy, sweet herbs",
                "Limit cooling herbs like licorice"
            ]
        }
    }
    return herbs.get(dominant, herbs['vata'])

def get_wellness_advice(dominant):
    """Get additional wellness advice"""
    advice = {
        'vata': {
            'seasonal_tips': [
                "Extra care in autumn and early winter (Vata season)",
                "Stay warm, avoid cold winds and dry climates",
                "Increase oil massage and warm baths during cold months"
            ],
            'stress_management': [
                "Practice grounding techniques: walking barefoot, gardening",
                "Maintain social connections and avoid isolation",
                "Create calm, peaceful environment at home"
            ],
            'digestive_care': [
                "Eat warm, well-cooked meals with digestive spices",
                "Sip warm water or ginger tea throughout the day",
                "Avoid eating when anxious or on-the-go"
            ]
        },
        'pitta': {
            'seasonal_tips': [
                "Extra care in summer and late spring (Pitta season)",
                "Stay cool, avoid excessive sun and heat",
                "Increase cooling foods and activities during hot months"
            ],
            'stress_management': [
                "Practice patience and avoid perfectionism",
                "Engage in cooling, non-competitive activities",
                "Spend time in nature, especially near water"
            ],
            'digestive_care': [
                "Never skip meals - eat at regular times",
                "Avoid spicy, acidic, and fried foods",
                "Use cooling digestive spices: coriander, fennel, mint"
            ]
        },
        'kapha': {
            'seasonal_tips': [
                "Extra care in late winter and spring (Kapha season)",
                "Increase activity and reduce heavy foods",
                "Practice detoxification during spring"
            ],
            'stress_management': [
                "Stay mentally and physically active",
                "Seek new experiences and challenges",
                "Avoid emotional eating and comfort foods"
            ],
            'digestive_care': [
                "Eat light meals and avoid overeating",
                "Use warming digestive spices: ginger, black pepper, turmeric",
                "Fast occasionally or skip breakfast if not hungry"
            ]
        }
    }
    return advice.get(dominant, advice['vata'])

def format_assessment_answers(answers):
    """Format assessment answers for LLM"""
    if not answers:
        return "No detailed answers provided"
    
    summary = []
    for key, value in answers.items():
        if isinstance(value, str):
            summary.append(f"{key}: {value}")
    
    return ", ".join(summary[:10])  # Limit to first 10 answers

def parse_llm_report(report_text, user_data, assessment_results):
    """Parse LLM-generated report into structured format"""
    # For now, return the text report with basic structure
    # Can be enhanced to parse sections
    
    return {
        'personal_details': {
            'name': user_data.get('name', 'User'),
            'age': user_data.get('age', 'N/A'),
            'gender': user_data.get('gender', 'N/A'),
            'location': user_data.get('location', 'N/A')
        },
        'full_report': report_text,
        'scores': assessment_results.get('scores', {}),
        'dominant': assessment_results.get('dominant', 'Vata'),
        'risk': assessment_results.get('risk', 'Low'),
        'timestamp': datetime.now().strftime('%d %B %Y at %I:%M %p')
    }
