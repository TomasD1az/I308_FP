import os
import requests
import zipfile
import shutil
from tqdm import tqdm

BASE_DIR = "datasets/KITTI_odom_gray"
KITTI_ZIP = "data_odometry_gray.zip"
KITTI_URL = "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_odometry_gray.zip"
SEQ = "00"
SEQ_PATH = os.path.join(BASE_DIR, SEQ)

def download_file(url, dest):
    if os.path.exists(dest):
        print(f"[✓] Ya existe: {dest}")
        return
    print(f"[↓] Descargando: {url}")
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(dest, 'wb') as file, tqdm(
        desc=os.path.basename(dest),
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    print(f"[✓] Descargado: {dest}")

def extract_sequence(zip_path, target_seq="00"):
    print(f"[⇪] Extrayendo secuencia {target_seq}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        members = [m for m in zip_ref.namelist() if f"sequences/{target_seq}/" in m]
        zip_ref.extractall(path="tmp_kitti_gray", members=members)

    src = os.path.join("tmp_kitti_gray", "sequences", target_seq)
    dst = os.path.join(BASE_DIR, target_seq)
    os.makedirs(dst, exist_ok=True)

    for cam in ["image_0", "image_1"]:
        src_cam = os.path.join(src, cam)
        dst_cam = os.path.join(dst, cam)
        if os.path.exists(dst_cam):
            shutil.rmtree(dst_cam)
        shutil.move(src_cam, dst_cam)
        print(f"[→] Movido: {src_cam} → {dst_cam}")

    shutil.rmtree("tmp_kitti_gray")
    print(f"[✓] Secuencia {target_seq} lista en: {dst}")

if __name__ == "__main__":
    os.makedirs(BASE_DIR, exist_ok=True)
    zip_dest = os.path.join(BASE_DIR, KITTI_ZIP)

    download_file(KITTI_URL, zip_dest)
    extract_sequence(zip_dest, SEQ)
    print(f"[✓] KITTI dataset preparado en: {SEQ_PATH}")