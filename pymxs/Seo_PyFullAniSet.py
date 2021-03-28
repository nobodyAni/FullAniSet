import MaxPlus
import pymxs
from PySide2 import QtWidgets, QtCore, QtGui
import re
RT = pymxs.runtime
class AniSet():
    m_setList =[]
    def __init__(self, name, startFrame, endFrame):
        self.name = name
        self.start_frame = startFrame
        self.end_frame = endFrame
    def SetData(self, index, item):
        pass
    def GetData(self, index):
        pass
    def ExportFrames(self, item):
        pass
class FullAniSetView(QtWidgets.QDialog):
    frame_range_min_int = -999999
    frame_range_max_int = 999999
    m_logEnable = False
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
#%% 콜백 그룹 -제작중
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
    def EnableCallback(self):
        ''' 맥스 스크립트 콜백을 등록'''
        RT.registerTimeCallback("fn_makeFrameViewer")
    def DiableCallback(self):
        ''' 맥스 스크립트 콜백 해제'''
        RT.unRegisterTimeCallback("fn_makeFrameViewer")
#%% UI
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
        self.option_buttonSet_layout = QtWidgets.QHBoxLayout()
        self.input_main_layout.addLayout(self.input_title_layout)
        self.input_main_layout.addLayout(self.input_frameSet_layout)
        self.input_main_layout.addLayout(self.input_buttonSet_layout)
        self.main_layout.addLayout(self.option_buttonSet_layout)
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
        self.input_buttonSet_layout.addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.editItme)
        # 버튼 : 하위 저장
        self.sub_save_button = QtWidgets.QPushButton(u"하위 저장", default = False, autoDefault = False)
        self.input_buttonSet_layout.addWidget(self.sub_save_button)
        self.sub_save_button.clicked.connect(self.SubSaveAniSet)
        # 프레임 이동
        frame_ctrl_bar = QtWidgets.QGroupBox()   #처음으로, #이전 프레임, #다음 프레임, #끝 프레임
        # 프레임 뷰어
        self.frame_tree_label = QtWidgets.QLabel(u"프레임 리스트")
        self.input_main_layout.addWidget(self.frame_tree_label)
        # 트리뷰어
        self.ani_frame_tree_widget = QtWidgets.QTreeWidget()
        self.ani_frame_tree_widget.setSortingEnabled(True) #정렬기능 활성화
        self.ani_frame_tree_widget.setExpandsOnDoubleClick(False)
        self.ani_frame_tree_widget.setHeaderLabels([u"이름", u"시작", u"끝", u"저장용문자",u'선택'])
        self.input_main_layout.addWidget(self.ani_frame_tree_widget)
        self.ani_frame_tree_widget.doubleClicked.connect(self.ItemDoubleClicked)
        ##헤드 설정
        head_item = self.ani_frame_tree_widget.headerItem()
        head_item.setSizeHint(0, QtCore.QSize(500, 25))
        head_view = self.ani_frame_tree_widget.header()
        head_view.setSectionHidden(3,True)
        head_view.resizeSection(0, 280)
        head_view.resizeSection(1, 45)
        # 분활 
        self.exportMaxFile_button = QtWidgets.QPushButton(u"파일 분활", default = False, autoDefault = False)
        self.option_buttonSet_layout.addWidget(self.exportMaxFile_button)
        self.exportMaxFile_button.clicked.connect(self.exportMaxFile_Run)
        #옵션 ##아직 보류중 
        self.enableRow4_button = QtWidgets.QPushButton(u"4열보기", default = False, autoDefault = False)
        #self.option_buttonSet_layout.addWidget(self.enableRow4_button)
        self.enableRow4_button.clicked.connect(self.SaveAniSet)
        ## 출력 - 미완료
        self.enableViewportText_QCheckBox = QtWidgets.QCheckBox(u"화면표시")
        # self.option_buttonSet_layout.addWidget(self.enableViewportText_QCheckBox)
        self.enableViewportText_QCheckBox.stateChanged.connect(lambda:self.TestPrint(u"enableViewportText_QCheckBox"))
        ## 갱신 - 불필요?
        self.refresh_button = QtWidgets.QPushButton(u"갱신", default = False, autoDefault = False)
        # self.option_buttonSet_layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.TestPrint)
        # 메뉴설정
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
#%% 자료입력
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
        '''사용안함..'''
        self.ani_frame_tree_widget.clear() 
        for ani_set in self.ani_list:
            item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
            item.setFlags(item.Flags() |QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable)
            item.setText(0,ani_set.name)
            item.setData(1, QtCore.Qt.DisplayRole, ani_set.start_frame)
            item.setData(2, QtCore.Qt.DisplayRole, ani_set.end_frame)
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
                    self.LogPrint(u'자료없음')
                    continue
                ani_item_list = main_str.split(',')
                item = QtWidgets.QTreeWidgetItem(self.ani_frame_tree_widget)
                isSub_int = 0
                for obj_str in ani_item_list:
                    if obj_str :
                        ani_split_list = obj_str.split('~')
                        ani_name =  ani_split_list[0]
                        start_frame = int(ani_split_list[1])
                        end_frame = int(ani_split_list[2])
                        if isSub_int > 0:
                            self.AddData(QtWidgets.QTreeWidgetItem(item), ani_name, start_frame, end_frame)
                        else:
                            self.AddData(item, ani_name, start_frame, end_frame)
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
    def CheckFrameNameString(self, frame_name_string):
        result = False
        if '(' in frame_name_string:
            result = True
        if ')' in frame_name_string:
            result = True
        if ',' in frame_name_string:
            result = True
        return result
    def AddData(self, item, frame_name, start_frame_int, end_frame_int):
        self.LogPrint(u'AddData')
        isFalse = False
        if start_frame_int > end_frame_int:
            self.LogPrint(u'시작 프레임이 작습니다.')
            isFalse = True
        if self.CheckFrameNameString(frame_name):
            self.LogPrint(u'프레임 이름에 잘못된 문자가 들있습니다.')
            isFalse = True
        if isFalse:
            return False
        full_string = (u'{0}~{1}~{2}'.format(frame_name, start_frame_int, end_frame_int))
        item.setText(0,frame_name)
        #item.setText(1,str(start_frame_int))
        item.setData(1, QtCore.Qt.DisplayRole, start_frame_int)
        #item.setText(2,str(end_frame_int))
        item.setData(2, QtCore.Qt.DisplayRole, end_frame_int)
        item.setText(self.m_full_string_key_num, full_string)
        item.setCheckState(0, QtCore.Qt.Unchecked )
    def refreshButtonClicked(self):
        self.ani_frame_tree_widget.clear()
        self.GetPropertyAnisetValue()
    def ChangeInputDataByCurrentIiem(self):
        '''
            더블 클릭 클릭했을때 프레임 입력란에 정보 업데이트
        '''
        self.LogPrint(u'ChangeInputDataByCurrentIiem')
        self.start_frame.setValue(int(self.GetSelectionData(1)))
        self.end_frame.setValue(int(self.GetSelectionData(2)))
        self.frameName_lineEdit.setText(self.GetSelectionData(0))
    def editItme(self):
        qt_QModelIndex = self.GetSelectionQModeIndex()
        qt_item = self.ani_frame_tree_widget.itemFromIndex(qt_QModelIndex)
        self.AddData(qt_item, self.frameName_lineEdit.text(), self.start_frame.value(), self.end_frame.value() )
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
    def ItemDoubleClicked(self):
        self.SetFrameRange()
        self.ChangeInputDataByCurrentIiem()
        RT.redrawViews()
    def SetFrameRange(self):
        ''' '''
        self.LogPrint(u'SetFrameRange')
        start_frame = int(self.GetSelectionData(1))
        end_frame = int(self.GetSelectionData(2))
        if start_frame >= end_frame :
            end_frame = end_frame + 1
        RT.animationRange = RT.interval(start_frame,end_frame)
    #버튼
    def exportMaxFile_Run(self):
        #pass
        checked_file_path_list = []
        def GetCheckList():
            checked_file_path_list = []
            root = self.ani_frame_tree_widget.invisibleRootItem()
            signal_count = root.childCount()
            print(str(signal_count))
            isChecked = QtCore.Qt.Checked
            for i in range(signal_count):
                signal = root.child(i)
                num_children = signal.childCount()
                if signal.checkState(0) == isChecked:
                    checked_file_path_list.append(signal.text(3))
                for n in range(num_children):
                    child = signal.child(n)
                    if child.checkState(0) == isChecked:
                        checked_file_path_list.append(child.text(3))
            return checked_file_path_list
        checked_file_path_list = GetCheckList()
        range_interval = RT.interval
        current_dir = RT.maxfilepath
        current_name = RT.maxFileName
        max_dir = RT.getFilenamePath(current_dir)
        maxfile_name = RT.getFilenameFile(current_name).split(',')[0]
        if checked_file_path_list.count == 0:
            QtWidgets.QMessageBox.about(self, u"알림",u'선택된 것이 없습니다. (Nothing is selected)' )
            return 
        maxfile_name, ok = QtWidgets.QInputDialog.getText(self,u"기본 파일명 입력", u"[입력이름_프레임이름] 형식으로 생성됩니다.",
                                                         QtWidgets.QLineEdit.EchoMode.Normal, maxfile_name)
        if not ok:
            return
        file_save = MaxPlus.FileManager.Save
        current_file = current_dir + current_name
        file_save(current_file)
        file_open = MaxPlus.FileManager.Open
        for path in checked_file_path_list:
            print(path)
            #프레임 설정
            name_list = path.split('~')
            name = name_list[0]
            start_frame = int(name_list[1])
            end_frame = int(name_list[2])
            if start_frame >= end_frame :
                end_frame = end_frame + 1
            RT.animationRange = range_interval(start_frame, end_frame)
            #프레임삭제
            max_script = '''
                fn GetAnimationRange_Interval target_nodeArray:(objects as Array)=
                (
                    local keyIdex_int = 0
                    local startKeyArray = #()
                    local endKeyArray = #()
                    local startFrame = undefined
                    local endFrame = undefined

                    for obj in target_nodeArray do (
                        if classof(obj.controller) == prs do (
                            keyIdex_int = numKeys obj.pos.controller
                            if (keyIdex_int != undefined and keyIdex_int >= 1) do
                            (
                                append startKeyArray (obj.pos.controller.keys[1]).time
                                append endKeyArray (obj.pos.controller.keys[keyIdex_int]).time
                            )
                            keyIdex_int = numKeys obj.rotation.controller
                            if (keyIdex_int != undefined and keyIdex_int >= 1) do
                            (
                                append startKeyArray (obj.rotation.controller.keys[1]).time
                                append endKeyArray (obj.rotation.controller.keys[keyIdex_int]).time
                            )
                            keyIdex_int = numKeys obj.scale.controller
                            if (keyIdex_int != undefined and keyIdex_int >= 1) do
                            (
                                append startKeyArray (obj.scale.controller.keys[1]).time
                                append endKeyArray (obj.scale.controller.keys[keyIdex_int]).time
                            )
                        )
                        if ClassOf obj == Biped_Object do 
                        (
                            keyIdex_int = numKeys obj.controller
                            if (keyIdex_int != undefined and keyIdex_int >= 1) do
                            (
                                append startKeyArray (biped.getKey obj.controller 1).time
                                append endKeyArray (biped.getKey obj.controller keyIdex_int).time
                            )
                        )
                    )
                    makeUniqueArray startKeyArray
                    makeUniqueArray endKeyArray
                    sort startKeyArray
                    sort endKeyArray

                    if startKeyArray.count > 0 then
                    (
                        startFrame
                        startKey_integer = 0
                        i_int = 1
                        --while (startFrame == undefined and i_int < startKeyArray.count  ) do (
                        --    startKey_integer = (startKeyArray[i_int] as integer)/TicksPerFrame
                        --    if startKey_integer > -9999 do 
                        --    (
                        --        startFrame = startKeyArray[i_int]
                        --    )
                        --    i_int = i_int + 1
                        --)
                        startFrame = startKeyArray[i_int]
                        endFrame = endKeyArray[endKeyArray.count]
                    )
                    else 
                    (
                        startFrame = 0
                        endFrame = 1
                    )
                    if (startFrame == undefined ) do 
                    (
                        startFrame = 0
                    )
                    if (endFrame == undefined) do 
                    (
                        endFrame == 1
                    )
                    if (startFrame == endFrame) do 
                    (
                        endFrame = endFrame+1
                    )
                    reInterval = Interval startFrame endFrame
                )
                fn OutOfFrameDelet_fn arg_objs_array =
                (
                    local startFrame =  copy(animationRange.start.frame)
                    local endFrame =  Copy(animationRange.end.frame)
                    local goObjs_array = #()
                    local fullAniRange_interval = GetAnimationRange_Interval()
                    print fullAniRange_interval
                    goObjs_array = arg_objs_array
                        for obj in goObjs_array do
                        (
                            keyIdex_int = 0
                            obj_ctrl = obj.controller
                            deselectKeys obj.controller
                            selectKeys obj.controller
                            deselectKeys obj.controller (interval startFrame endFrame)
                            if ClassOf(obj) == biped_Object do
                            (
                                if (getClassName obj_ctrl == "Body") then
                                (
                                    deleteKeys obj.controller.vertical.controller.keys #selection
                                    deleteKeys obj.controller.horizontal.controller.keys #selection
                                    deleteKeys obj.controller.turning.controller.keys #selection
                                )
                                else if obj.controller.keys.count > 0 do
                                (
                                    deleteKeys obj.controller.keys #selection
                                )
                            )
                            if endFrame < fullAniRange_interval.end do 
                            (
                                deleteTime obj (endFrame+1) (fullAniRange_interval.end + 1)
                            )
                            if fullAniRange_interval.start < (startFrame - 1) do 
                            (
                                deleteTime obj (fullAniRange_interval.start - 1) (startFrame-1) #noSlide
                            )
                        )
                )
                OutOfFrameDelet_fn (objects as Array)
            '''
            RT.execute(max_script)
            #파일저장
            save_file_name = u'{0}\\{1}_{2}.max'.format(max_dir, maxfile_name , name)
            file_save(save_file_name)
            file_open(current_file)
        RT.ShellLaunch(current_dir, "")
    def TestPrint(self, test_string=u"Test"):
        ''' 임시 함수로 인자값이나 기능 테스트용으로 사용 '''
        print("[TestLog] \n" + test_string + "\n\n")
        #index_QModelIndex = self.GetSelectionQModeIndex()
FullAniSetView()

