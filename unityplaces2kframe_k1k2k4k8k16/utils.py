import os
import xlwt
import os

def getvideo_nameandflamenum(tru_img_path):
    """
    return: video_inf, like {'place1_whitecane01.mp4':379, }
    """
    video_inf = {}

    # 找到该视频最后一帧的序号，即需要的file_num。通过这个来确定视频一共有多少帧。
    for file in os.listdir(tru_img_path):
        video_inf[file.split('mp4_')[0] + 'mp4'] = int(file.split('mp4_')[1][:3])
    
    return video_inf

def calculate_tpfptnfn_kframe(tru_txt_path, pre_txt_path, file_pre, file_num, unit_size, a, b, 
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
        
        # iterate an unit, and classify which status it is.
        for j in range(1, unit_size+1):
            if (j + i * unit_size) > 99:
                txtname = file_pre + '_{}.txt'.format(j + i * unit_size)
            elif 10 <= (j + i * unit_size) <= 99:
                txtname = file_pre + '_0{}.txt'.format(j + i * unit_size)
            else:
                txtname = file_pre + '_00{}.txt'.format(j + i * unit_size)
            pre_txt_path = os.path.join(folder_pre_name, txtname)
            tru_txt_path = os.path.join(folder_tru_name, txtname)

            if os.path.exists(tru_txt_path) and open(tru_txt_path).read():
                flame_truth_num += 1
            if os.path.exists(tru_txt_path) and open(tru_txt_path).read() and os.path.exists(pre_txt_path):
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
    
    return (tp,fp,tn,fn)

def calculate_fscore(tp, tn, fp, fn):
    """
    compute f-score
    """
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    return (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

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

def calculate_tpfptnfn_k1(tru_txt_path, pre_txt_path, file_pre, file_num, conf_thre=0.8, iou_thre=0.5):
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

    return (tp,fp,tn,fn)


def write_excel(results, file_pre):
    """
    write the results of k-frame to excel file.
    :param results: [[k, a, b, f-score],]
    :return none
    """
    # create 'result' filter
    if not os.path.exists('result'):
        os.mkdir('result')
        
    # default format 
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('k-frame result',cell_overwrite_ok=True)
    row0 = ('', 'β', '1/16', '2/16', '3/16', '4/16', '5/16', '6/16', '7/16', '8/16', '9/16', '10/16', '11/16', '12/16', '13/16', '14/16', '15/16', '1')
    col0 = ('k=1', 'k=2', 'k=4', 'k=8', 'k=16')
    col1 = ('a=1',
            'a=1/2', 'a=1',
            'a=1/4', 'a=2/4','a=3/4','a=1',
            'a=1/8','a=2/8','a=3/8','a=4/8','a=5/8','a=6/8','a=7/8','a=1',
            'a=1/16','a=2/16','a=3/16','a=4/16','a=5/16','a=6/16','a=7/16','a=8/16','a=9/16','a=10/16','a=11/16','a=12/16','a=13/16','a=14/16','a=15/16','a=1',
            )

    # write default format
    for i in range(len(row0)):
        sheet.write(0, i, row0[i])
    for i in range(len(col1)):
        sheet.write(i+1, 1, col1[i])
    sheet.write(1, 0, col0[0])
    sheet.write(2, 0, col0[1])
    sheet.write(4, 0, col0[2])
    sheet.write(8, 0, col0[3])
    sheet.write(16, 0, col0[4])

    # create a dic to give results the position(row) to write, (k, a): row
    r = 1
    dic = {}
    for i in (1, 2, 4, 8, 16):
        for j in range(1, i+1):
            dic[(i, j)] = r
            r += 1

    # write k-frame results
    for result in results:
        k = result[0]
        a = result[1]
        if k == 1:
            sheet.write(dic[(k, a)], 17, result[3])
        else:
            sheet.write(dic[(k, a)], result[2]+1, result[3])
    
    # save excel file
    name = f'k-frame_{file_pre}.xls'
    book.save(fr'result/{name}')
    print(name,'已保存。')


if __name__ == '__main__':
    write_excel(0, '212')