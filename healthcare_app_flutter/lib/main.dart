import 'package:flutter/material.dart';
import 'prediction_page.dart';

void main() {
  runApp(const HealthCarePredictorApp());
}

class HealthCarePredictorApp extends StatelessWidget {
  const HealthCarePredictorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Healthcare Cost Predictor',
      theme: ThemeData(primarySwatch: Colors.teal),
      home: const PredictionPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}
