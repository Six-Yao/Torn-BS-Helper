# TORN-BS-Helper
旨在给一个叫`Torn`的~~劣质~~网页游戏的BS数值提供计算工具
## 项目目标
根据用户提供的API key进行爬虫获得数据并计算
（我也不知道为什么这个api系统的公用信息也得绑个key才能查）
将爬虫能够爬取的信息自动填写入对应变量，其余由用户修正/补充
## 使用方法
### 环境配置(开发时使用python 3.13, 真实支持范围未知)
```shell
# 创建并激活虚拟环境
python -m venv .venv
# Windows
.venv\scripts\activate
# Linux/macOS
source venv/bin/activate
# 安装依赖
pip install -r requirements.txt
# 或
pip install requests
```
### 使用项目
1. 运行程序
```shell
python main.py
```
2. 在游戏内->settings->API keys中创建/复制一个至少为Limited Access的key到最上方文本框
3. 点击运行，等待爬取数据并填充
4. 检查并补充所有信息
5. 点击开始计算得到结果
## 施工进度
- [x] api输入/设置框
- [x] 属性输入框
- [x] 爬取、计算及检查
  - [x] 爬到了哪些数据？填在哪里？
  - [x] 数值是否完全？
- [x] 展示
- [x] 美化(数字位数切分与使用指引)
## 大概没有人会看这个项目，贡献啥的就不写了