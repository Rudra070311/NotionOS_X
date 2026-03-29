import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.image_tool import ImageTool, show_content_gallery

async def demo_create_thumbnail():
    print("\n" + "="*80)
    print("DEMO 1: CREATE & DISPLAY THUMBNAIL")
    print("="*80)
    
    tool = ImageTool()
    task_id = "viral_video_001"
    
    thumbnail = tool.create_sample_image(task_id, "thumbnail")
    
    print(f"\n✅ Thumbnail created: {thumbnail.filename}")
    print(f"   Path: {thumbnail.path}")
    print(f"   Size: {thumbnail.size_bytes} bytes")
    
    print(tool.display_image(thumbnail))

async def demo_generate_assets():
    print("\n" + "="*80)
    print("DEMO 2: GENERATE COMPLETE ASSET PACKAGE")
    print("="*80)
    
    task_id = "ai_safety_campaign"
    
    print(f"\n🎬 Generating assets for: {task_id}")
    print("   • Thumbnail design")
    print("   • Storyboard layout")
    print("   • Video mockup")
    
    show_content_gallery(task_id)

async def demo_list_images():
    print("\n" + "="*80)
    print("DEMO 3: LIST ALL GENERATED IMAGES")
    print("="*80)
    
    tool = ImageTool()
    
    all_images = tool.list_images()
    
    print(f"\n📁 Total images in gallery: {len(all_images)}")
    print("\nGrouped by Task:")
    
    tasks = {}
    for img in all_images:
        task_id = img.task_id or "unassigned"
        if task_id not in tasks:
            tasks[task_id] = []
        tasks[task_id].append(img)
    
    for task_id, images in sorted(tasks.items()):
        print(f"\n  {task_id}:")
        for img in images:
            print(f"    • {img.filename} ({img.size_bytes} bytes)")

async def demo_image_in_workflow():
    print("\n" + "="*80)
    print("DEMO 4: IMAGE GENERATION IN AI WORKFLOW")
    print("="*80)
    
    print("\n🤖 ORCHESTRATOR EXECUTING TASK: 'Create Marketing Campaign'")
    print("\nStep 1: Task Decomposition")
    print("  ✓ Research target audience")
    print("  ✓ Identify key messaging")
    print("  ✓ Plan distribution strategy")
    print("  → SUBTASK: Generate visual assets")
    
    print("\nStep 2: Agent Execution")
    print("  [Creative Director] Designing thumbnail...")
    
    tool = ImageTool()
    task_id = "marketing_campaign_2026"
    thumbnail = tool.create_sample_image(task_id, "thumbnail")
    
    print(f"  ✅ Thumbnail generated: {thumbnail.filename}")
    print(tool.display_image(thumbnail))
    
    print("  [Strategist] Creating storyboard...")
    storyboard = tool.create_sample_image(task_id, "storyboard")
    print(f"  ✅ Storyboard generated: {storyboard.filename}")
    print(tool.display_image(storyboard))
    
    print("\nStep 3: Quality Check")
    print("  [Quality Critic] 'Visual design follows brand guidelines' ✓")
    print("  [Creative Critic] 'Assets are high-engagement worthy' ✓")
    
    summary = tool.get_image_summary(task_id)
    print(f"\nStep 4: Summary")
    print(f"  Total Assets: {summary['total_images']}")
    print(f"  Total Size: {summary['total_size_kb']:.1f} KB")
    print(f"  Status: READY FOR DEPLOYMENT")

async def demo_multiple_formats():
    print("\n" + "="*80)
    print("DEMO 5: WORKING WITH MULTIPLE IMAGE TYPES")
    print("="*80)
    
    tool = ImageTool()
    task_id = "content_batch_001"
    
    print(f"\n📦 Batch Processing: {task_id}")
    
    image_types = ["thumbnail", "storyboard", "mockup"]
    
    for img_type in image_types:
        print(f"\n  Generating {img_type}...")
        image = tool.create_sample_image(task_id, img_type)
        print(f"  ✅ {image.filename}")
    
    print(f"\n📊 Final Summary:")
    summary = tool.get_image_summary(task_id)
    for img in summary['images']:
        print(f"  • {img['type']:12} - {img['size_kb']:6.1f} KB - {img['created']}")

async def main():
    print("\n" + "="*80)
    print("="*78 + "  ")
    print("==" + "  NOTIONOS X - IMAGE GENERATION & DISPLAY DEMO".center(76) + "==")
    print("="*78 + "  ")
    print("="*80)
    
    await demo_create_thumbnail()
    await demo_generate_assets()
    await demo_list_images()
    await demo_image_in_workflow()
    await demo_multiple_formats()
    
    print("\n" + "="*80)
    print("="*78 + "  ")
    print("==" + "  All demos completed successfully!".center(76) + "==")
    print("="*78 + "  ")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
