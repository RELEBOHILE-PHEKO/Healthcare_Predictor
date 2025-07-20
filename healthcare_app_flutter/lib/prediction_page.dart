import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:google_fonts/google_fonts.dart';

class PredictionPage extends StatefulWidget {
  const PredictionPage({super.key});

  @override
  State<PredictionPage> createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {
  final TextEditingController _priceIndexController = TextEditingController();
  final TextEditingController _bedsController = TextEditingController();
  final TextEditingController _publicSpendingController =
      TextEditingController();

  String _predictionResult = '';
  bool _loading = false;
  bool _showResult = false;

  Future<void> _makePrediction() async {
    setState(() {
      _loading = true;
      _predictionResult = '';
      _showResult = false;
    });

    final url = Uri.parse(
      'http://127.0.0.1:8000/predict',
    ); // 🔁 Change to your Render URL later

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'price_index': double.parse(_priceIndexController.text),
          'hospital_beds': double.parse(_bedsController.text),
          'public_spending_pct': double.parse(_publicSpendingController.text),
        }),
      );

      final data = jsonDecode(response.body);
      if (response.statusCode == 200 && data.containsKey('prediction')) {
        setState(() {
          _predictionResult =
              'Estimated Cost: \$${data['prediction'].toStringAsFixed(2)}';
          _showResult = true;
        });
      } else {
        setState(() {
          _predictionResult = 'Error: ${response.body}';
          _showResult = true;
        });
      }
    } catch (e) {
      setState(() {
        _predictionResult = 'Invalid input or server error.';
        _showResult = true;
      });
    } finally {
      setState(() => _loading = false);
    }
  }

  Widget buildInputField(String label, TextEditingController controller) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextField(
        controller: controller,
        keyboardType: TextInputType.numberWithOptions(decimal: true),
        decoration: InputDecoration(
          labelText: label,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: Colors.grey[100],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Healthcare Cost Predictor',
          style: GoogleFonts.poppins(fontWeight: FontWeight.w600),
        ),
        centerTitle: true,
        backgroundColor: Colors.teal,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            buildInputField('Price Index', _priceIndexController),
            buildInputField('Hospital Beds per 1,000', _bedsController),
            buildInputField('Public Spending %', _publicSpendingController),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.analytics_outlined),
                label: Text(
                  'Predict',
                  style: GoogleFonts.poppins(fontSize: 16),
                ),
                onPressed: _makePrediction,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  backgroundColor: Colors.teal,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),
            if (_loading)
              const CircularProgressIndicator()
            else if (_showResult)
              Card(
                elevation: 3,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Text(
                    _predictionResult,
                    style: GoogleFonts.poppins(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
