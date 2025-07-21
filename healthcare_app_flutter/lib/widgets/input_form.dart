import 'package:flutter/material.dart';
import '../screens/result_screen.dart';
import '../services/api_service.dart';

class InputForm extends StatefulWidget {
  const InputForm({super.key});

  @override
  State<InputForm> createState() => _InputFormState();
}

class _InputFormState extends State<InputForm> {
  final formKey = GlobalKey<FormState>();

  final ageController = TextEditingController();
  final incomeController = TextEditingController();
  final householdSizeController = TextEditingController();

  String sex = 'male';
  String region = 'Maseru';
  String employment = 'employed';
  String access = 'easy';
  String healthcareType = 'public';
  bool isInsured = true;

  bool isLoading = false;

  Future<void> submit() async {
    if (!formKey.currentState!.validate()) return;

    setState(() => isLoading = true);
    final result = await ApiService.predict({
      "age": int.parse(ageController.text),
      "sex": sex,
      "region": region,
      "is_insured": isInsured ? 1 : 0,
      "employment": employment,
      "household_size": int.parse(householdSizeController.text),
      "primary_healthcare_access": access,
      "annual_income": double.parse(incomeController.text),
      "healthcare_type": healthcareType,
    });

    setState(() => isLoading = false);

    if (result != null) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text("Prediction successful!"),
          backgroundColor: Colors.teal,
        ));
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ResultScreen(
              cost: result["predicted_healthcare_cost"],
              modelInfo: result["confidence_info"],
            ),
          ),
        );
      }
    } else {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text("Something went wrong. Try again."),
          backgroundColor: Colors.red,
        ));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: formKey,
      child: ListView(
        children: [
          TextFormField(
            controller: ageController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: "Age"),
            validator: (v) => v == null || v.isEmpty ? "Enter age" : null,
          ),
          TextFormField(
            controller: incomeController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: "Annual Income (LSL)"),
            validator: (v) => v == null || v.isEmpty ? "Enter income" : null,
          ),
          TextFormField(
            controller: householdSizeController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: "Household Size"),
            validator: (v) => v == null || v.isEmpty ? "Enter household size" : null,
          ),
          const SizedBox(height: 10),
          DropdownButtonFormField(
            value: sex,
            items: ['male', 'female'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => sex = v!),
            decoration: const InputDecoration(labelText: "Sex"),
          ),
          DropdownButtonFormField(
            value: region,
            items: ['Maseru', 'Leribe', 'Butha-Buthe', 'Thaba-Tseka', 'Mohale\'s Hoek', 'Mafeteng', 'Qacha\'s Nek', 'Quthing']
                .map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => region = v!),
            decoration: const InputDecoration(labelText: "Region"),
          ),
          DropdownButtonFormField(
            value: employment,
            items: ['employed', 'unemployed', 'self-employed'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => employment = v!),
            decoration: const InputDecoration(labelText: "Employment Status"),
          ),
          DropdownButtonFormField(
            value: access,
            items: ['easy', 'moderate', 'difficult'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => access = v!),
            decoration: const InputDecoration(labelText: "Access to Primary Healthcare"),
          ),
          DropdownButtonFormField(
            value: healthcareType,
            items: ['public', 'private'].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => healthcareType = v!),
            decoration: const InputDecoration(labelText: "Healthcare Type"),
          ),
          SwitchListTile(
            title: const Text("Are you insured?"),
            value: isInsured,
            onChanged: (v) => setState(() => isInsured = v),
          ),
          const SizedBox(height: 20),
          isLoading
              ? const Center(child: CircularProgressIndicator())
              : ElevatedButton.icon(
            icon: const Icon(Icons.send),
            onPressed: submit,
            label: const Text("Predict Healthcare Cost"),
          ),
        ],
      ),
    );
  }
}
