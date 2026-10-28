"""Generate original CC BY-SA 4.0 optimization diagrams with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT=Path('docs/assets/concept-animations')
BG='#f8fafc'; INK='#1a3045'; GREY='#cbd5e1'; BLUE='#277da8'; ORANGE='#c47633'
def font(n):
    for name in ('DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf'):
        try: return ImageFont.truetype(name,n*2)
        except OSError: pass
    raise RuntimeError('DejaVu Sans or Arial required')
def line(d,xy,fill,width=2): d.line([(int(x*2),int(y*2)) for x,y in xy],fill=fill,width=width*2)
def text(d,xy,s,size=16,fill=INK): d.text((xy[0]*2,xy[1]*2),s,font=font(size),fill=fill)
def dot(d,x,y,color,r=6): d.ellipse(((x-r)*2,(y-r)*2,(x+r)*2,(y+r)*2),fill=color)
def base(title):
    im=Image.new('RGB',(1440,800),BG); d=ImageDraw.Draw(im); text(d,(28,22),title,23); line(d,[(28,64),(692,64)],GREY); return im,d
def finish(name,frames):
    sheet=Image.new('RGB',(720,400*len(frames)))
    for i,f in enumerate(frames): sheet.paste(f,(0,400*i))
    palette=sheet.quantize(colors=96)
    frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=120,loop=0,disposal=1,optimize=True)
    print(name,(OUT/name).stat().st_size)
def frame(im): return im.resize((720,400),Image.Resampling.LANCZOS)
def sgd():
    # Scalar quadratic L(theta)=theta^2/2, gradients theta + fixed batch noise.
    noise=[.4,-.45,.3,-.2,.25,-.15,.12,-.1]; vals=[2.5]
    for n in noise: vals.append(vals[-1]-.35*(vals[-1]+n))
    def px(v): return 360+v*95
    def py(v): return 330-v*v*29
    frames=[]
    for f in range(64):
        im,d=base('Mini-batch SGD'); text(d,(30,87),'Loss',16); text(d,(617,346),'parameter',16)
        line(d,[(73,330),(675,330)],GREY); line(d,[(73,100),(73,330)],GREY)
        line(d,[(px(-2.7+i*.03),py(-2.7+i*.03)) for i in range(181)],'#89a5b8',2)
        step=min(f//8,7); t=(f%8)/7
        for j in range(step):
            line(d,[(px(vals[j]),py(vals[j])),(px(vals[j+1]),py(vals[j+1]))],ORANGE,2)
            dot(d,px(vals[j]),py(vals[j]),ORANGE,3)
        v=vals[step]+(vals[step+1]-vals[step])*t
        line(d,[(px(vals[step]),py(vals[step])),(px(v),py(v))],ORANGE,3)
        dot(d,px(v),py(v),BLUE,8)
        text(d,(100,355),'one batch per update',16); text(d,(410,100),'step '+str(step+1)+' / 8',16,BLUE)
        frames.append(frame(im))
    finish('sgd-minibatch-updates.gif',frames)
def schedule():
    frames=[]
    def x(t): return 92+t*570
    def y(t): return 326-220*(t/.2 if t<.2 else (1-t)/.8)
    for f in range(60):
        im,d=base('Learning-rate schedule'); text(d,(27,88),'rate',16); text(d,(622,348),'step',16)
        line(d,[(92,100),(92,326),(662,326)],GREY,2)
        line(d,[(x(0),y(0)),(x(.2),y(.2))],ORANGE,4)
        line(d,[(x(.2),y(.2)),(x(1),y(1))],BLUE,4)
        line(d,[(x(.2),102),(x(.2),326)],GREY,1)
        text(d,(99,346),'warm-up',16,ORANGE); text(d,(316,346),'linear decay',16,BLUE)
        t=f/59; line(d,[(x(t),y(t)),(x(t),326)],'#8fa6b7',1); dot(d,x(t),y(t),INK,7)
        frames.append(frame(im))
    finish('learning-rate-warmup-decay.gif',frames)
if __name__=='__main__': sgd(); schedule()
