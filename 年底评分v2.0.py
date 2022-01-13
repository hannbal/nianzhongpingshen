# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 08:24:56 2022

@author: tony
"""

#年底评分任意修改版
import pandas as pd


import  os.path, sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QGridLayout,QHBoxLayout,QVBoxLayout,QMessageBox,QCheckBox
from PyQt5.QtWidgets import QLabel,QGroupBox,QListWidget,QPushButton,QListWidgetItem,QRadioButton,QDoubleSpinBox#,QButtonGroup
from PyQt5.QtGui import QColor
import time,socket


class myqt(QMainWindow):
    
    filename = str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+socket.gethostname()+'-'+'.csv'
    pfbz = {}
    name_list=[]
    
#pandas数据
    pd_data={}
#配置文件数据   
    conf_dict={}
#评审角色列表
    ps_dict={}
#评审角色checkbox控件列表
    top_group=[]
#评价内容
    pfnr_list=[]
#评分选项
    pfx_list=[]
#评分选项radio控件列表
    op_list=[]
#当前评审角色
    ps_juese=''
    ps_max=0
    ps_min=0
    last_select=0
    sysm=''

    

    
    def __init__(self, *args, **kwargs):
        self.currectPath =os.getcwd()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()             
        super(myqt,self).__init__(*args, **kwargs)
        self.w_height = self.screenRect.height()
        self.w_width = self.screenRect.width()



#读取配置文件        
        self.read_conf()

        for key,value in self.conf_dict.items():
            if key =='psjs':
                for x in value.split(','):
                    if int(x.split('-')[1])==0 and int(x.split('-')[2])==0:
                        self.ps_dict[x.split('-')[0]]=[int(x.split('-')[1]),int(x.split('-')[2]),True]
                    else:
                        self.ps_dict[x.split('-')[0]]=[int(x.split('-')[1]),int(x.split('-')[2]),False]                                                     
            elif key =='pfnr':
                for x in value.split(','):
                    self.pfnr_list.append(x)
            elif key =='pfx':
                for x in value.split(','):
                    self.pfx_list.append(x)
            elif key =='sysm':
                self.sysm = value
                    

#主体窗口        
        self.setMinimumSize(1024, 800)
        self.setWindowTitle("综合评分 1.0")
    #嵌套第一层窗口           
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)        
        # self.centralwidget.setStyleSheet("QWidget{background-color: black;font: 16px;color: white;}")  
        self.centralwidget.setStyleSheet("QWidget{background-color: #f3f3f4;font: 25px;color: black;}")    
        
        pfx_len = len(self.pfx_list)
        pfnr_len = len(self.pfnr_list)
        for x in self.pfx_list:
            if self.pfx_list.index(x) ==0:
                self.pfbz[x] = round(100/pfnr_len,1)
            elif self.pfx_list.index(x) !=pfx_len-1:
                self.pfbz[x]= round((90-60)/pfnr_len,1)/(pfx_len-2)*(pfx_len-2-self.pfx_list.index(x)+1)+60/pfnr_len
            else:
                self.pfbz[x]=59.0/pfnr_len
      
    #调用窗口初始化   
        self.setupUi()
    
    
    def setupUi(self):
        self.layout= QGridLayout()
        #边界
        self.layout.setContentsMargins(20,20,20,20)
        #网格间距
        self.layout.setSpacing(10)
        
# #窗口top
        self.layout_top= QHBoxLayout()
    #使用说明
        self.label_name = QLabel("使用说明",self)
        self.label_name.setStyleSheet("QLabel{font:25px}")
        self.layout_top.addWidget(self.label_name)
        self.label_text = QLabel(self.sysm,self)
        
        self.label_text.setWordWrap(True)
        self.label_text.setStyleSheet("QLabel{padding:8px;font:30px}")
        self.layout_top.addWidget(self.label_text)
        
        self.layout_top_right = QGridLayout()
        self.box_top_right = QGroupBox()
        self.box_top_right.setLayout(self.layout_top_right)
        self.layout_top.addWidget(self.box_top_right)
        
        
    #评审角色
        for key,value in self.ps_dict.items():
            # print(key,value)
            temp = QCheckBox(key)
            temp.setObjectName(key)
            self.layout_top_right.addWidget(temp,value[0],value[1])
            self.top_group.append(temp)
    


    
#layout_top 列宽比例设置    
        self.layout_top.setStretch(0,1)
        self.layout_top.setStretch(1,10)
        self.layout_top.setStretch(2,10)        
    #添加到主窗口
        self.tab_top = QGroupBox()
        self.tab_top.setLayout(self.layout_top)
        self.layout.addWidget(self.tab_top)        
        
# #窗口middle       
    #左边文件列表
        self.layout_middle = QHBoxLayout()
        self.file_list_box = QGroupBox()
        self.file_list_box.setTitle('参评人')
        
        self.file_list_view = QListWidget(self.file_list_box)
        self.layout_list =QVBoxLayout()
        self.file_list_view.setStyleSheet("QListWidget{font:55px;}")
        #按钮        
       
        self.pb_savefile = QPushButton("保存")
        self.pb_savefile.setStyleSheet("QPushButton{background-color: #c2e9d4;font: 70px;color: blue;border-color:white;border-width:10px;}")

        self.layout_list.addWidget(self.file_list_view)
        self.layout_list.addWidget(self.pb_savefile)
        self.file_list_box.setLayout(self.layout_list)
    
    
    #右边操作按记录   
        self.op_list_box = QGroupBox()
        
        self.op_list_box.setTitle('评审内容')
        self.layout_table = QGridLayout()
        
        for value_pfnr in self.pfnr_list:

            temp_label = QLabel(value_pfnr,self)
            temp_gb =QGroupBox()
            self.layout_table.addWidget(temp_gb)
            temp_layout = QHBoxLayout()
            temp_gb.setLayout(temp_layout)
            temp_layout.addWidget(temp_label)
            temp_gbpfx = QGroupBox()
            temp_layoutpfx = QHBoxLayout()
            temp_gbpfx.setLayout(temp_layoutpfx)
            
            for value in self.pfx_list:
                # print(value_pfnr+value)
                temp_layout.addWidget(temp_gbpfx)
                
                radio_pfx = QRadioButton(value)
                radio_pfx.setObjectName(value_pfnr+'-'+value)       
                temp_layoutpfx.addWidget(radio_pfx)
                self.op_list.append(radio_pfx)
            temp_layout.setStretch(0,1)
            temp_layout.setStretch(1,5)   
            
        
        self.label_zf = QLabel("总分范围:{0}-{1}".format(self.ps_min,self.ps_max))
        self.gb_zf = QGroupBox()
        self.layout_table.addWidget(self.gb_zf)
        
        self.spb_sum = myQSpinBox(self)
        self.spb_sum.setStyleSheet("QSpinBox{height:100%;font-size:100px}")
        self.spb_sum.setMaximum(0)
        self.spb_sum.setMinimum(0)
        
        self.layout_zf =QHBoxLayout()
        self.gb_zf.setLayout(self.layout_zf)
        self.layout_zf.addWidget(self.label_zf)
        self.layout_zf.addWidget(self.spb_sum)



        
#右侧评审界面加入总界面        
        self.op_list_box.setLayout(self.layout_table)
   
    
   #下方左右两个加入下方总layout
        self.layout_middle.addWidget(self.file_list_box)
        self.layout_middle.addWidget(self.op_list_box)
        
    #middle两个部分 列宽比例设置     
        self.layout_middle.setStretch(0,1)
        self.layout_middle.setStretch(1,5)
    #添加到主窗口
        self.tab_middle = QGroupBox()
        self.tab_middle.setLayout(self.layout_middle)
        self.layout.addWidget(self.tab_middle)      


        self.centralwidget.setLayout(self.layout)        
#top middle bottom 行宽比例设置
        self.layout.setRowStretch(0,2)
        self.layout.setRowStretch(1,10)        

#按钮关联        
        self.pb_savefile.clicked.connect(self.save_file)
        self.file_list_view.clicked.connect(self.listview_changeevent)       
    #评审checkbox
        for checkbox in self.top_group:
            checkbox.stateChanged.connect(self.check_box)
    #评审radio
        for radio in self.op_list:
            radio.clicked.connect(self.radio_change)
        #全屏启动             
        self.isFullScreen()
        self.showMaximized()  

    def pd_readcsv(self,path):
        try:
            df = pd.read_csv(path,encoding="gbk")
            if df.size==0:                
                print('文件格式不正确')
                return 0
        except Exception:
            print('文件格式不正确')
            return 0
        self.pd_data = df
        # print(df)
        self.name_list = self.pd_data["姓名工号"]
        for name in self.name_list:
            item = QListWidgetItem()
            item.setText(name)
            self.file_list_view.addItem(item)
                
        self.file_list_view.setCurrentRow(0)
        self.pd_setup()
        self.label_zf.setText("总分范围:{0}-{1}".format(self.ps_min,self.ps_max))

    def pd_setup(self):
        #根据文件读取的值初始化checkbox
        if isinstance(self.pd_data.loc[self.file_list_view.currentRow(),'评审角色'],str):
            self.ps_juese = self.pd_data.loc[self.file_list_view.currentRow(),'评审角色']
        else:
            self.ps_juese =self.ps_dict[list(self.ps_dict.keys())[0]]
        
        check_row=None
        for ck_object in self.top_group:
            if  ck_object.objectName() in self.ps_juese:
                self.ps_dict[ck_object.objectName()][2]=True
                check_row = self.ps_dict[ck_object.objectName()][0]
            else:
                self.ps_dict[ck_object.objectName()][2]=False
        
        if check_row !=None:
            for key,value in self.ps_dict.items():
                if value[0] != check_row:
                    value[2]=False
                
            for ck_object in self.top_group:
                ck_object.setChecked(self.ps_dict[ck_object.objectName()][2])
            
        
        
        #根据文件读取的值初始化radio
        radio_value=False
        for radio in self.op_list:
            if self.pd_data.loc[self.file_list_view.currentRow(),radio.objectName().split('-')[0]] == radio.objectName().split('-')[1]:
                radio.setChecked(True)
                radio_value |=True
                
            else:
                radio.setChecked(False)
                radio_value |=False
            
        if radio_value ==False:
            for x in range(len(self.op_list)):
                if x%len(self.pfx_list) == 2:
                    self.op_list[x].setChecked(True)
        
        
        
        self.caculate()

    def check_box(self,event):   
        sender =self.sender()
        checked_status = sender.isChecked()
        #角色
        check_row=None
        for ck_object in self.top_group:
            if sender is ck_object:
                if checked_status:
                    self.ps_dict[ck_object.objectName()][2]=True
                    check_row = self.ps_dict[ck_object.objectName()][0]
                else:
                    self.ps_dict[ck_object.objectName()][2]=False
        
        if check_row !=None:
            for key,value in self.ps_dict.items():
                if value[0] != check_row:
                    value[2]=False
                
            for ck_object in self.top_group:
                ck_object.setChecked(self.ps_dict[ck_object.objectName()][2])

            
        
        self.ps_juese=''
        for key,value in self.ps_dict.items():
            if value[2]:
                self.ps_juese+=key
                self.ps_juese+='、'
        # print(self.ps_juese)
        self.pd_data['评审角色']=self.ps_juese
    
    def radio_change(self,event):
        sender = self.sender()
        self.pd_data.loc[self.pd_data['姓名工号']==self.name_list[self.file_list_view.currentRow()],sender.objectName().split('-')[0]] = sender.objectName().split('-')[1]
        self.caculate()
        
        
    def caculate(self):  
        self.ps_max=0.0
        self.ps_min=0.0
        ps_sum =0.0
        for radio in self.op_list:
            if radio.isChecked():
                ps_sum+=self.pfbz[radio.objectName().split('-')[1]]
                self.ps_max += round(self.pfbz[radio.objectName().split('-')[1]],1)
                
                if self.pfx_list.index(radio.objectName().split('-')[1]) ==0:
                    self.ps_min += round(90.0/len(self.pfnr_list),1)
                elif self.pfx_list.index(radio.objectName().split('-')[1]) !=len(self.pfx_list)-1:
                    
                    # print(self.pfbz[radio.objectName().split('-')[1]],(self.pfbz[radio.objectName().split('-')[1]]*len(self.pfnr_list)-60)/30,1/(len(self.pfx_list)-2))
                    self.ps_min += round((((self.pfbz[radio.objectName().split('-')[1]]*len(self.pfnr_list)-60)/30-1/(len(self.pfx_list)-2))*30+60)/len(self.pfnr_list),1)
                else:
                    self.ps_min += round(49.0/len(self.pfnr_list),1)
            

        self.spb_sum.setMaximum(round(self.ps_max,1))
        self.spb_sum.setMinimum(round(self.ps_min,1))
        if self.ps_min<self.pd_data.loc[self.file_list_view.currentRow(),'总分']<self.ps_max:
            self.spb_sum.setValue(self.pd_data.loc[self.file_list_view.currentRow(),'总分'])
        else:
            self.spb_sum.setValue(ps_sum)
            self.pd_data.loc[self.file_list_view.currentRow(),'总分']=round(self.ps_max,1)
        self.label_zf.setText("总分范围:{0}-{1}".format(round(self.ps_min,1),round(self.ps_max,1)))
        
    
    def listview_changeevent(self):
        
        print("切换至'{0}'".format(self.file_list_view.currentItem().text()))
        self.checkrow()
        self.last_select = self.file_list_view.currentRow()
        # self.check_box()
        self.save_file()
        self.pd_setup()    
    
    def checkrow(self):
        flag=True
        
        for x in self.pfnr_list:
            flag = flag & isinstance(self.pd_data.loc[self.last_select,x],str)
        if flag:
            self.file_list_view.item(self.last_select).setBackground(QColor('#f3f3f4'))
        else:
            self.file_list_view.item(self.last_select).setBackground(QColor('#facbff'))
            flag =True
        
    
    def save_file(self):
        sender =self.sender()
        filepath = 'test.csv'
        try:
            self.pd_data.to_csv(filepath,index=0,encoding='gbk')
            self.pd_data.to_csv(self.filename,index=0,encoding='gbk')
            if isinstance(sender,QPushButton):
                QMessageBox(QMessageBox.Warning,'提示','文件保存成功').exec_()
            print('保存成功')
            
        except Exception:
            if isinstance(sender,QPushButton):
                QMessageBox(QMessageBox.Warning,'jing','文件保存失败').exec_()
            print('file-saving failed')

    def read_conf(self):
        try:
            with open('config.inf','r',encoding='gbk') as conf: 
                lines= conf.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    self.conf_dict[str(line.split('=')[0])]=( line.split('=')[1])
        except Exception as e:
            print(e)
            

class myQSpinBox(QDoubleSpinBox):
    def __init__(self,myqt,*args, **kwargs):
        super(myQSpinBox,self).__init__(*args, **kwargs)
        self.myqt = myqt
        self.setSingleStep(0.1)
        self.setDecimals(1)
        
    def focusOutEvent(self,QfocusEvent):
        self.myqt.pd_data.loc[self.myqt.file_list_view.currentRow(),'总分'] = float(self.text())            
            
if __name__=='__main__':
    app = QApplication(sys.argv)
    ui = myqt()
    if os.path.exists(ui.filename):
        ui.pd_readcsv(ui.filename)
    else:
        ui.pd_readcsv('test.csv')
    sys.exit(app.exec_())
