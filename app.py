from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # সব ধরণের কানেকশন এলাউ করবে

@app.route('/')
def home():
    return "API is Running!"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # কুকিজ ছাড়া অনেক সময় ভিডিও পায় না, তাই সেটিংস আপডেট
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_direct_url = info.get('url')
            
            if video_direct_url:
                return redirect(video_direct_url)
            else:
                return jsonify({"error": "Video link not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
