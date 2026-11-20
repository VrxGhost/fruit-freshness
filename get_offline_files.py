"""Download the ONNX Runtime Web files into ./ort so the site also works with no internet.

Run once while you are online:   python get_offline_files.py
Then start the site offline:     python -m http.server 8000   and open http://localhost:8000
"""
import pathlib
import urllib.request

VERSION = "1.20.1"   # must match ORT_VERSION in index.html
BASE = f"https://cdn.jsdelivr.net/npm/onnxruntime-web@{VERSION}/dist/"
FILES = ["ort.wasm.min.js", "ort-wasm-simd-threaded.mjs", "ort-wasm-simd-threaded.wasm"]

out = pathlib.Path(__file__).resolve().parent / "ort"
out.mkdir(exist_ok=True)
for name in FILES:
    print(f"Downloading {name} ...", end=" ", flush=True)
    urllib.request.urlretrieve(BASE + name, out / name)
    print(f"{(out / name).stat().st_size / 1e6:.1f} MB")
print(f"\nDone. Files saved in {out}")
print("Now run:  python -m http.server 8000   and open http://localhost:8000")
