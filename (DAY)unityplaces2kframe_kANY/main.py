from utils import getvideo_nameandflamenum, calculate_tpfptnfn_kframe, calculate_fscore, calculate_tpfptnfn_k1, write_excel
import numpy as np


def main(conf_thre, iou_thre):
    tp, fp, tn, fn = 0,0,0,0
    # conf_thre, iou_thre = 0.5, 0.8
    video_inf = {}
    res = []
    print('start')

    # 计算使用Kframe的评价结果
    for k in (150,):
        a_start = 1
        for a in range(a_start, k+1):
            for b in range(1, 2):
                # there are 23 experimental places.
                for i in range(1,24):        
                    tru_img_path = fr'C:\Users\李志卿\datasets\place{i}\images'
                    tru_txt_path = fr'C:\Users\李志卿\datasets\place{i}\labels'
                    pre_txt_path = fr'D:\昼daytime23place_detectresult\exp{i}\labels'
                    video_inf = getvideo_nameandflamenum(tru_img_path)
                    for video, flamenum in video_inf.items():
                        tpfptnfn = calculate_tpfptnfn_kframe(tru_txt_path=tru_txt_path, pre_txt_path=pre_txt_path, file_pre=video,
                        file_num=flamenum, unit_size=k, a=a/k, b=b/k, conf_thre=conf_thre, iou_thre=iou_thre)
                        tp += tpfptnfn[0]
                        fp += tpfptnfn[1]
                        tn += tpfptnfn[2]
                        fn += tpfptnfn[3]
                fscore = calculate_fscore(tp, tn, fp, fn)
                tp, fp, tn, fn = 0,0,0,0
                res.append([k,a,b,fscore])
                print(fr'k:{k},a:{a}/{k},b:{b}/{k}, over')

    # 计算不适用kframe的评价结果，此时k，a，b都是1
    # for i in range(1,24):
    #     tru_img_path = fr'C:\Users\李志卿\datasets\place{i}\images'
    #     tru_txt_path = fr'C:\Users\李志卿\datasets\place{i}\labels'
    #     pre_txt_path = fr'C:\Users\李志卿\myyolov5\runs\detect\exp{i}\labels'
    #     video_inf = getvideo_nameandflamenum(tru_img_path)
    #     for video, flamenum in video_inf.items():
    #         tpfptnfn = calculate_tpfptnfn_k1(tru_txt_path=tru_txt_path, pre_txt_path=pre_txt_path, file_pre=video,
    #         file_num=flamenum, conf_thre=conf_thre, iou_thre=iou_thre)
    #         tp += tpfptnfn[0]
    #         fp += tpfptnfn[1]
    #         tn += tpfptnfn[2]
    #         fn += tpfptnfn[3]
    # fscore = calculate_fscore(tp, tn, fp, fn)
    # tp, fp, tn, fn = 0,0,0,0
    # res.append([1,1,1,fscore])
    # print('k=1, over')

    # 写结果到excel
    write_excel(k, res, f'c{conf_thre}_iou{iou_thre}')


if __name__ == '__main__':
    for conf_thre in np.arange(0.1, 0.2, 0.1):
        conf_thre = round(conf_thre, 1)
        for iou_thre in np.arange(0.1, 0.2, 0.1):
            iou_thre = round(iou_thre, 1)
            print(f'start c:{conf_thre}_iou:{iou_thre}')
            main(conf_thre, iou_thre)