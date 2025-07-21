import 'package:flutter/material.dart';
import 'screens/input_screen.dart';

void main() {
  runApp(const HealthcareApp());
}

class HealthcareApp extends StatelessWidget {
  const HealthcareApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lesotho Healthcare Predictor',
      theme: ThemeData(
        fontFamily: 'Roboto',
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      debugShowCheckedModeBanner: false,
      home: const InputScreen(),
    );
  }
}
