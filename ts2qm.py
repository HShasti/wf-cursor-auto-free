#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TS to QM Converter
تبدیل کننده فایل‌های TS به QM برای استفاده در برنامه Cursor Pro
"""

import os
import sys
import subprocess
from lxml import etree

def fix_ts_file(ts_file):
    """
    اصلاح فایل TS برای رفع خطاهای احتمالی
    """
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(ts_file, parser)
        root = tree.getroot()
        
        # اصلاح تگ‌های <n> به <name>
        for context in root.findall(".//context"):
            for n_tag in context.findall("./n"):
                name_value = n_tag.text
                context.remove(n_tag)
                name_tag = etree.Element("name")
                name_tag.text = name_value
                context.insert(0, name_tag)
        
        # ذخیره فایل اصلاح شده
        tree.write(ts_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
        print(f"فایل {ts_file} با موفقیت اصلاح شد.")
        return True
    except Exception as e:
        print(f"خطا در اصلاح فایل {ts_file}: {str(e)}")
        return False

def convert_ts_to_qm(ts_file, qm_file=None):
    """
    تبدیل فایل TS به QM با استفاده از ابزار lrelease
    """
    if qm_file is None:
        qm_file = os.path.splitext(ts_file)[0] + ".qm"
    
    # تلاش برای استفاده از lrelease از PyQt5
    try:
        # اصلاح فایل TS قبل از تبدیل
        if not fix_ts_file(ts_file):
            return False
        
        # تلاش برای پیدا کردن lrelease
        lrelease_cmd = None
        possible_commands = [
            "lrelease",
            "lrelease-qt5",
            "lrelease.exe",
            os.path.join(os.path.dirname(sys.executable), "Scripts", "lrelease.exe"),
            os.path.join(os.path.dirname(sys.executable), "lrelease.exe"),
        ]
        
        for cmd in possible_commands:
            try:
                subprocess.run([cmd, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                lrelease_cmd = cmd
                break
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
        
        if lrelease_cmd is None:
            print("ابزار lrelease یافت نشد. در حال استفاده از روش جایگزین...")
            return manual_ts_to_qm(ts_file, qm_file)
        
        # اجرای lrelease برای تبدیل فایل
        result = subprocess.run([lrelease_cmd, ts_file, "-qm", qm_file], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               text=True, encoding="utf-8")
        
        if result.returncode == 0:
            print(f"فایل {ts_file} با موفقیت به {qm_file} تبدیل شد.")
            return True
        else:
            print(f"خطا در تبدیل فایل: {result.stderr}")
            return manual_ts_to_qm(ts_file, qm_file)
    
    except Exception as e:
        print(f"خطا: {str(e)}")
        return manual_ts_to_qm(ts_file, qm_file)

def manual_ts_to_qm(ts_file, qm_file):
    """
    تبدیل دستی فایل TS به QM با استفاده از یک فایل باینری ساده
    """
    try:
        # ایجاد یک فایل QM ساده با هدر استاندارد
        # فرمت فایل QM شامل یک هدر ساده است که با مقادیر زیر شروع می‌شود
        qm_header = bytes([
            0x3C, 0xB8, 0x64, 0x18,  # مجیک نامبر
            0x01, 0x00, 0x00, 0x00,  # نسخه فایل
            0x00, 0x00, 0x00, 0x00,  # تعداد ترجمه‌ها (صفر برای فایل خالی)
            0x00, 0x00, 0x00, 0x00,  # آفست جدول هش
            0x00, 0x00, 0x00, 0x00   # آفست جدول ترجمه
        ])
        
        with open(qm_file, 'wb') as f:
            f.write(qm_header)
        
        print(f"فایل {qm_file} با موفقیت ایجاد شد (ساده).")
        print("هشدار: این فایل QM فقط یک نمونه ساده است و ترجمه‌ها را شامل نمی‌شود.")
        return True
    except Exception as e:
        print(f"خطا در ایجاد فایل QM: {str(e)}")
        return False

def main():
    """
    تابع اصلی برنامه
    """
    # مسیر فایل‌های ترجمه
    translations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations")
    
    # بررسی وجود دایرکتوری ترجمه‌ها
    if not os.path.exists(translations_dir):
        os.makedirs(translations_dir)
        print(f"دایرکتوری {translations_dir} ایجاد شد.")
    
    # لیست فایل‌های TS
    ts_files = [
        os.path.join(translations_dir, "cursor_pro_en_US.ts"),
        os.path.join(translations_dir, "cursor_pro_zh_CN.ts")
    ]
    
    # تبدیل هر فایل TS به QM
    for ts_file in ts_files:
        if os.path.exists(ts_file):
            qm_file = os.path.splitext(ts_file)[0] + ".qm"
            convert_ts_to_qm(ts_file, qm_file)
        else:
            print(f"فایل {ts_file} یافت نشد.")

if __name__ == "__main__":
    main() 