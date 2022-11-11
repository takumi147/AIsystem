from email.base64mime import body_encode


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
    # [n, x, y, w, h, c] to [bottom line, left line, top line, right line]
    for box in txt:
        if box:
            box = box.split(' ')
            bottom_line = float(box[2]) - float(box[4][:-2])/2
            left_line = float(box[1]) - float(box[3])/2
            top_line = float(box[2]) + float(box[4][:-2])/2
            right_line = float(box[1]) + float(box[3])/2
            boxes.append([bottom_line, left_line, top_line, right_line])

    return boxes

def get_iou(file1, file2):
    """
    compute iou from two result files.
    :param file1, file2: "xxx.txt"
    :return average iou
    """

    box1 = get_box(file1)
    box2 = get_box(file2)
    iou = 0

    # iterate every box in two file and compute all their iou
    for i in box1:
        for j in box2:
            iou += compute_iou(i, j)
    
    return (iou / (len(box1) * len(box2)))


if __name__ == "__main__":
    pass