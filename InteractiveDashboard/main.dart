import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool _isDarkMode = false;
  String _language = 'en';

  @override
  void initState() {
    super.initState();
    _loadTheme();
  }

  void _loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _isDarkMode = prefs.getBool('darkMode') ?? false;
      _language = prefs.getString('language') ?? 'en';
    });
  }

  void _toggleTheme() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _isDarkMode = !_isDarkMode;
      prefs.setBool('darkMode', _isDarkMode);
    });
  }

  void _changeLanguage(String lang) async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _language = lang;
      prefs.setString('language', lang);
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: _isDarkMode ? ThemeData.dark() : ThemeData.light(),
      home: HomeScreen(
        isDarkMode: _isDarkMode,
        toggleTheme: _toggleTheme,
        changeLanguage: _changeLanguage,
        language: _language,
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  final bool isDarkMode;
  final VoidCallback toggleTheme;
  final Function(String) changeLanguage;
  final String language;

  HomeScreen({
    required this.isDarkMode,
    required this.toggleTheme,
    required this.changeLanguage,
    required this.language,
  });

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  stt.SpeechToText _speech = stt.SpeechToText();
  String _searchText = "";

  final Map<String, Map<String, String>> _translations = {
    'en': {
      'title': "Smart Traffic Management",
      'subtitle': "Efficient & Intelligent Traffic Solutions",
      'user_dashboard': "User Dashboard",
      'authorities_dashboard': "Authorities Dashboard",
      'search': "Search...",
      'voice_command': "Voice Command"
    },
    'hi': {
      'title': "स्मार्ट ट्रैफिक प्रबंधन",
      'subtitle': "कुशल और बुद्धिमान ट्रैफिक समाधान",
      'user_dashboard': "उपयोगकर्ता डैशबोर्ड",
      'authorities_dashboard': "प्राधिकरण डैशबोर्ड",
      'search': "खोजें...",
      'voice_command': "वॉयस कमांड"
    },
    'ta': {
      'title': "சmart டிராஃபிக் மேலாண்மை",
      'subtitle': "திறமையான போக்குவரத்து தீர்வுகள்",
      'user_dashboard': "பயனர் டாஷ்போர்டு",
      'authorities_dashboard': "அதிகாரிகள் டாஷ்போர்டு",
      'search': "தேடுக...",
      'voice_command': "குரல் கட்டளை"
    },
    'bn': {
      'title': "স্মার্ট ট্রাফিক ব্যবস্থাপনা",
      'subtitle': "দক্ষ ট্রাফিক সমাধান",
      'user_dashboard': "ব্যবহারকারী ড্যাশবোর্ড",
      'authorities_dashboard': "কর্তৃপক্ষের ড্যাশবোর্ড",
      'search': "অনুসন্ধান করুন...",
      'voice_command': "ভয়েস কমান্ড"
    }
  };

  void _startListening() async {
    bool available = await _speech.initialize();
    if (available) {
      _speech.listen(onResult: (result) {
        setState(() {
          _searchText = result.recognizedWords;
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    var t = _translations[widget.language]!;
    return Scaffold(
      appBar: AppBar(
        title: Text(t['title']!, style: GoogleFonts.poppins()),
        actions: [
          IconButton(
            icon: Icon(widget.isDarkMode ? Icons.wb_sunny : Icons.nightlight_round),
            onPressed: widget.toggleTheme,
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Text(t['subtitle']!,
                style: GoogleFonts.poppins(fontSize: 18, fontWeight: FontWeight.w500)),
            SizedBox(height: 20),
            TextField(
              decoration: InputDecoration(
                labelText: t['search'],
                border: OutlineInputBorder(),
              ),
              controller: TextEditingController(text: _searchText),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: _startListening,
              child: Text(t['voice_command']!),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () {},
                  child: Text(t['user_dashboard']!),
                ),
                ElevatedButton(
                  onPressed: () {},
                  child: Text(t['authorities_dashboard']!),
                ),
              ],
            ),
            SizedBox(height: 20),
            DropdownButton<String>(
              value: widget.language,
              onChanged: (value) {
                if (value != null) {
                  widget.changeLanguage(value);
                }
              },
              items: ['en', 'hi', 'ta', 'bn']
                  .map((lang) => DropdownMenuItem(
                        value: lang,
                        child: Text(lang.toUpperCase()),
                      ))
                  .toList(),
            )
          ],
        ),
      ),
    );
  }
}

