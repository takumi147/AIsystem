"""
下のコードを.pyのファイルに書き込んで、実行時は「Anaconda Prompt」で呼び出せる。

実行時は下のファイル配置にする。

data
├── 【ビデオのフォルダ】
	 └──【ビデオ】
└── 本ツール


このツール実行すると、同じフォルダ内のすべてのビデオに対してフレーム抽出を行う。

python [ツール名].py
"""

import cv2
import sys, os
import time

frameFrequency=15 # 抽出時のフレーム間隔。ここでは、1フレームごとに抽出

RootPath = os.getcwd()
for root,dirs,files in os.walk(RootPath):
    for dir in dirs:
        os.chdir(os.path.join(RootPath,dir)) 
        filePath = os.getcwd() 
        
        for root2,dirs2,files2 in os.walk(filePath): 
            for file_name in files2:
                file_prefix = file_name.split('.')[0]
                file_suffix = file_name.split('.')[1]
                if(file_suffix == "mp4" ):
                    outPutDirName = os.path.join(filePath, 'images',  file_prefix)
                    if not os.path.exists(outPutDirName):
                        os.makedirs(outPutDirName) 
                    
                    
                    camera = cv2.VideoCapture(file_name)
                    #初期化
                    frame=0
                    while True:
                        frame+=1
                        res, image = camera.read()
                        if not res:
                            if frame > 1:
                                print('done')
                            else:
                                print('not res , not image')
                            break
                        if frame % frameFrequency == 0:
                            full_path = os.path.join(outPutDirName, os.path.basename(filePath) +'_'+file_name+'_'+str(frame)+'.jpg')
                            if os.path.exists(full_path):
                                print(full_path+" is existed")
                            else:
                                cv2.imwrite(full_path, image)
                                print(outPutDirName + os.path.basename(filePath) +'_'+file_name+'_'+str(frame)+'.jpg')
                    print('抽出が完了')
                    camera.release()