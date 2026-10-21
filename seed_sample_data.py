"""Seeds realistic portfolio-grade sample images into the platform library."""

from pathlib import Path
from PIL import Image

from backend.storage import StorageManager
from backend.local_editor import apply_preset_filter
from backend.config import SAMPLES_DIR, BASE_DIR

# Sample images included in assets/samples
SOURCE_IMAGES = [
    {
        "filename": "outdoor_portrait_creator.jpg",
        "title": "Sunlit Outdoor Creative Portrait",
        "caption": "A smiling young creative woman outdoors in an autumn park with warm golden hour backlighting, soft bokeh background greenery, and natural atmospheric depth.",
        "tags": ["portrait", "person", "woman", "smiling", "golden hour", "park", "outdoor", "bokeh", "autumn", "lifestyle"],
        "objects": ["young woman", "blazer", "leather backpack", "notebook", "foliage", "fountain"],
        "dominant_colors": ["Terracotta Orange", "Olive Green", "Warm Sunlight", "Deep Teal"],
        "sample_edit": ("golden_hour", "golden_hour", "Enhance with warm sunset golden hour lighting")
    },
    {
        "filename": "tropical_beach_sunset.jpg",
        "title": "Sunlit Tropical Beach Coast",
        "caption": "A breathtaking tropical beach bathed in radiant golden sunset light, with turquoise waves kissing fine white sand and graceful coconut palms leaning toward the ocean horizon.",
        "tags": ["beach", "tropical", "ocean", "sunset", "palm trees", "sand", "nature", "vacation", "golden hour", "waves"],
        "objects": ["coconut palm trees", "ocean waves", "sandy shoreline", "sunset sky", "distant hills"],
        "dominant_colors": ["Turquoise", "Golden Orange", "Warm Sand", "Azure Blue"],
        "sample_edit": ("enhance_clarity", "preset", "Remaster micro-contrast and vivid ocean tones")
    },
    {
        "filename": "artisanal_coffee_workspace.jpg",
        "title": "Artisanal Latte & Workspace",
        "caption": "An aesthetic top-down desktop scene featuring an artisanal latte with delicate swan latte art in a ceramic cup, next to an open notebook with handwritten reflections, tortoiseshell glasses, and a succulent.",
        "tags": ["coffee", "latte art", "workspace", "minimalist", "notebook", "glasses", "indoor", "succulent", "aesthetic", "cozy"],
        "objects": ["coffee cup", "saucer", "open notebook", "eyeglass frames", "potted succulent", "wooden tabletop"],
        "dominant_colors": ["Warm Oak Brown", "Cream Latte", "Sage Green", "Tortoiseshell"],
        "sample_edit": ("vintage_film", "preset", "Vintage 1970s analog 35mm film color grading")
    },
    {
        "filename": "golden_retriever_park.jpg",
        "title": "Playful Golden Retriever in Autumn",
        "caption": "A cheerful golden retriever sitting alert on vibrant green lawn grass in a sun-dappled park, surrounded by golden and russet autumn foliage and gentle afternoon sunlight.",
        "tags": ["dog", "golden retriever", "pet", "animal", "park", "autumn", "grass", "happy", "sunlight", "outdoor"],
        "objects": ["golden retriever dog", "collar", "green grass", "autumn trees", "park pathway"],
        "dominant_colors": ["Golden Fur", "Emerald Grass", "Amber Leaves", "Sky Blue"],
        "sample_edit": ("watercolor_art", "preset", "Convert to delicate watercolor illustration")
    }
]


def seed_library(clear_existing: bool = True):
    """Seed library with sample assets and pre-generated versions."""
    storage = StorageManager()
    if clear_existing:
        print("Clearing previous sample images to avoid duplicates...")
        for existing in storage.get_all_images():
            storage.delete_image(existing["id"])

    print("Seeding sample portfolio images...")

    for item in SOURCE_IMAGES:
        dest_sample = SAMPLES_DIR / item["filename"]

        if not dest_sample.exists():
            print(f"Warning: sample file not found at {dest_sample}, skipping.")
            continue

        target_image_path = dest_sample

        # Open image and add to storage manager
        with Image.open(target_image_path) as img:
            record = storage.add_original_image(
                pil_image=img,
                filename=item["filename"],
                title=item["title"],
                caption=item["caption"],
                tags=item["tags"],
                objects=item["objects"],
                dominant_colors=item["dominant_colors"]
            )
            print(f"Added original image: {record['title']} (ID: {record['id']})")

            # Apply sample edit to populate version history
            if "sample_edit" in item:
                preset_key, edit_type, prompt_desc = item["sample_edit"]
                edited_pil = apply_preset_filter(img, preset_key)
                storage.add_version(
                    image_id=record["id"],
                    edited_image=edited_pil,
                    prompt=prompt_desc,
                    edit_type=edit_type,
                    model_used=f"Smart Vision Engine ({preset_key})",
                    notes=f"Sample visual transformation ({preset_key})"
                )
                print(f"  -> Added version v1: {prompt_desc}")

    print("Seeding complete! Metadata and versions generated successfully.")


if __name__ == "__main__":
    seed_library()
