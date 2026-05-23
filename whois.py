import requests
import socket
import whois
from datetime import datetime

def get_ip_from_domain(domain):
    """دریافت IP از دامنه"""
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return None

def get_ip_info(ip):
    """دریافت اطلاعات IP از API های مختلف"""
    
    # اطلاعات اولیه از ip-api.com (بدون نیاز به API key)
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'success':
            info = {
                'IP': ip,
                'کشور': data.get('country', 'نامشخص'),
                'کد کشور': data.get('countryCode', 'نامشخص'),
                'منطقه': data.get('regionName', 'نامشخص'),
                'شهر': data.get('city', 'نامشخص'),
                'عرض جغرافیایی': data.get('lat', 'نامشخص'),
                'طول جغرافیایی': data.get('lon', 'نامشخص'),
                'ISP': data.get('isp', 'نامشخص'),
                'سازمان': data.get('org', 'نامشخص'),
                'AS': data.get('as', 'نامشخص'),
                'نوع IP': data.get('mobile', 'نامشخص'),
                'پروکسی': data.get('proxy', 'نامشخص'),
                'هاستینگ': data.get('hosting', 'نامشخص')
            }
            return info
        else:
            return None
    except Exception as e:
        print(f"خطا در دریافت اطلاعات از ip-api: {e}")
        return None

def get_domain_info(domain):
    """دریافت اطلاعات دامنه"""
    try:
        domain_info = whois.whois(domain)
        info = {
            'دامنه': domain,
            'ثبت‌کننده': domain_info.registrar if domain_info.registrar else 'نامشخص',
            'تاریخ ثبت': domain_info.creation_date if domain_info.creation_date else 'نامشخص',
            'تاریخ انقضا': domain_info.expiration_date if domain_info.expiration_date else 'نامشخص',
            'آخرین بروزرسانی': domain_info.updated_date if domain_info.updated_date else 'نامشخص',
            'نام سرورها': domain_info.name_servers if domain_info.name_servers else 'نامشخص'
        }
        return info
    except Exception as e:
        print(f"خطا در دریافت اطلاعات دامنه: {e}")
        return None

def check_datacenter(ip):
    """بررسی دیتاسنتر بودن IP"""
    try:
        # استفاده از API ipinfo.io برای اطلاعات دیتاسنتر
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url)
        data = response.json()
        
        # بررسی دیتاسنتر
        is_datacenter = False
        datacenter_name = "نامشخص"
        
        # بررسی hostname یا org برای تشخیص دیتاسنتر
        org = data.get('org', '').lower()
        hostname = data.get('hostname', '').lower()
        
        datacenter_keywords = ['datacenter', 'data center', 'cloud', 'hosting', 'amazon', 
                               'google', 'microsoft', 'digitalocean', 'ovh', 'hetzner', 
                               'linode', 'vultr', 'aws', 'azure', 'gcp']
        
        for keyword in datacenter_keywords:
            if keyword in org or keyword in hostname:
                is_datacenter = True
                datacenter_name = data.get('org', 'Unknown')
                break
        
        return {
            'is_datacenter': is_datacenter,
            'datacenter_name': datacenter_name if is_datacenter else 'Not a datacenter IP',
            'hostname': data.get('hostname', 'نامشخص'),
            'organization': data.get('org', 'نامشخص')
        }
    except:
        return {
            'is_datacenter': False,
            'datacenter_name': 'Unable to determine',
            'hostname': 'نامشخص',
            'organization': 'نامشخص'
        }

def print_ip_info(info):
    """چاپ اطلاعات IP با فرمت مناسب"""
    print("\n" + "="*50)
    print("📡 اطلاعات IP:")
    print("="*50)
    for key, value in info.items():
        if value != 'نامشخص':
            print(f"{key}: {value}")
    print("="*50)

def print_domain_info(info):
    """چاپ اطلاعات دامنه با فرمت مناسب"""
    if info:
        print("\n" + "="*50)
        print("🌐 اطلاعات دامنه:")
        print("="*50)
        for key, value in info.items():
            if value != 'نامشخص':
                if isinstance(value, list):
                    print(f"{key}: {', '.join(str(v) for v in value)}")
                else:
                    print(f"{key}: {value}")
        print("="*50)

def print_datacenter_info(info):
    """چاپ اطلاعات دیتاسنتر"""
    print("\n" + "="*50)
    print("🏢 اطلاعات دیتاسنتر:")
    print("="*50)
    print(f"آیا IP مربوط به دیتاسنتر است؟: {'بله' if info['is_datacenter'] else 'خیر'}")
    print(f"نام دیتاسنتر/سازمان: {info['datacenter_name']}")
    print(f"Hostname: {info['hostname']}")
    print(f"سازمان: {info['organization']}")
    print("="*50)

def main():
    print("🔍 ابزار جستجوی اطلاعات IP و دامنه")
    print("-" * 40)
    
    user_input = input("لطفا IP یا دامنه مورد نظر را وارد کنید: ").strip()
    
    # بررسی اینکه ورودی IP است یا دامنه
    is_ip = False
    try:
        socket.inet_aton(user_input)
        is_ip = True
    except:
        is_ip = False
    
    if is_ip:
        # اگر ورودی IP بود
        ip = user_input
        print(f"\n🔍 در حال جستجوی اطلاعات برای IP: {ip}")
        
        # دریافت اطلاعات IP
        ip_info = get_ip_info(ip)
        if ip_info:
            print_ip_info(ip_info)
        else:
            print("❌ خطا در دریافت اطلاعات IP")
        
        # بررسی دیتاسنتر
        datacenter_info = check_datacenter(ip)
        print_datacenter_info(datacenter_info)
        
    else:
        # اگر ورودی دامنه بود
        domain = user_input
        print(f"\n🔍 در حال جستجوی اطلاعات برای دامنه: {domain}")
        
        # دریافت IP از دامنه
        ip = get_ip_from_domain(domain)
        if ip:
            print(f"📍 IP معادل: {ip}")
            
            # دریافت اطلاعات IP
            ip_info = get_ip_info(ip)
            if ip_info:
                print_ip_info(ip_info)
            
            # بررسی دیتاسنتر
            datacenter_info = check_datacenter(ip)
            print_datacenter_info(datacenter_info)
        else:
            print("❌ خطا در دریافت IP دامنه")
        
        # دریافت اطلاعات دامنه
        domain_info = get_domain_info(domain)
        if domain_info:
            print_domain_info(domain_info)
        else:
            print("❌ خطا در دریافت اطلاعات دامنه")

if __name__ == "__main__":
    main()