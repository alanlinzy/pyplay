import random, string, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
font_path = "C:\\Windows\Fonts\simfang.ttf"
number = 4
size = (80,30)
bgcolor = (255,255,255)
fontcolor = (0,0,255)
linecolor = (255,0,0)
draw_line = True
line_num = random.randint(4,10)

def gen_txt():
    #source = list(string.letters)
    source = list(string.ascii_letters)
    for i in range(10):
        source.append(str(i))
    return ''.join(random.sample(source,number))

def gen_line(draw,w,h):
    begin = (random.randint(0,w),random.randint(0,h))
    end = (random.randint(0,w),random.randint(0,h))
    draw.line((begin,end), fill = linecolor)

def gen_code():
    w,h = size
    image = Image.new('RGBA',(w,h),bgcolor)
    font = ImageFont.truetype(font_path,25)#字体
    draw = ImageDraw.Draw(image)
    text = gen_txt()
    font_w, font_h = font.getsize(text)
    draw.text(((w-font_w)/number,(h-font_h)/number),
              text, font = font, fill = fontcolor)
    if draw_line:
        for i in range(line_num):
            gen_line(draw,w,h)
    image = image.transform((w+20,h+10), Image.AFFINE,
                            (1,-0.3,0,-0.1,1,0), Image.BILINEAR)
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    image.save("cap.png")

gen_code()
    
