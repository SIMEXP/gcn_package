import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric as tg
# import torch_geometric_temporal as tgt
import numpy as np

class YuGCN(torch.nn.Module):
    def __init__(self, edge_index, edge_weight, n_timepoints=50, n_classes=2):
        super().__init__()
        self.edge_index = edge_index
        self.edge_weight = edge_weight
        self.conv1 = tg.nn.ChebConv(in_channels=n_timepoints,out_channels=32,K=2,bias=True)
        self.conv2 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv3 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv4 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv5 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv6 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.fc1 = nn.Linear(512 * 32, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, n_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):

        x = self.conv1(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv2(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv3(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv4(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv5(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv6(x, self.edge_index, self.edge_weight)
        x = tg.nn.global_mean_pool(x,torch.from_numpy(np.array(range(x.size(0)),dtype=int)))

        x = x.view(-1, 512 * 32)
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x

class LoicGCN(torch.nn.Module):
    def __init__(self, edge_index, edge_weight, n_timepoints=50, n_classes=2):
        super().__init__()
        self.edge_index = edge_index
        self.edge_weight = edge_weight
        self.conv1 = tg.nn.ChebConv(in_channels=n_timepoints, out_channels=32, K=2, bias=True)
        self.conv2 = tg.nn.ChebConv(in_channels=32, out_channels=32, K=2, bias=True)
        self.conv3 = tg.nn.ChebConv(in_channels=32, out_channels=16, K=2, bias=True)
        self.fc1 = nn.Linear(512*16, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, n_classes)
        self.dropout = nn.Dropout(0.2)
        # adding persistent buffer for edges serialization
        # self.register_buffer('edge_index', edge_index)
        # self.register_buffer('edge_weight', edge_weight)

    def forward(self, x):
        x = self.conv1(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.conv3(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.dropout(x)
        x = tg.nn.global_mean_pool(x, torch.from_numpy(np.array(range(x.size(0)), dtype=int)))
        x = x.view(-1, 512*16)
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x

class STGCN(torch.nn.Module):
    def __init__(self, edge_index, edge_weight, n_timepoints=50, n_classes=2):
        super().__init__()
        self.edge_index = edge_index
        self.edge_weight = edge_weight
        self.conv1 = tg.nn.ChebConv(in_channels=n_timepoints, out_channels=32, K=2, bias=True)
        self.conv2 = tg.nn.ChebConv(in_channels=32, out_channels=32, K=2, bias=True)
        self.conv3 = tg.nn.ChebConv(in_channels=32, out_channels=16, K=2, bias=True)
        # self.recurent = tgt.nn.recurrent.STConv(in_channels=16, out_channels=16, K=2, hidden_channels=4, kernel_size=10)
        self.fc1 = nn.Linear(512*16, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, n_classes)
        self.dropout = nn.Dropout(0.2)
        # adding persistent buffer for edges serialization
        # self.register_buffer('edge_index', edge_index)
        # self.register_buffer('edge_weight', edge_weight)

    def forward(self, x):
        x = self.conv1(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.conv3(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.dropout(x)
        # x = self.recurent(x)
        # x = F.relu(x)
        # x = self.dropout(x)
        x = tg.nn.global_mean_pool(x, torch.from_numpy(np.array(range(x.size(0)), dtype=int)))
        x = x.view(-1, 512*16)
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)

        return x


class HaoGCN(torch.nn.Module):
    def __init__(self, edge_index, edge_weight, batch_size, n_roi, n_timepoints=50, n_classes=2):
        super().__init__()
        self.edge_index = edge_index
        self.edge_weight = edge_weight
        self.batch_size, self.n_roi = batch_size, n_roi
        self.conv1 = tg.nn.ChebConv(in_channels=n_timepoints,out_channels=32,K=2,bias=True)
        self.conv2 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv3 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv4 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv5 = tg.nn.ChebConv(in_channels=32,out_channels=32,K=2,bias=True)
        self.conv6 = tg.nn.ChebConv(in_channels=32,out_channels=batch_size,K=2,bias=True)
        self.fc1 = nn.Linear(batch_size * n_roi, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, n_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):

        x = self.conv1(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv2(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv3(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv4(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv5(x, self.edge_index, self.edge_weight)
        x = F.relu(x)
        x = self.conv6(x, self.edge_index, self.edge_weight)
        x = tg.nn.global_mean_pool(x,torch.from_numpy(np.array(range(x.size(0)),dtype=int)))

        x = x.view(-1, self.batch_size * self.n_roi)
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x
