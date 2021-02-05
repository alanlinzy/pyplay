import os,sys
import cv2
import qrcode

#import qrcode.image.svg#矢量
from pyzbar import pyzbar
from PIL import Image,ImageChops,ImageDraw,ImageEnhance,ImageFilter

#img = qrcode.make("lzy info")
#img.save("info_qr.png")

'''
qr = qrcode.QRCode(
    version = 10,#版本1-40
    error_correction = qrcode.constants.ERROR_CORRECT_L,#纠错级别
    box_size = 10,#像素
    border = 8,#边框
    )
qr.add_data("new lzy info")
qr.make(fit=True)
img = qr.make_image()
img.save("new_info_qr.png")
'''
'''
img = Image.open("info_qr.png")
img_dup = ImageChops.duplicate(img)
print(img_dup.mode)
img_diff = ImageChops.difference(img,img_dup)
draw = ImageDraw.Draw(img)
draw.line((0,0)+img.size, fill=128)
'''


def gen_qr(info,path,logo=""):
    qr = qrcode.QRCode(
        version = 2,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 8,
        border = 1,
        )
    qr.add_data(info)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")
    if logo and os.path.exists(logo):
        try:
            icon = Image.open(logo)
            img_w,img_h = img.size
        except Exception as e:
            print(e)
            sys.exit(0)
        factor =4
        #计算logo尺寸
        size_w = int(img_w/factor)
        size_h = int(img_h/factor)
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w,icon_h),Image.ANTIALIAS)
        x = int((img_w-icon_w)/2)
        y = int((img_h-icon_h)/2)
        icon = icon.convert("RGBA")
        img.paste(icon,(x,y),icon)
        img.save(path)
info = "add icon info qr"
pic_path = "add_icon_qr.png"
logo = "Hokusai.png"
gen_qr(info,pic_path,logo)

def decode_qr(path):
    img = Image.open(path)
    return pyzbar.decode(img,symbols=[pyzbar.ZBarSymbol.QRCODE])

results = decode_qr(pic_path)
if len(results):
    print(results[0].data.decode("utf8"))
else:
    print("can't recognize")



def decodeDisplay(image):
    barcodes = pyzbar.decode(image)
    status = False
    for barcode in barcodes:
        # 提取二维码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)

        # 提取二维码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (225, 225, 225), 2)

        # 向终端打印条形码数据和条形码类型
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        status = True
    return image,status


def detect():
    camera = cv2.VideoCapture(1)

    while True:
        # 读取当前帧
        ret, frame = camera.read()
        # 转为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        im,status = decodeDisplay(gray)

        cv2.waitKey(5)
        cv2.imshow("camera", im)
        # 如果按键q则跳出本次循环
        if cv2.waitKey(10) & 0xFF == ord('q') or status == True:
            break
    camera.release()
    cv2.destroyAllWindows()
    
detect()
