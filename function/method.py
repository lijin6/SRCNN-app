import os
import torch
import numpy as np
from PIL import Image
from datetime import datetime
from werkzeug.utils import secure_filename
from .SRCNN import SRCNN
from .utils import convert_rgb_to_ycbcr, convert_ycbcr_to_rgb
import uuid


class ImageProcessor:
    def __init__(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.models = self._load_models()
        
    def _load_models(self):
        models = {
            'x2': torch.load('checkpoints/srcnn_x2.pth', map_location=self.device),
            'x3': torch.load('checkpoints/srcnn_x3.pth', map_location=self.device),
            'x4': torch.load('checkpoints/srcnn_x4.pth', map_location=self.device)
        }
        for key in models:
            model = SRCNN().to(self.device)
            model.load_state_dict(models[key])
            model.eval()
            models[key] = model
        return models
    
    @staticmethod
    def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'bmp'}):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def generate_filename(original_filename):
        return secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}_{original_filename}")
    
    def process_image(self, image_path, scale, output_folder):
        # 验证缩放比例是否有效
        if scale not in self.models:
            raise ValueError(f"无效的缩放比例: {scale}")
            
        # 读取并处理图像
        image = Image.open(image_path).convert('RGB')
        image = np.array(image).astype(np.float32)
        ycbcr = convert_rgb_to_ycbcr(image)
        
        # 处理Y通道
        y = ycbcr[..., 0] / 255.
        y = torch.from_numpy(y).to(self.device).unsqueeze(0).unsqueeze(0)
        
        # 使用模型进行超分辨率
        with torch.no_grad():
            preds = self.models[scale](y).clamp(0.0, 1.0)
        preds = preds.mul(255.0).cpu().numpy().squeeze(0).squeeze(0)
        
        # 合并通道并转换回RGB
        output = np.array([preds, ycbcr[..., 1], ycbcr[..., 2]]).transpose([1, 2, 0])
        output = np.clip(convert_ycbcr_to_rgb(output), 0.0, 255.0).astype(np.uint8)
        output_image = Image.fromarray(output)
        
        # 保存输出图像
        original_name = os.path.splitext(os.path.basename(image_path))[0]
        output_filename = f"{original_name}_SRCNN_{scale}.png"
        output_path = os.path.join(output_folder, output_filename)
        output_image.save(output_path)
        
        return output_path
    
    def get_history(self, upload_folder, output_folder, limit=10):
        # 获取上传历史
        upload_files = sorted(
            [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))],
            key=lambda x: os.path.getmtime(os.path.join(upload_folder, x)), reverse=True
        )
        
        # 获取输出历史
        output_files = sorted(
            [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))],
            key=lambda x: os.path.getmtime(os.path.join(output_folder, x)), reverse=True
        )
        
        # 处理上传文件信息
        uploads = []
        for f in upload_files[:limit]:
            uploads.append({
                'name': f,
                'path': os.path.join(upload_folder, f),
                'date': datetime.fromtimestamp(os.path.getmtime(os.path.join(upload_folder, f))).strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # 处理输出文件信息
        outputs = []
        for f in output_files[:limit]:
            outputs.append({
                'name': f,
                'path': os.path.join(output_folder, f),
                'date': datetime.fromtimestamp(os.path.getmtime(os.path.join(output_folder, f))).strftime('%Y-%m-%d %H:%M:%S')
            })
            
        return uploads, outputs