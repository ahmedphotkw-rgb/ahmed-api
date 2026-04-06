from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- بياناتك اللي انطيتني إياها ---
TOKEN = "8793262042:AAG_WJTh3In4vfK2gsZyPQ_WGjU8txvK9Os"
ID = "6696928411"

@app.route('/')
def home():
    return "<h1>Ahmed's API Sniper is Live!</h1>"

@app.route('/check', methods=['GET'])
def check_user():
    # هذا السطر يستلم اسم اليوزر من أداة كالي
    user = request.args.get('user')
    
    if not user:
        return jsonify({"error": "No user provided"}), 400

    # رابط الفحص المباشر
    url = f"https://www.tiktok.com/@{user}"
    
    try:
        # هنا السيرفر يفحص اليوزر
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        # إذا كانت النتيجة 404 معناها اليوزر متاح (صيد)
        if response.status_code == 404:
            msg = f"✅ هب يا وحش! صيد جديد:\n👤 User: @{user}\n🚀 By Ahmed Sniper"
            # إرسال الرسالة لتليجرام مالتك
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")
            return jsonify({"status": "available", "user": user})
        
        return jsonify({"status": "taken"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # تشغيل السيرفر
    app.run(host='0.0.0.0', port=5000)

