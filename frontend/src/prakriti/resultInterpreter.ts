import { PrakritiInterpretation, DietSuggestions } from './questions';
import { CalculatedPrakriti } from './prakritiCalculator';

interface DoshaProfile {
  traits: string[];
  physical: string[];
  dietFavor: string[];
  dietAvoid: string[];
  lifestyle: string[];
  exercise: string[];
  sleep: string[];
  seasonal: string[];
  strengths: string[];
  tendencies: string[];
  interpretation: string;
}

const DOSHA_PROFILES: Record<'vata' | 'pitta' | 'kapha', DoshaProfile> = {
  vata: {
    traits: [
      "Highly creative, imaginative, and artistic",
      "Quick to grasp new ideas, but quick to forget them",
      "Enthusiastic, energetic, and vivacious",
      "Prone to sudden bursts of energy followed by quick exhaustion",
      "May experience anxiety, worry, or indecision when out of balance"
    ],
    physical: [
      "Thin, light, or delicate body frame",
      "Dry, rough, or cold skin",
      "Tendency to have cold hands and feet",
      "Fine, curly, or frizzy hair",
      "Prominent veins and crackling joints"
    ],
    dietFavor: [
      "Warm, cooked, and fresh meals",
      "Nourishing oils, ghee, and healthy fats",
      "Sweet, sour, and salty tastes",
      "Warm milk, nuts, avocados, and root vegetables"
    ],
    dietAvoid: [
      "Cold, raw, and dry foods (salads, crackers)",
      "Bitter, pungent, and astringent tastes",
      "Caffeine, carbonated drinks, and ice water"
    ],
    lifestyle: [
      "Maintain a consistent daily routine (Dinacharya)",
      "Practice daily self-massage (Abhyanga) with warm sesame oil",
      "Keep warm and stay hydrated throughout the day",
      "Avoid overstimulation, loud noises, and excessive screen time"
    ],
    exercise: [
      "Gentle, grounding activities (Yoga, walking, tai chi)",
      "Focus on slow, mindful movements",
      "Avoid exhaustive workouts or high-intensity cardio"
    ],
    sleep: [
      "Aim for 8 hours of deep, restful sleep",
      "Sleep early (by 10:00 PM) in a warm, dark room",
      "Practice calming breathing exercises before bed"
    ],
    seasonal: [
      "Protect yourself from dry, cold, and windy weather",
      "Wear warm, layered clothing in Autumn and Winter",
      "Favor warm baths, steam, and warming spices like ginger and cinnamon"
    ],
    strengths: [
      "Creativity, adaptability, quick responsiveness, and spiritual sensitivity"
    ],
    tendencies: [
      "Dry skin, constipation, bloating, anxiety, insomnia, and joint stiffness"
    ],
    interpretation: "Your dominant Vata dosha indicates a constitution governed by Air and Space. You are naturally creative, alert, and active, but you need grounding and warm nourishment to prevent anxiety and dryness."
  },
  pitta: {
    traits: [
      "Brilliant intellect, sharp comprehension, and focused mind",
      "Goal-oriented, ambitious, and strong leadership skills",
      "Passionate and courageous",
      "Highly organized and values cleanliness/efficiency",
      "Prone to irritation, anger, or impatience when stressed"
    ],
    physical: [
      "Medium build with moderate muscle tone",
      "Soft, warm skin that easily flushes or burns in the sun",
      "Acne, freckles, or moles may be present",
      "Fine, soft hair that may grey or thin prematurely",
      "Strong digestion and intense appetite"
    ],
    dietFavor: [
      "Cooling, refreshing, and moderately heavy foods",
      "Sweet, bitter, and astringent tastes",
      "Cucumbers, melons, leafy greens, coconut, and cooling herbs like cilantro"
    ],
    dietAvoid: [
      "Hot, spicy, and deeply fried foods",
      "Sour, salty, and pungent tastes",
      "Fermented foods, alcohol, vinegar, tomatoes, and citrus fruits"
    ],
    lifestyle: [
      "Avoid overheating; spend time in nature (near water or under moonlight)",
      "Practice work-life balance and avoid over-scheduling",
      "Express feelings constructively and cultivate compassion",
      "Use cooling essential oils like sandalwood, rose, or jasmine"
    ],
    exercise: [
      "Moderate, non-competitive physical activity",
      "Swimming, cycling, evening walks, or cooling Yoga (Moon Salutations)",
      "Exercise during cooler parts of the day (early morning/evening)"
    ],
    sleep: [
      "Aim for 7-8 hours of peaceful sleep",
      "Maintain a cool room temperature",
      "Avoid intense mental activity or debates before sleeping"
    ],
    seasonal: [
      "Take precautions during hot, humid Summer months",
      "Stay hydrated, wear light/loose clothing, and avoid direct midday sun",
      "Favor sweet and hydrating foods"
    ],
    strengths: [
      "Leadership, analytical capability, courage, passion, and decisiveness"
    ],
    tendencies: [
      "Acidity, heartburn, skin rashes, inflammation, hot flashes, and irritability"
    ],
    interpretation: "Your dominant Pitta dosha indicates a constitution governed by Fire and Water. You possess a sharp intellect, excellent digestion, and strong leadership traits, but require cooling and moderation to prevent burnout, inflammation, and irritability."
  },
  kapha: {
    traits: [
      "Calm, steady, patient, and deeply compassionate",
      "Loyal, stable friend with long-term memory",
      "Easygoing, peaceful nature that rarely gets angry",
      "Forgiving, grateful, and emotionally secure",
      "Can drift into lethargy, possessiveness, or resistance to change when out of balance"
    ],
    physical: [
      "Well-developed, sturdy, and stable body structure",
      "Thick, smooth, and naturally oily skin",
      "Thick, shiny, dark, or wavy hair",
      "Large, beautiful, calm eyes",
      "Slow but steady digestion; tendency to gain weight easily"
    ],
    dietFavor: [
      "Light, warm, dry, and spicy foods",
      "Pungent, bitter, and astringent tastes",
      "Warm ginger tea, fresh vegetables, legumes, and warming spices like black pepper"
    ],
    dietAvoid: [
      "Cold, heavy, sweet, and excessively oily foods",
      "Sour, salty, and sweet tastes",
      "Heavy dairy (cheese, cream), cold desserts, and fried food"
    ],
    lifestyle: [
      "Stay physically active and seek daily variety",
      "Wake up early (before 6:00 AM) and avoid sleeping during the day",
      "Keep dry and warm; massage with dry powders or warm mustard oil (Garshana)",
      "Embrace new experiences and changes"
    ],
    exercise: [
      "Vigorous, energetic workouts (high-intensity cardio, jogging, aerobics)",
      "Consistency is key to stimulate sluggish metabolism",
      "Outdoor sports, dancing, or power yoga"
    ],
    sleep: [
      "Aim for 6-7 hours. Avoid oversleeping, which increases lethargy",
      "Wake up with the sunrise",
      "Keep blankets lightweight"
    ],
    seasonal: [
      "Take care during damp, cold, or cloudy Spring and Winter seasons",
      "Keep active, dry, and warm",
      "Drink warm water and herbal teas containing warming spices"
    ],
    strengths: [
      "Stability, stamina, loyalty, compassion, calmness under pressure, and strong immunity"
    ],
    tendencies: [
      "Weight gain, congestion, sluggish digestion, depression, lethargy, and water retention"
    ],
    interpretation: "Your dominant Kapha dosha indicates a constitution governed by Water and Earth. You are naturally stable, calm, strong, and caring, but must stay active and favor warming, light nourishment to avoid lethargy, congestion, and weight gain."
  }
};

