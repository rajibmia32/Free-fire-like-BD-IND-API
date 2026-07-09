import requests
import json
import time

UIDPASS_FILE = "uidpass.json"
TOKEN_JSON_FILE = "tokens.json"

API_URL = "https://jwttoken-ten.vercel.app/token"

def read_uidpass():
    try:
        with open(UIDPASS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = [data]
            print(f"✅ {len(data)}টা অ্যাকাউন্ট পাওয়া গেছে")
            return data
    except Exception as e:
        print(f"❌ uidpass.json পড়তে সমস্যা: {e}")
        return []

def fetch_token(uid, password):
    try:
        print(f"   🔍 Requesting token for UID: {uid}")
        params = {"uid": uid, "password": password}
        response = requests.get(API_URL, params=params, timeout=25)
        
        print(f"   📡 Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ HTTP Error: {response.text[:200]}")
            return None

        data = response.json()
        print(f"   📥 API Response: {data}")

        if data.get("status") == "success":
            token = data.get("token")
            if token:
                print(f"   ✅ Token Received (length: {len(token)})")
                return token
        else:
            print(f"   ❌ API Failed: {data.get('message', data)}")
        return None

    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return None

def save_tokens(tokens_list):
    with open(TOKEN_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens_list, f, ensure_ascii=False, indent=4)
    
    print(f"\n✅ {len(tokens_list)}টা টোকেন tokens.json এ সেভ হয়েছে")

def main():
    print("🚀 JWT Token Updater Starting...\n")
    
    uidpass_list = read_uidpass()
    if not uidpass_list:
        return

    new_tokens = []
    success = 0

    for i, acc in enumerate(uidpass_list, 1):
        uid = str(acc.get("uid", "")).strip()
        password = str(acc.get("password", "")).strip()

        if not uid or not password:
            print(f"[{i}] ❌ UID বা Password খালি")
            continue

        token = fetch_token(uid, password)

        if token:
            new_tokens.append({"token": token})
            success += 1
        else:
            print(f"[{i}] ❌ Token পাওয়া যায়নি")

        time.sleep(2.5)

    save_tokens(new_tokens)
    print(f"\n🎯 মোট সফল: {success}/{len(uidpass_list)}")

if __name__ == "__main__":
    main()
