from PIL import Image, ImageDraw, ImageFont
import math, os

BASE = r"C:\Users\ThinK Pad\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\390597e3-66e2-428d-8580-47cc12dfe4bb\0aedb6b0-ce9d-4782-bd78-49b25f3cc056\skills\canvas-design"
OUT  = r"D:\syeda Gulzar Bano\Quarter5-Assignment\Q5-Assignment\fte_english_graphic.png"
FD   = os.path.join(BASE, "canvas-fonts")

W, H = 1080, 1350
S    = 2
W2, H2 = W * S, H * S

CATEGORY = "AGENT ECONOMY   .   WORKFORCE INTELLIGENCE   .   2026"
HEADLINE = [
    ("The Numbers Behind",  62),
    ("Digital FTEs",        80),
    ("Rewriting Work.",      80),
]
SUBLINE = "Cost Efficiency   .   Execution Model   .   AI Maturity"
CARDS = [
    dict(
        tag  = "COST & OUTPUT",
        title= "$500-2K Beats $4K-8K+",
        sub  = "168 hrs/week. Zero sick days. 4.2x output.",
        sub2 = "9,000 hrs/year vs 2,000 -- same cost window.",
        det  = "$500-2K/mo  .  168 hrs/wk  .  9,000 hrs/yr",
    ),
    dict(
        tag  = "EXECUTION MODEL",
        title= "The 10-80-10 Rule",
        sub  = "Humans set intent. AI executes. Humans verify.",
        sub2 = "You are not replaced. You are promoted.",
        det  = "Intent 10%  .  AI Execute 80%  .  Verify 10%",
    ),
    dict(
        tag  = "AI MATURITY",
        title= "Five Levels to 10x",
        sub  = "Level 1: AI Awareness to Level 5: AI-First.",
        sub2 = "Spec-Driven: write expertise once, run forever.",
        det  = "AI-Aware  .  AI-Assisted  .  AI-First Enterprise",
    ),
]
CREATOR  = "Agent Economy Intelligence"
ORG_LINE = "Digital Workforce   .   Agent Factory Framework"
HASHTAGS = "#DigitalFTE    #AgentFactory    #FutureOfWork    #AIFirst"

BG     = (243, 246, 252)
NAVY   = (2,   16,  50)
NAVY2  = (4,   36,  96)
BLUE   = (10,  102, 194)
BLUE2  = (6,   76,  158)
PURPLE = (74,  21,  75)
TEAL   = (15,  110, 86)
WHITE  = (255, 255, 255)
DARK   = (14,  18,  34)
MID    = (68,  80,  108)
LP  = [(6,72,152),  (56,12,58),   (8,84,64)]
LG  = [(52,118,196),(118,52,122), (42,142,112)]
RP  = [(240,247,255),(250,237,252),(232,252,244)]

def F(n, s): return ImageFont.truetype(os.path.join(FD, n), int(s * S))
BOLD  = lambda s: F("BigShoulders-Bold.ttf",      s)
TITLE = lambda s: F("WorkSans-Bold.ttf",           s)
BODY  = lambda s: F("WorkSans-Regular.ttf",        s)
JURA  = lambda s: F("Jura-Medium.ttf",             s)
LIGHT = lambda s: F("Jura-Light.ttf",              s)
SANSB = lambda s: F("InstrumentSans-Bold.ttf",     s)
SANS  = lambda s: F("InstrumentSans-Regular.ttf",  s)

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
    d.rounded_rectangle([x1,y1,x2,y2], radius=r*S, fill=fill, outline=outline, width=max(1,ow*S))

def left_panel(d, x1, y1, x2, y2, r, fill):
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
    d.line([(p1[0]*S,p1[1]*S),(p2[0]*S,p2[1]*S)], fill=col, width=max(1,w*S))

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

img = Image.new("RGB", (W2, H2), BG)
d   = ImageDraw.Draw(img)
MX  = W // 2

for x in range(0, W+1, 90):
    for y in range(0, H+1, 90):
        d.ellipse([x*S-4,y*S-4,x*S+4,y*S+4], fill=(210,220,238))

HDR = 484
vgrad(img, 0, 0, W, HDR, NAVY, BLUE2)
d = ImageDraw.Draw(img)

