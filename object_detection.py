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
    image_path = "test_image.jpg"  # Replace with your image or use camera

    # Load labels
    labels = read_label_file(label_path)

    # Load and initialize the model
    interpreter = make_interpreter(model_path)
    interpreter.allocate_tensors()

    # Load and preprocess image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image")
        return
    _, scale = common.set_resized_input(
        interpreter, image.shape[:2], lambda size: cv2.resize(image, size))

    # Run inference
    interpreter.invoke()
    objs = detect.get_objects(interpreter, score_threshold=0.3, image_scale=scale)

    # Draw results
    for obj in objs:
        bbox = obj.bbox
        label = labels.get(obj.id, "Unknown")
        confidence = obj.score
        print(f"Detected: {label} ({confidence:.2f}) at {bbox}")
        cv2.rectangle(image, (bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax), (0, 255, 0), 2)
        cv2.putText(image, f"{label} {confidence:.2f}", (bbox.xmin, bbox.ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display or save result
    cv2.imwrite("output.jpg", image)
    print("Output saved as output.jpg")

if __name__ == "__main__":
    main()
