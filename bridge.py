from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "8793262042:AAG_WJTh3In4vfK2gsZyPQ_WGjU8txvK9Os"
ID = "6696928411"

@app.route('/check', methods=['GET'])
def check_user():
    user = request.args.get('user')
    if not user: return jsonify({"error": "No user"}), 400

    # رابط الفحص المباشر (API الداخلي)
    # هذا الرابط يعطينا إذا اليوزر متاح للتسجيل أو لا
    url = f"https://www.tiktok.com/api/uniqueid/check/?unique_id={user}&region=IQ&aid=1988"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.tiktok.com/signup"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # status_code 0 معناه اليوزر متاح للتسجيل (صيد)
        if data.get("status_code") == 0:
            msg = f"✅ صيد مؤكد ياعبادي! \n👤 User: @{user}\n🚀 Type: TikTok Sniper"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")
            return jsonify({"status": "available", "user": user})
        else:
            return jsonify({"status": "taken"})
            
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
