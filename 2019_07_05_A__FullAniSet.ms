/* 콤보박스를 사용해보자
필요한것
리스트에서 선택 가능
프레임 삭제 및 수정
프레임 추가
구성 : 이름 ~ 넘버 ~ 넘버
입력은 각 개별 입력
입력창 별도 필요할듯
 */
--VersionText = "FullAniSet.ms Va06 1차 버전된듯..."
--VersionText = "FullAniSet.ms Va07 어느정도 해결된듯"
--VersionText = "FullAniSet.ms Va08 1차 완료!!"
--VersionText = "FullAniSet.ms Va11 기본익스포트"
--VersionText = "FullAniSet.ms Va16 프레임 수정 변환시에 프레임 이동"
--VersionText = "FullAniSet.ms Va16.1 이름 저장할때 공백삭제" --2018-12-18
-- 2019-02-24 :
--VersionText = "FullAniSet.ms Va17 단축키 매크로스크립트 추가"
-- 2019-02-25 :
VersionText = "FullAniSet Va17.1 한글변수 영어전환"
global RolloutAniSet
struct AniSet
(
    name,
    startFrame,
    endFrame
)
struct UISetDate
(
    widthGet = 250,
    heightGet = 450,
    fn heightSet value =
    (
        this.heightGet = value
    ),
    fn widthSet value =
    (
        this.widthGet = value
    )
)
AniSetUIDate = UISetDate()
format " \n %" VersionText
(
    local AniSetItemFilter = #()
    local AniSetItemText = ""
    local startFrame = 0
    local endFrame = 1
    local AniName = "이름"
    local widthSet = 350
    local AniSetItems = "" --UI 및 저장에 사용할 문자열값
    local SetAniProperty = #() -- AniSetItems의 관리를 위한 배열값

    fn AniSetExport AniName startFrame endFrame = 
    (
		animationRange = interval startFrame endFrame
		sliderTime = startFrame
		unitsType = units.SystemType
		checkBossAttack = false

		-- Export옵션	
			pluginManager.loadClass FBXExporter -- FBX익스포트 함수를 불러옴			
		-- Gometry 영역	
			FBXExporterSetParam "SmoothingGroups" false
			FBXExporterSetParam "NormalsPerPoly" false
			FBXExporterSetParam "TangentSpaceExport" false
			FBXExporterSetParam "SmoothMeshExport" true
			FBXExporterSetParam "Preserveinstances" false
			FBXExporterSetParam "SelectionSetExport" false
			FBXExporterSetParam "GeomAsBone" true
			FBXExporterSetParam "Triangulate" false
			FBXExporterSetParam "Preserveinstances" true
		-- Animation 영역

            FBXExporterSetParam "Animation" true

			--FBXExporterSetParam "Resampling" float값이 와야함. 잘모르겠음.
			FBXExporterSetParam "UseSceneName" false
			FBXExporterSetParam "Removesinglekeys" false
			FBXExporterSetParam "BakeAnimation" true
			FBXExporterSetParam "BakeFrameStart" startFrame
			FBXExporterSetParam "BakeFrameEnd" endFrame
			FBXExporterSetParam "BakeFrameStep" 1
			FBXExporterSetParam "BakeResampleAnimation" true
		-- Deformations 영역
			FBXExporterSetParam "Skin" true
			FBXExporterSetParam "Shape" true
		-- Curve Filters 영역
			FBXExporterSetParam "FilterKeyReducer" false -- Curve Filters 체크 유무
			-- 하위옵션은 조정불가				
		--	Point Cache File(s) 영역
			FBXExporterSetParam "PointCache" false				
		-- Cameras 영역	
			FBXExporterSetParam "Cameras" true			
		-- Light	영역
			FBXExporterSetParam "Lights" true			
		-- Embed Media 영역
            FBXExporterSetParam "EmbedTextures" true
		-- Advanced Options 영역
			FBXExporterSetParam "ScaleFactor" 1 -- ScaleFactor의 Automatic를 체크한 효과	
			if (unitsType == #meters) then
			(
				FBXExporterSetParam "ConvertUnit" "m"
                unitsTypeTxt = "(0.01)"
			)
			else if (unitsType == #centimeters) then
			(
				FBXExporterSetParam "ConvertUnit" "cm"
                unitsTypeTxt = "(1)"
			)
			FBXExporterSetParam "UpAxis" "Y"
			FBXExporterSetParam "ShowWarnings" false
			FBXExporterSetParam "GenerateLog" false
			FBXExporterSetParam "ASCII" false
			FBXExporterSetParam "FileVersion" "FBX2014/2015"
        
     -- 익스포트 분기
        exptFileName = getFilenameFile maxFileName --맥스의 파일명을 구함.
        unitsTypeTxt = unitsTypeTxt + "@"
        modelNo = ""
        --format "\n애니 익스포트 시작\n"
        exptFileNameArr = filterstring (getFilenameFile maxFileName) " @#,_"
        --저장되지 않은 파일일 경우
        try
        (
            ChrName = toLower exptFileNameArr[1] --케릭터 이름
            pathFile = maxfilepath + "\\" + ChrName + unitsTypeTxt + AniName + ".fbx"
        )
        catch
        ( 
            ChrName ="Untitled"
            pathFile = (GetDir #maxstart) + "\\" + ChrName + unitsTypeTxt + AniName + ".fbx"
            saveMaxFile AniName 
        )
        exportFile pathFile #noPrompt selectedOnly:true --using:FBXEXP
        --format "AniSetExport 분활 익스포트가 아닐때 \n"
        print pathFile      
        --format "export_fn 애니 익스포트 끝 \n"
    )
    fn PropertyNameFilter_fn itemName = --입력한 문자기반으로 필요한것 구분
    (-- AniSetItemFilter #()" AniName startFrame endFrame
        --format " \n AniSetItemFilter itemName %  \n" itemName
        if itemName != undefined do
        (
            AniSetItemFilter = filterstring itemName "-@~"
            AniName    = (AniSetItemFilter[1] as string)
            startFrame = (AniSetItemFilter[2] as integer)
            endFrame   = (AniSetItemFilter[3] as integer)
            local newAniSet = AniSet()
            newAniSet.name    = (AniSetItemFilter[1] as string)
            newAniSet.startFrame = (AniSetItemFilter[2] as integer)
            newAniSet.endFrame   = (AniSetItemFilter[3] as integer)
        )
        --format " \n AniSetItemFilter % % % \n" AniName startFrame endFrame
       -- AniSetItemFilter
       newAniSet
    )--AniSet
    fn SetAniPropertyToAniSetItems_fn obj =
    ( --배열을 저장을 위한 텍스트로 변환
        local NewItems = ""
        for i = 1 to obj.count do
        (
            stringTrimRight = trimright (obj[i] as string)
            append NewItems ("," + stringTrimRight)
        )
        AniSetItems = substring NewItems 2 NewItems.count -- 멘 앞의 ,를 삭제하기 위해서
    )
    fn setting_fn = -- 초기값 설정
    (
        local PropertyNum = 0
        PropertyNum = fileProperties.findProperty #custom "SetAniProperty"
        --format " \n setting_fn PropertyNum % \n" PropertyNum
        if 0 == PropertyNum then
        (
        )
        else
        (--정보가 있으면 받아서 SetAniProperty 에 저장하는 구간
            AniSetItems = (fileProperties.getPropertyValue #custom PropertyNum as string)
            --AniSetItems as string
            --format " \n setting_fn AniSetItems  % \n" AniSetItems
            SetAniProperty = filterstring (AniSetItems as string) ","
            --format " \n setting_fn SetAniProperty % \n" SetAniProperty
        )
    )
    fn update_fn = --정보 갱신 및 저장
    (--Rollout에 있는 리스트를 문자열로 변화후 SetAniPropert에 저장하고 UI상단 정보를 갱신함
        sort SetAniProperty
        SetAniPropertyToAniSetItems_fn SetAniProperty --저장하기 위해서 AniSetItems 를 갱신
        --format "\n update_fn AniSetItems % \n" AniSetItems
        fileProperties.addProperty #custom "SetAniProperty" AniSetItems
        max hold
        RolloutAniSet.UIAniName.text = (AniName as string)
        RolloutAniSet.UIStartFrame.value = startFrame as integer
        RolloutAniSet.UIEndFrame.value  = endFrame as integer
        SetAniProperty = filterstring (AniSetItems as string) ","
        sort SetAniProperty
        RolloutAniSet.UIAniSet.items = SetAniProperty
    )
    fn frameRangeChange_Fn stringName =
    (
        PropertyNameFilter_fn stringName
        animationRange = interval startFrame endFrame
        sliderTime = startFrame
        update_fn()
    )
    fn AllDelet =
    (
        AniSetItems = ""
        SetAniProperty = #()
        yesNoCancelBox "모든값 삭제하시겠습니까."
        if #yes == yesNoCancelBox do
        (
            fileProperties.deleteProperty #custom "SetAniProperty"
            max hold
        )
        update_fn()
    )
    fn SaveAniSet_fn aniName_string startFrame_int endFrame_int =
    (
        newItemText = ""
        AniName = aniName_string
        startFrame = (startFrame_int as string) as integer --소수점 안나오게 두번 변환
        endFrame = (endFrame_int as string) as integer
        newItemText =  AniName + "~" + (startFrame as string) +"~" + (endFrame as string)
        append SetAniProperty newItemText 
        --print SetAniProperty
        update_fn() --저장 및 갱신
    )
    fn DeletAniSet_fn itemName_string =
    (
        deleteName = itemName_string --선택한것

        for i = 1 to SetAniProperty.count do
        (
            if deleteName == SetAniProperty[i] do
            (
                deleteitem SetAniProperty i
            )
        )
        --format " \n UIdeletButton % \n" deleteName
        update_fn()
    )
    fn Fn_cutOutRangeKey objs =
    (
        local startFrame =  copy(animationRange.start.frame)
        local endFrame =  Copy(animationRange.end.frame)
        local bipcoms = #() --다중 바이패드를 찾기 위한 임시 모음
        try
        (
            --local a_bipedParts = bipedObjects
            for obj in objs do
            (
				--format "% start \n" obj.name
                deselectKeys obj.controller
                selectKeys obj.controller
                deselectKeys obj.controller (interval startFrame endFrame)
                if ClassOf(obj) == biped_Object do
                (
                    if obj == (biped.getNode obj #vertical) then
                    (
                        deleteKeys obj.controller.vertical.controller.keys #selection
                        deleteKeys obj.controller.horizontal.controller.keys #selection
                        deleteKeys obj.controller.turning.controller.keys #selection
                        append bipcoms obj
                    )
                    else if obj.controller.keys.count > 0 do
                    (
                        deleteKeys obj.controller.keys #selection
                    )
                )
                deleteTime obj endFrame 10000
                -- in임시 키만 삭제
                -- 앞프레임을 삭제하는건 바이페드 IK로 인하여 중복 삭제되는 문제가 발생함.
                -- 파일 저장후 타임바 수작업 필요
                deleteTime obj 0 startFrame #noSlide
                -- out 임시 키만 삭제
            )
            -- out 뒷 프레임 삭제
        )catch(print "벗어난프레임정리 오류")	
    )
	rollout RolloutAniSet "프레임셋" width:AniSetUIDate.widthGet height:AniSetUIDate.heightGet
	(
        group "설정"
        (
            edittext UIAniName "Name : " text:"" fieldWidth:100 offset:[5,0]
            spinner UIStartFrame "프레임 :     " fieldwidth:40 type:#integer  range:[-10000,10000,(startFrame as string) as integer] offset:[-10,0] across:2
            spinner UIEndFrame    " ~    "     fieldwidth:40  type:#integer range:[-10000,10000,(endFrame as string) as integer]   offset:[-20,0]
            button UIsaveButton "저장" offset:[0,0] across:4 align:#rigth 
            button UIdeletButton "삭제" offset:[0,0] align:#left
            button UIChangeButton "수정" offset:[0,0] align:#left
            button UIFbxButton "FBX" offset:[0,0] --align:#rigth
        
            on UIAniName entered txt do
            (
                if txt != "" do
                (
                    AniName = txt
                    --format " \n UIAniName % \n" AniName
                )
            )
            on UIStartFrame entered do
            (
                startFrame = UIStartFrame.value as integer
                --format " \n UIStartFrame % \n" startFrame
                animationRange = interval startFrame endFrame
            )
            on UIEndFrame entered do
            (
                endFrame = UIEndFrame.value as integer
                --format " \n UIEndFrame % \n" endFrame
                animationRange = interval startFrame endFrame
                
            )
            /* 
            on UIsaveButton pressed do -- 설정에 있는값을 fileProperties에 저장
            (
                newItemText = ""
                AniName = UIAniName.text
                startFrame = (UIStartFrame.value as string) as integer --소수점 안나오게 두번 변환
                endFrame = (UIEndFrame.value as string) as integer
                newItemText =  AniName + "~" + (startFrame as string) +"~" + (endFrame as string)
                append SetAniProperty newItemText 
                print SetAniProperty
                update_fn() --저장 및 갱신
            )
            on UIdeletButton pressed do --목록을 가져와서 이름 찾고 해당 목록 삭제
            (
                deleteName = RolloutAniSet.UIAniSet.selected --선택한것

                for i = 1 to SetAniProperty.count do
                (
                    if deleteName == SetAniProperty[i] do
                    (
                        deleteitem SetAniProperty i
                    )
                )
                --format " \n UIdeletButton % \n" deleteName
                update_fn()
            )
             */
            on UIsaveButton pressed do
            (
                saveAniSet_fn UIAniName.text UIStartFrame.value UIEndFrame.value
                animationRange = interval (UIStartFrame.value as integer) (UIEndFrame.value as integer)
            )
            on UIdeletButton pressed do
            (
                DeletAniSet_fn RolloutAniSet.UIAniSet.selected
            )
            on UIChangeButton pressed do --목록을 가져와서 이름 찾고 해당 목록 삭제
            (
                DeletAniSet_fn RolloutAniSet.UIAniSet.selected --선택한것
                saveAniSet_fn UIAniName.text UIStartFrame.value UIEndFrame.value
                animationRange = interval (UIStartFrame.value as integer) (UIEndFrame.value as integer)
            )
            on UIdeletButton rightclick do
            (
                AllDelet()
            )
            on UIFbxButton pressed do --해당프레임 익스포트
            (
                exportObjSelect_fn()
                AniSetExport UIAniName.text UIStartFrame.value UIEndFrame.value
            )
        )
        group ""
        (
            combobox UIAniSet "프레임셋" items:#("") height:14 offset:[0,0] align:#center
            on UIAniSet selected i do
            ( --선택 목록이 있을대만 작동
                if undefined != UIAniSet.selected do
                (
                    --PropertyNameFilter_fn UIAniSet.selected
                    --animationRange = interval startFrame endFrame
                    --sliderTime = startFrame
                    --update_fn()

                    frameRangeChange_Fn UIAniSet.selected
                )
            )

            button UIMaxFrame "수정" offset:[0,0] align:#Right
        )
        group ""
        (
            --button UISetting "갱신" offset:[0,0] 
            edittext UI_saveName "접두사:" text:maxFileName fieldWidth:100 offset:[0,0] across:2
            button UI_maxFileSave "각파일분활" offset:[15,0] 
            button UIAllDelet "모두삭제" offset:[0,0]
            on UISetting pressed do
            (
                max hold
                DestroyDialog RolloutAniSet
                createdialog RolloutAniSet AniSetUIDate.widthGet AniSetUIDate.heightGet
            )
            on UI_maxFileSave pressed do
            (
                local itemList = UIAniSet.items
                local getMaxfile = maxFilePath + maxFileName
                for i in itemList do
                (
                    local newAniSet = PropertyNameFilter_fn i
                    animationRange = interval newAniSet.startFrame newAniSet.endFrame
                    sliderTime = newAniSet.startFrame
                    local objs = objects as array
                    Fn_cutOutRangeKey (objects as array)
                    fileProperties.deleteProperty #custom "SetAniProperty"
                    saveMaxFile (maxfilepath + "\\" + UI_saveName.text + "@" + newAniSet.name + " ,Va00")
                    loadmaxfile getMaxfile useFileUnits:true quiet:true
                )
            )
            on UIAllDelet pressed do
            (
                AllDelet()
            )
        )
        on RolloutAniSet open do
        (
            --UIAniSet.height = 150
            local fileNameTemp = maxFileName
            if fileNameTemp == "" do fileNameTemp = "Untitled"
            UI_saveName.text = (filterstring fileNameTemp " @,")[1]
            UIAniSet.width = ((AniSetUIDate.widthGet)-50)
            setting_fn()
            update_fn()
            --format "\n RolloutAniSet open % \n" "시작"
        )
	)
)
createdialog RolloutAniSet AniSetUIDate.widthGet AniSetUIDate.heightGet

macroScript SEO_FullAniSet
category:"_AniSeoHyun"
tooltip:"FullAniSet"
icon:#("AnimLayerToolbar", 8)
(
    filein (getdir  #userScripts + "\\SEO_FullAniSet\\SEO_FullAniSet.ms")
)