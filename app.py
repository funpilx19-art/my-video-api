from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API is Running! All Social Media Supported."

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # সব সোশ্যাল মিডিয়ার জন্য পাওয়ারফুল সেটিংস
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            # TikTok/FB এর ব্লক এড়াতে এই হেডারগুলো মাস্ট
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
            'nocheckcertificate': True,
            'geo_bypass': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিও ডাটা ফেচ করা
            info = ydl.extract_info(video_url, download=False)
            
            # সরাসরি ডাউনলোড লিঙ্ক খোঁজা
            video_direct_url = info.get('url') or (info.get('formats')[-1].get('url') if info.get('formats') else None)
            
            if video_direct_url:
                # ব্রাউজারকে সরাসরি ভিডিও ফাইলটি ডাউনলোড করতে বাধ্য করবে
                return redirect(video_direct_url)
            else:
                return jsonify({"error": "Could not extract video link. Video might be private or restricted."}), 404

    except Exception as e:
        return jsonify({"error": "Server is busy or Social Media blocked the request. Try again!"}), 500

if __name__ == "__main__":
    # Render-এর জন্য পোর্ট সেটআপ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
