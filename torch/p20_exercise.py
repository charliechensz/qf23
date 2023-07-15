# 导入需要的包
import torch
from torch import nn
import pandas as pd
import matplotlib.pyplot as plt

# 封装数据处理函数
def process_data(filepath):
    """
    读取并处理信用卡欺诈数据集
    """
    df = pd.read_csv(filepath)
    
    # 删除时间戳列
    del df['Time']
    
    # 获分类标签和特征
    y = df['Class'].values
    X_columns = [c for c in df.columns if c != 'Class']
    X = df[X_columns].values
    
    # 返回分割并转换为Tensor的数据
    return torch.from_numpy(X).float(), torch.from_numpy(y).float()

# 封装模型类
class FraudModel(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim):
        """
        定义模型结构
        参数:
            input_dim: 输入特征维度
            hidden_dims: 隐层神经元数量
            output_dim: 输出维度
        """
        super().__init__()
        
        # 定义网络层
        self.layers = nn.ModuleList([
            nn.Linear(input_dim, hidden_dims[0]),
            nn.ReLU(),
            nn.Linear(hidden_dims[0], hidden_dims[1]),
            nn.ReLU(),
            nn.Linear(hidden_dims[1], output_dim),
            nn.Sigmoid()
        ])
        
    def forward(self, x):
        # 前向传播
        for layer in self.layers:
            x = layer(x)
        return x
    
# 封装模型训练和评估    
class FraudTrainer():
    
    def __init__(self, model, train_data, val_data, config):
        """
        参数:
            model: 定义的神经网络模型
            train_data: 训练数据
            val_data: 验证数据
            config: 训练超参数配置字典
        """
        self.model = model
        self.train_data = train_data
        self.val_data = val_data
        self.config = config
        
    def train(self):
        """模型训练"""
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config['lr']) 
        loss_fn = nn.BCELoss()
        
        train_inputs, train_labels = self.train_data
        val_inputs, val_labels = self.val_data
        
        # 训练循环
        losses = [] # 记录loss
        for epoch in range(self.config['epochs']):
            for x, y in DataLoader(TensorDataset(train_inputs, train_labels), 
                                   batch_size=self.config['batch_size']):
                pred = self.model(x)
                loss = loss_fn(pred, y)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            
            # 记录和输出loss
            losses.append(loss_fn(self.model(train_inputs), train_labels)) 
            print(f'Epoch {epoch+1}, Train Loss: {losses[-1]:.4f}')
        
        return losses
        
    def evaluate(self):
        """在验证集上评估模型"""
        val_inputs, val_labels = self.val_data
        
        with torch.no_grad():
            preds = self.model(val_inputs)
            acc = ((preds > 0.5) == val_labels).float().mean()
            print(f'Val Acc: {acc:.4f}')
            
# 可视化训练loss            
def plot_losses(losses):
    plt.plot(losses)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Train Loss')
    plt.show()
    
# 保存和加载模型
def save_model(model, path):
    torch.save(model.state_dict(), path)
    
def load_model(model, path):
    model.load_state_dict(torch.load(path))
    model.eval() # 设置为评估模式
    
# 配置并训练    
config = {'lr': 0.001, 'batch_size': 256, 'epochs': 10}

data_path = 'dataset/'
X_train, y_train = process_data(data_path+'creditcard-3w.csv')
# dataset\creditcard-3w.csv
X_val, y_val = process_data('creditcard-val.csv')

model = FraudModel(X_train.shape[1], [128, 64], 1)
trainer = FraudTrainer(model, (X_train, y_train), (X_val, y_val), config)
losses = trainer.train()

plot_losses(losses)
save_model(model, 'fraud_model.pth')

# 加载模型测试
model = FraudModel(X_train.shape[1], [128, 64], 1)
load_model(model, 'fraud_model.pth')

trainer.evaluate()