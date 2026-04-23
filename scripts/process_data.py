import os
import json
from PIL import Image

# 配置路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_dir = os.path.join(base_dir, 'images')
json_path = os.path.join(base_dir, 'data.json')

def process():
    print("开始处理数据...")

    # 1. 扫描并处理图片
    valid_images = {} # 存储 id: filename
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            name_part = os.path.splitext(filename)[0]
            # 尝试提取 ID
            try:
                card_id = int(name_part)
                img_path = os.path.join(image_dir, filename)
                
                # 统一转换格式并缩放（可选）
                with Image.open(img_path) as img:
                    img = img.convert('RGB')
                    # 统一保存为 jpg，质量 85
                    new_filename = f"{card_id}.jpg"
                    img.save(os.path.join(image_dir, new_filename), 'JPEG', quality=85)
                    valid_images[card_id] = f"./images/{new_filename}"
                
                # 如果原文件后缀不是 .jpg，删除旧文件
                if filename != new_filename:
                    os.remove(img_path)
            except ValueError:
                print(f"忽略非数字命名的文件: {filename}")

    # 2. 更新 JSON
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for card in data['cards']:
            card_id = card['id']
            if card_id in valid_images:
                card['image_url'] = valid_images[card_id]
                print(f"已匹配卡片 {card_id} 的本地图片")
            else:
                card['image_url'] = "" # 没图的清空链接
                print(f"警告：未找到卡片 {card_id} 的对应图片")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print("处理完成！你可以刷新网页看效果了。")

if __name__ == "__main__":
    process()