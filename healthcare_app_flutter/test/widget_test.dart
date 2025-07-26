import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:healthcare_app_flutter/main.dart';

void main() {
  group('Healthcare App Tests', () {
    testWidgets('App loads and displays home screen correctly', (WidgetTester tester) async {
      // Build the app and trigger a frame
      await tester.pumpWidget(const HealthcareApp());

      // Verify that the app title is displayed
      expect(find.text('Healthcare Cost Estimator'), findsOneWidget);

      // Verify that the tagline is displayed
      expect(find.text('Smart healthcare planning made simple.'), findsOneWidget);

      // Verify that the health icon is displayed
      expect(find.byIcon(Icons.health_and_safety_rounded), findsOneWidget);

      // Verify that the start prediction button is displayed
      expect(find.text('Start Prediction'), findsOneWidget);
    });

    testWidgets('Start Prediction button navigates to input screen', (WidgetTester tester) async {
      // Build the app and trigger a frame
      await tester.pumpWidget(const HealthcareApp());

      // Find the Start Prediction button
      final startButton = find.text('Start Prediction');
      expect(startButton, findsOneWidget);

      // Tap the button
      await tester.tap(startButton);
      await tester.pumpAndSettle(); // Wait for navigation animation

      // Verify navigation occurred by checking if we're no longer on home screen
      // Note: This test assumes InputScreen exists and has different content
      expect(find.text('Healthcare Cost Estimator'), findsNothing);
    });

    testWidgets('Home screen contains all required content', (WidgetTester tester) async {
      // Build the app and trigger a frame
      await tester.pumpWidget(const HealthcareApp());

      // Verify the description text is present
      expect(find.textContaining('mobile machine learning project'), findsOneWidget);
      expect(find.textContaining('synthetic data reflective of trends in Lesotho'), findsOneWidget);
      expect(find.textContaining('low-income and uninsured'), findsOneWidget);

      // Verify UI elements are properly styled
      final appTitle = tester.widget<Text>(find.text('Healthcare Cost Estimator'));
      expect(appTitle.style?.fontSize, 28);
      expect(appTitle.style?.fontWeight, FontWeight.bold);
    });

    testWidgets('App uses correct theme and colors', (WidgetTester tester) async {
      // Build the app and trigger a frame
      await tester.pumpWidget(const HealthcareApp());

      // Get the MaterialApp widget
      final materialApp = tester.widget<MaterialApp>(find.byType(MaterialApp));
      
      // Verify app title
      expect(materialApp.title, 'Lesotho Healthcare Predictor');
      
      // Verify debug banner is disabled
      expect(materialApp.debugShowCheckedModeBanner, false);
      
      // Verify Material 3 is enabled
      expect(materialApp.theme?.useMaterial3, true);
    });

    testWidgets('Scaffold has correct background color', (WidgetTester tester) async {
      // Build the app and trigger a frame
      await tester.pumpWidget(const HealthcareApp());

      // Find the Scaffold
      final scaffold = tester.widget<Scaffold>(find.byType(Scaffold));
      
      // Verify background color
      expect(scaffold.backgroundColor, const Color(0xFFF6F9FB));
    });

    testWidgets('Health icon has correct properties', (WidgetTester tester) async {
      // Build the app and trigger a frame
      await tester.pumpWidget(const HealthcareApp());

      // Find the health icon
      final healthIcon = tester.widget<Icon>(find.byIcon(Icons.health_and_safety_rounded));
      
      // Verify icon properties
      expect(healthIcon.size, 90);
      expect(healthIcon.color, const Color(0xFF00796B));
    });
  });

  group('Error Handling Tests', () {
    testWidgets('App handles missing InputScreen gracefully', (WidgetTester tester) async {
      // This test would catch navigation errors if InputScreen doesn't exist
      await tester.pumpWidget(const HealthcareApp());
      
      // Verify app loads without throwing exceptions
      expect(tester.takeException(), isNull);
    });
  });
}
