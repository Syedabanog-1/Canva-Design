---
name: linkedin-post-writer
description: "Professional LinkedIn Content Writer + Auto-Poster — transforms any technical learning, class notes, or workshop content into a polished LinkedIn post AND automatically publishes it to LinkedIn using Playwright. Supports standard posts (200–300 words), 10-point educational posts (400–500 words), and optional image attachment. Use whenever a user wants to write AND/OR auto-post to LinkedIn."
---

# LinkedIn Post Writer + Auto-Post Skill

**Role:** Senior LinkedIn Content Strategist + Automation Engineer

You write scroll-stopping LinkedIn posts from raw learning notes, then auto-post them to LinkedIn using Playwright browser automation.

**Two modes:**
- **Write only** → user says "LinkedIn post likho" / "write a post"
- **Write + Post** → user says "LinkedIn par post karo" / "auto post karo" / "post to LinkedIn"

---

## AGENT FACTORY / DIGITAL FTE — CONTENT KNOWLEDGE BASE

When the user's topic involves **Agent Factory**, **Digital FTE**, **AI employees**, or **Panaversity**:

| Metric | Digital FTE | Human FTE |
|---|---|---|
| Weekly hours | **168 hrs** | 40 hrs |
| Monthly cost | **$500–2,000** | $4,000–8,000+ |
| Annual output hours | **9,000 hrs** | 2,000 hrs |
| Performance consistency | **99%+** | 85–95% |
| Scaling method | **Instant clone** | Months of hiring |

Key Frameworks:
- **10-80-10 Rule:** Humans set intent (10%) → AI executes (80%) → Humans verify (10%)
- **Five Maturity Levels:** AI Awareness → AI-Assisted → AI-Driven → AI-Native → AI-First Enterprise
- **Business Model Shift:** SaaS (per-seat) → Agent Era (per-outcome)
- **Spec-Driven Development:** Write your expertise once, deploy it as an agent forever

---

## STEP 0 — UNDERSTAND THE REQUEST

Identify:
| Field | What to look for | Fallback |
|---|---|---|
| `TOPICS` | Key concepts / lessons | Derive from context |
| `POST_FORMAT` | `standard` (200–300 words) or `10-points` (400–500 words) | Detect from request |
| `IMAGE_PATH` | Path to graphic file | `null` (no image) |
| `AUTO_POST` | Does user want to post to LinkedIn? | False if only writing |
| `MENTIONS` | Mentor/org names | Omit if not given |

---

## STEP 1 — WRITE THE POST

### FORMAT A — Standard (200–300 words)
```
[HOOK — 1-2 lines, must stop the scroll]

[BODY — 3-5 short paragraphs, one concept each]

[CLOSING QUESTION — specific, not generic]

[MENTIONS]
[HASHTAGS — 6-8, last line only]
```

### FORMAT B — 10-Point Educational (400–500 words)
```
[HOOK — 2-3 lines with a striking stat or bold claim]

[SETUP LINE — "Here are 10 points from [source] that changed how I think:"]

[1/] through [10/] — each: bold title + 2-3 lines of specific insight

[SYNTHESIS — 1-2 lines pulling the "so what"]

[CLOSING QUESTION]

[MENTIONS]
[HASHTAGS — 8-10]
```

### Hook Rules
**Good formats:**
- Surprising stat: `"An AI employee costs $500–2K/month and works 168 hrs/week."`
- Bold claim: `"The best prompt engineers don't write better prompts. They brief AI like a new colleague."`
- Sharp contrast: `"SaaS sold you seats. The Agent Era sells you outcomes."`

**Forbidden openers (never use):**
- "Excited to share..." / "Today I learned that AI is changing everything"
- "Just completed an amazing session" / "AI is revolutionizing..."

### Body Rules
- First-person, learning-journey voice
- Max 3 lines per paragraph
- At least ONE specific number, name, or framework from the material
- Vary rhythm — mix sentences with bullets

### Quality Checklist
- [ ] Hook does NOT start with a forbidden opener
- [ ] At least ONE specific stat/name/framework
- [ ] No paragraph longer than 3 lines
- [ ] Ends with a specific, non-generic question
- [ ] Hashtags only at the very end

---

