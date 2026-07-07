export interface DoshaMetadata {
  label: string;
  color: string;
  text: string;
  desc: string;
  emoji: string;
  element: string;
}

export const DOSHAS: Record<'vata' | 'pitta' | 'kapha', DoshaMetadata> = {
  vata: {
    label: 'Vata',
    color: 'bg-sky-400',
    text: 'text-sky-700',
    desc: 'Governs movement, communication, and neurological functions. Associated with Air and Ether elements.',
    emoji: '🌬️',
    element: 'Air + Space'
  },
  pitta: {
    label: 'Pitta',
    color: 'bg-amber-400',
    text: 'text-amber-700',
    desc: 'Governs digestion, heat, metabolism, and mental transformation. Associated with Fire and Water elements.',
    emoji: '🔥',
    element: 'Fire + Water'
  },
  kapha: {
    label: 'Kapha',
    color: 'bg-emerald-400',
    text: 'text-emerald-700',
    desc: 'Governs structure, lubrication, cohesion, and physical growth. Associated with Earth and Water elements.',
    emoji: '🌿',
    element: 'Water + Earth'
  }
};
