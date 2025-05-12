/**
 * EmotionalMapping.js
 * 
 * Defines the emotional mapping model for the psychological analysis
 * based on drawing characteristics
 */

/**
 * Emotional categories and their descriptors
 */
const EMOTIONAL_CATEGORIES = {
  anxiety: {
    name: 'Anxiety',
    description: 'Feelings of worry, nervousness, or unease about something with an uncertain outcome',
    features: {
      lineIntensity: 'high',
      lineSize: 'varied',
      lineRepetition: 'high',
      spaceUsage: 'restricted',
      sharpAngles: 'many',
      colorIntensity: 'high',
      colorPreference: ['red', 'black'],
      reactionTime: 'quick',
      pressureVariation: 'high',
    },
    relatedStates: ['stress', 'fear', 'panic'],
  },
  
  depression: {
    name: 'Depression',
    description: 'Feelings of severe despondency and dejection',
    features: {
      lineIntensity: 'light',
      lineSize: 'small',
      lineRepetition: 'low',
      spaceUsage: 'minimal',
      sharpAngles: 'few',
      colorIntensity: 'low',
      colorPreference: ['blue', 'gray', 'black'],
      reactionTime: 'slow',
      pressureVariation: 'low',
    },
    relatedStates: ['sadness', 'melancholy', 'emptiness'],
  },
  
  anger: {
    name: 'Anger',
    description: 'Strong feeling of annoyance, displeasure, or hostility',
    features: {
      lineIntensity: 'very high',
      lineSize: 'large',
      lineRepetition: 'medium',
      spaceUsage: 'expansive',
      sharpAngles: 'many',
      colorIntensity: 'high',
      colorPreference: ['red', 'black', 'orange'],
      reactionTime: 'quick',
      pressureVariation: 'high',
    },
    relatedStates: ['frustration', 'irritation', 'rage'],
  },
  
  calm: {
    name: 'Calm',
    description: 'Not showing or feeling nervousness, anger, or other strong emotions',
    features: {
      lineIntensity: 'medium',
      lineSize: 'medium',
      lineRepetition: 'low',
      spaceUsage: 'balanced',
      sharpAngles: 'few',
      colorIntensity: 'medium',
      colorPreference: ['blue', 'green', 'purple'],
      reactionTime: 'medium',
      pressureVariation: 'low',
    },
    relatedStates: ['peaceful', 'relaxed', 'content'],
  },
  
  happiness: {
    name: 'Happiness',
    description: 'Feeling or showing pleasure or contentment',
    features: {
      lineIntensity: 'medium',
      lineSize: 'medium to large',
      lineRepetition: 'medium',
      spaceUsage: 'expansive',
      sharpAngles: 'few',
      colorIntensity: 'high',
      colorPreference: ['yellow', 'orange', 'bright colors'],
      reactionTime: 'quick',
      pressureVariation: 'medium',
    },
    relatedStates: ['joy', 'excitement', 'contentment'],
  },
  
  confusion: {
    name: 'Confusion',
    description: 'Lack of understanding or uncertainty about how to respond',
    features: {
      lineIntensity: 'varied',
      lineSize: 'varied',
      lineRepetition: 'high',
      spaceUsage: 'chaotic',
      sharpAngles: 'varied',
      colorIntensity: 'varied',
      colorPreference: ['varied'],
      reactionTime: 'slow',
      pressureVariation: 'high',
    },
    relatedStates: ['uncertainty', 'bewilderment', 'disorientation'],
  },
};

/**
 * Line characteristics and their psychological interpretations
 */
const LINE_INTERPRETATIONS = {
  intensity: {
    light: 'May indicate timidity, uncertainty, sensitivity, or depression',
    medium: 'Shows balance, control, and moderation',
    heavy: 'Can suggest confidence, intensity, anxiety, or aggression',
  },
  size: {
    small: 'May indicate introversion, focus on detail, or containment of emotions',
    medium: 'Suggests balance and proportion',
    large: 'Can indicate extroversion, expressiveness, or lack of inhibition',
  },
  repetition: {
    low: 'May indicate decisiveness, clarity, or minimalism',
    medium: 'Shows thoughtfulness and intentionality',
    high: 'Can suggest anxiety, obsessiveness, or need for reinforcement',
  },
};

/**
 * Color preferences and their psychological interpretations
 */
