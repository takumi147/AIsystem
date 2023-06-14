"""
The bounding boxes detected by yolo will be neglected if they are in static-object-list(sol).
mechanism:
In m flames, repeated boxes at same position are counted in a temporary static-object-list.
This tmpsols will refresh sols every m flames. 
"""


def in_sols(sols, xywh):
    # if xywh in sol, return True.
    # sols: [[xywh],].
    if not sols:
        return False
    xyxy = my_xywh2xyxy(xywh)
    sols = [my_xywh2xyxy(i) for i in sols]
    for sol in sols:
        if sol[0] <= xyxy[0] and sol[1] >= xyxy[1]\
            and sol[2] >= xyxy[2] and sol[3] <= xyxy[3]:
            return True
    return False

def in_tmpsol(tmpsol, xywh):
    # if xywh in temporary sol, return True.
    # tmpsol: [xywhc], c is count, not conf_threshold.
    if not tmpsol:
        return False
    xyxy = my_xywh2xyxy(xywh)
    tmpsol = my_xywh2xyxy(tmpsol[:-1])
    if tmpsol[0] <= xyxy[0] and tmpsol[1] >= xyxy[1]\
        and tmpsol[2] >= xyxy[2] and tmpsol[3] <= xyxy[3]:
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

def refreshsols(sols, tmpsols, size, seta):
    """
    replace sols with tmpsols.
    para:
    sols: [[xywh],]
    tmpsols: [[xywhc],], c is count.
    seta should be between 0~1
    return:
    sols, tmpsols
    """
    sols = [box[:-1] for box in tmpsols if box[-1] >= int(size*seta)]
    tmpsols = [box + [1] for box in sols]
    return sols, tmpsols

    
if __name__ == '__main__':
    # pred = [torch.tensor([[3.71641e+02, 3.61843e+01, 5.70891e+02, 3.73188e+02, 8.79886e-01, 0.00000e+00],
    #     [2.20988e+02, 2.30655e+02, 2.48304e+02, 3.67026e+02, 6.75375e-01, 2.70000e+01],
    #     [6.14922e+01, 1.08630e+02, 3.57368e+02, 3.71859e+02, 6.66169e-01, 0.00000e+00],
    #     [4.89497e+02, 1.68791e+02, 5.12649e+02, 2.19763e+02, 2.61550e-01, 2.70000e+01]], device='cpu')]
    # print(bl_delete(pred, [[485,170,520,210],]))

    x = '0 0.354167 0.348611 0.075 0.112037 0.332626'
    x = my_xywh2xyxy(x)
    print(x)