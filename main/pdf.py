from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from PIL import Image, ImageDraw
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from textwrap import wrap
from os import remove

def create(users, path):
    if users is not None:
        try:
            image = Image.open(users["photo"]+".jpg")
            rounded_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(rounded_image)
            center_x = image.width // 2
            center_y = image.height // 2
            radius = min(center_x, center_y)
            draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=(255, 255, 255))
            mask = Image.new("L", image.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
            rounded_image.paste(image, (0, 0), mask=mask)
            rounded_image.save(users["photo"]+".png")
        except:
            pass
        pdfmetrics.registerFont(TTFont('TR', 'main/storage/font/calibri.ttf'))
        canvas = Canvas(path, pagesize=A4)

        canvas.setFont("TR", 26)
        canvas.drawString(25, 800, users["name"])

        canvas.line(25, 790, 700, 790)
        try:
            canvas.drawInlineImage(users["photo"]+".png", 25, 630, 150, 150)
        except:
            pass

        canvas.setFont("TR", 20)
        canvas.drawString(25, 600, "CONTACT INFO")
        canvas.setFont("TR", 16)

        canvas.drawString(33, 576.5, "Email: " + users["email"])
        canvas.drawInlineImage("main/storage/pictures/mail.png", 20, 577, 10, 10)
        canvas.drawString(33, 546.5, "Phone: " + users["phone"])
        canvas.drawInlineImage("main/storage/pictures/phone.png", 20, 547, 10, 10)
        canvas.drawString(33, 516.5, "City: " + users["city"])
        canvas.drawInlineImage("main/storage/pictures/geo.png", 20, 517, 10, 10)
        canvas.drawString(23, 486.5, "Goal: " + users["goal"])

        canvas.setFont("TR", 20)
        canvas.drawString(225, 700, "EDUCATION")

       
        canvas.setFont("TR", 16)
        canvas.drawString(226, 680, users["education"])

        canvas.setFont("TR", 20)
        canvas.drawString(225, 600, "EXPERIENCE")

        canvas.setFont("TR", 16)
        canvas.drawString(226, 580, users["expierence"])


        canvas.setFont("TR", 20)
        canvas.drawString(225, 500, "HARD SKILLS")

        canvas.setFont("TR", 16)
        canvas.drawString(226, 480, users["hardSkills"])

        canvas.setFont("TR", 20)
        canvas.drawString(225, 400, "SOFT SKILLS")

        canvas.setFont("TR", 16)
        canvas.drawString(226, 380, users["softSkills"])

        canvas.setFont("TR", 20)
        canvas.drawString(225, 300, "ADDITIONAL INFO")

        canvas.setFont("TR", 16)
        canvas.drawString(226, 280, users["addInfo"])  

        canvas.save()

        try:
            remove(users["photo"]+".png")
        except:
            pass