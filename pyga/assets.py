import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(9,8)
        self.act = nn.Sigmoid()
    def forward(self,x):
        out = self.l1(x)
        out = self.act(out)
        return out
model = Net()
class settings:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.model = model
        self.vy = 0
        self.opp_vy = 0
        self.fitness = 0
        self.color = color
        self.width = 10
        self.height = 20
        self.on_ground = False
        self.is_alive = True
        self.distance = 0
class squ(settings):
    pass
class opp_squ(settings):
    pass
    