README.md

TP项目包含以下模块：

1.Agreement通信协议模块：
    |- serial_module.py 串口模块（用于数据接收）
    |- serial_test.py 串口测试模块（用于前期测试验证）
    |- server.py 网口模块（用于数据发送）
    
2.Algorithm算法模块：
    |- add_noise.py 加噪模块（用于前期测试验证）
    |- algorithm_main.py 算法主程序
    |- algorithm_main_test.py 算法主程序（用于测试）
    |- Image_extraction.py 图片提取模块（用于前期测试验证）
    |- interpolation.py 插值模块
    |- main_neural_network.py 神经网络主程序测试模块（用于前期测试验证）
    |- Neural_Networks.py 神经网络模块
    
3.Config配置信息模块：
    |- __init__.py 配置信息模块
    |- config.ini 配置信息文件
    
4.Database数据库模块：
    |- Data_lib文件夹，用来存放经过算法后的数据
    |- Data_pool文件夹，用来存放接收的原始数据
    |- Data_pool_backup文件夹，作为原始数据的备份文件夹
    |
    |- data_collection.py 数据获取模块（将新增数据加载到缓存，待算法程序调用）
    |- data_storage.py 数据存储模块
    |- scanning_interface.py 扫描接口模块（供通信模块调用，通信模块给出执行命令，开始扫描数据库）
    


TP项目包含以下文件：

|- al_main.py 主程序文件
|- func_collect.py 功能合集模块（各种功能的集合）
|- README.md 说明文件