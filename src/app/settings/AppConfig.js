/**
 * Application Configuration
 * 
 * Main configuration file for the app with environment-specific settings
 */

// Determine current environment
// In a real app, this would be set through environment variables or build flags
const ENV = process.env.NODE_ENV || 'development';

// API endpoints by environment
const API_ENDPOINTS = {
  development: {
    baseUrl: 'http://localhost:8000',
    timeout: 10000, // 10 seconds
  },
  staging: {
    baseUrl: 'https://api-staging.psychdoodle-analyzer.com',
    timeout: 15000, // 15 seconds
  },
  production: {
    baseUrl: 'https://api.psychdoodle-analyzer.com',
    timeout: 20000, // 20 seconds
  },
};

// Feature flags by environment
const FEATURES = {
  development: {
    enableDebugMode: true,
    enableMockData: true,
    enableAnalyticsTracking: false,
    enableDevTools: true,
    enableBetaFeatures: true,
    enableGauGAN: true,
    maxStoredDrawings: 50,
  },
  staging: {
    enableDebugMode: true,
    enableMockData: false,
    enableAnalyticsTracking: true,
    enableDevTools: true,
    enableBetaFeatures: true,
    enableGauGAN: true,
    maxStoredDrawings: 100,
  },
  production: {
    enableDebugMode: false,
    enableMockData: false,
    enableAnalyticsTracking: true,
    enableDevTools: false,
    enableBetaFeatures: false,
    enableGauGAN: true,
    maxStoredDrawings: 200,
  },
};

// Default predefined shapes for tracing
const DEFAULT_SHAPES = {
  basic: [
    {
      id: 'circle',
      name: 'Circle',
      description: 'A simple circle',
      complexity: 1,
      imageUrl: '/assets/shapes/circle.svg',
    },
    {
      id: 'square',
      name: 'Square',
      description: 'A simple square',
      complexity: 1,
      imageUrl: '/assets/shapes/square.svg',
    },
    {
      id: 'triangle',
      name: 'Triangle',
      description: 'A simple triangle',
      complexity: 1,
      imageUrl: '/assets/shapes/triangle.svg',
    },
  ],
  intermediate: [
    {
      id: 'star',
      name: 'Star',
      description: 'A five-pointed star',
      complexity: 2,
      imageUrl: '/assets/shapes/star.svg',
    },
    {
      id: 'house',
      name: 'House',
      description: 'A simple house',
      complexity: 2,
      imageUrl: '/assets/shapes/house.svg',
    },
    {
      id: 'flower',
      name: 'Flower',
      description: 'A simple flower',
      complexity: 2,
      imageUrl: '/assets/shapes/flower.svg',
    },
  ],
  advanced: [
    {
      id: 'mandala',
      name: 'Mandala',
      description: 'A simple mandala pattern',
      complexity: 3,
      imageUrl: '/assets/shapes/mandala.svg',
    },
    {
      id: 'maze',
      name: 'Maze',
      description: 'A simple maze',
      complexity: 3,
      imageUrl: '/assets/shapes/maze.svg',
    },
    {
      id: 'spiral',
      name: 'Spiral',
      description: 'A spiral pattern',
      complexity: 3,
      imageUrl: '/assets/shapes/spiral.svg',
    },
  ],
};

// Default emotional feedback templates
const FEEDBACK_TEMPLATES = {
  anxiety: [
    'Believe in the meaning of your existence.',
    'Don\'t project your inner shadows onto others. It becomes the source of almost all conflicts.',
    'Exercise helps you efficiently control your mood.',
  ],
  depression: [
    'A person who looks outward dreams, but a person who looks inward can awaken.',
    'Creative people like to play with what they love. Enjoy what you like.',
    'Depression often stems from continuously feeding yourself falsehoods. Try not to worry too much about things that aren\'t true.',
  ],
  stress: [
    'Seek the freedom to choose and express your emotions.',
    'To restore intimacy, you must be honest with your inner self.',
    'Try to lead intimate exchanges with people around you.',
  ],
  calm: [
    'Your current state of calm is a valuable resource for creativity.',
    'In tranquility, insights often emerge. Take time to listen to your inner voice.',
    'Balanced emotions allow for clearer perspective on challenges.',
  ],
  happy: [
    'Share your positive energy with those around you.',
    'Happiness is a powerful creative force. Channel it into expression.',
    'Remember this feeling of joy - you can return to it even in difficult moments.',
  ],
};

// App version information
const VERSION = {
  name: '1.0.0',
  code: 1,
  buildDate: new Date().toISOString(),
};

// Export configuration based on current environment
const AppConfig = {
  env: ENV,
  api: API_ENDPOINTS[ENV],
  features: FEATURES[ENV],
  shapes: DEFAULT_SHAPES,
  feedback: FEEDBACK_TEMPLATES,
  version: VERSION,
  
  // Helper method to check if a feature is enabled
  isFeatureEnabled(featureName) {
    return this.features[featureName] === true;
  },
  
  // Helper method to get API URL
  getApiUrl(endpoint) {
    return `${this.api.baseUrl}/${endpoint}`;
  },
  
  // Helper method to get appropriate shapes based on complexity level
  getShapesByComplexity(level = 'basic') {
    if (this.shapes[level]) {
      return this.shapes[level];
    }
    return this.shapes.basic;
  },
  
  // Helper method to get feedback templates for a specific emotion
  getFeedbackForEmotion(emotion) {
    if (this.feedback[emotion]) {
      return this.feedback[emotion];
    }
    // Return a random category if the specific emotion is not found
    const categories = Object.keys(this.feedback);
    const randomCategory = categories[Math.floor(Math.random() * categories.length)];
    return this.feedback[randomCategory];
  },
};

export default AppConfig;
