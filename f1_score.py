import os
from email.base64mime import body_encode


"""
文件说明：此乃多个video同时测试时。计算kframe的方法，修改了file_pre为file_pres.
file construct:
kframe.py
|-pre-xxxx.txt
|-tru-xxxx.txt

"""



def compute_iou(b1, b2):
    """
    compute IoU
    :param b1: [y0, x0, y1, x1], which reflect box's 
                bottom line, left line, top line, right line.
           b2: [y0, x0, y1, x1]
    :return scale value of IoU
    """
    # turn str into float, 1 -> 1.0
    b1 = list(map(float, b1))
    b2 = list(map(float, b2))

    # compute area of each 
    s_b1 = (b1[2] - b1[0]) * (b1[3] - b1[1])
    s_b2 = (b2[2] - b2[0]) * (b2[3] - b2[1])

    # compute the sum_area
    sum_area = s_b1 + s_b2

    # compute intersect area
    bottom_line = max(b1[0], b2[0])
    left_line = max(b1[1], b2[1])
    top_line = min(b1[2], b2[2])
    right_line = min(b1[3], b2[3])

    # judge if there is an intersect
    if bottom_line >= top_line or left_line >= right_line:
        return 0
    else:
        intersect_area = (top_line - bottom_line) * (right_line - left_line)
        return (intersect_area/(sum_area - intersect_area))

def xywh_to_bltr(box):
    """
    [x, y, w, h] to [bottom line, left line, top line, right line]
    so that we can use compute_iou
    """
    bottom_line = float(box[1]) - float(box[3])/2
    left_line = float(box[0]) - float(box[2])/2
    top_line = float(box[1]) + float(box[3])/2
    right_line = float(box[0]) + float(box[2])/2
    return [bottom_line, left_line, top_line, right_line]

def f_score(tp, tn, fp, fn):
    """
    compute f-score
    """
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    return (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0


def calculate_f1_score(conf_thre=0.8, iou_thre=0.5):
    """
    use f1_score to compute TP, TN, FP, FN
    如果某一张图片在tru中有空txt，说明是F样本。但pre里不会有空txt，说明是N样本。
    pre中的txt格式是'0 x y w h c\n'
    tru中的txt格式是'0 x y w h'
    :param  conf_thre: confidence thread to abandon unreliable flame.
            iou_thre: iou thread to abandon unreliable flame.
    :return f-score
    """
    # default some varities.
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    pre_path = os.path.join(os.getcwd(), 'pre')
    tru_path = os.path.join(os.getcwd(), 'tru')
    
    
    print('一共有{}个tru文件'.format(len(os.listdir(tru_path))))
    print('一共有{}个pre文件'.format(len(os.listdir(pre_path))))
    # calculate tp, tn, fp, fn.
    for label in os.listdir(tru_path):
        tru_txt = open(os.path.join(tru_path, label)).read()
        # 如果tru_txt里面非空，说明是t。由此进行讨论。
        if tru_txt:
            tru_labels = open(os.path.join(tru_path, label)).read().split(f'\n')
            tru_num = len(tru_labels)

            # 既存在tru_label.txt中的标记，也有pre_label.txt。需要每一条都拉出来比较iou和conf。
            if os.path.exists(os.path.join(pre_path, label)):
                pre_labels = open(os.path.join(pre_path, label)).read().split(f'\n')[:-1]
                pre_num = len(pre_labels)
                
                for tru_label in tru_labels:
                    for pre_label in pre_labels:
                        conf_score = float(pre_label.split(' ')[-1])
                        t = xywh_to_bltr(tru_label.split(' ')[1:])
                        p = xywh_to_bltr(pre_label.split(' ')[1:-1])
                        iou = compute_iou(t, p)

                        if conf_score >= conf_thre and iou >= iou_thre:
                            tp += 1
                            tru_num -= 1
                            pre_num -= 1

                if tru_num != 0:
                    tn += tru_num
                if pre_num != 0:
                    fp += pre_num

            # tn 的情况，tru_label.txt里有标记但没有pre_label.txt
            else:
                tn += tru_num

        # fp 的情况，tru_label.txt里没有标记但有pre_label.txt
        elif (not tru_txt) and os.path.exists(os.path.join(pre_path, label)):
            pre_num = len(open(os.path.join(pre_path, label)).read().split(f'\n')) - 1
            fp += pre_num

        # fn 的情况，tru_label.txt里没有标记且没有pre_label.txt
        elif (not tru_txt) and (not os.path.exists(os.path.join(pre_path, label))):
            fn += 1
            

    print(tp, tn, fp, fn)
    return f_score(tp, tn, fp, fn)


if __name__ == '__main__':
    print(calculate_f1_score(conf_thre=0.8, iou_thre=0.8))
                