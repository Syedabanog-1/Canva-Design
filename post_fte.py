"""
LinkedIn auto-post — Digital FTE: 10 Reasons AI Employees Win
Uses pyautogui + pywinauto (same approach that worked in auto_post_final.py)
"""
import pyautogui
import pyperclip
import time
import win32gui
import win32con

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

IMAGE_PATH = r"D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment\fte_graphic.png"
SDIR = r"D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment"

POST_TEXT = """میں نے پچھلے مہینے اپنا پہلا AI ملازم رکھا۔
$1,200/ماہ پر — 168 گھنٹے فی ہفتہ کام۔
میرا بہترین انسانی ملازم $5,000/ماہ لیتا ہے — اور صرف 40 گھنٹے دیتا ہے۔

یہ حساب تکلیف دہ ہے۔ Agent Factory کے یہ 10 نکات نے میری سوچ بدل دی:

1/ 168 گھنٹے بمقابلہ 40
Digital FTE کبھی نہیں سوتا، چھٹی نہیں لیتا، تھکتا نہیں۔ ہفتے میں 4.2 گنا زیادہ آؤٹ پٹ — بغیر اوور ٹائم کے۔

2/ $500–2K بمقابلہ $4K–8K+/ماہ
اپنا بہترین عمل ایک بار AI agent میں ڈھالیں۔ وہ بغیر رکے چلتا رہے گا۔

3/ سالانہ 9,000 گھنٹے بمقابلہ 2,000
ایک Digital FTE کا ایک سال = 4.5 انسانی سال کا کام۔ startup کی رفتار سے۔

4/ 99%+ consistency بمقابلہ 85–95%
انسانوں کے اچھے اور برے دن ہوتے ہیں۔ Digital FTE رات 3 بجے بھی وہی معیار دیتا ہے جو صبح 9 بجے۔

5/ 10-80-10 کا اصول
انسان: intent (10%) → AI: execute (80%) → انسان: verify (10%)۔
آپ replace نہیں ہوتے — promote ہوتے ہیں۔

6/ فوری cloning بمقابلہ مہینوں کی hiring
کوئی workflow کام کر رہا ہے؟ منٹوں میں 10 agents بنائیں — سہ ماہیوں میں نہیں۔

7/ Spec-Driven Development
ایک بار لکھیں، ہمیشہ کے لیے deploy کریں۔ آپ کی expertise ایک recipe بنتی ہے — جو آپ کے سوتے وقت چلتی ہے۔

8/ صفر overhead اخراجات
نہ benefits، نہ HR، نہ sick leave، نہ performance reviews۔ صرف outcomes۔

9/ SaaS سے Agent Era تک
Software نے seats بیچیں۔ AI outcomes بیچتا ہے۔
کل کا business model آج آ چکا ہے۔

10/ پانچ Maturity Levels
Level 1: AI Awareness (10-20% فائدہ)۔
Level 5: AI-First Enterprise (10x productivity)۔
Digital FTEs وہ پل ہیں جو آپ کو اوپر لے جاتے ہیں۔

جو کمپنیاں levels 3-5 پہلے سمجھ لیں گی — وہ صرف تیز نہیں چلیں گی۔
وہ ایک مختلف category میں ہوں گی۔

آپ کی organization ابھی کس level پر ہے؟

Sir Anas کے ساتھ سیکھ رہی ہوں @GIAIC | Panaversity Agent Factory

#AgentFactory #DigitalFTE #AIEmployee #FutureOfWork #GIAIC #Panaversity #AIAgents #LearnInPublic #10x #AIFirst"""


def log(msg):
    print(f"[FTE-POST] {msg}", flush=True)


def ss(name):
    path = f"{SDIR}\\{name}.png"
    pyautogui.screenshot(path)
    log(f"  Screenshot: {name}.png")


