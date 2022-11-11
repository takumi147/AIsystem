import os
from email.base64mime import body_encode


"""
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

def get_box(file):
    """
    extract box information from txt
    :param file: "xxx.txt"
    :return [[y0, x0, y1, x1],], which reflect boxes's 
                bottom line, left line, top line, right line.
    """
    # read txt and split different boxes
    txt = open(file, 'r').read().split('\n')
    
    # create the boxes list
    boxes = []

    # add boxes information into list
    # pre_txt: [n, x, y, w, h, c] to [bottom line, left line, top line, right line, c]
    # tru_txt: [n, x, y, w, h] to [bottom line, left line, top line, right line]
    for box in txt:
        if box:
            box = box.split(' ')
            bottom_line = float(box[2]) - float(box[4][:-2])/2
            left_line = float(box[1]) - float(box[3])/2
            top_line = float(box[2]) + float(box[4][:-2])/2
            right_line = float(box[1]) + float(box[3])/2
            
            if len(box) == 6:
                boxes.append([bottom_line, left_line, top_line, right_line, box[-1]])
            else:
                boxes.append([bottom_line, left_line, top_line, right_line])
    return boxes

def get_iou(tru_txt, pre_txt, conf_thre):
    """
    compute iou from two result files.
    :param tru_txt, pre_txt: "xxx.txt"
    :return average iou
    """

    box1 = get_box(tru_txt)
    box2 = get_box(pre_txt)
    iou = 0

    # iterate every box in two file and compute all their iou
    for i in box1:
        for j in box2:
            if j[-1] >= conf_thre:
                iou += compute_iou(i, j)
    
    return (iou / (len(box1) * len(box2)))


def f_score(tp, tn, fp, fn):
    """
    compute f-score
    """
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    return (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0


def calculate_f_score(file_pre='', file_num=0, unit_size=16, a=0.5, b=0.5, conf_thre=0.8, iou_thre=0.5):
    """
    use k-frame to compute TP, TN, FP, FN
    :param  file_pre: ep."place1_whitecane01.mp4_5.txt" pre is "place1_whitecane01.mp4"
            unit_size: how many flame compose an unit, = k.
            file_num: how many flame we have.
            a: the error modulus to judge true, false.
            b: the error modulus to judge positive, negative.
            conf_thre: confidence thread to abandon unreliable flame.
            iou_thre: iou thread to abandon unreliable flame.
    :return f-score
    """
    # default some varities.
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    unit_num = file_num // unit_size
    folder_pre_name = 'pre'
    folder_tru_name = 'tru'

    # use flame_truth_num and flame_pre_num to calculate the tp, tn, fp, fn.
    for i in range(unit_num+1):
        # count the number of flame of predition and truth.
        flame_truth_num = 0
        flame_pre_num = 0
        
        # iterate an unit, and judge which status it is.
        for j in range(1, unit_size+1):
            txtname = file_pre + '_{}.txt'.format(j + i * unit_size)
            pre_txt_path = os.path.join(folder_pre_name, txtname)
            tru_txt_path = os.path.join(folder_tru_name, txtname)

            if os.path.exists(tru_txt_path):
                flame_truth_num += 1
                if os.path.exists(pre_txt_path):
                    iou = get_iou(tru_txt_path, pre_txt_path, conf_thre)
                    if iou >= iou_thre:
                        flame_pre_num += 1

        # calculate the tp, tn, fp, fn.
        if flame_truth_num >= (unit_size * a) and flame_pre_num >= (unit_size * b):
            tp += 1
        elif flame_truth_num >= (unit_size * a) and flame_pre_num < (unit_size * b):
            fn += 1
        elif flame_truth_num < (unit_size * a) and flame_pre_num >= (unit_size * b):
            fp += 1       
        elif flame_truth_num < (unit_size * a) and flame_pre_num < (unit_size * b):
            tn += 1

        flame_truth_num = 0
        flame_pre_num = 0

    return f_score(tp, tn, fp, fn)



if __name__ == '__main__':
    file_pre = 'place1_whitecane01.mp4'
    file_num = 379
    print(calculate_f_score(file_pre, file_num, unit_size=16, a=0.5, b=0.5, conf_thre=0.8, iou_thre=0.5))
                