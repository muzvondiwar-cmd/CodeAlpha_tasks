from flask import Flask, render_template, request, jsonify
from google.cloud import translate_v2 as translate

app = Flask(__name__)

translate_client = translate.Client()

LANGUAGES = {
    "auto" : "auto",
    "english" : "en",
    "french" : "fr",
    "spanish" : "es"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate_text():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()
        source_language = data.get("source_language")
        target_language = data.get("target_language")

        if not text:
            return jsonify({
                "success": False,
                "message": "Please enter text to translate."
            }), 400
        
        if not source_language or not target_language:
            return jsonify({
                "success": False,
                "message": "Please select both source and target language"
            }), 400
        
        source_code = LANGUAGES.get(source_language)
        target_code = LANGUAGES.get(target_language)

        if not source_code or not target_code:
            return jsonify({
                "success": False,
                "message": "Unspported language selected."
            }), 400
        
        if source_code == target_code:
            return jsonify({
                "success": False,
                "message": "Source and Target languages cannot be the same."
            }), 400
        
        if source_code == "auto":
            result = translate_client.translate(
                text,
                target_language=target_code
            )

        else:
            result = translate_client.translate(
                text,
                source_language=source_code,
                target_language=target_code
            )

        return jsonify({
            "success": True,
            "translated_text": result["translatedText"],
            "detected_source_language": result.get("detectedSourceLanguage", source_code)
        })
    
    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Translation Failed. Please check your Google API Credentials or Internet connection",
            "error": str(error)
        }), 500
    
if __name__ == "__main__":
    app.run(debug=True)