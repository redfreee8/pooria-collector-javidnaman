import requests
import base64
import urllib.parse
from typing import List

# لیست لینک‌های سابسکریپشن شما
SUB_LINKS: List[str] = [
    "https://raw.githubusercontent.com/liketolivefree/kobabi/main/sub.txt",
    "https://lively-dream-c48b.mehdipost675.workers.dev",
    "https://leader.itn24.ir/v2ray_configs.txt?rand=12345",
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs.txt"
    "https://pooria.redorg1.ir/api/configs"
]

# نام فایل خروجی برای لینک ساب نهایی
OUTPUT_FILENAME: str = "POORIARED.txt"

def get_configs_from_sub(url: str) -> List[str]:
    """کانفیگ‌ها را از یک لینک سابسکریپشن دانلود و استخراج می‌کند."""
    try:
        print(f"در حال دریافت کانفیگ از: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        content = response.text
        decoded_content = ""
        
        try:
            decoded_content = base64.b64decode(content).decode('utf-8')
        except Exception:
            decoded_content = content
            print("محتوا Base64 نبود، به عنوان متن ساده پردازش شد.")

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
    """تابع اصلی برای جمع‌آوری و پردازش کانفیگ‌ها."""
    all_configs: List[str] = []
    
    for link in SUB_LINKS:
        all_configs.extend(get_configs_from_sub(link))
    
    print(f"\nمجموعاً {len(all_configs)} کانفیگ پیدا شد.")
    
    if not all_configs:
        print("هیچ کانفیگی برای پردازش وجود ندارد. خروج.")
        return

    renamed_configs: List[str] = []
    config_counter = 1
    
    for config in all_configs:
        base_link = config.split('#')[0]
        new_name = f"POORIA{config_counter}"
        encoded_name = urllib.parse.quote(new_name)
        new_link = f"{base_link}#{encoded_name}"
        renamed_configs.append(new_link)
        config_counter += 1
        
    final_config_str = "\n".join(renamed_configs)
    final_b64_config = base64.b64encode(final_config_str.encode('utf-8')).decode('utf-8')
    
    try:
        with open(OUTPUT_FILENAME, 'w') as f:
            f.write(final_b64_config)
        print(f"\nعملیات با موفقیت انجام شد. {len(renamed_configs)} کانفیگ در فایل '{OUTPUT_FILENAME}' ذخیره شد.")
    except IOError as e:
        print(f"خطا در نوشتن فایل خروجی: {e}")

if __name__ == "__main__":
    main()