const COLOR_INTERPRETATIONS = {
  red: 'Energy, passion, anger, danger, excitement',
  blue: 'Calm, trust, competence, peace, logic, security',
  green: 'Growth, harmony, nature, balance, healing',
  yellow: 'Happiness, optimism, creativity, warmth',
  purple: 'Luxury, wisdom, creativity, imagination, spirituality',
  black: 'Power, elegance, mystery, formality, or sadness',
  white: 'Purity, cleanliness, innocence, simplicity',
  brown: 'Reliability, stability, warmth, naturalness',
  gray: 'Neutrality, detachment, indecision, or depression',
  orange: 'Enthusiasm, creativity, determination, stimulation',
  pink: 'Nurturing, romance, gentleness, compassion',
};

/**
 * Drawing space usage interpretations
 */
const SPACE_INTERPRETATIONS = {
  minimal: 'May indicate introversion, reservation, depression, or focus',
  restricted: 'Can suggest containment, caution, anxiety, or control',
  balanced: 'Shows equilibrium, proportion, and security',
  expansive: 'May indicate extroversion, freedom, or lack of boundaries',
  chaotic: 'Can suggest confusion, high energy, or disorganization',
};

/**
 * Reaction time interpretations
 */
const REACTION_TIME_INTERPRETATIONS = {
  quick: 'May indicate impulsivity, confidence, or anxiety',
  medium: 'Shows thoughtfulness and balance',
  slow: 'Can suggest carefulness, uncertainty, depression, or deliberation',
};

/**
 * Calculates an emotional profile score based on drawing features
 * @param {Object} features - Drawing features extracted from analysis
 * @returns {Object} Emotional profile with scores for each category
 */
function calculateEmotionalProfile(features) {
  // This is a simplified version of what would be a more complex algorithm
  // In a real implementation, this would use machine learning models
  
  const profile = {};
  
  // Initialize scores for each emotional category
  Object.keys(EMOTIONAL_CATEGORIES).forEach(category => {
    profile[category] = 0;
  });
  
  // Calculate matches for each emotional category
  Object.entries(EMOTIONAL_CATEGORIES).forEach(([category, data]) => {
    let matchScore = 0;
    let totalFeatures = 0;
    
    // Compare each feature with the category's expected features
    Object.entries(data.features).forEach(([featureName, expectedValue]) => {
      if (features[featureName]) {
        totalFeatures++;
        
        // For array types (like colorPreference)
        if (Array.isArray(expectedValue)) {
          if (Array.isArray(features[featureName])) {
            // Calculate overlap between arrays
            const overlap = features[featureName].filter(value => 
              expectedValue.includes(value)
            ).length;
            
            matchScore += overlap / Math.max(expectedValue.length, features[featureName].length);
          } else if (expectedValue.includes(features[featureName])) {
            matchScore += 1;
          }
        } 
        // For string types
        else if (features[featureName] === expectedValue) {
          matchScore += 1;
        }
      }
    });
    
    // Calculate average match score if features were present
    if (totalFeatures > 0) {
      profile[category] = matchScore / totalFeatures;
    }
  });
  
  return profile;
}

/**
 * Generates feedback based on the emotional profile
 * @param {Object} profile - Emotional profile with scores
 * @returns {Object} Feedback object with primary emotion and suggestions
 */
function generateFeedback(profile) {
  // Find the highest scoring emotion
  let primaryEmotion = Object.keys(profile).reduce((a, b) => 
    profile[a] > profile[b] ? a : b
  );
  
  // Get the related states for the primary emotion
  const relatedStates = EMOTIONAL_CATEGORIES[primaryEmotion].relatedStates || [];
  
  // Create feedback object
  return {
    primaryEmotion,
    emotionName: EMOTIONAL_CATEGORIES[primaryEmotion].name,
    emotionDescription: EMOTIONAL_CATEGORIES[primaryEmotion].description,
    score: profile[primaryEmotion],
    relatedStates,
    // Full profile for reference
    fullProfile: profile,
  };
}

export default {
  EMOTIONAL_CATEGORIES,
  LINE_INTERPRETATIONS,
  COLOR_INTERPRETATIONS,
  SPACE_INTERPRETATIONS,
  REACTION_TIME_INTERPRETATIONS,
  calculateEmotionalProfile,
  generateFeedback,
};
