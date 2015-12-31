## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import ScreenInput
import CvEventInterface
import CvScreenEnums
import time
import Popup as PyPopup

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvWorldBuilderScreen:
	"World Builder Screen"

	def __init__ (self) :
		print("init-ing world builder screen")
		self.m_advancedStartTabCtrl = None
		self.m_normalPlayerTabCtrl = 0
		self.m_normalMapTabCtrl = 0
		self.m_tabCtrlEdit = 0
		self.m_bCtrlEditUp = False
		self.m_bUnitEdit = False
		self.m_bCityEdit = False
		self.m_bNormalPlayer = True
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = False
		self.m_bUnitEditCtrl = False
		self.m_bCityEditCtrl = False
		self.m_bShowBigBrush = False
		self.m_bLeftMouseDown = False
		self.m_bRightMouseDown = False
		self.m_bChangeFocus = False
		self.m_iNormalPlayerCurrentIndexes = []
		self.m_iNormalMapCurrentIndexes = []
		self.m_iNormalMapCurrentList = []
		self.m_iAdvancedStartCurrentIndexes = []
		self.m_iAdvancedStartCurrentList = []
		self.m_iCurrentPlayer = 0
		self.m_iCurrentTeam = 0
		self.m_iCurrentUnitPlayer = 0
		self.m_iCurrentUnit = 0
		self.m_iCurrentX = -1
		self.m_iCurrentY = -1
		self.m_pCurrentPlot = 0
		self.m_pActivePlot = 0
		self.m_pRiverStartPlot = -1
		
		self.m_iUnitTabID = -1
		self.m_iBuildingTabID = -1
		self.m_iTechnologyTabID = -1
		self.m_iImprovementTabID = -1
		self.m_iBonusTabID = -1
		self.m_iImprovementListID = -1
		self.m_iBonusListID = -1
		self.m_iTerrainTabID = -1
		self.m_iTerrainListID = -1
		self.m_iFeatureListID = -1
		self.m_iPlotTypeListID = -1
		self.m_iRouteListID = -1
		self.m_iTerritoryTabID = -1
		self.m_iTerritoryListID = -1
		
		self.m_iASUnitTabID = -1
		self.m_iASUnitListID = -1
		self.m_iASCityTabID = -1
		self.m_iASCityListID = -1
		self.m_iASBuildingsListID = -1
		self.m_iASAutomateListID = -1
		self.m_iASImprovementsTabID = -1
		self.m_iASRoutesListID = -1
		self.m_iASImprovementsListID = -1
		self.m_iASVisibilityTabID = -1
		self.m_iASVisibilityListID = -1
		self.m_iASTechTabID = -1
		self.m_iASTechListID = -1
		
		self.m_iBrushSizeTabID = -1
		self.m_iBrushWidth = 1
		self.m_iBrushHeight = 1
		self.m_iUnitEditCheckboxID = -1
		self.m_iCityEditCheckboxID = -1
		self.m_iNormalPlayerCheckboxID = -1
		self.m_iNormalMapCheckboxID = -1
		self.m_iRevealTileCheckboxID = -1
		self.m_iDiplomacyCheckboxID = -1
		self.m_iLandmarkCheckboxID = -1
		self.m_iEraseCheckboxID = -1
		self.iScreenWidth = 228
		
		self.m_bSideMenuDirty = false
		self.m_bASItemCostDirty = false
		self.m_iCost = 0


## Platy Builder ##
		self.m_iNewCivilization = -1
		self.m_iNewLeaderType = -1
		self.m_iImprovement = 0
		self.m_iYield = 0
		self.m_iDomain = 0
		self.m_iRoute = 0
		self.m_iOtherPlayer = 0
		self.m_iOtherTeam = 0
		self.m_iMemory = 0
		self.m_pScript = -1
		self.m_bMoveUnit = False
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Platy Builder ##

	def interfaceScreen (self):
		# This is the main interface screen, create it as such
		self.initVars()
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		screen.setCloseOnEscape(False)
		screen.setAlwaysShown(True)

		self.setSideMenu()
		self.refreshSideMenu()

		#add interface items
		self.refreshPlayerTabCtrl()
		
		self.refreshAdvancedStartTabCtrl(false)
		
		if (CyInterface().isInAdvancedStart()):
			pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
			pPlot = pPlayer.getStartingPlot()
			CyCamera().JustLookAtPlot(pPlot)

		self.m_normalMapTabCtrl = getWBToolNormalMapTabCtrl()

		self.m_normalMapTabCtrl.setNumColumns((gc.getNumBonusInfos()/10)+1);
		self.m_normalMapTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_IMPROVEMENTS",()));
		self.m_iImprovementTabID = 0
		self.m_iNormalMapCurrentIndexes.append(0)

		self.m_iNormalMapCurrentList.append(0)
		self.m_iImprovementListID = 0

		self.m_normalMapTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_BONUSES", ()));
		self.m_iBonusTabID = 1
		self.m_iNormalMapCurrentIndexes.append(0)

		self.m_iNormalMapCurrentList.append(0)
		self.m_iBonusListID = 0

		self.m_normalMapTabCtrl.setNumColumns((gc.getNumTerrainInfos()/10)+1);
		self.m_normalMapTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_TERRAINS",()))
		self.m_iTerrainTabID = 2
		self.m_iNormalMapCurrentIndexes.append(0)

		self.m_iNormalMapCurrentList.append(0)
		self.m_iTerrainListID = 0
		self.m_iPlotTypeListID = 1
		self.m_iFeatureListID = 2
		self.m_iRouteListID = 3
		
		# Territory
		
		self.m_normalMapTabCtrl.setNumColumns(8);
		self.m_normalMapTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_TERRITORY",()))
		self.m_iTerritoryTabID = 3
		self.m_iNormalMapCurrentIndexes.append(0)

		self.m_iNormalMapCurrentList.append(0)
		self.m_iTerritoryListID = 0

		# This should be a forced redraw screen
		screen.setForcedRedraw( True )

		screen.setDimensions( 0, 0, screen.getXResolution(), screen.getYResolution() )
		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

		setWBInitialCtrlTabPlacement()
		return 0

	def killScreen(self):
		if (self.m_tabCtrlEdit != 0):
			self.m_tabCtrlEdit.destroy()
			self.m_tabCtrlEdit = 0
			
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		screen.hideScreen()
		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)

	def handleInput (self, inputClass):				
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) and inputClass.isShiftKeyDown() and inputClass.isCtrlKeyDown():
			return 1
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() == "WorldBuilderPlayerChoice"):
				self.handlePlayerUnitPullDownCB(inputClass.getData())
## Player Game Data ##
			elif(inputClass.getFunctionName() == "WorldBuilderGameData"):
				self.handleWorldBuilderGameDataPullDownCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderAddUnits"):
				self.handleWorldBuilderAddUnitsPullDownCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderUnitCombat"):
				self.handleWorldBuilderUnitCombatPullDownCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderEditAreaMap"):
				self.handleWorldBuilderEditAreaMapPullDownCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderModifyAreaPlotType"):
				self.handleWorldBuilderModifyAreaPlotTypePullDownCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderModifyAreaTerrain"):
				self.handleWorldBuilderModifyAreaTerrainPullDownCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderModifyAreaRoute"):
				self.handleWorldBuilderModifyAreaRoutePullDownCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderModifyAreaFeature"):
				self.handleWorldBuilderModifyAreaFeaturePullDownCB(inputClass.getData())
## Player Game Data ##
			elif(inputClass.getFunctionName() == "WorldBuilderBrushSize"):
				self.handleBrushHeightCB(inputClass.getData())
				self.handleBrushWidthCB(inputClass.getData())
			elif(inputClass.getFunctionName() == "WorldBuilderTeamChoice"):
				self.handleSelectTeamPullDownCB(inputClass.getData())
		return 1

	def mouseOverPlot (self, argsList):
				
		if (self.m_bReveal):
			self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
			if (CyInterface().isLeftMouseDown() and self.m_bLeftMouseDown):
				self.setMultipleReveal(True)
			elif(CyInterface().isRightMouseDown() and self.m_bRightMouseDown):
				self.setMultipleReveal(False)
		else: #if ((self.m_tabCtrlEdit == 0) or (not self.m_tabCtrlEdit.isEnabled())):
			self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
			self.m_iCurrentX = self.m_pCurrentPlot.getX()
			self.m_iCurrentY = self.m_pCurrentPlot.getY()
			if (CyInterface().isLeftMouseDown() and self.m_bLeftMouseDown):
				if (self.useLargeBrush()):
					self.placeMultipleObjects()
				else:
					self.placeObject()
			elif (CyInterface().isRightMouseDown() and self.m_bRightMouseDown):
				if (not (self.m_bCityEdit or self.m_bUnitEdit)):
					if (self.useLargeBrush()):
						self.removeMultipleObjects()
					else:
						self.removeObject()
		return

	def getHighlightPlot (self, argsList):
		
		self.refreshASItemCost()
		
		if (self.m_pCurrentPlot != 0):
#			if (CyInterface().isInAdvancedStart() and self.m_pCurrentPlot.isAdjacentNonrevealed(CyGame().getActiveTeam())):
#				if (self.getASActiveVisibility() == -1):
#					return []
			if (CyInterface().isInAdvancedStart()):
				if (self.m_iCost <= 0):
					return []
				
		if ((self.m_pCurrentPlot != 0) and not self.m_bShowBigBrush and isMouseOverGameSurface()):
			return (self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY())
			
		return []
	
	def leftMouseDown (self, argsList):
		bShift, bCtrl, bAlt = argsList
		self.m_bLeftMouseDown = True

		if CyInterface().isInAdvancedStart():
			self.placeObject()
			return 1
## Edit Area Map ##
		if self.m_bPickArea:
			self.m_iArea = self.m_pCurrentPlot.getArea()
			self.refreshSideMenu()
			return 1
## Add Units ##
		elif self.m_iUnitType > -1:
			pNewUnit = gc.getPlayer(self.m_iCurrentPlayer).initUnit(self.m_iUnitType, self.m_iCurrentX, self.m_iCurrentY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			return 1
## Move Unit Start ##
		elif self.m_bMoveUnit:
			pUnit = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
			pNewUnit = gc.getPlayer(self.m_iCurrentPlayer).initUnit(pUnit.getUnitType(), self.m_iCurrentX, self.m_iCurrentY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			pNewUnit.convert(pUnit)
			pNewUnit.setBaseCombatStr(pUnit.baseCombatStr())
			pNewUnit.changeCargoSpace(pUnit.cargoSpace() - pNewUnit.cargoSpace())
			pNewUnit.setImmobileTimer(pUnit.getImmobileTimer())
			pNewUnit.setScriptData(pUnit.getScriptData())
			pUnit.kill(False, -1)
			self.m_bMoveUnit = False
			self.toggleUnitEditCB()
			return 1
## Move Unit End ##
		elif (bAlt and bCtrl) or  (self.m_bUnitEdit):
			if (self.m_pCurrentPlot.getNumUnits() > 0):
				self.m_iCurrentUnit = 0
				self.setUnitEditInfo(False)
			return 1
		elif (bCtrl) or (self.m_bCityEdit):
			if (self.m_pCurrentPlot.isCity()):
				self.initCityEditScreen()
			return 1
		elif (self.m_bReveal):
			if (self.m_pCurrentPlot != 0):
				self.setMultipleReveal(True)
		elif (bShift and not bCtrl and not bAlt):
			self.setPlotEditInfo(True)
			return 1

		if (self.useLargeBrush()):
			self.placeMultipleObjects()
		else:
			self.placeObject()
		return 1

	def rightMouseDown (self, argsList):
		self.m_bRightMouseDown = True

		if CyInterface().isInAdvancedStart():
			self.removeObject()
			return 1

		if (self.m_bCityEdit or self.m_bUnitEdit):
			self.setPlotEditInfo(True)
		elif (self.m_bReveal):
			if (self.m_pCurrentPlot != 0):
				self.setMultipleReveal(False)
		else:
			if (self.useLargeBrush()):
				self.removeMultipleObjects()
			else:
				self.removeObject()
			
		return 1

	def update(self, fDelta):
		if (not CyInterface().isLeftMouseDown()):
			self.m_bLeftMouseDown = False
		if (not CyInterface().isRightMouseDown()):
			self.m_bRightMouseDown = False

		if (not self.m_bChangeFocus) and (not isMouseOverGameSurface()):
			self.m_bChangeFocus = True

		if (self.m_bChangeFocus and isMouseOverGameSurface() and (not self.m_bUnitEdit and not self.m_bCityEdit)):
			self.m_bChangeFocus = False
			setFocusToCVG()
		return

	# Will update the screen (every 250 MS)
	def updateScreen(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		
		if (CyInterface().isInAdvancedStart()):
			if (self.m_bSideMenuDirty):
				self.refreshSideMenu()
			if (self.m_bASItemCostDirty):
				self.refreshASItemCost()
		
		if (CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT) and not CyInterface().isFocusedWidget()):
			self.refreshAdvancedStartTabCtrl(true)
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, false)
		
		if (self.useLargeBrush()):
			self.m_bShowBigBrush = True
		else:
			self.m_bShowBigBrush = False

		if (self.m_bCtrlEditUp):
			if ( (not self.m_bUnitEdit) and (not self.m_bCityEdit) and (not self.m_tabCtrlEdit.isEnabled()) and not CyInterface().isInAdvancedStart()):
				if (self.m_bNormalMap):
					self.m_normalMapTabCtrl.enable(True)
				if (self.m_bNormalPlayer):
					self.m_normalPlayerTabCtrl.enable(True)
				self.m_bCtrlEditUp = False
				return 0
		if ((self.m_bNormalMap) and(self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID) and (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iRouteListID)):
			if (self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] == gc.getNumRouteInfos()):
				if (self.m_pRiverStartPlot != -1):
					self.setRiverHighlights()
					return 0
		self.highlightBrush()
		return 0

	def redraw( self ):
		return 0

	def resetTechButtons( self ) :
		for i in range (gc.getNumTechInfos()):
			strName = "Tech_%s" %(i,)
			self.m_normalPlayerTabCtrl.setCheckBoxState("Technologies", gc.getTechInfo(i).getDescription(), gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).isHasTech(i))
		return 1
## Platy Change All Plots Start ##
	def handleAllPlotsCB ( self, popupReturn ) :
		iButton = popupReturn.getButtonClicked()
		iCount = 0
		for i in range (gc.getNumTerrainInfos()):
			if gc.getTerrainInfo(i).isGraphicalOnly(): continue
			iCount += 1
		if (iButton < PlotTypes.NUM_PLOT_TYPES + iCount):
			iTempVal = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
			self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] = iButton
			self.setAllPlots()
			self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] = iTempVal
		if (not (self.m_bUnitEdit or self.m_bCityEdit)):
			self.m_normalPlayerTabCtrl.enable(self.m_bNormalPlayer)
			self.m_normalMapTabCtrl.enable(self.m_bNormalMap)
		else:
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
		return 1

	def allPlotsCB(self):
		self.m_normalPlayerTabCtrl.enable(False)
		self.m_normalMapTabCtrl.enable(False)
		if (self.m_tabCtrlEdit != 0):
			self.m_tabCtrlEdit.enable(False)

		popup=PyPopup.PyPopup(CvUtil.EventWBAllPlotsPopup, EventContextTypes.EVENTCONTEXT_ALL)
		iPopupWidth = 200
		

		popup.setHeaderString(localText.getText("TXT_KEY_WB_CHANGE_ALL_PLOTS",()))

		iCount = 0
		for i in range (PlotTypes.NUM_PLOT_TYPES):
			if (i==0):
				popup.addButton(localText.getText("TXT_KEY_WB_ADD_MOUNTAIN",()))
			elif(i==1):
				popup.addButton(localText.getText("TXT_KEY_WB_ADD_HILL",()))
			elif(i==2):
				popup.addButton(localText.getText("TXT_KEY_WB_ADD_GRASS",()))
			elif(i==3):
				popup.addButton(localText.getText("TXT_KEY_WB_ADD_OCEAN",()))
			iCount += 1
		for i in range (gc.getNumTerrainInfos()):
			if gc.getTerrainInfo(i).isGraphicalOnly(): continue
			popup.addButton(gc.getTerrainInfo(i).getDescription())
			iCount += 1
		iPopupHeight = 39 * iCount
		popup.setSize(iPopupWidth, iPopupHeight)

		popup.addButton(localText.getText("TXT_KEY_SCREEN_CANCEL", ()))
		popup.launch(False)
		return 1

	def refreshReveal ( self ) :
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		for i in range (CyMap().getGridWidth()):
			for j in range (CyMap().getGridHeight()):
				pPlot = CyMap().plot(i,j)
				if (not pPlot.isNone()):
					self.showRevealed(pPlot)
		return 1

	def setAllPlots ( self ) :
		iPlotType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
		if iPlotType < PlotTypes.NUM_PLOT_TYPES:
			CyMap().setAllPlotTypes(iPlotType)
		else:
			lTerrain = []
			for i in xrange(gc.getNumTerrainInfos()):
				if gc.getTerrainInfo(i).isGraphicalOnly(): continue
				lTerrain.append(i)
			iTerrainType = iPlotType - PlotTypes.NUM_PLOT_TYPES
			bWater = False
			if gc.getTerrainInfo(iTerrainType).isWater():
				bWater = True
			for i in xrange (CyMap().getGridWidth()):
				for j in xrange (CyMap().getGridHeight()):
					pPlot = CyMap().plot(i,j)
					if (not pPlot.isNone()):
						if bWater and pPlot.isWater():
							pPlot.setTerrainType(lTerrain[iTerrainType], True, True)
						elif (not bWater) and (not pPlot.isWater()):
							pPlot.setTerrainType(lTerrain[iTerrainType], True, True)	
		return 1
## Platy Change All Plots End ##

	def handleUnitEditExperienceCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setExperience(int(argsList[0]),-1)
		return 1

	def handleUnitEditLevelCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setLevel(int(argsList[0]))
		return 1
#東方叙事詩・統合MOD追記
#powerをWB上で調整
	def handleUnitEditPowerCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setPower(int(argsList[0]))
		return 1

#CALをWB上で調整
	def handleUnitEditCALCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setNumAcquisSpellPromotion(int(argsList[0]) -1)
		return 1

#東方叙事詩・統合MOD追記ここまで

	def handleUnitEditNameCB (self, argsList) :
		if ((len(argsList[0]) < 1) or (self.m_pActivePlot == 0) or (self.m_iCurrentUnit < 0) or (self.m_pActivePlot.getNumUnits() <= self.m_iCurrentUnit)):
			return 1
		szNewName = argsList[0]
		unit = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
		if (unit):
			unit.setName(szNewName)
		return 1

## Platy World Builder Start ##
## Enter New Screen ##
	def handleEnterNewScreenCB ( self, argsList ) :
		strName = argsList[0]
		if strName == "PromotionEditScreen":
			self.setPromotionEditInfo()	
		elif strName == "BackToUnit":
			self.setUnitEditInfo(True)
		elif strName == "BackToTeam":
			self.setTeamEditInfo()
		elif strName == "ProjectEditScreen":
			self.setProjectEditInfo()
		elif strName == "TechEditScreen":
			self.setTechnologyEditInfo()
		elif strName == "BuildingEditScreen":
			self.setBuildingEditInfo()
		elif strName == "WonderEditScreen":
			self.setWonderEditInfo()
		elif strName == "ReligionEditScreen":
			self.setReligionEditInfo()
		elif strName == "CorporationEditScreen":
			self.setCorporationEditInfo()
		elif strName == "FreeSpecialistEditScreen":
			self.setFreeSpecialistEditInfo()
		elif strName == "GreatPeopleEditScreen":
			self.setGreatPeopleEditInfo()
		elif strName == "FreeBonusEditScreen":
			self.setFreeBonusEditInfo()
		elif strName == "BackToCity":
			self.setCityEditInfo(True)
		return 1
