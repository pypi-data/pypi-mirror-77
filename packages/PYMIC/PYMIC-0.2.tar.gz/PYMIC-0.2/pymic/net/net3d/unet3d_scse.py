# -*- coding: utf-8 -*-
from __future__ import print_function, division

import torch
import torch.nn as nn
import numpy as np
from pymic.layer.activation import get_acti_func
from pymic.layer.convolution import ConvolutionLayer
from pymic.layer.deconvolution import DeconvolutionLayer

class UNetBlock(nn.Module):
    def __init__(self,in_channels, out_channels, acti_func, acti_func_param):
        super(UNetBlock, self).__init__()
        
        self.in_chns   = in_channels
        self.out_chns  = out_channels
        self.acti_func = acti_func

        self.conv1 = ConvolutionLayer(in_channels,  out_channels, 3, 
                padding = 1, acti_func=get_acti_func(acti_func, acti_func_param))
        self.conv2 = ConvolutionLayer(out_channels, out_channels, 3, 
                padding = 1, acti_func=get_acti_func(acti_func, acti_func_param))

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        return x

class SCSEBlock(nn.Module):
    def __init__(self, in_chns):
        super(SCSEBlock, self).__init__()
        self.in_chns = in_chns 
        half_chns    = int(in_chns / 2)

        self.conv_s = nn.Conv3d(self.in_chns, 1,
                kernel_size = 1, bias = True)

        self.glb_pool = nn.AdaptiveAvgPool3d(1)
        self.conv_c_1 = nn.Conv3d(self.in_chns, half_chns,
                kernel_size = 1, bias = True)
        self.conv_c_2 = nn.Conv3d(half_chns, self.in_chns,
                kernel_size = 1, bias = True)
        self.act_relu = nn.ReLU()
        self.act_sigm = nn.Sigmoid()

    def forward(self, x):
        # get spatial attention coefficient
        att_s = self.conv_s(x)
        att_s = self.act_sigm(att_s)

        # get channel attention coefficient
        
        x_pool = self.glb_pool(x)
        att_c  = self.conv_c_1(x_pool)
        att_c  = self.act_relu(att_c)
        att_c  = self.conv_c_2(att_c)
        att_c  = self.act_sigm(att_c)

        y_s = x * att_s 
        y_c = x * att_c   
        output = torch.max(y_s, y_c)
        return output, att_s