hy_c = HDR * S // 2
for band_r in range(160*S, 0, -10):
    t    = 1 - band_r / (160*S)
    gcol = tuple(min(255, int(NAVY2[j]+(BLUE[j]-NAVY2[j])*t*0.55)) for j in range(3))
    d.ellipse([(MX*S-band_r*2, hy_c-band_r//2),(MX*S+band_r*2, hy_c+band_r//2)], fill=gcol)
d = ImageDraw.Draw(img)

for hx,hy,hr,hc in [(962,58,114,(14,60,142)),(994,236,78,(12,54,128)),
                     (876,368,58,(16,66,148)),(76,92,94,(12,54,128)),
                     (30,272,66,(10,48,116)),(136,408,48,(14,62,140))]:
    hex_out(d, hx, hy, hr, hc, 2)

TC = (18, 58, 132)
for ox,ex,ey in [(102,158,268),(W-102,W-158,268)]:
    circ(d, ox, 198, 4, TC)
    ln(d, (ox,198),(ex,198), TC, 1)
    ln(d, (ex,198),(ex,ey),  TC, 1)
    circ(d, ex, ey, 4, TC)

f_cat = JURA(12)
bcat  = d.textbbox((0,0), CATEGORY, font=f_cat)
cw1x  = (bcat[2]-bcat[0]) // S
ln(d,(76,52),(MX-cw1x//2-20,52),(76,130,208),1)
ln(d,(MX+cw1x//2+20,52),(W-76,52),(76,130,208),1)
diam(d, MX, 52, 4, (100,148,218))
cx(d, 38, CATEGORY, f_cat, (158,202,255))

y_cur = 80
HCOLS = [(220,235,255), WHITE, (88,196,255)]
for idx, (text, size) in enumerate(HEADLINE):
    fh  = BOLD(size)
    col = HCOLS[min(idx, 2)]
    bx  = d.textbbox((0,0), text, font=fh)
    d.text(((W2-(bx[2]-bx[0]))//2, y_cur*S), text, font=fh, fill=col)
    y_cur += (bx[3]-bx[1])//S + 10

bar_y = y_cur + 12
rect(d, (MX-62, bar_y, MX+62, bar_y+9),  fill=(88,156,224))
rect(d, (MX-54, bar_y+1, MX+54, bar_y+8), fill=(140,196,252))
ln(d,(76,bar_y+4),(MX-76,bar_y+4),TC,1)
ln(d,(MX+76,bar_y+4),(W-76,bar_y+4),TC,1)
cx(d, bar_y+22, SUBLINE, LIGHT(16), (152,200,255))

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

vgrad(img, 0, HDR, W, HDR+56, (200,224,252), BG)
d = ImageDraw.Draw(img)

CMX = 48; CY = 506; CH = 220; CG = 22; LPW = 278; CR = 18
CX1 = CMX; CX2 = W - CMX

for i, card in enumerate(CARDS):
    y1 = CY + i*(CH+CG); y2 = y1+CH
    col = NCOL[i]; lp = LP[i]; lg = LG[i]; rp = RP[i]

    for s_off in [8,5,2]:
        sv = 220 - s_off*8
        rr(d,(CX1+s_off,y1+s_off+2,CX2+s_off,y2+s_off+2),CR,fill=(sv,sv,min(255,sv+14)))

    rr(d, (CX1,y1,CX2,y2), CR, fill=rp)
    left_panel(d, CX1, y1, CX1+LPW, y2, CR, lp)

    f_wm = BOLD(102)
    ns   = str(i+1)
    bwm  = d.textbbox((0,0), ns, font=f_wm)
    nw,nh = bwm[2]-bwm[0], bwm[3]-bwm[1]
    d.text(((CX1+CX1+LPW)*S//2 - nw//2 - bwm[0],
            (y1+y2)*S//2 - nh//2 - bwm[1] + 10*S), ns, font=f_wm, fill=lg)

    cx_in(d, CX1, CX1+LPW, y2-24, card["tag"], JURA(11), WHITE)
    ln(d,(CX1+LPW,y1+CR//2),(CX1+LPW,y2-CR//2), col, 1)

    rx = CX1 + LPW + 28
    lx(d, rx, y1+22, card["title"], TITLE(30), DARK)
    lx(d, rx, y1+66, card["sub"],   BODY(17),  MID)
    lx(d, rx, y1+92, card["sub2"],  LIGHT(15), tuple(min(255,v+40) for v in col))
    ln(d,(rx,y2-62),(CX2-20,y2-62),(208,218,234),1)
    lx(d, rx, y2-46, card["det"], JURA(13), col)

    circ(d, CX2-30, y1+26, 9, col)
    circ(d, CX2-30, y1+26, 5, rp)
    circ(d, CX2-30, y1+26, 2, col)

FDY = CY + 3*CH + 2*CG + 34
ln(d,(54,FDY),(W-54,FDY),(194,210,232),1)
for dx,dc in zip([-16,0,16],[BLUE,PURPLE,TEAL]):
    diam(d, MX+dx, FDY, 4, dc)

TY = FDY + 28
cx(d, TY,    CREATOR,  SANSB(24), DARK)
cx(d, TY+38, ORG_LINE, SANS(14),  BLUE)
cx(d, TY+64, HASHTAGS, LIGHT(11), (128,152,198))

rect(d, (0,H-8,W,H), BLUE)

img = img.resize((W,H), Image.LANCZOS)
img.save(OUT, "PNG", dpi=(300,300))
print("Saved:", OUT)
