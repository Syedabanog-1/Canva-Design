"""
LinkedIn Auto-Post — Digital FTE (with image)
Fixes applied:
  - Close any lingering file dialogs before starting
  - Correct 'Start a post' coordinate (772, 198)
  - Detect only NEW file dialog (ignores pre-existing ones)
  - Escape any open post/preview panels first
"""
import pyautogui, pyperclip, time, win32gui, win32con

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.25

IMAGE_PATH = r"D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment\fte_graphic.png"
SDIR       = r"D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment"

POST_TEXT = """I hired my first AI employee last month.
$1,200/month. 168 hours a week. Zero sick days.
My best human hire costs $5,000/month and works 40 hours.

The math is uncomfortable. Here are 10 points from the Agent Factory that changed how I think:

1/ 168 hrs vs 40 hrs
A Digital FTE never sleeps, never vacations, never burns out. 4.2x the output in the same week - with zero overtime.

2/ $500-2K vs $4K-8K+/month
Build your best process into an AI agent once. It runs indefinitely at a fraction of the cost.

3/ 9,000 annual hours vs 2,000
One year of a Digital FTE equals 4.5 human-years of output. At startup speed.

4/ 99%+ consistency vs 85-95%
Humans have good days and bad days. A Digital FTE delivers the same quality at 3am that it does at 9am.

5/ The 10-80-10 Rule
Humans set intent (10%) -> AI executes (80%) -> Humans verify (10%).
You are not replaced. You are promoted.

6/ Instant cloning vs months of hiring
Found a workflow that works? Clone it across 10 agents in minutes, not quarters.

7/ Spec-Driven Development
Write your expertise once, deploy it forever. Your knowledge becomes a recipe that runs while you sleep.

8/ Zero overhead costs
No benefits. No HR. No sick leave. No performance reviews. Just outcomes.

9/ From SaaS to the Agent Era
Software sold you seats. AI sells you outcomes.
The business model of tomorrow is already here.

10/ Five Maturity Levels
Level 1 is AI Awareness (10-20% gains).
Level 5 is AI-First Enterprise (10x productivity).
Digital FTEs are the bridge that gets you there.

Companies that master levels 3-5 first will not just move faster.
They will operate in an entirely different category.

Which level is your organization at right now?

Learning with Sir Anas at GIAIC | Panaversity Agent Factory

#AgentFactory #DigitalFTE #AIEmployee #FutureOfWork #GIAIC #Panaversity #AIAgents #LearnInPublic #10x #AIFirst"""


# ── helpers ──────────────────────────────────────────────────────────────────

def log(msg):
    print(f"[POST] {msg}", flush=True)

def ss(name):
    pyautogui.screenshot(f"{SDIR}\\{name}.png")
    log(f"  Screenshot: {name}.png")

def all_dialog_hwnds():
    """Return set of hwnds of all currently open file-picker dialogs."""
    TITLES = ('open', 'select', 'choose', 'upload', 'file', 'openclaw')
    found = set()
    def cb(h, _):
        if win32gui.IsWindowVisible(h):
            t = win32gui.GetWindowText(h).lower()
            if any(k in t for k in TITLES):
                found.add(h)
    win32gui.EnumWindows(cb, None)
    return found

def close_old_dialogs():
    """Close any lingering file-picker / openclaw dialogs."""
    hwnds = all_dialog_hwnds()
    for h in hwnds:
        title = win32gui.GetWindowText(h)
        log(f"  Closing old dialog: '{title}'")
        win32gui.PostMessage(h, win32con.WM_CLOSE, 0, 0)
    if hwnds:
        time.sleep(1)

