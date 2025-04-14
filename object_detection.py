import cv2
import numpy as np
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

def main():
    # Model and labels paths
    model_path = "ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
    label_path = "coco_labels.txt"
    # iPhone stream URL from Iriun (replace with your iPhone's IP)
    stream_url = "http://10.0.1.16:5353"

    # Load labels
    labels = read_label_file(label_path)

    # Load and initialize the model
    interpreter = make_interpreter(model_path)
    interpreter.allocate_tensors()

    # Initialize video stream
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Could not open iPhone stream")
        return

    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame")
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

            # Save frame
            cv2.imwrite("output_frame.jpg", frame)
            print("Saved output_frame.jpg")

            # Optional: Break loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
