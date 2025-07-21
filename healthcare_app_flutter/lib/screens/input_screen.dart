import 'package:flutter/material.dart';
import '../widgets/input_form.dart';

class InputScreen extends StatefulWidget {
  const InputScreen({super.key});

  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Healthcare Cost Estimator')),
      body: const Padding(
        padding: EdgeInsets.all(16.0),
        child: InputForm(),
      ),
    );
  }
}