## Current Player ##
	def handleCurrentPlayerEditPullDownCB ( self, argsList ) :
		iIndex, strName = argsList
		iCount = 0
		for i in xrange(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive():
				if iCount == int(iIndex):
					self.m_iCurrentPlayer = i
					self.m_iCurrentTeam = gc.getPlayer(i).getTeam()
					if strName == "PlayerEditCurrentPlayer":
						self.setPlayerEditInfo()
						self.refreshSideMenu()
					elif strName == "DiplomacyEditCurrentPlayer":
						self.setDiplomacyEditInfo()
					elif strName == "PlotEditCurrentPlayer":
						self.setPlotEditInfo(False)
					elif strName == "UnitEditOwner":
						pUnit = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
						pNewUnit = gc.getPlayer(i).initUnit(pUnit.getUnitType(), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
						pNewUnit.convert(pUnit)
						pNewUnit.setBaseCombatStr(pUnit.baseCombatStr())
						pNewUnit.changeCargoSpace(pUnit.cargoSpace() - pNewUnit.cargoSpace())
						pNewUnit.setImmobileTimer(pUnit.getImmobileTimer())
						pUnit.kill(False, -1)
						self.setUnitEditInfo(True)
					elif strName == "CityEditOwner":
						gc.getPlayer(i).acquireCity(self.m_pActivePlot.getPlotCity(), False, True)
						self.setCityEditInfo(True)
					return 1
				iCount += 1


## Side Panel ##
	def handleWorldBuilderGameDataPullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		if iIndex == 0:
			self.setPlayerEditInfo()
		elif iIndex == 1:
			self.setTeamEditInfo()
		elif iIndex == 2:
			self.setGameOptionEditInfo()
		elif iIndex == 3:
			if CyGame().countCivPlayersEverAlive() != gc.getMAX_CIV_PLAYERS():
				self.AddNewPlayer(True)
		return 1

	def handleWorldBuilderAddUnitsPullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		if iIndex <= gc.getNumUnitCombatInfos():
			self.m_iUnitCombat = iIndex -1
			self.m_iUnitType = -1
		else:
			self.m_iUnitCombat = -2
		self.refreshSideMenu()
		return 1

	def handleWorldBuilderUnitCombatPullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		iCount = 0
		for i in xrange(gc.getNumUnitInfos()):
			if gc.getUnitInfo(i).getUnitCombatType() == self.m_iUnitCombat:
				if iCount == iIndex:
					self.m_iUnitType = i
					return 1
				iCount += 1
		self.m_iUnitType = -1
		return 1

	def handleWorldBuilderEditAreaMapPullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		if iIndex == 0:
			self.m_bPickArea = True
			self.m_bChangeAllPlots = False
			self.m_iArea = -1
		elif iIndex == 1:
			self.m_bPickArea = False
			self.m_bChangeAllPlots = True
		self.refreshSideMenu()
		return 1

	def handleWorldBuilderModifyAreaPlotTypePullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		if self.m_bChangeAllPlots:
			CyMap().setAllPlotTypes(iIndex)
		else:
			for i in xrange (CyMap().getGridWidth()):
				for j in xrange (CyMap().getGridHeight()):
					pPlot = CyMap().plot(i,j)
					if (not pPlot.isNone()) and pPlot.getArea() == self.m_iArea:
						if iIndex == 0:
							pPlot.setPlotType(PlotTypes.PLOT_PEAK, True, True)
						elif iIndex == 1:
							pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
						elif iIndex == 2:
							pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
						elif iIndex == 3:
							pPlot.setPlotType(PlotTypes.PLOT_OCEAN, True, True)
		self.refreshSideMenu()
		return 1

	def handleWorldBuilderModifyAreaTerrainPullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		lTerrain = []
		for i in xrange(gc.getNumTerrainInfos()):
			if gc.getTerrainInfo(i).isGraphicalOnly(): continue
			if self.m_bChangeAllPlots:
				lTerrain.append(i)
			elif CyMap().getArea(self.m_iArea).isWater() and gc.getTerrainInfo(i).isWater():
				lTerrain.append(i)
			elif not CyMap().getArea(self.m_iArea).isWater() and not gc.getTerrainInfo(i).isWater():
				lTerrain.append(i)
		for i in xrange (CyMap().getGridWidth()):
			for j in xrange (CyMap().getGridHeight()):
				pPlot = CyMap().plot(i,j)
				if pPlot.isNone(): continue
				if self.m_bChangeAllPlots:
					if gc.getTerrainInfo(iIndex).isWater() and pPlot.isWater():
						pPlot.setTerrainType(lTerrain[iIndex], True, True)
					elif (not gc.getTerrainInfo(iIndex).isWater()) and (not pPlot.isWater()):
						pPlot.setTerrainType(lTerrain[iIndex], True, True)	
				elif pPlot.getArea() == self.m_iArea:
					if iIndex < len(lTerrain):
						pPlot.setTerrainType(lTerrain[iIndex], True, True)
		self.refreshSideMenu()
		return 1

	def handleWorldBuilderModifyAreaRoutePullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		for i in xrange (CyMap().getGridWidth()):
			for j in xrange (CyMap().getGridHeight()):
				pPlot = CyMap().plot(i,j)
				if (not pPlot.isNone()) and pPlot.getArea() == self.m_iArea:
					if iIndex < gc.getNumRouteInfos():
						if pPlot.isImpassable(): continue
						pPlot.setRouteType(iIndex)
					elif iIndex < gc.getNumRouteInfos() + 1:
						pPlot.setRouteType(-1)
		self.refreshSideMenu()
		return 1

	def handleWorldBuilderModifyAreaFeaturePullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		for i in xrange (CyMap().getGridWidth()):
			for j in xrange (CyMap().getGridHeight()):
				pPlot = CyMap().plot(i,j)
				if (not pPlot.isNone()) and pPlot.getArea() == self.m_iArea:
					if iIndex == 0:
						if pPlot.isImpassable(): continue
						if pPlot.canHaveFeature(gc.getInfoTypeForString("FEATURE_JUNGLE")):
							pPlot.setFeatureType(gc.getInfoTypeForString("FEATURE_JUNGLE"), 0)
					elif iIndex == 1:
						if pPlot.isImpassable(): continue
						if pPlot.canHaveFeature(gc.getInfoTypeForString("FEATURE_FOREST")):
							if pPlot.getLatitude() < 27:
								pPlot.setFeatureType(gc.getInfoTypeForString("FEATURE_FOREST"), 0)
							elif pPlot.getLatitude() < 54:
								pPlot.setFeatureType(gc.getInfoTypeForString("FEATURE_FOREST"), 1)
							else:
								pPlot.setFeatureType(gc.getInfoTypeForString("FEATURE_FOREST"), 2)
					elif iIndex == 2:
						pPlot.setFeatureType(-1, 0)
		self.refreshSideMenu()
		return 1
## City Data ##

	def handleCityEditPopulationCB (self, argsList) :
		self.m_pActivePlot.getPlotCity().setPopulation(int(argsList[0]))
		self.setCityEditInfo(True)
		return 1

	def handleCityEditCultureCB (self, argsList) :
		self.m_pActivePlot.getPlotCity().setCulture(self.m_iCurrentPlayer, int(argsList[0]), True)
		self.setCityEditInfo(True)
		return 1

	def handleCultureLevelCB ( self, argsList ) :
		self.m_pActivePlot.getPlotCity().setCulture(self.m_iCurrentPlayer, gc.getCultureLevelInfo(int(argsList[0])).getSpeedThreshold(CyGame().getGameSpeedType()), True)
		self.setCityEditInfo(True)
		return 1

	def handleCityEditHappinessCB (self, argsList) :
		self.m_pActivePlot.getPlotCity().changeExtraHappiness(int(argsList[0]) - self.m_pActivePlot.getPlotCity().happyLevel() + self.m_pActivePlot.getPlotCity().unhappyLevel(0))
		return 1

	def handleCityEditHealthCB (self, argsList) :
		self.m_pActivePlot.getPlotCity().changeExtraHealth(int(argsList[0]) - self.m_pActivePlot.getPlotCity().goodHealth() + self.m_pActivePlot.getPlotCity().badHealth(False))
		return 1

	def handleCityEditOccupationTimerCB (self, argsList) :
		self.m_pActivePlot.getPlotCity().setOccupationTimer(int(argsList[0]))
		self.setCityEditInfo(True)
		return 1

	def handleCityEditDefenseCB (self, argsList) :
		iNewDefenseDamage =100 - 100 * int(argsList[0])/self.m_pActivePlot.getPlotCity().getTotalDefense(False)
		self.m_pActivePlot.getPlotCity().changeDefenseDamage(iNewDefenseDamage - self.m_pActivePlot.getPlotCity().getDefenseDamage())
		return 1

	def handleCityEditTradeRouteCB (self, argsList) :
		self.m_pActivePlot.getPlotCity().changeExtraTradeRoutes(int(argsList[0]) - self.m_pActivePlot.getPlotCity().getTradeRoutes())
		return 1

	def handleBuildingCommandsCB (self, argsList) :
		iIndex = int(argsList[0])
		if iIndex == 1:
			for i in xrange(gc.getNumBuildingInfos()):
				if isNationalWonderClass(gc.getBuildingInfo(i).getBuildingClassType()) or isWorldWonderClass(gc.getBuildingInfo(i).getBuildingClassType()): continue
				if self.m_pActivePlot.getPlotCity().canConstruct(i, True, True, True):
					self.m_pActivePlot.getPlotCity().setNumRealBuilding(i, 1)
		elif iIndex == 2:
			for i in xrange(gc.getNumBuildingInfos()):
				if isNationalWonderClass(gc.getBuildingInfo(i).getBuildingClassType()) or isWorldWonderClass(gc.getBuildingInfo(i).getBuildingClassType()): continue
				self.m_pActivePlot.getPlotCity().setNumRealBuilding(i, 0)
		elif iIndex == 3:
			for i in xrange(gc.getNumBuildingInfos()):
				if isNationalWonderClass(gc.getBuildingInfo(i).getBuildingClassType()) or isWorldWonderClass(gc.getBuildingInfo(i).getBuildingClassType()): continue
				(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).firstCity(false)
				while(loopCity):
					if self.m_pActivePlot.getPlotCity().isHasBuilding(i):
						loopCity.setNumRealBuilding(i, 1)
					else:
						loopCity.setNumRealBuilding(i, 0)
					(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).nextCity(iter, false)
		self.setBuildingEditInfo()
		return 1

	def handleEditCityReligionCB (self, argsList) :
		iIndex, strName = argsList
		self.m_pActivePlot.getPlotCity().setHasReligion(int(strName), int(iIndex), False, False)
		if self.m_pActivePlot.getPlotCity().isHolyCityByType(int(strName)) and not iIndex:
			CyGame().clearHolyCity(int(strName))
		self.setReligionEditInfo()
		return 1

	def handleEditHolyCityCB (self, argsList) :
		iIndex, strName = argsList
		CyGame().clearHolyCity(int(strName))
		if iIndex:
			CyGame().setHolyCity(int(strName), self.m_pActivePlot.getPlotCity(), False)
		self.setReligionEditInfo()
		return 1

	def handleReligionCommandsCB (self, argsList) :
		iIndex = int(argsList[0])
		if iIndex == 1:
			for i in xrange(gc.getNumReligionInfos()):
				self.m_pActivePlot.getPlotCity().setHasReligion(i, True, False, False)
		elif iIndex == 2:
			for i in xrange(gc.getNumReligionInfos()):
				self.m_pActivePlot.getPlotCity().setHasReligion(i, False, False, False)
				if self.m_pActivePlot.getPlotCity().isHolyCityByType(i):
					CyGame().clearHolyCity(i)
		elif iIndex == 3:
			for i in xrange(gc.getNumReligionInfos()):
				(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).firstCity(false)
				while(loopCity):
					if self.m_pActivePlot.getPlotCity().isHasReligion(i):
						loopCity.setHasReligion(i, True, False, False)
					else:
						loopCity.setHasReligion(i, False, False, False)
						if loopCity.isHolyCityByType(i):
							CyGame().clearHolyCity(i)
					(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).nextCity(iter, false)
		self.setReligionEditInfo()
		return 1

	def handleEditCityCorporationCB (self, argsList) :
		iIndex, strName = argsList
		self.m_pActivePlot.getPlotCity().setHasCorporation(int(strName), int(iIndex), False, False)
		if self.m_pActivePlot.getPlotCity().isHeadquartersByType(int(strName)) and not iIndex:
			CyGame().clearHeadquarters(int(strName))
		self.setCorporationEditInfo()
		return 1

	def handleEditHeadquartersCB (self, argsList) :
		iIndex, strName = argsList
		CyGame().clearHeadquarters(int(strName))
		if iIndex:
			CyGame().setHeadquarters(int(strName), self.m_pActivePlot.getPlotCity(), False)
		self.setCorporationEditInfo()
		return 1

	def handleCorporationCommandsCB (self, argsList) :
		iIndex = int(argsList[0])
		if iIndex == 1:
			for i in xrange(gc.getNumReligionInfos()):
				self.m_pActivePlot.getPlotCity().setHasCorporation(i, False, False, False)
				if self.m_pActivePlot.getPlotCity().isHeadquartersByType(i):
					CyGame().clearHeadquarters(i)
		elif iIndex == 2:
			for i in xrange(gc.getNumCorporationInfos()):
				(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).firstCity(false)
				while(loopCity):
					if self.m_pActivePlot.getPlotCity().isHasCorporation(i):
						loopCity.setHasCorporation(i, True, False, False)
					else:
						loopCity.setHasCorporation(i, False, False, False)
						if loopCity.isHeadquartersByType(i):
							CyGame().clearHeadquarters(i)
					(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).nextCity(iter, false)
		self.setCorporationEditInfo()
		return 1

	def handleCityEditSpecialistCB (self, argsList) :
		iIndex, strName = argsList
		self.m_pActivePlot.getPlotCity().setFreeSpecialistCount(int(strName), int(iIndex))
		return 1

	def handleCityEditGreatPeopleCB (self, argsList) :
		iIndex, strName = argsList
		self.m_pActivePlot.getPlotCity().setGreatPeopleUnitProgress(int(strName), int(iIndex))

	def handleCityEditBonusCB (self, argsList) :
		iIndex, strName = argsList
		self.m_pActivePlot.getPlotCity().changeFreeBonus(int(strName), int(iIndex) - self.m_pActivePlot.getPlotCity().getFreeBonus(int(strName)))
		return 1

	def handleEditCityCycleCB (self, argsList) :
		bFound = False
		bFirst = False
		iCurrentCity = self.m_pActivePlot.getPlotCity().getID()
		(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).firstCity(false)
		while(loopCity):
			if bFirst == False:
				bFirst = True
				self.m_pActivePlot = loopCity.plot()
			if bFound == True:
				self.m_pActivePlot = loopCity.plot()
				self.setCityEditInfo(True)
				return 1
			if iCurrentCity == loopCity.getID():
				bFound = True
			(loopCity, iter) = gc.getPlayer(self.m_iCurrentPlayer).nextCity(iter, false)
		self.setCityEditInfo(True)
		return 1
		
## Unit Data ##

	def handleUnitEditStrengthCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setBaseCombatStr(int(argsList[0]))
		return 1

	def handleUnitEditDamageCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setDamage(int(argsList[0]), -1)
		return 1

	def handleUnitEditMovesCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setMoves(self.m_pActivePlot.getUnit(self.m_iCurrentUnit).maxMoves() - (int(argsList[0]) * gc.getDefineINT("MOVE_DENOMINATOR")))
		return 1

	def handleUnitEditCargoCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).changeCargoSpace(int(argsList[0]) - self.m_pActivePlot.getUnit(self.m_iCurrentUnit).cargoSpace())
		return 1

	def handleUnitEditImmobileTimerCB (self, argsList):
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setImmobileTimer(int(argsList[0]))
		return 1

	def handleUnitEditPromotionReadyCB (self, argsList) :
		iPromotionReady = int(argsList[0])
		if self.m_pActivePlot.getUnit(self.m_iCurrentUnit).experienceNeeded() > self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getExperience():
			iPromotionReady = 0
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setPromotionReady(iPromotionReady)
		self.setUnitEditInfo(True)
		return 1

	def handleUnitEditMadeAttackCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setMadeAttack(int(argsList[0]))
		return 1

	def handleUnitEditMadeInterceptionCB (self, argsList) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setMadeInterception(int(argsList[0]))
		return 1

	def handleMoveUnitCB (self, argsList) :
		self.m_bMoveUnit = True
		self.toggleUnitEditCB()
		return 1

	def handleEditUnitPromotionCB (self, argsList) :
		iIndex, strName = argsList
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setHasPromotion(int(strName), int(iIndex))
		return 1

	def handlePromotionCommandsCB (self, argsList) :
		iIndex = int(argsList[0])
		if iIndex == 1:
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				pUnit = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
				if pUnit.canAcquirePromotion(iPromotion):
					if gc.getInfoTypeForString("PROMOTION_LEADER") > -1 and iPromotion == gc.getInfoTypeForString("PROMOTION_LEADER"): continue
					pUnit.setHasPromotion(iPromotion, True)
		elif iIndex == 2:
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setHasPromotion(iPromotion, False)
		self.setPromotionEditInfo()
		return 1

	def handleUnitEditDuplicateCB (self, argsList) :
		pUnit = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
		for i in range (2):
			pNewUnit = gc.getPlayer(self.m_iCurrentPlayer).initUnit(pUnit.getUnitType(), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			pNewUnit.convert(pUnit)
			pNewUnit.setBaseCombatStr(pUnit.baseCombatStr())
			pNewUnit.changeCargoSpace(pUnit.cargoSpace() - pNewUnit.cargoSpace())
			pNewUnit.setImmobileTimer(pUnit.getImmobileTimer())
			pNewUnit.setScriptData(pUnit.getScriptData())
		pUnit.kill(False, -1)
		self.setUnitEditInfo(True)
		return 1

## Player Data ##

	def handleCurrentEraEditPullDownCB ( self, argsList ) :
		gc.getPlayer(self.m_iCurrentPlayer).setCurrentEra(int(argsList[0]))
		return 1

	def handleTeamEditCommerceFlexibleCB (self, argsList) :
		iIndex, strName = argsList
		if int(iIndex):
			gc.getTeam(self.m_iCurrentTeam).changeCommerceFlexibleCount(int(strName),  1)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeCommerceFlexibleCount(int(strName),  - gc.getTeam(self.m_iCurrentTeam).getCommerceFlexibleCount(int(strName)))
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditResearchPercentCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).setCommercePercent(CommerceTypes.COMMERCE_RESEARCH,  int(argsList[0]))
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditCulturePercentCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).setCommercePercent(CommerceTypes.COMMERCE_CULTURE,  int(argsList[0]))
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditEspionagePercentCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).setCommercePercent(CommerceTypes.COMMERCE_ESPIONAGE,  int(argsList[0]))
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditGoldenAgeCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).changeGoldenAgeTurns(int(argsList[0]) - gc.getPlayer(self.m_iCurrentPlayer).getGoldenAgeTurns())
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditGoldenAgeUnitsCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).changeNumUnitGoldenAges(int(argsList[0]) - gc.getPlayer(self.m_iCurrentPlayer).unitsRequiredForGoldenAge())
		return 1

	def handlePlayerEditAnarchyCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).changeAnarchyTurns(int(argsList[0]) - gc.getPlayer(self.m_iCurrentPlayer).getAnarchyTurns())
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditCombatExperienceCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).setCombatExperience(int(argsList[0]))
		self.setPlayerEditInfo()
		return 1

	def handleCivicEditPullDownCB ( self, argsList ) :
		iIndex, strName = argsList
		iCount = 0
		for i in xrange(gc.getNumCivicInfos()):
			if gc.getCivicInfo(i).getCivicOptionType() == int(strName):
				if int(iIndex) == iCount:
					if gc.getPlayer(self.m_iCurrentPlayer).canDoCivics(i):
						gc.getPlayer(self.m_iCurrentPlayer).setCivics(int(strName), i)
					self.setPlayerEditInfo()
					return 1
				iCount = iCount + 1

	def handleStateReligionEditPullDownCB ( self, argsList ) :
		gc.getPlayer(self.m_iCurrentPlayer).convert(int(argsList[0]) - 1)
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditStateReligionUnitProductionCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).changeStateReligionUnitProductionModifier(int(argsList[0]) - gc.getPlayer(self.m_iCurrentPlayer).getStateReligionUnitProductionModifier())
		return 1

	def handlePlayerEditStateReligionBuildingProductionCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).changeStateReligionBuildingProductionModifier(int(argsList[0]) - gc.getPlayer(self.m_iCurrentPlayer).getStateReligionBuildingProductionModifier())
		return 1

	def handleCurrentTechEditPullDownCB ( self, argsList ) :
		iCount = 0
		gc.getPlayer(self.m_iCurrentPlayer).clearResearchQueue()
		for i in xrange(gc.getNumTechInfos()):
			if gc.getPlayer(self.m_iCurrentPlayer).canResearch(i, False):
				iCount += 1
				if iCount == int(argsList[0]):
					gc.getPlayer(self.m_iCurrentPlayer).pushResearch(i, True)
					break
		self.setPlayerEditInfo()
		return 1

	def handleTeamEditResearchProgressCB (self, argsList) :
		gc.getTeam(self.m_iCurrentTeam).setResearchProgress(gc.getPlayer(self.m_iCurrentPlayer).getCurrentResearch(), int(argsList[0]), self.m_iCurrentPlayer)
		self.setPlayerEditInfo()
		return 1

	def handlePlayerEditGoldCB (self, argsList) :
		gc.getPlayer(self.m_iCurrentPlayer).setGold(int(argsList[0]))
		return 1
