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
    |- wheel_analysis.py 车轮数据分析模块
    
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

|- main_TP.py 主程序文件
|- README.md 说明文件


# == Version_Control ==
20200709
更新：
1.data_splitting_integration.py 中wheel_data_splitting()函数改为optical_data_splitting()函数，并将内容扩充；新增optical_data_to_wheel()函数，将（12个）传感器分割后的数据拼接成各个轮子的数据；
2.optical_fiber.py 中的time_temp_wave()函数添加了频率选择功能，目前可选频率为10Hz、100Hz和2KHz，系统根据时间自动判定，不可手动更改；
3.data_storage.py 中data_to_txt()函数优化；新增函数：(1)read_json()函数：固定读取.json文件；(2)write_json()函数：将字典类型的数据写成.json的文件；(3)car_json()函数：整车json文件；(4)carriage_json()函数：各车厢json文件；(5)wheel_json()函数：各车轮json文件；(6)car_json_integration()函数：将以上三个json文件函数整合成一个json文件；
4.scanning_interface.py 中的压力应变片相关内容注释掉，后期要分开来写；
5.main_TP.py 中新增对json文件的读取、转换及保存；
6.部分代码更新优化：data_collection.py；picture.py。
新增：
1.TP_json.json模块： 车辆数据存储的格式。


20200711
大版本更新：v2.4.0
1.algorithm_main.py 修改文件读取格式。兼容两种txt格式：日期-时间-数据 和 日期-时间-1，8，1-数据；
2.data_splitting_integration.py 设定左右传感器（各6个）；
3.data_storage.py 整车、车厢、车轮的json格式增加参数（参数补全），对car_json_integration()主体函数进行了优化；
4.scanning_interface.py 对“.txt/.AEI”文件缺失的情况进行json文件的补全（程序继续运算，修改了之前遇到缺失文件直接结束程序的情况）；
5..小修改：data_collection.py / main_TP.py
6.测试调试：optical_fiber.py

20200713
小版本更新：v2.4.4
1.Debug:data_splitting_integration.py / optical_fiber.py / data_storage.py / main_TP.py
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
8.main_TP.py 主程序中在数据处理之前，加入了配置信息读取、主程序路径读取及数据预处理。
*.本版本添加了新的文件夹：Original_temp_DB，用于存放（光纤和压力应变片）传感器采集到的原始数据，并将其转换到所需的格式，然后存放到Original_DB文件夹。

20200721
小版本更新：v2.5.2
1.Config.__init__.py 增加配置函数json_storage_path()，json文件的保存位置可以在config.ini文件中配置
2.加入判断语句，修改数据量少导致的Bug：data_collection.py/data_storage.py/data_splitting_integration.py

20200723
小版本更新：v2.5.4
1.data_splitting_integration.py / scanning_interface.py 调整配置调用结构
2.main_TP.py 调整配置调用结构，增加配置文件缺失提示
3.data_storage.py 软件版本号迭代更新

20200728
小版本更新：v2.5.5
1.data_splitting_integration.py 修改Bug，将不符合数据格式的数据置空
2.data_collection.py 新增原始数据格式处理方式
3.data_storage.py 迭代版本号
4.main_TP.py 新增注释

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

20200819
小版本更新：v2.6.1
1.data_splitting_integration.py 
    |- 修改了每个轮子选取的数量
    |- 修改了坐标系（将整个坐标系上移，使得当没有列车经过时的图像在x轴上）
    |- 根据经验值修改了分割线的数值
2.data_storage.py 迭代版本号

20200901
大版本更新：v2.7.0
1.algorithm_main.py 新增al_main_2()函数:对车轮数据进行读取；原al_main()函数更名为al_main_1()函数；
2.data_splitting_integration.py 中
    |- 将原data_normalization()函数改为data_standardization()函数，只将车轮数据标准化；新增data_normalization()函数。
    |- optical_data_splitting()函数中，修改了dividing_line参数，根据不同的均值来给定不同的分割线
    |- optical_data_splitting()函数中，新增optical_all_data的size不一致的处理方式，不同的size使用零矩阵代替
