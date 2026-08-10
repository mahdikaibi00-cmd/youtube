import base64
import os

profile_py = """import os, time, zipfile, shutil
from seleniumbase import SB

profile_zip = r'H:\\Colab_AutoVideoCreator\\gemini_profile.zip'
extract_dir = r'C:\\temp_profile'

print('[*] Extracting profile from:', profile_zip)
if not os.path.exists(profile_zip):
    print('[!] Profile ZIP not found!')
    exit(1)

if os.path.exists(extract_dir):
    try:
        shutil.rmtree(extract_dir)
    except:
        pass

os.makedirs(extract_dir, exist_ok=True)

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
"""

gemini_cookies_py = """import os, time, json
from seleniumbase import SB

cookies_file = r'H:\\Colab_AutoVideoCreator\\gemini_cookies.json'

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
        except Exception as e:
            pass
            
    print('[*] Cookies injected. Navigating to Gemini...')
    sb.open('https://gemini.google.com/app')
    time.sleep(10)
    
    if 'Sign in' in sb.get_page_source() or sb.get_current_url().startswith('https://accounts.google.com'):
        print('\\n[!] COOKIES TEST FAILED: Browser is asking for login.\\n')
    else:
        print('\\n[+] COOKIES TEST PASSED: Successfully loaded Gemini chat!\\n')
"""

chatgpt_cookies_py = """import os, time, json
from seleniumbase import SB

cookies_file = r'H:\\Colab_AutoVideoCreator\\chatgpt_cookies.json'

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
        except Exception as e:
            pass
            
    print('[*] Cookies injected. Refreshing ChatGPT...')
    sb.open('https://chatgpt.com')
    time.sleep(10)
    
    page_text = sb.get_page_source()
    if 'Log in' in page_text or 'Sign up' in page_text or sb.get_current_url() == 'https://chatgpt.com/auth/login':
        print('\\n[!] COOKIES TEST FAILED: Browser is asking for login.\\n')
    else:
        print('\\n[+] COOKIES TEST PASSED: Successfully loaded ChatGPT interface!\\n')
"""

