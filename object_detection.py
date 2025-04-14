import cv2
import numpy as np
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

def main():
    model_path = "ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
    label_path = "coco_labels.txt"

    labels = read_label_file(label_path)
    interpreter = make_interpreter(model_path)
    interpreter.allocate_tensors()

    # Initialize camera (use 0 for USB webcam, or picamera2 for Pi Camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess frame
        _, scale = common.set_resized_input(
            interpreter, frame.shape[:2], lambda size: cv2.resize(frame, size))

        # Run inference
        interpreter.invoke()
        objs = detect.get_objects(interpreter, score_threshold=0.3, image_scale=scale)

        # Draw results
        for obj in objs:
            bbox = obj.bbox
            label = labels.get(obj.id, "Unknown")
            confidence = obj.score
            cv2.rectangle(frame, (bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (bbox.xmin, bbox.ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display frame (optional, requires X server)
        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
