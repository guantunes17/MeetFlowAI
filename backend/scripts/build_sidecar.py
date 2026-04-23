import platform
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_target_triple() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        if machine in {"amd64", "x86_64"}:
            return "x86_64-pc-windows-msvc"
        if machine in {"arm64", "aarch64"}:
            return "aarch64-pc-windows-msvc"
    if system == "linux":
        if machine in {"amd64", "x86_64"}:
            return "x86_64-unknown-linux-gnu"
        if machine in {"arm64", "aarch64"}:
            return "aarch64-unknown-linux-gnu"
    if system == "darwin":
        if machine in {"arm64", "aarch64"}:
            return "aarch64-apple-darwin"
        return "x86_64-apple-darwin"

    raise RuntimeError(f"Plataforma não suportada para sidecar: {system}/{machine}")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    backend_dir = repo_root / "backend"
    frontend_dir = repo_root / "frontend"
    spec_file = backend_dir / "meetflow_backend.spec"

    if not spec_file.exists():
        raise FileNotFoundError(f"Spec do PyInstaller não encontrado: {spec_file}")

    print("Gerando sidecar do backend com PyInstaller...")
    pyinstaller = shutil.which("pyinstaller")
    command = [pyinstaller, str(spec_file.name), "--noconfirm"] if pyinstaller else [sys.executable, "-m", "PyInstaller", str(spec_file.name), "--noconfirm"]
    subprocess.run(command, cwd=backend_dir, check=True)

    exe_name = "meetflow-backend.exe" if platform.system().lower() == "windows" else "meetflow-backend"
    built_binary = backend_dir / "dist" / exe_name
    if not built_binary.exists():
        raise FileNotFoundError(f"Binário do sidecar não encontrado após build: {built_binary}")

    target_triple = resolve_target_triple()
    output_dir = frontend_dir / "src-tauri" / "binaries"
    output_dir.mkdir(parents=True, exist_ok=True)

    suffix = ".exe" if platform.system().lower() == "windows" else ""
    output_name = f"meetflow-backend-{target_triple}{suffix}"
    output_path = output_dir / output_name
    shutil.copy2(built_binary, output_path)

    print(f"Sidecar pronto: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Falha ao construir sidecar: {exc}")
        raise SystemExit(exc.returncode)
    except Exception as exc:
        print(f"Erro: {exc}")
        raise SystemExit(1)