## Diplomacy Data ##

	def handleOtherPlayerEditPullDownCB ( self, argsList ) :
		lOtherPlayer = []
		for i in xrange(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive() and i != self.m_iCurrentPlayer:
				lOtherPlayer.append(i)
		self.m_iOtherPlayer = lOtherPlayer[int(argsList[0])]
		self.m_iOtherTeam = gc.getPlayer(self.m_iOtherPlayer).getTeam()
		self.setDiplomacyEditInfo()
		return 1

	def handleTeamEditMetStatusCB (self, argsList) :
		if int(argsList[0]):
			gc.getTeam(self.m_iCurrentTeam).meet(self.m_iOtherTeam, False)
		return 1

	def handleMeetAllCB (self, argsList) :
		for i in xrange(gc.getMAX_CIV_TEAMS()):
			if gc.getTeam(i).isAlive() and i != self.m_iCurrentTeam:
				gc.getTeam(self.m_iCurrentTeam).meet(i, False)
		self.setDiplomacyEditInfo()
		return 1

	def handleWarStatusAllCB (self, argsList) :
		if int(argsList[0]) == 1:
			for i in xrange(gc.getMAX_CIV_TEAMS()):
				if gc.getTeam(i).isAlive() and i != self.m_iCurrentTeam:
					if gc.getTeam(i).isVassal(self.m_iCurrentTeam) or gc.getTeam(self.m_iCurrentTeam).isVassal(i): continue
					if gc.getTeam(self.m_iCurrentTeam).isHasMet(i):
						gc.getTeam(self.m_iCurrentTeam).declareWar(i, True, -1)
		elif int(argsList[0]) == 2:
			for i in xrange(gc.getMAX_CIV_TEAMS()):
				if gc.getTeam(i).isAlive() and i != self.m_iCurrentTeam:
					gc.getTeam(self.m_iCurrentTeam).makePeace(i)
		self.setDiplomacyEditInfo()
		return 1

	def handleTeamEditWarStatusCB (self, argsList) :
		if int(argsList[0]):
			gc.getTeam(self.m_iCurrentTeam).declareWar(self.m_iOtherTeam, True, -1)
		else:
			gc.getTeam(self.m_iCurrentTeam).makePeace(self.m_iOtherTeam)
		self.setDiplomacyEditInfo()
		return 1

	def handleTeamEditRelationshipCB (self, argsList) :
		iIndex, strName = argsList
		iTeam1 = int(strName)
		if iTeam1 == self.m_iCurrentTeam:
			iTeam2 = self.m_iOtherTeam
		else:
			iTeam2 = self.m_iCurrentTeam
		if int(iIndex) == 0:
			gc.getTeam(iTeam1).freeVassal(iTeam2)
			gc.getTeam(iTeam2).freeVassal(iTeam1)
			gc.getTeam(iTeam2).assignVassal(iTeam1, False)
		elif int(iIndex) == 1:
			gc.getTeam(iTeam1).freeVassal(iTeam2)
			gc.getTeam(iTeam2).freeVassal(iTeam1)
			gc.getTeam(iTeam2).assignVassal(iTeam1, True)
		elif int(iIndex) == 2:
			gc.getTeam(iTeam2).freeVassal(iTeam1)
			gc.getTeam(iTeam1).freeVassal(iTeam2)
			gc.getTeam(iTeam1).assignVassal(iTeam2, True)
		else:
			gc.getTeam(iTeam2).freeVassal(iTeam1)
			gc.getTeam(iTeam1).freeVassal(iTeam2)
		self.setDiplomacyEditInfo()

	def handleMemoryEditPullDownCB ( self, argsList ) :
		self.m_iMemory = int(argsList[0])
		self.setDiplomacyEditInfo()
		return 1

	def handlePlayerEditMemoryCB (self, argsList) :
		iIndex, strName = argsList
		iPlayer1 = int(strName)
		if iPlayer1 == self.m_iCurrentPlayer:
			iPlayer2 = self.m_iOtherPlayer
		else:
			iPlayer2 = self.m_iCurrentPlayer
		gc.getPlayer(iPlayer1).AI_changeMemoryCount(iPlayer2, self.m_iMemory, (int(iIndex) - gc.getPlayer(iPlayer1).AI_getMemoryCount(iPlayer2, self.m_iMemory)))
		self.setDiplomacyEditInfo()
		return 1

	def handleAttitudeEditPullDownCB ( self, argsList ) :
		iIndex, strName = argsList
		iPlayer1 = int(strName)
		if iPlayer1 == self.m_iCurrentPlayer:
			iPlayer2 = self.m_iOtherPlayer
		else:
			iPlayer2 = self.m_iCurrentPlayer
		while int(iIndex) != gc.getPlayer(iPlayer1).AI_getAttitude(iPlayer2):
			if int(iIndex) < gc.getPlayer(iPlayer1).AI_getAttitude(iPlayer2):
				gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, -1)
			else:
				gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, 1)
		self.setDiplomacyEditInfo()
		return 1

	def handleTeamEditEspionagePointsCB (self, argsList) :
		iIndex, strName = argsList
		iTeam1 = int(strName)
		if iTeam1 == self.m_iCurrentTeam:
			iTeam2 = self.m_iOtherTeam
		else:
			iTeam2 = self.m_iCurrentTeam
		gc.getTeam(iTeam1).setEspionagePointsAgainstTeam(iTeam2, int(iIndex))
		return 1

	def handleTeamEditCounterEspionageCB (self, argsList) :
		iIndex, strName = argsList
		iTeam1 = int(strName)
		if iTeam1 == self.m_iCurrentTeam:
			iTeam2 = self.m_iOtherTeam
		else:
			iTeam2 = self.m_iCurrentTeam
		gc.getTeam(iTeam1).setCounterespionageTurnsLeftAgainstTeam(iTeam2, int(iIndex))
		return 1

	def handleTeamEditCounterEspionageModCB (self, argsList) :
		iIndex, strName = argsList
		iTeam1 = int(strName)
		if iTeam1 == self.m_iCurrentTeam:
			iTeam2 = self.m_iOtherTeam
		else:
			iTeam2 = self.m_iCurrentTeam
		gc.getTeam(iTeam1).setCounterespionageModAgainstTeam(iTeam2, int(iIndex))
		return 1

	def handleTeamEditWarWearinessCB (self, argsList) :
		iIndex, strName = argsList
		iTeam1 = int(strName)
		if iTeam1 == self.m_iCurrentTeam:
			iTeam2 = self.m_iOtherTeam
		else:
			iTeam2 = self.m_iCurrentTeam
		gc.getTeam(iTeam1).setWarWeariness(iTeam2, int(iIndex))
		return 1

	def handleTeamEditSignOpenBordersCB (self, argsList) :
		if int(argsList[0]):
			gc.getTeam(self.m_iOtherTeam).signOpenBorders(self.m_iCurrentTeam)
			self.setDiplomacyEditInfo()
			return 1
		else:
			for i in xrange(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeam1 = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeam2 = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if (iTeam1 == self.m_iOtherTeam and iTeam2 == self.m_iCurrentTeam) or (iTeam2 == self.m_iOtherTeam and iTeam1 == self.m_iCurrentTeam):
					for j in xrange(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_OPEN_BORDERS:	
							pDeal.kill()
							self.setDiplomacyEditInfo()
							return 1

	def handleOpenBordersAllCB (self, argsList) :
		if int(argsList[0]) == 1:
			for i in xrange(gc.getMAX_CIV_TEAMS()):
				if gc.getTeam(i).isAlive() and i != self.m_iCurrentTeam:
					if gc.getTeam(self.m_iCurrentTeam).isHasMet(i):
						gc.getTeam(self.m_iCurrentTeam).signOpenBorders(i)
		elif int(argsList[0]) == 2:
			for i in xrange(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeam1 = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeam2 = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if iTeam1 == self.m_iCurrentTeam or iTeam2 == self.m_iCurrentTeam:
					for j in xrange(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_OPEN_BORDERS:	
							pDeal.kill()
		self.setDiplomacyEditInfo()
		return 1

	def handleTeamEditSignDefensivePactCB (self, argsList) :
		if int(argsList[0]):
			gc.getTeam(self.m_iOtherTeam).signDefensivePact(self.m_iCurrentTeam)
			self.setDiplomacyEditInfo()
			return 1
		else:
			for i in xrange(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeam1 = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeam2 = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if (iTeam1 == self.m_iOtherTeam and iTeam2 == self.m_iCurrentTeam) or (iTeam2 == self.m_iOtherTeam and iTeam1 == self.m_iCurrentTeam):
					for j in xrange(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_DEFENSIVE_PACT:	
							pDeal.kill()
							self.setDiplomacyEditInfo()
							return 1

	def handleDefensivePactAllCB (self, argsList) :
		if int(argsList[0]) == 1:
			for i in xrange(gc.getMAX_CIV_TEAMS()):
				if gc.getTeam(i).isAlive() and i != self.m_iCurrentTeam:
					if gc.getTeam(self.m_iCurrentTeam).isHasMet(i):
						gc.getTeam(self.m_iCurrentTeam).signDefensivePact(i)
		elif int(argsList[0]) == 2:
			for i in xrange(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeam1 = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeam2 = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if iTeam1 == self.m_iCurrentTeam or iTeam2 == self.m_iCurrentTeam:
					for j in xrange(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_DEFENSIVE_PACT:	
							pDeal.kill()
		self.setDiplomacyEditInfo()

## Team Data ##

	def handleTeamEditPullDownCB ( self, argsList ) :
		lTeam = []
		for i in xrange(gc.getMAX_TEAMS()):
			if gc.getTeam(i).isEverAlive():
				lTeam.append(i)
		self.m_iCurrentTeam = lTeam[int(argsList[0])]
		self.m_iCurrentPlayer = gc.getTeam(self.m_iCurrentTeam).getLeaderID()
		self.setTeamEditInfo()
		self.refreshSideMenu()
		return 1

	def handleAddTeamCB ( self, argsList ) :
		iCount = 1
		for i in xrange(gc.getMAX_TEAMS()):
			if gc.getTeam(i).isEverAlive():
				if i == self.m_iCurrentTeam: continue
				if int(argsList[0]) == iCount:
					gc.getTeam(self.m_iCurrentTeam).addTeam(i)
					self.setTeamEditInfo()
					return 1
				iCount += 1

	def handleEditTeamProjectCB (self, argsList) :
		iIndex, strName = argsList
		gc.getTeam(self.m_iCurrentTeam).changeProjectCount(int(strName), int(iIndex) - gc.getTeam(self.m_iCurrentTeam).getProjectCount(int(strName)))
		if gc.getProjectInfo(int(strName)).isAllowsNukes():
			if CyGame().getProjectCreatedCount(int(strName)) == 0:
				CyGame().makeNukesValid(False)
		return 1

	def handleEditTeamTechnologyCB (self, argsList) :
		iIndex, strName = argsList
		gc.getTeam(self.m_iCurrentTeam).setHasTech(int(strName), int(iIndex), self.m_iCurrentPlayer, False, False)
		self.refreshPlayerTabCtrl()
		self.setTechnologyEditInfo()
		return 1

	def handleTeamEditNukeInterceptionCB (self, argsList) :
		gc.getTeam(self.m_iCurrentTeam).changeNukeInterception(int(argsList[0]) - gc.getTeam(self.m_iCurrentTeam).getNukeInterception())
		return 1

	def handleDomainEditPullDownCB ( self, argsList ) :
		self.m_iDomain = int(argsList[0])
		self.setTeamEditInfo()
		return 1

	def handleTeamEditDomainMovesCB (self, argsList) :
		gc.getTeam(self.m_iCurrentTeam).changeExtraMoves(self.m_iDomain, int(argsList[0]) - gc.getTeam(self.m_iCurrentTeam).getExtraMoves(self.m_iDomain))
		return 1

	def handleRouteEditPullDownCB ( self, argsList ) :
		self.m_iRoute = int(argsList[0])
		self.setTeamEditInfo()
		return 1

	def handleTeamEditRouteChangeCB (self, argsList) :
		gc.getTeam(self.m_iCurrentTeam).changeRouteChange(self.m_iRoute, int(argsList[0]) - gc.getTeam(self.m_iCurrentTeam).getRouteChange(self.m_iRoute))
		return 1

	def handleImprovementEditPullDownCB ( self, argsList ) :
		self.m_iImprovement = int(argsList[0])
		self.setTeamEditInfo()
		return 1

	def handleYieldEditPullDownCB ( self, argsList ) :
		self.m_iYield = int(argsList[0])
		self.setTeamEditInfo()
		return 1

	def handleTeamEditImprovementYieldCB (self, argsList) :
		iCount = 0
		for i in xrange(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isGraphicalOnly(): continue
			if iCount == self.m_iImprovement:
				gc.getTeam(self.m_iCurrentTeam).changeImprovementYieldChange(i, self.m_iYield, int(argsList[0]) - gc.getTeam(self.m_iCurrentTeam).getImprovementYieldChange(i, self.m_iYield))
				return 1
			iCount += 1
	
	def handleTeamEditMapCenteringCB (self, argsList) :
		gc.getTeam(self.m_iCurrentTeam).setMapCentering(int(argsList[0]))
		return 1

	def handleTeamEditGoldTradingCB (self, argsList) :
		iGoldTrading = int(argsList[0])
		if iGoldTrading == 1:
			gc.getTeam(self.m_iCurrentTeam).changeGoldTradingCount(iGoldTrading)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeGoldTradingCount( - gc.getTeam(self.m_iCurrentTeam).getGoldTradingCount())
		return 1

	def handleTeamEditTechTradingCB (self, argsList) :
		iTechTrading = int(argsList[0])
		if iTechTrading == 1:
			gc.getTeam(self.m_iCurrentTeam).changeTechTradingCount(iTechTrading)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeTechTradingCount( - gc.getTeam(self.m_iCurrentTeam).getTechTradingCount())
		return 1

	def handleTeamEditMapTradingCB (self, argsList) :
		iMapTrading = int(argsList[0])
		if iMapTrading == 1:
			gc.getTeam(self.m_iCurrentTeam).changeMapTradingCount(iMapTrading)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeMapTradingCount( - gc.getTeam(self.m_iCurrentTeam).getMapTradingCount())
		return 1

	def handleTeamEditOpenBordersTradingCB (self, argsList) :
		iOpenBordersTrading = int(argsList[0])
		if iOpenBordersTrading == 1:
			gc.getTeam(self.m_iCurrentTeam).changeOpenBordersTradingCount(iOpenBordersTrading)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeOpenBordersTradingCount( - gc.getTeam(self.m_iCurrentTeam).getOpenBordersTradingCount())
		return 1

	def handleTeamEditPermanentAllianceTradingCB (self, argsList) :
		iPermanentAllianceTrading = int(argsList[0])
		if iPermanentAllianceTrading == 1:
			gc.getTeam(self.m_iCurrentTeam).changePermanentAllianceTradingCount(iPermanentAllianceTrading)
		else:
			gc.getTeam(self.m_iCurrentTeam).changePermanentAllianceTradingCount( - gc.getTeam(self.m_iCurrentTeam).getPermanentAllianceTradingCount())
		return 1

	def handleTeamEditDefensivePactTradingCB (self, argsList) :
		iDefensivePactTrading = int(argsList[0])
		if iDefensivePactTrading == 1:
			gc.getTeam(self.m_iCurrentTeam).changeDefensivePactTradingCount(iDefensivePactTrading)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeDefensivePactTradingCount( - gc.getTeam(self.m_iCurrentTeam).getDefensivePactTradingCount())
		return 1

	def handleTeamEditVassalTradingCB (self, argsList) :
		iVassalTrading = int(argsList[0])
		if iVassalTrading == 1:
			gc.getTeam(self.m_iCurrentTeam).changeVassalTradingCount(iVassalTrading)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeVassalTradingCount( - gc.getTeam(self.m_iCurrentTeam).getVassalTradingCount())
		return 1

	def handleTeamEditWaterWorkCB (self, argsList) :
		iWaterWork = int(argsList[0])
		if iWaterWork == 1:
			gc.getTeam(self.m_iCurrentTeam).changeWaterWorkCount(iWaterWork)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeWaterWorkCount( - gc.getTeam(self.m_iCurrentTeam).getWaterWorkCount())
		return 1

	def handleTeamEditExtraWaterSeeFromCB (self, argsList) :
		iExtraWaterSeeFrom = int(argsList[0])
		if iExtraWaterSeeFrom == 1:
			gc.getTeam(self.m_iCurrentTeam).changeExtraWaterSeeFromCount(iExtraWaterSeeFrom)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeExtraWaterSeeFromCount( - gc.getTeam(self.m_iCurrentTeam).getExtraWaterSeeFromCount())
		return 1

	def handleTeamEditBridgeBuildingCB (self, argsList) :
		iBridgeBuilding = int(argsList[0])
		if iBridgeBuilding == 1:
			gc.getTeam(self.m_iCurrentTeam).changeBridgeBuildingCount(iBridgeBuilding)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeBridgeBuildingCount( - gc.getTeam(self.m_iCurrentTeam).getBridgeBuildingCount())
		return 1

	def handleTeamEditIrrigationCB (self, argsList) :
		iIrrigation = int(argsList[0])
		if iIrrigation == 1:
			gc.getTeam(self.m_iCurrentTeam).changeIrrigationCount(iIrrigation)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeIrrigationCount( - gc.getTeam(self.m_iCurrentTeam).getIrrigationCount())
		return 1

	def handleTeamEditIgnoreIrrigationCB (self, argsList) :
		iIgnoreIrrigation = int(argsList[0])
		if iIgnoreIrrigation == 1:
			gc.getTeam(self.m_iCurrentTeam).changeIgnoreIrrigationCount(iIgnoreIrrigation)
		else:
			gc.getTeam(self.m_iCurrentTeam).changeIgnoreIrrigationCount( - gc.getTeam(self.m_iCurrentTeam).getIgnoreIrrigationCount())
		return 1

## Game Options ##

	def handleGameOptionCB (self, argsList) :
		self.setGameOptionEditInfo()
		return 1

	def handleEditGameOptionCB ( self, argsList ) :
		iIndex, strName = argsList
		CyGame().setOption(int(strName), int(iIndex))
		if int(strName) == GameOptionTypes.GAMEOPTION_NO_GOODY_HUTS and iIndex:
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_GOODY_HUT"):
					pPlot.setImprovementType(-1)
		elif int(strName) == GameOptionTypes.GAMEOPTION_NO_VASSAL_STATES and iIndex:
			for iTeamX in xrange(gc.getMAX_CIV_TEAMS()):
				pTeamX = gc.getTeam(iTeamX)
				for iTeamY in xrange(gc.getMAX_CIV_TEAMS()):
					pTeamX.freeVassal(iTeamY)
		elif int(strName) == GameOptionTypes.GAMEOPTION_ALWAYS_PEACE and iIndex:
			for iTeamX in xrange(gc.getMAX_CIV_TEAMS()):
				pTeamX = gc.getTeam(iTeamX)
				if CyGame().isOption(GameOptionTypes.GAMEOPTION_ALWAYS_WAR) and pTeamX.isHuman(): continue
				for iTeamY in xrange(gc.getMAX_CIV_TEAMS()):
					if CyGame().isOption(GameOptionTypes.GAMEOPTION_ALWAYS_WAR) and gc.getTeam(iTeamY).isHuman(): continue
					pTeamX.makePeace(iTeamY)
		elif int(strName) == GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE and iIndex:
			for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isHuman():
					(loopCity, iter) = pPlayerX.firstCity(false)
					while(loopCity):
						if not loopCity.isCapital():
							loopCity.kill()
						(loopCity, iter) = pPlayerX.nextCity(iter, false)
		elif int(strName) == GameOptionTypes.GAMEOPTION_NO_BARBARIANS and iIndex:
			pPlayerBarb = gc.getPlayer(gc.getBARBARIAN_PLAYER ())
			(loopCity, iter) = pPlayerBarb.firstCity(false)
			while(loopCity):
				loopCity.kill()
				(loopCity, iter) = pPlayerBarb.nextCity(iter, false)
			(loopUnit, iter) = pPlayerBarb.firstUnit(false)
			while(loopUnit):
				loopUnit.kill(False, -1)
				(loopUnit, iter) = pPlayerBarb.nextUnit(iter, false)
		return 1

	def handleAddPlayerCivilizationCB ( self, argsList ) :
		iIndex = int(argsList[0])
		if int(iIndex) == 0:
			self.m_iNewCivilization = -1
			self.AddNewPlayer(False)
			return 1
		iCount = 1
		for i in xrange(gc.getNumCivilizationInfos()):
			if not CyGame().isCivEverActive(i):
				if iCount == iIndex:
					self.m_iNewCivilization = i
					self.m_iNewLeaderType = -1
					self.AddNewPlayer(False)
					return 1
				iCount+= 1
		

	def handleAddPlayerLeaderTypeCB ( self, argsList ) :
		iIndex = int(argsList[0])
		if int(iIndex) == 0:
			self.m_iNewLeaderType = -1
			self.AddNewPlayer(False)
			return 1
		iCount = 1
		for i in xrange(gc.getNumLeaderHeadInfos()):
			if not CyGame().isLeaderEverActive(i):
				if not CyGame().isOption(GameOptionTypes.GAMEOPTION_LEAD_ANY_CIV):
					if not gc.getCivilizationInfo(self.m_iNewCivilization).isLeaders(i): continue
				if iCount == iIndex:
					self.m_iNewLeaderType = i
					self.AddNewPlayer(False)
					return 1
				iCount+= 1

	def handleCreatePlayerCB ( self, argsList ) :
		for i in xrange(gc.getMAX_CIV_PLAYERS()):
			if not gc.getPlayer(i).isEverAlive():
				CyGame().addPlayer(i, self.m_iNewLeaderType, self.m_iNewCivilization)
				self.m_iCurrentPlayer = i
				self.m_iCurrentTeam = gc.getPlayer(i).getTeam()
				self.refreshSideMenu()
				self.normalPlayerTabModeCB()
				return 1

## Plot Data ##

	def handlePlotEditCultureCB (self, argsList) :
		self.m_pActivePlot.setCulture(self.m_iCurrentPlayer, int(argsList[0]), True)
		self.setPlotEditInfo(False)
		return 1

	def handlePlotEditYieldCB ( self, argsList ) :
		iIndex, strName = argsList
		if strName == "PlotEditFood":
			CyGame().setPlotExtraYield(self.m_pActivePlot.getX(), self.m_pActivePlot.getY(), YieldTypes.YIELD_FOOD, int(iIndex) - self.m_pActivePlot.getYield(YieldTypes.YIELD_FOOD))
		elif strName == "PlotEditProduction":
			CyGame().setPlotExtraYield(self.m_pActivePlot.getX(), self.m_pActivePlot.getY(), YieldTypes.YIELD_PRODUCTION, int(iIndex) - self.m_pActivePlot.getYield(YieldTypes.YIELD_PRODUCTION))
		else:
			CyGame().setPlotExtraYield(self.m_pActivePlot.getX(), self.m_pActivePlot.getY(), YieldTypes.YIELD_COMMERCE, int(iIndex) - self.m_pActivePlot.getYield(YieldTypes.YIELD_COMMERCE))
		return 1

	def handlePlotEditCityCB ( self, argsList ) :
		self.setCityEditInfo(True)
		return 1

	def handlePlotAddCityCB ( self, argsList ) :
		gc.getPlayer(self.m_iCurrentPlayer).initCity(self.m_pActivePlot.getX(), self.m_pActivePlot.getY())
		self.setPlotEditInfo(False)
		return 1

	def handlePlotEditPlotTypeCB ( self, argsList ) :
		iIndex = int(argsList[0])
		if iIndex == 0:
			self.m_pActivePlot.setPlotType(PlotTypes.PLOT_PEAK, True, True)
		elif iIndex == 1:
			self.m_pActivePlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
		elif iIndex == 1:
			self.m_pActivePlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
		else:
			self.m_pActivePlot.setPlotType(PlotTypes.PLOT_OCEAN, True, True)

	def handlePlotEditTerrainCB ( self, argsList ) :
		iIndex = int(argsList[0])
		iCount = 0
		for i in xrange(gc.getNumTerrainInfos()):
			if gc.getTerrainInfo(i).isGraphicalOnly(): continue
			if iCount == iIndex:
				self.m_pActivePlot.setTerrainType(i, True, True)
				self.setPlotEditInfo(False)
				return 1
			iCount += 1

	def handlePlotEditFeatureCB ( self, argsList ) :
		iIndex = int(argsList[0]) -1
		if iIndex == -1:
			self.m_pActivePlot.setFeatureType(-1, 0)
		elif gc.getFeatureInfo(iIndex).getNumVarieties() == 1:
			self.m_pActivePlot.setFeatureType(iIndex, 0)
		else:
			self.m_pActivePlot.setFeatureType(iIndex, self.m_tabCtrlEdit.getDropDownSelection(localText.getText("TXT_KEY_WB_PLOT_DATA",(self.m_pActivePlot.getX(), self.m_pActivePlot.getY())) , "PlotEditFeature"))
		self.setPlotEditInfo(False)
		return 1

	def handlePlotEditVarietyCB ( self, argsList ) :
		self.m_pActivePlot.setFeatureType(self.m_pActivePlot.getFeatureType(), int(argsList[0]))
		return 1

	def handlePlotEditBonusCB ( self, argsList ) :
		self.m_pActivePlot.setBonusType(int(argsList[0]) - 1)
		self.setPlotEditInfo(False)
		return 1

	def handlePlotEditImprovementCB ( self, argsList ) :
		iIndex = int(argsList[0])
		if iIndex == 0:
			self.m_pActivePlot.setImprovementType(-1)
			self.setPlotEditInfo(False)
			return 1
		iCount = 1
		for i in xrange(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isGraphicalOnly(): continue
			if iIndex == iCount:
				self.m_pActivePlot.setImprovementType(i)
				self.setPlotEditInfo(False)
				return 1
			iCount += 1

	def handlePlotEditUpgradeProgressCB ( self, argsList ) :
		iUpgradeTime = gc.getImprovementInfo(self.m_pActivePlot.getImprovementType()).getUpgradeTime()
		self.m_pActivePlot.setUpgradeProgress(iUpgradeTime - int(argsList[0]))
		return 1

	def handlePlotEditRouteCB ( self, argsList ) :
		self.m_pActivePlot.setRouteType(int(argsList[0]) - 1)
		self.setPlotEditInfo(False)
		return 1

## Platy World Builder End ##

	def handleCityEditNameCB (self, argsList) :
		if ((len(argsList[0]) < 1) or (not self.m_pActivePlot.isCity())):
			return 1
		szNewName = argsList[0]
		city = self.m_pActivePlot.getPlotCity()
		if (city):
			city.setName(szNewName, False)
		return 1

	def handleUnitEditPullDownCB ( self, argsList ) :
		self.m_iCurrentUnit = int(argsList[0])
		self.setUnitEditInfo(True)
		return 1

	def handleUnitAITypeEditPullDownCB ( self, argsList ) :
		self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setUnitAIType(int(argsList[0]))		
		return 1

## Platy World Builder Start ##
	def handlePlayerUnitPullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		iCount = 0
		for i in xrange( gc.getMAX_PLAYERS() ):
			if gc.getPlayer(i).isEverAlive():
				if iCount == iIndex:
					self.m_iCurrentPlayer = i
					self.m_iCurrentTeam = gc.getPlayer(i).getTeam()
					self.refreshSideMenu()
					self.refreshPlayerTabCtrl()
					return 1
				iCount += 1
## Platy World Builder End ##

## Platy Tech By Era Start ##
	def handleTechByEraPullDownCB ( self, argsList ) :
		iIndex = int(argsList[0])
		for i in xrange(gc.getNumTechInfos()):
			if gc.getTechInfo(i).getEra() == iIndex -1 or iIndex > gc.getNumEraInfos():
				gc.getTeam(self.m_iCurrentTeam).setHasTech(i, True, self.m_iCurrentPlayer, False, False)
		self.setTechnologyEditInfo()
		return 1

	def handleRemoveTechByEraPullDownCB ( self, argsList ) :
		iIndex = int(argsList[0])
		for i in xrange(gc.getNumTechInfos()):
			if gc.getTechInfo(i).getEra() == iIndex -1 or iIndex > gc.getNumEraInfos():
				gc.getTeam(self.m_iCurrentTeam).setHasTech(i, False, self.m_iCurrentPlayer, False, False)
		self.setTechnologyEditInfo()
		return 1
## Platy Tech By Era End ##

	def handleSelectTeamPullDownCB ( self, argsList ) :
		iIndex = int(argsList)
		iCount = -1
		for i in xrange( gc.getMAX_CIV_TEAMS() ):
			if gc.getTeam(i).isEverAlive():
				iCount = iCount + 1
				if (iCount == iIndex):
					self.m_iCurrentTeam = i
		self.refreshReveal()
		return 1

	def hasPromotion(self, iPromotion):
		return self.m_pActivePlot.getUnit(self.m_iCurrentUnit).isHasPromotion(iPromotion)

	def hasTech(self, iTech):
		return gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).isHasTech(iTech)

	def getNumBuilding(self, iBuilding):
		return self.m_pActivePlot.getPlotCity().getNumBuilding(iBuilding)

	def handleTechCB (self, argsList) :
		bOn, strName = argsList
		if ((strName.find("_") != -1) and (self.m_iCurrentPlayer >= 0)):
			iTech = int(strName[strName.find("_")+1:])
			gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).setHasTech(iTech, bOn, self.m_iCurrentPlayer, False, False)
			self.resetTechButtons()
		return 1
	
## Platy Edit Building ##
	def handleEditCityBuildingCB (self, argsList) :
		bOn, strName = argsList
		iNewBuilding = int(strName)
		if bOn:
			self.m_pActivePlot.getPlotCity().setNumRealBuilding(iNewBuilding, 1)
		else:
			self.m_pActivePlot.getPlotCity().setNumRealBuilding(iNewBuilding, 0)
		return 1
## Platy Edit Building ##

	def handleBrushWidthCB (self, argsList):
		if (int(argsList) == 0):
			self.m_iBrushWidth = int(1)
		elif (int(argsList) == 1):
			self.m_iBrushWidth = int(2)
		elif (int(argsList) == 2):
			self.m_iBrushWidth = int(3)
		return 1

	def handleBrushHeightCB (self, argsList):
		if (int(argsList) == 0):
			self.m_iBrushHeight = int(1)
		elif (int(argsList) == 1):
			self.m_iBrushHeight = int(2)
		elif (int(argsList) == 2):
			self.m_iBrushHeight = int(3)
		return 1

	def handleLandmarkCB (self, argsList):
		return 1
	
	########################################################
	### Advanced Start Stuff
	########################################################
	
	def refreshASItemCost(self):
		
		if (CyInterface().isInAdvancedStart()):
			
			self.m_iCost = 0
			
			if (self.m_pCurrentPlot != 0):
				
#				if (not self.m_pCurrentPlot.isAdjacentNonrevealed(CyGame().getActiveTeam()) and self.m_pCurrentPlot.isRevealed(CyGame().getActiveTeam(), false)):
				if (self.m_pCurrentPlot.isRevealed(CyGame().getActiveTeam(), false)):
					
					# Unit mode
					if (self.getASActiveUnit() != -1):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartUnitCost(self.getASActiveUnit(), true, self.m_pCurrentPlot)
					elif (self.getASActiveCity() != -1):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartCityCost(true, self.m_pCurrentPlot)
					elif (self.getASActivePop() != -1 and self.m_pCurrentPlot.isCity()):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartPopCost(true, self.m_pCurrentPlot.getPlotCity())
					elif (self.getASActiveCulture() != -1 and self.m_pCurrentPlot.isCity()):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartCultureCost(true, self.m_pCurrentPlot.getPlotCity())
					elif (self.getASActiveBuilding() != -1 and self.m_pCurrentPlot.isCity()):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartBuildingCost(self.getASActiveBuilding(), true, self.m_pCurrentPlot.getPlotCity())
					elif (self.getASActiveRoute() != -1):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartRouteCost(self.getASActiveRoute(), true, self.m_pCurrentPlot)
					elif (self.getASActiveImprovement() != -1):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartImprovementCost(self.getASActiveImprovement(), true, self.m_pCurrentPlot)
						
				elif (self.m_pCurrentPlot.isAdjacentNonrevealed(CyGame().getActiveTeam())):
					if (self.getASActiveVisibility() != -1):
						self.m_iCost = gc.getPlayer(self.m_iCurrentPlayer).getAdvancedStartVisibilityCost(true, self.m_pCurrentPlot)
				
			if (self.m_iCost < 0):
				self.m_iCost = 0

			self.refreshSideMenu()
	
	def getASActiveUnit(self):
		# Unit Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID):
			iUnitType = getASUnit(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
			return iUnitType
		
		return -1
		
	def getASActiveCity(self):
		# City Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID):
			# City List
			if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID):
				iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
				# Place City
				if (iOptionID == 0):
					return 1
		
		return -1
		
	def getASActivePop(self):
		# City Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID):
			# City List
			if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID):
				iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
				# Place Pop
				if (iOptionID == 1):
					return 1
		
		return -1
		
	def getASActiveCulture(self):
		# City Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID):
			# City List
			if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID):
				iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
				# Place Culture
				if (iOptionID == 2):
					return 1
		
		return -1
	
	def getASActiveBuilding(self):
		# Building Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID):
			# Buildings List
			if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASBuildingsListID):
				iBuildingType = getASBuilding(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
				return iBuildingType
		
		return -1
	
	def getASActiveRoute(self):
		# Improvements Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID):
			# Routes List
			if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASRoutesListID):
				iRouteType = getASRoute(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
				if -1 == iRouteType:
					self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] = self.m_iASImprovementsListID
				return iRouteType
		
		return -1
	
	def getASActiveImprovement(self):
		# Improvements Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID):
			# Improvements List
			if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASImprovementsListID):
				iImprovementType = getASImprovement(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
				if -1 == iImprovementType:
					self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] = self.m_iASRoutesListID
				return iImprovementType
		
		return -1
			
	def getASActiveVisibility(self):
		# Visibility Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID):
			return 1
		
		return -1
			
	def getASActiveTech(self):
		# Tech Tab
		if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASTechTabID):
			return 1
		
		return -1

	def placeObject( self ) :
		
		# Advanced Start
		if (CyInterface().isInAdvancedStart()):
			
			pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
			pPlot = CyMap().plot(self.m_iCurrentX, self.m_iCurrentY)
			
			iActiveTeam = CyGame().getActiveTeam()
			if (self.m_pCurrentPlot.isRevealed(iActiveTeam, false)):
							
				# City Tab
				if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID):
					
					# City List
					if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID):
						
						iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
						
						# Place City
						if (iOptionID == 0):
							
							# Cost -1 means may not be placed here
							if (pPlayer.getAdvancedStartCityCost(true, pPlot) != -1):
								
								CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CITY, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, true)	#Action, Player, X, Y, Data, bAdd
						
						# City Population
						elif (iOptionID == 1):
							
							if (pPlot.isCity()):
								pCity = pPlot.getPlotCity()
								
								# Cost -1 means may not be placed here
								if (pPlayer.getAdvancedStartPopCost(true, pCity) != -1):
										
										CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, true)	#Action, Player, X, Y, Data, bAdd
						
						# City Culture
						elif (iOptionID == 2):
							
							if (pPlot.isCity()):
								pCity = pPlot.getPlotCity()
								
								# Cost -1 means may not be placed here
								if (pPlayer.getAdvancedStartCultureCost(true, pCity) != -1):
									
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CULTURE, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, true)	#Action, Player, X, Y, Data, bAdd
										
					# Buildings List
					elif (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASBuildingsListID):
							
							if (pPlot.isCity()):
								pCity = pPlot.getPlotCity()
								
								iBuildingType = getASBuilding(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
								
								# Cost -1 means may not be placed here
								if (iBuildingType != -1 and pPlayer.getAdvancedStartBuildingCost(iBuildingType, true, pCity) != -1):
									
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, iBuildingType, true)	#Action, Player, X, Y, Data, bAdd
				
				# Unit Tab
				elif (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID):
					iUnitType = getASUnit(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
					
					# Cost -1 means may not be placed here
					if (iUnitType != -1 and pPlayer.getAdvancedStartUnitCost(iUnitType, true, pPlot) != -1):
						
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, iUnitType, true)	#Action, Player, X, Y, Data, bAdd
							
				# Improvements Tab
				elif (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID):
					
					# Routes List
					if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASRoutesListID):
						
						iRouteType = getASRoute(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						
						# Cost -1 means may not be placed here
						if (iRouteType != -1 and pPlayer.getAdvancedStartRouteCost(iRouteType, true, pPlot) != -1):
							
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, iRouteType, true)	#Action, Player, X, Y, Data, bAdd
					
					# Improvements List
					elif (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASImprovementsListID):
						
						iImprovementType = getASImprovement(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						
						# Cost -1 means may not be placed here
						if (pPlayer.getAdvancedStartImprovementCost(iImprovementType, true, pPlot) != -1):
							
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, iImprovementType, true)	#Action, Player, X, Y, Data, bAdd
							
			# Adjacent nonrevealed
			else:
				
				# Visibility Tab
				if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID):
					
					# Cost -1 means may not be placed here
					if (pPlayer.getAdvancedStartVisibilityCost(true, pPlot) != -1):
						
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_VISIBILITY, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, true)	#Action, Player, X, Y, Data, bAdd
			
			self.m_bSideMenuDirty = true
			self.m_bASItemCostDirty = true
				
			return 1
		
		if ((self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()] == -1) or (self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] == -1) or (self.m_iCurrentX == -1) or (self.m_iCurrentY == -1) or (self.m_iCurrentPlayer == -1)):
			return 1

		if (self.m_bEraseAll):
			self.eraseAll()
		elif ((self.m_bNormalPlayer) and (self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iUnitTabID)):
			iUnitType = self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()]
			pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
			iPlotX = self.m_iCurrentX
			iPlotY = self.m_iCurrentY
			pPlayer.initUnit(iUnitType, iPlotX, iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
		elif ((self.m_bNormalPlayer) and (self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iBuildingTabID)):
			iBuildingType = self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()]
			if ((self.m_pCurrentPlot.isCity()) and (iBuildingType != 0)):
				self.m_pCurrentPlot.getPlotCity().setNumRealBuilding(iBuildingType-1, 1)
			if (iBuildingType == 0):
				if (not self.m_pCurrentPlot.isCity()):
					pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
					iX = self.m_pCurrentPlot.getX()
					iY = self.m_pCurrentPlot.getY()
					pPlayer.initCity(iX, iY)
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iImprovementTabID)):
			iImprovementType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
			iIndex = -1
			iCounter = -1
			while ((iIndex < iImprovementType) and (iCounter < gc.getNumImprovementInfos())):
				iCounter = iCounter + 1
				if (not gc.getImprovementInfo(iCounter).isGraphicalOnly()):
					iIndex = iIndex + 1
			if (iIndex > -1):
				self.m_pCurrentPlot.setImprovementType(iCounter)
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iBonusTabID)):
			iBonusType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
			self.m_pCurrentPlot.setBonusType(iBonusType)
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID)):
			if (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iTerrainListID):
				iTerrainType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
				self.m_pCurrentPlot.setTerrainType(iTerrainType, True, True)
			elif (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iFeatureListID):
				iButtonIndex = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
				iCount = -1
				for i in range (gc.getNumFeatureInfos()):
					for j in range (gc.getFeatureInfo(i).getNumVarieties()):
						iCount = iCount + 1
						if (iCount == iButtonIndex):
							self.m_pCurrentPlot.setFeatureType(i, j)
			elif (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iPlotTypeListID):
				iPlotType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
				if (iPlotType >= 0) and (iPlotType < PlotTypes.NUM_PLOT_TYPES):
					self.m_pCurrentPlot.setPlotType(PlotTypes(iPlotType), True, True)
			elif (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iRouteListID):
				iRouteType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
				if (iRouteType == gc.getNumRouteInfos()):
					if (self.m_pRiverStartPlot == self.m_pCurrentPlot):
						self.m_pRiverStartPlot = -1
						CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
						return 1
					if (self.m_pRiverStartPlot != -1):
						iXDiff = 0
						iYDiff = 0
						if (self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX()):
							iXDiff = self.m_pCurrentPlot.getX() - self.m_pRiverStartPlot.getX()
						elif (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX()):
							iXDiff = self.m_pRiverStartPlot.getX() - self.m_pCurrentPlot.getX()
						if (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY()):
							iYDiff = self.m_pCurrentPlot.getY() - self.m_pRiverStartPlot.getY()
						elif (self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY()):
							iYDiff = self.m_pRiverStartPlot.getY() - self.m_pCurrentPlot.getY()

						if ((iXDiff == iYDiff) and (iXDiff == 1) and (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX()) and (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY())):
							self.placeRiverNW(True)
							self.m_pRiverStartPlot = CyMap().plot(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY()+1)
						elif ((iXDiff == 0) and (iYDiff == 1) and (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY())):
							self.placeRiverN(True)
							self.m_pRiverStartPlot = self.m_pCurrentPlot
						elif ((iXDiff == iYDiff) and (iXDiff == 1) and (self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX()) and (self.m_pRiverStartPlot.getY() < self.m_pCurrentPlot.getY())):
							self.placeRiverNE(True)
							self.m_pRiverStartPlot = self.m_pCurrentPlot
						elif ((iXDiff == 1) and (iYDiff == 0) and (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX())):
							self.placeRiverW(True)
							self.m_pRiverStartPlot = self.m_pCurrentPlot
						elif ((iXDiff == 1) and (iYDiff == 0) and (self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX())):
							self.placeRiverE(True)
							self.m_pRiverStartPlot = self.m_pCurrentPlot
						elif ((iXDiff == iYDiff) and (iXDiff == 1) and (self.m_pRiverStartPlot.getX() > self.m_pCurrentPlot.getX()) and (self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY())):
							self.placeRiverSW(True)
							self.m_pRiverStartPlot = self.m_pCurrentPlot
						elif ((iXDiff == 0) and (iYDiff == 1) and (self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY())):
							self.placeRiverS(True)
							self.m_pRiverStartPlot = self.m_pCurrentPlot
						elif ((iXDiff == iYDiff) and (iXDiff == 1) and (self.m_pRiverStartPlot.getX() < self.m_pCurrentPlot.getX()) and (self.m_pRiverStartPlot.getY() > self.m_pCurrentPlot.getY())):
							self.placeRiverSE(True)
							self.m_pRiverStartPlot = self.m_pCurrentPlot
						else:
							self.m_pRiverStartPlot = self.m_pCurrentPlot
					else:
						self.m_pRiverStartPlot = self.m_pCurrentPlot
				else:
					self.m_pCurrentPlot.setRouteType(iRouteType)
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerritoryTabID)):
			iPlayer = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
			if (gc.getPlayer(iPlayer).isEverAlive()):
				self.m_pCurrentPlot.setOwner(iPlayer)
		elif (self.m_bLandmark):
			CvEventInterface.beginEvent(CvUtil.EventWBLandmarkPopup)
		return 1

	def removeObject( self ):
		
		# Advanced Start
		if (CyInterface().isInAdvancedStart()):
			
			pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
			pPlot = CyMap().plot(self.m_iCurrentX, self.m_iCurrentY)
			
			iActiveTeam = CyGame().getActiveTeam()
