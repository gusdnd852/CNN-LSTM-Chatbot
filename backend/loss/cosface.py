import torch
from torch import nn
from torch.autograd import Variable

"""
code reference :
https://github.com/YirongMao/softmax_variants
"""


class CosFace(nn.Module):

    def __init__(self, d_model, label_dict, s=7.00, m=0.2):
        super(CosFace, self).__init__()
        self.d_model = d_model
        self.classes = len(label_dict)
        self.s = s
        self.m = m
        self.centers = nn.Parameter(torch.randn(self.classes, d_model))

    def forward(self, feat, label):
        batch_size = feat.shape[0]
        norms = torch.norm(feat, p=2, dim=-1, keepdim=True)
        nfeat = torch.div(feat, norms)

        norms_c = torch.norm(self.centers, p=2, dim=-1, keepdim=True)
        ncenters = torch.div(self.centers, norms_c)
        logits = torch.matmul(nfeat, torch.transpose(ncenters, 0, 1))

        y_onehot = torch.FloatTensor(batch_size, self.num_classes)
        y_onehot.zero_()
        y_onehot = Variable(y_onehot).cuda()
        y_onehot.scatter_(1, torch.unsqueeze(label, dim=-1), self.m)
        margin_logits = self.s * (logits - y_onehot)
        return logits, margin_logits