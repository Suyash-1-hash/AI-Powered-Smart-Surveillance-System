from ultralytics import YOLO

def train():
    model = YOLO("yolov8n.pt")

    model.train(
        data="Weapon Detection.v1i.yolov8/data.yaml",
        epochs=50,
        imgsz=640,
        device=0
    )

if __name__ == "__main__":
    train()