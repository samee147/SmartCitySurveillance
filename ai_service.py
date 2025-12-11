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

        total_frames = len(results)
        if total_frames == 0:
            total_frames = 1 

        total_counts = {}

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                total_counts[class_name] = total_counts.get(class_name, 0) + 1

        avg_summary = {}
        for class_name, total_count in total_counts.items():
            avg_summary[class_name] = round(total_count / total_frames)

        civic_issue_detected = "None"
        
        avg_people = avg_summary.get('person', 0)
        avg_vehicles = (avg_summary.get('car', 0) + 
                        avg_summary.get('bus', 0) + 
                        avg_summary.get('truck', 0))

        if avg_people > 5:
            civic_issue_detected = "Public Overcrowding (Street Vendor/Pedestrian)"
        elif avg_vehicles > 8:
            civic_issue_detected = "Heavy Traffic Congestion"

        filename = video_path.split('\\')[-1].split('/')[-1]
        output_filename = filename.rsplit('.', 1)[0] + '.avi'

        output_data = {
            "status": "success",
            "summary": avg_summary, 
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