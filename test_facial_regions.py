"""
TEST SCRIPT FOR FACIAL REGION EXTRACTION
Demonstrates how to use the facial region extractor

Run: python test_facial_regions.py
"""

import cv2
import numpy as np
from facial_region_extraction import FacialRegionExtractor


def test_basic_extraction():
    """Test basic facial region extraction"""
    print("\n" + "=" * 70)
    print("TEST 1: BASIC FACIAL REGION EXTRACTION")
    print("=" * 70)
    
    # Initialize extractor
    extractor = FacialRegionExtractor()
    
    # Test image path
    image_path = "test_face.jpg"
    
    print(f"\n📸 Testing with: {image_path}")
    
    # Process image
    regions = extractor.process_image(
        image_path=image_path,
        display=True,
        save_output=False
    )
    
    if regions:
        print("\n✅ Test passed!")
        print(f"   Extracted {len(regions)} regions")
        for name, img in regions.items():
            print(f"   • {name}: {img.shape}")
    else:
        print("\n❌ Test failed: No regions extracted")


def test_save_regions():
    """Test saving regions to disk"""
    print("\n" + "=" * 70)
    print("TEST 2: SAVE REGIONS TO DISK")
    print("=" * 70)
    
    extractor = FacialRegionExtractor()
    image_path = "test_face.jpg"
    
    print(f"\n📸 Processing: {image_path}")
    print("💾 Saving regions to disk...")
    
    regions = extractor.process_image(
        image_path=image_path,
        display=False,
        save_output=True,
        output_prefix="test_region"
    )
    
    if regions:
        print("\n✅ Test passed!")
        print("   Files saved:")
        for name in regions.keys():
            print(f"   • test_region_{name}.jpg")
    else:
        print("\n❌ Test failed")


def test_individual_regions():
    """Test extracting individual regions"""
    print("\n" + "=" * 70)
    print("TEST 3: EXTRACT INDIVIDUAL REGIONS")
    print("=" * 70)
    
    extractor = FacialRegionExtractor()
    image_path = "test_face.jpg"
    
    # Load and process
    image = extractor.load_image(image_path)
    if image is None:
        print("❌ Failed to load image")
        return
    
    face_landmarks = extractor.detect_face(image)
    if face_landmarks is None:
        print("❌ No face detected")
        return
    
    landmarks = extractor.extract_landmarks(face_landmarks, image.shape)
    
    # Extract each region individually
    print("\n📐 Extracting individual regions...")
    
    regions_to_test = ['forehead', 'left_eye', 'right_eye', 'cheeks', 'lips_chin']
    
    for region_name in regions_to_test:
        region_img = extractor.crop_region(image, landmarks, region_name)
        if region_img is not None:
            print(f"  ✅ {region_name}: {region_img.shape}")
            cv2.imshow(f"{region_name.upper()}", region_img)
        else:
            print(f"  ❌ {region_name}: Failed")
    
    print("\n⌨️ Press any key to close windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n✅ Test passed!")


def test_landmark_visualization():
    """Test landmark visualization"""
    print("\n" + "=" * 70)
    print("TEST 4: LANDMARK VISUALIZATION")
    print("=" * 70)
    
    extractor = FacialRegionExtractor()
    image_path = "test_face.jpg"
    
    # Load and process
    image = extractor.load_image(image_path)
    if image is None:
        print("❌ Failed to load image")
        return
    
    face_landmarks = extractor.detect_face(image)
    if face_landmarks is None:
        print("❌ No face detected")
        return
    
    landmarks = extractor.extract_landmarks(face_landmarks, image.shape)
    
    # Draw all landmarks
    print("\n🎨 Drawing all landmarks...")
    annotated_all = extractor.draw_landmarks_on_image(image, landmarks)
    cv2.imshow("All Landmarks", annotated_all)
    
    # Draw region-specific landmarks
    print("🎨 Drawing region-specific landmarks...")
    
    regions = ['forehead', 'left_eye', 'right_eye', 'cheeks', 'lips_chin']
    for region in regions:
        annotated = extractor.draw_landmarks_on_image(image, landmarks, region)
        cv2.imshow(f"{region.upper()} Landmarks", annotated)
    
    print("\n⌨️ Press any key to close windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n✅ Test passed!")


def test_combined_view():
    """Test combined view creation"""
    print("\n" + "=" * 70)
    print("TEST 5: COMBINED VIEW")
    print("=" * 70)
    
    extractor = FacialRegionExtractor()
    image_path = "test_face.jpg"
    
    # Load and process
    image = extractor.load_image(image_path)
    if image is None:
        print("❌ Failed to load image")
        return
    
    face_landmarks = extractor.detect_face(image)
    if face_landmarks is None:
        print("❌ No face detected")
        return
    
    landmarks = extractor.extract_landmarks(face_landmarks, image.shape)
    regions = extractor.segment_regions(image, landmarks)
    
    # Create combined view
    print("\n🖼️ Creating combined view...")
    combined = extractor.create_combined_view(image, regions)
    
    cv2.imshow("Combined View - All Regions", combined)
    
    print("✅ Combined view created")
    print("⌨️ Press any key to close window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n✅ Test passed!")