def focus_chrome():
    """Bring the LinkedIn Feed Chrome window to front."""
    best = None
    def cb(h, _):
        nonlocal best
        if not win32gui.IsWindowVisible(h):
            return
        t = win32gui.GetWindowText(h)
        if 'Feed' in t and 'LinkedIn' in t:
            best = h
        elif best is None and ('LinkedIn' in t or 'Chrome' in t):
            best = h
    win32gui.EnumWindows(cb, None)
    if best:
        win32gui.ShowWindow(best, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(best)
        time.sleep(1.5)

def wait_for_new_dialog(before_hwnds, timeout=10):
    """
    Wait until a file-picker dialog appears that was NOT in before_hwnds.
    Returns its hwnd or None on timeout.
    """
    TITLES = ('open', 'select', 'choose', 'upload', 'file')
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = set()
        def cb(h, _):
            if win32gui.IsWindowVisible(h):
                t = win32gui.GetWindowText(h).lower()
                if any(k in t for k in TITLES):
                    current.add(h)
        win32gui.EnumWindows(cb, None)
        new = current - before_hwnds
        if new:
            hwnd = next(iter(new))
            title = win32gui.GetWindowText(hwnd)
            log(f"  New file dialog: '{title}'")
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.6)
            return hwnd
        time.sleep(0.3)
    log("  WARNING: no new file dialog appeared")
    return None


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    log("=== LinkedIn Auto-Post with Image ===")

    # 0. Close old lingering dialogs + escape any open panels
    log("Step 0: Cleanup — close old dialogs & escape open panels")
    close_old_dialogs()
    focus_chrome()
    pyautogui.press('escape')
    time.sleep(0.5)
    pyautogui.press('escape')
    time.sleep(0.5)

    # 1. Navigate to LinkedIn feed
    log("Step 1: Navigate to linkedin.com/feed/")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write('linkedin.com/feed/', interval=0.03)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.hotkey('ctrl', 'Home')
    time.sleep(1.5)
    ss("p0_feed")

    # 2. Click "Start a post" — correct coordinate (772, 198)
    log("Step 2: Click 'Start a post' at (772, 198)")
    pyautogui.click(772, 198)
    time.sleep(3)
    ss("p1_modal")

    # 3. Click inside text area and paste post content
    log("Step 3: Paste post text")
    pyautogui.click(728, 320)
    time.sleep(0.6)
    pyperclip.copy(POST_TEXT)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    ss("p2_text")

    # 4. Snapshot existing dialogs, then click photo button
    log("Step 4: Click photo button (tracking pre-existing dialogs)")
    before = all_dialog_hwnds()
    pyautogui.click(585, 555)
    time.sleep(1.5)
    ss("p3_photo_btn")

    # 5. Wait for the NEW file dialog and paste image path into it
    log("Step 5: Waiting for new file dialog...")
    dlg = wait_for_new_dialog(before, timeout=10)

    pyperclip.copy(IMAGE_PATH)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.4)
    ss("p4_path_entered")
    pyautogui.press('enter')
    time.sleep(7)
    ss("p5_image_loaded")

    # 6. Bring Chrome back to focus (file dialog may have shifted focus)
    focus_chrome()
    time.sleep(1)

    # 7. Click "Next" if image-preview/caption screen appeared
    log("Step 6: Looking for Next button")
    for coord in [(1025, 185), (900, 185), (1025, 660), (900, 660)]:
        px = pyautogui.pixel(coord[0], coord[1])
        # blue button: R<100, G<150, B>150
        if px[0] < 100 and px[2] > 150:
            log(f"  Blue pixel at {coord} -> clicking Next")
            pyautogui.click(coord[0], coord[1])
            time.sleep(2.5)
            break
    ss("p6_after_next")

    # 8. Click Post button
    log("Step 7: Clicking Post button")
    for coord in [(1014, 622), (1014, 640), (900, 622)]:
        px = pyautogui.pixel(coord[0], coord[1])
        if px[0] < 100 and px[2] > 150:
            log(f"  Blue pixel at {coord} -> clicking Post")
            pyautogui.click(coord[0], coord[1])
            time.sleep(7)
            break
    ss("p7_posted")
    log("=== Done! Check p7_posted.png ===")


if __name__ == "__main__":
    log("Starting in 3 seconds — switch to Chrome now!")
    time.sleep(3)
    main()
