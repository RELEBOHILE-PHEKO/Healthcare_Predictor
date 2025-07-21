import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:8000'; // Use IP for emulator or localhost:8000

  static Future<Map<String, dynamic>?> predict(Map<String, dynamic> data) async {
    final url = Uri.parse('$baseUrl/predict');

    try {
      final response = await http.post(url,
          headers: {"Content-Type": "application/json"},
          body: json.encode(data));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        print("Error: ${response.statusCode}, ${response.body}");
        return null;
      }
    } catch (e) {
      print("Exception: $e");
      return null;
    }
  }
}