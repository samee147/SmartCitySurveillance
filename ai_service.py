import sys
import json
from ultralytics import YOLO

model = YOLO('yolov8n.pt') 

def analyze_video(video_path):
    try:
        results = model.predict(
            source=video_path, 
            save=True, 
            project='public/uploads', 
            name='processed', 
            exist_ok=True, 
            conf=0.25,
            verbose=False
        )

        summary = {}
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                summary[class_name] = summary.get(class_name, 0) + 1

        civic_issue_detected = "None"
        
        person_count = summary.get('person', 0)
        vehicle_count = summary.get('car', 0) + summary.get('bus', 0) + summary.get('truck', 0)

        if person_count > 5:
            civic_issue_detected = "Public Overcrowding (Street Vendor/Pedestrian)"
        elif vehicle_count > 5:
            civic_issue_detected = "Heavy Traffic Congestion"

        filename = video_path.split('\\')[-1].split('/')[-1]
        output_filename = filename.rsplit('.', 1)[0] + '.avi'

        output_data = {
            "status": "success",
            "summary": summary,
            "civic_issue": civic_issue_detected, 
            "output_video": f"uploads/processed/{output_filename}"
        }

        print("---JSON_START---")
        print(json.dumps(output_data))
        print("---JSON_END---")

    except Exception as e:
        error_data = {"status": "error", "message": str(e)}
        print("---JSON_START---")
        print(json.dumps(error_data))
        print("---JSON_END---")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_video(sys.argv[1])