"""
Deployment verification script
Tests GitHub connection and Render configuration
"""
import sys
import subprocess
import requests
import time


def check_git_config():
    """Verify Git configuration"""
    print("🔍 Checking Git configuration...")
    
    try:
        # Check remote
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        
        if 'plannerprogenerator.git' in remote_url:
            print(f"✅ Git remote configured: {remote_url}")
            return True
        else:
            print(f"❌ Wrong remote: {remote_url}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Git remote not configured: {e}")
        return False


def check_render_health():
    """Check Render deployment health"""
    print("\n🏥 Checking Render deployment health...")
    
    url = "https://plannerprogenerator.onrender.com/healthz"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            version = data.get('version', 'unknown')
            print(f"✅ Render is healthy - Version: {version}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Cannot reach Render: {e}")
        return False


def check_render_config():
    """Verify render.yaml configuration"""
    print("\n📋 Checking render.yaml...")
    
    try:
        with open('render.yaml', 'r') as f:
            content = f.read()
            
        checks = [
            ('buildCommand' in content, "buildCommand present"),
            ('startCommand' in content, "startCommand present"),
            ('PYTHON_VERSION' in content, "Python version specified"),
            ('PORT' in content, "Port configured")
        ]
        
        all_good = True
        for check, msg in checks:
            if check:
                print(f"  ✅ {msg}")
            else:
                print(f"  ❌ {msg}")
                all_good = False
        
        return all_good
    except FileNotFoundError:
        print("❌ render.yaml not found")
        return False


def smoke_test_api():
    """Perform basic API smoke test"""
    print("\n🧪 Running API smoke test...")
    
    url = "https://plannerprogenerator.onrender.com/api/generate"
    payload = {
        'cantidad_ordenes': 2,
        'ct_origen': 'Test CD',
        'fecha_entrega': '2025-01-15',
        'capacidad_min': 1.0,
        'capacidad_max': 5.0,
        'ventana_inicio': '09:00',
        'ventana_fin': '17:00',
        'pais': 'Chile',
        'ciudad': 'Santiago'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'spreadsheetml' in content_type and len(response.content) > 1000:
                print(f"✅ API test passed - Generated {len(response.content)} bytes")
                return True
            else:
                print(f"❌ Unexpected response format")
                return False
        else:
            print(f"❌ API test failed: HTTP {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False


def main():
    """Run all verification checks"""
    print("="*60)
    print("🚀 DEPLOYMENT VERIFICATION")
    print("="*60)
    
    results = []
    
    # Run checks
    results.append(("Git Configuration", check_git_config()))
    results.append(("Render Configuration", check_render_config()))
    results.append(("Render Health", check_render_health()))
    results.append(("API Smoke Test", smoke_test_api()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("🎉 All checks passed! Deployment is ready.")
        return 0
    else:
        print("⚠️  Some checks failed. Please review and fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
