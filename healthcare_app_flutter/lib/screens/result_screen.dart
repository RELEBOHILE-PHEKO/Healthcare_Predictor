import 'package:flutter/material.dart';

class ResultScreen extends StatefulWidget {
  final double cost;
  final String modelInfo;

  const ResultScreen({
    super.key,
    required this.cost,
    required this.modelInfo,
  });

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.teal[50],
      appBar: AppBar(title: const Text('Estimated Cost')),
      body: Center(
        child: Card(
          margin: const EdgeInsets.all(20),
          elevation: 5,
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.health_and_safety, color: Colors.teal, size: 80),
                const SizedBox(height: 20),
                Text("Predicted Healthcare Cost", style: Theme.of(context).textTheme.titleLarge),
                Text(
                  "M${widget.cost.toStringAsFixed(2)}",
                  style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: Colors.teal),
                ),
                const SizedBox(height: 20),
                Text(widget.modelInfo, textAlign: TextAlign.center),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Try Again'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
