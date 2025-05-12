/**
 * DrawingCanvas Component
 * 
 * A component for capturing user drawings and doodles
 */

import React, { useRef, useState, useEffect } from 'react';
import { View, StyleSheet, PanResponder, Dimensions } from 'react-native';
import Svg, { Path, G } from 'react-native-svg';

const DrawingCanvas = ({
  height = Dimensions.get('window').height * 0.6,
  width = Dimensions.get('window').width * 0.9,
  strokeColor = '#000000',
  strokeWidth = 4,
  backgroundColor = '#FFFFFF',
  originalImage = null,
  isTracing = false,
  onDrawingComplete = () => {},
  onDrawingStart = () => {},
  onClear = () => {},
}) => {
  // Store current drawing paths
  const [paths, setPaths] = useState([]);
  // Current drawing path
  const [currentPath, setCurrentPath] = useState('');
  // Track if currently drawing
  const [isDrawing, setIsDrawing] = useState(false);
  // Store start time for tracing measurement
  const [startTime, setStartTime] = useState(null);
  // Store SVG content for export
  const svgRef = useRef(null);

  // Create PanResponder for touch events
  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onStartShouldSetPanResponderCapture: () => true,
      onMoveShouldSetPanResponder: () => true,
      onMoveShouldSetPanResponderCapture: () => true,

      onPanResponderGrant: (event) => {
        // Start drawing
        const { locationX, locationY } = event.nativeEvent;
        setCurrentPath(`M${locationX},${locationY}`);
        setIsDrawing(true);
        
        // If tracing, record start time
        if (isTracing && !startTime) {
          setStartTime(Date.now());
        }
        
        // Callback for drawing start
        onDrawingStart();
      },

      onPanResponderMove: (event) => {
        if (isDrawing) {
          const { locationX, locationY } = event.nativeEvent;
          setCurrentPath(prevPath => `${prevPath} L${locationX},${locationY}`);
        }
      },

      onPanResponderRelease: () => {
        // End current path and add to paths array
        if (isDrawing && currentPath) {
          setPaths(prevPaths => [...prevPaths, { d: currentPath, stroke: strokeColor, strokeWidth }]);
          setCurrentPath('');
          setIsDrawing(false);
        }
      },
    })
  ).current;

  // Clear drawing
  const clearCanvas = () => {
    setPaths([]);
    setCurrentPath('');
    setStartTime(null);
    onClear();
  };

  // Export drawing as base64 encoded SVG
  const exportDrawing = () => {
    if (svgRef.current && paths.length > 0) {
      // Calculate drawing time if tracing
      let drawingTime = null;
      if (isTracing && startTime) {
        drawingTime = (Date.now() - startTime) / 1000; // Convert to seconds
      }
      
      // Convert SVG content to a string
      const svgData = `
        <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">
          <rect width="100%" height="100%" fill="${backgroundColor}" />
          ${paths.map(path => 
            `<path d="${path.d}" stroke="${path.stroke}" stroke-width="${path.strokeWidth}" fill="none" />`
          ).join('')}
        </svg>
      `;
      
      // Convert to base64
      const base64 = btoa(svgData);
      
      // Call completion callback with drawing data
      onDrawingComplete({
        svgData,
        base64,
        drawingTime,
        paths,
      });
      
      // Reset start time if tracing
      if (isTracing) {
        setStartTime(null);
      }
    }
  };

  // Expose methods to parent component
  useEffect(() => {
    // Parent can use this to access export and clear functions
    if (typeof onDrawingComplete === 'function') {
      onDrawingComplete({
        exportDrawing,
        clearCanvas,
      });
    }
  }, [paths]);

  return (
    <View
      style={[styles.container, { height, width, backgroundColor }]}
      {...panResponder.panHandlers}
    >
      {/* Background original image for tracing */}
      {isTracing && originalImage && (
        <View style={styles.originalImageContainer}>
          {originalImage}
        </View>
      )}
      
      {/* SVG drawing surface */}
      <Svg 
        ref={svgRef} 
        height="100%" 
        width="100%" 
        style={styles.drawingSurface}
      >
        <G>
          {/* Draw completed paths */}
          {paths.map((path, index) => (
            <Path
              key={index}
              d={path.d}
              stroke={path.stroke}
              strokeWidth={path.strokeWidth}
              fill="none"
            />
          ))}
          
          {/* Draw current path */}
          {currentPath ? (
            <Path
              d={currentPath}
              stroke={strokeColor}
              strokeWidth={strokeWidth}
              fill="none"
            />
          ) : null}
        </G>
      </Svg>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#CCCCCC',
    position: 'relative',
  },
  drawingSurface: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  originalImageContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    opacity: 0.3, // Semi-transparent to see your drawing on top
    zIndex: -1,
  },
});

export default DrawingCanvas;
