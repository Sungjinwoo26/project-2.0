#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Update Hindi translations with new strings
hi_translations = {
    "Returns Management": "रिटर्न प्रबंधन",
    "Process Return": "रिटर्न प्रक्रिया करें",
    "Recent Returns": "हालिया रिटर्न",
    "Last 50": "अंतिम 50",
    "Date & Time": "तारीख और समय",
    "Quantity Returned": "रिटर्न मात्रा",
    "No returns yet. Scan a product barcode to process a return.": "अभी तक कोई रिटर्न नहीं। रिटर्न प्रक्रिया करने के लिए उत्पाद बारकोड स्कैन करें।",
    "Stock Movement History": "स्टॉक आंदोलन इतिहास",
    "Complete audit trail of all inventory operations": "सभी इन्वेंटरी संचालन का पूर्ण ऑडिट ट्रेल",
    "Buy Operations": "खरीद संचालन",
    "Sell Operations": "विक्रय संचालन",
    "Return Operations": "रिटर्न संचालन",
    "Total Operations": "कुल संचालन",
    "All time": "सभी समय",
    "Product SKU": "उत्पाद SKU",
    "Operation": "संचालन",
    "Timestamp": "समय मुहर्त",
    "Uncategorized": "वर्गीकृत नहीं",
    "No stock movements recorded yet": "अभी तक कोई स्टॉक आंदोलन दर्ज नहीं किया गया",
    "Start by adding products and performing buy/sell/return operations": "उत्पाद जोड़कर और खरीद/विक्रय/रिटर्न संचालन करके शुरू करें",
    "POS Billing System": "POS बिलिंग सिस्टम",
    "Product Found": "उत्पाद मिला",
    "Enter Return Quantity": "रिटर्न मात्रा दर्ज करें",
    "Product Name:": "उत्पाद का नाम:",
    "SKU:": "SKU:",
    "Category:": "श्रेणी:",
    "Stock Action": "स्टॉक कार्य",
    "Recent Returns (Last 50)": "हालिया रिटर्न (अंतिम 50)",
}

mr_translations = {
    "Returns Management": "रिटर्न व्यवस्थापन",
    "Process Return": "रिटर्न प्रक्रिया करा",
    "Recent Returns": "अलीकडील रिटर्न",
    "Last 50": "शेवटचे 50",
    "Date & Time": "तारीख आणि वेळ",
    "Quantity Returned": "रिटर्न केलेली प्रमाण",
    "No returns yet. Scan a product barcode to process a return.": "अजून कोणतीही रिटर्न नाही. रिटर्न प्रक्रिया करण्यासाठी उत्पाद बारकोड स्कॅन करा.",
    "Stock Movement History": "स्टॉक मूव्हमेंट इतिहास",
    "Complete audit trail of all inventory operations": "सर्व इन्व्हेंटरी ऑपरेशन्सचा पूर्ण ऑडिट ट्रेल",
    "Buy Operations": "खरेदी ऑपरेशन्स",
    "Sell Operations": "विक्रय ऑपरेशन्स",
    "Return Operations": "रिटर्न ऑपरेशन्स",
    "Total Operations": "एकूण ऑपरेशन्स",
    "All time": "सर्व काळ",
    "Product SKU": "उत्पाद SKU",
    "Operation": "ऑपरेशन",
    "Timestamp": "वेळमोहर",
    "Uncategorized": "वर्गीकृत नाही",
    "No stock movements recorded yet": "अजून कोणती स्टॉक मूव्हमेंट रेकॉर्ड केली जात नाही",
    "Start by adding products and performing buy/sell/return operations": "उत्पादे जोडून आणि खरेदी/विक्रय/रिटर्न ऑपरेशन्स करून सुरू करा",
    "POS Billing System": "POS बिलिंग सिस्टम",
    "Product Found": "उत्पाद आढळले",
    "Enter Return Quantity": "रिटर्न प्रमाण प्रविष्ट करा",
    "Product Name:": "उत्पाद नाव:",
    "SKU:": "SKU:",
    "Category:": "श्रेणी:",
    "Stock Action": "स्टॉक कृती",
    "Recent Returns (Last 50)": "अलीकडील रिटर्न (शेवटचे 50)",
}

# Read and update Hindi translations
with open('translations/hi/LC_MESSAGES/messages.po', 'r', encoding='utf-8') as f:
    hi_content = f.read()

# Add new translations
for english, hindi in hi_translations.items():
    if f'msgid "{english}"' not in hi_content:
        hi_content = hi_content.rstrip() + f'\n\nmsgid "{english}"\nmsgstr "{hindi}"\n'

with open('translations/hi/LC_MESSAGES/messages.po', 'w', encoding='utf-8') as f:
    f.write(hi_content)

# Read and update Marathi translations
with open('translations/mr/LC_MESSAGES/messages.po', 'r', encoding='utf-8') as f:
    mr_content = f.read()

for english, marathi in mr_translations.items():
    if f'msgid "{english}"' not in mr_content:
        mr_content = mr_content.rstrip() + f'\n\nmsgid "{english}"\nmsgstr "{marathi}"\n'

with open('translations/mr/LC_MESSAGES/messages.po', 'w', encoding='utf-8') as f:
    f.write(mr_content)

print("Translations updated successfully!")
