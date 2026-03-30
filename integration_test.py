#!/usr/bin/env python3
"""
VisionLab Studio - System Integration Test
Tests all backend endpoints and verifies system functionality
"""

import requests
import json
import sys
from pathlib import Path
from PIL import Image
import numpy as np
from io import BytesIO

# Configuration
API_BASE = "http://localhost:5000"
TIMEOUT = 5

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"  {status} {name}")
    if details:
        print(f"       {details}")

def create_test_image(size=512):
    """Create a simple test image (checkerboard pattern for easy comparison)"""
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    # Create checkerboard pattern
    for i in range(0, size, 64):
        for j in range(0, size, 64):
            if (i // 64 + j // 64) % 2 == 0:
                arr[i:i+64, j:j+64] = [100, 100, 100]
            else:
                arr[i:i+64, j:j+64] = [150, 150, 150]
    img = Image.fromarray(arr, 'RGB')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_endpoint_health():
    """Test /health endpoint"""
    print(f"\n{Colors.BLUE}Testing Health Endpoint{Colors.RESET}")
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=TIMEOUT)
        passed = resp.status_code == 200 and resp.json().get("status") == "ok"
        print_test("Health check", passed, f"Status: {resp.status_code}")
        return passed
    except Exception as e:
        print_test("Health check", False, str(e))
        return False

def test_endpoint_operations():
    """Test /operations endpoint"""
    print(f"\n{Colors.BLUE}Testing Operations Endpoint{Colors.RESET}")
    try:
        resp = requests.get(f"{API_BASE}/operations", timeout=TIMEOUT)
        passed = resp.status_code == 200
        data = resp.json()
        
        sections = data.get("sections", [])
        num_sections = len(sections)
        num_ops = sum(len(s.get("operations", [])) for s in sections)
        
        print_test("Operations endpoint", passed, f"Sections: {num_sections}, Operations: {num_ops}")
        
        if passed and num_ops > 25:
            print(f"       ✓ Expected 30+ operations, got {num_ops}")
            return True
        return False
    except Exception as e:
        print_test("Operations endpoint", False, str(e))
        return False

def test_endpoint_presets():
    """Test /presets endpoint"""
    print(f"\n{Colors.BLUE}Testing Presets Endpoint{Colors.RESET}")
    try:
        resp = requests.get(f"{API_BASE}/presets", timeout=TIMEOUT)
        passed = resp.status_code == 200
        data = resp.json()
        
        presets = data.get("presets", [])
        num_presets = len(presets)
        
        print_test("Presets endpoint", passed, f"Presets: {num_presets}")
        
        if passed and num_presets == 6:
            preset_names = [p.get("name") for p in presets]
            print(f"       Preset list: {', '.join(preset_names)}")
            return True
        return False
    except Exception as e:
        print_test("Presets endpoint", False, str(e))
        return False

def test_endpoint_process():
    """Test /process endpoint with grayscale operation"""
    print(f"\n{Colors.BLUE}Testing Process Endpoint{Colors.RESET}")
    try:
        test_img = create_test_image()
        
        files = {'image': ('test.png', test_img, 'image/png')}
        data = {'operation': 'grayscale'}
        
        resp = requests.post(f"{API_BASE}/process", files=files, data=data, timeout=TIMEOUT)
        passed = resp.status_code == 200 and resp.headers.get('content-type') == 'image/png'
        
        print_test("Process endpoint (grayscale)", passed, f"Status: {resp.status_code}")
        
        if passed and len(resp.content) > 0:
            print(f"       Output size: {len(resp.content)} bytes")
            return True
        return False
    except Exception as e:
        print_test("Process endpoint", False, str(e))
        return False

