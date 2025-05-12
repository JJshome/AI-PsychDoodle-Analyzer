/**
 * DrawingDataHandler
 * 
 * Handles processing and management of drawing data
 */

import { Platform } from 'react-native';
import * as FileSystem from 'expo-file-system';
import uuid from 'react-native-uuid';

class DrawingDataHandler {
  constructor() {
    this.localStorageDir = `${FileSystem.documentDirectory}drawings/`;
    this.initializeStorage();
  }

  /**
   * Initialize local storage directory
   */
  async initializeStorage() {
    try {
      const dirInfo = await FileSystem.getInfoAsync(this.localStorageDir);
      if (!dirInfo.exists) {
        await FileSystem.makeDirectoryAsync(this.localStorageDir, { intermediates: true });
      }
    } catch (error) {
      console.error('Failed to initialize storage:', error);
    }
  }

  /**
   * Process drawing data for analysis
   * @param {Object} drawingData - Drawing data from DrawingCanvas
   * @param {Object} options - Processing options
   * @returns {Object} Processed drawing data
   */
  async processDrawingData(drawingData, options = {}) {
    try {
      const { svgData, base64, drawingTime, paths } = drawingData;
      const { saveLocally = true, compressImage = true } = options;
      
      // Generate unique ID for the drawing
      const drawingId = uuid.v4();
      
      // Prepare metadata
      const metadata = {
        id: drawingId,
        timestamp: new Date().toISOString(),
        drawingTime,
        pathCount: paths.length,
        deviceInfo: this.getDeviceInfo(),
        ...options.metadata,
      };
      
      // Save locally if requested
      let localUri = null;
      if (saveLocally) {
        localUri = await this.saveDrawingLocally(drawingId, svgData, base64);
      }
      
      // Compress image if requested
      let processedBase64 = base64;
      if (compressImage && base64) {
        processedBase64 = await this.compressImage(base64);
      }
      
      return {
        drawingId,
        base64: processedBase64,
        metadata,
        localUri,
      };
    } catch (error) {
      console.error('Error processing drawing data:', error);
      throw new Error('Failed to process drawing data');
    }
  }

  /**
   * Save drawing data locally
   * @param {string} drawingId - Unique ID for the drawing
   * @param {string} svgData - SVG data
   * @param {string} base64 - Base64 encoded image data
   * @returns {string} Local URI of saved drawing
   */
  async saveDrawingLocally(drawingId, svgData, base64) {
    try {
      // Create directory for this drawing
      const drawingDir = `${this.localStorageDir}${drawingId}/`;
      await FileSystem.makeDirectoryAsync(drawingDir, { intermediates: true });
      
      // Save SVG data
      const svgUri = `${drawingDir}drawing.svg`;
      await FileSystem.writeAsStringAsync(svgUri, svgData);
      
      // Save base64 data
      if (base64) {
        const base64Uri = `${drawingDir}drawing.txt`;
        await FileSystem.writeAsStringAsync(base64Uri, base64);
      }
      
      // Save JSON metadata
      const metadataUri = `${drawingDir}metadata.json`;
      const metadata = {
        id: drawingId,
        timestamp: new Date().toISOString(),
        svgUri,
        base64Uri: base64 ? `${drawingDir}drawing.txt` : null,
      };
      await FileSystem.writeAsStringAsync(metadataUri, JSON.stringify(metadata, null, 2));
      
      return svgUri;
    } catch (error) {
      console.error('Failed to save drawing locally:', error);
      return null;
    }
  }

  /**
   * Compress image data
   * @param {string} base64 - Base64 encoded image data
   * @returns {string} Compressed base64 data
   */
  async compressImage(base64) {
    // This is a placeholder for actual compression
    // In a real implementation, you would use a library like react-native-image-manipulator
    // to compress the image before returning it
    
    return base64;
  }

  /**
   * Get device information
   * @returns {Object} Device info
   */
  getDeviceInfo() {
    return {
      platform: Platform.OS,
      version: Platform.Version,
      model: Platform.OS === 'ios' ? 'iOS Device' : 'Android Device',
    };
  }

  /**
   * Load drawing from local storage
   * @param {string} drawingId - Drawing ID
   * @returns {Object} Drawing data
   */
  async loadDrawing(drawingId) {
    try {
      const drawingDir = `${this.localStorageDir}${drawingId}/`;
      const metadataUri = `${drawingDir}metadata.json`;
      
      // Check if metadata exists
      const metadataInfo = await FileSystem.getInfoAsync(metadataUri);
      if (!metadataInfo.exists) {
        throw new Error(`Drawing with ID ${drawingId} not found`);
      }
      
      // Load metadata
      const metadataStr = await FileSystem.readAsStringAsync(metadataUri);
      const metadata = JSON.parse(metadataStr);
      
      // Load SVG data
      let svgData = null;
      if (metadata.svgUri) {
        svgData = await FileSystem.readAsStringAsync(metadata.svgUri);
      }
      
      // Load base64 data
      let base64 = null;
      if (metadata.base64Uri) {
        base64 = await FileSystem.readAsStringAsync(metadata.base64Uri);
      }
      
      return {
        drawingId,
        svgData,
        base64,
        metadata,
      };
    } catch (error) {
      console.error(`Failed to load drawing ${drawingId}:`, error);
      return null;
    }
  }

  /**
   * List all saved drawings
   * @returns {Array} Array of drawing metadata
   */
  async listSavedDrawings() {
    try {
      const dirContents = await FileSystem.readDirectoryAsync(this.localStorageDir);
      const drawings = [];
      
      for (const item of dirContents) {
        const metadataUri = `${this.localStorageDir}${item}/metadata.json`;
        try {
          const metadataInfo = await FileSystem.getInfoAsync(metadataUri);
          if (metadataInfo.exists) {
            const metadataStr = await FileSystem.readAsStringAsync(metadataUri);
            const metadata = JSON.parse(metadataStr);
            drawings.push(metadata);
          }
        } catch (error) {
          console.warn(`Failed to read metadata for drawing ${item}:`, error);
        }
      }
      
      return drawings;
    } catch (error) {
      console.error('Failed to list saved drawings:', error);
      return [];
    }
  }
}

export default new DrawingDataHandler();
