import { QUESTION_BANK } from './questionBank';
import { PrakritiScores } from './questions';

export function calculateRawScores(answers: Record<string, string>): PrakritiScores {
  const scores: PrakritiScores = { vata: 0, pitta: 0, kapha: 0 };

  Object.entries(answers).forEach(([key, selectedText]) => {
    // Expected key format is 'q1', 'q2', etc. Or matches the question id
    const match = key.match(/^q(\d+)$/);
    if (!match) return;
    
    const questionId = parseInt(match[1], 10);
    const question = QUESTION_BANK.find(q => q.id === questionId);
    if (!question) return;

    const selectedOption = question.options.find(opt => opt.text === selectedText);
    if (!selectedOption) return;

    const dosha = selectedOption.dosha.toLowerCase();
    if (dosha === 'vata') {
      scores.vata += 1;
    } else if (dosha === 'pitta') {
      scores.pitta += 1;
    } else if (dosha === 'kapha') {
      scores.kapha += 1;
    }
  });

  return scores;
}
