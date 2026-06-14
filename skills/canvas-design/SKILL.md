---
name: canvas-design
description: "Professional LinkedIn Graphic Designer — generates premium 1080×1350 px post graphics for any topic using Python + Pillow. Split-panel card design, gradient header, 2× supersampling. Invoke whenever a user wants to create a LinkedIn post graphic, educational card, or visual content for any topic."
license: Complete terms in LICENSE.txt
---

# Canvas Design Skill
**Role:** Senior Visual Designer — LinkedIn Post Graphics

You generate premium, print-ready LinkedIn post graphics from user-provided content. Every graphic is 1080 × 1350 px, professionally typeset, and ready to upload to LinkedIn.

**Outputs only:** a design-philosophy `.md` file and a `linkedin_graphic.png`. No explanatory text beyond a one-line delivery note.

---

## STEP 0 — EXTRACT CONTENT FROM THE USER'S PROMPT

Before writing a single line of code, read the user's prompt and fill this table. **Never guess without evidence — derive intelligently from context.**

| Variable | What to look for | Fallback |
|---|---|---|
| `CATEGORY` | Class name / org / post category | `"LEARNING NOTES  ·  [TOPIC]  ·  [YEAR]"` |
| `HEADLINE` | The hook — max 9 words, split into 2–3 punchy lines | Generate from topic |
| `SUBLINE` | 3 micro-labels (one per card), joined by ` · ` | Derive from 3 key points |
| `CREATOR` | Full name of the person posting | `"Author"` |
| `ORG_LINE` | Combine: Organization · Mentor (if any) · Date | `"[Today's date]"` |
| `HASHTAGS` | 3–5 relevant hashtags | Derive from topic |

### 3 Card Sections
Always produce exactly **3** cards. Each card needs:

| Field | Description | Limit |
|---|---|---|
| `tag` | Short ALL-CAPS category label | 2–4 words |
| `title` | Bold main point | 3–5 words |
| `sub` | Primary insight sentence | 6–10 words |
| `sub2` | Supporting detail, formula, or example | 6–10 words |
| `det` | Key terms / formula for bottom accent line | one concise line |

If the user gives >3 points → pick the 3 most important.
If <3 → derive the missing ones from the topic.

**GOLDEN RULE:** Zero hardcoded strings. Every word on the graphic must flow from named Python variables defined at the top of the script — never scattered string literals inside draw calls.

---

## STEP 1 — DESIGN PHILOSOPHY FILE

Save `[topic_slug]_philosophy.md` to the skill base directory.
- Name the visual movement (2 words, e.g. "Voltage Grid", "Signal Meridian", "Precision Bloom")
- Write 3–4 short paragraphs: composition, color, typography, craftsmanship
- Emphasize that the result must look meticulously hand-crafted — the work of a seasoned designer

---

## STEP 2 — GENERATE THE GRAPHIC

### Canvas Spec
- **Output:** 1080 × 1350 px, PNG, 300 DPI → `[BASE]/linkedin_graphic.png`
- **Render:** 2160 × 2700 (2× supersampled) → `img.resize((1080, 1350), Image.LANCZOS)`
- **Library:** Pillow only (no numpy, no cv2)

---

### Color System

Three fixed accent colors drive the three cards. Always in this order:

| Slot | Name | Full color | Deep (left panel) | Ghost (watermark) | Right tint |
|---|---|---|---|---|---|
| 0 | Blue | (10, 102, 194) | (6, 72, 152) | (52, 118, 196) | (240, 247, 255) |
| 1 | Purple | (74, 21, 75) | (56, 12, 58) | (118, 52, 122) | (250, 237, 252) |
| 2 | Teal | (15, 110, 86) | (8, 84, 64) | (42, 142, 112) | (232, 252, 244) |

The **primary accent** (from user prompt, default LinkedIn Blue `(10, 102, 194)`) controls:
- Header gradient end color
- Node circle outlines
- Footer org-line color
- Bottom accent bar

Fixed neutrals:
```
BG     = (243, 246, 252)   # page background
NAVY   = (2,   16,  50)    # header gradient start
DARK   = (14,  18,  34)    # heading text
MID    = (68,  80,  108)   # body text
WHITE  = (255, 255, 255)
```

---

### Layout Diagram (all measurements in 1× px)