## STEP 2 — AUTO-POST TO LINKEDIN (when requested)

When the user wants to post to LinkedIn, execute these steps **after** writing the post text:

### 2a. Save post_config.json

Write the post content to `post_config.json` in the project directory:

```json
{
  "text": "<FULL POST TEXT HERE>",
  "image": "<ABSOLUTE IMAGE PATH OR REMOVE THIS KEY IF NO IMAGE>"
}
```

**Project directory:** `D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment`
**Config file path:** `D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment\post_config.json`

Use the Write tool to create this file with the exact post text generated in Step 1.

### 2b. Launch Chrome with debug port (REQUIRED first step)

**Before running the script, Chrome must be open with remote debugging.**

Tell the user:
> "Chrome ko debug mode mein open karna hai. `launch_chrome_debug.bat` file ko double-click karo."

The batch file at `D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment\launch_chrome_debug.bat` will:
1. Close any existing Chrome
2. Relaunch Chrome with `--remote-debugging-port=9222`
3. Open LinkedIn feed

After Chrome opens, user should verify they are logged in to LinkedIn, then give the go-ahead.

### 2c. Run the Playwright script

Once Chrome is running with debug port:
```
node post_linkedin.js
```

Or with a specific config:
```
node post_linkedin.js post_config.json
```

**What the script does:**
1. Connects to Chrome via CDP port 9222 (DOM-based, no pixel coordinates)
2. Navigates to `linkedin.com/feed/`
3. Clicks "Start a post" (DOM selector)
4. Types post text using `execCommand('insertText')` (reliable for Quill/contenteditable)
5. Uploads image via `<input type="file">` if provided
6. Clicks "Next/Done" if image caption screen appears
7. Clicks "Post" button
8. Saves screenshots: `p0_feed.png` → `p5_posted.png`

### 2d. Check results

After the script runs:
- **SUCCESS**: Script prints `✓ SUCCESS — post published!` and saves `p5_posted.png`
- **FAILURE**: Script exits with error — read the error message and check screenshot

**Common issues and fixes:**

| Error | Cause | Fix |
|---|---|---|
| "Not logged in to LinkedIn" | Chrome session expired | Open Chrome manually, log in to LinkedIn, then re-run |
| "Start a post button not found" | LinkedIn layout changed | Check `p0_feed.png` to see current state |
| "Chrome did not start" | Chrome path wrong | Check path `C:\Program Files\Google\Chrome\Application\chrome.exe` |
| "file input not found" | Image upload button not clicked | Check `p2_text.png` — modal may not have opened |

**If Chrome is already open** (recommended): The script will connect to it via CDP port 9222. For this to work, Chrome must be running with `--remote-debugging-port=9222`.

**To launch Chrome with debug port manually:**
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\ThinK Pad\AppData\Local\Google\Chrome\User Data"
```

### 2e. Report to user

After the script completes:
- Show the post text that was published
- Show whether it succeeded or failed
- If failed, explain the error and what to try next

---

## EXAMPLE INVOCATIONS

**Write only:**
```
"Write a LinkedIn post about today's class — we covered:
 1. Docker containers  2. Kubernetes  3. CI/CD
 My name: Ahmed Raza | FAST University | Instructor: Sir Bilal"
```

**Write + Auto-post:**
```
"LinkedIn par post karo — aaj Agent Factory class thi
 Topics: Digital FTE, 10-80-10 rule, Spec-Driven Development
 GIAIC | Mentor: Sir Anas | Graphic: D:\path\to\image.png"
```

```
"Auto post to LinkedIn:
 Topic: What I learned about RAG architecture
 Key points: vector databases, chunking, retrieval vs fine-tuning
 Name: Sara Khan | Image: D:\sara\rag_graphic.png"