3.Neural_Network.py 将神经网络过程分模块写成函数，新增tensor_unsqueeze()、optimization_choose()、visualization()、train_neural_network()、neural_network_module()等模块
4.data_collection.py 将12个传感器的顺序按照现场的顺序进行重新排序（12个txt文档在处理前重新命名）
5.data_storage.py data_to_txt()函数中将数据归一化改成数据标准化；迭代版本号
6.main_TP.py 新增车轮数据分析算法
新增：
1.Algorithm模块下新增wheel_analysis.py 用于对生成的车轮数据进行分析
    |- read_wheel_data()读取车轮数据函数
    |- neural_network_analysis()神经网络分析函数

20200925
大版本更新：v2.8.0
1.al_func_collection.py 新增fft_func()快速傅里叶变换函数；新增butter_lowpass_filter()低通滤波器函数；
2.algorithm_main.py al_main_1()函数名称还原成al_main()；al_main_2()函数名称变更为al_main_weight():对车轮进行称重；
3.data_splitting_integration.py 中将部分注释删除；
    |- optical_data_splitting()函数中添加fft及低通滤波的算法，同时将取点区间由2000缩短为200，并重新制定dividing_line的算法；
4.wheel_analysis.py 新增wheel_weigh()车轮称重函数及wheel_weight_analysis()车轮重量分析函数；
5.data_collection.py 算法主程序的名称恢复为al_main()
6.data_storage.py car_json()函数中添加total_weight列车总重字段；
    |- wheel_json()函数中添加wheel_weight/axle_weight/bogie_weight字段
    |- car_json_integration()中新增上述添加的字段
    |- 迭代版本号
7.main_TP.py 新增计算车辆相关参数的重量的算法 

20201027
大版本更新：2.9.0
1.algorithm_main.py al_main_weight()函数更新，通过车号文件新增偏载检测；
2.data_splitting_integration.py data_standardization()函数：修改wd_base_line的计算规则；
3.optical_fiber.py 添加配置文件；新增data_integration()函数和wave_display()函数；
4.wheel_analysis.py wheel_weigh()函数中新增通过车号文件分析车轮的重量以及车辆超偏载；wheel_weight_analysis()函数中新增车号文件参数，并修改整辆列车的称重算法；
    |- 新增unbalanced_loads()偏载函数；
5.Config.__init__ 中新增weight_data重量数据参数和time_gap_value时间间隔数值参数；config.ini配置文件中新增GAP和WEIGHT初始化参数；
6.data_storage.py carriage_json()函数中添加defectType1超偏载缺陷字段；
    |- car_json_integration()中对wheel_single_json添加判断；
    |- 迭代版本号
7.scanning_interface.py 删除部分注释程序
8.main.py 将超偏载结果添加进主程序；
新增：
1.Picture.original_data_to_pic.py文件：将12个传感器txt文件中的数据，校零标准化并显示出图片；
2.TP_test.show_pic.py文件：将txt中的数据校零并显示图片；
3.主项目目录下新增gongda_test.py文件：用于工大测试并做称重验证；

20201104
小版本更新：2.9.1
1.导入模块调整，注释修改删除：al_func_collection.py、algorithm_main.py、data_splitting_integration.py、Image_extraction.py、interpolation.py、data_storage.py、gongda_test.py；
2.wheel_analysis.py 新增整车冲击当量的计算；
3.data_storage.py wheel_json()函数中新增冲击当量字段
    |- car_json_integration()函数中对wheel_json()、carriage_json()进行了debug并修正了bug；
    |- 迭代版本号
4.gongda_test.py 新增test_pic_display()函数；

20201201
小版本更新：2.9.5
1.data_splitting_integration.py optical_data_splitting() 增加异常处理；
2.wheel_analysis.py 
    |- wheel_weigh()函数，通过mean_car_set来修改算法，使同轴两个车轮的差值减小；
    |- wheel_weight_analysis()函数中，更新整车重量的关键系数；同时调整了末班车（根据时间判断）的重量信息；
    |- unbalanced_loads()函数中，修改偏载规则；
3.data_collection.py 
    |- optical_fiber_collection()函数中，新增对传感器的数据进行修正（基本信号标准统一化），但是未使用（效果不佳）；
    |- format_conversion()函数中，将路径改成固定路径；
4.data_storage.py 
    |- write_json()函数中，新增json文件的备份文件夹（供数据迁移使用）
    |- car_json()迭代版本号；
    |- carriage_json()新增车厢重量；
