import os

filepath = r"C:\Users\mkaib\.gemini\antigravity\scratch\youtube\.github\workflows\auth_setup.yml"

with open(filepath, "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Lines that don't start with space and aren't completely empty
    if line.strip() != "" and not line.startswith(" "):
        if not line.startswith("name:") and not line.startswith("on:") and not line.startswith("jobs:"):
            if not line.startswith("\"@"):
                new_lines.append("          " + line)
                continue
            
    # Fix the closing "@ tag
    if line.startswith("\"@") and "Out-File" in "".join(lines[i:i+3]):
        new_lines.append("          \"@\n")
        var_name = lines[i-1].strip().split(".")[0]
        if "sb.get_current_url" in lines[i-1] or "Successfully loaded" in lines[i-1]:
            # Guessing variable name based on surrounding context isn't safe, let's just use regex replace statically:
            pass
        continue

    new_lines.append(line)

# Wait, the above logic is brittle. I'll just write a static string replacement for the exact lines.
with open(filepath, "r") as f:
    content = f.read()

# Replace block 1
block1_old = """          $pyTestGeminiProfile = @"
import os, time, zipfile, shutil
from seleniumbase import SB
profile_zip = r'H:\\Colab_AutoVideoCreator\\engine_auth\\gemini_profile.zip'
extract_dir = r'C:\\temp_profile'
print('[*] Extracting profile from:', profile_zip)
if not os.path.exists(profile_zip):
    print('[!] Profile ZIP not found!')
    exit(1)
if os.path.exists(extract_dir):
    shutil.rmtree(extract_dir)
os.makedirs(extract_dir)
with zipfile.ZipFile(profile_zip, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
print('[*] Launching browser with extracted profile...')
with SB(uc=True, headless=False, user_data_dir=extract_dir) as sb:
    sb.open('https://gemini.google.com/app')
    time.sleep(10)
    if 'Sign in' in sb.get_page_source() or sb.get_current_url().startswith('https://accounts.google.com'):
        print('\\n[!] PROFILE TEST FAILED: Browser is asking for login.\\n')
    else:
        print('\\n[+] PROFILE TEST PASSED: Successfully loaded Gemini chat!\\n')
"@
          Out-File -FilePath "C:\\Users\\Public\\Desktop\\test_gemini_profile.py" -InputObject $pyTestGeminiProfile -Encoding utf8"""

block1_new = """          $pyTestGeminiProfile = @"
          import os, time, zipfile, shutil
          from seleniumbase import SB
          profile_zip = r'H:\\Colab_AutoVideoCreator\\engine_auth\\gemini_profile.zip'
          extract_dir = r'C:\\temp_profile'
          print('[*] Extracting profile from:', profile_zip)
          if not os.path.exists(profile_zip):
              print('[!] Profile ZIP not found!')
              exit(1)
          if os.path.exists(extract_dir):
              shutil.rmtree(extract_dir)
          os.makedirs(extract_dir)
          with zipfile.ZipFile(profile_zip, 'r') as zip_ref:
              zip_ref.extractall(extract_dir)
          print('[*] Launching browser with extracted profile...')
          with SB(uc=True, headless=False, user_data_dir=extract_dir) as sb:
              sb.open('https://gemini.google.com/app')
              time.sleep(10)
              if 'Sign in' in sb.get_page_source() or sb.get_current_url().startswith('https://accounts.google.com'):
                  print('\\n[!] PROFILE TEST FAILED: Browser is asking for login.\\n')
              else:
                  print('\\n[+] PROFILE TEST PASSED: Successfully loaded Gemini chat!\\n')
          "@
          $pyTestGeminiProfile = $pyTestGeminiProfile -replace '(?m)^ {10}', ''
          Out-File -FilePath "C:\\Users\\Public\\Desktop\\test_gemini_profile.py" -InputObject $pyTestGeminiProfile -Encoding utf8"""

content = content.replace(block1_old, block1_new)

# Replace block 2
block2_old = """          $pyTestGeminiCookies = @"
import os, time, json
from seleniumbase import SB
cookies_file = r'H:\\Colab_AutoVideoCreator\\engine_auth\\gemini_cookies.json'
print('[*] Loading cookies from:', cookies_file)
if not os.path.exists(cookies_file):
    print('[!] Cookies file not found!')
    exit(1)
with open(cookies_file, 'r') as f:
    cookies = json.load(f)
print('[*] Launching browser and injecting cookies...')
with SB(uc=True, headless=False) as sb:
    sb.open('https://google.com')
    time.sleep(2)
    for c in cookies:
        vc = {k: v for k, v in c.items() if k in ['name', 'value', 'domain', 'path', 'httpOnly', 'secure']}
        try:
            sb.driver.add_cookie(vc)
        except:
            pass
    print('[*] Cookies injected. Navigating to Gemini...')
    sb.open('https://gemini.google.com/app')
    time.sleep(10)
    if 'Sign in' in sb.get_page_source() or sb.get_current_url().startswith('https://accounts.google.com'):
        print('\\n[!] COOKIES TEST FAILED: Browser is asking for login.\\n')
    else:
        print('\\n[+] COOKIES TEST PASSED: Successfully loaded Gemini chat!\\n')
"@
          Out-File -FilePath "C:\\Users\\Public\\Desktop\\test_gemini_cookies.py" -InputObject $pyTestGeminiCookies -Encoding utf8"""

block2_new = """          $pyTestGeminiCookies = @"
          import os, time, json
          from seleniumbase import SB
          cookies_file = r'H:\\Colab_AutoVideoCreator\\engine_auth\\gemini_cookies.json'
          print('[*] Loading cookies from:', cookies_file)
          if not os.path.exists(cookies_file):
              print('[!] Cookies file not found!')
              exit(1)
          with open(cookies_file, 'r') as f:
              cookies = json.load(f)
          print('[*] Launching browser and injecting cookies...')
          with SB(uc=True, headless=False) as sb:
              sb.open('https://google.com')
              time.sleep(2)
              for c in cookies:
                  vc = {k: v for k, v in c.items() if k in ['name', 'value', 'domain', 'path', 'httpOnly', 'secure']}
                  try:
                      sb.driver.add_cookie(vc)
                  except:
                      pass
              print('[*] Cookies injected. Navigating to Gemini...')
              sb.open('https://gemini.google.com/app')
              time.sleep(10)
              if 'Sign in' in sb.get_page_source() or sb.get_current_url().startswith('https://accounts.google.com'):
                  print('\\n[!] COOKIES TEST FAILED: Browser is asking for login.\\n')
              else:
                  print('\\n[+] COOKIES TEST PASSED: Successfully loaded Gemini chat!\\n')
          "@
          $pyTestGeminiCookies = $pyTestGeminiCookies -replace '(?m)^ {10}', ''
          Out-File -FilePath "C:\\Users\\Public\\Desktop\\test_gemini_cookies.py" -InputObject $pyTestGeminiCookies -Encoding utf8"""

content = content.replace(block2_old, block2_new)

# Replace block 3
block3_old = """          $pyTestChatGptCookies = @"
import os, time, json
from seleniumbase import SB
cookies_file = r'H:\\Colab_AutoVideoCreator\\engine_auth\\chatgpt_cookies.json'
print('[*] Loading cookies from:', cookies_file)
if not os.path.exists(cookies_file):
    print('[!] Cookies file not found!')
    exit(1)
with open(cookies_file, 'r') as f:
    cookies = json.load(f)
print('[*] Launching browser and injecting cookies...')
with SB(uc=True, headless=False) as sb:
    sb.open('https://chatgpt.com')
    time.sleep(2)
    for c in cookies:
        vc = {k: v for k, v in c.items() if k in ['name', 'value', 'domain', 'path', 'httpOnly', 'secure']}
        try:
            sb.driver.add_cookie(vc)
        except:
            pass
    print('[*] Cookies injected. Refreshing ChatGPT...')
    sb.open('https://chatgpt.com')
    time.sleep(10)
    page_text = sb.get_page_source()
    if 'Log in' in page_text or 'Sign up' in page_text or sb.get_current_url() == 'https://chatgpt.com/auth/login':
        print('\\n[!] COOKIES TEST FAILED: Browser is asking for login.\\n')
    else:
        print('\\n[+] COOKIES TEST PASSED: Successfully loaded ChatGPT interface!\\n')
"@
          Out-File -FilePath "C:\\Users\\Public\\Desktop\\test_chatgpt_cookies.py" -InputObject $pyTestChatGptCookies -Encoding utf8"""

block3_new = """          $pyTestChatGptCookies = @"
          import os, time, json
          from seleniumbase import SB
          cookies_file = r'H:\\Colab_AutoVideoCreator\\engine_auth\\chatgpt_cookies.json'
          print('[*] Loading cookies from:', cookies_file)
          if not os.path.exists(cookies_file):
              print('[!] Cookies file not found!')
              exit(1)
          with open(cookies_file, 'r') as f:
              cookies = json.load(f)
          print('[*] Launching browser and injecting cookies...')
          with SB(uc=True, headless=False) as sb:
              sb.open('https://chatgpt.com')
              time.sleep(2)
              for c in cookies:
                  vc = {k: v for k, v in c.items() if k in ['name', 'value', 'domain', 'path', 'httpOnly', 'secure']}
                  try:
                      sb.driver.add_cookie(vc)
                  except:
                      pass
              print('[*] Cookies injected. Refreshing ChatGPT...')
              sb.open('https://chatgpt.com')
              time.sleep(10)
              page_text = sb.get_page_source()
              if 'Log in' in page_text or 'Sign up' in page_text or sb.get_current_url() == 'https://chatgpt.com/auth/login':
                  print('\\n[!] COOKIES TEST FAILED: Browser is asking for login.\\n')
              else:
                  print('\\n[+] COOKIES TEST PASSED: Successfully loaded ChatGPT interface!\\n')
          "@
          $pyTestChatGptCookies = $pyTestChatGptCookies -replace '(?m)^ {10}', ''
          Out-File -FilePath "C:\\Users\\Public\\Desktop\\test_chatgpt_cookies.py" -InputObject $pyTestChatGptCookies -Encoding utf8"""

content = content.replace(block3_old, block3_new)

with open(filepath, "w") as f:
    f.write(content)
