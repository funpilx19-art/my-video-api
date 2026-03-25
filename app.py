from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API is Ready!"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL"}), 400

    try:
        # এই সেটিংসটি TikTok এর ব্লক ভাঙ্গতে সাহায্য করবে
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_link = info.get('url')
            return redirect(video_link)

    except Exception as e:
        return jsonify({"error": "Failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