#			if (not self.m_pCurrentPlot.isAdjacentNonrevealed(iActiveTeam) and self.m_pCurrentPlot.isRevealed(iActiveTeam, false)):
			if (self.m_pCurrentPlot.isRevealed(iActiveTeam, false)):
							
				# City Tab
				if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASCityTabID):
					
					# City List
					if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASCityListID):
						
						iOptionID = self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()]
						
						# Place City
						if (iOptionID == 0):
							
							# Ability to remove cities not allowed because of 'sploitz (visibility, chopping down jungle, etc.)
							return 1
							
							if (self.m_pCurrentPlot.isCity()):
								
								if (self.m_pCurrentPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer):
									
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CITY, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, false)	#Action, Player, X, Y, Data, bAdd
						
						# City Population
						elif (iOptionID == 1):
							
							if (pPlot.isCity()):
								if (pPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer):
									
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, false)	#Action, Player, X, Y, Data, bAdd
						
						# City Culture
						elif (iOptionID == 2):
							
							# Ability to remove cities not allowed because of 'sploitz (visibility)
							return 1
							
							if (pPlot.isCity()):
								if (pPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer):
									
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CULTURE, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, false)	#Action, Player, X, Y, Data, bAdd
					
					# Buildings List
					elif (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASBuildingsListID):
						
						if (pPlot.isCity()):
							if (pPlot.getPlotCity().getOwner() == self.m_iCurrentPlayer):
								
								iBuildingType = getASBuilding(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
								
								if -1 != iBuildingType:
									CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, iBuildingType, false)	#Action, Player, X, Y, Data, bAdd
				
				# Unit Tab
				elif (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASUnitTabID):
					
					iUnitType = getASUnit(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
					
					if -1 != iUnitType:
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT, self.m_iCurrentPlayer, self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY(), iUnitType, false)	#Action, Player, X, Y, Data, bAdd
							
				# Improvements Tab
				elif (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASImprovementsTabID):
					
					# Routes List
					if (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASRoutesListID):
						
						iRouteType = getASRoute(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						
						if -1 != iRouteType:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, iRouteType, false)	#Action, Player, X, Y, Data, bAdd
					
					# Improvements List
					elif (self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] == self.m_iASImprovementsListID):
						
						iImprovementType = getASImprovement(self.m_iAdvancedStartCurrentIndexes[self.m_advancedStartTabCtrl.getActiveTab()])
						
						if -1 != iImprovementType:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, iImprovementType, false)	#Action, Player, X, Y, Data, bAdd
						
			# Adjacent nonrevealed
			else:
				
				# Visibility Tab
				if (self.m_advancedStartTabCtrl.getActiveTab() == self.m_iASVisibilityTabID):
					
					# Ability to remove sight not allowed because of 'sploitz
					return 1
					
					# Remove Visibility
					if (pPlot.isRevealed(iActiveTeam, false)):
						
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_VISIBILITY, self.m_iCurrentPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, false)	#Action, Player, X, Y, Data, bAdd
			
			self.m_bSideMenuDirty = true
			self.m_bASItemCostDirty = true
			
			return 1
			
		if ((self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()] == -1) or (self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()] == -1) or (self.m_iCurrentX == -1) or (self.m_iCurrentY == -1) or (self.m_iCurrentPlayer == -1)):
			return 1

		if (self.m_bEraseAll):
			self.eraseAll()
		elif ((self.m_bNormalPlayer) and (self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iUnitTabID)):
			for i in range (self.m_pCurrentPlot.getNumUnits()):
				pUnit = self.m_pCurrentPlot.getUnit(i)
				if (pUnit.getUnitType() == self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()]):
					pUnit.kill(false, PlayerTypes.NO_PLAYER)
					return 1
			if (self.m_pCurrentPlot.getNumUnits() > 0):
				pUnit = self.m_pCurrentPlot.getUnit(0)
				pUnit.kill(false, PlayerTypes.NO_PLAYER)
				return 1
		elif ((self.m_bNormalPlayer) and (self.m_normalPlayerTabCtrl.getActiveTab() == self.m_iBuildingTabID)):
			if (self.m_pCurrentPlot.isCity()):
				iBuildingType = self.m_iNormalPlayerCurrentIndexes[self.m_normalPlayerTabCtrl.getActiveTab()]
				if (iBuildingType == 0) :
					self.m_pCurrentPlot.getPlotCity().kill()
				else:
					self.m_pCurrentPlot.getPlotCity().setNumRealBuilding(iBuildingType-1, 0)
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iImprovementTabID)):
			self.m_pCurrentPlot.setImprovementType(-1)
			return 1
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iBonusTabID)):
			iBonusType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
			self.m_pCurrentPlot.setBonusType(-1)
			return 1
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID)):
			if (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iTerrainListID):
				return 1
			elif (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iFeatureListID):
				iFeatureType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
				self.m_pCurrentPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
				return 1
			elif (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iPlotTypeListID):
				return 1
			elif (self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iRouteListID):
				iRouteType = self.m_iNormalMapCurrentIndexes[self.m_normalMapTabCtrl.getActiveTab()]
				if (iRouteType == gc.getNumRouteInfos()):
					if (self.m_pRiverStartPlot != -1):
						self.m_pRiverStartPlot = -1
						CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
					else:
						self.m_pCurrentPlot.setNOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
						self.m_pCurrentPlot.setWOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
				else:
					self.m_pCurrentPlot.setRouteType(-1)
		elif ((self.m_bNormalMap) and (self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerritoryTabID)):
			self.m_pCurrentPlot.setOwner(-1)
			return 1
		elif (self.m_bLandmark):
			self.removeLandmarkCB()
		return 1

	def handleClicked( self ):
		return

	def isIntString ( self, arg ):
		for i in range (len(arg)):
			if (arg[i] > '9') :
				return False
			elif (arg[i] < '0') :
				return False
		return True
		
	def placeRiverNW ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)
			
		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY())
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY()+1)
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		return

	def placeRiverN ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)

		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()+1)
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		return

	def placeRiverNE ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY())
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY()+1)
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		return

	def placeRiverW ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY())
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)
		return

	def placeRiverE ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY())
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
		return

	def placeRiverSW ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_WEST)

		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY()-1)
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
		return

	def placeRiverS ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)

		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()-1)
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
		return

	def placeRiverSE ( self, bUseCurrent ):
		if (bUseCurrent):
			pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY())
			if (not pRiverStepPlot.isNone()):
				pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)

		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY())
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setNOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_EAST)
		pRiverStepPlot = CyMap().plot(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY()-1)
		if (not pRiverStepPlot.isNone()):
			pRiverStepPlot.setWOfRiver(True, CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
		return

	def setUnitEditInfo(self, bSamePlot):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		self.m_bUnitEditCtrl = True
		self.m_bCityEditCtrl = False

		if not bSamePlot:
			self.m_pActivePlot = self.m_pCurrentPlot

		self.m_tabCtrlEdit.setNumColumns((gc.getNumPromotionInfos()/10)+1)
		self.m_tabCtrlEdit.setColumnLength(16)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_UNIT_DATA",(self.m_pActivePlot.getX(), self.m_pActivePlot.getY())))
		strTest = ()
		for i in range(self.m_pActivePlot.getNumUnits()):
			if (len(self.m_pActivePlot.getUnit(i).getNameNoDesc())):
				strTest = strTest + (self.m_pActivePlot.getUnit(i).getNameNoDesc(),)
			else:
				strTest = strTest + (self.m_pActivePlot.getUnit(i).getName(),)

		self.m_tabCtrlEdit.addSectionDropdown("Current_Unit", strTest, "CvScreensInterface", "WorldBuilderHandleUnitEditPullDownCB", "UnitEditPullDown", 0, self.m_iCurrentUnit)

## Platy Builder ##
		self.m_iCurrentPlayer = self.m_pActivePlot.getUnit(self.m_iCurrentUnit).getOwner()
		self.m_iCurrentTeam = gc.getPlayer(self.m_iCurrentPlayer).getTeam()
		pUnit = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
## Platy Builder ##

		if (len(pUnit.getNameNoDesc())):
			strName = pUnit.getNameNoDesc()
		else:
			strName = pUnit.getName()
		self.m_tabCtrlEdit.addSectionEditCtrl(strName, "CvScreensInterface", "WorldBuilderHandleUnitEditNameCB", "UnitEditName", 0)
## Experience ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_EXPERIENCE",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditExperienceCB", "CvScreensInterface", "WorldBuilderHandleUnitEditExperienceCB", "UnitEditExperience", 0, 0, 10000, 1, pUnit.getExperience(), 0, 0)
## Level ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_LEVEL",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditLevelCB", "CvScreensInterface", "WorldBuilderHandleUnitEditLevelCB", "UnitEditLevel", 0, 1, 100, 1, pUnit.getLevel(), 0, 0)
## Base Strength ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_STRENGTH",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditStrengthCB", "CvScreensInterface", "WorldBuilderHandleUnitEditStrengthCB", "UnitEditStrength", 0, 0, 1000, 1, pUnit.baseCombatStr(), 0, 0)
## Damage % ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_DAMAGE",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditDamageCB", 	"CvScreensInterface", "WorldBuilderHandleUnitEditDamageCB", "UnitEditDamage", 0, 0, 100, 1, pUnit.getDamage(), 0, 0)
## Cargo ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CARGO",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditCargoCB", "CvScreensInterface", "WorldBuilderHandleUnitEditCargoCB", 	"UnitEditCargo", 0, 0, min(100, pUnit.cargoSpace() * 100), 1, pUnit.cargoSpace(), 0, 0)
## Moves ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_MOVES",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditMovesCB", "CvScreensInterface", "WorldBuilderHandleUnitEditMovesCB", "UnitEditMoves", 0, 0, pUnit.baseMoves(), 1, pUnit.movesLeft() / gc.getDefineINT("MOVE_DENOMINATOR"), 0, 0)
## Immobile Timer ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_IMMOBILE_TIMER",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditImmobileTimerCB", "CvScreensInterface", "WorldBuilderHandleUnitEditImmobileTimerCB", "UnitEditImmobileTimer", 0, 0, 100, 1, pUnit.getImmobileTimer(), 0, 0)

#東方叙事詩・統合MOD追記
#powerをWB上で調整
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_POWER",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditPowerCB", "CvScreensInterface", "WorldBuilderHandleUnitEditPowerCB", "UnitEditPower", 0, 0, 4, 1, pUnit.getPower(), 0, 0)

#CAレベルをWB上で調整
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CAL",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("UnitEditCALCB", "CvScreensInterface", "WorldBuilderHandleUnitEditCALCB", "UnitEditCAL", 0, 0, 254, 1, pUnit.countCardAttackLevel(), 0, 0)

