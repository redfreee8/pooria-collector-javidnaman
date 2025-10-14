import requests
import base64
import urllib.parse
import random
from typing import List, Set

# .لیستی از جاویدنامان خیزش زن، زندگی، آزادی. این لیست برای یادبود این عزیزان استفاده شده است
JAVID_NAMAN: List[str] = [
    "مهسا امینی", "نیکا شاکرمی", "سارینا اسماعیل‌زاده", "حدیث نجفی", "مینو مجیدی", "غزاله چلابی",
    "حنانه کیا", "محسن شکاری", "مجیدرضا رهنورد", "محمدمهدی کرمی", "سید محمد حسینی", "کیان پیرفلک",
    "خدیجه نقدی", "جواد حیدری", "فرشته احمدی", "رضا شهپرنیا", "عرفان زمانی", "یلدا آقافضلی",
    "ابوالفضل آدینه‌زاده", "اسرا پناهی", "محسن قیصری", "حمیدرضا روحی", "آیلار حقی", "سپهر مقصودی",
    "مهدی زارع اشکذری", "دنیا فرهادی", "آرشیا امامقلی‌زاده", "نگین عبدالمالکی", "مهرشاد شهیدی",
    "سارینا ساعدی", "کومار درافتاده", "بهناز افشاری", "آرمین صیادی", "امیرحسین شمس", "دانیال پابندی",
    "عرفان خزایی", "شیرین علیزاده", "فواد محمدی", "پویا شیدا", "مهرگان زحمتکش", "سیاوش محمودی",
    "پدرام آذرنوش", "علی روزبهانی", "مهدی حضرتی", "آرمان عمادی", "میلاد سعیدیان‌جو", "آیدا رستمی",
    "علی سیدی", "امیرمهدی فرخی‌پور", "سمانه نیک‌نام", "اسماعیل دزوار", "فریدون محمودی", "رضا لطفی",
    "زکریا خیال", "مومن زندکریمی", "صدرالدین لیتانی", "عاطفه نعامی", "آرنیکا قائم مقامی",
    "محمدحسن ترکمان", "مبین میرزایی", "جواد موسوی", "آیدین درویش", "متین نصرتی", "سینا نادری",
    "عرفان کاکایی", "اسماعیل مولودی", "آرین مریدی", "سینا ملایری", "امید حسنی", "آرین خوش‌گواریان",
    "روزبه خادمیان", "رضا کاظمی", "حمید گلی", "محمد حاجی‌رسول‌پور", "شمال خدیری‌پور", "ابراهیم میرزایی",
    "نسرین قادری", "آرمان اکبری", "پوریا احمدی", "محمدامین هاشمی", "امیر فلاحت‌دوست", "میلاد خوشکام",
    "هومن عبداللهی", "امیرمحمد رحیمی", "شورش نیکنام", "محمدحسین کمندلو", "محمود احمدی", "حمیدرضا براهویی",
    "محمد اقبال شهنوازی", "محمد ریگی", "عمر شهنوازی", "سامر هاشم‌زهی", "متین قنبرزهی", "جابر شیروزهی"
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

    # --- تغییر اصلی: تصادفی‌سازی در هر بار اجرا ---
    # دیگر از تاریخ استفاده نمی‌کنیم، بنابراین با هر بار اجرا ترتیب نام‌ها عوض می‌شود
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
        
        # انتخاب نام از لیست به هم ریخته شده
        name_index = i % len(shuffled_names)
        javid_nam = shuffled_names[name_index]
        
        # --- تغییر اصلی: اضافه کردن پیشوند POORIA ---
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

