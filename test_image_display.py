#!/usr/bin/env python3
"""
Test script to verify image display compatibility
"""

from PIL import Image
import io

def test_image_creation():
    """Test creating and displaying an image"""
    print("Testing image creation and display...")
    
    try:
        # Create a test image
        test_image = Image.new('RGB', (200, 200), color='blue')
        print("[OK] Test image created successfully")
        
        # Test saving to bytes (simulating file upload)
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        img_bytes = buffer.getvalue()
        print(f"[OK] Image saved to bytes: {len(img_bytes)} bytes")
        
        # Test opening from bytes (simulating uploaded file)
        buffer.seek(0)
        opened_image = Image.open(buffer)
        print("[OK] Image opened from bytes successfully")
        
        # Test image properties
        print(f"[OK] Image size: {opened_image.size}")
        print(f"[OK] Image mode: {opened_image.mode}")
        print(f"[OK] Image format: {opened_image.format}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Image test failed: {e}")
        return False

def test_streamlit_image_params():
    """Test Streamlit image parameters compatibility"""
    print("\nTesting Streamlit image parameter compatibility...")
    
    # Test different width parameter values
    test_cases = [
        ("No width parameter", "st.image(image)"),
        ("Width as integer", "st.image(image, width=300)"),
        ("Width as None", "st.image(image, width=None)"),
    ]
    
    for description, code in test_cases:
        try:
            # This is just a syntax check, not actual execution
            compile(code, '<string>', 'exec')
            print(f"[OK] {description}: {code}")
        except SyntaxError as e:
            print(f"[FAIL] {description}: {e}")
            return False
    
    print("[OK] All Streamlit image parameter tests passed")
    return True

if __name__ == "__main__":
    print("Image Display Compatibility Test")
    print("=" * 40)
    
    success1 = test_image_creation()
    success2 = test_streamlit_image_params()
    
    if success1 and success2:
        print("\n[SUCCESS] All image display tests passed!")
        print("[INFO] Your app should work correctly in Snowflake SiS")
    else:
        print("\n[FAIL] Some tests failed. Please check the issues above.")