5.scanning_interface.py database_creation()函数修改地址为固定地址；
6.original_data_to_pic.py data_read()函数修改Bug；
7.gongda_test.py 新增data_calibration()、tw_txt_integration_display()、wave_display_limit()函数；
新增：
1.gongda_static_test.py 用于工大测试重量的程序；

20201202
小版本更新：2.9.6
1.wheel_analysis.py 新增偏载系数配置；
    |- 新增超重检测函数overload()；
    |- 修改了偏载检测程序，使用各个车厢的重量进行判断；
2.Config.__init__.py 新增偏载系数配置程序；
3.data_storage.py 迭代版本号；

20201204
小版本更新：2.9.7
1.data_splitting_integration.py 修改bug，dividing_line的数值进行规定
2.data_storage.py 
    |- write_json()函数中，添加对json文件进行打包压缩的代码；
    |- car_json_integration()函数中，添加将信息进行base64编码的程序（未使用上，增加了文件的大小）；
    |- 迭代版本号；
3.func_collection.py 新增pack_json()——json文件打包压缩函数；

20201214
小版本更新：2.9.8
1.al_func_collection.py 新增不圆度检测函数non_circularity()；
2.algorithm_main.py 新增故障检测函数fault_detection()；
3.data_splitting_integration.py 删减部分无用注释；
4.wheel_analysis.py 添加部分注释；
5.show_pic.py 图像显示范围变化；
6.data_storage.py 迭代版本号；
7.main_TP.py 新增车辆故障检测功能；

20201217
小版本更新：2.9.13
1.algorithm_main.py al_main_weight()函数中新增every_wheel_speed参数；
2.wheel_analysis.py 
    |- wheel_weight()函数中，车轮重量分析中输出新增every_wheel_speed参数；
    |- wheel_weight_analysis()函数中，新增列车速度信息采集方法；
        |- 修正了冲击当量的算法；
    |- impact_equivalent_algorithm()修正冲击当量函数算法；
3.Config.__init__.py 中新增speed_json_path()、speed_json_delay_time()函数
4.data_storage.py 
    |- 将read_json()函数修改为read_speed_json()函数，用于读取速度信息数据；
    |- 新增progressbar()进度显示函数；
    |- car_json_integration()函数中，新增列车速度读取方法，更新列车平均速度算法，并调整相关json数据的存储；
    |- 迭代版本号；
5.main_TP.py 新增了列车速度信息数据；

20201218
小版本更新：2.9.14
1.所有文件的整理、注释的精简删除、版本的迭代；
2.冲击当量<0的置零；

20201222
小版本更新：2.9.15
1.algorithm_main.py al_main_weight()函数中新增输出参数test_date_time；
2.data_collection.py 新增read_json_file()函数，对json进行读取；
3.data_storage.py 
    |- read_speed_json()函数中新增对速度json文件中检测时间的读取；
    |- car_json_integration()函数中更新检测时间为速度json文件中的速度；
    |- 待办：根据冲击当量设置踏面损伤报警；
    |- 迭代版本号；
4.wheel_analysis.py wheel_weight_analysis()函数中对采集列车速度信息的代码做了更新；
5.main_TP.py 将速度json文件中的检测时间更新上去；
小版本更新：2.9.15
1.TP_test文件夹中，新增read_json.py模块，主要功能是对TP主程序算法生成的json文件进行车轮数据分析展示；
2.修改部分bug；

20201224
小版本更新：2.9.16
1.func_collection.py 新增remove_json()函数，目的为了在算法程序开始之前移除上一个遗留的速度json文件；
2.read_json.py 对分析并展示json文件中某一轴做了调试与修改；
3.main_TP.py 新增在算法程序之前移除速度json文件；
4.data_storage.py 迭代版本号；

20210120：
小版本更新：2.9.17
1.wheel_analysis.py 中impact_equivalent_algorithm()函数进行debug，修正了异常；
2.al_func_collection.py 中non_circularity()函数进行补充；
3.data_storage.py 迭代版本号；

20210126:
大版本更新：2.10.0
1.data_storage.py 
    |- data_to_txt()注释掉将数据写成txt文档；
    |- 迭代版本号
2.scanning_interface.py database_creation()注释掉数据备份；
3.main_TP.py 注释掉车辆故障检测待后续补充完整再释放；
