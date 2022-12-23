from kframe import calculate_kflame, calculate_fscore
from result_to_excel import write_excel
import os


if __name__ == "__main__":
    print('程序开始！记得修改路径注意文件名')
    conf_thre = 0.5
    iou_thre = 0.8
    for i in range(2,24):
        tru_img_path = fr'C:\Users\李志卿\datasets\place{i}\images'
        tru_txt_path = fr'C:\Users\李志卿\datasets\place{i}\labels'
        pre_txt_path = fr'C:\Users\李志卿\myyolov5\runs\detect\exp{i}\labels'
        file_inf = {}
        # 找到该视频最后一帧的序号，即需要的file_num。通过这个来确定视频一共有多少帧。
        for file in os.listdir(tru_img_path):
            file_inf[file.split('mp4_')[0] + 'mp4'] = int(file.split('mp4_')[1][:3])
        
        for file_pre, file_num in file_inf.items():
            results = []
            # 把除了k=1的计算结果全部丢进去
            for k in (2, 4, 8, 16):
                a_start = 1
                for a in range(a_start, k+1):
                    for b in range(1, 17):
                        result = [k, a, b, calculate_kflame(file_pre=file_pre, file_num=file_num, unit_size=k,
                                     a=a/k, b=b/16, conf_thre=conf_thre, iou_thre=iou_thre, tru_txt_path=tru_txt_path, pre_txt_path=pre_txt_path)]
                        results.append(result)
            # 把k=1的计算结果丢进去,此时a,b也是1。
            results.append([1, 1, 1, calculate_fscore(file_pre=file_pre, file_num=file_num, conf_thre=conf_thre, iou_thre=iou_thre, tru_txt_path=tru_txt_path, pre_txt_path=pre_txt_path)])
            # 写execl
            write_excel(results, file_pre)

    print('程序结束！')