```
┌──────────────────────────────────────────────────────┐  y = 0
│  CATEGORY LABEL — tracked caps, centered             │
│                                                      │
│        HEADLINE LINE 1 (BigShoulders 60–65pt)        │  HEADER
│        HEADLINE LINE 2 (BigShoulders 78–84pt)        │  ZONE
│        HEADLINE LINE 3 (BigShoulders 78–84pt)        │  navy → blue
│              ────── accent bar ──────                │  gradient
│    tag1   ·   tag2   ·   tag3  (Jura Light)          │  + hex marks
│                                                      │  + circuit
│  ○────────────────○────────────────○                 │  traces
│  01              02               03  (nodes)         │
├──────────────────────────────────────────────────────┤  y ≈ 500
│                                                      │
│ ┌──────────┬──────────────────────────────────────┐  │
│ │ [BLUE]   │  TITLE (WorkSans Bold 30pt)          │  │  CARD 1
│ │  ghost 1 │  Sub (WorkSans Regular 17pt)         │  │
│ │          │  Sub2 (Jura Light 15pt, accent tint) │  │
│ │ TAG LABEL│  ─────────────────────────────────── │  │
│ └──────────┘  Det (Jura Medium 13pt, accent col)  │  │
│                                                      │
│ ┌──────────┬──────────────────────────────────────┐  │
│ │ [PURPLE] │  TITLE                               │  │  CARD 2
│ │  ghost 2 │  Sub / Sub2 / Det                    │  │
│ └──────────┴──────────────────────────────────────┘  │
│                                                      │
│ ┌──────────┬──────────────────────────────────────┐  │
│ │ [TEAL]   │  TITLE                               │  │  CARD 3
│ │  ghost 3 │  Sub / Sub2 / Det                    │  │
│ └──────────┴──────────────────────────────────────┘  │
│                                                      │
│          ◆   ◆   ◆   (triple colored diamonds)       │
│          CREATOR NAME  (InstrumentSans Bold 24pt)    │  FOOTER
│          ORG · Mentor · Date  (InstrumentSans 14pt)  │
│          #tag1  #tag2  #tag3  (Jura Light 11pt)      │
└──────────────────────────────────────────────────────┘  y = 1342
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓ BLUE BOTTOM BAR (8 px) ▓▓▓▓▓▓▓▓▓▓▓▓▓│  y = 1350
```

---

### Script Structure — Follow Exactly

