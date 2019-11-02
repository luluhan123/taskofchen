#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-10-22 22:38:01
# @Author  : han lulu (han.fire@foxmail.com)
# @Link    : https://github.com/luluhan123/
# @Version : $Id$

import os
from .BasicModule import BasicModule
from torch import nn
from torch.nn import functional as F


class ResidualBlock(nn.Module):
    '''
    实现子module: Residual Block
    '''

    def __init__(self, inchannel, outchannel, stride=1, shortcut=None):
        super(ResidualBlock, self).__init__()
        self.left = nn.Sequential(
            nn.Conv2d(inchannel, outchannel, 3, stride, 1, bias=False),
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),
            nn.Conv2d(outchannel, outchannel, 3, 1, 1, bias=False),
            nn.BatchNorm2d(outchannel))
        self.right = shortcut

    def forward(self, x):
        out = self.left(x)
        residual = x if self.right is None else self.right(x)
        out += residual
        return F.relu(out)


class ResNet34(BasicModule):
    '''
    实现主module：ResNet34
    ResNet34包含多个layer，每个layer又包含多个Residual block
    用子module来实现Residual block，用_make_layer函数来实现layer
    '''

    def __init__(self, num_classes=2):
        super(ResNet34, self).__init__()
        self.model_name = 'resnet34'

        # 前几层: 图像转换
        self.pre = nn.Sequential(
            nn.Conv2d(3, 64, 7, 2, 3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2, 1))

        # 重复的layer，分别有3，4，6，3个residual block
        self.layer1 = self._make_layer(64, 128, 3)
        self.layer2 = self._make_layer(128, 256, 4, stride=2)
        self.layer3 = self._make_layer(256, 512, 6, stride=2)
        self.layer4 = self._make_layer(512, 512, 3, stride=2)

        # 分类用的全连接
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, inchannel, outchannel, block_num, stride=1):
        '''
        构建layer,包含多个residual block
        '''
        shortcut = nn.Sequential(
            nn.Conv2d(inchannel, outchannel, 1, stride, bias=False),
            nn.BatchNorm2d(outchannel))

        layers = []
        layers.append(ResidualBlock(inchannel, outchannel, stride, shortcut))

        for i in range(1, block_num):
            layers.append(ResidualBlock(outchannel, outchannel))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.pre(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = F.avg_pool2d(x, 16)  # 512->256->128->64->32->16
        x = x.view(x.size(0), -1)
        return self.fc(x)

    # 定义权值初始化
    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                torch.nn.init.xavier_normal_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                torch.nn.init.normal_(m.weight.data, 0, 0.01)
                m.bias.data.zero_()


# finetune
'''
net = Net()     # 创建一个网络

# ================================ #
#        finetune 权值初始化
# ================================ #

# load params
pretrained_dict = torch.load('net_params.pkl')

# 获取当前网络的dict
net_state_dict = net.state_dict()

# 剔除不匹配的权值参数
pretrained_dict_1 = {k: v for k, v in pretrained_dict.items() if k in net_state_dict}

# 更新新模型参数字典
net_state_dict.update(pretrained_dict_1)

# 将包含预训练模型参数的字典"放"到新模型中
net.load_state_dict(net_state_dict)
'''

# 为不同层设置不同的学习率
'''
# 将fc3层的参数从原始网络参数中剔除
ignored_params = list(map(id, net.fc3.parameters()))
base_params = filter(lambda p: id(p) not in ignored_params, net.parameters())

# 为fc3层设置需要的学习率
optimizer = optim.SGD([
    {'params': base_params},
    {'params': net.fc3.parameters(), 'lr': lr_init*10}],  lr_init, momentum=0.9, weight_decay=1e-4)

criterion = nn.CrossEntropyLoss()                                                   # 选择损失函数
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.1)     # 设置学习率下降策略
'''
