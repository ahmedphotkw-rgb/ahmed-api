from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# بيانات التليجرام مالتك
TOKEN = "8793262042:AAG_WJTh3In4vfK2gsZyPQ_WGjU8txvK9Os"
ID = "6696928411"

@app.route('/check', methods=['GET'])
def check_user():
    user = request.args.get('user')
    if not user: return jsonify({"error": "No user"}), 400

    url = 'https://www.instagram.com/api/v1/users/check_username/'
    
    # البصمة اللي صيدتها أنت (نقلتها لك هنا بدقة)
    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'csrftoken=3Cdgpg_nalU2CckHOH1wu_; datr=AYTQaaX4pnz9aNylmkyKhFW8; ig_did=C148D1E0-D17F-4FE5-A1EB-7F0BC2596FF5; mid=adCEAQABAAFggjsTkpCFkypL3haz;',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/emailsignup/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'x-csrftoken': '3Cdgpg_nalU2CckHOH1wu_',
        'x-ig-app-id': '936619743392459'
    }

    data = {'username': user}

    try:
        # فحص يوزر إنستغرام
        response = requests.post(url, headers=headers, data=data, timeout=10)
        res_json = response.json()
        
        # إذا كان متاح للتسجيل
        if res_json.get("status") == "ok" and res_json.get("available") == True:
            msg = f"💎 صيد إنستغرام ملكي! \n👤 User: @{user}\n🚀 Type: Instagram"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")
            return jsonify({"status": "available", "user": user})
        else:
            return jsonify({"status": "taken"})
            
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