def b64(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')

yml_content = f"""name: Cloud Auth Setup (Gemini & ChatGPT)

on:
  workflow_dispatch:

jobs:
  auth-setup:
    runs-on: windows-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install playwright playwright-stealth seleniumbase
          python -m playwright install chromium

      - name: Setup Ngrok RDP & Desktop Scripts
        run: |
          Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server'-name "fDenyTSConnections" -Value 0
          Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
          Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -name "UserAuthentication" -Value 1
          net user "Mahdi Kaibi" "${{{{ secrets.RDP_PASSWORD }}}}" /add
          net localgroup Administrators "Mahdi Kaibi" /add
          
          # 1. SETUP SCRIPTS
          \$batContentGemini = @"
          @echo off
          echo [*] Mounting Google Drive to H:\...
          start /b rclone --config `"C:\Users\Public\rclone.conf`" mount engine: H: --vfs-cache-mode writes --network-mode
          timeout /t 5
          echo [*] Installing dependencies for RDP user...
          python -m pip install seleniumbase
          echo [*] Launching Gemini Setup...
          python `"H:\Colab_AutoVideoCreator\setup_gemini_cookies.py`"
          pause
          "@
          Out-File -FilePath "C:\Users\Public\Desktop\1_Run_Gemini_Setup.bat" -InputObject \$batContentGemini -Encoding ascii
          
          \$batContentChatGPT = @"
          @echo off
          echo [*] Mounting Google Drive to H:\...
          start /b rclone --config `"C:\Users\Public\rclone.conf`" mount engine: H: --vfs-cache-mode writes --network-mode
          timeout /t 5
          echo [*] Installing dependencies for RDP user...
          python -m pip install seleniumbase
          echo [*] Launching ChatGPT Setup...
          python `"H:\Colab_AutoVideoCreator\setup_chatgpt_cookies.py`"
          pause
          "@
          Out-File -FilePath "C:\Users\Public\Desktop\2_Run_ChatGPT_Setup.bat" -InputObject \$batContentChatGPT -Encoding ascii
          
          # 2. PYTHON TEST SCRIPTS (BASE64 EXTRACTED TO AVOID INDENTATION ERRORS)
          \$b64Profile = "{b64(profile_py)}"
          [System.IO.File]::WriteAllBytes("C:\Users\Public\Desktop\test_gemini_profile.py", [System.Convert]::FromBase64String(\$b64Profile))
          
          \$b64GeminiCookies = "{b64(gemini_cookies_py)}"
          [System.IO.File]::WriteAllBytes("C:\Users\Public\Desktop\test_gemini_cookies.py", [System.Convert]::FromBase64String(\$b64GeminiCookies))
          
          \$b64ChatGptCookies = "{b64(chatgpt_cookies_py)}"
          [System.IO.File]::WriteAllBytes("C:\Users\Public\Desktop\test_chatgpt_cookies.py", [System.Convert]::FromBase64String(\$b64ChatGptCookies))
          
          # 3. TEST BAT FILES
          \$batTestGeminiProfile = @"
          @echo off
          echo [*] Mounting Google Drive to H:\...
          start /b rclone --config `"C:\Users\Public\rclone.conf`" mount engine: H: --vfs-cache-mode writes --network-mode
          timeout /t 5
          echo [*] Installing dependencies for RDP user...
          python -m pip install seleniumbase
          echo [*] Testing Gemini Profile Auth...
          python `"C:\Users\Public\Desktop\test_gemini_profile.py`"
          pause
          "@
          Out-File -FilePath "C:\Users\Public\Desktop\3_Test_Gemini_Profile.bat" -InputObject \$batTestGeminiProfile -Encoding ascii
          
          \$batTestGeminiCookies = @"
          @echo off
          echo [*] Mounting Google Drive to H:\...
          start /b rclone --config `"C:\Users\Public\rclone.conf`" mount engine: H: --vfs-cache-mode writes --network-mode
          timeout /t 5
          echo [*] Installing dependencies for RDP user...
          python -m pip install seleniumbase
          echo [*] Testing Gemini Cookies Auth...
          python `"C:\Users\Public\Desktop\test_gemini_cookies.py`"
          pause
          "@
          Out-File -FilePath "C:\Users\Public\Desktop\4_Test_Gemini_Cookies.bat" -InputObject \$batTestGeminiCookies -Encoding ascii

          \$batTestChatGptCookies = @"
          @echo off
          echo [*] Mounting Google Drive to H:\...
          start /b rclone --config `"C:\Users\Public\rclone.conf`" mount engine: H: --vfs-cache-mode writes --network-mode
          timeout /t 5
          echo [*] Installing dependencies for RDP user...
          python -m pip install seleniumbase
          echo [*] Testing ChatGPT Cookies Auth...
          python `"C:\Users\Public\Desktop\test_chatgpt_cookies.py`"
          pause
          "@
          Out-File -FilePath "C:\Users\Public\Desktop\5_Test_ChatGPT_Cookies.bat" -InputObject \$batTestChatGptCookies -Encoding ascii
        shell: powershell

      - name: Install Rclone & WinFsp
        run: choco install rclone winfsp -y
        shell: powershell

      - name: Configure and Mount Rclone to H:\\
        env:
          ENGINE_TOKEN_RAW: ${{{{ secrets.G_DRIVE_TOKEN_ENGINE }}}}
          CLIENT_ID: ${{{{ secrets.CLIENT_ID }}}}
          CLIENT_SECRET: ${{{{ secrets.CLIENT_SECRET }}}}
        run: |
          mkdir -p \$env:USERPROFILE\.config\\rclone
          \$E_ACCESS = (\$env:ENGINE_TOKEN_RAW | ConvertFrom-Json).token
          \$E_REFRESH = (\$env:ENGINE_TOKEN_RAW | ConvertFrom-Json).refresh_token
          \$E_EXPIRY = (\$env:ENGINE_TOKEN_RAW | ConvertFrom-Json).expiry
          \$ENGINE_TOKEN = "{{`"access_token`":`"\$E_ACCESS`",`"token_type`":`"Bearer`",`"refresh_token`":`"\$E_REFRESH`",`"expiry`":`"\$E_EXPIRY`"}}"
          
          @"
          [engine]
          type = drive
          client_id = \$env:CLIENT_ID
          client_secret = \$env:CLIENT_SECRET
          scope = drive
          token = \$ENGINE_TOKEN
          "@ | Out-File -FilePath "\$env:USERPROFILE\.config\\rclone\\rclone.conf" -Encoding utf8
          
          Copy-Item -Path "\$env:USERPROFILE\.config\\rclone\\rclone.conf" -Destination "C:\Users\Public\\rclone.conf" -Force
          
          Start-Process -FilePath "rclone" -ArgumentList "mount engine: H: --vfs-cache-mode writes --network-mode" -NoNewWindow
          Start-Sleep -Seconds 5
        shell: powershell

      - name: Download and Run Ngrok
        env:
          NGROK_AUTH_TOKEN: ${{{{ secrets.NGROK_TOKEN }}}}
        run: |
          choco install ngrok -y
          ngrok authtoken \$Env:NGROK_AUTH_TOKEN
          Start-Process -FilePath "ngrok" -ArgumentList "tcp 3389 --log=ngrok.log" -WindowStyle Hidden
          
          \$tunnelUrl = ""
          for (\$i = 0; \$i -lt 15; \$i++) {{
              Start-Sleep -Seconds 2
              try {{
                  \$resp = Invoke-RestMethod -Uri http://localhost:4040/api/tunnels -ErrorAction Stop
                  if (\$resp.tunnels.Count -gt 0) {{
                      \$tunnelUrl = \$resp.tunnels[0].public_url
                      break
                  }}
              }} catch {{
                  Write-Host "Waiting for ngrok to start..."
              }}
          }}
          
          if (\$tunnelUrl -eq "") {{
              Write-Host "Ngrok failed to start! Printing logs:"
              Get-Content ngrok.log -ErrorAction SilentlyContinue
              exit 1
          }}
          
          Write-Host "=========================================="
          Write-Host "Please connect to RDP using the address: \$tunnelUrl"
          Write-Host "=========================================="
        shell: powershell

      - name: Keep Runner Alive for Login
        run: Start-Sleep -Seconds 3600
        shell: powershell
"""

with open(r"C:\Users\mkaib\.gemini\antigravity\scratch\youtube\.github\workflows\auth_setup.yml", "w", encoding="utf-8") as f:
    f.write(yml_content)