class UNet3DSCSE(nn.Module):
    def __init__(self, params):
        super(UNet3DSCSE, self).__init__()
        self.params = params
        self.in_chns   = self.params['in_chns']
        self.ft_chns   = self.params['feature_chns']
        self.n_class   = self.params['class_num']
        self.acti_func = self.params['acti_func']
        self.dropout   = self.params['dropout']
        self.ouput_att = self.params.get('output_att', False)
        self.resolution_level = len(self.ft_chns)
        assert(self.resolution_level == 5 or self.resolution_level == 4)

        self.block1 = UNetBlock(self.in_chns, self.ft_chns[0], 
             self.acti_func, self.params)

        self.block2 = UNetBlock(self.ft_chns[0], self.ft_chns[1], 
             self.acti_func, self.params)

        self.block3 = UNetBlock(self.ft_chns[1], self.ft_chns[2], 
             self.acti_func, self.params)

        self.block4 = UNetBlock(self.ft_chns[2], self.ft_chns[3], 
             self.acti_func, self.params)

        if(self.resolution_level == 5):
            self.block5 = UNetBlock(self.ft_chns[3], self.ft_chns[4], 
                 self.acti_func, self.params)

            self.block6 = UNetBlock(self.ft_chns[3] * 2, self.ft_chns[3], 
                 self.acti_func, self.params)

        self.block7 = UNetBlock(self.ft_chns[2] * 2, self.ft_chns[2], 
             self.acti_func, self.params)

        self.block8 = UNetBlock(self.ft_chns[1] * 2, self.ft_chns[1], 
             self.acti_func, self.params)

        self.block9 = UNetBlock(self.ft_chns[0] * 2, self.ft_chns[0], 
             self.acti_func, self.params)

        self.down1 = nn.MaxPool3d(kernel_size = 2)
        self.down2 = nn.MaxPool3d(kernel_size = 2)
        self.down3 = nn.MaxPool3d(kernel_size = 2)
        if(self.resolution_level == 5):
            self.down4 = nn.MaxPool3d(kernel_size = 2)

            self.up1 = DeconvolutionLayer(self.ft_chns[4], self.ft_chns[3], kernel_size = 2,
                stride = 2, acti_func = get_acti_func(self.acti_func, self.params))
        self.up2 = DeconvolutionLayer(self.ft_chns[3], self.ft_chns[2], kernel_size = 2,
            stride = 2, acti_func = get_acti_func(self.acti_func, self.params))
        self.up3 = DeconvolutionLayer(self.ft_chns[2], self.ft_chns[1], kernel_size = 2,
            stride = 2, acti_func = get_acti_func(self.acti_func, self.params))
        self.up4 = DeconvolutionLayer(self.ft_chns[1], self.ft_chns[0], kernel_size = 2,
            stride = 2, acti_func = get_acti_func(self.acti_func, self.params))

        if(self.dropout > 0.0):
             self.drop3 = nn.Dropout(self.dropout)
             self.drop4 = nn.Dropout(self.dropout)
             if(self.resolution_level == 5):
                  self.drop5 = nn.Dropout(self.dropout)
        if(self.resolution_level == 5):          
            self.scse6 = SCSEBlock(self.ft_chns[3])
        self.scse7 = SCSEBlock(self.ft_chns[2])
        self.scse8 = SCSEBlock(self.ft_chns[1])
        self.scse9 = SCSEBlock(self.ft_chns[0])

        self.conv = nn.Conv3d(self.ft_chns[0], self.n_class, 
            kernel_size = 3, padding = 1)

    def forward(self, x):
        f1 = self.block1(x)
        d1 = self.down1(f1)

        f2 = self.block2(d1)
        d2 = self.down2(f2)

        f3 = self.block3(d2)
        if(self.dropout):
             f3 = self.drop3(f3)
        d3 = self.down3(f3)

        f4 = self.block4(d3)
        if(self.dropout):
             f4 = self.drop4(f4)

        if(self.resolution_level == 5):
            d4 = self.down4(f4)
            f5 = self.block5(d4)
            if(self.dropout):
                 f5 = self.drop5(f5)

            f5up  = self.up1(f5)
            f4cat = torch.cat((f4, f5up), dim = 1)
            f6    = self.block6(f4cat)
            f6, att_s6 = self.scse6(f6)

            f6up  = self.up2(f6)
            f3cat = torch.cat((f3, f6up), dim = 1)
        else:
            f4up  = self.up2(f4)
            f3cat = torch.cat((f3, f4up), dim = 1)
        f7    = self.block7(f3cat)
        f7, att_s7 = self.scse7(f7)

        f7up  = self.up3(f7)
        f2cat = torch.cat((f2, f7up), dim = 1)
        f8    = self.block8(f2cat)
        f8, att_s8  = self.scse8(f8)

        f8up  = self.up4(f8)
        f1cat = torch.cat((f1, f8up), dim = 1)
        f9    = self.block9(f1cat)
        f9, att_s9  = self.scse9(f9)

        output = self.conv(f9)
        if(self.ouput_att):
            return att_s9
        else:
            return output

if __name__ == "__main__":
    params = {'input_chn_num':4,
              'feature_chn_nums':[2, 8, 32, 48, 64],
              'class_num': 2}
    Net = UNet3DSCSE(params)
    Net = Net.double()

    x  = np.random.rand(4, 4, 96, 96, 96)
    xt = torch.from_numpy(x)
    xt = torch.tensor(xt)
    
    y = Net(xt)
    y = y.detach().numpy()
    print(y.shape)
