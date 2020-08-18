README.md

# == TP项目包含以下模块：==

1.Agreement通信协议模块：
    |- serial_module.py 串口模块（用于数据接收）
    |- serial_test.py 串口测试模块（用于前期测试验证）
    |- server.py 网口模块（用于数据发送）
    
2.Algorithm算法模块：
    |- add_noise.py 加噪模块（用于前期测试验证）
    |- al_func_collection.py 算法模块中所涉及的功能模块
    |- algorithm_main.py 算法主程序
    |- algorithm_main_test.py 算法主程序（用于测试）
    |- data_splitting_integration.py 数据分割、整合模块 
    |- Image_extraction.py 图片提取模块（用于前期测试验证）
    |- interpolation.py 插值模块
    |- main_neural_network.py 神经网络主程序测试模块（用于前期测试验证）
    |- Neural_Networks.py 神经网络模块
    |- optical_fiber.py 光纤模块（做光纤波长数据的前期处理）
    
3.Config配置信息模块：
    |- __init__.py 配置信息模块
    |- config.ini 配置信息文件
    
4.DB数据库：
    |- Data_lib文件夹，用来存放经过算法后的数据
    |- Data_pool文件夹，用来存放接收的原始数据
    |- Data_pool_backup文件夹，作为原始数据的备份文件夹
    
5.Database数据库模块：
    |- data_collection.py 数据获取模块（将新增数据加载到缓存，待算法程序调用）
    |- data_storage.py 数据存储模块
    |- http_test.py 网口测试模块
    |- scanning_interface.py 扫描接口模块（供通信模块调用，通信模块给出执行命令，开始扫描数据库）

6.Function功能模块：
    |- func_collect.py 功能合集模块（各种功能的集合）

7.Picture图像模块：
    |- picture.py 图像显示模块

8.test测试模块：
    |- 各种测试py文件

# == TP项目包含以下文件：== 

|- main.py 主程序文件
|- README.md 说明文件


# == Version_Control ==
20200709
更新：
1.data_splitting_integration.py 中wheel_data_splitting()函数改为optical_data_splitting()函数，并将内容扩充；新增optical_data_to_wheel()函数，将（12个）传感器分割后的数据拼接成各个轮子的数据；
2.optical_fiber.py 中的time_temp_wave()函数添加了频率选择功能，目前可选频率为10Hz、100Hz和2KHz，系统根据时间自动判定，不可手动更改；
3.data_storage.py 中data_to_txt()函数优化；新增函数：(1)read_json()函数：固定读取.json文件；(2)write_json()函数：将字典类型的数据写成.json的文件；(3)car_json()函数：整车json文件；(4)carriage_json()函数：各车厢json文件；(5)wheel_json()函数：各车轮json文件；(6)car_json_integration()函数：将以上三个json文件函数整合成一个json文件；
4.scanning_interface.py 中的压力应变片相关内容注释掉，后期要分开来写；
5.main.py 中新增对json文件的读取、转换及保存；
6.部分代码更新优化：data_collection.py；picture.py。
新增：
1.TP_json.json模块： 车辆数据存储的格式。


20200711
大版本更新：v2.4.0
1.algorithm_main.py 修改文件读取格式。兼容两种txt格式：日期-时间-数据 和 日期-时间-1，8，1-数据；
2.data_splitting_integration.py 设定左右传感器（各6个）；
3.data_storage.py 整车、车厢、车轮的json格式增加参数（参数补全），对car_json_integration()主体函数进行了优化；
4.scanning_interface.py 对“.txt/.AEI”文件缺失的情况进行json文件的补全（程序继续运算，修改了之前遇到缺失文件直接结束程序的情况）；
5..小修改：data_collection.py / main.py
6.测试调试：optical_fiber.py

20200713
小版本更新：v2.4.4
1.Debug:data_splitting_integration.py / optical_fiber.py / data_storage.py / main.py
2.scanning_interface.py 对有数据无车号的情况，增加了json文件的数据采集；
3.func_collection.py 多个函数的注释标注；
4.data_collection.py 新增format_conversion()格式转换函数，修改了删除空文件夹。

20200716
大版本更新：v2.5.0
1.小修改：algorithm_main.py（新增时间格式整合）; data_storage.py（修改ewd小数点保留位数：6位）;
2.data_splitting_integration.py 增加两车轮峰值间的时间间隔选择（100Hz和2KHz的时间间隔不同）;
3.重要更新：Config.__init__.py ConfigInfo()函数中路径的更新（该路径影响配置文件的读取）；在配置文件中添加了三个新的配置：1)original_db_name;2)original_temp_db_name;3)optical_fiber_frequency;
4.data_collection.py 中format_conversion()函数根据规定的数据格式进行了修改，在主程序中属于数据预处理;
5.scanning_interface.py 中database_creation()增加了配置文件的读取，从配置文件中读取文件夹名称;
6.func_collection.py 中folder_creation()函数添加返回值，返回值为新建文件夹的绝对路径;
7.picture.py 增加配置文件读取;
8.main.py 主程序中在数据处理之前，加入了配置信息读取、主程序路径读取及数据预处理。
*.本版本添加了新的文件夹：Original_temp_DB，用于存放（光纤和压力应变片）传感器采集到的原始数据，并将其转换到所需的格式，然后存放到Original_DB文件夹。

20200721
小版本更新：v2.5.2
1.Config.__init__.py 增加配置函数json_storage_path()，json文件的保存位置可以在config.ini文件中配置
2.加入判断语句，修改数据量少导致的Bug：data_collection.py/data_storage.py/data_splitting_integration.py

20200723
小版本更新：v2.5.4
1.data_splitting_integration.py / scanning_interface.py 调整配置调用结构
2.main.py 调整配置调用结构，增加配置文件缺失提示
3.data_storage.py 软件版本号迭代更新

20200728
小版本更新：v2.5.5
1.data_splitting_integration.py 修改Bug，将不符合数据格式的数据置空
2.data_collection.py 新增原始数据格式处理方式
3.data_storage.py 迭代版本号
4.main.py 新增注释

20200817
小版本更新：v2.5.6
1.data_storage.py 修改了车号文件丢失的情况，pass_time的显示问题；迭代版本号
2.picture.py 中添加了频率采集错误的问题描述（错误注释）

20200818
大版本更新：v2.6.0
1.data_splitting_integration.py 
    |- 根据采样频率设定不同的时间间隔，以此采集每个车轮数据
    1）optical_data_splitting()函数：
        |- ①车轮选取峰值分割线以所有车轮数据均值+0.3作为选取标准；
        |- ②横坐标取值范围重新制定
        |- ③不足32个车轮的数据照常输出，有多少输出多少（重点更新）
    2）optical_data_to_wheel()函数
        |- ①根据采样频率和时间间隔重新构建数组
2.data_storage.py 迭代版本号