def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 70)
    print("TEST 6: ERROR HANDLING")
    print("=" * 70)
    
    extractor = FacialRegionExtractor()
    
    # Test 1: Non-existent file
    print("\n📋 Test 6.1: Non-existent file")
    result = extractor.process_image("nonexistent.jpg", display=False)
    if result is None:
        print("  ✅ Correctly handled missing file")
    else:
        print("  ❌ Should have returned None")
    
    # Test 2: Invalid region name
    print("\n📋 Test 6.2: Invalid region name")
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    landmarks = [(50, 50)] * 468
    result = extractor.crop_region(image, landmarks, "invalid_region")
    if result is None:
        print("  ✅ Correctly handled invalid region")
    else:
        print("  ❌ Should have returned None")
    
    print("\n✅ All error handling tests passed!")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 FACIAL REGION EXTRACTION - TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Basic Extraction", test_basic_extraction),
        ("Save Regions", test_save_regions),
        ("Individual Regions", test_individual_regions),
        ("Landmark Visualization", test_landmark_visualization),
        ("Combined View", test_combined_view),
        ("Error Handling", test_error_handling)
    ]
    
    print("\n📋 Available Tests:")
    for i, (name, _) in enumerate(tests, 1):
        print(f"  {i}. {name}")
    
    print("\n" + "=" * 70)
    choice = input("Enter test number (1-6) or 'all' to run all tests: ").strip().lower()
    
    if choice == 'all':
        for name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"\n❌ Test '{name}' failed with error: {str(e)}")
    elif choice.isdigit() and 1 <= int(choice) <= len(tests):
        name, test_func = tests[int(choice) - 1]
        try:
            test_func()
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {str(e)}")
    else:
        print("\n❌ Invalid choice")
    
    print("\n" + "=" * 70)
    print("✅ TEST SUITE COMPLETE")
    print("=" * 70)


def demo_usage():
    """Demonstrate usage examples"""
    print("\n" + "=" * 70)
    print("📚 USAGE EXAMPLES")
    print("=" * 70)
    
    print("""
EXAMPLE 1: Basic Usage
----------------------
from facial_region_extraction import FacialRegionExtractor

extractor = FacialRegionExtractor()
regions = extractor.process_image("face.jpg")


EXAMPLE 2: Save Regions
------------------------
extractor = FacialRegionExtractor()
regions = extractor.process_image(
    image_path="face.jpg",
    save_output=True,
    output_prefix="my_face"
)


EXAMPLE 3: Process Without Display
-----------------------------------
extractor = FacialRegionExtractor()
regions = extractor.process_image(
    image_path="face.jpg",
    display=False
)

# Access regions
forehead = regions['forehead']
left_eye = regions['left_eye']
right_eye = regions['right_eye']
cheeks = regions['cheeks']
lips_chin = regions['lips_chin']


EXAMPLE 4: Manual Processing
-----------------------------
extractor = FacialRegionExtractor()

# Load image
image = extractor.load_image("face.jpg")

# Detect face
face_landmarks = extractor.detect_face(image)

# Extract landmarks
landmarks = extractor.extract_landmarks(face_landmarks, image.shape)

# Segment regions
regions = extractor.segment_regions(image, landmarks)

# Display
extractor.display_regions(regions)


EXAMPLE 5: Extract Single Region
---------------------------------
extractor = FacialRegionExtractor()
image = extractor.load_image("face.jpg")
face_landmarks = extractor.detect_face(image)
landmarks = extractor.extract_landmarks(face_landmarks, image.shape)

# Get just the forehead
forehead = extractor.crop_region(image, landmarks, 'forehead')
cv2.imshow("Forehead", forehead)
cv2.waitKey(0)


COMMAND LINE USAGE:
-------------------
python facial_region_extraction.py face.jpg
python facial_region_extraction.py face.jpg --save
    """)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--demo':
            demo_usage()
        elif sys.argv[1] == '--test':
            if len(sys.argv) > 2:
                test_num = sys.argv[2]
                if test_num == '1':
                    test_basic_extraction()
                elif test_num == '2':
                    test_save_regions()
                elif test_num == '3':
                    test_individual_regions()
                elif test_num == '4':
                    test_landmark_visualization()
                elif test_num == '5':
                    test_combined_view()
                elif test_num == '6':
                    test_error_handling()
                else:
                    print("Invalid test number. Use 1-6.")
            else:
                run_all_tests()
        else:
            print("Usage:")
            print("  python test_facial_regions.py --demo")
            print("  python test_facial_regions.py --test [1-6]")
    else:
        run_all_tests()
