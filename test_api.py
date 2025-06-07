import base64
import requests
import json

# Test image path - use a YOLO validation image
test_image_path = r"c:\project_root\dataset\dataset_yolo\images\val\refrig-35_jpeg.rf.6dfe5472ede86ab1e97f7471dc0f818e.jpg"

# Read and encode image
try:
    with open(test_image_path, 'rb') as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    print(f"✅ Image loaded: {len(image_base64)} characters")
    
    # Send to API
    api_url = "http://localhost:5000/api/detect"
    payload = {
        "image": f"data:image/jpeg;base64,{image_base64}"
    }
    
    print("🔄 Sending to detection API...")
    response = requests.post(api_url, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get('has_defects'):
            print(f"\n🎯 Found defects:")
            print(f"   Count: {result.get('defect_count')}")
            print(f"   Types: {result.get('defect_types')}")
            print(f"   Names: {result.get('defect_names')}")
            print(f"   Has result image: {'Yes' if result.get('result_image') else 'No'}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