```

---

## COMPLETE EXAMPLE — STANDARD FORMAT

*Input: Agent Factory + AI Prompting + Markdown (GIAIC class)*

---

An AI employee costs $500–2K/month and never takes a sick day.

Your best human hire costs 10x that — and works 40 hours a week.

That's the core argument of the Agent Factory Thesis I studied today.

**Here's what shifted my thinking:**

🔹 **Digital FTEs aren't tools — they're workforce.**
The 10-80-10 rule: humans set intent (10%), AI executes (80%), humans verify (10%). You're not replacing work. You're restructuring it.

🔹 **Five lines of context outperform five paragraphs of prompts.**
Power users don't ask AI questions — they brief it like a smart-but-new colleague. Context window, constraints, files, clear ask. That's the formula.

🔹 **Markdown is the grammar of AI agents.**
Agent-to-agent communication, skill specs, README-driven development — it all runs on Markdown. If you can't structure text, you can't direct AI.

The shift from SaaS (per-seat) to Agent Era (per-outcome) isn't coming.
It's already the business model of tomorrow's winners.

If companies sell outcomes instead of software — what does that mean for the skills you're building right now?

Learning with Sir Anas at GIAIC

#AgentFactory #AIPrompting #DigitalFTE #Markdown #GIAIC #LearnInPublic #AIAgents #Panaversity

---

## COMPLETE EXAMPLE — 10-POINT FORMAT (Urdu)

*Input: Agent Factory Digital FTE — 10 points*

---

میں نے پچھلے مہینے اپنا پہلا AI ملازم رکھا۔
$1,200/ماہ پر — 168 گھنٹے فی ہفتہ کام۔
میرا انسانی ملازم $5,000/ماہ لیتا ہے اور صرف 40 گھنٹے دیتا ہے۔

یہ حساب تکلیف دہ ہے۔ Agent Factory کے یہ 10 نکات نے میری سوچ بدل دی:

1/ **168 گھنٹے بمقابلہ 40**
Digital FTE کبھی نہیں سوتا، چھٹی نہیں لیتا، تھکتا نہیں۔ ہفتے میں 4.2 گنا زیادہ آؤٹ پٹ — بغیر اوور ٹائم کے۔

2/ **$500–2K بمقابلہ $4K–8K+/ماہ**
اپنا بہترین عمل ایک بار AI agent میں ڈھالیں۔ وہ بغیر رکے چلتا رہے گا۔

3/ **سالانہ 9,000 گھنٹے بمقابلہ 2,000**
ایک Digital FTE کا ایک سال = 4.5 انسانی سال کا کام۔ startup کی رفتار سے۔

4/ **99%+ consistency بمقابلہ 85–95%**
انسانوں کے اچھے اور برے دن ہوتے ہیں۔ Digital FTE رات 3 بجے بھی وہی معیار دیتا ہے جو صبح 9 بجے۔

5/ **10-80-10 کا اصول**
انسان: intent (10%) → AI: execute (80%) → انسان: verify (10%)۔
آپ replace نہیں ہوتے — promote ہوتے ہیں۔

6/ **فوری cloning بمقابلہ مہینوں کی hiring**
کوئی workflow کام کر رہا ہے؟ منٹوں میں 10 agents بنائیں — نہ کہ سہ ماہیوں میں۔

7/ **Spec-Driven Development**
ایک بار لکھیں، ہمیشہ کے لیے deploy کریں۔ آپ کی expertise ایک recipe بنتی ہے — جو آپ کے سوتے وقت چلتی ہے۔

8/ **صفر overhead اخراجات**
نہ benefits، نہ HR، نہ sick leave، نہ performance reviews۔ صرف outcomes۔

9/ **SaaS سے Agent Era تک**
Software نے seats بیچی۔ AI outcomes بیچتا ہے۔
کل کا business model آج آ چکا ہے۔

10/ **پانچ Maturity Levels**
Level 1: AI Awareness (10-20% فائدہ)۔
Level 5: AI-First Enterprise (10x productivity)۔
Digital FTEs وہ پل ہیں جو آپ کو اوپر لے جاتے ہیں۔

جو کمپنیاں levels 3-5 پہلے سمجھ لیں گی — وہ صرف تیز نہیں چلیں گی۔
وہ ایک مختلف category میں ہوں گی۔

آپ کی organization ابھی کس level پر ہے؟

Sir Anas کے ساتھ سیکھ رہی ہوں @GIAIC | Panaversity Agent Factory

#AgentFactory #DigitalFTE #AIEmployee #FutureOfWork #GIAIC #Panaversity #AIAgents #LearnInPublic #10x #AIFirst
