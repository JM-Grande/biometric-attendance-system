import os

# Get the absolute path of the current script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))

def check_null_bytes(filename):
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            if b'\x00' in content:
                print(f"❌ FAIL: {filename} contains null bytes!")
                print(f"   Size: {len(content)} bytes")
                # print(f"   First 20 bytes: {content[:20]}")
            else:
                print(f"✅ PASS: {filename} is clean.")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

files_to_check = [
    "main.py",
    "ui/__init__.py",
    "ui/main_window.py",
    "ui/home_frame.py",
    "ui/register_frame.py",
    "ui/attendance_frame.py",
    "core/__init__.py",
    "utils/__init__.py"
]

print(f"Checking for null bytes in {base_dir}...")
for f in files_to_check:
    check_null_bytes(f)
