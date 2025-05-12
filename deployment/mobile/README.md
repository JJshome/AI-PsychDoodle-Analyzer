# AI-PsychDoodle-Analyzer Mobile App Deployment

This directory contains configuration and deployment scripts for the AI-PsychDoodle-Analyzer mobile applications.

## Directory Structure

```
mobile/
├── android/           # Android-specific configurations
├── ios/               # iOS-specific configurations
├── flutter/           # Flutter integration files
├── react-native/      # React Native integration files
└── assets/            # Shared assets for mobile apps
```

## Deployment Prerequisites

### Android

- Android Studio 4.2+
- Java Development Kit (JDK) 11+
- Android SDK 30+
- Gradle 7.0+

### iOS

- Xcode 13+
- CocoaPods 1.11+
- iOS 14.0+ deployment target
- macOS development machine

### Flutter

- Flutter SDK 3.0+
- Dart 2.17+

### React Native

- Node.js 16+
- npm 8+ or Yarn 1.22+
- React Native CLI 0.69+

## Configuration

### API Configuration

Edit the `assets/config.json` file to configure the API connection:

```json
{
  "api": {
    "baseUrl": "https://your-api-server.com",
    "apiKey": "your_api_key_if_required",
    "timeout": 30000
  },
  "analytics": {
    "enabled": true,
    "trackingId": "UA-XXXXXXXX-X"
  },
  "features": {
    "offlineMode": true,
    "debugMode": false
  }
}
```

### App Icons and Splash Screens

Place your app icons and splash screens in the `assets/images/` directory following the naming conventions for each platform.

## Build Instructions

### Android

1. Navigate to the Android project directory:
   ```bash
   cd android
   ```

2. Build the release APK:
   ```bash
   ./gradlew assembleRelease
   ```

3. The APK will be available at `android/app/build/outputs/apk/release/app-release.apk`

### iOS

1. Navigate to the iOS project directory:
   ```bash
   cd ios
   ```

2. Install dependencies:
   ```bash
   pod install
   ```

3. Open the workspace in Xcode:
   ```bash
   open PsychDoodleAnalyzer.xcworkspace
   ```

4. Build the project for release in Xcode (Product → Archive)

## Continuous Integration / Continuous Deployment

### CI/CD Pipeline

We use GitHub Actions for automated builds. See the workflow configurations in `.github/workflows/`:

- `android-build.yml`: Android CI build
- `ios-build.yml`: iOS CI build
- `app-release.yml`: Release deployment workflow

### App Store / Play Store Deployment

#### Google Play Store

1. Sign the APK with your release key
2. Use the Google Play Developer API to automate publishing

#### Apple App Store

1. Use App Store Connect API for automated submissions
2. Manage TestFlight releases through CI/CD

## Troubleshooting

### Common Issues

1. **API Connection Failures**
   - Verify network permissions in app manifests
   - Check API URL configuration
   - Ensure proper SSL certificate handling

2. **Performance Issues**
   - Reduce model size for inference
   - Implement image size limitations
   - Use background processing for analysis

3. **Deployment Rejections**
   - Ensure privacy policy addresses drawing data collection
   - Document psychological analysis methodology
   - Provide disclaimer about analysis accuracy

## Support

For any deployment issues, contact the development team at [dev@example.com](mailto:dev@example.com)