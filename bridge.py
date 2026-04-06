import requests, random, string
from flask import Flask, request, jsonify

app = Flask(__name__)

# بياناتك
TOKEN = "8793262042:AAG_WJTh3In4vfK2gsZyPQ_WGjU8txvK9Os"
ID = "6696928411"

def get_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@app.route('/check', methods=['GET'])
def check_user():
    user = request.args.get('user')
    if not user: return jsonify({"error": "No user"}), 400

    # هيدرز "المحترف" - محاكاة كاملة لمتصفح آمن
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.tiktok.com/signup",
        "Origin": "https://www.tiktok.com",
        "Cookie": f"tt_webid_v2={get_random_string(19)};" # توليد كوكيز وهمي لكل فحص
    }

    url = f"https://www.tiktok.com/api/uniqueid/check/?unique_id={user}&aid=1988"

    try:
        # فحص مباشر مع جلسة
        response = session.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # إذا كان status_code هو 0 يعني اليوزر متاح 100%
        if data.get("status_code") == 0:
            # إرسال الصيد فوراً
            msg = f"🚀 هب يابطل! صيد نووي: @{user}\n🎯 النوع: تيك توك"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")
            return jsonify({"status": "available", "user": user})
        else:
            return jsonify({"status": "taken"})
            
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
