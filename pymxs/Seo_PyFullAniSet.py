import MaxPlus
import pymxs
from PySide2 import QtWidgets, QtCore, QtGui
import re
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
    m_logEnable = True
    m_full_string_key_num = 3 #전체문자가 자정되어있는 칼럼(열)위치번호
    m_property_name = "Py_SetAniProperty"
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(FullAniSetView, self).__init__(parent)
        RT.clearlistener()
        self.CreateUI()
    def LogPrint(self,log_string,eanblePrint = m_logEnable):
        ''' 확인용으로 사용하는 print문을 한번에 on off 할수 있는 기능
        '''
        if eanblePrint :
            print (log_string)
    def MaxscriptCallbackFn(self):
        ''' 화면에 표시 될 콜백'''
        maxscript_str = '''
        fn fn_makeFrameViewer =
        (
            gw.setTransform (getCPTM())
            size_point2 = 	getViewSize() 
            pos_point3 = [ 0, size_point2.x * 0.5, 0]
            frame_name_text_string
            gw.hText pos_point3 frame_name_text_string color:yellow
            gw.enlargeUpdateRect #whole  
            gw.updateScreen() 
        )
        '''
        RT.execute(maxscript_str)
    def CreateUI(self):
        self.LogPrint(u"CreateUI")
        self.setWindowTitle(u"프레임 툴")
        self.resize(QtCore.QSize(420,300))
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
        self.save_button = QtWidgets.QPushButton(u"저장", default = False, autoDefault = False)
        self.input_buttonSet_layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.SaveAniSet)
        # 버튼 : 수정 -아직 미적용
        self.edit_button = QtWidgets.QPushButton(u"수정", default = False, autoDefault = False)
        #self.input_buttonSet_layout.addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.ChangeData)
        # 버튼 : 하위 저장
        self.sub_save_button = QtWidgets.QPushButton(u"하위 저장", default = False, autoDefault = False)
        self.input_buttonSet_layout.addWidget(self.sub_save_button)
        self.sub_save_button.clicked.connect(self.SubSaveAniSet)
        # 프레임 뷰어
        self.frame_tree_label = QtWidgets.QLabel(u"프레임 리스트")
        self.input_main_layout.addWidget(self.frame_tree_label)
        # 트리뷰어
        self.ani_frame_tree_widget = QtWidgets.QTreeWidget()
        self.ani_frame_tree_widget.setExpandsOnDoubleClick(False)
        self.ani_frame_tree_widget.setHeaderLabels([u"이름", u"시작", u"끝", u"저장용문자"])
        self.input_main_layout.addWidget(self.ani_frame_tree_widget)
        self.ani_frame_tree_widget.doubleClicked.connect(self.SetFrameRange)
        ##헤드 설정
        head_item = self.ani_frame_tree_widget.headerItem()
        head_item.setSizeHint(0, QtCore.QSize(500, 25))
        head_view = self.ani_frame_tree_widget.header()
        head_view.setSectionHidden(3,True)
        head_view.resizeSection(0, 280)
        head_view.resizeSection(1, 45)
        ##메뉴차가
        self.ani_frame_tree_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy(QtCore.Qt.CustomContextMenu))
        self.ani_frame_tree_widget.customContextMenuRequested.connect(self.ItemListMenu)
        #
        self.GetPropertyAnisetValue()
        self.setLayout(self.main_layout)
        self.show()
    def ItemListMenu(self, pos):
        menu = QtWidgets.QMenu(self)
        menu.addAction(u'목록 삭제', self.ItemDeleteMenu)
        menu.exec_(QtGui.QCursor.pos())
    def ItemDelete_bak(self):
        ''' 리스트의 아이템 삭제 '''
        self.LogPrint(u"아이템 삭제")
        QItemSelectionModel = self.ani_frame_tree_widget.selectionModel()
        index_QModelIndex = QItemSelectionModel.currentIndex()
        print(index_QModelIndex.row())
        self.ani_frame_tree_widget.takeTopLevelItem(index_QModelIndex.row())
    def ItemDeleteMenu(self):
        self.ItemDelete()
        self.SetPropertyAnisetValue()
    def ItemDelete(self):
        ''' 리스트의 아이템 삭제 '''
        self.LogPrint(u"아이템 삭제")
        root_QTreeWidgetItem = self.ani_frame_tree_widget.invisibleRootItem()
        for item in self.ani_frame_tree_widget.selectedItems():
            root_QTreeWidgetItem.removeChild(item)
    def GetSelectionQModeIndex(self):
        ''' -> index_QModelIndex '''
        self.LogPrint(u'GetSelectionQModeIndex')
        a_QItemSelectionModel = self.ani_frame_tree_widget.selectionModel()
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        return index_QModelIndex
    def GetSelectionData(self, target_column_int):
        ''' -> string target_modelIndex.data() '''
        self.LogPrint(u'GetSelectionData')
        index_QModelIndex = self.GetSelectionQModeIndex()
        target_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(), target_column_int)
        return target_modelIndex.data()
    def MakeTreeWidgetData(self):
        self.ani_frame_tree_widget.clear() 
        for ani_set in self.ani_list:
            item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
            item.setText(0,ani_set.name)
            item.setText(1,ani_set.start_frame)
            item.setText(2,ani_set.end_frame)
    def GetPropertyAnisetValue_max(self):
        self.LogPrint(u"in_GetPropertyAnisetValue_max")
        RT.execute('PropertyNum = fileProperties.findProperty #custom "SetAniProperty"')
        if RT.PropertyNum == 0 :
            self.LogPrint(u"정보없음")
        else:
            RT.execute('m_AniSetsString = (fileProperties.getPropertyValue #custom PropertyNum as string)')
            RT.execute('m_AniSetStringArray = filterstring m_AniSetsString ","')
            ani_set_string_array = list(RT.m_AniSetStringArray)
            for obj_str in ani_set_string_array:
                ani_split_list = obj_str.split('~')
                if len(ani_split_list) > 3 :
                    self.LogPrint(u'파이썬버전 설정입니다.')
                item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
                self.AddData(item, ani_split_list[0], ani_split_list[1], ani_split_list[2])
    def GetPropertyAnisetValue(self):
        self.LogPrint(u"in_GetPropertyAnisetValue")
        property_num_int = RT.fileProperties.findProperty(RT.name('custom'), self.m_property_name )
        if property_num_int == 0 :
            self.LogPrint(u"정보없음")
        else:
            #RT.execute('m_AniSetsString = (fileProperties.getPropertyValue #custom '+ str(property_num_int) + ')')
            #ani_str = (RT.m_AniSetsString).encode('UTF-8')
            ani_str = RT.fileProperties.getPropertyValue(RT.name('custom'), property_num_int )
            ani_set_string_array = ani_str.split(')')
            for fll_main_str in ani_set_string_array:
                main_str = fll_main_str[1:]
                if not main_str:
                    continue
                ani_item_list = main_str.split(',')
                item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
                isSub_int = 0
                for obj_str in ani_item_list:
                    if obj_str :
                        ani_split_list = obj_str.split('~')
                        if isSub_int > 0:
                            self.AddData(QtWidgets.QTreeWidgetItem(item), ani_split_list[0], ani_split_list[1], ani_split_list[2])
                        else:
                            self.AddData(item, ani_split_list[0], ani_split_list[1], ani_split_list[2])
                    isSub_int = isSub_int + 1
    def SetPropertyAnisetValue(self):
        ''' 자료저장'''
        save_data = ''
        root_QTreeWidgetItem = self.ani_frame_tree_widget.invisibleRootItem()
        for count_int in range(0, root_QTreeWidgetItem.childCount()):
            QTreeWidgetItem = root_QTreeWidgetItem.child(count_int)
            save_data = save_data + '(' + QTreeWidgetItem.text(3)
            self.LogPrint(QTreeWidgetItem.text(3)) #저장할 데이터
            #하위 자식 확인
            for sub_count_int in range(0, QTreeWidgetItem.childCount()):
                sub_QTreeWidgetItem = QTreeWidgetItem.child(sub_count_int)
                save_data = save_data + ',' + sub_QTreeWidgetItem.text(3)
                self.LogPrint(sub_QTreeWidgetItem.text(3))
            save_data = save_data + ')'
        RT.fileProperties.addProperty( RT.name('custom'), self.m_property_name, save_data)
    def AddData(self, item, frame_name, start_frame_int, end_frame_int):
        self.LogPrint(u'AddData')
        if start_frame_int > end_frame_int:
            return self.LogPrint(u'시작 프레임이 작습니다.')
        full_string = (u'{0}~{1}~{2}'.format(frame_name, start_frame_int, end_frame_int))
        item.setText(0,frame_name)
        item.setText(1,str(start_frame_int))
        item.setText(2,str(end_frame_int))
        item.setText(self.m_full_string_key_num, full_string)
    def ChangeData(self):
        self.LogPrint(u'ChangeData')
    def LoadAniSetList(self):
        self.LogPrint( u'LoadAniSetList')
    def SaveAniSet(self):
        self.LogPrint(u'SaveAniSEt')
        item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
        self.AddData(item, self.frameName_lineEdit.text(), self.start_frame.value(), self.end_frame.value() )
        self.SetPropertyAnisetValue()
    def SubSaveAniSet(self):
        self.LogPrint(u'하위 저장')
        QTreeWidgetItem = self.ani_frame_tree_widget.currentItem()
        if QTreeWidgetItem is None:
            return
        parent_QTreeWidgetItem = QTreeWidgetItem.parent()
        if not (parent_QTreeWidgetItem is None):
            QTreeWidgetItem = parent_QTreeWidgetItem
        sub_item = QtWidgets.QTreeWidgetItem(QTreeWidgetItem)
        self.AddData(sub_item, self.frameName_lineEdit.text(), self.start_frame.value(), self.end_frame.value() )
        self.SetPropertyAnisetValue()
    def SetFrameRange(self):
        ''' '''
        self.LogPrint(u'SetFrameRange')
        start_frame = int(self.GetSelectionData(1))
        end_frame = int(self.GetSelectionData(2))
        if start_frame >= end_frame :
            end_frame = end_frame + 1
        RT.animationRange = RT.interval(start_frame,end_frame)

ani_set = FullAniSetView()