#東方叙事詩・統合MOD追記ここまで
## Owner ##
		strTest = ()
		iCount = 0
		for i in xrange(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive():
				strTest = strTest + (gc.getPlayer(i).getName(),)
				if i == self.m_iCurrentPlayer:
					iUnitOwner = iCount
				iCount = iCount + 1
		self.m_tabCtrlEdit.addSectionDropdown("Unit Owner", strTest, "CvScreensInterface", "WorldBuilderHandleCurrentPlayerEditPullDownCB", "UnitEditOwner", 0, iUnitOwner)
## Promotion Ready ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_PROMOTION_READY",()), "CvScreensInterface", "WorldBuilderHandleUnitEditPromotionReadyCB", "UnitEditPromotionReady", 0, pUnit.isPromotionReady())
## Made Attack ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_MADE_ATTACK",()), "CvScreensInterface", "WorldBuilderHandleUnitEditMadeAttackCB", "UnitEditMadeAttack", 0, pUnit.isMadeAttack())
## Made Interception ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_MADE_INTERCEPT",()), "CvScreensInterface", "WorldBuilderHandleUnitEditMadeInterceptionCB", "UnitEditMadeInterception", 0, pUnit.isMadeInterception())
## Unit AI Type ##
		strTest = ()
		for i in xrange(UnitAITypes.NUM_UNITAI_TYPES):
			strTest = strTest + (gc.getUnitAIInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Unit_AI_Type", strTest, "CvScreensInterface", "WorldBuilderHandleUnitAITypeEditPullDownCB", "UnitAITypeEditPullDown", 0, pUnit.getUnitAIType())
## Promotions ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_PROMOTIONS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "PromotionEditScreen", 0)
## Move Unit ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_MOVE_UNIT",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleMoveUnitCB", "MoveUnit", 0)
## Duplicate ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_DUPLICATE",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleUnitEditDuplicateCB", "UnitEditDuplicate", 0)
## Unit Script ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_ADD_SCRIPT",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEditScriptCB", "UnitEditScript", 0)
##
		initWBToolEditCtrlTab(True)
			
		if (not self.m_tabCtrlEdit.isNone()):
			print("Enabling map control 4")
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return

## Promotion Edit Screen ##
	def setPromotionEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 4
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_PROMOTIONS",()))

		lPromotions = []
		for i in xrange(gc.getNumPromotionInfos()):
			lPromotions.append(gc.getPromotionInfo(i).getDescription() + "_Platy_" + str(i))
		lPromotions.sort()

		iColumnLength = (len(lPromotions) +2) /iNumColumns
		if (len(lPromotions) +2) %iNumColumns > 0:
			iColumnLength += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(min(1000, iNumColumns * 200), min(700, max(5, iColumnLength) * 42))

		for i in lPromotions:
			sPromotion = i[:i.find("_Platy_")]
			iPromotion = int(i[i.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionCheckbox(sPromotion, "CvScreensInterface", "WorldBuilderHandleEditUnitPromotionCB", str(iPromotion), 0, self.m_pActivePlot.getUnit(self.m_iCurrentUnit).isHasPromotion(iPromotion))
		for i in range(iNumColumns * iColumnLength - (len(lPromotions) +2)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)

		strTest = (localText.getText("TXT_KEY_WB_COMMANDS",()),) + (localText.getText("TXT_KEY_WB_ALL_PROMOTIONS",()),) + (localText.getText("TXT_KEY_WB_CLEAR_ALL",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Promotion Commands", strTest, "CvScreensInterface", "WorldBuilderHandlePromotionCommandsCB", "Promotion Commands", 0, 0)

		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToUnit", 0)
		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Promotion Edit Screen ##

	def setCityEditInfo(self, bSamePlot):
		self.m_bUnitEditCtrl = False
		self.m_bCityEditCtrl = True

		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()
## Platy City Data ##
		if not bSamePlot:
			self.m_pActivePlot = self.m_pCurrentPlot
		pCity = self.m_pActivePlot.getPlotCity()
		self.m_iCurrentPlayer = pCity.getOwner()
		self.m_iCurrentTeam = gc.getPlayer(self.m_iCurrentPlayer).getTeam()
		self.m_tabCtrlEdit.setNumColumns((gc.getNumBuildingInfos()/10)+2)
		self.m_tabCtrlEdit.setColumnLength(17)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_CITY_DATA",(self.m_pActivePlot.getX(), self.m_pActivePlot.getY())))
## City Name ##
		self.m_tabCtrlEdit.addSectionEditCtrl(pCity.getName(), "CvScreensInterface", "WorldBuilderHandleCityEditNameCB", "CityEditName", 0)
## Owner ##
		strTest = ()
		iCount = 0
		for i in range(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive():
				strTest = strTest + (gc.getPlayer(i).getName(),)
				if i == self.m_iCurrentPlayer:
					iOwner = iCount
				iCount = iCount + 1
		self.m_tabCtrlEdit.addSectionDropdown("Owner", strTest, "CvScreensInterface", "WorldBuilderHandleCurrentPlayerEditPullDownCB", "CityEditOwner", 0, iOwner)
## Population ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_POPULATION",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("CityEditPopulationCB", "CvScreensInterface", "WorldBuilderHandleCityEditPopulationCB", "CityEditPopulation", 0, 1, 1000, 1, pCity.getPopulation(), 0, 0)
## Culture ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CULTURE",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("CityEditCultureCB", "CvScreensInterface", "WorldBuilderHandleCityEditCultureCB", "CityEditCulture", 0, 1, 100000000, 1, pCity.getCulture(self.m_iCurrentPlayer), 0, 0)
		strTest = ()
		for i in xrange(gc.getNumCultureLevelInfos()):
			strTest = strTest + (gc.getCultureLevelInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Culture Level", strTest, "CvScreensInterface", "WorldBuilderHandleCultureLevelCB", "CityEditCultureLevel", 0, pCity.getCultureLevel())
## Happiness ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_HAPPINESS",()),  0)
		strHappiness = str("CityEditHappinessCB")
		self.m_tabCtrlEdit.addSectionSpinner(strHappiness, "CvScreensInterface", "WorldBuilderHandleCityEditHappinessCB", "CityEditHappiness", 0, -1000, 1000, 1, pCity.happyLevel() - pCity.unhappyLevel(0), 0, 0)
## Health ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_HEALTH",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("CityEditHealthCB", "CvScreensInterface", "WorldBuilderHandleCityEditHealthCB", "CityEditHealth", 0, -1000, 1000, 1, pCity.goodHealth() - pCity.badHealth(False), 0, 0)
## Occupation Timer##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_OCCUPATIONTIMER",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("CityEditOccupationTimerCB", "CvScreensInterface", "WorldBuilderHandleCityEditOccupationTimerCB", "CityEditOccupationTimer", 0, 0, 1000, 1, pCity.getOccupationTimer(), 0, 0)
## Defense ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_DEFENSE",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("CityEditDefenseCB", "CvScreensInterface", "WorldBuilderHandleCityEditDefenseCB", "CityEditDefense", 0, 0, pCity.getTotalDefense(False), 1, pCity.getTotalDefense(False) * (100 - pCity.getDefenseDamage())/100, 0, 0)
## Trade Routes ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_TRADE_ROUTE",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("CityEditTradeRouteCB", "CvScreensInterface", "WorldBuilderHandleCityEditTradeRouteCB", "CityEditTradeRoute", 0, 0, gc.getDefineINT("MAX_TRADE_ROUTES"), 1, pCity.getTradeRoutes(), 0, 0)
## New Screens ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BUILDINGS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BuildingEditScreen", 0)
		self.m_tabCtrlEdit.addSectionButton( localText.getText("TXT_KEY_WB_WONDERS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "WonderEditScreen", 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_RELIGION",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "ReligionEditScreen", 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_CORPORATION",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "CorporationEditScreen", 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_FREE_SPECIALISTS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "FreeSpecialistEditScreen", 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_GREAT_PEOPLE",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "GreatPeopleEditScreen", 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_FREE_BONUS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "FreeBonusEditScreen", 0)
## City Script ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_ADD_SCRIPT",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEditScriptCB", "CityEditScript", 0)
## City Cycle ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_NEXT_CITY",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEditCityCycleCB", "EditCityCycle", 0)
		return

## Building Edit Screen ##
	def setBuildingEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 5
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_BUILDINGS",()))

		lBuildings = []
		for i in xrange(gc.getNumBuildingInfos()):
			BuildingInfo = gc.getBuildingInfo(i)
			if isNationalWonderClass(BuildingInfo.getBuildingClassType()) or isTeamWonderClass(BuildingInfo.getBuildingClassType()) or isWorldWonderClass(BuildingInfo.getBuildingClassType()): continue
			lBuildings.append(BuildingInfo.getDescription() + "_Platy_" + str(i))
		lBuildings.sort()

		iColumnLength = (len(lBuildings) +2) /iNumColumns
		if (len(lBuildings) +2) %iNumColumns > 0:
			iColumnLength += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(1000, 700)

		for i in lBuildings:
			sBuilding = i[:i.find("_Platy_")]
			iBuilding = int(i[i.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionCheckbox(sBuilding, "CvScreensInterface", "WorldBuilderHandleEditCityBuildingCB", str(iBuilding), 0, self.m_pActivePlot.getPlotCity().isHasBuilding(iBuilding))
		for i in range(iNumColumns * iColumnLength - (len(lBuildings) +2)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)

		strTest = (localText.getText("TXT_KEY_WB_COMMANDS",()),) + (localText.getText("TXT_KEY_WB_BUILD_ALL",()),) + (localText.getText("TXT_KEY_WB_CLEAR_ALL",()),) + (localText.getText("TXT_KEY_WB_COPY_ALL",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Building Commands", strTest, "CvScreensInterface", "WorldBuilderHandleBuildingCommandsCB", "Building Commands", 0, 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToCity", 0)
		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Building Edit Screen ##

## Wonder Edit Screen ##
	def setWonderEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 4
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_WONDERS",()))

		lNationalWonders = []
		lTeamWonders = []
		lWorldWonders = []
		for i in xrange(gc.getNumBuildingInfos()):
			BuildingInfo = gc.getBuildingInfo(i)
			if isNationalWonderClass(BuildingInfo.getBuildingClassType()):
				lNationalWonders.append(BuildingInfo.getDescription() + "_Platy_" + str(i))
			elif isTeamWonderClass(BuildingInfo.getBuildingClassType()):
				lNationalWonders.append(BuildingInfo.getDescription() + "_Platy_" + str(i))
			elif isWorldWonderClass(BuildingInfo.getBuildingClassType()):
				lWorldWonders.append(BuildingInfo.getDescription() + "_Platy_" + str(i))
		lNationalWonders.sort()
		lTeamWonders.sort()
		lWorldWonders.sort()
		iWonderType = 1
		if len(lNationalWonders) > 0:
			iWonderType += 1
		if len(lTeamWonders) > 0:
			iWonderType += 1
		if len(lWorldWonders) > 0:
			iWonderType += 1

		iColumnLength = (len(lNationalWonders) + len(lTeamWonders) + len(lWorldWonders) +iWonderType) /iNumColumns
		if (len(lNationalWonders) + len(lTeamWonders) + len(lWorldWonders) +iWonderType) %iNumColumns > 0:
			iColumnLength += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(1000, 700)
		if len(lNationalWonders) > 0:
			self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_NATIONAL_WONDERS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleNationalWonderCB", "NationalWonder", 0)
			for i in lNationalWonders:
				sWonder = i[:i.find("_Platy_")]
				iWonder = int(i[i.find("_Platy_") +7:])
				self.m_tabCtrlEdit.addSectionCheckbox(sWonder, "CvScreensInterface", "WorldBuilderHandleEditCityBuildingCB", str(iWonder), 0, self.m_pActivePlot.getPlotCity().isHasBuilding(iWonder))
		if len(lTeamWonders) > 0:
			self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_TEAM_WONDERS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleTeamWonderCB", "TeamWonder", 0)
			for i in lTeamWonders:
				sWonder = i[:i.find("_Platy_")]
				iWonder = int(i[i.find("_Platy_") +7:])
				self.m_tabCtrlEdit.addSectionCheckbox(sWonder, "CvScreensInterface", "WorldBuilderHandleEditCityBuildingCB", str(iWonder), 0, self.m_pActivePlot.getPlotCity().isHasBuilding(iWonder))
		if len(lWorldWonders) > 0:
			self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_WORLD_WONDERS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleWorldWonderCB", "WorldWonder", 0)			
			for i in lWorldWonders:
				sWonder = i[:i.find("_Platy_")]
				iWonder = int(i[i.find("_Platy_") +7:])
				self.m_tabCtrlEdit.addSectionCheckbox(sWonder, "CvScreensInterface", "WorldBuilderHandleEditCityBuildingCB", str(iWonder), 0, self.m_pActivePlot.getPlotCity().isHasBuilding(iWonder))
		for i in range(iNumColumns * iColumnLength - (len(lNationalWonders) + len(lTeamWonders) + len(lWorldWonders) + iWonderType)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToCity", 0)
		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Wonder Edit Screen ##

## Religion Edit Screen ##
	def setReligionEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 4
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		iReligionPerColumn = (gc.getNumReligionInfos() +1) /iNumColumns
		if (gc.getNumReligionInfos() +1) % iNumColumns > 0:
			iReligionPerColumn += 1
		iColumnLength = iReligionPerColumn *4 -1
		iReligionColumn = (gc.getNumReligionInfos() +1) / iReligionPerColumn
		if (gc.getNumReligionInfos() +1) % iReligionPerColumn > 0:
			iReligionColumn += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(min(1000, iReligionColumn * 200), min(600, max(5, iColumnLength) * 42))

		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_RELIGION",()))
		lReligion = []
		for i in xrange(gc.getNumReligionInfos()):
			lReligion.append(gc.getReligionInfo(i).getDescription() + "_Platy_" + str(i))
		lReligion.sort()

		for i in xrange(len(lReligion)):
			sI = lReligion[i]
			sReligion = sI[:sI.find("_Platy_")]
			iReligion = int(sI[sI.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionLabel(sReligion, 0)
			self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_PRESENT",()), "CvScreensInterface", "WorldBuilderHandleEditCityReligionCB", str(iReligion), 0, self.m_pActivePlot.getPlotCity().isHasReligion(iReligion))
			self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_HOLY_CITY",()), "CvScreensInterface", "WorldBuilderHandleEditHolyCityCB", str(iReligion), 0, self.m_pActivePlot.getPlotCity().isHolyCityByType(iReligion))
			if (i+1) % iReligionPerColumn != 0:
				self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		
		for i in range(iReligionColumn * iColumnLength - (gc.getNumReligionInfos()*4 - iReligionColumn + 3)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		strTest = (localText.getText("TXT_KEY_WB_COMMANDS",()),) + (localText.getText("TXT_KEY_WB_SPREAD_ALL",()),) + (localText.getText("TXT_KEY_WB_CLEAR_ALL",()),) + (localText.getText("TXT_KEY_WB_COPY_ALL",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Religion Commands", strTest, "CvScreensInterface", "WorldBuilderHandleReligionCommandsCB", "Religion Commands", 0, 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToCity", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Religion Edit Screen ##

## Corporation Edit Screen ##
	def setCorporationEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 4

		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		iCorporationPerColumn = (gc.getNumCorporationInfos() +1) /iNumColumns
		if (gc.getNumCorporationInfos() +1) % iNumColumns > 0:
			iCorporationPerColumn += 1
		iColumnLength = iCorporationPerColumn *4 -1
		iCorporationColumn = (gc.getNumCorporationInfos() +1) / iCorporationPerColumn
		if (gc.getNumCorporationInfos() +1) % iCorporationPerColumn > 0:
			iCorporationColumn += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(min(1000, iCorporationColumn * 200), min(600, max(5, iColumnLength) * 42))

		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_CORPORATION",()))
		lCorporation = []
		for i in xrange(gc.getNumCorporationInfos()):
			lCorporation.append(gc.getCorporationInfo(i).getDescription() + "_Platy_" + str(i))
		lCorporation.sort()
		for i in xrange(len(lCorporation)):
			sI = lCorporation[i]
			sCorporation = sI[:sI.find("_Platy_")]
			iCorporation = int(sI[sI.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionLabel(sCorporation, 0)
			self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_PRESENT",()), "CvScreensInterface", "WorldBuilderHandleEditCityCorporationCB", str(iCorporation), 0, self.m_pActivePlot.getPlotCity().isHasCorporation(iCorporation))
			self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_HEADQUARTERS",()), "CvScreensInterface", "WorldBuilderHandleEditHeadquartersCB", str(iCorporation), 0, self.m_pActivePlot.getPlotCity().isHeadquartersByType(iCorporation))
			if (i+1) % iCorporationPerColumn != 0:
				self.m_tabCtrlEdit.addSectionLabel(" ",  0)

		for i in range(iCorporationColumn * iColumnLength - (gc.getNumCorporationInfos()*4 - iCorporationColumn + 3)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		strTest = (localText.getText("TXT_KEY_WB_COMMANDS",()),) + (localText.getText("TXT_KEY_WB_CLEAR_ALL",()),) + (localText.getText("TXT_KEY_WB_COPY_ALL",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Corporation Commands", strTest, "CvScreensInterface", "WorldBuilderHandleCorporationCommandsCB", "Corporation Commands", 0, 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToCity", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Corporation Edit Screen ##

## Free Specialists Edit Screen ##
	def setFreeSpecialistEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 4
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)

		iColumnLength = (gc.getNumSpecialistInfos() *2 +1) /iNumColumns
		if (gc.getNumSpecialistInfos() *2 +1) %iNumColumns > 0:
			iColumnLength += 1
		if iColumnLength %2 == 1:
			iColumnLength += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(min(1000, iNumColumns * 200), min(600, max(5, iColumnLength) * 42))

		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_FREE_SPECIALISTS",()))
		lSpecialist = []
		lGreatSpecialist = []
		for i in xrange(gc.getNumSpecialistInfos()):
			sSpecialist = gc.getSpecialistInfo(i).getType()
			if sSpecialist.find("GREAT") > -1:
				lGreatSpecialist.append(gc.getSpecialistInfo(i).getDescription() + "_Platy_" + str(i))
			else:
				lSpecialist.append(gc.getSpecialistInfo(i).getDescription() + "_Platy_" + str(i))
		lSpecialist.sort()
		lGreatSpecialist.sort()

		for i in lSpecialist:
			sSpecialist = i[:i.find("_Platy_")]
			iSpecialist = int(i[i.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionLabel(sSpecialist,  0)
			self.m_tabCtrlEdit.addSectionSpinner(sSpecialist, "CvScreensInterface", "WorldBuilderHandleCityEditSpecialistCB", str(iSpecialist), 0, 0, 100, 1, self.m_pActivePlot.getPlotCity().getFreeSpecialistCount(iSpecialist), 0, 0)
		for i in lGreatSpecialist:
			sSpecialist = i[:i.find("_Platy_")]
			iSpecialist = int(i[i.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionLabel(sSpecialist,  0)
			self.m_tabCtrlEdit.addSectionSpinner(sSpecialist, "CvScreensInterface", "WorldBuilderHandleCityEditSpecialistCB", str(iSpecialist), 0, 0, 100, 1, self.m_pActivePlot.getPlotCity().getFreeSpecialistCount(iSpecialist), 0, 0)

		for i in range(iNumColumns * iColumnLength - (gc.getNumSpecialistInfos() *2 +1)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToCity", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Free Specialists Edit Screen ##

## Great People Edit Screen ##
	def setGreatPeopleEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 4
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)

		lGreatPeople = []
		for i in xrange(gc.getNumUnitInfos()):
			if gc.getUnitInfo(i).isGoldenAge():
				lGreatPeople.append(gc.getUnitInfo(i).getDescription() + "_Platy_" + str(i))
		lGreatPeople.sort()

		iColumnLength = (len(lGreatPeople) *2 +1) /iNumColumns
		if (len(lGreatPeople) *2 +1) %iNumColumns > 0:
			iColumnLength += 1
		if iColumnLength %2 == 1:
			iColumnLength += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(min(1000, iNumColumns * 200), min(600, max(5, iColumnLength) * 40))
		
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_GREAT_PEOPLE",()))
		for i in lGreatPeople:
			sGreatPeople = i[:i.find("_Platy_")]
			iGreatPeople = int(i[i.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionLabel(sGreatPeople,  0)
			self.m_tabCtrlEdit.addSectionSpinner(sGreatPeople, "CvScreensInterface", "WorldBuilderHandleCityEditGreatPeopleCB", str(iGreatPeople), 0, 0, 99999, 1, self.m_pActivePlot.getPlotCity().getGreatPeopleUnitProgress(iGreatPeople), 0, 0)
		for i in range(iColumnLength * iNumColumns - (len(lGreatPeople) *2 +1)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToCity", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Great People Edit Screen ##

## Free Bonus Edit Screen ##
	def setFreeBonusEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 5
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)

		iColumnLength = (gc.getNumBonusInfos() *2 +1) /iNumColumns
		if (gc.getNumBonusInfos() *2 +1) %iNumColumns > 0:
			iColumnLength += 1
		if iColumnLength %2 == 1:
			iColumnLength += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(min(1000, iNumColumns * 200), min(600, max(5, iColumnLength) * 35))
		
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_FREE_BONUS",()))
		lBonus = []
		for i in xrange(gc.getNumBonusInfos()):
			lBonus.append(gc.getBonusInfo(i).getDescription() + "_Platy_" + str(i))
		lBonus.sort()

		for i in lBonus:
			sBonus = i[:i.find("_Platy_")]
			iBonus = int(i[i.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionLabel(sBonus,  0)
			self.m_tabCtrlEdit.addSectionSpinner(sBonus, "CvScreensInterface", "WorldBuilderHandleCityEditBonusCB", str(iBonus), 0, 0, 100, 1, self.m_pActivePlot.getPlotCity().getFreeBonus(iBonus), 0, 0)
		for i in range(iNumColumns * iColumnLength - (gc.getNumBonusInfos() *2 +1)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToCity", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Free Bonus Edit Screen ##

## Player Edit Screen ##
	def setPlayerEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()
		iNumColumns = 4
		iExtraSpace = max(0, gc.getNumCivicOptionInfos() - 7)
		iColumnLength = 10 + iExtraSpace
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(750, min(400, iColumnLength * 40))
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_PLAYER_DATA",()))
## Current Player ##
		strTest = ()
		iCount = 0
		for i in xrange(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive():
				strPlayerAliveStatus = gc.getPlayer(i).getName()
				if not gc.getPlayer(i).isAlive():
					strPlayerAliveStatus = strPlayerAliveStatus + " " + localText.getText("TXT_KEY_WB_DEAD",())
				strTest = strTest + (strPlayerAliveStatus,)
				if i == self.m_iCurrentPlayer:
					iCurrentPlayer = iCount
				iCount += 1
		self.m_tabCtrlEdit.addSectionDropdown("Current Player", strTest, "CvScreensInterface", "WorldBuilderHandleCurrentPlayerEditPullDownCB", "PlayerEditCurrentPlayer", 0, iCurrentPlayer)
		pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
## Current Era ##
		strTest = ()
		for i in xrange(gc.getNumEraInfos()):
			strTest = strTest + (localText.getText("TXT_KEY_WB_ERA",(gc.getEraInfo(i).getDescription(),)),)
		self.m_tabCtrlEdit.addSectionDropdown("Current Era", strTest, "CvScreensInterface", "WorldBuilderHandleCurrentEraEditPullDownCB", "PlayerEditCurrentEra", 0, pPlayer.getCurrentEra())
## Team ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_TEAM",(self.m_iCurrentTeam,)),  0)
## Traits ##
		lTraits = []
		for i in xrange(gc.getNumTraitInfos()):
			if pPlayer.hasTrait(i):
				lTraits.append(i)
		sTrait = ""
		for i in xrange(len(lTraits)):
			sTrait += gc.getTraitInfo(lTraits[i]).getDescription()
			if i != len(lTraits) -1:
				sTrait += ", "
		if len(lTraits) == 0:
			sTrait = localText.getText("TXT_KEY_WB_NONE",())
		self.m_tabCtrlEdit.addSectionLabel(sTrait,  0)
## Commerce Sliders ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_RESEARCH",()), "CvScreensInterface", "WorldBuilderHandleTeamEditCommerceFlexibleCB", str(1), 0, pPlayer.isCommerceFlexible(CommerceTypes.COMMERCE_RESEARCH))
		if gc.getPlayer(self.m_iCurrentPlayer).isCommerceFlexible(CommerceTypes.COMMERCE_RESEARCH):
			self.m_tabCtrlEdit.addSectionSpinner("PlayerEditResearchCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditResearchPercentCB", "Research", 0, 0, 100, 10, pPlayer.getCommercePercent(CommerceTypes.COMMERCE_RESEARCH), 0, 0)
		else:
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_CULTURE",()), "CvScreensInterface", "WorldBuilderHandleTeamEditCommerceFlexibleCB", str(2), 0, pPlayer.isCommerceFlexible(CommerceTypes.COMMERCE_CULTURE))
		if gc.getPlayer(self.m_iCurrentPlayer).isCommerceFlexible(CommerceTypes.COMMERCE_CULTURE):
			self.m_tabCtrlEdit.addSectionSpinner("PlayerEditCultureCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditCulturePercentCB", "Culture", 0, 0, 100, 10, pPlayer.getCommercePercent(CommerceTypes.COMMERCE_CULTURE), 0, 0)
		else:
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_ESPIONAGE",()), "CvScreensInterface", "WorldBuilderHandleTeamEditCommerceFlexibleCB", str(3), 0, pPlayer.isCommerceFlexible(CommerceTypes.COMMERCE_ESPIONAGE))
		if gc.getPlayer(self.m_iCurrentPlayer).isCommerceFlexible(CommerceTypes.COMMERCE_ESPIONAGE):
			self.m_tabCtrlEdit.addSectionSpinner("PlayerEditEspionageCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditEspionagePercentCB", "Espionage", 0, 0, 	100, 10, pPlayer.getCommercePercent(CommerceTypes.COMMERCE_ESPIONAGE), 0, 0)
		else:
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
##
		for i in range (iExtraSpace):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
## Golden Age ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_GOLDEN_AGE",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlayerEditGoldenAgeCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditGoldenAgeCB", "PlayerEditGoldenAge", 0, 0, 1000, 1, pPlayer.getGoldenAgeTurns(), 0, 0)
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_GOLDEN_AGE_UNITS",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlayerEditGoldenAgeUnitsCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditGoldenAgeUnitsCB", "PlayerEditGoldenAgeUnits", 0, 1, 10, 1, pPlayer.unitsRequiredForGoldenAge(), 0, 0)
## Anarchy ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_ANARCHY",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlayerEditAnarchyCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditAnarchyCB", "PlayerEditAnarchy", 0, 0, 1000, 1, pPlayer.getAnarchyTurns(), 0, 0)
## Combat Experience ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_COMBAT_EXPERIENCE",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlayerEditCombatExperienceCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditCombatExperienceCB", "PlayerEditCombatExperience", 0, 0, 1000, 1, pPlayer.getCombatExperience(), 0, 0)
## Gold ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_GOLD",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlayerEditGoldCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditGoldCB", "PlayerEditGold", 0, -10000, 1000000, 1, pPlayer.getGold(), 0, 0)
##
		for i in range (iExtraSpace):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
## State Religion ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_STATE_RELIGION",()),  0)
		strTest = (localText.getText("TXT_KEY_WB_NONE",()),)
		for i in xrange(gc.getNumReligionInfos()):
			strTest = strTest + (gc.getReligionInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("State Religion", strTest, "CvScreensInterface", "WorldBuilderHandleStateReligionEditPullDownCB", "StateReligionEditPullDown", 0, pPlayer.getStateReligion() + 1)
## State Religion Unit Production ##
		if gc.getPlayer(self.m_iCurrentPlayer).getStateReligion() == -1:
			for i in range (4):
				self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		else:
			self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_STATE_RELIGION_UNIT",()),  0)
			self.m_tabCtrlEdit.addSectionSpinner("PlayerEditStateReligionUnitProductionCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditStateReligionUnitProductionCB", "PlayerEditStateReligionUnitProduction", 0, 0, 1000, 1, pPlayer.getStateReligionUnitProductionModifier(), 0, 0)
## State Religion Building Production ##
			self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_STATE_RELIGION_BUILDING",()),  0)
			self.m_tabCtrlEdit.addSectionSpinner("PlayerEditStateReligionBuildingProductionCB", "CvScreensInterface", "WorldBuilderHandlePlayerEditStateReligionBuildingProductionCB", "PlayerEditStateReligionBuildingProduction", 0, 0, 1000, 1, pPlayer.getStateReligionBuildingProductionModifier(), 0, 0)
## Current Research ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_WB_CURRENT_RESEARCH",()),  0)
		strTest = (localText.getText("TXT_KEY_WB_NONE",()),)
		lCurrentTech = [-1]
		iCurrentTech = 0
		iCount = 0
		for i in xrange(gc.getNumTechInfos()):
			if pPlayer.canResearch(i, False):
				iCount += 1
				lCurrentTech.append(i)
				strTest = strTest + (gc.getTechInfo(i).getDescription(),)
				if pPlayer.getCurrentResearch() == i:
					iCurrentTech = iCount
		self.m_tabCtrlEdit.addSectionDropdown("Current Tech", strTest, "CvScreensInterface", "WorldBuilderHandleCurrentTechEditPullDownCB", "CurrentTechEditPullDown", 0, iCurrentTech)
## Research Progress ##
		if pPlayer.getCurrentResearch() == -1:
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		else:
			self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_RESEARCH_PROGRESS",(gc.getTeam(self.m_iCurrentTeam).getResearchCost(pPlayer.getCurrentResearch()),)),  0)
			self.m_tabCtrlEdit.addSectionSpinner("TeamEditResearchProgressCB", "CvScreensInterface", "WorldBuilderHandleTeamEditResearchProgressCB", "TeamEditResearchProgress", 0, 0, gc.getTeam(self.m_iCurrentTeam).getResearchCost(pPlayer.getCurrentResearch()), 1, gc.getTeam(self.m_iCurrentTeam).getResearchProgress(pPlayer.getCurrentResearch()), 0, 0)
##
		for i in range (iExtraSpace):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
## Civics ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CIVICS",()),  0)
		for iCivicOption in xrange(gc.getNumCivicOptionInfos()):
			strTest = ()
			iCount = 0
			for i in xrange(gc.getNumCivicInfos()):
				if gc.getCivicInfo(i).getCivicOptionType() == iCivicOption:
					strTest = strTest + (gc.getCivicInfo(i).getDescription(),)
					if pPlayer.isCivic(i):
						iCivic = iCount
					iCount = iCount + 1
			self.m_tabCtrlEdit.addSectionDropdown(str(iCivicOption), strTest, "CvScreensInterface", "WorldBuilderHandleCivicEditPullDownCB", str(iCivicOption), 0, iCivic)
##
		for i in range (iColumnLength - 2 - gc.getNumCivicOptionInfos()):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
## Player Script ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_ADD_SCRIPT",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEditScriptCB", "PlayerEditScript", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Player Edit Screen ##

## Team Edit Screen ##
	def setTeamEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()
		self.m_tabCtrlEdit.setNumColumns(2)
		self.m_tabCtrlEdit.setColumnLength(15)		
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_TEAM_DATA",()))
## Team ##
		strTest = ()
		iCount = 0
		for i in xrange(gc.getMAX_TEAMS()):
			if gc.getTeam(i).isEverAlive():
				strName = gc.getTeam(i).getName()
				if not gc.getTeam(i).isAlive():
					strName = gc.getPlayer(gc.getTeam(i).getLeaderID()).getName() + " " + localText.getText("TXT_KEY_WB_DEAD",())
				strTest = strTest + (strName,)
				if i == self.m_iCurrentTeam:
					iTeam = iCount
				iCount = iCount + 1
		self.m_tabCtrlEdit.addSectionDropdown("Team", strTest, "CvScreensInterface", "WorldBuilderHandleTeamEditPullDownCB", "TeamEditPullDown", 0, iTeam)
		pTeam = gc.getTeam(self.m_iCurrentTeam)
## Info ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_LEADER",(gc.getPlayer(pTeam.getLeaderID()).getName(),)),  0)
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_MAP_CENTERING",()), "CvScreensInterface", "WorldBuilderHandleTeamEditMapCenteringCB", "TeamEditMapCentering", 0, pTeam.isMapCentering())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_GOLD_TRADING",()), "CvScreensInterface", "WorldBuilderHandleTeamEditGoldTradingCB", "TeamEditGoldTrading", 0, pTeam.isGoldTrading())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_TECH_TRADING",()), "CvScreensInterface", "WorldBuilderHandleTeamEditTechTradingCB", "TeamEditTechTrading", 0, pTeam.isTechTrading())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_MAP_TRADING",()), "CvScreensInterface", "WorldBuilderHandleTeamEditMapTradingCB", "TeamEditMapTrading", 0, pTeam.isMapTrading())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_WATER_WORK",()), "CvScreensInterface", "WorldBuilderHandleTeamEditWaterWorkCB", "TeamEditWaterWork", 0, pTeam.isWaterWork())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_EXTRA_WATER_SIGHT",()), "CvScreensInterface", "WorldBuilderHandleTeamEditExtraWaterSeeFromCB", "TeamEditExtraWaterSeeFrom", 0, pTeam.isExtraWaterSeeFrom())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_BRIDGE_BUILDING",()), "CvScreensInterface", "WorldBuilderHandleTeamEditBridgeBuildingCB", "TeamEditBridgeBuilding", 0, pTeam.isBridgeBuilding())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_IRRIGATION",()), "CvScreensInterface", "WorldBuilderHandleTeamEditIrrigationCB", "TeamEditIrrigation", 0, pTeam.isIrrigation())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_IGNORE_IRRIGATION",()), "CvScreensInterface", "WorldBuilderHandleTeamEditIgnoreIrrigationCB", "TeamEditIgnoreIrrigation", 0, pTeam.isIgnoreIrrigation())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_OPEN_BORDERS",()), "CvScreensInterface", "WorldBuilderHandleTeamEditOpenBordersTradingCB", "TeamEditOpenBordersTrading", 0, pTeam.isOpenBordersTrading())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_PERMANENT_ALLIANCE",()), "CvScreensInterface", "WorldBuilderHandleTeamEditPermanentAllianceTradingCB", "TeamEditPermanentAllianceTrading", 0, pTeam.isPermanentAllianceTrading())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_DEFENSIVE_PACT",()), "CvScreensInterface", "WorldBuilderHandleTeamEditDefensivePactTradingCB", "TeamEditDefensivePactTrading", 0, pTeam.isDefensivePactTrading())
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_VASSAL_TRADING",()), "CvScreensInterface", "WorldBuilderHandleTeamEditVassalTradingCB", "TeamEditVassalTrading", 0, pTeam.isVassalStateTrading())
## Merge Team ##
		strTest = (localText.getText("TXT_KEY_WB_MERGE_TEAM",()),)
		for i in xrange(gc.getMAX_TEAMS()):
			if gc.getTeam(i).isEverAlive():
				if i == self.m_iCurrentTeam: continue
				strName = gc.getTeam(i).getName()
				if not gc.getTeam(i).isAlive():
					strName = gc.getPlayer(gc.getTeam(i).getLeaderID()).getName() + " " + localText.getText("TXT_KEY_WB_DEAD",())
				strTest = strTest + (strName,)
		self.m_tabCtrlEdit.addSectionDropdown("AddTeam", strTest, "CvScreensInterface", "WorldBuilderHandleAddTeamCB", "AddTeam", 0, 0)
## Projects ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_PROJECTS",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "ProjectEditScreen", 0)
## Technology ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_TECHNOLOGY",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "TechEditScreen", 0)
## Nuke Interception ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_NUKE_INTERCEPTION",()),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditNukeInterceptionCB", "CvScreensInterface", "WorldBuilderHandleTeamEditNukeInterceptionCB", "TeamEditNukeInterception", 0, -100, 100, 1, pTeam.getNukeInterception(), 0, 0)
## Domain Moves ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_DOMAIN_MOVES",()),  0)
		strTest = ()
		for i in range(3):
			strTest = strTest + (gc.getDomainInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Domain", strTest, "CvScreensInterface", "WorldBuilderHandleDomainEditPullDownCB", "DomainEditPullDown", 0, self.m_iDomain)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditDomainMovesCB", "CvScreensInterface", "WorldBuilderHandleTeamEditDomainMovesCB", "TeamEditDomainMoves", 0, 0, 10, 1, pTeam.getExtraMoves(self.m_iDomain), 0, 0)
## Route Change ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_ROUTE_CHANGE",()),  0)
		strTest = ()
		for i in xrange(gc.getNumRouteInfos()):
			strTest = strTest + (gc.getRouteInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Route", strTest, "CvScreensInterface", "WorldBuilderHandleRouteEditPullDownCB", "RouteEditPullDown", 0, self.m_iRoute)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditRouteChangeCB", "CvScreensInterface", "WorldBuilderHandleTeamEditRouteChangeCB", "TeamEditRouteChange", 0, -100, 100, 1, pTeam.getRouteChange(self.m_iRoute), 0, 0)
## Improvement Extra Yield ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_IMPROVEMENT_YIELD",()),  0)
		strTest = ()
		lImprovements = []
		for i in xrange(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isGraphicalOnly(): continue
			strTest = strTest + (gc.getImprovementInfo(i).getDescription(),)
			lImprovements.append(i)
		self.m_tabCtrlEdit.addSectionDropdown("Improvement", strTest, "CvScreensInterface", "WorldBuilderHandleImprovementEditPullDownCB", "ImprovementEditPullDown", 0, self.m_iImprovement)
		strTest = ()
		for i in xrange(3):
			strTest = strTest + (gc.getYieldInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Yield", strTest, "CvScreensInterface", "WorldBuilderHandleYieldEditPullDownCB", "YieldEditPullDown", 0, self.m_iYield)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditImprovementYieldCB", "CvScreensInterface", "WorldBuilderHandleTeamEditImprovementYieldCB", "TeamEditImprovementYield", 0, 0, 10, 1, 	pTeam.getImprovementYieldChange(lImprovements[self.m_iImprovement], self.m_iYield), 0, 0)
##
		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Team Edit Screen ##

## Project Edit Screen ##
	def setProjectEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 5
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_PROJECTS",()))

		iProjectPerColumn = (gc.getNumProjectInfos() +1) /iNumColumns
		if (gc.getNumProjectInfos() +1) % iNumColumns > 0:
			iProjectPerColumn += 1
		iColumnLength = iProjectPerColumn *2
		iProjectColumn = (gc.getNumProjectInfos() +1) / iProjectPerColumn
		if (gc.getNumProjectInfos() +1) % iProjectPerColumn > 0:
			iProjectColumn += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)
		self.m_tabCtrlEdit.setSize(min(1000, iProjectColumn * 200), min(700, max(5, iColumnLength) * 42))

		lProject = []
		for i in xrange(gc.getNumProjectInfos()):
			lProject.append(gc.getProjectInfo(i).getDescription() + "_Platy_" + str(i))
		lProject.sort()

		for i in lProject:
			sProject = i[:i.find("_Platy_")]
			iProject = int(i[i.find("_Platy_") +7:])
			self.m_tabCtrlEdit.addSectionLabel(sProject,  0)
			self.m_tabCtrlEdit.addSectionSpinner(sProject, "CvScreensInterface", "WorldBuilderHandleEditTeamProjectCB", str(iProject), 0, 	0, max(1, gc.getProjectInfo(iProject).getVictoryThreshold(gc.getInfoTypeForString("VICTORY_SPACE_RACE"))), 1, gc.getTeam(self.m_iCurrentTeam).getProjectCount(iProject), 0, 0)		

		for i in range(iProjectColumn * iColumnLength - (gc.getNumProjectInfos() *2 +1)):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToTeam", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Project Edit Screen ##

## Technology Edit Screen ##
	def setTechnologyEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 7
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_TECHNOLOGY",()))
		iEraPerColumn = (gc.getNumEraInfos() + 6) / iNumColumns
		iMax = 0
		for iEra in xrange(0, gc.getNumEraInfos(), iEraPerColumn):
			iCount = 0
			for i in xrange(gc.getNumTechInfos()):
				if gc.getTechInfo(i).getEra() >= iEra and gc.getTechInfo(i).getEra() < (iEra + iEraPerColumn):
					iCount += 1
			iMax = max(iCount, iMax)
		self.m_tabCtrlEdit.setColumnLength(iMax +iEraPerColumn *2 -1)
		self.m_tabCtrlEdit.setSize(1000, 600)

		iCount = 0
		for iEra in xrange(gc.getNumEraInfos()):
			self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_ERA",(gc.getEraInfo(iEra).getDescription(),)),  0)
			lTech = []
			for i in xrange(gc.getNumTechInfos()):
				if gc.getTechInfo(i).getEra() == iEra:
					lTech.append(gc.getTechInfo(i).getDescription() + "_Platy_" + str(i))
					iCount += 1
			lTech.sort()
			for i in lTech:
				sTech = i[:i.find("_Platy_")]
				iTech = int(i[i.find("_Platy_") +7:])
				self.m_tabCtrlEdit.addSectionCheckbox(sTech, "CvScreensInterface", "WorldBuilderHandleEditTeamTechnologyCB", str(iTech), 0, gc.getTeam(self.m_iCurrentTeam).isHasTech(iTech))
			if iEra == gc.getNumEraInfos() -1:
				for i in range(iMax - iCount -3):
					self.m_tabCtrlEdit.addSectionLabel(" ",  0)
			elif (iEra +1) % iEraPerColumn > 0:
				self.m_tabCtrlEdit.addSectionLabel(" ",  0)
			else:
				for i in range(iMax - iCount):
					self.m_tabCtrlEdit.addSectionLabel(" ",  0)
				iCount = 0

		strTest = (localText.getText("TXT_KEY_WB_ADD_ERA",()),)
		for i in xrange(gc.getNumEraInfos()):
			strTest = strTest + (localText.getText("TXT_KEY_WB_ERA", (gc.getEraInfo(i).getDescription(),)),)
		strTest = strTest + (localText.getText("TXT_KEY_WB_ALL_TECHS",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Tech By Era", strTest, "CvScreensInterface", "WorldBuilderHandleTechByEraPullDownCB", "TechByEraPullDown", 0, 0)
		strTest = (localText.getText("TXT_KEY_WB_REMOVE_ERA",()),)
		for i in xrange(gc.getNumEraInfos()):
			strTest = strTest + (localText.getText("TXT_KEY_WB_ERA", (gc.getEraInfo(i).getDescription(),)),)
		strTest = strTest + (localText.getText("TXT_KEY_WB_ALL_TECHS",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Tech By Era", strTest, "CvScreensInterface", "WorldBuilderHandleRemoveTechByEraPullDownCB", "RemoveTechByEraPullDown", 0, 0)
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_BACK",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEnterNewScreenCB", "BackToTeam", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Technology Edit Screen ##

## Diplomacy Edit Screen ##		
	def setDiplomacyEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		self.m_tabCtrlEdit.setNumColumns(2)
		self.m_tabCtrlEdit.setColumnLength(18)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_DIPLOMACY",()))

## Setting up Other Player ##
		if self.m_iCurrentPlayer == self.m_iOtherPlayer:
			for i in xrange(gc.getMAX_PLAYERS()):
				if gc.getPlayer(i).isEverAlive() and self.m_iCurrentPlayer != i:
					self.m_iOtherPlayer = i
					break
## Current Player ##
		strTest = ()
		iCount = 0
		for i in xrange(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive():
				strPlayerAliveStatus = gc.getPlayer(i).getName()
				if not gc.getPlayer(i).isAlive():
					strPlayerAliveStatus = strPlayerAliveStatus + localText.getText("TXT_KEY_WB_DEAD",())
				strTest = strTest + (strPlayerAliveStatus,)
				if i == self.m_iCurrentPlayer:
					iCurrentPlayer = iCount
				iCount += 1
		self.m_tabCtrlEdit.addSectionDropdown("Current Player", strTest, "CvScreensInterface", "WorldBuilderHandleCurrentPlayerEditPullDownCB", "DiplomacyEditCurrentPlayer", 0, iCurrentPlayer)
		pOtherPlayer = gc.getPlayer(self.m_iOtherPlayer)
		self.m_iOtherTeam = pOtherPlayer.getTeam()
		pPlayer = gc.getPlayer(self.m_iCurrentPlayer)
		pTeam = gc.getTeam(self.m_iCurrentTeam)
## Meet Status ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_MET",()), "CvScreensInterface", "WorldBuilderHandleTeamEditMetStatusCB", "TeamEditMetStatus", 0, pTeam.isHasMet(self.m_iOtherTeam))
## War Status ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_WAR",()), "CvScreensInterface", "WorldBuilderHandleTeamEditWarStatusCB", "TeamEditWarStatus", 0, pTeam.isAtWar(self.m_iOtherTeam))
## Sign Open Borders ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_OPEN_BORDERS",()), "CvScreensInterface", "WorldBuilderHandleTeamEditSignOpenBordersCB", "TeamEditSignOpenBorders", 0, pTeam.isOpenBorders(self.m_iOtherTeam))
## Sign Defensive Pact ##
		self.m_tabCtrlEdit.addSectionCheckbox(localText.getText("TXT_KEY_WB_DEFENSIVE_PACT",()), "CvScreensInterface", "WorldBuilderHandleTeamEditSignDefensivePactCB", "TeamEditSignDefensivePact", 0, pTeam.isDefensivePact(self.m_iOtherTeam))
## Relationship ##
		strTest = (localText.getText("TXT_KEY_WB_FVASSAL_OF",(pOtherPlayer.getName(),)),) + (localText.getText("TXT_KEY_WB_CVASSAL_OF",(pOtherPlayer.getName(),)),) + (localText.getText("TXT_KEY_WB_MASTER_OF",(pOtherPlayer.getName(),)),) + (localText.getText("TXT_KEY_WB_NONE",()),)
		self.m_tabCtrlEdit.addSectionDropdown(str(self.m_iCurrentPlayer), strTest, "CvScreensInterface", "WorldBuilderHandleTeamEditRelationshipCB", str(self.m_iCurrentPlayer), 0, self.relationshipStatus(self.m_iCurrentTeam, self.m_iOtherTeam))
## Memory ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_MEMORY",(pOtherPlayer.getName(),)),  0)
		strTest = ()
		for i in range(33):
			strTest = strTest + (gc.getMemoryInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Memory", strTest, "CvScreensInterface", "WorldBuilderHandleMemoryEditPullDownCB", "MemoryEditPullDown", 0, self.m_iMemory)
		self.m_tabCtrlEdit.addSectionSpinner("Current Player", "CvScreensInterface", 	"WorldBuilderHandlePlayerEditMemoryCB", str(self.m_iCurrentPlayer), 0, 0, 100, 1, gc.getPlayer(self.m_iCurrentPlayer).AI_getMemoryCount(self.m_iOtherPlayer, self.m_iMemory), 0, 0)
## Attitude ##
		strTest = ()
		for i in range(5):
			strTest = strTest + (localText.getText("TXT_KEY_WB_ATTITUDE_TOWARDS",(gc.getAttitudeInfo(i).getDescription(), pOtherPlayer.getName(),)),)
		self.m_tabCtrlEdit.addSectionDropdown("Attitude", strTest, "CvScreensInterface", "WorldBuilderHandleAttitudeEditPullDownCB", str(self.m_iCurrentPlayer), 0, gc.getPlayer(self.m_iCurrentPlayer).AI_getAttitude(self.m_iOtherPlayer))
## Espionage ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_ESPIONAGE_POINTS",(pOtherPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditEspionagePointsCB", "CvScreensInterface", "WorldBuilderHandleTeamEditEspionagePointsCB", str(self.m_iCurrentTeam), 0, 0, 1000000, 1, pTeam.getEspionagePointsAgainstTeam(self.m_iOtherTeam), 0, 0)
## Counter Espionage ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_COUNTER_ESPIONAGE_MOD",(pOtherPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditCounterEspionageModCB", "CvScreensInterface", "WorldBuilderHandleTeamEditCounterEspionageModCB", str(self.m_iCurrentTeam), 0, 0, 1000, 1, pTeam.getCounterespionageModAgainstTeam(self.m_iOtherTeam), 0, 0)

		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_COUNTER_ESPIONAGE",(pOtherPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditCounterEspionageCB", "CvScreensInterface", "WorldBuilderHandleTeamEditCounterEspionageCB", str(self.m_iCurrentTeam), 0, 0, 1000, 1, pTeam.getCounterespionageTurnsLeftAgainstTeam(self.m_iOtherTeam), 0, 0)
## War Weariness ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_WAR_WEARINESS",(pOtherPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditWarWearinessCB", "CvScreensInterface", "WorldBuilderHandleTeamEditWarWearinessCB", str(self.m_iCurrentTeam), 0, 0, 10000, 	1, pTeam.getWarWeariness(self.m_iOtherTeam), 0, 0)
## Other Player Data ##
		strTest = ()
		iCount = 0
		for i in xrange(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive() and i != self.m_iCurrentPlayer:
				strPlayerAliveStatus = gc.getPlayer(i).getName()
				if not gc.getPlayer(i).isAlive():
					strPlayerAliveStatus = strPlayerAliveStatus + " " + localText.getText("TXT_KEY_WB_DEAD",())
				strTest = strTest + (strPlayerAliveStatus,)
				if self.m_iOtherPlayer == self.m_iCurrentPlayer:
					iOtherPlayer = 0
					self.m_iOtherPlayer = i
				if self.m_iOtherPlayer == i:
					iOtherPlayer = iCount
				iCount += 1
		self.m_tabCtrlEdit.addSectionDropdown("Other Player", strTest, "CvScreensInterface", "WorldBuilderHandleOtherPlayerEditPullDownCB", "OtherPlayerEditPullDown", 0, iOtherPlayer)
		pOtherPlayer = gc.getPlayer(self.m_iOtherPlayer)
		self.m_iOtherTeam = pOtherPlayer.getTeam()
		pOtherTeam = gc.getTeam(self.m_iOtherTeam)
## Status with All ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_MEET_ALL",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleMeetAllCB", "MeetAll", 0)
		strTest = (localText.getText("TXT_KEY_WB_STATUS_ALL",()),) + (localText.getText("TXT_KEY_WB_WAR",()),) + (localText.getText("TXT_KEY_WB_PEACE",()),)
		self.m_tabCtrlEdit.addSectionDropdown("War Status All", strTest, "CvScreensInterface", "WorldBuilderHandleWarStatusAllCB", "WarStatusAll", 0, 0)
		strTest = (localText.getText("TXT_KEY_WB_STATUS_ALL",()),) + (localText.getText("TXT_KEY_WB_SIGN_ALL",()),) + (localText.getText("TXT_KEY_WB_CANCEL_ALL",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Open Borders All", strTest, "CvScreensInterface", "WorldBuilderHandleOpenBordersAllCB", "OpenBordersAll", 0, 0)
		strTest = (localText.getText("TXT_KEY_WB_STATUS_ALL",()),) + (localText.getText("TXT_KEY_WB_SIGN_ALL",()),) + (localText.getText("TXT_KEY_WB_CANCEL_ALL",()),)
		self.m_tabCtrlEdit.addSectionDropdown("Open Borders All", strTest, "CvScreensInterface", "WorldBuilderHandleDefensivePactAllCB", "DefensivePactAll", 0, 0)
## Relationship ##
		strTest = (localText.getText("TXT_KEY_WB_FVASSAL_OF",(pPlayer.getName(),)),) + (localText.getText("TXT_KEY_WB_CVASSAL_OF",(pPlayer.getName(),)),) + (localText.getText("TXT_KEY_WB_MASTER_OF",(pPlayer.getName(),)),) + (localText.getText("TXT_KEY_WB_NONE",()),)
		self.m_tabCtrlEdit.addSectionDropdown(str(self.m_iOtherPlayer), strTest, "CvScreensInterface", "WorldBuilderHandleTeamEditRelationshipCB", str(self.m_iOtherPlayer), 0, self.relationshipStatus(self.m_iOtherTeam, self.m_iCurrentTeam))
## Memory ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_MEMORY",(pPlayer.getName(),)),  0)
		strTest = ()
		for i in range(33):
			strTest = strTest + (gc.getMemoryInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Memory", strTest, "CvScreensInterface", "WorldBuilderHandleMemoryEditPullDownCB", "MemoryEditPullDown", 0, self.m_iMemory)
		self.m_tabCtrlEdit.addSectionSpinner(str(self.m_iOtherPlayer), "CvScreensInterface", "WorldBuilderHandlePlayerEditMemoryCB", str(self.m_iOtherPlayer), 0, 0, 100, 1, pOtherPlayer.AI_getMemoryCount(self.m_iCurrentPlayer, self.m_iMemory), 0, 0)
## Attitude ##
		strTest = ()
		for i in range(5):
			strTest = strTest + (localText.getText("TXT_KEY_WB_ATTITUDE_TOWARDS",(gc.getAttitudeInfo(i).getDescription(), pPlayer.getName(),)),)
		self.m_tabCtrlEdit.addSectionDropdown("AttitudeOC", strTest, "CvScreensInterface", "WorldBuilderHandleAttitudeEditPullDownCB", str(self.m_iOtherPlayer), 0, pOtherPlayer.AI_getAttitude(self.m_iCurrentPlayer))
## Espionage ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_ESPIONAGE_POINTS",(pPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditEspionageOCPointsCB", "CvScreensInterface", "WorldBuilderHandleTeamEditEspionagePointsCB", str(self.m_iOtherTeam), 0, 0, 1000000, 1, pOtherTeam.getEspionagePointsAgainstTeam(self.m_iCurrentTeam), 0, 0)
## Counter Espionage ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_COUNTER_ESPIONAGE_MOD",(pPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditCounterEspionageModCB", "CvScreensInterface", "WorldBuilderHandleTeamEditCounterEspionageModCB", str(self.m_iOtherTeam), 0, 0, 1000, 1, pOtherTeam.getCounterespionageModAgainstTeam(self.m_iCurrentTeam), 0, 0)

		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_COUNTER_ESPIONAGE",(pPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditCounterEspionageCB", "CvScreensInterface", "WorldBuilderHandleTeamEditCounterEspionageCB", str(self.m_iOtherTeam), 0, 0, 1000, 1, pOtherTeam.getCounterespionageTurnsLeftAgainstTeam(self.m_iCurrentTeam), 0, 0)
## War Weariness ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_WAR_WEARINESS",(pPlayer.getName(),)),  0)
		self.m_tabCtrlEdit.addSectionSpinner("TeamEditWarWearinessCB", "CvScreensInterface", "WorldBuilderHandleTeamEditWarWearinessCB", str(self.m_iOtherTeam), 0, 0, 10000, 1, pOtherTeam.getWarWeariness(self.m_iCurrentTeam), 0, 0)
##			
		if (not self.m_tabCtrlEdit.isNone()):
			print("Enabling map control 5")
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Diplomacy Edit Screen ##

## Add New Player ##
	def AddNewPlayer(self, bInitial):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		self.m_tabCtrlEdit.setNumColumns(1)
		self.m_tabCtrlEdit.setColumnLength(10)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_ADD_NEW_PLAYER",()))

		if bInitial:
			self.m_iNewCivilization = -1
			self.m_iNewLeaderType = -1
		strTest = (localText.getText("TXT_KEY_WB_CHOOSE_CIVILIZATION",()),)
		iSelectedCiv = 0
		iCount = 1
		for i in xrange(gc.getNumCivilizationInfos()):
			if not CyGame().isCivEverActive(i):
				strTest = strTest + (gc.getCivilizationInfo(i).getDescription(),)
				if i == self.m_iNewCivilization:
					iSelectedCiv = iCount
				iCount+= 1
		self.m_tabCtrlEdit.addSectionDropdown("New Civilization", strTest, "CvScreensInterface", "WorldBuilderHandleAddPlayerCivilizationCB", "AddPlayerCivilization", 0, iSelectedCiv)
		if self.m_iNewCivilization > -1:
			strTest = (localText.getText("TXT_KEY_WB_CHOOSE_PLAYER",()),)
			iSelectedLeaderType = 0
			iCount = 1
			for i in xrange(gc.getNumLeaderHeadInfos()):
				if not CyGame().isLeaderEverActive(i):
					if not CyGame().isOption(GameOptionTypes.GAMEOPTION_LEAD_ANY_CIV):
						if not gc.getCivilizationInfo(self.m_iNewCivilization).isLeaders(i): continue
					strTest = strTest + (gc.getLeaderHeadInfo(i).getDescription(),)
					if i == self.m_iNewLeaderType:
						iSelectedLeaderType = iCount
					iCount+= 1
			self.m_tabCtrlEdit.addSectionDropdown("New Leader", strTest, "CvScreensInterface", "WorldBuilderHandleAddPlayerLeaderTypeCB", "AddPlayerLeaderType", 0, iSelectedLeaderType)
			if self.m_iNewLeaderType > -1:
				lTraits = []
				for i in xrange(gc.getNumTraitInfos()):
					if gc.getLeaderHeadInfo(self.m_iNewLeaderType).hasTrait(i):
						lTraits.append(i)
				sTrait = ""
				for j in xrange(len(lTraits)):
					sTrait += gc.getTraitInfo(lTraits[j]).getDescription()
					if j != len(lTraits) -1:
						sTrait += ", "
				if len(lTraits) == 0:
					sTrait = localText.getText("TXT_KEY_WB_NONE",())
				self.m_tabCtrlEdit.addSectionLabel(sTrait,  0)
				self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_CREATE_PLAYER",())+"\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleCreatePlayerCB", "Create Player", 0)
			
		if (not self.m_tabCtrlEdit.isNone()):
			print("Enabling map control 5")
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Add New Player ##

## Game Option Screen ##
	def setGameOptionEditInfo(self):
		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()

		iNumColumns = 4
		self.m_tabCtrlEdit.setNumColumns(iNumColumns)
		iColumnLength = gc.getNumGameOptionInfos() /iNumColumns
		if gc.getNumGameOptionInfos() %iNumColumns > 0:
			iColumnLength += 1
		self.m_tabCtrlEdit.setColumnLength(iColumnLength)

		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_GAME_OPTION",()))
		for i in xrange(gc.getNumGameOptionInfos()):
			self.m_tabCtrlEdit.addSectionCheckbox(gc.getGameOptionInfo(i).getDescription(), "CvScreensInterface", "WorldBuilderHandleEditGameOptionCB", str(i), 0, CyGame().isOption(i))
		for i in range(iNumColumns * iColumnLength - gc.getNumGameOptionInfos()):
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)

		if (not self.m_tabCtrlEdit.isNone()):
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Game Option Screen ##

## Plot Edit Screen ##
	def setPlotEditInfo(self, bNewPlot):

		initWBToolEditCtrl()
		self.m_tabCtrlEdit = getWBToolEditTabCtrl()
		if bNewPlot:
			self.m_pActivePlot = self.m_pCurrentPlot

		self.m_tabCtrlEdit.setNumColumns(3)
		self.m_tabCtrlEdit.setColumnLength(9)
		self.m_tabCtrlEdit.addTabSection(localText.getText("TXT_KEY_WB_PLOT_DATA",(self.m_pActivePlot.getX(), self.m_pActivePlot.getY())))
## Culture ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CULTURE",()),  0)
		strTest = ()
		iCount = 0
		for i in xrange(gc.getMAX_PLAYERS()):
			if gc.getPlayer(i).isEverAlive():
				strTest = strTest + (gc.getPlayer(i).getName(),)
				if i == self.m_iCurrentPlayer:
					iOwner = iCount
				iCount = iCount + 1
		self.m_tabCtrlEdit.addSectionDropdown("Owner", strTest, "CvScreensInterface", "WorldBuilderHandleCurrentPlayerEditPullDownCB", "PlotEditCurrentPlayer", 0, iOwner)
		self.m_tabCtrlEdit.addSectionSpinner("PlotEditCultureCB", "CvScreensInterface", "WorldBuilderHandlePlotEditCultureCB", "PlotEditCulture", 0, 1, 100000000, 1, self.m_pActivePlot.getCulture(self.m_iCurrentPlayer), 0, 0)
## Plot Yield ##
		self.m_tabCtrlEdit.addSectionLabel(gc.getYieldInfo(0).getDescription() + ":",  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlotEditYieldCB", "CvScreensInterface", "WorldBuilderHandlePlotEditYieldCB", "PlotEditFood", 0, 0, 20, 1, self.m_pActivePlot.getYield(YieldTypes.YIELD_FOOD), 0, 0)
		self.m_tabCtrlEdit.addSectionLabel(gc.getYieldInfo(1).getDescription() + ":",  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlotEditYieldCB", "CvScreensInterface", "WorldBuilderHandlePlotEditYieldCB", "PlotEditProduction", 0, 0, 20, 1, self.m_pActivePlot.getYield(YieldTypes.YIELD_PRODUCTION), 0, 0)
		self.m_tabCtrlEdit.addSectionLabel(gc.getYieldInfo(2).getDescription() + ":",  0)
		self.m_tabCtrlEdit.addSectionSpinner("PlotEditYieldCB", "CvScreensInterface", "WorldBuilderHandlePlotEditYieldCB", "PlotEditCommerce", 0, 0, 20, 1, self.m_pActivePlot.getYield(YieldTypes.YIELD_COMMERCE), 0, 0)
## Plot Type ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CHANGE_PLOTTYPE",()),  0)
		strTest = (localText.getText("TXT_KEY_WB_MOUNTAIN",()),) + (localText.getText("TXT_KEY_WB_HILL",()),) + (localText.getText("TXT_KEY_WB_LAND",()),) + (localText.getText("TXT_KEY_WB_OCEAN",()),)
		self.m_tabCtrlEdit.addSectionDropdown("PlotEditPlotType", strTest, "CvScreensInterface", "WorldBuilderHandlePlotEditPlotTypeCB", "PlotEditPlotType", 0, self.m_pActivePlot.getPlotType())
## Terrain ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CHANGE_TERRAIN",()),  0)
		strTest = ()
		iTerrain = 0
		iCount = 0
		for i in xrange(gc.getNumTerrainInfos()):
			if gc.getTerrainInfo(i).isGraphicalOnly(): continue
			if self.m_pActivePlot.getTerrainType() == i:
				iTerrain = iCount
			strTest = strTest + (gc.getTerrainInfo(i).getDescription(),)
			iCount += 1
		self.m_tabCtrlEdit.addSectionDropdown("Plot Terrain", strTest, "CvScreensInterface", "WorldBuilderHandlePlotEditTerrainCB", "PlotEditTerrain", 0, iTerrain)
## Bonus ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_BONUS",()),  0)
		strTest = (localText.getText("TXT_KEY_WB_NONE",()),)
		for i in xrange(gc.getNumBonusInfos()):
			strTest = strTest + (gc.getBonusInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Bonus", strTest, "CvScreensInterface", "WorldBuilderHandlePlotEditBonusCB", "PlotEditBonus", 0, self.m_pActivePlot.getBonusType(-1) +1)
## Feature ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_FEATURE_VARIETY",()),  0)
		strTest = (localText.getText("TXT_KEY_WB_NONE",()),)
		for i in xrange(gc.getNumFeatureInfos()):
			strTest = strTest + (gc.getFeatureInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("PlotEditFeature", strTest, "CvScreensInterface", "WorldBuilderHandlePlotEditFeatureCB", "PlotEditFeature", 0, self.m_pActivePlot.getFeatureType() +1)
## Variety ##
		if self.m_pActivePlot.getFeatureType() > -1 and gc.getFeatureInfo(self.m_pActivePlot.getFeatureType()).getNumVarieties() > 1:
			self.m_tabCtrlEdit.addSectionSpinner("PlotEditVarietyCB", "CvScreensInterface", "WorldBuilderHandlePlotEditVarietyCB", "PlotEditVariety", 0, 0, gc.getFeatureInfo(self.m_pActivePlot.getFeatureType()).getNumVarieties(), 1, self.m_pActivePlot.getFeatureVariety(), 0, 0)
		else:
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
## Route ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_CHANGE_ROUTE",()),  0)
		strTest = (localText.getText("TXT_KEY_WB_NONE",()),)
		for i in xrange(gc.getNumRouteInfos()):
			strTest = strTest + (gc.getRouteInfo(i).getDescription(),)
		self.m_tabCtrlEdit.addSectionDropdown("Route", strTest, "CvScreensInterface", "WorldBuilderHandlePlotEditRouteCB", "PlotEditRoute", 0, self.m_pActivePlot.getRouteType() +1)
## Improvement ##
		self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_IMPROVEMENT",()),  0)
		strTest = (localText.getText("TXT_KEY_WB_NONE",()),)
		iImprovement = 0
		iCount = 1
		for i in xrange(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isGraphicalOnly(): continue
			if self.m_pActivePlot.getImprovementType() == i:
				iImprovement = iCount
			strTest = strTest + (gc.getImprovementInfo(i).getDescription(),)
			iCount += 1
		self.m_tabCtrlEdit.addSectionDropdown("Improvement", strTest, "CvScreensInterface", "WorldBuilderHandlePlotEditImprovementCB", "PlotEditImprovement", 0, iImprovement)
## Upgrade Timer ##
		if self.m_pActivePlot.getOwner() > -1 and self.m_pActivePlot.getImprovementType() > -1 and gc.getImprovementInfo(self.m_pActivePlot.getImprovementType()).getUpgradeTime() > 0:
			self.m_tabCtrlEdit.addSectionLabel(localText.getText("TXT_KEY_WB_UPGRADE_PROGRESS",()),  0)
			self.m_tabCtrlEdit.addSectionSpinner("PlotEditUpgradeProgressCB", "CvScreensInterface", "WorldBuilderHandlePlotEditUpgradeProgressCB", "PlotEditUpgradeProgress", 0, 1, 1000, 1, self.m_pActivePlot.getUpgradeTimeLeft(self.m_pActivePlot.getImprovementType(), self.m_pActivePlot.getOwner()), 0, 0)
		else:
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
			self.m_tabCtrlEdit.addSectionLabel(" ",  0)
## City ##
		if (self.m_pActivePlot.isCity()):
			self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_EDIT_CITY",()) + "\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandlePlotEditCityCB", "PlotEditCity", 0)
		else:
			self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_ADD_CITY",()) + "\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandlePlotAddCityCB", "PlotAddCity", 0)
## Unit ##
		if (self.m_pActivePlot.getNumUnits() > 0):
			strTest = ()
			for i in xrange(self.m_pActivePlot.getNumUnits()):
				if (len(self.m_pActivePlot.getUnit(i).getNameNoDesc())):
					strTest = strTest + (self.m_pActivePlot.getUnit(i).getNameNoDesc(),)
				else:
					strTest = strTest + (self.m_pActivePlot.getUnit(i).getName(),)
			strTest = strTest + (localText.getText("TXT_KEY_WB_EDIT_UNIT",()),)
			self.m_tabCtrlEdit.addSectionDropdown("Current_Unit", strTest, "CvScreensInterface", "WorldBuilderHandleUnitEditPullDownCB", "UnitEditPullDown", 0, self.m_pActivePlot.getNumUnits())
## Script ##
		self.m_tabCtrlEdit.addSectionButton(localText.getText("TXT_KEY_WB_ADD_SCRIPT",()) + "\b\b\b\b\b\b", "CvScreensInterface", "WorldBuilderHandleEditScriptCB", "PlotEditScript", 0)

		if (not self.m_tabCtrlEdit.isNone()):
			print("Enabling map control 5")
			self.m_normalPlayerTabCtrl.enable(False)
			self.m_normalMapTabCtrl.enable(False)
			self.m_bCtrlEditUp = True
		return
## Plot Edit Screen ##

	def initCityEditScreen(self):
		self.setCityEditInfo(False)
		return

	def toggleUnitEditCB(self):
		self.m_bUnitEdit = True
		self.m_bCityEdit = False
		self.m_bNormalPlayer = False
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = False
## Add Units ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Add Units ##

		if (self.m_tabCtrlEdit != 0):
			print("Enabling map control 6")
			self.m_tabCtrlEdit.enable(False)

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iUnitEditCheckboxID)
		print("Enabling map control 7")
		self.m_normalPlayerTabCtrl.enable(False)
		self.m_normalMapTabCtrl.enable(False)
		if (self.m_tabCtrlEdit != 0):
			self.m_tabCtrlEdit.destroy()
		return

	def toggleCityEditCB(self):
		self.m_bCityEdit = True
		self.m_bUnitEdit = False
		self.m_bNormalPlayer = False
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = False
## Add Units ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Add Units ##

		if (self.m_tabCtrlEdit != 0):
			print("Enabling map control 8")
			self.m_tabCtrlEdit.enable(False)

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iCityEditCheckboxID)
		print("Enabling map control 9")
		self.m_normalPlayerTabCtrl.enable(False)
		self.m_normalMapTabCtrl.enable(False)
		if (self.m_tabCtrlEdit != 0):
			self.m_tabCtrlEdit.destroy()
		return

	def normalPlayerTabModeCB(self):
		self.m_bCityEdit = False
		self.m_bUnitEdit = False
		self.m_bNormalPlayer = True
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = False
##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
##

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		
		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iNormalPlayerCheckboxID)
		if (self.m_normalMapTabCtrl):
			print("Disabling Map Tab")
			self.m_normalMapTabCtrl.enable(False)
		if (not self.m_normalPlayerTabCtrl.isEnabled() and not CyInterface().isInAdvancedStart()):
			print("Enabling Player Tab")
			self.m_normalPlayerTabCtrl.enable(True)
			if (self.m_tabCtrlEdit):
				self.m_tabCtrlEdit.enable(False)
			self.m_bCtrlEditUp = False
		return

	def normalMapTabModeCB(self):
		self.m_bCityEdit = False
		self.m_bUnitEdit = False
		self.m_bNormalPlayer = False
		self.m_bNormalMap = True
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = False
## Add Units ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Add Units ##

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iNormalMapCheckboxID)
		if (self.m_normalPlayerTabCtrl):
			print("Disabling Player Tab")
			self.m_normalPlayerTabCtrl.enable(False)
		if (not self.m_normalMapTabCtrl.isEnabled() and not CyInterface().isInAdvancedStart()):
			print("Enabling Map Tab")
			self.m_normalMapTabCtrl.enable(True)
			if (self.m_tabCtrlEdit):
				self.m_tabCtrlEdit.enable(False)
			self.m_bCtrlEditUp = False
		return

	def revealTabModeCB(self):
		self.m_bCtrlEditUp = False
		self.m_bCityEdit = False
		self.m_bUnitEdit = False
		self.m_bNormalPlayer = False
		self.m_bNormalMap = False
		self.m_bReveal = True
		self.m_bLandmark = False
		self.m_bEraseAll = False
## Add Units ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Add Units ##

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		self.refreshReveal()
		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iRevealTileCheckboxID)
		if (self.m_normalPlayerTabCtrl):
			self.m_normalPlayerTabCtrl.enable(False)
		if (self.m_normalMapTabCtrl):
			self.m_normalMapTabCtrl.enable(False)
		if (self.m_tabCtrlEdit):
			self.m_tabCtrlEdit.enable(False)
		return

	def diplomacyModeCB(self):
		self.m_bCtrlEditUp = False
		self.m_bCityEdit = False
		self.m_bUnitEdit = False
		self.m_bNormalPlayer = False
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = False
## Add Units ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Add Units ##

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iDiplomacyCheckboxID)
		if (self.m_normalPlayerTabCtrl != 0):
			self.m_normalPlayerTabCtrl.enable(False)
		if (self.m_normalMapTabCtrl != 0):
			self.m_normalMapTabCtrl.enable(False)
		if (self.m_tabCtrlEdit != 0):
			self.m_tabCtrlEdit.enable(False)
## Diplomacy Screen ##
		self.setDiplomacyEditInfo()
## Diplomacy Screen ##
		return

	def landmarkModeCB(self):
		self.m_bCtrlEditUp = False
		self.m_bCityEdit = False
		self.m_bUnitEdit = False
		self.m_bNormalPlayer = False
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = True
		self.m_bEraseAll = False
## Add Units ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Add Units ##

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iLandmarkCheckboxID)
		if (self.m_normalPlayerTabCtrl != 0):
			self.m_normalPlayerTabCtrl.enable(False)
		if (self.m_normalMapTabCtrl != 0):
			self.m_normalMapTabCtrl.enable(False)
		if (self.m_tabCtrlEdit != 0):
			self.m_tabCtrlEdit.enable(False)
		return

	def eraseCB(self):
		self.m_bCtrlEditUp = False
		self.m_bCityEdit = False
		self.m_bUnitEdit = False
		self.m_bNormalPlayer = False
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = True
		self.m_pRiverStartPlot = -1
## Add Units ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Add Units ##

		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		self.refreshSideMenu()
		self.setCurrentModeCheckbox(self.m_iEraseCheckboxID)
		if (self.m_normalPlayerTabCtrl != 0):
			self.m_normalPlayerTabCtrl.enable(False)
		if (self.m_normalMapTabCtrl != 0):
			self.m_normalMapTabCtrl.enable(False)
		if (self.m_tabCtrlEdit != 0):
			self.m_tabCtrlEdit.enable(False)
		return
		
	def setCurrentNormalPlayerIndex(self, argsList):
		iIndex = int(argsList)
		if (self.m_normalPlayerTabCtrl.getActiveTab() != self.m_iTechnologyTabID):
			self.m_iNormalPlayerCurrentIndexes [self.m_normalPlayerTabCtrl.getActiveTab()] = int(argsList)
		else:
			bOn = gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).isHasTech(iIndex)
			bOn = not bOn
			gc.getTeam(gc.getPlayer(self.m_iCurrentPlayer).getTeam()).setHasTech(iIndex, bOn, self.m_iCurrentPlayer, False, False)
## Add Units Start ##
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.refreshSideMenu()
## Add Units End ##
		return 1

	def setCurrentNormalMapIndex(self, argsList):
		iIndex = int(argsList)
		self.m_iNormalMapCurrentIndexes [self.m_normalMapTabCtrl.getActiveTab()] = int(argsList)
## Edit Area Map Start ##
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
		self.refreshSideMenu()
## Edit Area Map End ##
		return 1

	def setCurrentNormalMapList(self, argsList):
		self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] = int(argsList)
		return 1

	def setCurrentAdvancedStartIndex(self, argsList):
		iIndex = int(argsList)
		self.m_iAdvancedStartCurrentIndexes [self.m_advancedStartTabCtrl.getActiveTab()] = int(argsList)
		return 1

	def setCurrentAdvancedStartList(self, argsList):
		self.m_iAdvancedStartCurrentList[self.m_advancedStartTabCtrl.getActiveTab()] = int(argsList)
		return 1

## Platy World Builder Start ##
	def setEditButtonClicked(self, argsList):
		iIndex = int(argsList)
		if (self.m_bUnitEditCtrl):
			bOn = not self.m_pActivePlot.getUnit(self.m_iCurrentUnit).isHasPromotion(iIndex)
			self.m_pActivePlot.getUnit(self.m_iCurrentUnit).setHasPromotion(iIndex, bOn)
		return 1

	def relationshipStatus(self, iTeam1, iTeam2):
		if gc.getTeam(iTeam1).isVassal(iTeam2):
			for i in range(CyGame().getIndexAfterLastDeal()):
				pDeal = CyGame().getDeal(i)
				iPlayer1 = pDeal.getFirstPlayer()
				iPlayer2 = pDeal.getSecondPlayer()
				if iPlayer1 == -1 or iPlayer2 == -1: continue
				iTeamX = gc.getPlayer(pDeal.getFirstPlayer()).getTeam()
				iTeamY = gc.getPlayer(pDeal.getSecondPlayer()).getTeam()
				if (iTeam1 == iTeamX and iTeam2 == iTeamY) or (iTeam2 == iTeamX and iTeam1 == iTeamY):
					for j in range(pDeal.getLengthFirstTrades()):
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_VASSAL:	
							return 0
						if pDeal.getFirstTrade(j).ItemType == TradeableItems.TRADE_SURRENDER:	
							return 1
					for j in range(pDeal.getLengthSecondTrades()):
						if pDeal.getSecondTrade(j).ItemType == TradeableItems.TRADE_VASSAL:	
							return 0
						if pDeal.getSecondTrade(j).ItemType == TradeableItems.TRADE_SURRENDER:	
							return 1
		elif gc.getTeam(iTeam2).isVassal(iTeam1):
			return 2
		return 3
## Platy World Builder End ##

	def getUnitTabID(self):
		return self.m_iUnitTabID

	def getBuildingTabID(self):
		return self.m_iBuildingTabID

	def getTechnologyTabID(self):
		return self.m_iTechnologyTabID

	def getImprovementTabID(self):
		return self.m_iImprovementTabID

	def getBonusTabID(self):
		return self.m_iBonusTabID

	def getImprovementListID(self):
		return self.m_iImprovementListID

	def getBonusListID(self):
		return self.m_iBonusListID

	def getTerrainTabID(self):
		return self.m_iTerrainTabID

	def getTerrainListID(self):
		return self.m_iTerrainListID

	def getFeatureListID(self):
		return self.m_iFeatureListID

	def getPlotTypeListID(self):
		return self.m_iPlotTypeListID

	def getRouteListID(self):
		return self.m_iRouteListID

	def getTerritoryTabID(self):
		return self.m_iTerritoryTabID

	def getTerritoryListID(self):
		return self.m_iTerritoryListID

	def getASUnitTabID(self):
		return self.m_iASUnitTabID

	def getASUnitListID(self):
		return self.m_iASUnitListID

	def getASCityTabID(self):
		return self.m_iASCityTabID

	def getASCityListID(self):
		return self.m_iASCityListID

	def getASBuildingsListID(self):
		return self.m_iASBuildingsListID

	def getASAutomateListID(self):
		return self.m_iASAutomateListID

	def getASImprovementsTabID(self):
		return self.m_iASImprovementsTabID

	def getASRoutesListID(self):
		return self.m_iASRoutesListID

	def getASImprovementsListID(self):
		return self.m_iASImprovementsListID

	def getASVisibilityTabID(self):
		return self.m_iASVisibilityTabID

	def getASVisibilityListID(self):
		return self.m_iASVisibilityListID

	def getASTechTabID(self):
		return self.m_iASTechTabID

	def getASTechListID(self):
		return self.m_iASTechListID

	def highlightBrush(self):
				
		if (self.m_bShowBigBrush):
			if (self.m_pCurrentPlot == 0):
				return
				
			CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
			CyEngine().fillAreaBorderPlotAlt(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
			for i in range( (self.m_iBrushWidth-1) ):
				for j in range((self.m_iBrushHeight)):
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX()-(i+1), self.m_pCurrentPlot.getY()-(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY()-(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX()+(i+1), self.m_pCurrentPlot.getY()-(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX()-(i+1), self.m_pCurrentPlot.getY()+(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY()+(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX()+(i+1), self.m_pCurrentPlot.getY()+(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
			if (not self.m_iBrushWidth):
				pPlot = CyMap().plot(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY())
				if (not pPlot.isNone()):
					CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
				for j in range((self.m_iBrushHeight)):
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY()-(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
					pPlot = CyMap().plot(self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY()-(j))
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", 1)
				
		return

	def placeMultipleObjects(self):
		bInsideForLoop = False
		permCurrentPlot = self.m_pCurrentPlot
		for i in range( (self.m_iBrushWidth-1) ):
			for j in range((self.m_iBrushHeight)):
				bInsideForLoop = True
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()-(i+1), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()+(i+1), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()-(i+1), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()+(i+1), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
		if (not bInsideForLoop):
			self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY())
			if (not self.m_pCurrentPlot.isNone()):
				self.placeObject()
			for j in range((self.m_iBrushHeight)):
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.placeObject()
		self.m_pCurrentPlot = permCurrentPlot
		return

	def removeMultipleObjects(self):
		bInsideForLoop = False
		permCurrentPlot = self.m_pCurrentPlot
		for i in range( (self.m_iBrushWidth-1) ):
			for j in range((self.m_iBrushHeight)):
				bInsideForLoop = True
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()-(i+1), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()+(i+1), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()-(i+1), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()+(i+1), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
		if (not bInsideForLoop):
			self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY())
			if (not self.m_pCurrentPlot.isNone()):
				self.removeObject()
			for j in range((self.m_iBrushHeight)):
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.removeObject()
		self.m_pCurrentPlot = permCurrentPlot
		return

	def showMultipleReveal(self):
		print "showMultipleReveal"
		self.refreshReveal()
		return

	def setMultipleReveal(self, bReveal):
		print "setMultipleReveal"
		bInsideForLoop = False
		permCurrentPlot = self.m_pCurrentPlot
		for i in range( (self.m_iBrushWidth-1) ):
			for j in range((self.m_iBrushHeight)):
				bInsideForLoop = True
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()-(i+1), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()+(i+1), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()-(i+1), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX()+(i+1), permCurrentPlot.getY()+(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
		if (not bInsideForLoop):
			self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY())
			if (not self.m_pCurrentPlot.isNone()):
				self.RevealCurrentPlot(bReveal)
			for j in range((self.m_iBrushHeight)):
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
				self.m_pCurrentPlot = CyMap().plot(permCurrentPlot.getX(), permCurrentPlot.getY()-(j))
				if (not self.m_pCurrentPlot.isNone()):
					self.RevealCurrentPlot(bReveal)
		self.m_pCurrentPlot = permCurrentPlot
		self.showMultipleReveal()
		return

	def useLargeBrush(self):
		if 	(
				(
					(self.m_bNormalMap) and 
					(not self.m_bUnitEdit) and 
					(not self.m_bCityEdit)
				) 
				and
				(
					(
						(self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerrainTabID) and
						(
							(self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iTerrainListID) or
							(self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iFeatureListID) or
							(self.m_iNormalMapCurrentList[self.m_normalMapTabCtrl.getActiveTab()] == self.m_iPlotTypeListID)
						)
					) 
					or
					(
						(self.m_normalMapTabCtrl.getActiveTab() == self.m_iBonusTabID)
					)
					or
					(
						(self.m_normalMapTabCtrl.getActiveTab() == self.m_iTerritoryTabID)
					)
				)
			):
			return True
		elif (self.m_bReveal):
			return True
		else:
			return False

	def clearSideMenu(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		screen.deleteWidget("WorldBuilderMainPanel")
		screen.deleteWidget("WorldBuilderBackgroundPanel")

		screen.deleteWidget("WorldBuilderSaveButton")
		screen.deleteWidget("WorldBuilderLoadButton")
		screen.deleteWidget("WorldBuilderAllPlotsButton")
		screen.deleteWidget("WorldBuilderExitButton")
		
		screen.deleteWidget("WorldBuilderUnitEditMode")
		screen.deleteWidget("WorldBuilderCityEditMode")

		screen.deleteWidget("WorldBuilderNormalPlayerMode")
		screen.deleteWidget("WorldBuilderNormalMapMode")
		screen.deleteWidget("WorldBuilderRevealMode")

		screen.deleteWidget("WorldBuilderPlayerChoice")
## Side Panel ##
		screen.deleteWidget("WorldBuilderGameData")
		screen.deleteWidget("WorldBuilderAddUnits")
		screen.deleteWidget("WorldBuilderUnitCombat")
		screen.deleteWidget("WorldBuilderEditAreaMap")
		screen.deleteWidget("WorldBuilderModifyAreaPlotType")
		screen.deleteWidget("WorldBuilderModifyAreaTerrain")
		screen.deleteWidget("WorldBuilderModifyAreaRoute")
		screen.deleteWidget("WorldBuilderModifyAreaFeature")
## Side Panel ##
		screen.deleteWidget("WorldBuilderBrushSize")
		screen.deleteWidget("WorldBuilderRegenerateMap")
		screen.deleteWidget("WorldBuilderTeamChoice")

		screen.deleteWidget("WorldBuilderRevealAll")
		screen.deleteWidget("WorldBuilderUnrevealAll")
		screen.deleteWidget("WorldBuilderRevealPanel")

		screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
		return

	def setSideMenu(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )

		iMaxScreenWidth = screen.getXResolution()
		iMaxScreenHeight = screen.getYResolution()
		iScreenHeight = 10+37+37

		iButtonWidth = 32
		iButtonHeight = 32
		iButtonX = 0
		iButtonY = 0

		if (CyInterface().isInAdvancedStart()):
			iX = 0
		else:
			iX = iMaxScreenWidth-self.iScreenWidth
			
		screen.addPanel( "WorldBuilderBackgroundPanel", "", "", True, True, iX, 0, self.iScreenWidth, iScreenHeight, PanelStyles.PANEL_STYLE_MAIN )		
		screen.addScrollPanel( "WorldBuilderMainPanel", "", iX, 0, self.iScreenWidth, iScreenHeight, PanelStyles.PANEL_STYLE_MAIN )
				
		if (CyInterface().isInAdvancedStart()):
									
			iX = 50
			iY = 15
			szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_POINTS", (gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(), )) + "</font>"
			screen.setLabel("AdvancedStartPointsText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			iY += 30
			szText = localText.getText("TXT_KEY_ADVANCED_START_BEGIN_GAME", ())
			screen.setButtonGFC( "WorldBuilderExitButton", szText, "", iX, iY, 130, 28, WidgetTypes.WIDGET_WB_EXIT_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

			szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_COST_THIS_LOCATION", (self.m_iCost, )) + u"</font>"
			iY = 85
			screen.setLabel("AdvancedStartCostText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX-20, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
		else:
			
			iPanelWidth = 35*6
			screen.attachPanelAt( 
				"WorldBuilderMainPanel", 
				"WorldBuilderLoadSavePanel", 
				"", 
				"", 
				False, 
				True, 
				PanelStyles.PANEL_STYLE_CITY_TANSHADE, 
				70,
				0,
				iPanelWidth-70,
				35,
				WidgetTypes.WIDGET_GENERAL, -1, -1)
			
			screen.setImageButtonAt( "WorldBuilderAllPlotsButton", "WorldBuilderLoadSavePanel", ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_CHANGE_ALL_PLOTS").getPath(), iButtonX, iButtonY, iButtonWidth, iButtonHeight, WidgetTypes.WIDGET_WB_ALL_PLOTS_BUTTON, -1, -1)
			iButtonX = iButtonX + 35
			screen.setImageButtonAt( "WorldBuilderSaveButton", "WorldBuilderLoadSavePanel", ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_SAVE").getPath(), iButtonX, iButtonY, iButtonWidth, iButtonHeight, WidgetTypes.WIDGET_WB_SAVE_BUTTON, -1, -1)
			iButtonX = iButtonX + 35
			screen.setImageButtonAt( "WorldBuilderLoadButton", "WorldBuilderLoadSavePanel", ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_LOAD").getPath(), iButtonX, iButtonY, iButtonWidth, iButtonHeight, WidgetTypes.WIDGET_WB_LOAD_BUTTON, -1, -1)
			iButtonX = iButtonX + 35
			screen.setImageButtonAt( "WorldBuilderExitButton", "WorldBuilderLoadSavePanel", ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_EXIT").getPath(), iButtonX, iButtonY, iButtonWidth, iButtonHeight, WidgetTypes.WIDGET_WB_EXIT_BUTTON, -1, -1)
	
			iButtonWidth = 32
			iButtonHeight = 32
			iButtonX = 0
			iButtonY = 0
			self.m_iUnitEditCheckboxID = 0
			screen.addCheckBoxGFC(
				"WorldBuilderUnitEditModeButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_TOGGLE_UNIT_EDIT_MODE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10+36),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_UNIT_EDIT_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				
			iButtonX = iButtonX + 35
			self.m_iCityEditCheckboxID = 1
			screen.addCheckBoxGFC(
				"WorldBuilderCityEditModeButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_TOGGLE_CITY_EDIT_MODE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10+36),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_CITY_EDIT_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				
			iButtonX = iButtonX + 35
			self.m_iNormalPlayerCheckboxID = 2
			screen.addCheckBoxGFC(
				"WorldBuilderNormalPlayerModeButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_NORMAL_UNIT_MODE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10+36),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_NORMAL_PLAYER_TAB_MODE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				
			iButtonX = iButtonX + 35
			self.m_iNormalMapCheckboxID = 3
			screen.addCheckBoxGFC(
				"WorldBuilderNormalMapModeButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_NORMAL_MAP_MODE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10+36),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_NORMAL_MAP_TAB_MODE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				
			iButtonX = iButtonX + 35
			self.m_iRevealTileCheckboxID = 4
			screen.addCheckBoxGFC(
				"WorldBuilderRevealTileModeButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_REVEAL_TILE_MODE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10+36),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_REVEAL_TAB_MODE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				
			iButtonX = iButtonX + 35
			self.m_iDiplomacyCheckboxID = 5
			screen.addCheckBoxGFC(
				"WorldBuilderDiplomacyModeButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_DIPLOMACY_MODE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10+36),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_DIPLOMACY_MODE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
	
			iButtonX = 0
			self.m_iLandmarkCheckboxID = 6
			screen.addCheckBoxGFC(
				"WorldBuilderLandmarkButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_LANDMARK_MODE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_LANDMARK_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
	
			iButtonX = iButtonX + 35
			self.m_iEraseCheckboxID = 7
			screen.addCheckBoxGFC(
				"WorldBuilderEraseButton",	
				ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_ERASE").getPath(), 
				ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				(iMaxScreenWidth-self.iScreenWidth)+8+iButtonX,
				(10),
				iButtonWidth, 
				iButtonHeight, 
				WidgetTypes.WIDGET_WB_ERASE_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
	
			self.setCurrentModeCheckbox(self.m_iNormalPlayerCheckboxID)
			
		return

	def refreshSideMenu(self):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )

		iMaxScreenWidth = screen.getXResolution()
		iMaxScreenHeight = screen.getYResolution()
		iScreenHeight = 10+37+37 
		
		if (CyInterface().isInAdvancedStart()):
			
			iX = 50
			iY = 15
			szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_POINTS", (gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartPoints(), )) + "</font>"
			screen.setLabel("AdvancedStartPointsText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_COST_THIS_LOCATION", (self.m_iCost, )) + u"</font>"
			iY = 85
			screen.setLabel("AdvancedStartCostText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, iX-20, iY, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
		else:
	
			screen.deleteWidget("WorldBuilderPlayerChoice")
## Game Data ##
			screen.deleteWidget("WorldBuilderGameData")
			screen.deleteWidget("WorldBuilderAddUnits")
			screen.deleteWidget("WorldBuilderUnitCombat")
			screen.deleteWidget("WorldBuilderEditAreaMap")
			screen.deleteWidget("WorldBuilderModifyAreaPlotType")
			screen.deleteWidget("WorldBuilderModifyAreaTerrain")
			screen.deleteWidget("WorldBuilderModifyAreaRoute")
			screen.deleteWidget("WorldBuilderModifyAreaFeature")
## Game Data ##
			screen.deleteWidget("WorldBuilderBrushSize")
			screen.deleteWidget("WorldBuilderRegenerateMap")
			screen.deleteWidget("WorldBuilderTeamChoice")
	
			screen.deleteWidget("WorldBuilderRevealAll")
			screen.deleteWidget("WorldBuilderUnrevealAll")
			screen.deleteWidget("WorldBuilderRevealPanel")
			screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
	
			iPanelWidth = 35*6
			if self.m_bReveal:
				screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45 + 37, PanelStyles.PANEL_STYLE_MAIN )
			elif (self.m_bNormalPlayer and (not self.m_bUnitEdit) and (not self.m_bCityEdit)):
				if self.m_iUnitCombat > -2:
					screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45 + 37 * 3, PanelStyles.PANEL_STYLE_MAIN )
				else:
					screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45 + 37 * 2, PanelStyles.PANEL_STYLE_MAIN )	
			elif self.m_bNormalMap:
				if self.m_bChangeAllPlots:
					screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45 + 37 * 3, PanelStyles.PANEL_STYLE_MAIN )
				elif self.m_iArea == -1:
					screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45 + 37, PanelStyles.PANEL_STYLE_MAIN )
				else:
					if CyMap().getArea(self.m_iArea).isWater():
						screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45 + 37 * 3, PanelStyles.PANEL_STYLE_MAIN )
					else:
						screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45 + 37 * 5, PanelStyles.PANEL_STYLE_MAIN )
			else:
				screen.addPanel( "WorldBuilderBackgroundBottomPanel", "", "", True, True, iMaxScreenWidth-self.iScreenWidth, 10+32+32, self.iScreenWidth, 45, PanelStyles.PANEL_STYLE_MAIN )		
	
			if (self.m_bNormalPlayer and (not self.m_bUnitEdit) and (not self.m_bCityEdit)):
				szDropdownName = str("WorldBuilderPlayerChoice")
				screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
## Dead Player ##
				for i in xrange( gc.getMAX_PLAYERS() ):
					if ( gc.getPlayer(i).isEverAlive() ):
						strPlayerAliveStatus = gc.getPlayer(i).getName()
						if not gc.getPlayer(i).isAlive():
							strPlayerAliveStatus = strPlayerAliveStatus + " " + localText.getText("TXT_KEY_WB_DEAD",())
						if (i == self.m_iCurrentPlayer):
							screen.addPullDownString(szDropdownName, strPlayerAliveStatus, i, i, True )

						else:
							screen.addPullDownString(szDropdownName, strPlayerAliveStatus, i, i, False )
## Game Data Start##
				szDropdownName = str("WorldBuilderGameData")
				screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_PLAYER_DATA",()), 0, 0, True )
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_TEAM_DATA",()), 0, 0, True )
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_GAME_OPTION",()), 0, 0, True )
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_ADD_NEW_PLAYER",()), 0, 0, True )
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_EDIT_DATA",()), 0, 0, True )
## Adds Units Start ##
				szDropdownName = str("WorldBuilderAddUnits")
				screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_NO_CLASS",()), 0, 0, True )
				for i in xrange(gc.getNumUnitCombatInfos()):
					szPullDownString = gc.getUnitCombatInfo(i).getDescription()
					screen.addPullDownString(szDropdownName, szPullDownString, i, i, True )
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_ADD_UNITS",()), i, i, True )

				if self.m_iUnitCombat > -2:
					szDropdownName = str("WorldBuilderUnitCombat")
					screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					for i in xrange(gc.getNumUnitInfos()):
						if gc.getUnitInfo(i).getUnitCombatType() == self.m_iUnitCombat:
							szPullDownString = gc.getUnitInfo(i).getDescription()
							screen.addPullDownString(szDropdownName, szPullDownString, i, i, True )
					if self.m_iUnitCombat == -1:
						screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_NO_CLASS",()), i, i, True )
					else:
						screen.addPullDownString(szDropdownName, gc.getUnitCombatInfo(self.m_iUnitCombat).getDescription(), i, i, True )
## Adds Units Ends ##

			elif(self.m_bNormalMap and (not self.m_bUnitEdit) and (not self.m_bCityEdit)):
				iButtonWidth = 32
				iButtonHeight = 32
				iButtonX = 0
				iButtonY = 0
				screen.setImageButton( "WorldBuilderRegenerateMap", ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(), (iMaxScreenWidth-self.iScreenWidth)+8+iButtonX, (10+36+36), iButtonWidth, iButtonHeight, WidgetTypes.WIDGET_WB_REGENERATE_MAP, -1, -1)
	
				szDropdownName = str("WorldBuilderBrushSize")
				screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+48, (10+36+36), iPanelWidth-40, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				bActive = False
				if (self.m_iBrushWidth == 1):
					bActive = True
				else:
					bActive = False
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_1_BY_1",()), 1, 1, bActive )
				if (self.m_iBrushWidth == 2):
					bActive = True
				else:
					bActive = False
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_3_BY_3",()), 2, 2, bActive )
				if (self.m_iBrushWidth == 3):
					bActive = True
				else:
					bActive = False
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_5_BY_5",()), 3, 3, bActive )
## Edit Area Map Start##
				szDropdownName = str("WorldBuilderEditAreaMap")
				screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_PICK_AREA",()), 0, 0, True )
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_CHANGE_ALL_PLOTS",()), 1, 1, True )
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_EDIT_AREA",()), 2, 2, True )
				if self.m_iArea > -1 or  self.m_bChangeAllPlots:
					szDropdownName = str("WorldBuilderModifyAreaPlotType")
					screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_MOUNTAIN",()), 0, 0, True )
					screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_HILL",()), 0, 0, True )
					screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_LAND",()), 0, 0, True )
					screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_OCEAN",()), 0, 0, True )
					screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_CHANGE_PLOTTYPE",()), 0, 0, True )

					szDropdownName = str("WorldBuilderModifyAreaTerrain")
					screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
					for i in xrange(gc.getNumTerrainInfos()):
						if gc.getTerrainInfo(i).isGraphicalOnly(): continue
						if self.m_bChangeAllPlots:
							screen.addPullDownString(szDropdownName, gc.getTerrainInfo(i).getDescription(), 0, 0, True )
						elif CyMap().getArea(self.m_iArea).isWater() and gc.getTerrainInfo(i).isWater():
							screen.addPullDownString(szDropdownName, gc.getTerrainInfo(i).getDescription(), 0, 0, True )
						elif not CyMap().getArea(self.m_iArea).isWater() and not gc.getTerrainInfo(i).isWater():
							screen.addPullDownString(szDropdownName, gc.getTerrainInfo(i).getDescription(), 0, 0, True )
					screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_CHANGE_TERRAIN",()), 0, 0, True )

					if not CyMap().getArea(self.m_iArea).isWater() and not self.m_bChangeAllPlots:
						szDropdownName = str("WorldBuilderModifyAreaRoute")
						screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
						for i in xrange(gc.getNumRouteInfos()):
							screen.addPullDownString(szDropdownName, gc.getRouteInfo(i).getDescription(), 0, 0, True )
						screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_CLEAR_ALL",()), 0, 0, True )
						screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_CHANGE_ROUTE",()), 0, 0, True )

						szDropdownName = str("WorldBuilderModifyAreaFeature")
						screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36+36+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
						screen.addPullDownString(szDropdownName, gc.getFeatureInfo(gc.getInfoTypeForString("FEATURE_JUNGLE")).getDescription(), 0, 0, True )
						screen.addPullDownString(szDropdownName, gc.getFeatureInfo(gc.getInfoTypeForString("FEATURE_FOREST")).getDescription(), 0, 0, True )
						screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_CLEAR_ALL",()), 0, 0, True )
						screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_CHANGE_FEATURE",()), 0, 0, True )
## Edit Area Map Start ##
				
			elif(self.m_bReveal):
				iPanelWidth = 35*6
				iButtonWidth = 32
				iButtonHeight = 32
				iButtonX = 0
				iButtonY = 0
				screen.setImageButton( "WorldBuilderRevealAll", ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_REVEAL_ALL_TILES").getPath(), (iMaxScreenWidth-self.iScreenWidth)+8+iButtonX, (10+36+36), iButtonWidth, iButtonHeight, WidgetTypes.WIDGET_WB_REVEAL_ALL_BUTTON, -1, -1)
				iButtonX = iButtonX + 35
				screen.setImageButton( "WorldBuilderUnrevealAll", ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_UNREVEAL_ALL_TILES").getPath(), (iMaxScreenWidth-self.iScreenWidth)+8+iButtonX, (10+36+36), iButtonWidth, iButtonHeight, WidgetTypes.WIDGET_WB_UNREVEAL_ALL_BUTTON, -1, -1)
				iButtonX = iButtonX + 35
	
				szDropdownName = str("WorldBuilderBrushSize")
				screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8+80, (10+36+36), iPanelWidth-80, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				bActive = False
				if (self.m_iBrushWidth == 1):
					bActive = True
				else:
					bActive = False
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_1_BY_1",()), 1, 1, bActive )
				if (self.m_iBrushWidth == 2):
					bActive = True
				else:
					bActive = False
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_3_BY_3",()), 2, 2, bActive )
				if (self.m_iBrushWidth == 3):
					bActive = True
				else:
					bActive = False
				screen.addPullDownString(szDropdownName, localText.getText("TXT_KEY_WB_5_BY_5",()), 3, 3, bActive )
	
				szDropdownName = str("WorldBuilderTeamChoice")
				screen.addDropDownBoxGFC(szDropdownName, (iMaxScreenWidth-self.iScreenWidth)+8, (10+36+36+36), iPanelWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in range( gc.getMAX_CIV_TEAMS() ):
					if (gc.getTeam(i).isEverAlive()):
## Show Dead Team ##
						strName = gc.getTeam(i).getName()
						if not gc.getTeam(i).isAlive():
							strName = gc.getPlayer(gc.getTeam(i).getLeaderID()).getName() + " " + localText.getText("TXT_KEY_WB_DEAD",())
						if (i == self.m_iCurrentTeam):

							screen.addPullDownString(szDropdownName, strName, i, i, True )
						else:
							screen.addPullDownString(szDropdownName, strName, i, i, False )
## Show Dead Team ##
	
			else:
				screen.deleteWidget("WorldBuilderBackgroundBottomPanel")
	
		return

	def revealAll(self, bReveal):
		for i in range (CyMap().getGridWidth()):
			for j in range (CyMap().getGridHeight()):
				pPlot = CyMap().plot(i,j)
				if (not pPlot.isNone()):
					if bReveal or (not pPlot.isVisible(self.m_iCurrentTeam, False)):
						pPlot.setRevealed(self.m_iCurrentTeam, bReveal, False, -1);
		self.refreshReveal()
		return

	def RevealCurrentPlot(self, bReveal):
		if bReveal or (not self.m_pCurrentPlot.isVisible(self.m_iCurrentTeam, False)):
			self.m_pCurrentPlot.setRevealed(self.m_iCurrentTeam, bReveal, False, -1)
		return

	def showRevealed(self, pPlot):
		if (not pPlot.isRevealed(self.m_iCurrentTeam, False)):
			CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS, "COLOR_BLACK", 1.0)
		return

	def getNumPlayers(self):
		iCount = 0
		for i in range( gc.getMAX_CIV_PLAYERS() ):
			if ( gc.getPlayer(i).isEverAlive() ):
				iCount = iCount + 1

		return iCount

	def Exit(self):		
		CyInterface().setWorldBuilder(false)
		return

	def setLandmarkCB(self, szLandmark):
		self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
		CyEngine().addLandmarkPopup(self.m_pCurrentPlot) # , u"%s" %(szLandmark))
		return
		
	def removeLandmarkCB(self):
		self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
		CyEngine().removeLandmark(self.m_pCurrentPlot)
		return

	def refreshPlayerTabCtrl(self):
		
		initWBToolPlayerControl()
		
		self.m_normalPlayerTabCtrl = getWBToolNormalPlayerTabCtrl()

		self.m_normalPlayerTabCtrl.setNumColumns((gc.getNumUnitInfos()/10)+2);
		self.m_normalPlayerTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_UNITS",()));
		self.m_iUnitTabID = 0
		self.m_iNormalPlayerCurrentIndexes.append(0)

		self.m_normalPlayerTabCtrl.setNumColumns((gc.getNumBuildingInfos()/10)+1);
		self.m_normalPlayerTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_BUILDINGS",()));
		self.m_iBuildingTabID = 1
		self.m_iNormalPlayerCurrentIndexes.append(0)

		self.m_normalPlayerTabCtrl.setNumColumns((gc.getNumTechInfos()/10)+1);
		self.m_normalPlayerTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_TECHNOLOGIES",()));
		self.m_iTechnologyTabID = 2
		self.m_iNormalPlayerCurrentIndexes.append(0)
		
		addWBPlayerControlTabs()
		return

	def refreshAdvancedStartTabCtrl(self, bReuse):
		
		if (CyInterface().isInAdvancedStart()):
			
			if (self.m_advancedStartTabCtrl and bReuse):
				iActiveTab = self.m_advancedStartTabCtrl.getActiveTab()
				iActiveList = self.m_iAdvancedStartCurrentList[iActiveTab]
				iActiveIndex = self.m_iAdvancedStartCurrentIndexes[iActiveTab]
			else:
				iActiveTab = 0
				iActiveList = 0
				iActiveIndex = 0
			
			self.m_iCurrentPlayer = CyGame().getActivePlayer()
			self.m_iCurrentTeam = CyGame().getActiveTeam()
			self.m_iAdvancedStartCurrentIndexes = []
			self.m_iAdvancedStartCurrentList = []
			
			initWBToolAdvancedStartControl()
			
			self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()

			self.m_advancedStartTabCtrl.setNumColumns((gc.getNumBuildingInfos()/10)+2);
			self.m_advancedStartTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_AS_CITIES",()));
			self.m_iASCityTabID = 0
			self.m_iAdvancedStartCurrentIndexes.append(0)
			
			self.m_iASCityListID = 0
			self.m_iASBuildingsListID = 2
			self.m_iASAutomateListID = 1
			self.m_iAdvancedStartCurrentList.append(self.m_iASCityListID)

			self.m_advancedStartTabCtrl.setNumColumns((gc.getNumUnitInfos()/10)+2);
			self.m_advancedStartTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_AS_UNITS",()));
			self.m_iASUnitTabID = 1
			self.m_iAdvancedStartCurrentIndexes.append(0)
			
			self.m_iAdvancedStartCurrentList.append(0)
			self.m_iASUnitListID = 0

			self.m_advancedStartTabCtrl.setNumColumns((gc.getNumImprovementInfos()/10)+2);
			self.m_advancedStartTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_AS_IMPROVEMENTS",()));
			self.m_iASImprovementsTabID = 2
			self.m_iAdvancedStartCurrentIndexes.append(0)
			
			self.m_iASRoutesListID = 0
			self.m_iASImprovementsListID = 1
			self.m_iAdvancedStartCurrentList.append(self.m_iASRoutesListID)

			self.m_advancedStartTabCtrl.setNumColumns(1);
			self.m_advancedStartTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_AS_VISIBILITY",()));
			self.m_iASVisibilityTabID = 3
			self.m_iAdvancedStartCurrentIndexes.append(0)
			
			self.m_iAdvancedStartCurrentList.append(0)
			self.m_iASVisibilityListID = 0

			self.m_advancedStartTabCtrl.setNumColumns(1);
			self.m_advancedStartTabCtrl.addTabSection(localText.getText("TXT_KEY_WB_AS_TECH",()));
			self.m_iASTechTabID = 4
			self.m_iAdvancedStartCurrentIndexes.append(0)
			
			self.m_iAdvancedStartCurrentList.append(0)
			self.m_iASTechListID = 0
			
			addWBAdvancedStartControlTabs()

			self.m_advancedStartTabCtrl.setActiveTab(iActiveTab)
			self.setCurrentAdvancedStartIndex(iActiveIndex)
			self.setCurrentAdvancedStartList(iActiveList)
		else:
			
			self.m_advancedStartTabCtrl = getWBToolAdvancedStartTabCtrl()
			
			self.m_advancedStartTabCtrl.enable(false)
		
		return

	def eraseAll(self):
		# kill all units on plot if one is selected
		if (self.m_pCurrentPlot != 0):
			while (self.m_pCurrentPlot.getNumUnits() > 0):
				pUnit = self.m_pCurrentPlot.getUnit(0)
				pUnit.kill(false, PlayerTypes.NO_PLAYER)

			self.m_pCurrentPlot.setBonusType(-1)
			self.m_pCurrentPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)

			if (self.m_pCurrentPlot.isCity()):
				self.m_pCurrentPlot.getPlotCity().kill()

			self.m_pCurrentPlot.setRouteType(-1)
			self.m_pCurrentPlot.setNOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
			self.m_pCurrentPlot.setWOfRiver(False, CardinalDirectionTypes.NO_CARDINALDIRECTION)
			self.m_pCurrentPlot.setImprovementType(-1)
			self.removeLandmarkCB()
		return

## Edit Script ##
	def handleEditScriptCB ( self, argsList ) :
		strName = argsList[0]
		if strName == "UnitEditScript":
			self.m_pScript = self.m_pActivePlot.getUnit(self.m_iCurrentUnit)
		elif strName == "CityEditScript":
			self.m_pScript = self.m_pActivePlot.getPlotCity()
		elif strName == "PlayerEditScript":
			self.m_pScript = gc.getPlayer(self.m_iCurrentPlayer)
		elif strName == "PlotEditScript":
			self.m_pScript = self.m_pActivePlot
		self.getScript()
		return 1

	def getScript(self):
		CvEventInterface.beginEvent(CvUtil.EventWBScriptPopup)
		return

	def setScriptCB(self, szScript):
		if (self.m_pScript != -1):
			self.m_pScript.setScriptData(CvUtil.convertToStr(szScript))
			self.m_pScript = -1
			return

	def getCurrentScript(self):
		if (self.m_pScript != -1):
			return self.m_pScript.getScriptData()
## Edit Script ##

	def getNewStartYear(self):
		CvEventInterface.beginEvent(CvUtil.EventWBStartYearPopup)
		return

	def setStartYearCB(self, iStartYear):
		gc.getGame().setStartYear(iStartYear)
		return
		
	def setRiverHighlights(self):
		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY(), PlotStyles.PLOT_STYLE_RIVER_SOUTH, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_GREEN", 1)

		fAlpha = .2
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY()+1, PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()+1, PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY()+1, PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY(), PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)

		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY(), PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX()-1, self.m_pRiverStartPlot.getY()-1, PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX(), self.m_pRiverStartPlot.getY()-1, PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)
		CyEngine().addColoredPlotAlt(self.m_pRiverStartPlot.getX()+1, self.m_pRiverStartPlot.getY()-1, PlotStyles.PLOT_STYLE_BOX_FILL, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS, "COLOR_WHITE", fAlpha)
		return

	def setCurrentModeCheckbox(self, iButton):
		screen = CyGInterfaceScreen( "WorldBuilderScreen", CvScreenEnums.WORLDBUILDER_SCREEN )
		#print("iButton: %s" %(str(iButton)))

		#print("m_iUnitEditCheckboxID: %s" %(str(self.m_iUnitEditCheckboxID)))
		#print("m_iCityEditCheckboxID: %s" %(str(self.m_iCityEditCheckboxID)))
		#print("m_iNormalPlayerCheckboxID: %s" %(str(self.m_iNormalPlayerCheckboxID)))
		#print("m_iNormalMapCheckboxID: %s" %(str(self.m_iNormalMapCheckboxID)))
		#print("m_iRevealTileCheckboxID: %s" %(str(self.m_iRevealTileCheckboxID)))
		#print("m_iDiplomacyCheckboxID: %s" %(str(self.m_iDiplomacyCheckboxID)))

		if (iButton == self.m_iUnitEditCheckboxID):
			screen.setState("WorldBuilderUnitEditModeButton", True)
		else:
			screen.setState("WorldBuilderUnitEditModeButton", False)

		if (iButton == self.m_iCityEditCheckboxID):
			screen.setState("WorldBuilderCityEditModeButton", True)
		else:
			screen.setState("WorldBuilderCityEditModeButton", False)

		if (iButton == self.m_iNormalPlayerCheckboxID):
			screen.setState("WorldBuilderNormalPlayerModeButton", True)
		else:
			screen.setState("WorldBuilderNormalPlayerModeButton", False)

		if (iButton == self.m_iNormalMapCheckboxID):
			screen.setState("WorldBuilderNormalMapModeButton", True)
		else:
			screen.setState("WorldBuilderNormalMapModeButton", False)

		if (iButton == self.m_iRevealTileCheckboxID):
			screen.setState("WorldBuilderRevealTileModeButton", True)
		else:
			screen.setState("WorldBuilderRevealTileModeButton", False)

		if (iButton == self.m_iDiplomacyCheckboxID):
			screen.setState("WorldBuilderDiplomacyModeButton", True)
		else:
			screen.setState("WorldBuilderDiplomacyModeButton", False)

		if (iButton == self.m_iLandmarkCheckboxID):
			screen.setState("WorldBuilderLandmarkButton", True)
		else:
			screen.setState("WorldBuilderLandmarkButton", False)

		if (iButton == self.m_iEraseCheckboxID):
			screen.setState("WorldBuilderEraseButton", True)
		else:
			screen.setState("WorldBuilderEraseButton", False)

		return

	def initVars(self):
		self.m_normalPlayerTabCtrl = 0
		self.m_normalMapTabCtrl = 0
		self.m_tabCtrlEdit = 0
		self.m_bCtrlEditUp = False
		self.m_bUnitEdit = False
		self.m_bCityEdit = False
		self.m_bNormalPlayer = True
		self.m_bNormalMap = False
		self.m_bReveal = False
		self.m_bLandmark = False
		self.m_bEraseAll = False
		self.m_bUnitEditCtrl = False
		self.m_bCityEditCtrl = False
		self.m_bShowBigBrush = False
		self.m_bLeftMouseDown = False
		self.m_bRightMouseDown = False
		self.m_bChangeFocus = False
		self.m_iNormalPlayerCurrentIndexes = []
		self.m_iNormalMapCurrentIndexes = []
		self.m_iNormalMapCurrentList = []
		self.m_iCurrentPlayer = 0
		self.m_iCurrentTeam = 0
		self.m_iCurrentUnitPlayer = 0
		self.m_iCurrentUnit = 0
		self.m_iCurrentX = -1
		self.m_iCurrentY = -1
		self.m_pCurrentPlot = 0
		self.m_pActivePlot = 0
		self.m_pRiverStartPlot = -1
		self.m_iUnitTabID = -1
		self.m_iBuildingTabID = -1
		self.m_iTechnologyTabID = -1
		self.m_iImprovementTabID = -1
		self.m_iBonusTabID = -1
		self.m_iImprovementListID = -1
		self.m_iBonusListID = -1
		self.m_iTerrainTabID = -1
		self.m_iTerrainListID = -1
		self.m_iFeatureListID = -1
		self.m_iPlotTypeListID = -1
		self.m_iRouteListID = -1
		self.m_iTerritoryTabID = -1
		self.m_iTerritoryListID = -1
		self.m_iBrushSizeTabID = -1
		self.m_iBrushWidth = 1
		self.m_iBrushHeight = 1
		self.m_iUnitEditCheckboxID = -1
		self.m_iCityEditCheckboxID = -1
		self.m_iNormalPlayerCheckboxID = -1
		self.m_iNormalMapCheckboxID = -1
		self.m_iRevealTileCheckboxID = -1
		self.m_iDiplomacyCheckboxID = -1
		self.m_iLandmarkCheckboxID = -1
		self.m_iEraseCheckboxID = -1
		self.iScreenWidth = 228

## Platy Builder ##
		self.m_iNewCivilization = -1
		self.m_iNewLeaderType = -1
		self.m_iImprovement = 0
		self.m_iYield = 0
		self.m_iDomain = 0
		self.m_iRoute = 0
		self.m_iOtherPlayer = 0
		self.m_iOtherTeam = 0
		self.m_iMemory = 0
		self.m_pScript = -1
		self.m_bMoveUnit = False
		self.m_iUnitCombat = -2
		self.m_iUnitType = -1
		self.m_bPickArea = False
		self.m_bChangeAllPlots = False
		self.m_iArea = -1
## Platy Builder ##
		return
