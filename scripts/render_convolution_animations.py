"""Original CC BY-SA 4.0 teaching diagrams. Run from repo root; requires Pillow.

Fonts: DejaVu Sans on Linux, Arial on Windows. No downloaded art or model data.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('docs/assets/concept-animations')
S = 2
BG, INK, MUTED, LINE = '#f8fafc', '#193047', '#52677c', '#cbd5e1'
COLORS = ['#277da8', '#c47633', '#448b70']

def font(size):
    for name in ['DejaVuSans.ttf', 'C:/Windows/Fonts/arial.ttf']:
        try:
            return ImageFont.truetype(name, size*S)
        except OSError:
            pass
    raise RuntimeError('Install DejaVu Sans or Arial')

class Canvas:
    def __init__(self, title):
        self.im = Image.new('RGB', (720*S, 400*S), BG)
        self.d = ImageDraw.Draw(self.im)
        self.text(28, 22, title, 23)
        self.line((28, 64), (692, 64), LINE)

    def text(self, x, y, text, size=16, color=INK):
        self.d.text((x*S, y*S), text, fill=color, font=font(size))

    def line(self, a, b, color=LINE, width=2):
        self.d.line(tuple(v*S for p in [a,b] for v in p), fill=color, width=width*S)

    def box(self, x, y, w, h, fill, outline=None, width=1):
        self.d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S), radius=3*S,
                                fill=fill, outline=outline, width=width*S)

    def dot(self, x, y, color, r=5):
        self.d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S), fill=color)

    def frame(self):
        return self.im.resize((720,400), Image.Resampling.LANCZOS)

def save(name, frames):
    # One common palette prevents temporal palette flicker.
    sheet = Image.new('RGB', (720,400*len(frames)))
    for i, frame in enumerate(frames):
        sheet.paste(frame, (0,400*i))
    palette = sheet.quantize(colors=96)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT/name, save_all=True, append_images=indexed[1:],
                    loop=0, duration=100, disposal=1, optimize=True)
    print(name, (OUT/name).stat().st_size)

def dilation():
    frames=[]
    for f in range(60):
        c=Canvas('Dilated convolution')
        # Five output positions, then a visually explicit replay reset.
        step=min(f//12,4); phase=(f%12)/11
        center=4+step
        for row, rate in enumerate([1,2,3]):
            y=112+row*88; color=COLORS[row]
            c.text(28,y-7,f'd = {rate}',18,color)
            for j in range(13):
                x=145+j*38
                c.box(x,y,25,25,'#e5ebf0')
            for off in [-rate,0,rate]:
                x=157+(center+off)*38
                c.line((x,y+26),(157+center*38,y+58),color,1)
                c.box(x-12,y,25,25,color)
                t=min(phase*1.6,1)
                c.dot(x+(center*38+157-x)*t,y+26+32*t,color,4)
            for j in range(4,9):
                c.box(145+j*38,y+56,25,14,color if j<=center else '#e5ebf0')
            c.box(145+center*38,y+54,25,18,None,INK,2)
        c.text(28,371,'3 taps',15,MUTED)
        c.text(145,371,'Input',15,MUTED)
        c.text(510,371,'stride = 1',15,MUTED)
        frames.append(c.frame())
    save('dilated-convolution-sampling.gif',frames)

def depthwise():
    frames=[]
    for f in range(60):
        c=Canvas('Depthwise separable convolution')
        c.text(30,82,'Input',17)
        c.text(232,82,'3 x 3',17)
        c.text(365,82,'Depthwise',17)
        c.text(535,82,'1 x 1',17)
        c.text(623,82,'Output',17)
        stage=min(f//20,2); t=(f%20)/19
        ys=[157,239,321]
        for ch,(y,color) in enumerate(zip(ys,COLORS)):
            for r in range(5):
                for col in range(5):
                    shade=(r*3+col*2+ch)%5
                    c.box(30+col*12,y-30+r*12,10,10,color if shade<3 else '#dce5eb')
            c.box(29,y-31,36,36,None,INK,2)
            c.line((100,y),(242,y),color)
            for r in range(3):
                for col in range(3):
                    c.box(222+col*12,y-18+r*12,10,10,color)
            c.line((260,y),(396,y),color)
            c.box(385,y-11,22,22,color if stage>=1 else '#e5ebf0',color)
            if stage==0:
                c.dot(100+280*t,y,color)
            for oy in [198,280]:
                c.line((408,y),(632,oy),LINE,1)
                if stage==1:
                    c.dot(408+224*t,y+(oy-y)*t,color,5)
        # Each output uses its own learned channel weights; line colors do not encode sign.
        for oy in [198,280]:
            c.box(628,oy-15,30,30,'#7567a8' if stage==2 else '#e5ebf0',INK)
        c.text(28,371,'3 channels',15,MUTED)
        c.text(278,371,'Independent filters',15,MUTED)
        c.text(550,371,'Channel mixing',15,MUTED)
        frames.append(c.frame())
    save('depthwise-channel-mixing.gif',frames)

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    dilation()
    depthwise()