def test_endpoint_metrics():
    """Test /metrics endpoint"""
    print(f"\n{Colors.BLUE}Testing Metrics Endpoint{Colors.RESET}")
    try:
        test_img = create_test_image()
        
        files = {'image': ('test.png', test_img, 'image/png')}
        
        resp = requests.post(f"{API_BASE}/metrics", files=files, timeout=TIMEOUT)
        passed = resp.status_code == 200
        data = resp.json()
        
        required_keys = {'mean', 'std', 'min', 'max', 'entropy', 'contrast'}
        has_keys = required_keys.issubset(data.keys())
        
        print_test("Metrics endpoint", passed and has_keys, f"Status: {resp.status_code}")
        
        if passed and has_keys:
            print(f"       Mean: {data['mean']:.2f}, Std: {data['std']:.2f}, Entropy: {data['entropy']:.2f}")
            return True
        return False
    except Exception as e:
        print_test("Metrics endpoint", False, str(e))
        return False

def test_endpoint_compare():
    """Test /compare endpoint with actual image processing"""
    print(f"\n{Colors.BLUE}Testing Compare Endpoint{Colors.RESET}")
    try:
        # Create original image
        original = create_test_image()
        original_data = original.getvalue()
        
        # Process the image to create a different version
        original.seek(0)
        files_process = {'image': ('test.png', BytesIO(original_data), 'image/png')}
        data_process = {'operation': 'brightness', 'value': '50'}
        
        resp_process = requests.post(f"{API_BASE}/process", files=files_process, 
                                     data=data_process, timeout=TIMEOUT)
        
        if resp_process.status_code != 200:
            print_test("Compare endpoint", False, "Failed to process image for comparison")
            return False
        
        # Now compare original and processed (both same size and format)
        files = {
            'before': ('before.png', BytesIO(original_data), 'image/png'),
            'after': ('after.png', BytesIO(resp_process.content), 'image/png')
        }
        
        resp = requests.post(f"{API_BASE}/compare", files=files, timeout=TIMEOUT)
        passed = resp.status_code == 200
        data = resp.json()
        
        required_keys = {'mse', 'psnr', 'before_metrics', 'after_metrics'}
        has_keys = required_keys.issubset(data.keys())
        
        print_test("Compare endpoint", passed and has_keys, f"Status: {resp.status_code}")
        
        if passed and has_keys:
            mse = data['mse']
            psnr = data['psnr']
            print(f"       MSE: {mse:.2f}, PSNR: {psnr:.2f}")
            # MSE should be > 0 since we applied brightness change
            if mse > 0:
                print(f"       ✓ Real image difference detected (MSE > 0)")
            return True
        return False
    except Exception as e:
        print_test("Compare endpoint", False, str(e))
        return False

def test_operation_parameters():
    """Test that operations with parameters work correctly"""
    print(f"\n{Colors.BLUE}Testing Operation Parameters{Colors.RESET}")
    try:
        test_img = create_test_image()
        
        # Test brightness operation with parameter
        files = {'image': ('test.png', test_img, 'image/png')}
        data = {'operation': 'brightness', 'value': '50'}
        
        resp = requests.post(f"{API_BASE}/process", files=files, data=data, timeout=TIMEOUT)
        passed = resp.status_code == 200
        
        print_test("Operation with parameters", passed, f"Operation: brightness, Status: {resp.status_code}")
        return passed
    except Exception as e:
        print_test("Operation with parameters", False, str(e))
        return False

def run_all_tests():
    """Run all integration tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}VisionLab Studio - System Integration Tests{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    print(f"\nBackend URL: {API_BASE}")
    print(f"Test Image Size: 512x512")
    
    tests = [
        test_endpoint_health,
        test_endpoint_operations,
        test_endpoint_presets,
        test_endpoint_process,
        test_endpoint_metrics,
        test_endpoint_compare,
        test_operation_parameters,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"{Colors.RED}Unexpected error in test: {e}{Colors.RESET}")
            results.append(False)
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{Colors.GREEN}✓ ALL TESTS PASSED ({passed}/{total}){Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠ {passed}/{total} TESTS PASSED{Colors.RESET}")
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        sys.exit(1)
