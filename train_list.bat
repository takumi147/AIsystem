@echo off
call C:\ANACONDA\Scripts\activate.bat C:\ANACONDA\envs\yolov5
python train.py --data data/place1.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place2.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place3.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place4.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place5.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place6.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place7.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place8.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place9.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place10.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place11.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place12.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place13.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place14.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place15.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place16.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place17.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place18.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place19.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place20.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place21.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place22.yaml --weights models/yolov5m.pt --epochs 200
python train.py --data data/place23.yaml --weights models/yolov5m.pt --epochs 200
pause