import os
from email.base64mime import body_encode
from blacklist import in_tmpbl, enlarge_box, in_blacklists, my_yxyxc2xywh


"""
file construct:
kframe.py
|-pre-xxxx.txt
|-tru-xxxx.txt

kframe2.py是在一个unit内，先遍历所有label，把不动的box列进blacklist里，再遍历所有的label，跳过blacklist计算混沌矩阵。
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

def get_pre_boxes_yxyxc(file):
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
    # pre_txt: [n, x, y, w, h, c] to [bottom line, left line, top line, right line, c], yxyxc
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


def get_pre_boxes_xywhc(file):
    """
    param: file path
    return: [[xywhc],]
    """
    # get [' x y w h','']
    txt = open(file, 'r').read().split('\n')
    txt = [i.split(' ')[1:] for i in txt if i]
    for i in range(len(txt)):
        txt[i] = [float(j) for j in txt[i]]
    return txt


def get_iou_txt(tru_txt, pre_txt, conf_thre, bls):
    """
    compute iou from two result files.
    :param tru_txt, pre_txt: "xxx.txt"
    :return average iou
    """

    t_boxes = get_tru_boxes(tru_txt)
    p_boxes = get_pre_boxes_yxyxc(pre_txt)
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


def calculate_f_score(file_pre='', file_num=0, unit_size=16, a=0.5, b=0.5, conf_thre=0.8, iou_thre=0.5, c=0.5):
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
    for i in range(unit_num):
        # count the number of flame of predition and truth.
        flame_truth_num = 0
        flame_pre_num = 0
        bls = []  # if bls is empty, for bl in bls won't execute

        # iterate an unit to generate the blacklist
        for j in range(1, unit_size+1):
            n = j + i * unit_size
            if 0 <= n < 10:
                n = '00' + str(n)
            elif 10 <= n < 100:
                n = '0' + str(n)
            else:
                n = str(n)    
            txtname = file_pre + '_{}.txt'.format(n)
            pre_txt_path = os.path.join(folder_pre_name, txtname)
            boxes = get_pre_boxes_xywhc(pre_txt_path)
            for box in boxes:
                for bl in bls.copy():
                    if in_tmpbl(bl, box):
                        bl[-1] += 1
                        break
                else:
                    bls.append(enlarge_box(box) + [1]) 

        bls = [i[:-1] for i in bls if int(i[-1]) >= unit_size * c]
        print('unit size:', unit_size, 'i:', i, 'bls:', bls)

        # iterate an unit, and judge which status it is.
        for j in range(1, unit_size+1):
            n = j + i * unit_size
            if 0 <= n < 10:
                n = '00' + str(n)
            elif 10 <= n < 100:
                n = '0' + str(n)
            else:
                n = str(n)    
            txtname = file_pre + '_{}.txt'.format(n)
            pre_txt_path = os.path.join(folder_pre_name, txtname)
            tru_txt_path = os.path.join(folder_tru_name, txtname)

            if os.path.exists(tru_txt_path):
                flame_truth_num += 1
            if os.path.exists(pre_txt_path):
                p_boxes = get_pre_boxes_xywhc(pre_txt_path)
                p_boxes = [i for i in p_boxes if not in_blacklists(bls, i[:-1])]
                if p_boxes:
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
                