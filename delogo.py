import cv2
import os
import numpy as np
import argparse 

def SetPoints(windowname, img):
    """
    输入图片，打开该图片进行标记点，返回的是标记的几个点的字符串
    """
    print('(提示：单击需要标记的坐标，Enter确定，Esc下一张，其它重试。)')
    points = []

    def onMouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(temp_img, (x, y), 5, (102, 217, 239), -1)
            points.append([x, y])
            cv2.imshow(windowname, temp_img)

    temp_img = img.copy()
    cv2.namedWindow(windowname)
    cv2.imshow(windowname, temp_img)
    cv2.setMouseCallback(windowname, onMouse)
    key = cv2.waitKey(0)
    if key == 13:  # Enter
        print('坐标为：', points)
        del temp_img
        cv2.destroyAllWindows()
        return np.array(points).reshape(-1,2)
    elif key == 27:  # ESC
        print('跳过该张图片')
        del temp_img
        cv2.destroyAllWindows()
        return None
    else:
        print('重试!')
        return SetPoints(windowname, img)


def parser_args():
    """
        Parser args for input video and output video
    """

    parser = argparse.ArgumentParser(description='Video infos')
    parser.add_argument('--input',type=str,required=True,help="input video path")
    parser.add_argument('--output',type=str,required=True,help="output video path")
    parser.add_argument('--point_upper',type=int,default=720,help="标点的时候可视化的图像尺寸,与保存视频无关,仅标点")

    args = parser.parse_args()

    return args

def main(args):

    video = args.input # "video\\B1.mp4"
    out_video = args.output # "video\\out.mp4"

    img_size = args.point_upper
    _GAP = 50
    cap = cv2.VideoCapture(video)

    if not os.path.exists(video):
        print("watermark video {} not exist.".format(video))
        exit(1)

    index = 0
    get_rect = False
    rect_start = None
    rect_end = None
    frame = None
    while True:
        result, frame = cap.read()
        if not result: break

        if index % _GAP is 0 :

            if img_size > 0:
                frame = cv2.resize(frame,(img_size,img_size))

            if not get_rect:
                points = SetPoints("getPoint",frame)
                if points is None or points.shape[0]<2:
                    print("获取失败，在下一张重新获取")
                    continue

                rect_start = np.min(points,0)
                rect_end = np.max(points,0)
                get_rect = True
                break

        index += 1


    rect_frame = frame[rect_start[1]:rect_end[1],rect_start[0]:rect_end[0],:]
    cv2.imshow("rect_frame", rect_frame)

    cv2.waitKey(1000)

    _start_y = rect_start[0]
    _start_x = rect_start[1]
    _end_y = rect_end[0]
    _end_x = rect_end[1]

    if img_size > 0:
        size_ratio = np.array((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))) / img_size
        _start_y = (_start_y * size_ratio[1]).astype(np.int)
        _start_x = (_start_x * size_ratio[0]).astype(np.int)
        _end_y = (_end_y * size_ratio[1]).astype(np.int)
        _end_x = (_end_x * size_ratio[0]).astype(np.int)

    print("裁剪位置坐标：[{}, {}] [{}, {}]".format(_start_y,_start_x,_end_y,_end_x))

    result, frame = cap.read()
    naive_rect_frame = frame[_start_x:_end_x,_start_y:_end_y,:]
    cv2.imshow("naive_rect_frame", naive_rect_frame)

    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    cap.release()

    cmd = f'ffmpeg -i {video} -vf "delogo=x={_start_y}:y={_start_x}:w={_end_y-_start_y}:h={_end_x-_start_x}" {out_video}'

    try:
        os.system(cmd)
    except Exception as e:
        print("Error:{}".format(e))



if __name__ == "__main__":
    args = parser_args()
    main(args)