```python
#!/usr/bin/env python3
"""
LinkedIn Graphic — [TOPIC NAME]
Premium split-panel design | 2x supersampled
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

# ── PATHS ─────────────────────────────────────────────────────────────────────
BASE = r"[PASTE SKILL BASE DIRECTORY PATH HERE]"
OUT  = os.path.join(BASE, "linkedin_graphic.png")
FD   = os.path.join(BASE, "canvas-fonts")

# ── CANVAS ────────────────────────────────────────────────────────────────────
W, H = 1080, 1350
S    = 2
W2, H2 = W * S, H * S

# ══════════════════════════════════════════════════════════════════════════════
#  CONTENT  ← ONLY EDIT THIS SECTION FOR NEW POSTS
# ══════════════════════════════════════════════════════════════════════════════
CATEGORY = "CATEGORY LABEL  ·  TOPIC  ·  YEAR"

# Headline: list of (text, font_size) tuples — 2 or 3 lines
# Line 1: shorter intro (60–65pt), Line 2–3: punchy main/payoff (78–84pt)
HEADLINE = [
    ("Intro line here",    62),
    ("Main Statement.",    80),
    ("Payoff here.",       80),
]

# Sub-tag line under the accent bar (one short label per card, joined by  ·)
SUBLINE = "Tag One   ·   Tag Two   ·   Tag Three"

# Three cards — one per key point
CARDS = [
    dict(
        tag  = "CATEGORY ONE",
        title= "Card Title",
        sub  = "Primary insight sentence here",
        sub2 = "Supporting detail or formula",
        det  = "Key Term  ·  Key Term  ·  Key Term",
    ),
    dict(
        tag  = "CATEGORY TWO",
        title= "Card Title",
        sub  = "Primary insight here",
        sub2 = "Supporting detail here",
        det  = "Key Term  ·  Key Term  ·  Key Term",
    ),
    dict(
        tag  = "CATEGORY THREE",
        title= "Card Title",
        sub  = "Primary insight here",
        sub2 = "Supporting detail here",
        det  = "Key Term  ·  Key Term",
    ),
]

CREATOR  = "Full Name"
ORG_LINE = "Organization  ·  Context  ·  Date"
HASHTAGS = "#Tag1    #Tag2    #Tag3    #Tag4"
# ══════════════════════════════════════════════════════════════════════════════

# ── PALETTE ───────────────────────────────────────────────────────────────────
BG     = (243, 246, 252)
NAVY   = (2,   16,  50)
NAVY2  = (4,   36,  96)
BLUE   = (10,  102, 194)   # ← primary accent (swap this for different themes)
BLUE2  = (6,   76,  158)   # header gradient end
PURPLE = (74,  21,  75)
TEAL   = (15,  110, 86)
WHITE  = (255, 255, 255)
DARK   = (14,  18,  34)
MID    = (68,  80,  108)

# Card left-panel colors (deep), ghost (watermark), right-panel tints
LP  = [(6,72,152),  (56,12,58),   (8,84,64)]
LG  = [(52,118,196),(118,52,122), (42,142,112)]
RP  = [(240,247,255),(250,237,252),(232,252,244)]

# ── FONTS ─────────────────────────────────────────────────────────────────────
def F(n, s): return ImageFont.truetype(os.path.join(FD, n), int(s * S))
BOLD  = lambda s: F("BigShoulders-Bold.ttf",      s)
TITLE = lambda s: F("WorkSans-Bold.ttf",           s)
BODY  = lambda s: F("WorkSans-Regular.ttf",        s)
JURA  = lambda s: F("Jura-Medium.ttf",             s)
LIGHT = lambda s: F("Jura-Light.ttf",              s)
SANSB = lambda s: F("InstrumentSans-Bold.ttf",     s)
SANS  = lambda s: F("InstrumentSans-Regular.ttf",  s)

# ── PRIMITIVES (all x/y in 1x coords) ─────────────────────────────────────────
def cx(d, y, text, fnt, fill):
    bx = d.textbbox((0,0), text, font=fnt)
    d.text(((W2-(bx[2]-bx[0]))//2, y*S), text, font=fnt, fill=fill)

def lx(d, x, y, text, fnt, fill):
    bx = d.textbbox((0,0), text, font=fnt)
    d.text((x*S - bx[0], y*S - bx[1]), text, font=fnt, fill=fill)

def cx_in(d, x1, x2, y, text, fnt, fill):
    bx = d.textbbox((0,0), text, font=fnt)
    tx = ((x1+x2)*S - (bx[2]-bx[0])) // 2 - bx[0]
    d.text((tx, y*S - bx[1]), text, font=fnt, fill=fill)

def rr(d, box, r, fill=None, outline=None, ow=1):
    x1,y1,x2,y2 = [v*S for v in box]
    d.rounded_rectangle([x1,y1,x2,y2], radius=r*S,
                         fill=fill, outline=outline, width=max(1,ow*S))

def left_panel(d, x1, y1, x2, y2, r, fill):
    """Rectangle rounded on left side only (1x coords)."""
    X1,Y1,X2,Y2,R = x1*S,y1*S,x2*S,y2*S,r*S
    d.rectangle([X1+R, Y1, X2, Y2],        fill=fill)
    d.rectangle([X1,   Y1+R, X1+R, Y2-R],  fill=fill)
    d.pieslice([X1, Y1,     X1+2*R, Y1+2*R], 180, 270, fill=fill)
    d.pieslice([X1, Y2-2*R, X1+2*R, Y2],     90,  180, fill=fill)

def vgrad(img, x1, y1, x2, y2, c1, c2):
    d2 = ImageDraw.Draw(img)
    ht = (y2-y1)*S
    for i in range(ht):
        t = i / max(ht-1, 1)
        c = tuple(int(c1[j]+(c2[j]-c1[j])*t) for j in range(3))
        d2.line([(x1*S, y1*S+i),(x2*S, y1*S+i)], fill=c)

def ln(d, p1, p2, col, w=1):
    d.line([(p1[0]*S,p1[1]*S),(p2[0]*S,p2[1]*S)],
           fill=col, width=max(1,w*S))

def circ(d, cx2, cy2, r, fill=None, outline=None, ow=2):
    d.ellipse([cx2*S-r*S, cy2*S-r*S, cx2*S+r*S, cy2*S+r*S],
               fill=fill, outline=outline, width=max(1,ow*S))

def diam(d, cx2, cy2, r, fill):
    d.polygon([(cx2*S,(cy2-r)*S),((cx2+r)*S,cy2*S),
               (cx2*S,(cy2+r)*S),((cx2-r)*S,cy2*S)], fill=fill)

def rect(d, box, fill):
    d.rectangle([v*S for v in box], fill=fill)

def hex_out(d, hx, hy, hr, col, lw=2):
    pts = [(hx*S + hr*S*math.cos(math.radians(60*i+30)),
            hy*S + hr*S*math.sin(math.radians(60*i+30))) for i in range(6)]
    for i in range(6):
        d.line([pts[i], pts[(i+1)%6]], fill=col, width=max(1,lw*S))

# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    img = Image.new("RGB", (W2, H2), BG)
    d   = ImageDraw.Draw(img)
    MX  = W // 2

    # 1. Dot grid
    for x in range(0, W+1, 90):
        for y in range(0, H+1, 90):
            d.ellipse([x*S-4,y*S-4,x*S+4,y*S+4], fill=(210,220,238))

    # 2. Header gradient
    HDR = 484
    vgrad(img, 0, 0, W, HDR, NAVY, BLUE2)
    d = ImageDraw.Draw(img)

    # 3. Center glow band
    hy_c = HDR * S // 2
    for band_r in range(160*S, 0, -10):
        t    = 1 - band_r / (160*S)
        gcol = tuple(min(255, int(NAVY2[j]+(BLUE[j]-NAVY2[j])*t*0.55)) for j in range(3))
        d.ellipse([(MX*S-band_r*2, hy_c-band_r//2),
                   (MX*S+band_r*2, hy_c+band_r//2)], fill=gcol)
    d = ImageDraw.Draw(img)

    # 4. Hex watermarks
    for hx,hy,hr,hc in [(962,58,114,(14,60,142)),(994,236,78,(12,54,128)),
                         (876,368,58,(16,66,148)),(76,92,94,(12,54,128)),
                         (30,272,66,(10,48,116)),(136,408,48,(14,62,140))]:
        hex_out(d, hx, hy, hr, hc, 2)

    # 5. Circuit traces
    TC = (18, 58, 132)
    for ox,ex,ey in [(102,158,268),(W-102,W-158,268)]:
        circ(d, ox, 198, 4, TC)
        ln(d, (ox,198),(ex,198), TC, 1)
        ln(d, (ex,198),(ex,ey),  TC, 1)
        circ(d, ex, ey, 4, TC)

    # 6. Category label
    f_cat = JURA(12)
    bcat  = d.textbbox((0,0), CATEGORY, font=f_cat)
    cw1x  = (bcat[2]-bcat[0]) // S
    ln(d,(76,52),(MX-cw1x//2-20,52),(76,130,208),1)
    ln(d,(MX+cw1x//2+20,52),(W-76,52),(76,130,208),1)
    diam(d, MX, 52, 4, (100,148,218))
    cx(d, 38, CATEGORY, f_cat, (158,202,255))

    # 7. Headline
    y_cur = 80
    HEADLINE_COLORS = [(220,235,255), WHITE, (88,196,255)]
    for idx, (text, size) in enumerate(HEADLINE):
        fh   = BOLD(size)
        col  = HEADLINE_COLORS[min(idx, 2)]
        bx   = d.textbbox((0,0), text, font=fh)
        d.text(((W2-(bx[2]-bx[0]))//2, y_cur*S), text, font=fh, fill=col)
        y_cur += (bx[3]-bx[1])//S + 10

    # 8. Accent bar + sub-tag
    bar_y = y_cur + 12
    rect(d, (MX-62, bar_y,   MX+62, bar_y+9),  fill=(88,156,224))
    rect(d, (MX-54, bar_y+1, MX+54, bar_y+8),  fill=(140,196,252))
    ln(d,(76,bar_y+4),(MX-76,bar_y+4),TC,1)
    ln(d,(MX+76,bar_y+4),(W-76,bar_y+4),TC,1)
    cx(d, bar_y+22, SUBLINE, LIGHT(16), (152,200,255))

    # 9. Node circles
    BY   = 444
    NXS  = [238, 540, 842]
    NCOL = [BLUE, PURPLE, TEAL]
    for i in range(2):
        ln(d,(NXS[i]+36,BY),(NXS[i+1]-36,BY),(70,118,188),1)
    for nx,nc,lbl in zip(NXS, NCOL, ["01","02","03"]):
        circ(d, nx, BY, 28, WHITE)
        circ(d, nx, BY, 28, None, nc, 3)
        fn  = SANSB(16)
        bx  = d.textbbox((0,0), lbl, font=fn)
        tw2,th2 = bx[2]-bx[0], bx[3]-bx[1]
        d.text((nx*S-tw2//2, BY*S-th2//2-S), lbl, font=fn, fill=nc)

    # 10. Header→body fade
    vgrad(img, 0, HDR, W, HDR+56, (200,224,252), BG)
    d = ImageDraw.Draw(img)

    # 11. Cards (split-panel)
    CMX = 48;  CY = 506;  CH = 220;  CG = 22;  LPW = 278;  CR = 18
    CX1 = CMX;  CX2 = W - CMX

    for i, card in enumerate(CARDS):
        y1 = CY + i*(CH+CG);  y2 = y1+CH
        col = NCOL[i];  lp = LP[i];  lg = LG[i];  rp = RP[i]

        # Shadow
        for s_off in [8,5,2]:
            sv = 220 - s_off*8
            rr(d,(CX1+s_off,y1+s_off+2,CX2+s_off,y2+s_off+2),CR,
               fill=(sv,sv,min(255,sv+14)))

        # Full card (right tint)
        rr(d, (CX1,y1,CX2,y2), CR, fill=rp)

        # Left colored panel
        left_panel(d, CX1, y1, CX1+LPW, y2, CR, lp)

        # Ghost number
        f_wm = BOLD(102)
        ns   = str(i+1)
        bwm  = d.textbbox((0,0), ns, font=f_wm)
        nw,nh = bwm[2]-bwm[0], bwm[3]-bwm[1]
        d.text(((CX1+CX1+LPW)*S//2 - nw//2 - bwm[0],
                (y1+y2)*S//2 - nh//2 - bwm[1] + 10*S),
               ns, font=f_wm, fill=lg)

        # Tag label (bottom of left panel)
        cx_in(d, CX1, CX1+LPW, y2-24, card["tag"], JURA(11), WHITE)

        # Separator line
        ln(d,(CX1+LPW,y1+CR//2),(CX1+LPW,y2-CR//2), col, 1)

        # Right panel content
        rx = CX1 + LPW + 28
        lx(d, rx, y1+22,  card["title"], TITLE(30), DARK)
        lx(d, rx, y1+66,  card["sub"],   BODY(17),  MID)
        lx(d, rx, y1+92,  card["sub2"],  LIGHT(15),
           tuple(min(255,v+40) for v in col))
        ln(d,(rx,y2-62),(CX2-20,y2-62),(208,218,234),1)
        lx(d, rx, y2-46, card["det"], JURA(13), col)

        # Accent dot
        circ(d, CX2-30, y1+26, 9, col)
        circ(d, CX2-30, y1+26, 5, rp)
        circ(d, CX2-30, y1+26, 2, col)

    # 12. Footer
    FDY = CY + 3*CH + 2*CG + 34
    ln(d,(54,FDY),(W-54,FDY),(194,210,232),1)
    for dx,dc in zip([-16,0,16],[BLUE,PURPLE,TEAL]):
        diam(d, MX+dx, FDY, 4, dc)

    TY = FDY + 28
    cx(d, TY,    CREATOR,  SANSB(24), DARK)
    cx(d, TY+38, ORG_LINE, SANS(14),  BLUE)
    cx(d, TY+64, HASHTAGS, LIGHT(11), (128,152,198))

    # 13. Bottom bar
    rect(d, (0,H-8,W,H), BLUE)

    # 14. Downsample
    img = img.resize((W,H), Image.LANCZOS)
    img.save(OUT, "PNG", dpi=(300,300))
    print(f"Saved: {OUT}")

if __name__ == "__main__":
    build()
```

