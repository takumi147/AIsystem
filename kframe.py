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

def get_tru_boxes(file):
    """
    extract box information from txt
    :param file: "xxx.txt"
    :return [[y0, x0, y1, x1, ],]
            which reflect boxes's bottom line, left line, top line, right line.
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
            
            boxes.append([bottom_line, left_line, top_line, right_line])

    return boxes

def get_pre_boxes(file):
    """
    extract box information from txt
    :param file: "xxx.txt"
    :return [[y0, x0, y1, x1, c],]
            which reflect boxes's bottom line, left line, top line, right line.
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
            
            boxes.append([bottom_line, left_line, top_line, right_line, float(box[-1])])

    return boxes

def get_iou(tru_txt, pre_txt, conf_thre):
    """
    compute iou from two result files.
    :param tru_txt, pre_txt: "xxx.txt"
    :return average iou
    """

    t_boxes = get_tru_boxes(tru_txt)
    p_boxes = get_pre_boxes(pre_txt)
    ious = []

    # iterate every box in two file and compute all their iou
    for t_box in t_boxes:
        for p_box in p_boxes:
            if p_box[-1] >= conf_thre:
                iou = compute_iou(t_box, p_box)
                ious.append(iou)
    
    return max(ious) if ious else 0


def f_score(tp, tn, fp, fn):
    """
    compute f-score
    """
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    return (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0


def calculate_kflame(tru_txt_path, pre_txt_path, file_pre, file_num, unit_size, a, b, 
        conf_thre=0.8, iou_thre=0.5):
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
    folder_pre_name = pre_txt_path
    folder_tru_name = tru_txt_path

    # use flame_truth_num and flame_pre_num to calculate the tp, tn, fp, fn.
    for i in range(unit_num+1):
        # count the number of flame of predition and truth.
        flame_truth_num = 0
        flame_pre_num = 0
        
        # iterate an unit, and judge which status it is.
        for j in range(1, unit_size+1):
            if (j + i * unit_size) > 99:
                txtname = file_pre + '_{}.txt'.format(j + i * unit_size)
            elif 10 <= (j + i * unit_size) <= 99:
                txtname = file_pre + '_0{}.txt'.format(j + i * unit_size)
            else:
                txtname = file_pre + '_00{}.txt'.format(j + i * unit_size)
            pre_txt_path = os.path.join(folder_pre_name, txtname)
            tru_txt_path = os.path.join(folder_tru_name, txtname)

            if os.path.exists(tru_txt_path):
                flame_truth_num += 1
            if os.path.exists(pre_txt_path):
                    # iou = get_iou(tru_txt_path, pre_txt_path, conf_thre)
                txt = open(pre_txt_path,'r').read().split('\n')
                for box in txt:
                    conf = float(box[-1]) if len(box) > 0 else 0
                    if conf >= conf_thre:
                        flame_pre_num += 1
                        break

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

def calculate_fscore(tru_txt_path, pre_txt_path, file_pre, file_num, conf_thre=0.8, iou_thre=0.5):
    """

    """
    # default some varities.
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    folder_pre_name = pre_txt_path
    folder_tru_name = tru_txt_path


    for j in range(1, file_num):
        t = 0
        p = 0
        if j > 99:
            txtname = file_pre + '_{}.txt'.format(j)
        elif 10 <= j <= 99:
            txtname = file_pre + '_0{}.txt'.format(j)
        else:
            txtname = file_pre + '_00{}.txt'.format(j)
        pre_txt_path = os.path.join(folder_pre_name, txtname)
        tru_txt_path = os.path.join(folder_tru_name, txtname)

        if os.path.exists(tru_txt_path):
            t = 1
        if os.path.exists(pre_txt_path):
            try:
                iou = get_iou(tru_txt_path, pre_txt_path, conf_thre)
                if iou > iou_thre:
                    p = 1
            except:
                p = 0

        # calculate the tp, tn, fp, fn.
        if p and t:
            tp += 1
        elif p and not t:
            fp += 1
        elif not p and t:
            fn += 1       
        elif not p and not t:
            tn += 1

    return f_score(tp, tn, fp, fn)

if __name__ == '__main__':
    file_pre = 'place1_whitecane01.mp4'
    file_num = 379
    print(calculate_kflame(file_pre, file_num, unit_size=16, a=0.5, b=0.5, conf_thre=0.8, iou_thre=0.5))
                