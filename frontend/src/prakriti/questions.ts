export interface Option {
  text: string;
  dosha: 'Vata' | 'Pitta' | 'Kapha' | 'None';
}

export interface Question {
  id: number;
  question: string;
  options: Option[];
}

export interface PrakritiScores {
  vata: number;
  pitta: number;
  kapha: number;
}

export interface DietSuggestions {
  foods_to_favor: string[];
  foods_to_avoid: string[];
}

export interface PrakritiInterpretation {
  dominant: string;
  scores: PrakritiScores;
  risk: 'Low' | 'Moderate' | 'High';
  dosha_state: 'Balanced' | 'Imbalanced';
  agni_state: string;
  ama_status: 'None' | 'Mild' | 'Moderate' | 'High';
  vikriti: string;
  justification: string;
  personality_traits: string[];
  physical_characteristics: string[];
  dietary_recommendations: string[];
  lifestyle_recommendations: string[];
  exercise_recommendations: string[];
  sleep_recommendations: string[];
  seasonal_precautions: string[];
  strengths: string[];
  possible_health_tendencies: string[];
  recommendations: string[]; // for backwards compatibility with existing UI
  diet_suggestions: DietSuggestions; // for backwards compatibility with existing UI
  lifestyle_tips: string[]; // for backwards compatibility with existing UI
}
