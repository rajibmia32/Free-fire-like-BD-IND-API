import requests
import json
import time
import os

# API URL
API_URL = "https://jwttoken-ten.vercel.app/token"

# Regional Configurations
REGIONS = {
    "BD": {
        "uidpass_file": "uidpass_bd.json",
        "token_file": "token_bd.json"
    },
    "IND": {
        "uidpass_file": "uidpass_ind.json",
        "token_file": "token_ind.json"
    }
}

def read_uidpass(file_path):
    if not os.path.exists(file_path):
        print(f"⚠️  ফাইল পাওয়া যায়নি: {file_path}")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = [data]
            return data
    except Exception as e:
        print(f"❌ {file_path} পড়তে সমস্যা: {e}")
        return []

def fetch_token(uid, password):
    try:
        params = {"uid": uid, "password": password}
        response = requests.get(API_URL, params=params, timeout=25)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("token")
        return None
    except Exception:
        return None

def process_region(region_name, config):
    print(f"\n🌍 Processing Region: {region_name}")
    uidpass_list = read_uidpass(config["uidpass_file"])
    
    if not uidpass_list:
        print(f"ℹ️  {region_name} এর জন্য কোনো অ্যাকাউন্ট পাওয়া যায়নি।")
        return

    print(f"✅ {len(uidpass_list)}টা অ্যাকাউন্ট পাওয়া গেছে।")
    new_tokens = []
    success = 0

    for i, acc in enumerate(uidpass_list, 1):
        uid = str(acc.get("uid", "")).strip()
        password = str(acc.get("password", "")).strip()

        if not uid or not password:
            continue

        print(f"   [{i}/{len(uidpass_list)}] Requesting token for UID: {uid}...", end="\r")
        token = fetch_token(uid, password)

        if token:
            new_tokens.append({"token": token})
            success += 1
        
        time.sleep(2.0) # Delay to avoid rate limits

    if new_tokens:
        with open(config["token_file"], "w", encoding="utf-8") as f:
            json.dump(new_tokens, f, ensure_ascii=False, indent=4)
        print(f"\n✅ {success}টা টোকেন {config['token_file']} এ সেভ হয়েছে।")
    else:
        print(f"\n❌ {region_name} এর জন্য কোনো টোকেন পাওয়া যায়নি।")

def main():
    print("🚀 Regional JWT Token Updater Starting...")
    
    for region, config in REGIONS.items():
        process_region(region, config)
        
    print("\n🎯 All regions processed successfully!")

if __name__ == "__main__":
    main()
