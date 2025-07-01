
from langchain_community.document_loaders import PyMuPDFLoader
from utils.llm import get_response, get_llm
from PIL import Image
import fitz
import json
import datetime
import os

class ResumeLoader:    
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.file_name = os.path.basename(file_path)
        self.cache_dir = os.path.dirname(file_path)
        
    def update_time(self, key):
        with open(os.path.join(self.cache_dir, 'datetime.json'), 'r') as f:
                original_js = json.loads(f.read())
        original_js[key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(os.path.join(self.cache_dir, 'datetime.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(original_js, indent=4))
        
    @property
    def content(self):
        content_file_path = os.path.join(self.cache_dir, 'content.txt')
        if os.path.exists(content_file_path):
            with open(content_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            loader = PyMuPDFLoader(self.file_path)
            pages = loader.load()
            content = ''
            for page in pages:
                content += page.page_content
            
            with open(os.path.join(self.cache_dir, 'content.txt'), 'w', encoding='utf-8') as f:
                f.write(content)
            self.update_time('content')
            return content
        
    @property        
    def summary(self, max_length=2048, api_key=None, base_url=None):
        summary_file_path = os.path.join(self.cache_dir,'summary.md')
        if os.path.exists(summary_file_path):
            with open(summary_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            prompt = (
                "请你根据用户的简历，生成简历摘要，要求提取出以下内容"
                "1. 教育背景，包括学校以及专业"
                "2. 工作经验，即工作时间为几年"
                "3. 工作技能，从校内、实习、工作项目、经历或其他地方提取出掌握的所有技能"
                "4. 对每一个项目进行总结"
                "输出格式要求：按照markdown格式输出，只输出摘要，不要返回其他内容"
                "用户简历\n{content}"
            )
            messages = [
                {"role": "system", "content": "你是一个智能的简历生成助手，能够根据用户的简历生成简历摘要。"},
                {"role": "user", "content": prompt.format(content=self.content)},
            ]
            LLM = get_llm(api_key=api_key, base_url=base_url)
            response = get_response(LLM, messages, max_tokens=max_length)
            with open(os.path.join(self.cache_dir,'summary.md'), 'w', encoding='utf-8') as f:
                f.write(response)
            self.update_time('summary')
            return response
    
    @property
    def picture_path(self):
        # 如果没有图片，则将pdf转换为一张图片，返回图片路径
        final_image_path = os.path.join(self.cache_dir, 'cv.png')
        
        if not os.path.exists(final_image_path):
            pdfDoc = fitz.open(self.file_path)
            images = []
            
            for pg in range(pdfDoc.page_count):
                page = pdfDoc[pg]
                zoom_x, zoom_y = 3, 3
                mat = fitz.Matrix(zoom_x, zoom_y)
                pix = page.get_pixmap(matrix=mat, alpha=False)

                # 通过内存直接转成PIL
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
            
            pdfDoc.close()
            
            # 纵向拼接
            total_height = sum(img.height for img in images)
            max_width = max(img.width for img in images)
            
            new_img = Image.new("RGB", (max_width, total_height), (255,255,255))
            
            y_offset = 0
            for img in images:
                new_img.paste(img, (0, y_offset))
                y_offset += img.height
            
            new_img.save(final_image_path)
            self.update_time('picture')
            
        return final_image_path