def focus_chrome():
    target = None
    def cb(hwnd, _):
        nonlocal target
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if 'LinkedIn' in t or 'Chrome' in t:
                target = hwnd
    win32gui.EnumWindows(cb, None)
    if target:
        win32gui.ShowWindow(target, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(target)
        time.sleep(1.5)


def find_button_center(btn_name):
    try:
        from pywinauto import Application
        app = Application(backend='uia').connect(title_re='.*LinkedIn.*')
        win = app.top_window()
        btn = win.child_window(title=btn_name, control_type='Button')
        r = btn.rectangle()
        return ((r.left + r.right) // 2, (r.top + r.bottom) // 2)
    except Exception as e:
        log(f"  UIA find '{btn_name}' failed: {e}")
        return None


def main():
    log("=== LinkedIn FTE Post ===")

    focus_chrome()
    time.sleep(1)

    log("Step 1: Navigate to LinkedIn feed...")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite('linkedin.com/feed/', interval=0.04)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.hotkey('ctrl', 'Home')
    time.sleep(1)
    ss("fte0_feed")

    log("Step 2: Clicking 'Start a post' at (772, 198)...")
    pyautogui.moveTo(772, 198, duration=0.4)
    time.sleep(0.3)
    pyautogui.click(772, 198)
    time.sleep(3)
    ss("fte1_modal")

    log("Step 3: Finding text area in modal...")
    text_area_coords = None
    try:
        from pywinauto import Application
        app = Application(backend='uia').connect(title_re='.*LinkedIn.*')
        win = app.top_window()
        for title in ['Text editor for creating content', 'Start a post', 'What do you want to talk about?']:
            try:
                elem = win.child_window(title=title, control_type='Edit')
                r = elem.rectangle()
                text_area_coords = ((r.left + r.right) // 2, (r.top + r.bottom) // 2)
                log(f"  Found text area '{title}' at {text_area_coords}")
                break
            except Exception:
                pass
        if not text_area_coords:
            try:
                elem = win.child_window(control_type='Document')
                r = elem.rectangle()
                text_area_coords = ((r.left + r.right) // 2, (r.top + r.bottom) // 2)
                log(f"  Found Document control at {text_area_coords}")
            except Exception:
                pass
    except Exception as e:
        log(f"  UIA text area search failed: {e}")

    if not text_area_coords:
        text_area_coords = (772, 380)
        log(f"  Using fallback text area coords: {text_area_coords}")

    log(f"Step 4: Clicking text area at {text_area_coords}...")
    pyautogui.click(text_area_coords[0], text_area_coords[1])
    time.sleep(0.6)

    log("Step 5: Pasting post text...")
    pyperclip.copy(POST_TEXT)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    ss("fte2_text")

    log("Step 6: Finding photo/media button...")
    photo_coords = None
    try:
        from pywinauto import Application
        app = Application(backend='uia').connect(title_re='.*LinkedIn.*')
        win = app.top_window()
        for name in ['Add media', 'Add a photo', 'Photo', 'Media', 'Add photos/videos']:
            try:
                elem = win.child_window(title=name, control_type='Button')
                r = elem.rectangle()
                photo_coords = ((r.left + r.right) // 2, (r.top + r.bottom) // 2)
                log(f"  Found photo button '{name}' at {photo_coords}")
                break
            except Exception:
                pass
    except Exception as e:
        log(f"  UIA photo button search failed: {e}")

    if not photo_coords:
        photo_coords = (556, 660)
        log(f"  Using fallback photo coords: {photo_coords}")

    log(f"Step 7: Clicking photo button at {photo_coords}...")
    pyautogui.moveTo(photo_coords[0], photo_coords[1], duration=0.4)
    time.sleep(0.3)
    ss("fte3_before_photo")
    pyautogui.click(photo_coords[0], photo_coords[1])
    time.sleep(3)
    ss("fte4_after_photo")

    log("Step 8: Handling file dialog — pasting image path...")
    pyperclip.copy(IMAGE_PATH)
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    ss("fte5_file_path")
    pyautogui.press('enter')
    time.sleep(5)
    ss("fte6_image_loaded")

    log("Step 9: Looking for Next button...")
    next_coords = find_button_center('Next')
    if next_coords:
        log(f"  Clicking Next at {next_coords}")
        pyautogui.click(next_coords[0], next_coords[1])
        time.sleep(2)
    else:
        log("  No Next button found, trying (1150, 185)...")
        pyautogui.click(1150, 185)
        time.sleep(2)
    ss("fte7_after_next")

    log("Step 10: Looking for Post button...")
    post_coords = find_button_center('Post')
    if post_coords:
        log(f"  Clicking Post at {post_coords}")
        pyautogui.click(post_coords[0], post_coords[1])
    else:
        log("  No Post button found, trying (900, 655)...")
        pyautogui.click(900, 655)

    time.sleep(8)
    ss("fte8_final")
    log("=== DONE! Check fte8_final.png ===")


if __name__ == "__main__":
    log("Starting in 3 seconds — switch to Chrome!")
    time.sleep(3)
    main()
