2022/09
1. 决定在之前的k-frame基础上增加iou这一参数，增加了对模型效果的评估。避免因为预测图中有白杖但没检测出，却把栏杆当成白杖，
这种预测图不能算严格的P样本。
Q:
1. 针对不能移动的容易被检测的物体，比如栏杆水管，希望增加一种过滤手段。避免系统在实际没有白杖的情况下误识别出白杖。

2022/11/15
1. 最终决定用预测图片和实际图片之间每组中最大的iou进行计算k-frame，而不是平均iou。换句话说，模型可以误检测，但是只要检测
出真实的白杖，就无所谓误检测。
2. 使用人为设定的黑名单来过滤不能移动的物体。
Q:
1. 人为设定黑名单过于麻烦。首先需要针对场景进行调试，其次如果场景中容易被误检测的物体被移动了，比如研究室里的可移动白板，
其支柱容易被误检测，但白板容易被碰撞产生位移。

2022/11/23
1. 更新黑名单机制，使用一个暂时的(比如5秒)黑名单来记忆检测出的所有box，然后在下一个5秒时屏蔽上一个5秒所检测出的所有box，
每5秒更新一次黑名单(黑名单=暂时的黑名单)。以place3为场景的实验结果通过肉眼观察，间隔为5帧的时候效果最好。
Q:
1. 实验发现，如果栏杆被人所遮挡一段时间，则该区域只会部分或者不会完全进入黑名单，导致误检测再次出现。尤其当栏杆逐渐显露
出来的时候。由于必须实时对黑名单进行更新，这个问题显得尤为复杂。
似乎回到了最初的问题，白杖被遮挡无法被检测，那么栏杆被遮挡如何被检测出来呢。

2022/11/25
1. 加入了计数器，现在更新黑名单的时候，该box的出现次数必须满足一定数量，才能进入黑名单。
Q:
1. 还是栏杆被遮挡，逐渐出现时还是会检测到。
2. 黑名单显示有3个，但其实应该有2个，确实因此出现了漏检，而且有3个的话，为什么拉杆没有被屏蔽呢？需要进一步debug。

2022/11/29
1. 针对11/25的问题1优化了更新黑名单的算法，现在更新黑名单的时候，计数用的黑名单(tmpbl)不再从[]开始，而是将更新后的黑名单
中的每一个box都以计数1的情况加入计数用黑名单。这样即使栏杆被遮挡，误检测出部分栏杆的时候，也将划分到整个栏杆属于的box中去。
顺便一提也可以用增加更新黑名单时的时间间隔来解决。
2. 针对11/25的问题2，发现是时间间隔太短，白杖还没有从原来的地方离开。所以多更新了一个黑名单。只能通过增加更新黑名单时的时
间间隔（后称“更新间隔”）来解决。
Q:
1. 实验发现，更新间隔太短的话，使用黑名单机制会导致k-frame评价变差（原因见11/25的问题2），增加更新间隔后也只能恢复至不使用
黑名单机制的效果。令人沮丧，有跟没有这机制，并没有区别。
到此为止，一个iou机制，一个黑名单机制，都不能在现有数据集上显示出有效提升，针对iou机制，需要拍摄：在误检测出背景（栏杆）的
时候，人拿着拐杖过去，但是拐杖没检测出来的情况。听上去有点离谱，但这种情况普遍出现在使用黑名单机制后的检测结果，可以增加实
验结果的可信度。
针对黑名单机制，需要拍摄：在误检测出背景（栏杆）的时候，人没有拿着拐杖过去。使用黑名单机制后把fp变成tn，应该可以提升k-
frame评价。
2. 检测图片的时候，yolo的顺序是1->10->100->101，不符合期望的1->2->3，需要把文件名中的1改成001，10改成010。为此创建了
change_txt_1_001.py，批量完成。
R:(recommend)
1. 所以模型不行你跟我说毛系统呢，天天跟我说模型效果不能达到100%所以要用系统微调，我信你个鬼，模型连大范围的时间内都检测不
出来的话，K-frame就是搞笑。想搞模型就跟我说，nonono这样别人就研究过了，不是独创，我tm泥头车创si你，资料少又不主流，我掉
头发给你想是吧。
老子就是要搞模型，搞训练策略，你捶死我。

2022/12/23
1. 现在可以自动化计算多个place的kframe。
2. 现在a从1/k开始，b从1/16开始。