export function interpretResult(prakriti: CalculatedPrakriti): PrakritiInterpretation {
  const { dominant, percentages, vikriti, dosha_state } = prakriti;

  // Determine dominant profiles to merge
  let interpretation = '';
  let traits: string[] = [];
  let physical: string[] = [];
  let dietFavor: string[] = [];
  let dietAvoid: string[] = [];
  let lifestyle: string[] = [];
  let exercise: string[] = [];
  let sleep: string[] = [];
  let seasonal: string[] = [];
  let strengths: string[] = [];
  let tendencies: string[] = [];

  // Parse type
  const lowerDominant = dominant.toLowerCase();

  if (lowerDominant.includes('sama')) {
    // Tridoshic / Sama
    interpretation = "You have a Sama (Tridoshic) constitution, meaning your Vata, Pitta, and Kapha doshas are naturally balanced in nearly equal proportions. This is a rare and highly stable constitution, providing excellent health potential, emotional stability, and high resilience.";
    
    // Combine general positive traits from all
    traits = ["Extremely balanced, adaptable, and emotionally stable", "Has a mixture of creativity (Vata), focus (Pitta), and patience (Kapha)", "Resilient mind with calm temperament"];
    physical = ["Proportional, balanced body structure", "Even complexion and moderate metabolism", "Strong overall immunity and endurance"];
    dietFavor = ["A balanced diet containing all six tastes, adjusting seasonally", "Moderation in all food types", "Warm, freshly cooked meals with mild spices"];
    dietAvoid = ["Excess of any single extreme taste (too spicy, too cold, too heavy)", "Overeating or skipping meals frequently"];
    lifestyle = ["Follow general Ayurvedic daily routines (Dinacharya)", "Adjust routines to match the active season (Vata in Autumn, Pitta in Summer, Kapha in Spring)", "Maintain mindfulness and balanced activity"];
    exercise = ["A balanced mix of moderate cardio, stretching, and strength training", "Yoga, swimming, and hiking"];
    sleep = ["7-8 hours of sound sleep", "Regular sleep and wake times"];
    seasonal = ["Transition smoothly between seasons; perform mild detoxes (Panchakarma or seasonal fasting) during seasonal shifts"];
    strengths = ["Exceptional resilience, natural physical and mental balance, high adaptability"];
    tendencies = ["Generally low susceptibility to illness, but imbalances can occur if lifestyle becomes highly irregular or extreme"];
  } else if (lowerDominant.includes('-')) {
    // Dual Dosha (e.g. Vata-Pitta, Pitta-Kapha, Vata-Kapha)
    const parts = dominant.split(' ')[0].split('-');
    const dosha1 = parts[0].toLowerCase() as 'vata' | 'pitta' | 'kapha';
    const dosha2 = parts[1].toLowerCase() as 'vata' | 'pitta' | 'kapha';

    const p1 = DOSHA_PROFILES[dosha1];
    const p2 = DOSHA_PROFILES[dosha2];

    interpretation = `You have a dual-dosha ${dominant} constitution. Your nature is governed by the qualities of both ${p1.interpretation.split('governed by')[1].split('.')[0]} and ${p2.interpretation.split('governed by')[1].split('.')[0]}. You will notice a blend of characteristics from both doshas depending on seasons, age, and lifestyle.`;

    traits = [...p1.traits.slice(0, 3), ...p2.traits.slice(0, 2)];
    physical = [...p1.physical.slice(0, 3), ...p2.physical.slice(0, 2)];
    dietFavor = Array.from(new Set([...p1.dietFavor.slice(0, 2), ...p2.dietFavor.slice(0, 2)]));
    dietAvoid = Array.from(new Set([...p1.dietAvoid.slice(0, 2), ...p2.dietAvoid.slice(0, 2)]));
    lifestyle = Array.from(new Set([...p1.lifestyle.slice(0, 2), ...p2.lifestyle.slice(0, 2)]));
    exercise = Array.from(new Set([...p1.exercise.slice(0, 2), ...p2.exercise.slice(0, 2)]));
    sleep = Array.from(new Set([...p1.sleep.slice(0, 2), ...p2.sleep.slice(0, 2)]));
    seasonal = Array.from(new Set([...p1.seasonal.slice(0, 2), ...p2.seasonal.slice(0, 2)]));
    strengths = Array.from(new Set([...p1.strengths, ...p2.strengths]));
    tendencies = Array.from(new Set([...p1.tendencies, ...p2.tendencies]));
  } else {
    // Single Dosha
    const d = dominant.split(' ')[0].toLowerCase() as 'vata' | 'pitta' | 'kapha';
    const profile = DOSHA_PROFILES[d];

    interpretation = profile.interpretation;
    traits = profile.traits;
    physical = profile.physical;
    dietFavor = profile.dietFavor;
    dietAvoid = profile.dietAvoid;
    lifestyle = profile.lifestyle;
    exercise = profile.exercise;
    sleep = profile.sleep;
    seasonal = profile.seasonal;
    strengths = profile.strengths;
    tendencies = profile.tendencies;
  }

  // Calculate risk level (conservative Ayurvedic heuristic)
  const sorted = Object.entries(percentages).sort((a, b) => b[1] - a[1]);
  const highestScore = sorted[0][1];
  let risk: 'Low' | 'Moderate' | 'High' = 'Low';

  if (highestScore >= 60) risk = 'High';
  else if (highestScore >= 45) risk = 'Moderate';

  // Backwards compatible fields
  const recommendations = [
    ...lifestyle.slice(0, 3),
    ...exercise.slice(0, 2),
    ...sleep.slice(0, 2)
  ];
  
  const diet_suggestions: DietSuggestions = {
    foods_to_favor: dietFavor,
    foods_to_avoid: dietAvoid
  };

  const lifestyle_tips = lifestyle;

  // Determine Agni and Ama state based on percentages/dominant doshas
  let agni_state = 'Sama Agni (Balanced Digestion)';
  let ama_status: 'None' | 'Mild' | 'Moderate' | 'High' = 'None';

  if (vikriti === 'Vata') {
    agni_state = 'Vishama Agni (Irregular Digestion)';
    ama_status = 'Mild';
  } else if (vikriti === 'Pitta') {
    agni_state = 'Tikshna Agni (Sharp/Hyperactive Digestion)';
    ama_status = 'Moderate';
  } else if (vikriti === 'Kapha') {
    agni_state = 'Manda Agni (Sluggish/Slow Digestion)';
    ama_status = 'Mild';
  }

  const justification = `Based on a 22-question clinical Prakriti assessment, a ${dominant} constitution is identified. ` +
    `Scores: Vata ${percentages.vata}%, Pitta ${percentages.pitta}%, Kapha ${percentages.kapha}%. ` +
    `Primary dosha display matches ${vikriti} qualities.`;

  return {
    dominant,
    scores: percentages, // percentages are used as display scores in frontend
    risk,
    dosha_state,
    agni_state,
    ama_status,
    vikriti,
    justification,
    personality_traits: traits,
    physical_characteristics: physical,
    dietary_recommendations: dietFavor,
    lifestyle_recommendations: lifestyle,
    exercise_recommendations: exercise,
    sleep_recommendations: sleep,
    seasonal_precautions: seasonal,
    strengths,
    possible_health_tendencies: tendencies,
    recommendations,
    diet_suggestions,
    lifestyle_tips
  };
}
