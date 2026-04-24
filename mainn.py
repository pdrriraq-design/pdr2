import scapy.all as scapy
import socket

# قاعدة بيانات مصغرة لبصمات المصنعين (MAC OUI) الخاصة بكاميرات المراقبة
CAMERA_VENDORS = {
    "00:40:8c": "Axis Communications",
    "00:1a:07": "Hikvision Digital",
    "bc:ad:28": "Dahua Technology",
    "00:0b:3c": "Bosch Security",
    "00:02:d1": "Vivotek",
    # يمكن إضافة المزيد من البصمات هنا
}

def scan_network(ip_range):
    print(f"[*] جاري تفعيل الرادار الرقمي للنطاق: {ip_range}...")
    
    # إنشاء حزمة ARP طلب للاستعلام عن الأجهزة
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    # إرسال واستقبال الحزم
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    discovered_devices = []
    for element in answered_list:
        device_info = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc,
            "vendor": "Unknown Device"
        }
        
        # تحليل بصمة الـ MAC لاكتشاف الكاميرات
        mac_prefix = element[1].hwsrc[:8].lower()
        if mac_prefix in CAMERA_VENDORS:
            device_info["vendor"] = f"POTENTIAL CAMERA: {CAMERA_VENDORS[mac_prefix]}"
            
        discovered_devices.append(device_info)
    
    return discovered_devices

def display_results(devices):
    print("-" * 60)
    print("IP Address\t\tMAC Address\t\tDevice Type/Vendor")
    print("-" * 60)
    for device in devices:
        print(f"{device['ip']}\t\t{device['mac']}\t{device['vendor']}")

if __name__ == "__main__":
    # ملاحظة: استبدل النطاق بما يتوافق مع شبكتك للتجربة (مثلاً 192.168.1.1/24)
    target_range = "192.168.0.1/24" 
    results = scan_network(target_range)
    display_results(results)
