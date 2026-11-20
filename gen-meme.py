from PIL import Image, ImageDraw, ImageFont
import random
import math

S = 1600
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
PAPER = (247, 241, 222)
INKGREY = (92, 103, 119)
MAGENTA = (224, 33, 138)
GREEN = (30, 125, 79)
SERIF = '/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf'
ITALIC = '/usr/share/fonts/truetype/noto/NotoSerifDisplay-Italic.ttf'
SANS = '/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf'
SANS_BLACK = '/usr/share/fonts/truetype/noto/NotoSansDisplay-Black.ttf'
MONO = '/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf'
PERFORATION_X = 1190
VALUE_RIGHT = 1150

def font(path, size):
    return ImageFont.truetype(path, size)

def center(draw, xy, text, f, fill, anchor='mm'):
    draw.text(xy, text, font=f, fill=fill, anchor=anchor)

def ghost(draw, cx, cy, scale, outline=(5, 8, 15), coin=True):
    w, h = int(110*scale), int(135*scale)
    x0, y0 = cx-w//2, cy-h//2
    draw.ellipse((x0, y0, x0+w, y0+int(h*.83)), fill='white', outline=outline, width=max(3,int(7*scale)))
    draw.rectangle((x0, y0+int(h*.42), x0+w, y0+int(h*.77)), fill='white')
    pts=[(x0,y0+int(h*.73))]
    for i in range(4):
        a=x0+i*w/4
        pts += [(a+w/8,y0+h),(a+w/4,y0+int(h*.73))]
    draw.line(pts, fill=outline, width=max(3,int(7*scale)), joint='curve')
    draw.line((x0,y0+int(h*.45),x0,y0+int(h*.73)), fill=outline,width=max(3,int(7*scale)))
    draw.line((x0+w,y0+int(h*.45),x0+w,y0+int(h*.73)), fill=outline,width=max(3,int(7*scale)))
    for ex in (cx-22*scale,cx+22*scale):
        ey=cy-14*scale; r=10*scale
        draw.polygon([(ex,ey-r),(ex+r*.48,ey),(ex,ey+r),(ex-r*.48,ey)], fill=outline)
    draw.ellipse((cx+w*.27,cy+3*scale,cx+w*.27+22*scale,cy+25*scale),fill='white',outline=outline,width=max(2,int(4*scale)))
    if coin:
        kx,ky=cx+w*.27+18*scale,cy+16*scale
        r=24*scale
        draw.ellipse((kx-r,ky-r,kx+r,ky+r),fill=MAGENTA,outline='white',width=max(2,int(4*scale)))
        star=[]
        for i in range(8):
            a=-math.pi/2+i*math.pi/4; rr=(12 if i%2==0 else 4)*scale
            star.append((kx+rr*math.cos(a),ky+rr*math.sin(a)))
        draw.polygon(star,fill='white')

def barcode(draw, x, y, width, height, seed):
    rng=random.Random(seed); pos=x
    while pos < x+width:
        bw=rng.choice([3,5,7,10,13])
        if pos+bw>x+width: break
        if rng.random()>.32: draw.rectangle((pos,y,pos+bw,y+height),fill=NAVY)
        pos+=bw+rng.choice([3,4,6])

