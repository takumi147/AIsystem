from kframe import calculate_f_score
from result_to_excel import write_excel


if __name__ == "__main__":
    file_pre = 'place1_whitecane01.mp4'
    file_num = 878  # the number of truth flames  
    results = []
    for k in (2, 4, 8, 16):
        a_start = int(k/2)
        for a in range(a_start, k+1):
            for b in range(8, 17):
                result = [k, a, b, calculate_f_score(file_pre, file_num, unit_size=k, a=a/k, b=b/16, conf_thre=0.8, iou_thre=0.8)]
                results.append(result)
    write_excel(results)
    print('程序结束！')