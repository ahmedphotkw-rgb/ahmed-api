from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "8793262042:AAG_WJTh3In4vfK2gsZyPQ_WGjU8txvK9Os"
ID = "6696928411"

@app.route('/check', methods=['GET'])
def check_user():
    user = request.args.get('user')
    if not user: return jsonify({"error": "No user"}), 400

    # هيدرز حقيقية توهم تيك توك إنك متصفح آيفون
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    url = f"https://www.tiktok.com/@{user}"
    
    try:
        # السر هنا: نمنع التحويل (allow_redirects=False)
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=False)
        
        # تيك توك يعطي 404 لليوزر المتاح إذا منعنا التحويل
        if response.status_code == 404:
            msg = f"✅ صيد مؤكد ياعبادي! \n👤 User: @{user}\n🚀 Type: TikTok"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")
            return jsonify({"status": "available", "user": user})
        
        return jsonify({"status": "taken"})
    except:
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
