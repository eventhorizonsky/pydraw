from PIL import Image, ImageDraw, ImageFont

def create_image_with_text(text, title, img_width, img_height):
    # 创建一个透明背景的图片
    image = Image.new("RGBA", (img_width, img_height), (255, 255, 255, 0))  # 透明背景
    draw = ImageDraw.Draw(image)

    # 设置字体和大小
    try:
        # 替换为你的中文字体文件路径
        font_path = "SourceHanSerifSC-Bold.ttf"
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        font = ImageFont.load_default()

    # 获取文本的边界框
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 计算文本位置，使其居中
    text_x = (img_width - text_width) / 2
    text_y = (img_height - text_height) / 2
    baseline_offset = -3
    text_y += baseline_offset

    # 绘制紫色描边
    outline_color = (28, 24, 128, 255)  # 加入Alpha通道
    for offset in [-1, 1, 1]:  # 描边效果
        draw.text((text_x + offset, text_y), text, font=font, fill=outline_color)
        draw.text((text_x, text_y + offset), text, font=font, fill=outline_color)

    # 绘制字符本体，颜色为纯白
    draw.text((text_x, text_y), text, font=font, fill=(200, 200, 200, 255))

    # 获取图像数据
    image.save(title + ".bmp")
    outline_pixels = image.getdata()

    # 创建遮罩，包含字符本体和描边区域
    special_mask = Image.new("L", image.size, 0)
    mask_pixels = special_mask.load()

    # 设置描边部分为255
    for y in range(img_height):
        for x in range(img_width):
            pixel = outline_pixels[y * img_width + x]
            if pixel[:3] == outline_color[:3]:  # 检测描边颜色，不考虑alpha
                mask_pixels[x, y] = 255

    # 确保字符本体区域准确为0
    for y in range(img_height):
        for x in range(img_width):
            if outline_pixels[y * img_width + x] == (255, 255, 255, 255):  # 检测白色本体
                mask_pixels[x, y] = 0

    # 创建一个特殊图像，仅保留描边遮罩
    special_image = Image.new("RGBA", (img_width, img_height), (255, 0, 0, 0))
    special_image.putalpha(special_mask)
    special_image.save(title + "_special.bmp")


# 示例调用
img_width = 280
img_height = 24
create_image_with_text("你好，世界", "C_OLF00_frame_0_palette_12_position_65396", img_width, img_height)
