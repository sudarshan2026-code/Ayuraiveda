import { calculateRawScores } from './scoringEngine';
import { PrakritiScores, DietSuggestions } from './questions';

export interface CalculatedPrakriti {
  dominant: string;
  scores: PrakritiScores;
  percentages: PrakritiScores;
  vikriti: string;
  dosha_state: 'Balanced' | 'Imbalanced';
}

export function calculatePrakriti(answers: Record<string, string>): CalculatedPrakriti {
  const rawScores = calculateRawScores(answers);
  const total = rawScores.vata + rawScores.pitta + rawScores.kapha;

  let vataPct = 33.3;
  let pittaPct = 33.3;
  let kaphaPct = 33.3;

  if (total > 0) {
    // Calculate percentages and round to 1 decimal place
    vataPct = Math.round((rawScores.vata / total) * 1000) / 10;
    pittaPct = Math.round((rawScores.pitta / total) * 1000) / 10;
    kaphaPct = Math.round((rawScores.kapha / total) * 1000) / 10;

    // Adjust rounding errors to ensure they sum to 100%
    const diff = 100 - (vataPct + pittaPct + kaphaPct);
    if (Math.abs(diff) > 0.01) {
      // Add the tiny rounding difference to the highest score
      if (vataPct >= pittaPct && vataPct >= kaphaPct) vataPct = Math.round((vataPct + diff) * 10) / 10;
      else if (pittaPct >= vataPct && pittaPct >= kaphaPct) pittaPct = Math.round((pittaPct + diff) * 10) / 10;
      else kaphaPct = Math.round((kaphaPct + diff) * 10) / 10;
    }
  }

  const pcts = [
    { name: 'Vata', pct: vataPct },
    { name: 'Pitta', pct: pittaPct },
    { name: 'Kapha', pct: kaphaPct }
  ];

  // Sort descending
  pcts.sort((a, b) => b.pct - a.pct);

  const highest = pcts[0];
  const second = pcts[1];
  const lowest = pcts[2];

  let dominant = '';
  let dosha_state: 'Balanced' | 'Imbalanced' = 'Imbalanced';

  // 1. Sama (Tridoshic) Constitution
  // If the difference between highest and lowest is within 5%
  if (highest.pct - lowest.pct <= 5) {
    dominant = 'Sama Prakriti (Tridoshic)';
    dosha_state = 'Balanced';
  }
  // 2. Dual Dosha Constitution
  // If the difference between the two highest is within 6%
  else if (highest.pct - second.pct <= 6) {
    dominant = `${highest.name}-${second.name} Prakriti`;
    dosha_state = 'Imbalanced';
  }
  // 3. Single Dosha Constitution
  else {
    dominant = `${highest.name} Prakriti`;
    dosha_state = highest.pct >= 55 ? 'Imbalanced' : 'Balanced';
  }

  return {
    dominant,
    scores: rawScores,
    percentages: {
      vata: vataPct,
      pitta: pittaPct,
      kapha: kaphaPct
    },
    vikriti: highest.name,
    dosha_state
  };
}
