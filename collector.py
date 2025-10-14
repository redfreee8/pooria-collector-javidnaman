import requests
import base64
import urllib.parse
import random
from typing import List, Set

# .لیستی از جاویدنامان خیزش زن، زندگی، آزادی به فینگلیش برای سازگاری با همه اپلیکیشن‌ها
JAVID_NAMAN: List[str] = [
    "Mahsa Amini", "Nika Shakarami", "Sarina Esmailzadeh", "Hadis Najafi", "Minoo Majidi", "Ghazaleh Chalabi",
    "Hananeh Kia", "Mohsen Shekari", "Majidreza Rahnavard", "Mohammad Mehdi Karami", "Seyed Mohammad Hosseini",
    "Kian Pirfalak", "Khadijeh Naghdi", "Javad Heydari", "Fereshteh Ahmadi", "Reza Shahparnia", "Erfan Zamani",
    "Yalda Aghafazli", "Abolfazl Adinezadeh", "Asra Panahi", "Mohsen Ghaysari", "Hamidreza Rouhi", "Aylar Haghi",
    "Sepehr Maghsoudi", "Mehdi Zare Ashkzari", "Donya Farhadi", "Arshia Emamgholizadeh", "Negin Abdolmaleki",
    "Mehrshad Shahidi", "Sarina Saedi", "Komar Daroftadeh", "Behnaz Afshari", "Armin Sayadi", "Amirhossein Shams",
    "Danial Pabandi", "Erfan Khazaei", "Shirin Alizadeh", "Fouad Mohammadi", "Pouya Sheida", "Mehregan Zahmatkesh",
    "Siavash Mahmoudi", "Pedram Azarnoush", "Ali Roozbahani", "Mehdi Hazrati", "Arman Emadi", "Milad Saeidianjou",
    "Aida Rostami", "Ali Seyedi", "AmirMehdi Farrokhipour", "Samaneh Niknam", "Esmaeil Dezvar", "Fereydoun Mahmoudi",
    "Reza Lotfi", "Zakaria Khiyal", "Momen Zandkarimi", "Sadraddin Litani", "Atefeh Naami", "Arnika Ghaem Maghami",
    "MohammadHassan Torkaman", "Mobin Mirzaei", "Javad Mousavi", "Aidin Darvish", "Matin Nosrati", "Sina Naderi",
    "Erfan Kakaei", "Esmaeil Moloudi", "Arian Moridi", "Sina Molayeri", "Omid Hassani", "Arian Khoshgouvarian",
    "Rouzbeh Khademian", "Reza Kazemi", "Hamid Goli", "Mohammad Haji Rasoulpour", "Shomal Khadiripour",
    "Ebrahim Mirzaei", "Nasrin Ghaderi", "Arman Akbari", "Pouria Ahmadi", "MohammadAmin Hashemi", "Amir Falahatdoust",
    "Milad Khoshkam", "Houman Abdollahi", "AmirMohammad Rahimi", "Shouresh Niknam", "MohammadHossein Kamandloo",
    "Mahmoud Ahmadi", "Hamidreza Barahouyi", "Mohammad Eghbal Shahnavazi", "Mohammad Rigi", "Omar Shahnavazi",
    "Samer Hashemzehi", "Matin Ghanbarzehi", "Jaber Shirouzehi"
]

# لیست لینک‌های سابسکریپشن شما
SUB_LINKS: List[str] = [
    "https://raw.githubusercontent.com/liketolivefree/kobabi/main/sub.txt",
    "https://long-credit-187f.mehdipost675.workers.dev/?token=jHfTut2MRAd9yyPUJQ7K05kiRFDW4hKV",
    "https://withered-math-1242.mehdipost675.workers.dev/?token=U47yXioeT6Q4nwXbkDztDBQBsaDoB5UH",
    "https://lively-dream-c48b.mehdipost675.workers.dev/?token=fedfed7b41b828f17cfb2371c8ee16df"
]

# نام فایل خروجی برای لینک ساب نهایی
OUTPUT_FILENAME: str = "POORIAJavidanIran.txt"

# اضافه کردن هدر برای اینکه درخواست‌ها طبیعی‌تر به نظر برسند
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_configs_from_sub(url: str) -> List[str]:
    """کانفیگ‌ها را از یک لینک سابسکریپشن دانلود و استخراج می‌کند."""
    try:
        print(f"در حال دریافت کانفیگ از: {url}")
        response = requests.get(url, timeout=20, headers=HEADERS)
        response.raise_for_status()
        
        content = response.text
        decoded_content = ""
        
        try:
            missing_padding = len(content) % 4
            if missing_padding:
                content += '=' * (4 - missing_padding)
            decoded_content = base64.b64decode(content).decode('utf-8')
        except Exception:
            decoded_content = content

        configs = [line.strip() for line in decoded_content.splitlines() if line.strip()]
        print(f"تعداد {len(configs)} کانفیگ از این لینک پیدا شد.")
        return configs
        
    except requests.exceptions.RequestException as e:
        print(f"خطا در دریافت لینک {url}: {e}")
        return []
    except Exception as e:
        print(f"خطایی ناشناخته در پردازش لینک {url}: {e}")
        return []

def main():
    """تابع اصلی برنامه"""
    if not JAVID_NAMAN:
        print("لیست نام‌ها خالی است. برنامه متوقف شد.")
        return

    shuffled_names = JAVID_NAMAN[:]
    random.shuffle(shuffled_names)
    print("\nترتیب نام‌ها به صورت تصادفی برای این اجرا مشخص شد.")
    
    all_configs: List[str] = []
    for link in SUB_LINKS:
        all_configs.extend(get_configs_from_sub(link))
    
    print(f"\nمجموعاً {len(all_configs)} کانفیگ (با احتساب موارد تکراری) پیدا شد.")
    
    unique_configs: Set[str] = set(all_configs)
    print(f"تعداد {len(unique_configs)} کانفیگ منحصر به فرد یافت شد.")
    
    if not unique_configs:
        print("هیچ کانفیگی برای پردازش وجود ندارد. خروج.")
        return

    renamed_configs: List[str] = []
    sorted_unique_configs = sorted(list(unique_configs))
    
    for i, config in enumerate(sorted_unique_configs):
        base_link = config.split('#')[0]
        
        name_index = i % len(shuffled_names)
        javid_nam = shuffled_names[name_index]
        
        new_name = f"POORIA {javid_nam}"
        
        encoded_name = urllib.parse.quote(new_name)
        new_link = f"{base_link}#{encoded_name}"
        renamed_configs.append(new_link)
        
    final_config_str = "\n".join(renamed_configs)
    final_b64_config = base64.b64encode(final_config_str.encode('utf-8')).decode('utf-8')
    
    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(final_b64_config)
        print(f"\nیادشان گرامی. {len(renamed_configs)} کانفیگ با نام جاویدنامان در فایل '{OUTPUT_FILENAME}' ذخیره شد.")
    except IOError as e:
        print(f"خطا در نوشتن فایل خروجی: {e}")

if __name__ == "__main__":
    main()