---

## STEP 3 — REFINEMENT CHECK

After saving the PNG, read it back and verify:
- [ ] No text clips outside card bounds
- [ ] Headline readable at thumbnail size (150 × 150 preview)
- [ ] Three cards visually distinct by color
- [ ] Footer text does not go below y = 1330
- [ ] Word count on graphic ≤ 80 words

If a check fails → adjust font size or spacing constant, regenerate once.

---

## FILES PRODUCED

| File | Purpose |
|---|---|
| `[slug]_philosophy.md` | Visual design rationale |
| `create_graphic.py` | Fully dynamic script — content variables at top |
| `linkedin_graphic.png` | Final 1080 × 1350 px PNG, 300 DPI |

All files saved to the skill base directory.

---

## EXAMPLE INVOCATIONS

```
"Docker & Kubernetes LinkedIn post
 3 points: Containerization, Orchestration, CI/CD
 Name: Ahmed Raza | DevOps Pakistan | July 2026"

"Next.js 15 features post:
 Turbopack stable · Server Actions · Partial Prerendering
 Creator: Sara Khan · FAST University"

"Aaj ki class ka LinkedIn post — topics:
 Data Structures, Sorting Algorithms, Big-O Notation
 My name: Ali Hassan | Instructor: Dr. Waseem | NUST"

"LinkedIn post about Agentic AI:
 1. Planning & Reasoning  2. Tool Use  3. Memory Systems
 Syeda Gulzar Bano | GIAIC | Mentor: Sir Anas | June 2026"
```

This skill works for **any** technical, educational, or professional topic.
The Python script always places ALL content in the labelled `CONTENT` block at the top — never buried in draw calls.
