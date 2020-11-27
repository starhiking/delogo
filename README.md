# 可选位置去除视频水印

（交互式选则） （选择合适帧，开头帧可能没有水印的情况）

dependices: python + opencv + ffmpeg

原理: 利用opencv进行视频解析,找到合适帧之后选则水印位置,利用ffmpeg进行去除水印.

cmd: `python delogo.py --input {i_video_path} --output {o_video_path}`

example: `python delogo.py --input video\\B2.mp4 --output video\\out.mp4` (可以下载视频看效果)

---

ffmpeg的效果比CVPR17年的论文[Dekel_On_the_Effectiveness](http://openaccess.thecvf.com/content_cvpr_2017/papers/Dekel_On_the_Effectiveness_CVPR_2017_paper.pdf)(复现[地址](https://github.com/starhiking/de_watermark_video)) 要好,主要体现在速度上.

操作平台用的windows, [ffmpeg](http://ffmpeg.org/download.html) 需要单独安装,并且 <strong>bin</strong> 目录需要放到path环境变量中。

linux没有进行测试，欢迎直接PR
