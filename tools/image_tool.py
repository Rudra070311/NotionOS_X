import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class ImageMetadata:
    filename: str
    path: str
    size_bytes: int
    format: str
    width: Optional[int] = None
    height: Optional[int] = None
    description: str = ""
    task_id: str = ""
    created_at: str = ""

class ImageTool:

    def __init__(self, image_dir: str = "images"):
        self.image_dir = image_dir
        self.metadata_file = os.path.join(image_dir, "image_metadata.json")
        
        os.makedirs(image_dir, exist_ok=True)
        self._load_metadata()

    def _load_metadata(self):
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except:
                self.metadata = []
        else:
            self.metadata = []

    def _save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def create_sample_image(self, task_id: str, image_type: str = "thumbnail") -> ImageMetadata:
        os.makedirs(self.image_dir, exist_ok=True)
        
        filename = f"{image_type}_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.image_dir, filename)
        
        image_content = self._generate_image_content(image_type)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(image_content)
        
        file_size = os.path.getsize(filepath)
        
        metadata = {
            "filename": filename,
            "path": filepath,
            "size_bytes": file_size,
            "format": "ascii_art",
            "width": 60,
            "height": 20,
            "description": f"Generated {image_type} for task {task_id}",
            "task_id": task_id,
            "created_at": datetime.now().isoformat()
        }
        
        self.metadata.append(metadata)
        self._save_metadata()
        
        return ImageMetadata(**metadata)

    def _generate_image_content(self, image_type: str) -> str:
        if image_type == "thumbnail":
            return """
    +=============================================================+
    |                     THUMBNAIL DESIGN                        |
    |                                                              |
    |                  +-------+  +-------+                        |
    |                  |   AI  |  |SAFETY |                        |
    |                  +-------+  +-------+                        |
    |                                                              |
    |              VIRAL VIDEO CONCEPT                            |
    |         "The AI Safety Crisis Nobody Talks About"           |
    |                                                              |
    |            [Trending on YouTube - Potential]                |
    |                                                              |
    |    Design Elements:                                         |
    |    • Bold red warning icon (top-left)                       |
    |    • Gen-Z color palette (neon + dark)                      |
    |    • Intriguing question in 72pt font                       |
    |    • Creator face (speaking pose)                           |
    |                                                              |
    +=============================================================+
            """
        elif image_type == "storyboard":
            return """
    +=============================================================+
    |                      STORYBOARD LAYOUT                      |
    |                                                              |
    |  Scene 1: Hook         Scene 2: Setup                       |
    |  +--------+            +--------+                           |
    |  | SHOCK  |  FAST CUT  | REALITY|                           |
    |  +--------+            +--------+                           |
    |                                                              |
    |  Scene 3: Conflict     Scene 4: Resolution                  |
    |  +--------+            +--------+                           |
    |  |TENSION |  DEBATE    |SOLUTION|                           |
    |  +--------+            +--------+                           |
    |                                                              |
    |  Pacing: 2s, 3s, 5s, 4s                                    |
    |  Total Duration: 14 seconds (SHORT + ENGAGING)              |
    |                                                              |
    +=============================================================+
            """
        elif image_type == "mockup":
            return """
    +=============================================================+
    |                  VIDEO MOCKUP PREVIEW                       |
    |                                                              |
    |              FRAME 1 (0:00-0:02s)                           |
    |                                                              |
    |        [TITLE CARD - RED BACKGROUND]                        |
    |                                                              |
    |        "Your AI Isn't What You Think"                       |
    |                                                              |
    |        [Fade to presenter]                                  |
    |        "Most people don't realize one thing..."             |
    |                                                              |
    |        [B-roll: AI generated content]                       |
    |                                                              |
    |        [Cut to interview soundbite]                         |
    |        Expert: "The alignment problem is critical"          |
    |                                                              |
    |        [Conclude with call-to-action]                       |
    |        "Subscribe to understand the future of AI"           |
    |                                                              |
    +=============================================================+
            """
        else:
            return """
    +=============================================================+
    |                    DEFAULT IMAGE ASSET                      |
    |                                                              |
    |                    NO IMAGE SET                             |
    |                                                              |
    |              Use image_tool.display_image()                 |
    |                   to show content                           |
    |                                                              |
    +=============================================================+
            """

    def display_image(self, image_metadata: ImageMetadata) -> str:
        if not os.path.exists(image_metadata.path):
            return f"Error: Image not found at {image_metadata.path}"
        
        try:
            with open(image_metadata.path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            output = []
            output.append("\n" + "="*80)
            output.append(f"FRAME: {image_metadata.filename}")
            output.append(f"   Task ID: {image_metadata.task_id}")
            output.append(f"   Created: {image_metadata.created_at}")
            output.append(f"   Size: {image_metadata.size_bytes} bytes")
            output.append("="*80)
            output.append(content)
            output.append("="*80 + "\n")
            
            return "\n".join(output)
        except Exception as e:
            return f"Error reading image: {str(e)}"

    def list_images(self, task_id: Optional[str] = None) -> List[ImageMetadata]:
        images = []
        for meta in self.metadata:
            if task_id is None or meta.get("task_id") == task_id:
                images.append(ImageMetadata(**meta))
        return images

    def delete_image(self, filename: str) -> bool:
        try:
            for i, meta in enumerate(self.metadata):
                if meta["filename"] == filename:
                    filepath = meta["path"]
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    self.metadata.pop(i)
                    self._save_metadata()
                    return True
            return False
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False

    def get_image_summary(self, task_id: str) -> Dict:
        task_images = [m for m in self.metadata if m.get("task_id") == task_id]
        
        return {
            "task_id": task_id,
            "total_images": len(task_images),
            "images": [
                {
                    "filename": img["filename"],
                    "type": img["filename"].split("_")[0],
                    "size_kb": img["size_bytes"] / 1024,
                    "created": img["created_at"]
                }
                for img in task_images
            ],
            "total_size_kb": sum(img["size_bytes"] for img in task_images) / 1024
        }

def show_content_gallery(task_id: str):
    tool = ImageTool()
    
    print("\n" + "="*80)
    print(f"CONTENT GALLERY FOR TASK: {task_id}")
    print("="*80)
    
    thumbnail = tool.create_sample_image(task_id, "thumbnail")
    storyboard = tool.create_sample_image(task_id, "storyboard")
    mockup = tool.create_sample_image(task_id, "mockup")
    
    print(tool.display_image(thumbnail))
    print(tool.display_image(storyboard))
    print(tool.display_image(mockup))
    
    summary = tool.get_image_summary(task_id)
    print("\n" + "="*80)
    print("CONTENT SUMMARY")
    print("="*80)
    print(f"Total Assets Generated: {summary['total_images']}")
    print(f"Total Size: {summary['total_size_kb']:.1f} KB")
    print("\nAssets:")
    for img in summary['images']:
        print(f"  • {img['filename']} ({img['type']}) - {img['size_kb']:.1f} KB")
    print("="*80 + "\n")
    
    return summary