def main():
    im=Image.new('RGB',(S,S),PAPER); px=im.load()
    for y in range(S):
        for x in range(S):
            d=math.sqrt(((x-800)/1150)**2+((y-760)/1150)**2)
            shade=max(0,min(1,(d-.48)*.10))
            px[x,y]=tuple(int(c*(1-shade)) for c in PAPER)
    d=ImageDraw.Draw(im,'RGBA')
    d.rectangle((36,36,1564,1564),outline=NAVY,width=10)
    d.rectangle((52,52,1548,1548),outline=GOLD,width=2)
    d.rectangle((62,62,1538,312),fill=NAVY)
    d.ellipse((82,69,318,305),fill=MAGENTA)
    ghost(d,200,187,1.33)
    d.text((342,125),'LEONIDA AIR',font=font(SERIF,79),fill=GOLD)
    d.text((347,226),'VICE CITY  ·  LEONIDA  ·  EST. 2013',font=font(SANS,31),fill=PAPER)
    d.text((1490,124),'BOARDING PASS',font=font(SANS,43),fill=PAPER,anchor='ra')
    d.text((1490,183),'ELECTRONIC TICKET',font=font(MONO,23),fill=GOLD,anchor='ra')
    d.rectangle((62,312,1538,364),fill=GOLD)
    center(d,(800,338),'PRIORITY BOARDING  —  13-YEAR WAIT RECOGNISED',font(SANS,27),NAVY)
    d.rectangle((PERFORATION_X,364,1538,1500),fill=(241,234,213))
    # perforation and notches
    for yy in range(380,1480,28): d.line((PERFORATION_X,yy,PERFORATION_X,yy+13),fill=(20,33,61,150),width=3)
    d.ellipse((1172,352,1208,388),fill=PAPER); d.ellipse((1172,1480,1208,1516),fill=PAPER)
    d.line((1172,370,1208,370),fill=GOLD,width=2); d.line((1172,1498,1208,1498),fill=GOLD,width=2)
    # Route block: the two loops are the visual punchline for the two delays.
    center(d,(145,478),'V',font(SERIF,205),NAVY)
    vi_pos, vi_font = (1080,478), font(SERIF,190)
    center(d,vi_pos,'VI',vi_font,NAVY)
    vi_left = d.textbbox(vi_pos,'VI',font=vi_font,anchor='mm')[0]
    arrow_tip = vi_left - 30
    loop_top, delay_y = 402, 385
    delay_font = font(MONO,20)
    delay_gaps = []
    for loop_x, label in ((465,'DELAY No. 1'),(715,'DELAY No. 2')):
        d.arc((loop_x-155,loop_top,loop_x+155,615),200,520,fill=GOLD,width=5)
        center(d,(loop_x,delay_y),label,delay_font,INKGREY)
        delay_gaps.append(loop_top - d.textbbox((loop_x,delay_y),label,font=delay_font,anchor='mm')[3])
    d.line((390,500,arrow_tip-29,500),fill=GOLD,width=4)
    d.polygon([(arrow_tip,500),(arrow_tip-38,480),(arrow_tip-29,500),(arrow_tip-38,520)],fill=NAVY)
    d.text((75,590),'LOS SANTOS',font=font(SANS,35),fill=NAVY)
    d.text((75,636),'17 SEP 2013  ·  09:00',font=font(MONO,25),fill=INKGREY)
    d.text((865,590),'LEONIDA',font=font(SANS,35),fill=NAVY)
    d.text((800,636),'19 NOV 2026  ·  00:01',font=font(MONO,25),fill=INKGREY)

    rows=[
        ('PASSENGER','ONE PATIENT GAMER'),('FLIGHT','LA 2013'),
        ('SEAT','13A  ·  HELD SINCE 2013'),('STATUS','DELAYED 4,811 DAYS'),
        ('BAGGAGE','214 GB  ·  CLEARED'),('ENTERTAINMENT','TRAILER 2 · 87 TIMES'),
        ('SICK DAYS','5  ·  DOCTOR APPROVED')]
    label_font, value_font = font(SANS,20), font(MONO,30)
    value_positions = []
    for y, (label,value) in zip(range(730,730+56*len(rows),56),rows):
        label_pos, value_pos = (78,y), (VALUE_RIGHT,y-8)
        d.text(label_pos,label,font=label_font,fill=INKGREY)
        d.text(value_pos,value,font=value_font,fill=NAVY,anchor='ra')
        label_right = d.textbbox(label_pos,label,font=label_font)[2]
        value_box = d.textbbox(value_pos,value,font=value_font,anchor='ra')
        for dot_x in range(label_right+16,value_box[0]-16,8):
            d.ellipse((dot_x,y+19,dot_x+2,y+21),fill=(130,133,135,160))
        value_positions.append((label,value,value_box))
    d.line((75,1175,1145,1175),fill=GOLD,width=3)
    fare_boxes = {}
    for name, text, pos, face, fill in (
        ('FARE','FARE  $79.99',(80,1191),font(SERIF,36),NAVY),
        ('TAXES','TAXES: TWO DELAYS  —  WAIVED',(710,1201),font(MONO,21),INKGREY),
        ('TOTAL','TOTAL  $79.99',(80,1240),font(SERIF,40),NAVY),
    ):
        d.text(pos,text,font=face,fill=fill)
        fare_boxes[name] = d.textbbox(pos,text,font=face)

    stamp_sub_font = font(MONO,61)

    def stamp(text, sub, xy, color, angle, width):
        layer = Image.new('RGBA',(width,100))
        stamp_draw = ImageDraw.Draw(layer)
        stamp_draw.rounded_rectangle((3,3,width-4,96),radius=15,outline=color,width=4)
        stamp_draw.rounded_rectangle((9,9,width-10,90),radius=10,outline=color,width=2)
        stamp_draw.text((width//2,14),text,font=font(SANS,29),fill=color,anchor='mt')
        stamp_draw.text((width//2,39),sub,font=stamp_sub_font,fill=color,anchor='mt')
        layer = layer.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        left, top = xy[0]-layer.width//2, xy[1]-layer.height//2
        im.paste(layer,(left,top),layer)
        xmin, ymin, xmax, ymax = layer.getchannel('A').getbbox()
        return left+xmin, top+ymin, left+xmax, top+ymax

    stamp_boxes = {
        'LANDED': stamp('LANDED','19 NOV 2026',(278,1361),GREEN,-1,432),
        'PAID BY MY AI AGENT': stamp('PAID BY MY AI AGENT','EARNED ON MAKE.FUN',(830,1361),MAGENTA,1,692),
    }

    center(d,(1365,430),'LEONIDA AIR',font(SANS,25),NAVY)
    ghost(d,1365,520,.55)
    stub=[('V → VI',650),('SEAT 13A',735),('GATE 6',820),('BOARD 00:01',905),('GROUP: LAST',990)]
    for value, yy in stub: center(d,(1365,yy),value,font(MONO,25),NAVY)
    barcode(d,1235,1080,260,100,613)
    center(d,(1365,1210),'VI·2013·2026',font(MONO,20),NAVY)
    separator_y = 1432
    d.line((75,separator_y,1145,separator_y),fill=GOLD,width=2)
    barcode(d,90,1440,1020,26,2013)
    barcode_caption = 'VI 2013 2026  ·  4,811 DAYS  ·  SEAT 13A'
    caption_pos, caption_font = (600,1480), font(MONO,24)
    center(d,caption_pos,barcode_caption,caption_font,NAVY)
    barcode_band = (75,separator_y,1146,d.textbbox(caption_pos,barcode_caption,font=caption_font,anchor='mm')[3])

    footer = '13 years at the gate. My agent paid for the seat.'
    footer_pos, footer_font = (600,1505), font(ITALIC,31)
    center(d,footer_pos,footer,footer_font,NAVY)
    footer_box = d.textbbox(footer_pos,footer,font=footer_font,anchor='mm')
    tagline = 'MAKE.FUN  —  WHERE PEOPLE AND THEIR AI AGENTS EARN REAL MONEY'
    tagline_font, tracking = font(SANS_BLACK,22), 1.5
    tagline_width = sum(tagline_font.getlength(char) for char in tagline) + tracking*(len(tagline)-1)
    tagline_x = 600 - tagline_width/2
    tagline_boxes = []
    for char in tagline:
        pos = (round(tagline_x),1537)
        d.text(pos,char,font=tagline_font,fill=NAVY,anchor='lm')
        tagline_boxes.append(d.textbbox(pos,char,font=tagline_font,anchor='lm'))
        tagline_x += tagline_font.getlength(char) + tracking

    im.save('meme.png',quality=95)
    preview_path = '/tmp/gta6-meme-x-01-r2-preview.png'
    with Image.open('meme.png') as check:
        assert check.size == (1600,1600), check.size
        print(f'meme.png: {check.width}x{check.height}')
        check.resize((480,480),Image.Resampling.LANCZOS).save(preview_path)
    for label, value, box in value_positions:
        width = value_font.getlength(value)
        start = VALUE_RIGHT - width
        assert 700 <= start and 700 <= box[0] and box[2] <= VALUE_RIGHT < PERFORATION_X, (label,box)
        print(f'{label}: width={width:.2f}, x={start:.2f}..{VALUE_RIGHT}, text box={box}')
    print(f'Fare and total boxes: {fare_boxes}; barcode band: {barcode_band}')
    footer_top = min(footer_box[1], *(box[1] for box in tagline_boxes))

    def intersects(first, second):
        return first[0] < second[2] and first[2] > second[0] and first[1] < second[3] and first[3] > second[1]

    for name, box in stamp_boxes.items():
        total_gap = box[1] - fare_boxes['TOTAL'][3]
        separator_gap = barcode_band[1] - box[3]
        assert all(not intersects(box,text_box) for text_box in fare_boxes.values()), (name,box)
        assert not intersects(box,barcode_band) and box[2] <= PERFORATION_X-15, (name,box)
        assert total_gap >= 15 and separator_gap >= 15 and box[3] < footer_top, (name,box)
        print(f'{name}: stamp box={box}, TOTAL gap={total_gap}px, separator gap={separator_gap}px')
    cap_top, cap_bottom = stamp_sub_font.getbbox('H')[1::2]
    cap_height = cap_bottom - cap_top
    assert cap_height >= 44 and min(delay_gaps) > 0
    print(f'Stamp subline cap height: {cap_height}px ({cap_height*480/S:.1f}px at 480)')
    print(f'Barcode caption: 18 -> 24px (+33.3%); footer: 16 -> 22px (+37.5%), black weight, 1.5px tracking')
    print(f'Header disc: 192 -> 236px (+{(236/192-1)*100:.1f}%); ghost: 1.08 -> 1.33 (+{(1.33/1.08-1)*100:.1f}%)')
    print(f'Delay label gaps: {delay_gaps}px; arrow-to-VI gap: {vi_left-arrow_tip}px')
    with Image.open(preview_path) as preview:
        assert preview.size == (480,480), preview.size
        print(f'Preview: {preview_path}, {preview.width}x{preview.height}')

if __name__ == '__main__':
    main()
