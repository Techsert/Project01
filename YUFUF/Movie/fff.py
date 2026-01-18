import sys
import importlib.util
import pkg_resources

print("🔎 Python Executable:", sys.executable)
print("🔎 Python Version:", sys.version)

package_name = "moviepy"

# تحقق إذا موجودة ولا لا
spec = importlib.util.find_spec(package_name)
if spec is None:
    print(f"❌ {package_name} NOT installed.")
else:
    print(f"✅ {package_name} is installed.")
    # اطبع مكانها
    module = importlib.import_module(package_name)
    print(f"📂 {package_name} location:", module.__file__)

# تحقق من كل المكتبات المهمة
print("\n--- Installed packages check ---")
for pkg in ["moviepy", "gtts", "Pillow"]:
    try:
        version = pkg_resources.get_distribution(pkg).version
        print(f"✅ {pkg} version {version}")
    except pkg_resources.DistributionNotFound:
        print(f"❌ {pkg} not found")
