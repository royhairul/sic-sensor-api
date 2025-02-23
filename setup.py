import os
import sys
import subprocess

def create_virtualenv():
    """Membuat dan mengaktifkan virtual environment"""
    venv_dir = "venv"
    
    if not os.path.exists(venv_dir):
        print("📌 Membuat virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
    
    activate_script = os.path.join(venv_dir, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_dir, "bin", "activate")
    
    print(f"✅ Virtual environment dibuat di {venv_dir}")
    return activate_script

def install_requirements():
    """Menginstal dependensi dari requirements.txt"""
    print("📌 Menginstal dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ Instalasi dependencies selesai.")

if __name__ == "__main__":
    create_virtualenv()
    install_requirements()
    print("\n🎉 Setup selesai! Aktifkan virtual environment:")
    print("   Windows: venv\\Scripts\\activate")
    print("   macOS/Linux: source venv/bin/activate")
