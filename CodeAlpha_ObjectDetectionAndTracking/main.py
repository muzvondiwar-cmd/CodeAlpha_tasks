import cv2
import argparse
from ultralytics import YOLO


def parse_arguments():
    parser = argparse.ArgumentParser(description="Real-Time Object Detection and Tracking")

    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Video source. Use 0 for webcam or provide a video file path."
    )

    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help="YOLO model file. Default is yolov8n.pt"
    )

    parser.add_argument(
        "--confidence",
        type=float,
        default=0.4,
        help="Minimum confidence score for detection."
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    source = int(args.source) if args.source.isdigit() else args.source

    print("Loading YOLO model...")
    model = YOLO(args.model)

    print("Opening video source...")
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Error: Could not open webcam or video file.")
        return

    print("Object detection and tracking started.")
    print("Press 'q' to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            print("End of video or failed to read frame.")
            break

        results = model.track(
            frame,
            persist=True,
            conf=args.confidence,
            tracker="bytetrack.yaml",
            verbose=False
        )

        annotated_frame = results[0].plot()

        cv2.imshow("Object Detection and Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()