import MaxPlus
import pymxs
from PySide2 import QtWidgets, QtCore, QtGui
RT = pymxs.runtime
#
class AniSet():
    def __init__(self, name, startFrame, endFrame):
        self.name = name
        self.start_frame = startFrame
        self.end_frame = endFrame
class FullAniSetView(QtWidgets.QDialog):
    frame_range_min_int = -999999
    frame_range_max_int = 999999
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(FullAniSetView, self).__init__(parent)
        RT.clearlistener()
        self.CreateUI()
    
    def CreateUI(self):
        self.setWindowTitle(u"프레임 툴")
        # 레이아웃 구성 
        self.main_layout = QtWidgets.QVBoxLayout()
        self.input_main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.input_main_layout)
        self.input_title_layout = QtWidgets.QHBoxLayout()
        self.input_frameSet_layout = QtWidgets.QHBoxLayout()
        self.input_buttonSet_layout = QtWidgets.QHBoxLayout()
        self.input_main_layout.addLayout(self.input_title_layout)
        self.input_main_layout.addLayout(self.input_frameSet_layout)
        self.input_main_layout.addLayout(self.input_buttonSet_layout)
        # 프레임 입력
        self.frameSet_label = QtWidgets.QLabel(u"프레임 정보")
        self.input_title_layout.addWidget(self.frameSet_label)
        # 입력칸 : 프레임 이름
        self.frameName_lineEdit = QtWidgets.QLineEdit(u"프레임 이름", self)
        self.input_frameSet_layout.addWidget(self.frameName_lineEdit)

        # 입력칸 : 스타트 프레임
        self.start_frame = QtWidgets.QSpinBox()
        self.start_frame.setRange(self.frame_range_min_int, self.frame_range_max_int)
        self.input_frameSet_layout.addWidget(self.start_frame)
        # 입력칸 : 엔드 플레임
        self.end_frame = QtWidgets.QSpinBox()
        self.end_frame.setRange(self.frame_range_min_int, self.frame_range_max_int)
        self.input_frameSet_layout.addWidget(self.end_frame)
        # 버튼 : 저장
        self.save_button = QtWidgets.QPushButton(u"저장", default = True, autoDefault = True)
        self.input_buttonSet_layout.addWidget(self.save_button)
        # 버튼 : 수정
        self.edit_button = QtWidgets.QPushButton(u"수정", default = False, autoDefault = False)
        self.input_buttonSet_layout.addWidget(self.edit_button)
        # 버튼 : 하위 저장
        self.sub_save_button = QtWidgets.QPushButton(u"하위 저장", default = True, autoDefault = True)
        self.input_buttonSet_layout.addWidget(self.sub_save_button)
        # 프레임 뷰어
        self.frame_tree_label = QtWidgets.QLabel(u"프레임 리스트")
        self.input_main_layout.addWidget(self.frame_tree_label)
        # 트리뷰어
        self.ani_frame_tree_widget = QtWidgets.QTreeWidget()
        self.ani_frame_tree_widget.setHeaderLabels([u"이름", u"시작", u"끝", u"저장용문자"])
        self.input_main_layout.addWidget(self.ani_frame_tree_widget)
        #
        self.GetPropertyAnisetValue()
        self.setLayout(self.main_layout)
        self.show()
    def MakeTreeWidgetData(self):
        self.ani_frame_tree_widget.clear() 
        for ani_set in self.ani_list:
            item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
            item.setText(0,ani_set.name)
            item.setText(1,ani_set.start_frame)
            item.setText(2,ani_set.end_frame)
    def GetPropertyAnisetValue(self):
        RT.execute('PropertyNum = fileProperties.findProperty #custom "SetAniProperty"')
        if RT.PropertyNum == 0 :
            print "정보없음."
        else:
            RT.execute('m_AniSetsString = (fileProperties.getPropertyValue #custom PropertyNum as string)')
            RT.execute('m_AniSetStringArray = filterstring m_AniSetsString ","')
            ani_set_string_array = list(RT.m_AniSetStringArray)
            for obj_str in ani_set_string_array:
                item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
                ani_split_list = obj_str.split('~')
                item.setText(0,ani_split_list[0])
                item.setText(1,ani_split_list[1])
                item.setText(2,ani_split_list[2])
                item.setText(3,obj_str)


    def AddData(self):
        pass
    def LoadAniSetList(self):
        pass
    def SaveAniSet(self):
        pass
    def SetEndFrame(sefl):
        pass
    def SetStartFrame(sefl):
        pass

FullAniSetView()

