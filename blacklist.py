import torch

def ssbl_delete(pred, blists = []):
    """
    para: 
        pred is tensor(xyxy), xy1 is left-top, xy2 is right-bottom. then conf, cls.
        i.e. [tensor([[3.71641e+02, 3.61843e+01, 5.70891e+02, 3.73188e+02, 8.79886e-01, 0.00000e+00],
        [2.20988e+02, 2.30655e+02, 2.48304e+02, 3.67026e+02, 6.75375e-01, 2.70000e+01],
        [6.14922e+01, 1.08630e+02, 3.57368e+02, 3.71859e+02, 6.66169e-01, 0.00000e+00],
        [4.89497e+02, 1.68791e+02, 5.12649e+02, 2.19763e+02, 2.61550e-01, 2.70000e+01]], device='cuda:0')]
    return tensors without boxes in blacklist 
    """
    if not blists:
        return pred

    r = []
    for i in pred[0]:
        for j in blists:
            if i[0] >= j[0] and i[1] <= j[1] \
                and i[2] <= j[2] and i[3] >= j[3]:
                continue
            else:
                r.append(i)
    return list(set(r))


def ssmy_xywh2xyxy(x):
    # Convert nx6 boxes from '0, x, y, w, h, c' to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    x = x.split(' ')
    x = list(map(float, x))

    y = [0] * 4
    y[0] = (x[1] - x[3]/2)
    y[1] = (x[2] + x[4]/2)
    y[2] = (x[1] + x[3]/2)
    y[3] = (x[2] - x[4]/2)
    return y

def in_blacklists(blacklists, xywh):
    # if xywh in blacklist, return True
    # blacklist: [xywh]
    if not blacklists:
        return False
    xyxy = my_xywh2xyxy(xywh)
    blacklists = [my_xywh2xyxy(i) for i in blacklists]
    for blacklist in blacklists:
        if blacklist[0] <= xyxy[0] and blacklist[1] >= xyxy[1]\
            and blacklist[2] >= xyxy[2] and blacklist[3] <= xyxy[3]:
            return True
    return False

def in_tmpbl(box, xywh):
    # if xywh in tmp, return True
    # box: [xywhc]
    if not box:
        return False
    xyxy = my_xywh2xyxy(xywh)
    box = my_xywh2xyxy(box[:-1])
    if box[0] <= xyxy[0] and box[1] >= xyxy[1]\
        and box[2] >= xyxy[2] and box[3] <= xyxy[3]:
        return True
    return False

def my_xywh2xyxy(xywh):
    # list xywh to xyxy
    xyxy = [0] * 4
    xyxy[0] = xywh[0] - xywh[2]/2
    xyxy[1] = xywh[1] + xywh[3]/2
    xyxy[2] = xywh[0] + xywh[2]/2
    xyxy[3] = xywh[1] - xywh[3]/2
    return xyxy

def enlarge_box(xywh, scale=1.2):
    # elarge box， xywh is [x,y,w,h]
    return [xywh[0], xywh[1], xywh[2]*scale, xywh[3]*scale]

def refreshbl(bl, tmpbl, size, scale):
    # replace bl with tmpbl, scale should be between 0~1
    bl = [box[:-1] for box in tmpbl if box[-1] >= int(size*scale)]
    tmpbl = [box + [1] for box in bl]
    return bl, tmpbl


if __name__ == '__main__':
    # pred = [torch.tensor([[3.71641e+02, 3.61843e+01, 5.70891e+02, 3.73188e+02, 8.79886e-01, 0.00000e+00],
    #     [2.20988e+02, 2.30655e+02, 2.48304e+02, 3.67026e+02, 6.75375e-01, 2.70000e+01],
    #     [6.14922e+01, 1.08630e+02, 3.57368e+02, 3.71859e+02, 6.66169e-01, 0.00000e+00],
    #     [4.89497e+02, 1.68791e+02, 5.12649e+02, 2.19763e+02, 2.61550e-01, 2.70000e+01]], device='cpu')]
    # print(bl_delete(pred, [[485,170,520,210],]))

    x = '0 0.354167 0.348611 0.075 0.112037 0.332626'
    x = my_xywh2xyxy(x)
    print(x)