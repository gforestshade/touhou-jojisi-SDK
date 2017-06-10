## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import time
import sre
import operator

import MonkeyTools as mt
import string
import CvConfigParser
import TradeResourcePanel
import CityInfoPanelPS
import CvUnitPlacementScreen
import AlertsLog
import Version
import CGEUtils
import SdToolKitAdvanced
import UserPrefs

##### <written by F> #####
#スペルインフォ読み込み
import SpellInfo
import TohoUnitList
import CvGameUtils

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

g_NumEmphasizeInfos = 0
g_NumCityTabTypes = 0
g_NumHurryInfos = 0
g_NumUnitClassInfos = 0
g_NumBuildingClassInfos = 0
g_NumProjectInfos = 0
g_NumProcessInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

MAX_SELECTED_TEXT = 5
MAX_DISPLAYABLE_BUILDINGS = 15
MAX_DISPLAYABLE_TRADE_ROUTES = 4
MAX_BONUS_ROWS = 10
MAX_CITIZEN_BUTTONS = 8

SELECTION_BUTTON_COLUMNS = 8
SELECTION_BUTTON_ROWS = 2
NUM_SELECTION_BUTTONS = SELECTION_BUTTON_ROWS * SELECTION_BUTTON_COLUMNS

g_iNumBuildingWidgets = MAX_DISPLAYABLE_BUILDINGS
g_iNumTradeRouteWidgets = MAX_DISPLAYABLE_TRADE_ROUTES

# END OF TURN BUTTON POSITIONS
######################
iEndOfTurnButtonSize = 32
iEndOfTurnPosX = 296 # distance from right
iEndOfTurnPosY = 147 # distance from bottom

# MINIMAP BUTTON POSITIONS
######################
iMinimapButtonsExtent = 228
iMinimapButtonsX = 227
iMinimapButtonsY_Regular = 160
iMinimapButtonsY_Minimal = 32
iMinimapButtonWidth = 24
iMinimapButtonHeight = 24

# Globe button
iGlobeButtonX = 48
iGlobeButtonY_Regular = 168
iGlobeButtonY_Minimal = 40
iGlobeToggleWidth = 48
iGlobeToggleHeight = 48

# GLOBE LAYER OPTION POSITIONING
######################
iGlobeLayerOptionsX  = 235
iGlobeLayerOptionsY_Regular  = 170# distance from bottom edge
iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
iGlobeLayerOptionsWidth = 400
iGlobeLayerOptionHeight = 24

# STACK BAR
#####################
iStackBarHeight = 27


# MULTI LIST
#####################
iMultiListXL = 318
iMultiListXR = 332
iMultiListXOffset = iMultiListXL+iMultiListXR + 68

# TOP CENTER TITLE
#####################
iCityCenterRow1X = 398
iCityCenterRow1Y = 78
iCityCenterRow2X = 398
iCityCenterRow2Y = 104

iCityCenterRow1Xa = 347
iCityCenterRow2Xa = 482


g_iNumTradeRoutes = 0
g_iNumBuildings = 0
g_iNumLeftBonus = 0
g_iNumCenterBonus = 0
g_iNumRightBonus = 0

g_szTimeText = ""
g_szOldTimeText = ""
g_iTimeTextCounter = 0

g_pSelectedUnit = 0

CFG_CIV_NAME_ON_SCOREBOARD = True
CFG_MASTER_NAME_ON_SCOREBOARD = True
CFG_RAWCOMMERCEDISPLAY = True
CFG_Specialist_Stacker = True
CFG_Combat_Experience_Counter = True
CFG_Unit_Statistics = False
CFG_Show_GameTurn_Bar = True
g_ShowGameTurnBarColor = -1
CFG_Enabled_Compress_Mode = True
CFG_Show_GreatPerson_Bar = True
CFG_Show_TopCultureCities = True

# < NJAGCM Start >
g_bAlternateTimeText = True
g_iAlternatingTime = 15
g_bShowTurns = True
g_bShowGameClock = True
g_bShowGameCompletedPercent = True
g_bShowGameCompletedTurns = False
g_bAlternateShowTurns = True
g_bAlternateShowGameClock = True
g_bAlternateShowGameCompletedPercent = False
g_bAlternateShowGameCompletedTurns = True
g_bShowEra = True
g_bShowReflectEraInTurnColor = True
g_eraTurnColorDictionary = {}
g_eraColor = "COLOR_WHITE"
g_eraText = ""
# < NJAGCM End >

# <STACKER START>
SPECIALIST_STACK_WIDTH = 9
g_bHighlightForcedSpecialists = True
g_bStackSuperSpecialists = True
MAX_SUPER_SPECIALIST_BUTTONS = 6
SUPER_SPECIALIST_STACK_WIDTH = 15
g_bDisplayUniqueSuperSpecialistsOnly = False
g_bDynamicSuperSpecialistsSpacing = True
g_bStackAngryCitizens = True
MAX_ANGRY_CITIZEN_BUTTONS = 6
ANGRY_CITIZEN_STACK_WIDTH = 15
g_bDynamicAngryCitizensSpacing = True
g_iSuperSpecialistCount = 0
g_iAngryCitizensCount = 0
# <STACKER END>

# < Dead Civ Scoreboard Mod Start >
g_bHideDeadCivilizations = False
g_bGreyOutDeadCivilizations = True
g_bShowDeadTag = True
# < Dead Civ Scoreboard Mod End >

# Advanced Plot List Globals
lAPLUnitList = set()
lAPLUnitListNOK = set()
listAPLButtons = dict()
listPrevAPLButtons = dict()
listPrevAPLUpgradeIndicator = dict()
listPrevAPLHealthBar = dict()
listPrevAPLSpotIcons = dict()

bAPLFilterModeWound		= True
bAPLFilterModeNotWound	= True
bAPLWoundSelectMode		= False
bAPLFilterModeAir		= True
bAPLFilterModeSea		= True
bAPLFilterModeLand		= True
bAPLFilterModeDom		= True
bAPLFilterModeMil		= True
bAPLFilterModeOwn		= True
bAPLFilterModeForeign	= True

iMaxPlotListIcons = 0
bShowPromoUpgrade = False
bShowWarlordIndicator = False
bShowActionIcons = False
bCompressShow = False
bCompressMode = False
bPrevCompMode = CFG_Enabled_Compress_Mode
APLCombatStrDict = dict()
iPercentWithGPBY = 75
GPBarText = u""
gCombatXPText = u""
g_iGameTurn = -1
g_BottomContIconSize = 48
gTopCivCultureText = u""
gTopCivCulturePos = 0
szGoldText = ""

# sre compile
removeTag = sre.compile(r'<font=.*?>|</font>|<color=.*?>|</color>|<link=.*?>|</link>')
removeLinks = sre.compile(r'<link=.*?>|</link>')
removeColor = sre.compile(r'<color=.*?>|</color>')

class CvMainInterface:
	"Main Interface Screen"

	def __init__(self):
		self.PLOT_LIST_MINUS_NAME	= "PlotListMinus"
		self.PLOT_LIST_PLUS_NAME	= "PlotListPlus"
		self.PLOT_LIST_UP_NAME		= "PlotListUp"
		self.PLOT_LIST_DOWN_NAME	= "PlotListDown"
		self.PLOT_LIST_PROMO_NAME	= "PlotListPromo"
		self.PLOT_LIST_UPGRADE_NAME	= "PlotListUpgrade"

		self.APL_MODE_MULTILINE		= "APL_MODE_MULTILINE1"
		self.APL_MODE_STACK_VERT	= "APL_MODE_STACK_VERT1"
		self.APL_MODE_STACK_HORIZ	= "APL_MODE_STACK_HORIZ1"

		self.APL_WOUND_SELECT		= "APL_WOUND_SELECT1"
		self.APL_FILTER_AIR			= "APL_FILTER_AIR1"
		self.APL_FILTER_SEA			= "APL_FILTER_SEA1"
		self.APL_FILTER_LAND		= "APL_FILTER_LAND1"
		self.APL_FILTER_DOM			= "APL_FILTER_DOM1"
		self.APL_FILTER_MIL			= "APL_FILTER_MIL1"

		self.APL_PROMO_BUTTONS_UNITINFO = "APL_PROMO_BUTTONS_UNITINFO"

		self.APL_GRP_UNITTYPE	= "APL_GRP_UNITTYPE1"
		self.APL_GRP_GROUPS		= "APL_GRP_GROUPS1"
		self.APL_GRP_PROMO		= "APL_GRP_PROMO1"
		self.APL_GRP_UPGRADE	= "APL_GRP_UPGRADE1"

		self.MainInterfaceInputMap = {
			"PlotListButton"			: self.getPlotListButtonName,
			self.PLOT_LIST_MINUS_NAME	: self.getPlotListMinusName,
			self.PLOT_LIST_PLUS_NAME	: self.getPlotListPlusName,
			self.PLOT_LIST_UP_NAME		: self.getPlotListUpName,
			self.PLOT_LIST_DOWN_NAME	: self.getPlotListDownName,
			self.APL_WOUND_SELECT		: self.setAPLWoundSelect,
			self.APL_FILTER_AIR			: self.setAPLFilterAir,
			self.APL_FILTER_SEA			: self.setAPLFilterSea,
			self.APL_FILTER_LAND		: self.setAPLFilterLand,
			self.APL_FILTER_DOM			: self.setAPLFilterDom,
			self.APL_FILTER_MIL			: self.setAPLFilterMil,
			self.PLOT_LIST_PROMO_NAME	: self.unitPromotion,
			self.PLOT_LIST_UPGRADE_NAME	: self.unitUpgrade,
		}

		self.iColOffset		= 0
		self.iRowOffset		= 0
		self.pOldPlot 		= 0
		self.sAPLMode		= self.APL_MODE_MULTILINE
		self.nAPLGrpMode	= self.APL_GRP_UNITTYPE
		self.bAPLSelectOnly = False

		self.bAPLHide		= False

		self.lFilteredUnitList = []
		self.dUnitPromoList		= {}
		self.dUnitUpgradeList	= {}

		self.tLastMousePos		= (0, 0, 0, 0)
		self.bInfoPaneActive	= False

		self.xResolution = 0
		self.yResolution = 0

	def getMaxCol(self):
		return ((self.xResolution - iMultiListXOffset) / 38)

	def getMaxRow(self):
		return int((self.yResolution - 160) / 66) # (self.yResolution - 160) / 44) * 2/3

	def getRow(self, i):
		return i / ((self.xResolution - iMultiListXOffset) / 38)#self.getMaxCol()

	def getCol(self, i):
		return i % ((self.xResolution - iMultiListXOffset) / 38)#self.getMaxCol()

	def getX(self, nCol):
		return 315 + (nCol * 36)

	def getY(self, nRow):
		return self.yResolution - 179 - (nRow * 44) 

	# APL Mode Switcher functions
	def setAPLWoundSelect(self, inputClass):
		global bAPLWoundSelectMode

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.hideInfoPane()
			bAPLWoundSelectMode = not bAPLWoundSelectMode
			screen.setState(self.APL_WOUND_SELECT, bAPLWoundSelectMode)
			return 1

	# APL Mode Switcher functions
	def setAPLFilterAir(self, inputClass):
		global bAPLFilterModeAir
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.hideInfoPane()
			bAPLFilterModeAir = not bAPLFilterModeAir
			screen.setState(self.APL_FILTER_AIR, not bAPLFilterModeAir)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1

	# APL Mode Switcher functions
	def setAPLFilterSea(self, inputClass):
		global bAPLFilterModeSea
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.hideInfoPane()
			bAPLFilterModeSea = not bAPLFilterModeSea
			screen.setState(self.APL_FILTER_SEA, not bAPLFilterModeSea)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1

	# APL Mode Switcher functions
	def setAPLFilterLand(self, inputClass):
		global bAPLFilterModeLand
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.hideInfoPane()
			bAPLFilterModeLand = not bAPLFilterModeLand
			screen.setState(self.APL_FILTER_LAND, not bAPLFilterModeLand)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1

	# APL Mode Switcher functions
	def setAPLFilterDom(self, inputClass):
		global bAPLFilterModeDom
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.hideInfoPane()
			bAPLFilterModeDom = not bAPLFilterModeDom
			screen.setState(self.APL_FILTER_DOM, not bAPLFilterModeDom)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1

	# APL Mode Switcher functions
	def setAPLFilterMil(self, inputClass):
		global bAPLFilterModeMil
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.hideInfoPane()
			bAPLFilterModeMil = not bAPLFilterModeMil
			screen.setState(self.APL_FILTER_MIL, not bAPLFilterModeMil)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1

	# handles the unit promotion button inputs
	def unitPromotion(self, inputClass):
		id = inputClass.getID()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON):
			if (not CyInterface().isCityScreenUp()):
				self.showPromoInfoPane(id)
			return 1
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			self.hidePromoInfoPane()
			return 1
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			self.doPromotion(id)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0

	# Arrow Up
	def getPlotListUpName(self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			self.iRowOffset += 1
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0

	# Arrow Down
	def getPlotListDownName(self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.iRowOffset > 0):
				self.iRowOffset -= 1
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0

	# Arrow Left
	def getPlotListMinusName(self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.iColOffset > 0):
				self.iColOffset -= 1
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0

	# Arrow Right
	def getPlotListPlusName(self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			self.iColOffset += 1
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0

	# determines the unit button
	def getPlotListButtonName(self, inputClass):
		global bCompressMode

		iNotifyCode = inputClass.getNotifyCode()
		getKeyEvent = CvEventInterface.getEventManager()
		if (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_ON):
			id = inputClass.getID()
			if (not CyInterface().isCityScreenUp()):
				if (bCompressMode):
					self.showCompactUnitInfoPane(id)
				else:
					self.showUnitInfoPane(id)
			return 1
		elif (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			self.hideUnitInfoPane()
			return 1
		elif (iNotifyCode == NotifyCode.NOTIFY_CLICKED):
			id = inputClass.getID()
			if (0 <= id <= iMaxPlotListIcons):
				if (bCompressMode):
					bCompressMode = False
					self.hideUnitInfoPane()
					if (not CyInterface().isCityScreenUp()):
						(iOwner, iUnitType) = listAPLButtons[id]
						self.checkDisplayFilterUnitList(False, False)
						for (iLoopOwner, iLoopID, _, _) in self.lFilteredUnitList:
							pLoopUnit = gc.getPlayer(iLoopOwner).getUnit(iLoopID)
							if (iOwner == iLoopOwner and iUnitType == pLoopUnit.getUnitType()):
								CyInterface().selectGroup(pLoopUnit, False, False, False)
								break
				else:
					self.hideUnitInfoPane()
					(iOwner, iID) = listAPLButtons[id]
					CGEUtils.CGEUtils().showAutoReconTargetPlot(iID)
					self.selectGroup(id, getKeyEvent.bShift, getKeyEvent.bCtrl, getKeyEvent.bAlt)
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0

	# handles the unit upgrade button inputs
	def unitUpgrade(self, inputClass):
		id = inputClass.getID()
		iNotifyCode = inputClass.getNotifyCode()
		if (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_ON):
			if not CyInterface().isCityScreenUp():
				self.showUpgradeInfoPane(id)
			return 1
		elif (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			self.hideUpgradeInfoPane()
			return 1
		elif (iNotifyCode == NotifyCode.NOTIFY_CLICKED):
			self.hideUpgradeInfoPane()
			self.doUpgrade(id)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0

	# APL Mode Select
	def showAPLModeSelect(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screen.addPanel("APLModeSelectBackground", u"", u"", True, False, 315, self.yResolution - 210, 200, 110, PanelStyles.PANEL_STYLE_MAIN)
		screen.show("APLModeSelectBackground")
		screen.addTableControlGFC("APLModeSelectList", 1, 330, self.yResolution - 190, 170, 74, False, False, 20, 20, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("APLModeSelectList", True)
		screen.setStyle("APLModeSelectList", "Table_StandardCiv_Style")
		screen.setTableColumnHeader("APLModeSelectList", 0, "", 170)
		iRow = screen.appendTableRow("APLModeSelectList")
		screen.setTableText("APLModeSelectList", 0, iRow, u"<font=3>%s</font>"%("Multi Line Mode"), ArtFileMgr.getInterfaceArtInfo("APL_MULTI_MODE").getPath(), WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		iRow = screen.appendTableRow("APLModeSelectList")
		screen.setTableText("APLModeSelectList", 0, iRow, u"<font=3>%s</font>"%("Vertical Mode"), ArtFileMgr.getInterfaceArtInfo("APL_VERT_MODE").getPath(), WidgetTypes.WIDGET_GENERAL, 1, 1, CvUtil.FONT_LEFT_JUSTIFY)
		iRow = screen.appendTableRow("APLModeSelectList")
		screen.setTableText("APLModeSelectList", 0, iRow, u"<font=3>%s</font>"%("Horizontal Mode"), ArtFileMgr.getInterfaceArtInfo("APL_HORIZ_MODE").getPath(), WidgetTypes.WIDGET_GENERAL, 2, 2, CvUtil.FONT_LEFT_JUSTIFY)

		if (self.sAPLMode == self.APL_MODE_MULTILINE):
			screen.selectRow("APLModeSelectList", 0, True)
		elif (self.sAPLMode == self.APL_MODE_STACK_VERT):
			screen.selectRow("APLModeSelectList", 1, True)
		elif (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			screen.selectRow("APLModeSelectList", 2, True)

	def hideAPLModeSelect(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screen.hide("APLModeSelectBackground")
		screen.hide("APLModeSelectList")


	def setAPLMode(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		if (self.sAPLMode == self.APL_MODE_MULTILINE):
			szFile = ArtFileMgr.getInterfaceArtInfo("APL_MULTI_MODE").getPath()
		elif (self.sAPLMode == self.APL_MODE_STACK_VERT):
			szFile = ArtFileMgr.getInterfaceArtInfo("APL_VERT_MODE").getPath()
		elif (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			szFile = ArtFileMgr.getInterfaceArtInfo("APL_HORIZ_MODE").getPath()
		else:
			szFile = ""
		screen.changeImageButton("APLModeSelect", szFile)

	# APL Mode Select
	def showAPLGrpModeSelect(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screen.addPanel("APLGrpModeSelectBackground", u"", u"", True, False, 345, self.yResolution - 230, 200, 135, PanelStyles.PANEL_STYLE_MAIN)
		screen.show("APLGrpModeSelectBackground")
		screen.addTableControlGFC("APLGrpModeSelectList", 1, 360, self.yResolution - 210, 170, 98, False, False, 20, 20, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("APLGrpModeSelectList", True)
		screen.setStyle("APLGrpModeSelectList", "Table_StandardCiv_Style")
		screen.setTableColumnHeader("APLGrpModeSelectList", 0, "", 170)
		iRow = screen.appendTableRow("APLGrpModeSelectList")
		screen.setTableText("APLGrpModeSelectList", 0, iRow, u"<font=3>%s</font>"%("Unit Type Mode"), ArtFileMgr.getInterfaceArtInfo("APL_UNITTYPE_MODE").getPath(), WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		iRow = screen.appendTableRow("APLGrpModeSelectList")
		screen.setTableText("APLGrpModeSelectList", 0, iRow, u"<font=3>%s</font>"%("Group Mode"), ArtFileMgr.getInterfaceArtInfo("APL_GROUP_MODE").getPath(), WidgetTypes.WIDGET_GENERAL, 1, 1, CvUtil.FONT_LEFT_JUSTIFY)
		iRow = screen.appendTableRow("APLGrpModeSelectList")
		screen.setTableText("APLGrpModeSelectList", 0, iRow, u"<font=3>%s</font>"%("Promotion Mode"), ArtFileMgr.getInterfaceArtInfo("APL_PROMO_MODE").getPath(), WidgetTypes.WIDGET_GENERAL, 2, 2, CvUtil.FONT_LEFT_JUSTIFY)
		iRow = screen.appendTableRow("APLGrpModeSelectList")
		screen.setTableText("APLGrpModeSelectList", 0, iRow, u"<font=3>%s</font>"%("Upgrade Mode"), ArtFileMgr.getInterfaceArtInfo("APL_UPGRADE_MODE").getPath(), WidgetTypes.WIDGET_GENERAL, 3, 3, CvUtil.FONT_LEFT_JUSTIFY)

		if (self.nAPLGrpMode == self.APL_GRP_UNITTYPE):
			screen.selectRow("APLGrpModeSelectList", 0, True)
		elif (self.nAPLGrpMode == self.APL_GRP_GROUPS):
			screen.selectRow("APLGrpModeSelectList", 1, True)
		elif (self.nAPLGrpMode == self.APL_GRP_PROMO):
			screen.selectRow("APLGrpModeSelectList", 2, True)
		elif (self.nAPLGrpMode == self.APL_GRP_UPGRADE):
			screen.selectRow("APLGrpModeSelectList", 3, True)

	def hideAPLGrpModeSelect(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screen.hide("APLGrpModeSelectBackground")
		screen.hide("APLGrpModeSelectList")

	def setAPLGrpMode(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		if (self.nAPLGrpMode == self.APL_GRP_UNITTYPE):
			szFile = ArtFileMgr.getInterfaceArtInfo("APL_UNITTYPE_MODE").getPath()
		elif (self.nAPLGrpMode == self.APL_GRP_GROUPS):
			szFile = ArtFileMgr.getInterfaceArtInfo("APL_GROUP_MODE").getPath()
		elif (self.nAPLGrpMode == self.APL_GRP_PROMO):
			szFile = ArtFileMgr.getInterfaceArtInfo("APL_PROMO_MODE").getPath()
		elif (self.nAPLGrpMode == self.APL_GRP_UPGRADE):
			szFile = ArtFileMgr.getInterfaceArtInfo("APL_UPGRADE_MODE").getPath()
		screen.changeImageButton("APLGrpModeSelect", szFile)

	# displayes the plot list switches (views, filters, groupings)
	def showPlotListButtonObjects(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# show APL filter switches
		screen.show(self.APL_WOUND_SELECT)

		screen.show(self.APL_FILTER_AIR)
		screen.show(self.APL_FILTER_SEA)
		screen.show(self.APL_FILTER_LAND)

		screen.show(self.APL_FILTER_DOM)
		screen.show(self.APL_FILTER_MIL)

		screen.show("APLModeSelect")
		screen.show("APLGrpModeSelect")
		screen.show("APLFilterBackground")

		self.bAPLHide = False

	# hides all plot list objects
	def hidePlotListButtons(self):
		global bShowPromoUpgrade
		global bShowWarlordIndicator
		global bShowActionIcons
		global bCompressShow
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screenHide = screen.hide

		# hide horizontal scroll buttons
		screen.hide(self.PLOT_LIST_MINUS_NAME)
		screen.hide(self.PLOT_LIST_PLUS_NAME)
		# hide vertical scroll buttons
		screen.hide(self.PLOT_LIST_UP_NAME)
		screen.hide(self.PLOT_LIST_DOWN_NAME)

		# hides all unit button objects
		for i in listAPLButtons.keys():
			# hide unit button
			szString = "PlotListButton" + str(i)
			# hide colored spot
			screenHide(szString + "Icon")
			# hide health bar
			screenHide(szString + "Health")
			# hide upgrade arrow
			screenHide(szString + "Upgrade")
			screenHide(szString)

		# hide warlord icon
		if (bShowWarlordIndicator):
			for i in listAPLButtons.keys():
				screenHide("PlotListButton" + str(i) + "Warlord")
			bShowWarlordIndicator = False

		# hide mission info
		if (bShowActionIcons):
			for i in listAPLButtons.keys():
				screenHide("PlotListButton" + str(i) + "Action")
			bShowActionIcons = False

		# hide compress mode items
		if (bCompressShow):
			for i in listAPLButtons.keys():
				screenHide("PlotListButton" + str(i) + "Num")
			bCompressShow = False

		# hides all promotion an upgrade button objects
		if (bShowPromoUpgrade):
			MaxRow = self.getMaxRow() + 1
			for nCol in xrange(self.getMaxCol() + 1):
				for nRow in xrange(MaxRow):
					# hide promotion button
					screenHide(self.PLOT_LIST_PROMO_NAME + "%02d%02d"%(nRow, nCol))
					# hide upgrade button
					screenHide(self.PLOT_LIST_UPGRADE_NAME + "%02d%02d"%(nRow, nCol))
			bShowPromoUpgrade = False

	# hides all plot list switches (views, filters, groupings)
	def hidePlotListButtonObjects(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# hide APL filter switches
		screen.hide(self.APL_WOUND_SELECT)
		screen.hide(self.APL_FILTER_AIR)
		screen.hide(self.APL_FILTER_SEA)
		screen.hide(self.APL_FILTER_LAND)
		screen.hide(self.APL_FILTER_DOM)
		screen.hide(self.APL_FILTER_MIL)

		screen.hide("APLModeSelect")
		screen.hide("APLGrpModeSelect")
		screen.hide("APLFilterBackground")

		self.bAPLHide = True

	# prepares the display of the mode, view, grouping, filter  switches
	def preparePlotListObjects(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		xResolution = self.xResolution
		yResolution = self.yResolution

		# APL Mode Select
		screen.setImageButton("APLModeSelect", "", 300, yResolution - 140, 28, 28, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.hide("APLModeSelect")
		screen.setStyle("APLModeSelect", "Button_HUDSmall_Style")

		# APL Group Mode Select
		screen.setImageButton("APLGrpModeSelect", "", 330, yResolution - 140, 28, 28, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.hide("APLGrpModeSelect")
		screen.setStyle("APLGrpModeSelect", "Button_HUDSmall_Style")

		# APL Filter Select
		screen.addPanel("APLFilterBackground", u"", u"", True, False, 360, self.yResolution - 146, 215, 36, PanelStyles.PANEL_STYLE_MAIN)
		screen.hide("APLFilterBackground")

		iY = yResolution - 138
		nXOff	= 377
		nDist	= 26
		nBSize	= 24

		# place the APL mode switches
		szString = self.APL_WOUND_SELECT
		screen.addCheckBoxGFC(szString, ArtFileMgr.getInterfaceArtInfo("APL_WOUND_SELECT").getPath(), ArtFileMgr.getInterfaceArtInfo("APL_WOUND_SELECT_HILITE").getPath(), nXOff, iY -1, nBSize, nBSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.hide(szString)

		# place the APL domain filter switches
		nXOff += int(nDist*1.5)
		szString = self.APL_FILTER_AIR
		screen.addCheckBoxGFC(szString, ArtFileMgr.getInterfaceArtInfo("APL_AIR").getPath(), ArtFileMgr.getInterfaceArtInfo("APL_FILTER_OVERLAY").getPath(), nXOff, iY, nBSize, nBSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.hide(szString)

		nXOff += nDist
		szString = self.APL_FILTER_SEA
		screen.addCheckBoxGFC(szString, ArtFileMgr.getInterfaceArtInfo("APL_SEA").getPath(), ArtFileMgr.getInterfaceArtInfo("APL_FILTER_OVERLAY").getPath(), nXOff, iY, nBSize, nBSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.hide(szString)

		nXOff += nDist
		szString = self.APL_FILTER_LAND
		screen.addCheckBoxGFC(szString, ArtFileMgr.getInterfaceArtInfo("APL_LAND").getPath(), ArtFileMgr.getInterfaceArtInfo("APL_FILTER_OVERLAY").getPath(), nXOff, iY, nBSize, nBSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.hide(szString)

		# place the APL unittype filter switches
		nXOff += int(nDist*1.5)
		szString = self.APL_FILTER_DOM
		screen.addCheckBoxGFC(szString, ArtFileMgr.getInterfaceArtInfo("APL_DOMESTIC").getPath(), ArtFileMgr.getInterfaceArtInfo("APL_FILTER_OVERLAY").getPath(), nXOff, iY, nBSize, nBSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.hide(szString)

		nXOff += nDist
		szString = self.APL_FILTER_MIL
		screen.addCheckBoxGFC(szString, ArtFileMgr.getInterfaceArtInfo("APL_MILITARY").getPath(), ArtFileMgr.getInterfaceArtInfo("APL_FILTER_OVERLAY").getPath(), nXOff, iY, nBSize, nBSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.hide(szString)

	# deselects all units in the plot list
	def deselectAll(self, pPlot):
		global lAPLUnitList
		lAPLUnitList = set()
		UnitListadd = lAPLUnitList.add
		for i in xrange(pPlot.getNumUnits()):
			pLoopUnit = pPlot.getUnit(i)
			UnitListadd((pLoopUnit.getOwner(), pLoopUnit.getID()))
			if (pLoopUnit.IsSelected()):
				CyInterface().selectUnit(pLoopUnit, True, True, False)

	def saveFilteredUnits(self, bShift, bHurt):
		global lAPLUnitListNOK

		self.checkDisplayFilterUnitList(True, bHurt)
		lAPLUnitListNOK = lAPLUnitList.difference(set([(iOwner, iID) for (iOwner, iID, _, _) in self.lFilteredUnitList]))
		if bShift:
			lTempListNOK = lAPLUnitListNOK.copy()
			APLUnitListNOKremove = lAPLUnitListNOK.remove
			for (iOwner, iID) in lTempListNOK:
				pLoopUnitNOK = gc.getPlayer(iOwner).getUnit(iID)
				if (pLoopUnitNOK.IsSelected()):
					APLUnitListNOKremove((iOwner, iID))

	def deSelectUnit(self):
		global lAPLUnitListNOK
		for (iOwner, iID) in lAPLUnitListNOK:
			pLoopUnit = gc.getPlayer(iOwner).getUnit(iID)
			if (pLoopUnit.IsSelected()):
				CyInterface().removeFromSelectionList(pLoopUnit)
		lAPLUnitListNOK.clear()

	def getAllUnitList(self, pPlot):
		global lAPLUnitList
		lAPLUnitList = set()
		for i in xrange(pPlot.getNumUnits()):
			pLoopUnit = pPlot.getUnit(i)
			if (pLoopUnit):
				lAPLUnitList.add((pLoopUnit.getOwner(), pLoopUnit.getID()))

	# replacement of the civ 4 version
	def selectGroup(self, iID, bShift, bCtrl, bAlt):
		(iOwner, iUnitID) = listAPLButtons[iID]
		pUnit = gc.getPlayer(iOwner).getUnit(iUnitID)
		if (not (bShift or bCtrl or bAlt)):
			# save act selection
			CyInterface().selectGroup(pUnit, False, False, False)
			self.bAPLSelectOnly = True
		elif (bShift and (not (bCtrl or bAlt))):
			CyInterface().selectGroup(pUnit, True, False, False)
			self.bAPLSelectOnly = True
		elif (bCtrl and (not (bShift or bAlt))):
			self.deselectAll(pUnit.plot())
			self.saveFilteredUnits(False, pUnit.isHurt())
			CyInterface().selectGroup(pUnit, False, True, False)
			self.deSelectUnit()
			self.bAPLSelectOnly = True
		elif (bCtrl and bShift and (not bAlt)):
			self.getAllUnitList(pUnit.plot())
			self.saveFilteredUnits(True, pUnit.isHurt())
			CyInterface().selectGroup(pUnit, True, True, False)
			self.deSelectUnit()
			self.bAPLSelectOnly = True
		elif (bAlt and (not (bCtrl or bShift))):
			self.deselectAll(pUnit.plot())
			self.saveFilteredUnits(False, pUnit.isHurt())
			CyInterface().selectUnit(pUnit, True, True, False)
			CyInterface().selectGroup(pUnit, True, False, True)
			self.deSelectUnit()
			self.bAPLSelectOnly = True
		# check if the unit has been selected from the city screen
		# if we came from city screen -> focus view on the selected unit
		if (CyInterface().isCityScreenUp()):
			CyCamera().JustLookAtPlot(pUnit.plot())

	# checks if the unit matches actual filter conditions
	def checkDisplayFilterUnitList(self, bSelect, bHurt):
		bGroupMode = (self.nAPLGrpMode == self.APL_GRP_GROUPS)
		bWoundSelect = (bSelect and bAPLWoundSelectMode)
		self.lFilteredUnitList = []
		tempUnitListappend = self.lFilteredUnitList.append
		GetUnit = CyInterface().getCachedInterfacePlotUnit

		if ((self.nAPLGrpMode == self.APL_GRP_UNITTYPE or bGroupMode) and (not bSelect) and bAPLFilterModeAir and bAPLFilterModeSea and bAPLFilterModeLand and bAPLFilterModeDom and bAPLFilterModeMil):
			for i in xrange(CyInterface().getNumCachedInterfacePlotUnits()):
				pLoopUnit = GetUnit(i)
				if (pLoopUnit):
					if (pLoopUnit.isCargo()):
						tempUnitListappend((pLoopUnit.getOwner(), pLoopUnit.getID(), pLoopUnit.getTransportUnit().getUnitType(), -pLoopUnit.getTransportUnit().getGroupID()))
					else:
						tempUnitListappend((pLoopUnit.getOwner(), pLoopUnit.getID(), pLoopUnit.getUnitType(), -pLoopUnit.getGroupID()))
			if (bGroupMode):
				self.lFilteredUnitList.sort(key = operator.itemgetter(3))
			return

		bPromoMode = (self.nAPLGrpMode == self.APL_GRP_PROMO)
		bUpgradeMode = (self.nAPLGrpMode == self.APL_GRP_UPGRADE)
		for i in xrange(CyInterface().getNumCachedInterfacePlotUnits()):
			pLoopUnit = GetUnit(i)
			if (pLoopUnit):

				pTempUnit = pLoopUnit
				# in case of Promotion or Upgrade Display
				if (bPromoMode and (not pLoopUnit.isPromotionReady())):
					continue
				elif (bUpgradeMode and (not mt.checkAnyUpgrade(pLoopUnit))):
					continue
				elif (pLoopUnit.isCargo()):
					# in case the unit is a cargo unit, the decision is made by the tranporting unit.
					# that ensures, that cargo is always displayed or not displayed together with its tranporting unit
					pTempUnit = pLoopUnit.getTransportUnit()
					if (bPromoMode and (not pTempUnit.isPromotionReady())):
						continue
					elif (bUpgradeMode and (not mt.checkAnyUpgrade(pTempUnit))):
						continue

				bFilterOK = False

				if (bWoundSelect):
					if (pTempUnit.isHurt()):
						# unit wounded and filter active
						bFilterOK = bHurt
					else:
						# unit not wounded and filter active
						bFilterOK = not bHurt
				else:
					bFilterOK = True

				if bFilterOK:
					pUnitTypeInfo = gc.getUnitInfo(pTempUnit.getUnitType())
					UnitDomainType = pUnitTypeInfo.getDomainType()

					# is unit a air unit and filter active
					if ((UnitDomainType == DomainTypes.DOMAIN_AIR and bAPLFilterModeAir) or \
						(UnitDomainType == DomainTypes.DOMAIN_SEA and bAPLFilterModeSea) or \
						(((UnitDomainType == DomainTypes.DOMAIN_LAND) or (UnitDomainType == DomainTypes.DOMAIN_IMMOBILE)) and bAPLFilterModeLand)):
						# is unit a domestic unit and filter active (domestic means -> no Combat or AirCombat values!
						# is unit a combat unit and filter active (combat means -> Combat or AirCombat values > 0!
						if ((bAPLFilterModeDom and (pUnitTypeInfo.getCombat() == 0) and (pUnitTypeInfo.getAirCombat() == 0)) or \
							(bAPLFilterModeMil and ((pUnitTypeInfo.getCombat() > 0) or (pUnitTypeInfo.getAirCombat() > 0)))):
							tempUnitListappend((pLoopUnit.getOwner(), pLoopUnit.getID(), pTempUnit.getUnitType(), -pTempUnit.getGroupID()))

		if (bGroupMode):
			self.lFilteredUnitList.sort(key = operator.itemgetter(3))
		return

	# displayes all the possible promotion buttons for a unit
	def displayUnitPromos(self, iOwner, iID, nRow, nCol):
		global bShowPromoUpgrade
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		lPromos = mt.getPossiblePromos(gc.getPlayer(iOwner).getUnit(iID))
		bPLHORIZMode = (self.sAPLMode == self.APL_MODE_STACK_HORIZ)
		# determine which dimension is the unit and which the promotion
		if (bPLHORIZMode):
			iU = nRow
		else:
			iU = nCol
		# display the promotions
		for iPromo in lPromos:
			if (bPLHORIZMode):
				nCol += 1
				iP = nCol
			else:
				nRow += 1
				iP = nRow
			x = self.getX(nCol)
			y = self.getY(nRow)

			szStringUnitPromo = "%s%02d%02d"%(self.PLOT_LIST_PROMO_NAME, iU, iP)
			szFileNamePromo = gc.getPromotionInfo(iPromo).getButton()
			screen.setImageButton(szStringUnitPromo, szFileNamePromo, x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, gc.getPromotionInfo(iPromo).getActionInfoIndex(), -1)
			screen.show(szStringUnitPromo)
			bShowPromoUpgrade = True
		self.dUnitPromoList[iU] = lPromos
		return

	# performs the units promotion
	def doPromotion(self, id):
		idPromo = id % 100
		idUnit1 = id / 100
		idUnit2 = idUnit1
		if (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			idUnit1 = idUnit1 * self.getMaxCol()
		(iOwner, iID) = listAPLButtons[idUnit1]
		pUnit = gc.getPlayer(iOwner).getUnit(iID)
		iPromo = self.dUnitPromoList[idUnit2][idPromo-1]

		pUnit.promote(iPromo, -1)

	# displayes all the possible upgrade buttons for a unit
	def displayUnitUpgrades(self, iOwner, iID, nRow, nCol):
		global bShowPromoUpgrade
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		lUpgrades = []
		pUnit = gc.getPlayer(iOwner).getUnit(iID)

		# reading all upgrades
		lUpgrades = mt.getPossibleUpgrades(pUnit)
		bPLHORIZMode = (self.sAPLMode == self.APL_MODE_STACK_HORIZ)

		# determine which dimension is the unit and which the upgrade
		if (bPLHORIZMode):
			iU = nRow
		else:
			iU = nCol

		# displaying the results
		for iUnitIndex in lUpgrades:
			if (bPLHORIZMode):
				nCol += 1
				iP = nCol
			else:
				nRow += 1
				iP = nRow
			x = self.getX(nCol)
			y = self.getY(nRow)

			szStringUnitUpgrade = "%s%02d%02d"%(self.PLOT_LIST_UPGRADE_NAME, iU, iP)
			szFileNameUpgrade = gc.getUnitInfo(iUnitIndex).getButton()
			screen.setImageButton(szStringUnitUpgrade, szFileNameUpgrade, x, y, 34, 34, WidgetTypes.WIDGET_GENERAL, iUnitIndex, -1)

			screen.enable(szStringUnitUpgrade, pUnit.canUpgrade(iUnitIndex, False))
			screen.show(szStringUnitUpgrade)
			bShowPromoUpgrade = True
		self.dUnitUpgradeList[iU] = lUpgrades
		return

	# performs the unit upgrades
	def doUpgrade(self, id):
		idUpgrade	= id % 100
		idUnit1		= id / 100
		idUnit2		= idUnit1
		if (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			idUnit1 = idUnit1 * self.getMaxCol()
		(iOwner, iID) = listAPLButtons[idUnit1]
		pUnit = gc.getPlayer(iOwner).getUnit(iID)
		iUnitType	= self.dUnitUpgradeList[idUnit2][idUpgrade-1]
		getKeyEvent = CvEventInterface.getEventManager()
		if getKeyEvent.bCtrl:
			pPlot = pUnit.plot()
			iCompUnitType = pUnit.getUnitType()
			for i in xrange(pPlot.getNumUnits()):
				pLoopUnit = pPlot.getUnit(i)
				if (pLoopUnit.getUnitType() == iCompUnitType):
					pLoopUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)
		elif getKeyEvent.bAlt:
			pActPlayer = gc.getActivePlayer()
			iCompUnitType = pUnit.getUnitType()
			for i in xrange(pActPlayer.getNumUnits()):
				pLoopUnit = pActPlayer.getUnit(i)
				if (pLoopUnit.getUnitType() == iCompUnitType):
					pLoopUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)
		else:
			pUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)

	# handles display of the promotion bottun info pane
	def showPromoInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		idPromo = id % 100
		idUnit1 = id / 100
		idUnit2 = idUnit1
		if (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			idUnit1 = idUnit1 * self.getMaxCol()
		(iOwner, iID) = listAPLButtons[idUnit1]
		pUnit = gc.getPlayer(iOwner).getUnit(iID)
		iPromo	= self.dUnitPromoList[idUnit2][idPromo-1]

		# promo info
		szPromoInfo = u"<font=2>%s</font>\n"%(removeLinks.sub("", CyGameTextMgr().getPromotionHelp(iPromo, False)))

		# unit level
		iLevel = pUnit.getLevel()
		iMaxLevel = mt.GetPossiblePromotions(pUnit.experienceNeeded(), pUnit.getExperience())
		if iMaxLevel <> iLevel:
			# actual / available (= number of possible promotions)
			szLevel = u"<font=2>%s%i / %i</font>\n"%(localText.getText("INTERFACE_PANE_LEVEL", ()), iLevel, (iMaxLevel+iLevel))
		else:
			# actual
			szLevel = u"<font=2>%s%i</font>\n"%(localText.getText("INTERFACE_PANE_LEVEL", ()), iLevel)

		# unit experience (actual / needed)
		iExperience = pUnit.getExperience()
		if (iExperience > 0):
			szExperience = u"<font=2>%s: %i / %i</font>\n"%(localText.getText("INTERFACE_PANE_EXPERIENCE", ()), iExperience, pUnit.experienceNeeded())
		else:
			szExperience = u""

		szText = szPromoInfo + szLevel + szExperience

		# display the info pane
		self.displayInfoPane(szText)
		(nRow, nCol) = divmod(idUnit1, self.getMaxCol())
		if (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			nCol += idPromo
		else:
			nRow += idPromo
		x = 315 + nCol * 36
		y = self.yResolution - 179 - nRow * 44
		self.tLastMousePos = (x, y, x + 32, y + 32)

	def hidePromoInfoPane(self):
		self.hideInfoPane()

	# handles display of the promotion bottun info pane
	def showUpgradeInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		idUpgrade	= id % 100
		idUnit1		= id / 100
		idUnit2		= idUnit1
		if (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			idUnit1 = idUnit1 * self.getMaxCol()
		(iOwner, iID) = listAPLButtons[idUnit1]
		pUnit = gc.getPlayer(iOwner).getUnit(iID)
		iUnitType		= self.dUnitUpgradeList[idUnit2][idUpgrade-1]
		pUnitTypeInfo 	= gc.getUnitInfo(iUnitType)

		# reading attributes
		szUnitName = localText.changeTextColor(pUnitTypeInfo.getDescription(), self.CFG_INFOPANE_COLOR_UNIT_COL) + "\n"
		if pUnitTypeInfo.getUnitCombatType() != -1:
			szCombatType = gc.getUnitCombatInfo(pUnitTypeInfo.getUnitCombatType()).getDescription() + "\n"
		else:
			szCombatType = u""
		if (pUnitTypeInfo.getAirCombat() > 0):
			iStrength = pUnitTypeInfo.getAirCombat()
		else:
			iStrength = pUnitTypeInfo.getCombat()
		szStrength = u"%i %c"%(iStrength, CyGame().getSymbolID( FontSymbols.STRENGTH_CHAR ))
		szMovement = u", %i %c"%(pUnitTypeInfo.getMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
		if (pUnitTypeInfo.getAirRange() > 0):
			szRange = u", %s\n"%(localText.getText("TXT_KEY_UNIT_AIR_RANGE", ( pUnitTypeInfo.getAirRange(), ) ))
		else:
			szRange = u"\n"
		szSpecialText = removeLinks.sub("", CyGameTextMgr().getUnitHelp(iUnitType, True, False, False, None)[1:]) + "\n"

		# determining the unit upgrade price
		iUpgradePriceSingle = mt.getUpgradePrice(pUnit, iUnitType, 0)
		iUpgradePricePlot	= mt.getUpgradePrice(pUnit, iUnitType, 2)
		iUpgradePriceAll 	= mt.getUpgradePrice(pUnit, iUnitType, 3)

		iGold = gc.getActivePlayer().getGold()
		if iUpgradePriceSingle > iGold:
			szUpgradePriceSingle = localText.changeTextColor(u"%i"%iUpgradePriceSingle, self.CFG_INFOPANE_UPGRADE_NOT_POSSIBLE_COL)
		else:
			szUpgradePriceSingle = localText.changeTextColor(u"%i"%iUpgradePriceSingle, self.CFG_INFOPANE_UPGRADE_POSSIBLE_COL)
		if iUpgradePricePlot > iGold:
			szUpgradePricePlot = localText.changeTextColor(u"%i"%iUpgradePricePlot, self.CFG_INFOPANE_UPGRADE_NOT_POSSIBLE_COL)
		else:
			szUpgradePricePlot = localText.changeTextColor(u"%i"%iUpgradePricePlot, self.CFG_INFOPANE_UPGRADE_POSSIBLE_COL)
		if iUpgradePriceAll > iGold:
			szUpgradePriceAll = localText.changeTextColor(u"%i"%iUpgradePriceAll, self.CFG_INFOPANE_UPGRADE_NOT_POSSIBLE_COL)
		else:
			szUpgradePriceAll = localText.changeTextColor(u"%i"%iUpgradePriceAll, self.CFG_INFOPANE_UPGRADE_POSSIBLE_COL)

		szUpgradePrice = "%s / %s / %s %c\n"%(szUpgradePriceSingle, szUpgradePricePlot, szUpgradePriceAll, gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar())
		szSelectedUnitDomain = u"None"

		szSelectedUnitDomain = self.DomainTextMap[pUnitTypeInfo.getDomainType()]

		szUpgradeHelp = localText.getText("TXT_KEY_APL_UPGRADE_HELP", (gc.getUnitInfo(pUnit.getUnitType()).getDescription(), szSelectedUnitDomain,))

		szText = u"<font=2>%s%s%s%s%s%s%s%s</font>"%(szUnitName, szCombatType, szStrength, szMovement, szRange, szSpecialText, szUpgradePrice, szUpgradeHelp)

		# display the info pane
		self.displayInfoPane(szText)
		(nRow, nCol) = divmod(idUnit1, self.getMaxCol())
		if (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
			nCol += idUpgrade
		else:
			nRow += idUpgrade
		x = 315 + nCol * 36
		y = self.yResolution - 179 - nRow * 44
		self.tLastMousePos = (x, y, x + 32, y + 32)

	def hideUpgradeInfoPane(self):
		self.hideInfoPane()

	# handles the diaplay of the units info pane
	def showUnitInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		GetText = localText.getText
		(iOwner, iID) = listAPLButtons[id]
		pUnit = gc.getPlayer(iOwner).getUnit(iID)
		iUnitType		= pUnit.getUnitType()
		eUnitDomain		= gc.getUnitInfo(iUnitType).getDomainType()
		szText = u"<font=2>"

		# warlord
		if (pUnit.isHasPromotion(self.iPromoLeader)):
			szText += u"<img=" + gc.getPromotionInfo(self.iPromoLeader).getButton() + u" size=18></img> "

		szText += localText.changeTextColor(pUnit.getName(), self.CFG_INFOPANE_COLOR_UNIT_COL)

		# get units owner name if its not a player unit
		if (pUnit.getOwner() != gc.getGame().getActivePlayer()):
			pOwner = gc.getPlayer(pUnit.getOwner())
			szText += u" [" + localText.changeTextColor(pOwner.getName(), gc.getPlayerColorInfo(pOwner.getPlayerColor()).getTextColorType()) + u"]"

		# unit type description + unit name (if given)
		szText += u"</font>\n"

		# count the promotions
		szPromotion = u""
		iPromotionCount = 0
		szProButtonTag = u" size=" + str(self.CFG_INFOPANE_BUTTON_SIZE) + u"></img>"
		for i in xrange(gc.getNumPromotionInfos()):
			if (pUnit.isHasPromotion(i) and i != self.iPromoLeader):
				iPromotionCount += 1
				szPromotion += u"<img=" + gc.getPromotionInfo(i).getButton() + szProButtonTag
			if (iPromotionCount >= self.CFG_INFOPANE_BUTTON_PER_LINE -1):
				szPromotion += u"\n"
				iPromotionCount = 0
		if (len(szPromotion)):
			szPromotion += u"\n"
		szText += szPromotion

		# strength
		if (eUnitDomain == DomainTypes.DOMAIN_AIR):
			fMaxStrength = float(pUnit.airBaseCombatStr())
		else:
			fMaxStrength = float(pUnit.baseCombatStr())
		fCurrStrength = fMaxStrength*(1.0-pUnit.getDamage()*0.01)
		if fCurrStrength != fMaxStrength:
			HealFactor = mt.getPlotHealFactor(pUnit)
			if (HealFactor != 0):
				iTurnsToHeal = int((fMaxStrength-fCurrStrength)/(fMaxStrength*HealFactor*0.01)+0.999) # force to round upwards
				szTurnsToHeal = u" (" + str(iTurnsToHeal) + u")"
			else:
				szTurnsToHeal = u" (Not Healing)"
			szCurrStrength = u" %.1f" % fCurrStrength
			szMaxStrength = u" / %i" % fMaxStrength
		else:
			iTurnsToHeal = 0
			szCurrStrength = u" %i" % fCurrStrength
			szMaxStrength = u""
			szTurnsToHeal = u""

		# movement
		fMaxMoves = pUnit.baseMoves()
		fCurrMoves = fMaxMoves - pUnit.getMoves()/60.0
		if (eUnitDomain == DomainTypes.DOMAIN_AIR):
			szAirRange = u", " + localText.getText("TXT_KEY_UNIT_AIR_RANGE", (pUnit.airRange(), ))
		else:
			szAirRange = u""
		if fCurrMoves != 0:
			szCurrMoves = u" %.1f" % fCurrMoves
			szMaxMoves = u" / %i" % fMaxMoves
		else:
			szCurrMoves = u" %i" % fMaxMoves
			szMaxMoves = u""

		# compressed display for stadnard display
		szText += u"<font=2>" + szCurrStrength + szMaxStrength + szTurnsToHeal + unichr(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)) + ", " + szCurrMoves + szMaxMoves + unichr(CyGame().getSymbolID(FontSymbols.MOVES_CHAR)) + szAirRange + u"</font>\n"

		# unit level
		iLevel = pUnit.getLevel()
		iMaxLevel = int(mt.GetPossiblePromotions(pUnit.experienceNeeded(), pUnit.getExperience()))
		if (iMaxLevel > 0) or (iLevel > 1):
			szLevel = u"<font=2>" + GetText("INTERFACE_PANE_LEVEL", ()) + " " + str(iLevel)
			if (iMaxLevel > 0):
				szLevel += u" / " + str(iMaxLevel+iLevel)
			szLevel += "</font>\n"
		else:
			szLevel = u""
		szText += szLevel

		# unit experience (actual / needed (possible promos))
		iExperience = pUnit.getExperience()
		if (iExperience > 0):
			szText += u"<font=2>" + GetText("INTERFACE_PANE_EXPERIENCE", ()) + ": " + str(iExperience) + " / " + str(pUnit.experienceNeeded()) + "</font>\n"

		# cargo space
		iCargoSpace = pUnit.cargoSpace()
		if iCargoSpace > 0:
			szText += u"<font=2>" + GetText("TXT_KEY_UNIT_HELP_CARGO_SPACE", (pUnit.getCargo(), iCargoSpace)) + u"</font>\n"

		# fortify bonus
		iFortifyBonus = pUnit.fortifyModifier()
		if iFortifyBonus > 0:
			szText += u"<font=2>" + GetText("TXT_KEY_UNIT_HELP_FORTIFY_BONUS", (iFortifyBonus, )) + u"\n</font>"

		# unit type specialities 
		szSpecialText = u"<font=2>" + GetText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u":\n" + CyGameTextMgr().getUnitHelp(iUnitType, True, False, False, None)[1:] + u"</font>"
		szSpecialText = localText.changeTextColor(szSpecialText, self.CFG_INFOPANE_UNITTYPE_SPECS_COL)

		if iLevel > 0:
			szSpecialText += u"\n" + localText.changeTextColor(mt.getPromotionInfoText(pUnit), self.CFG_INFOPANE_PROMO_SPECS_COL)
		szText += removeLinks.sub("", szSpecialText)

		if (gc.getUnitInfo(iUnitType).isSpy()):
			szEspText = mt.getDoEspionageText(pUnit)
			if (szEspText != ""):
				if (pUnit.getFortifyTurns() > 0):
					szTurn = GetText("INTERFACE_CITY_TURNS", (pUnit.getFortifyTurns(),))
				else:
					szTurn = u""
				szText += u"<font=2>" + GetText("TXT_KEY_CGE_ESPIONAGE_MISSION", ()) + szTurn + u":\n" + szEspText + u"</font>"

		szSelectedUnitDomain = self.DomainTextMap.get(eUnitDomain, u"None")

		szText += u"\n<font=2>" + GetText("TXT_KEY_APL_UPGRADE_HELP", (gc.getUnitInfo(iUnitType).getDescription(), szSelectedUnitDomain)) + u"</font>"

		# display the info pane
		self.displayInfoPane(szText)
		self.setLastMousePos(id)

	def showCompactUnitInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		(iOwner, iUnitType) = listAPLButtons[id]

		szText = u""
		szProButtonTag = u" size=16></img>"
		pPlot = CyInterface().getSelectionPlot()
		GetUnit = CyInterface().getInterfacePlotUnit
		eUnitDomain = gc.getUnitInfo(iUnitType).getDomainType()

		for i in xrange(pPlot.getNumUnits()):
			pLoopUnit = GetUnit(pPlot, i)
			if (pLoopUnit):
				if (pLoopUnit.getUnitType() == iUnitType):
					szText += "<font=2>" + localText.changeTextColor(pLoopUnit.getName(), self.CFG_INFOPANE_COLOR_UNIT_COL) + u" "

					# get units owner name if its not a player unit
					if (pLoopUnit.getOwner() != gc.getGame().getActivePlayer()):
						pOwner = gc.getPlayer(pLoopUnit.getOwner())
						szText += u" [" + localText.changeTextColor(pOwner.getName(), gc.getPlayerColorInfo(pOwner.getPlayerColor()).getTextColorType()) + u"] "

					# strength
					if (eUnitDomain == DomainTypes.DOMAIN_AIR):
						fMaxStrength = float(pLoopUnit.airBaseCombatStr())
					else:
						fMaxStrength = float(pLoopUnit.baseCombatStr())
					fCurrStrength = fMaxStrength*(1.0-pLoopUnit.getDamage()*0.01)
					if fCurrStrength != fMaxStrength:
						szCurrStrength = u" %.1f" % fCurrStrength
						szMaxStrength = u"/%i" % fMaxStrength
					else:
						szCurrStrength = u" %i" % fCurrStrength
						szMaxStrength = u""

					# movement
					fMaxMoves = pLoopUnit.baseMoves()
					fCurrMoves = fMaxMoves - pLoopUnit.getMoves()/60.0
					if (eUnitDomain == DomainTypes.DOMAIN_AIR):
						szAirRange = u", " + localText.getText("TXT_KEY_UNIT_AIR_RANGE", (pLoopUnit.airRange(), ))
					else:
						szAirRange = u""
					if fCurrMoves != 0:
						szCurrMoves = u" %.1f" % fCurrMoves
						szMaxMoves = u" /%i" % fMaxMoves
					else:
						szCurrMoves = u" %i" % fMaxMoves
						szMaxMoves = u""

					# compressed display for stadnard display
					szText += szCurrStrength + szMaxStrength + unichr(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)) + ", " + szCurrMoves + szMaxMoves + unichr(CyGame().getSymbolID(FontSymbols.MOVES_CHAR)) + szAirRange + u" "

					# unit experience (actual / needed (possible promos))
					iExperience = pLoopUnit.getExperience()
					if (iExperience > 0):
						szText += localText.getText("INTERFACE_PANE_EXPERIENCE", ()) + ": " + str(iExperience) + "/" + str(pLoopUnit.experienceNeeded())

					for i in xrange(gc.getNumPromotionInfos()):
						if (pLoopUnit.isHasPromotion(i) and i != self.iPromoLeader):
							szText += u"<img=" + gc.getPromotionInfo(i).getButton() + szProButtonTag

					# unit type description + unit name (if given)
					szText += u"</font>\n"
		szText += u"\n<font=2>" + localText.getText("TXT_KEY_APL_EXPAND_PLOT_LIST", ()) + u"</font>"

		# display the info pane
		self.displayInfoPane(szText)
		self.setLastMousePos(id)

	def hideUnitInfoPane(self):
		self.hideInfoPane()

	# base function to display a self sizing info pane
	def displayInfoPane(self, szText):

		self.bInfoPaneActive = True
		self.tLastMousePos = (CyInterface().getMousePos().x-30, CyInterface().getMousePos().y-30, CyInterface().getMousePos().x + 30, CyInterface().getMousePos().y + 30)

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# calculate text size
		iNormalLines = 0
		iBulletLines = 0
		lChapters = removeTag.sub("", szText).split('\n')
		sComp = u"%c"%CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		InfoPaneWidth = self.CFG_INFOPANE_DX - 3
		for LoopChapters in lChapters:
			iWidth = CyInterface().determineWidth(LoopChapters)/InfoPaneWidth + 1
			if (LoopChapters.find(sComp) != -1):
				iBulletLines += iWidth
			else:
				iNormalLines += iWidth
		dy = iNormalLines*self.CFG_INFOPANE_PIX_PER_LINE_1 + iBulletLines*self.CFG_INFOPANE_PIX_PER_LINE_2 + 13# + 20

		# draw panel
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			y = self.CFG_INFOPANE_Y - dy
		else:
			y = self.CFG_INFOPANE_Y2 - dy

		screen.hide("APL_UNIT_INFO_PANE_ID")
		screen.hide("APL_UNIT_INFO_TEXT_ID")
		screen.hide("APL_UNIT_INFO_TEXT_SHADOW_ID")

		screen.setPanelSize("APL_UNIT_INFO_PANE_ID", self.CFG_INFOPANE_X, y, self.CFG_INFOPANE_DX, dy)

		# create shadow text
		szTextBlack = localText.changeTextColor(removeColor.sub("", szText), gc.getInfoTypeForString("COLOR_BLACK"))

		# display shadow text
		screen.addMultilineText("APL_UNIT_INFO_TEXT_SHADOW_ID", szTextBlack, self.CFG_INFOPANE_X + 5, y + 9, self.CFG_INFOPANE_DX - 3, dy - 3,  WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		# display text
		screen.addMultilineText("APL_UNIT_INFO_TEXT_ID", szText, self.CFG_INFOPANE_X + 4, y + 8, self.CFG_INFOPANE_DX - 3, dy - 3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.moveToFront("APL_UNIT_INFO_PANE_ID")
		screen.moveToFront("APL_UNIT_INFO_TEXT_SHADOW_ID")
		screen.moveToFront("APL_UNIT_INFO_TEXT_ID")
		screen.show("APL_UNIT_INFO_PANE_ID")
		screen.show("APL_UNIT_INFO_TEXT_ID")
		screen.show("APL_UNIT_INFO_TEXT_SHADOW_ID")

	# hides the info pane
	def hideInfoPane(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide("APL_UNIT_INFO_TEXT_ID")
		screen.hide("APL_UNIT_INFO_TEXT_SHADOW_ID")
		screen.hide("APL_UNIT_INFO_PANE_ID")

		self.bInfoPaneActive = False

	def setLastMousePos(self, id):
		(nRow, nCol) = divmod(id, self.getMaxCol())
		x = 315 + nCol * 36
		y = self.yResolution - 179 - nRow * 44
		self.tLastMousePos = (x, y, x + 32, y + 32)

	def numPlotListButtons(self):
		return self.m_iNumPlotListButtons

	def interfaceScreen(self):

		# Global variables being set here
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos

		global MAX_SELECTED_TEXT
		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS
		global MAX_CITIZEN_BUTTONS

		# <STACKER START>
		global SPECIALIST_STACK_WIDTH
		global g_bHighlightForcedSpecialists
		global g_bStackSuperSpecialists
		global MAX_SUPER_SPECIALIST_BUTTONS
		global SUPER_SPECIALIST_STACK_WIDTH
		global g_bDisplayUniqueSuperSpecialistsOnly
		global g_bDynamicSuperSpecialistsSpacing
		global g_bStackAngryCitizens
		global MAX_ANGRY_CITIZEN_BUTTONS
		global ANGRY_CITIZEN_STACK_WIDTH
		global g_bDynamicAngryCitizensSpacing
		global g_iSuperSpecialistCount
		global g_iAngryCitizensCount
		# <STACKER END>

		# < Dead Civ Scoreboard Mod Start >
		global g_bHideDeadCivilizations
		global g_bGreyOutDeadCivilizations
		global g_bShowDeadTag

		# < Dead Civ Scoreboard Mod End  >

		# < NJAGCM Start >
		global g_bAlternateTimeText
		global g_iAlternatingTime
		global g_bShowTurns
		global g_bShowGameClock
		global g_bShowGameCompletedTurns
		global g_bShowGameCompletedPercent

		global g_bAlternateShowTurns
		global g_bAlternateShowGameClock
		global g_bAlternateShowGameCompletedPercent
		global g_bAlternateShowGameCompletedTurns

		global g_bShowEra
		global g_bShowReflectEraInTurnColor
		global g_eraTurnColorDictionary
		global g_eraText
		global g_szOldTimeText
		# < NJAGCM End >
		global g_WinAMP
		global CFG_CIV_NAME_ON_SCOREBOARD
		global CFG_MASTER_NAME_ON_SCOREBOARD
		global CFG_RAWCOMMERCEDISPLAY
		global CFG_Specialist_Stacker
		global CFG_Combat_Experience_Counter
		global CFG_Unit_Statistics
		global CFG_Show_GameTurn_Bar
		global g_ShowGameTurnBarColor
		global CFG_Show_GreatPerson_Bar
		global CFG_Show_TopCultureCities
		global bCompressMode

		global listPrevAPLButtons
		global listPrevAPLSpotIcons
		global listPrevAPLUpgradeIndicator
		global listPrevAPLHealthBar
		global iMaxPlotListIcons

		global GPBarText
		global gCombatXPText
		global g_BottomContIconSize
		global gTopCivCultureText
		global gTopCivCulturePos
		global szGoldText

		if ( CyGame().isPitbossHost() ):
			return

		##### <written by F> #####
		#スペルの初期化処理
		### やっぱ戻す
		SpellInfo.init()
		##### </written by F> #####

		# This is the main interface screen, create it as such
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.setForcedRedraw(True)

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34

		screen.setDimensions(0, 0, xResolution, yResolution)

		config = CvConfigParser.CvConfigParser("Civ IV Gameplay Enhancements Config.ini")
		if (config != None):
			self.CFG_Enabled_APL = config.getboolean("APL General", "Enabled", True)

		if (self.CFG_Enabled_APL):
			self.pOldPlot = 0
			self.xResolution = xResolution
			self.yResolution = yResolution

		if (config != None):
			self.CFG_APL_STACK_MODE						= config.getint("APL General",			"Stack Mode", 					0)
			self.CFG_MISSION_INFO_ENABLED				= config.getboolean("APL General",		"Mission Info Enabled",			True)
			self.CFG_HEALTH_BAR_ENABLED					= config.getboolean("APL General",		"Health Bar Enabled",			True)
			self.CFG_MOVE_BAR_ENABLED					= config.getboolean("APL General",		"Move Bar Enabled",				True)
			self.CFG_UPGRADE_INDICATOR_ENABLED			= config.getboolean("APL General",		"Upgrade Indicator Enabled",	True)
			self.CFG_PROMO_INDICATOR_ENABLED			= config.getboolean("APL General",		"Promotion Indicator Enabled",	True)
			self.CFG_WOUNDED_INDICATOR_ENABLED			= config.getboolean("APL General",		"Wounded Indicator Enabled",	True)
			self.CFG_WARLORD_INDICATOR_ENABLED			= config.getboolean("APL General",		"Warlord Indicator Enabled",	True)
			self.CFG_INFOPANE_PIX_PER_LINE_1 			= config.getint("APL Info Pane",		"Pixel Per Line Type 1",		24)
			self.CFG_INFOPANE_PIX_PER_LINE_2 			= config.getint("APL Info Pane",		"Pixel Per Line Type 2",		19)
			self.CFG_INFOPANE_X 						= config.getint("APL Info Pane",		"X Position",					5)
			self.CFG_INFOPANE_Y 						= config.getint("APL Info Pane",		"Y Position",					160)
			self.CFG_INFOPANE_DX 						= config.getint("APL Info Pane",		"X Size",						290)
			self.CFG_INFOPANE_COLOR_UNIT_COL			= config.get("APL Info Pane Colors",	"Unit Name Color",				"COLOR_YELLOW")
			self.CFG_INFOPANE_UPGRADE_POSSIBLE_COL		= config.get("APL Info Pane Colors",	"Upgrade Possible Color",		"COLOR_GREEN")
			self.CFG_INFOPANE_UPGRADE_NOT_POSSIBLE_COL	= config.get("APL Info Pane Colors",	"Upgrade Not Possible Color",	"COLOR_RED")
			self.CFG_INFOPANE_PROMO_SPECS_COL			= config.get("APL Info Pane Colors",	"Promotion Specialties Color",	"COLOR_LIGHT_GREY")
			self.CFG_INFOPANE_UNITTYPE_SPECS_COL		= config.get("APL Info Pane Colors",	"Unit Type Specialties Color",	"COLOR_WHITE")
			self.CFG_STACKEDBAR_HEALTH_COL				= config.get("APL Stacked Bar Colors",	"Health Color",					"COLOR_GREEN")
			self.CFG_STACKEDBAR_WOUNDED_COL				= config.get("APL Stacked Bar Colors",	"Wounded Color",				"COLOR_RED")
			self.CFG_STACKEDBAR_MOVE_COL				= config.get("APL Stacked Bar Colors",	"Movement Color",				"COLOR_BLUE")
			self.CFG_STACKEDBAR_NOMOVE_COL				= config.get("APL Stacked Bar Colors",	"No Movement Color",			"COLOR_YELLOW")

			self.CFG_INFOPANE_COLOR_UNIT_COL			= gc.getInfoTypeForString(self.CFG_INFOPANE_COLOR_UNIT_COL)
			self.CFG_INFOPANE_UPGRADE_POSSIBLE_COL		= gc.getInfoTypeForString(self.CFG_INFOPANE_UPGRADE_POSSIBLE_COL)
			self.CFG_INFOPANE_UPGRADE_NOT_POSSIBLE_COL	= gc.getInfoTypeForString(self.CFG_INFOPANE_UPGRADE_NOT_POSSIBLE_COL)
			self.CFG_INFOPANE_PROMO_SPECS_COL			= gc.getInfoTypeForString(self.CFG_INFOPANE_PROMO_SPECS_COL)
			self.CFG_INFOPANE_UNITTYPE_SPECS_COL		= gc.getInfoTypeForString(self.CFG_INFOPANE_UNITTYPE_SPECS_COL)
			self.CFG_STACKEDBAR_HEALTH_COL				= gc.getInfoTypeForString(self.CFG_STACKEDBAR_HEALTH_COL)
			self.CFG_STACKEDBAR_WOUNDED_COL				= gc.getInfoTypeForString(self.CFG_STACKEDBAR_WOUNDED_COL)
			self.CFG_STACKEDBAR_MOVE_COL				= gc.getInfoTypeForString(self.CFG_STACKEDBAR_MOVE_COL)
			self.CFG_STACKEDBAR_NOMOVE_COL				= gc.getInfoTypeForString(self.CFG_STACKEDBAR_NOMOVE_COL)

			# <STACKER START>
			g_bHighlightForcedSpecialists = config.getboolean("Specialist Stacker", "Highlight Forced Specialists", g_bHighlightForcedSpecialists)
			SPECIALIST_STACK_WIDTH = config.getint("Specialist Stacker", "Specialist Stack Width", SPECIALIST_STACK_WIDTH)
			g_bStackSuperSpecialists = config.getboolean("Specialist Stacker", "Stack Super Specialists", g_bStackSuperSpecialists)
			MAX_SUPER_SPECIALIST_BUTTONS = config.getint("Specialist Stacker", "Max Super Specialist Buttons", MAX_SUPER_SPECIALIST_BUTTONS)
			SUPER_SPECIALIST_STACK_WIDTH = config.getint("Specialist Stacker", "Super Specialist Stack Width", SUPER_SPECIALIST_STACK_WIDTH)
			g_bDisplayUniqueSuperSpecialistsOnly = config.getboolean("Specialist Stacker", "Display Unique Super Specialists Only", g_bDisplayUniqueSuperSpecialistsOnly)
			g_bDynamicSuperSpecialistsSpacing = config.getboolean("Specialist Stacker", "Dynamic Super Specialists Spacing", g_bDynamicSuperSpecialistsSpacing)
			g_bStackAngryCitizens = config.getboolean("Specialist Stacker", "Stack Angry Citizens", g_bStackAngryCitizens)
			MAX_ANGRY_CITIZEN_BUTTONS = config.getint("Specialist Stacker", "Max Angry Citizen Buttons", MAX_ANGRY_CITIZEN_BUTTONS)
			ANGRY_CITIZEN_STACK_WIDTH = config.getint("Specialist Stacker", "Angry Citizen Stack Width", ANGRY_CITIZEN_STACK_WIDTH)
			g_bDynamicAngryCitizensSpacing = config.getboolean("Specialist Stacker", "Dynamic Angry Citizen Spacing", g_bDynamicAngryCitizensSpacing)
			# <STACKER END>
			g_bHideDeadCivilizations = config.getboolean("Dead Civ Scoreboard Mod", "Hide Dead Civilizations", True)
			g_bGreyOutDeadCivilizations = config.getboolean("Dead Civ Scoreboard Mod", "Grey Out Dead Civilizations", True)
			g_bShowDeadTag = config.getboolean("Dead Civ Scoreboard Mod", "Show Dead Tag", True)
			# < NJAGCM Start   >
			g_bAlternateTimeText = config.getboolean("Not Just Another Game Clock Mod", "Alternate Time Text", True)
			g_iAlternatingTime = config.getint("Not Just Another Game Clock Mod", "Alternating Time", 15)
			g_bShowTurns = config.getboolean("Not Just Another Game Clock Mod", "Show Turns", True)
			g_bShowGameClock = config.getboolean("Not Just Another Game Clock Mod", "Show Game Clock", True)
			g_bShowGameCompletedPercent = config.getboolean("Not Just Another Game Clock Mod", "Show Game Completed Percent", True)
			g_bShowGameCompletedTurns = config.getboolean("Not Just Another Game Clock Mod", "Show Game Completed Turns", False)
			g_bAlternateShowTurns = config.getboolean("Not Just Another Game Clock Mod", "Alternate Show Turns", True)
			g_bAlternateShowGameClock = config.getboolean("Not Just Another Game Clock Mod", "Alternate Show Game Clock", True)
			g_bAlternateShowGameCompletedPercent = config.getboolean("Not Just Another Game Clock Mod", "Alternate Show Game Completed Percent", False)
			g_bAlternateShowGameCompletedTurns = config.getboolean("Not Just Another Game Clock Mod", "Alternate Show Game Completed Turns", True)
			g_bShowEra = config.getboolean("Not Just Another Game Clock Mod", "Show Era", True)
			g_bShowReflectEraInTurnColor = config.getboolean("Not Just Another Game Clock Mod", "Show Reflect Era In Turn Color", True)

			for i in xrange(gc.getNumEraInfos()):
				eraType = gc.getEraInfo(i).getType()
				tmpString = config.get("Not Just Another Game Clock Mod", eraType, "")
				if(tmpString):
					g_eraTurnColorDictionary[eraType] = gc.getInfoTypeForString(tmpString)
			g_eraText = ""
			g_szOldTimeText = ""
			# < NJAGCM End   >

			# スコアボードに文明名を表示
			CFG_CIV_NAME_ON_SCOREBOARD	= config.getboolean("Civ Name", "Enabled", True)
			# 都市画面に商業力を表示
			CFG_RAWCOMMERCEDISPLAY		= config.getboolean("Raw Commerce Display", "Enabled", True)
			# Specialist Stacker
			CFG_Specialist_Stacker		= config.getboolean("Specialist Stacker", "Enabled", True)
			# Winamp GUI
			g_WinAMP 					= config.getboolean("Winamp GUI", "Enabled", False)
			# Combat Experience Counter
			CFG_Combat_Experience_Counter = config.getboolean("Combat Experience Counter", "Enabled", True)
			# Game Turn Bar
			CFG_Show_GameTurn_Bar = config.getboolean("Game Turn Bar", "Enabled", True)
			g_ShowGameTurnBarColor = -1
			CFG_Show_GreatPerson_Bar = config.getboolean("Great Person Bar", "Enabled", True)
			CFG_Show_TopCultureCities = config.getboolean("Top Culture Cities", "Enabled", True)
			CFG_Enabled_Compress_Mode = config.getboolean("APL General", "Compress Mode", True)
			bBottomContSmallIcon = config.getboolean("Bottom Container Icon", "Small", True)
			CFG_MASTER_NAME_ON_SCOREBOARD = config.getboolean("Master Name", "Enabled", True)
			if (CFG_Enabled_Compress_Mode):
				bCompressMode = True
			else:
				bCompressMode = False

		self.CFG_INFOPANE_Y		 			= yResolution - self.CFG_INFOPANE_Y
		self.CFG_INFOPANE_BUTTON_SIZE		= self.CFG_INFOPANE_PIX_PER_LINE_1-2
		self.CFG_INFOPANE_BUTTON_PER_LINE	= self.CFG_INFOPANE_DX / self.CFG_INFOPANE_BUTTON_SIZE
		self.CFG_INFOPANE_Y2				= self.CFG_INFOPANE_Y + 105

		self.OVERLAY_ACTION_FORTIFY = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_FORTIFY").getPath()
		self.OVERLAY_ACTION_SLEEP = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SLEEP").getPath()
		self.OVERLAY_ACTION_RECON = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_RECON").getPath()

		self.ActivityIconMap = {
			ActivityTypes.ACTIVITY_INTERCEPT	: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PATROL").getPath(),	# 5
			ActivityTypes.ACTIVITY_HEAL			: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_HEAL").getPath(),		# 3
			ActivityTypes.ACTIVITY_SENTRY		: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SENTRY").getPath(),	# 4
			ActivityTypes.ACTIVITY_HOLD			: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SKIP").getPath(),		# 1
			#ActivityTypes.ACTIVITY_SLEEP		: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SLEEP").getPath(),		# 2
			ActivityTypes.ACTIVITY_PATROL		: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PATROL").getPath(),	# 7
			ActivityTypes.ACTIVITY_PLUNDER		: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PLUNDER").getPath(),	# 8
		}

		self.AutomateIconMap = {
			AutomateTypes.AUTOMATE_EXPLORE	: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_EXPLORE").getPath(),		# 3
			AutomateTypes.AUTOMATE_BUILD	: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_BUILD").getPath(),	# 0
			AutomateTypes.AUTOMATE_CITY		: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_CITY").getPath(),		# 2
			AutomateTypes.AUTOMATE_NETWORK	: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_NETWORK").getPath(),	# 1
			AutomateTypes.AUTOMATE_RELIGION	: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SPREAD").getPath(),	# 4
		}

		self.MissionIconMap = {
			MissionTypes.MISSION_MOVE_TO		: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_GOTO").getPath(),		# 0
			MissionTypes.MISSION_MOVE_TO_UNIT	: ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_GOTO").getPath(),		# 2
		}

		self.DomainTextMap = {
			DomainTypes.DOMAIN_AIR		: localText.getText("TXT_KEY_DOMAIN_AIR", ()),
			DomainTypes.DOMAIN_SEA		: localText.getText("TXT_KEY_DOMAIN_SEA", ()),
			DomainTypes.DOMAIN_LAND		: localText.getText("TXT_KEY_DOMAIN_LAND", ()),
			DomainTypes.DOMAIN_IMMOBILE	: localText.getText("TXT_KEY_DOMAIN_IMMOBILE", ()),
		}

		self.SpotIconState = {
			1: ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath(),
			2: ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath(),
			3: ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath(),
			4: ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath(),
			5: ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY_INJURED").getPath(),
			6: ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED_INJURED").getPath(),
			7: ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE_INJURED").getPath(),
			8: ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE_INJURED").getPath(),
		}

		self.UpgradePromoIconMap = {
			1: ArtFileMgr.getInterfaceArtInfo("APL_UPGRADE_ARROW").getPath(),
			2: ArtFileMgr.getInterfaceArtInfo("APL_PROMO_STAR").getPath(),
			3: ArtFileMgr.getInterfaceArtInfo("APL_UPGRADE_PROMO").getPath(),
		}

		listPrevAPLButtons = dict()
		listPrevAPLSpotIcons = dict()
		listPrevAPLUpgradeIndicator = dict()
		listPrevAPLHealthBar = dict()
		self.bAPLSelectOnly = False

		if (self.CFG_APL_STACK_MODE == 0):
			self.sAPLMode = self.APL_MODE_MULTILINE
		elif (self.CFG_APL_STACK_MODE == 1):
			self.sAPLMode = self.APL_MODE_STACK_VERT
		elif (self.CFG_APL_STACK_MODE == 2):
			self.sAPLMode = self.APL_MODE_STACK_HORIZ
		else:
			self.sAPLMode = self.APL_MODE_MULTILINE
		self.setAPLMode()

		mt.InitUpgradePath()

		self.Era = gc.getPlayer(gc.getGame().getActivePlayer()).getCurrentEra()

		GPBarText = u""
		gCombatXPText = u""
		gTopCivCultureText = u""
		gTopCivCulturePos = 0
		szGoldText = ""

		self.iSeeDemoMission = -1
		self.iSeeResMission = -1
		for iMissionLoop in xrange(gc.getNumEspionageMissionInfos()):
			if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
				self.iSeeDemoMission = iMissionLoop
			if (gc.getEspionageMissionInfo(iMissionLoop).isSeeResearch()):
				self.iSeeResMission = iMissionLoop

		self.iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
		self.GPUnitList = [gc.getInfoTypeForString(szUnit) for szUnit in ["UNIT_PROPHET", "UNIT_ARTIST", "UNIT_SCIENTIST", "UNIT_MERCHANT", "UNIT_ENGINEER", "UNIT_GREAT_SPY"]]

		if (CFG_Show_TopCultureCities):
			iVC = gc.getInfoTypeForString("VICTORY_CULTURAL")
			if (gc.getGame().isVictoryValid(iVC)):
				victory = gc.getVictoryInfo(iVC)
				if (not (victory.getCityCulture() != CultureLevelTypes.NO_CULTURELEVEL and victory.getNumCultureCities() > 0)):
					CFG_Show_TopCultureCities = False

		if (bBottomContSmallIcon):
			g_BottomContIconSize = 34
		else:
			g_BottomContIconSize = 48

		# score text cache
		self.ScoreAttCache = []
		self.ScoreTextCache = dict()
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			self.ScoreTextCache[iLoopPlayer] = ""

		self.CityButtonResolution = (0, 0)

		self.CommerceText = dict()
		self.CommerceText[-1] = -1
		for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			self.CommerceText[i] = [-1, -1, -1]

		self.autoInsertcandidates = dict()
		pActivePlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		getBuildingVal = gc.getCivilizationInfo(pActivePlayer.getCivilizationType()).getCivilizationBuildings
		for iBuilding in xrange(gc.getNumBuildingClassInfos()):
			iLoopBuilding = getBuildingVal(iBuilding)
			if (not isLimitedWonderClass(iBuilding)):
				for iI in xrange(gc.getNumBuildingClassInfos()):
					if (gc.getBuildingInfo(iLoopBuilding).isBuildingClassNeededInCity(iI)):
						self.autoInsertcandidates[iLoopBuilding] = getBuildingVal(iI)

		self.iAutoInsertQueueCityID = -1

		self.bHasCGEDLL = False
# CGE-LE - begin
		self.bHasCGELEDLL = False
		try:
			if (gc.isCGEBuild()):
				self.bHasCGEDLL = True
		except:
			try:
				if (gc.isCGELEBuild()):
					self.bHasCGELEDLL = True
			except:
				pass
# CGE-LE - end
		# Set up our global variables...
		g_NumEmphasizeInfos = gc.getNumEmphasizeInfos()
		g_NumCityTabTypes = CityTabTypes.NUM_CITYTAB_TYPES
		g_NumHurryInfos = gc.getNumHurryInfos()
		g_NumUnitClassInfos = gc.getNumUnitClassInfos()
		g_NumBuildingClassInfos = gc.getNumBuildingClassInfos()
		g_NumProjectInfos = gc.getNumProjectInfos()
		g_NumProcessInfos = gc.getNumProcessInfos()
		g_NumActionInfos = gc.getNumActionInfos()

		# Help Text Area
		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )

		# Center Left
		screen.addPanel( "InterfaceCenterLeftBackgroundWidget", u"", u"", True, False, 0, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterLeftBackgroundWidget", "Panel_City_Left_Style" )
		screen.hide( "InterfaceCenterLeftBackgroundWidget" )

		# Top Left
		screen.addPanel( "InterfaceTopLeftBackgroundWidget", u"", u"", True, False, 258, 0, xResolution - 516, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceTopLeftBackgroundWidget", "Panel_City_Top_Style" )
		screen.hide( "InterfaceTopLeftBackgroundWidget" )

		# Center Right
		screen.addPanel( "InterfaceCenterRightBackgroundWidget", u"", u"", True, False, xResolution - 258, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterRightBackgroundWidget", "Panel_City_Right_Style" )
		screen.hide( "InterfaceCenterRightBackgroundWidget" )

		screen.addPanel( "CityScreenAdjustPanel", u"", u"", True, False, 10, 44, 238, 105, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityScreenAdjustPanel", "Panel_City_Info_Style" )
		screen.hide( "CityScreenAdjustPanel" )

## Sevo - Raw Commerce Display - begin
		if (CFG_RAWCOMMERCEDISPLAY):
			screen.addPanel("CityScreenAdjustPanelb", u"", u"", True, False, 10, 154, 238, 90, PanelStyles.PANEL_STYLE_STANDARD)
			screen.setStyle("CityScreenAdjustPanelb", "Panel_City_Info_Style")
			screen.hide("CityScreenAdjustPanelb")
## Sevo - Raw Commerce Display - end

		screen.addPanel( "TopCityPanelLeft", u"", u"", True, False, 260, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelLeft", "Panel_City_TanTL_Style" )
		screen.hide( "TopCityPanelLeft" )

		screen.addPanel( "TopCityPanelRight", u"", u"", True, False, xResolution/2, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelRight", "Panel_City_TanTR_Style" )
		screen.hide( "TopCityPanelRight" )

		# Top Bar

		# SF CHANGE
		screen.addPanel( "CityScreenTopWidget", u"", u"", True, False, 0, -2, xResolution, 41, PanelStyles.PANEL_STYLE_STANDARD )

		screen.setStyle( "CityScreenTopWidget", "Panel_TopBar_Style" )
		screen.hide( "CityScreenTopWidget" )

		# Top Center Title
		screen.addPanel( "CityNameBackground", u"", u"", True, False, 260, 31, xResolution - (260*2), 38, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityNameBackground", "Panel_City_Title_Style" )
		screen.hide( "CityNameBackground" )

		# Left Background Widget
		screen.addDDSGFC( "InterfaceLeftBackgroundWidget", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOTTOM_LEFT").getPath(), 0, yResolution - 164, 304, 164, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Center Background Widget
		screen.addPanel( "InterfaceCenterBackgroundWidget", u"", u"", True, False, 296, yResolution - 133, xResolution - (296*2), 133, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceCenterBackgroundWidget", "Panel_Game_HudBC_Style" )
		screen.hide( "InterfaceCenterBackgroundWidget" )

		# Left Background Widget
		screen.addPanel( "InterfaceLeftBackgroundWidget", u"", u"", True, False, 0, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceLeftBackgroundWidget", "Panel_Game_HudBL_Style" )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Right Background Widget
		screen.addPanel( "InterfaceRightBackgroundWidget", u"", u"", True, False, xResolution - 304, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceRightBackgroundWidget", "Panel_Game_HudBR_Style" )
		screen.hide( "InterfaceRightBackgroundWidget" )

		# Top Center Background

		# SF CHANGE
		screen.addPanel( "InterfaceTopCenter", u"", u"", True, False, 273, -2, xResolution - 546, 48, PanelStyles.PANEL_STYLE_STANDARD)

		screen.setStyle( "InterfaceTopCenter", "Panel_Game_HudTC_Style" )
		screen.hide( "InterfaceTopCenter" )

		# Top Left Background
		screen.addPanel( "InterfaceTopLeft", u"", u"", True, False, 0, -2, 283, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopLeft", "Panel_Game_HudTL_Style" )
		screen.hide( "InterfaceTopLeft" )

		# Top Right Background
		screen.addPanel( "InterfaceTopRight", u"", u"", True, False, xResolution - 283, -2, 283, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopRight", "Panel_Game_HudTR_Style" )
		screen.hide( "InterfaceTopRight" )

		# Info Panel
		screen.addPanel("APL_UNIT_INFO_PANE_ID", u"", u"", True, True, self.CFG_INFOPANE_X, screen.getYResolution() - 208, self.CFG_INFOPANE_DX, 1, PanelStyles.PANEL_STYLE_HUD_HELP)
		screen.hide("APL_UNIT_INFO_PANE_ID")

		# City Placement Mode Info Panel
		screen.addPanel("CIPS_INFO_PANE", u"", u"", True, True, 5, screen.getYResolution() - 208, 290, 1, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide("CIPS_INFO_PANE")

		#Unit Placement Button
		screen.setImageButton("UnitPlacementButton1", "Art/Interface/Buttons/UnitPlacement.dds", 27, yResolution - 166, 28, 28, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide("UnitPlacementButton1")
		screen.setStyle( "UnitPlacementButton1", "Button_HUDSmall_Style" )

		# Trade Resource Panel Button
		screen.setImageButton("TradeResourceButton1", "Art/Interface/Buttons/Trade_Resource.dds", 60, 25, 28, 28, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide("TradeResourceButton1")
		screen.setStyle( "TradeResourceButton1", "Button_HUDSmall_Style" )

		# Alerts Log Button
		screen.setImageButton("AlertsLogButton1", "Art/Interface/Buttons/AlertsLog.dds", 87, 25, 28, 28, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide("AlertsLogButton1")
		screen.setStyle( "AlertsLogButton1", "Button_HUDSmall_Style" )

		iBtnWidth	= 28
		iBtnAdvance = 25
		iBtnY = 27
		iBtnX = 27

		# Turn log Button
		screen.setImageButton( "TurnLogButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
		screen.setStyle( "TurnLogButton", "Button_HUDLog_Style" )
		screen.hide( "TurnLogButton" )

		iBtnX = xResolution - 277

		# Advisor Buttons...
		screen.setImageButton( "DomesticAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "DomesticAdvisorButton", "Button_HUDAdvisorDomestic_Style" )
		screen.hide( "DomesticAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "FinanceAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FINANCIAL_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "FinanceAdvisorButton", "Button_HUDAdvisorFinance_Style" )
		screen.hide( "FinanceAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "CivicsAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVICS_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CivicsAdvisorButton", "Button_HUDAdvisorCivics_Style" )
		screen.hide( "CivicsAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "ForeignAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ForeignAdvisorButton", "Button_HUDAdvisorForeign_Style" )
		screen.hide( "ForeignAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "MilitaryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "MilitaryAdvisorButton", "Button_HUDAdvisorMilitary_Style" )
		screen.hide( "MilitaryAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "TechAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1 )
		screen.setStyle( "TechAdvisorButton", "Button_HUDAdvisorTechnology_Style" )
		screen.hide( "TechAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "ReligiousAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RELIGION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ReligiousAdvisorButton", "Button_HUDAdvisorReligious_Style" )
		screen.hide( "ReligiousAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "CorporationAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CORPORATION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CorporationAdvisorButton", "Button_HUDAdvisorCorporation_Style" )
		screen.hide( "CorporationAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "VictoryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "VictoryAdvisorButton", "Button_HUDAdvisorVictory_Style" )
		screen.hide( "VictoryAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "InfoAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1 )
		screen.setStyle( "InfoAdvisorButton", "Button_HUDAdvisorRecord_Style" )
		screen.hide( "InfoAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
		screen.hide( "EspionageAdvisorButton" )

		# City Tabs
		iBtnX = xResolution - 324
		iBtnY = yResolution - 94
		iBtnWidth = 24
		iBtnAdvance = 24

		screen.setButtonGFC( "CityTab0", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab0", "Button_HUDJumpUnit_Style" )
		screen.hide( "CityTab0" )

		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab1", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab1", "Button_HUDJumpBuilding_Style" )
		screen.hide( "CityTab1" )

		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab2", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 2, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab2", "Button_HUDJumpWonder_Style" )
		screen.hide( "CityTab2" )

		# Minimap initialization
		screen.setMainInterface(True)

		screen.addPanel( "MiniMapPanel", u"", u"", True, False, xResolution - 214, yResolution - 151, 208, 151, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "MiniMapPanel", "Panel_Game_HudMap_Style" )
		screen.hide( "MiniMapPanel" )

		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )
		gc.getMap().updateMinimapColor()

		self.createMinimapButtons()

		# Help button (always visible)
		screen.setImageButton( "InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), xResolution - 28, 2, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1 )
		screen.hide( "InterfaceHelpButton" )

		screen.setImageButton( "MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), xResolution - 50, 2, 24, 24, WidgetTypes.WIDGET_MENU_ICON, -1, -1 )
		screen.hide( "MainMenuButton" )

		# Globeview buttons
		self.createGlobeviewButtons( )

		width = xResolution - (iMultiListXL+iMultiListXR)
		height = 100
		if (g_BottomContIconSize == 34):
			height = 110
		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, width, height, 4, g_BottomContIconSize, g_BottomContIconSize, TableStyles.TABLE_STYLE_STANDARD )
		self.BottomContainerSize = (xResolution, yResolution, g_BottomContIconSize)
		screen.hide( "BottomButtonContainer" )

		screen.addCheckBoxGFC("AutoInsertQueueButton1", "Art/Interface/Buttons/autoinsertqueue.dds", "", iMultiListXR - 36, yResolution - 113, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.hide("AutoInsertQueueButton1")

		# *********************************************************************************
		# PLOT LIST BUTTONS
		# *********************************************************************************

		if (self.CFG_Enabled_APL):
			iMaxPlotListIcons = self.getMaxCol() * self.getMaxRow()
			iDenom = (self.xResolution - iMultiListXOffset) / 38
			iYoffset = self.yResolution - 179

			for i in xrange(iMaxPlotListIcons):

				#x = self.getX(self.getCol(i))
				#y = self.getY(self.getRow(i))
				x =  315 + (i % iDenom) * 36
				y = iYoffset - (i / iDenom) * 44

				szString = "PlotListButton" + str(i)

				szStringTemp = szString + "Health"
				screen.addStackedBarGFC(szStringTemp, x+5, y-7, 28, 11, 2, WidgetTypes.WIDGET_GENERAL, i, -1)
				screen.setStackedBarColors(szStringTemp, InfoBarTypes.INFOBAR_STORED, self.CFG_STACKEDBAR_HEALTH_COL)
				screen.setStackedBarColors(szStringTemp, InfoBarTypes.INFOBAR_RATE, self.CFG_STACKEDBAR_WOUNDED_COL)
				screen.setBarPercentage(szStringTemp, InfoBarTypes.INFOBAR_RATE, 1.0)
				screen.setBarPercentage(szStringTemp, InfoBarTypes.INFOBAR_STORED, 1.0)
				screen.hide(szStringTemp)

				screen.addCheckBoxGFC(szString, "", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, i, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.hide(szString)

				szStringTemp = szString + "Upgrade"
				screen.addDDSGFC(szStringTemp, "", x-3, y + 18, 12, 12, WidgetTypes.WIDGET_GENERAL, i, -1)
				screen.hide(szStringTemp)

			self.preparePlotListObjects()

			self.setAPLMode()
			self.setAPLGrpMode()
		else:
			for j in xrange(gc.getMAX_PLOT_LIST_ROWS()):
				yRow = (j - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34
				yPixel = yResolution - 169 + yRow - 3
				xPixel = 315 - 3
				xWidth = self.numPlotListButtons() * 34 + 3
				yHeight = 32 + 3

				szStringPanel = "PlotListPanel" + str(j)
				screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

				for i in xrange(self.numPlotListButtons()):
					k = j*self.numPlotListButtons()+i

					xOffset = i * 34

					szString = "PlotListButton" + str(k)
					screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
					screen.hide( szString )

					szStringHealth = szString + "Health"
					screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 26, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
					screen.hide( szStringHealth )

					szStringIcon = szString + "Icon"
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
					screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
					screen.hide( szStringIcon )

		# End Turn Text
		screen.setLabel( "EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - 188, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "EndTurnText", HitTestTypes.HITTEST_NOHIT )

		# Three states for end turn button...
		screen.setImageButton( "EndTurnButton", "", xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_END_TURN, -1, -1 )
		screen.setStyle( "EndTurnButton", "Button_HUDEndTurn_Style" )
		screen.setEndTurnState( "EndTurnButton", "Red" )
		screen.hide( "EndTurnButton" )

		# *********************************************************************************
		# RESEARCH BUTTONS
		# *********************************************************************************

		for i in xrange( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.setImageButton( szName, gc.getTechInfo(i).getButton(), 0, 0, 28, 28, WidgetTypes.WIDGET_RESEARCH, i, -1 )
			screen.hide( szName )

		for i in xrange(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
				szButton = gc.getReligionInfo(i).getGenericTechButton()
			else:
				szButton = gc.getReligionInfo(i).getTechButton()
			screen.setImageButton( szName, szButton, 0, 0, 28, 28, WidgetTypes.WIDGET_RESEARCH, gc.getReligionInfo(i).getTechPrereq(), -1 )
			screen.hide( szName )

		screen.addPanel("ResearchButtonBackgroundPanel", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP)
		screen.hide("ResearchButtonBackgroundPanel")

		##### <written by F > #####
		
		# *********************************************************************************
		# TOHO UNIT BUTTONS
		# *********************************************************************************
		
		i = 0
		for i in range( gc.getNumUnitInfos() ):
			if gc.getUnitInfo(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or gc.getUnitInfo(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
				szName = "TohoUnitButton" + str(i)
				pediaID = i - ( ( i - gc.getInfoTypeForString('UNIT_SANAE0') ) % 7 ) + 1
				screen.setImageButton( szName, gc.getUnitInfo(i).getButton(), 0, 0, 16, 16, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TOHOUNIT, pediaID, -1 )
				screen.hide( szName )
		
		for i in range( gc.getNumUnitInfos() ):
			if gc.getUnitInfo(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or gc.getUnitInfo(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
				szName = "TohoUnitButton" + str(i)
				pediaID = i - ( ( i - gc.getInfoTypeForString('UNIT_SANAE0') ) % 7 ) + 1
				screen.setImageButton( szName, gc.getUnitInfo(i).getButton(), 0, 0, 16, 16, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TOHOUNIT, pediaID, -1 )
				screen.hide( szName )

		##### </written by F > #####

		# *********************************************************************************
		# CITIZEN BUTTONS
		# *********************************************************************************

		szHideCitizenList = []

		# Angry Citizens
		for i in xrange(MAX_CITIZEN_BUTTONS):
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - 74 - (26 * i), yResolution - 238, 24, 24, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.hide( szName )

		iCount = 0

		# Increase Specialists...
		for i in xrange( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "IncreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 46, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Decrease specialists
		for i in xrange( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "DecreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 24, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Citizen Buttons
		for i in xrange( gc.getNumSpecialistInfos() ):

			if (gc.getSpecialistInfo(i).isVisible()):

				szName = "CitizenDisabledButton" + str(i)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), xResolution - 74, (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_DISABLED_CITIZEN, i, -1 )
				screen.enable( szName, False )
				screen.hide( szName )

				for j in xrange(MAX_CITIZEN_BUTTONS):
					szName = "CitizenButton" + str((i * 100) + j)
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.hide( szName )

		# **********************************************************
		# GAME DATA STRINGS
		# **********************************************************

		TradeResourcePanel.TradeResourcePanel().createTradeResourcePanels()
		CityInfoPanelPS.CityInfoPanelPS().createCityInfoPanelPS()

		screen.addStackedBarGFC( "ResearchBar", 283 + ( (xResolution - 1024) / 2 ), 2, 457, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar" )

		if (CFG_Combat_Experience_Counter):
			screen.addStackedBarGFC("CombatXPBar", 171, 16, 100, 22, 2, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
			screen.setStackedBarColors("CombatXPBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors("CombatXPBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			eCombatXPButton = "<img=" + gc.getUnitInfo(gc.getInfoTypeForString("UNIT_GREAT_GENERAL")).getButton() + " size=16></img>"
			screen.setLabel("CombatXPButton", "Background", eCombatXPButton, CvUtil.FONT_RIGHT_JUSTIFY, 171, 20, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
			screen.hide("CombatXPBar")
			screen.hide("CombatXPButton")

		if (CFG_Show_GameTurn_Bar):
			if (gc.getGame().getMaxTurns() > 0):
				screen.addStackedBarGFC("GameTurnBar", xResolution - 271, 18, 221, 11, 2, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setStackedBarColors("GameTurnBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
				screen.setStackedBarColors("GameTurnBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
				screen.hide("GameTurnBar")
			else:
				CFG_Show_GameTurn_Bar = False

		if (CFG_Show_GreatPerson_Bar):
			screen.addStackedBarGFC("GreatPersonBar", 5, 50, 266, 24, 2, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1)
			screen.setStackedBarColors("GreatPersonBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors("GreatPersonBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.hide("GreatPersonBar")

		# *********************************************************************************
		# SELECTION DATA BUTTONS/STRINGS
		# *********************************************************************************

		screen.addStackedBarGFC( "PopulationBar", iCityCenterRow1X, iCityCenterRow1Y-4, xResolution - (iCityCenterRow1X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColorsAlpha( "PopulationBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), 0.8 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "PopulationBar" )

		screen.addStackedBarGFC( "ProductionBar", iCityCenterRow2X, iCityCenterRow2Y-4, xResolution - (iCityCenterRow2X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_PRODUCTION, -1, -1 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType() )
		screen.setStackedBarColorsAlpha( "ProductionBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), 0.8 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ProductionBar" )

		screen.addStackedBarGFC( "GreatPeopleBar", xResolution - 246, yResolution - 184, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPeopleBar" )

		screen.addStackedBarGFC( "CultureBar", 16, yResolution - 188, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_CULTURE, -1, -1 )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CULTURE_STORED") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "CultureBar" )

		# Holy City Overlay
		for i in xrange( gc.getNumReligionInfos() ):
			xCoord = xResolution - 242 + (i * 34)
			yCoord = 42
			szName = "ReligionHolyCityDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
			screen.hide( szName )

		for i in xrange( gc.getNumCorporationInfos() ):
			xCoord = xResolution - 242 + (i * 34)
			yCoord = 66
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
			screen.hide( szName )

		screen.addStackedBarGFC( "NationalityBar", 16, yResolution - 214, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_NATIONALITY, -1, -1 )
		screen.hide( "NationalityBar" )

		screen.setButtonGFC( "CityScrollMinus", u"", "", 274, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "CityScrollMinus" )

		screen.setButtonGFC( "CityScrollPlus", u"", "", 288, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "CityScrollPlus" )

		if (self.CFG_Enabled_APL):
			screen.setButtonGFC( self.PLOT_LIST_MINUS_NAME, u"", "", 325 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
			screen.hide( self.PLOT_LIST_MINUS_NAME )
			screen.setButtonGFC( self.PLOT_LIST_PLUS_NAME, u"", "", 308 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
			screen.hide( self.PLOT_LIST_PLUS_NAME )

			screen.setImageButton( self.PLOT_LIST_UP_NAME, ArtFileMgr.getInterfaceArtInfo("APL_ARROW_UP").getPath(), 325 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.hide( self.PLOT_LIST_UP_NAME )
			screen.setImageButton( self.PLOT_LIST_DOWN_NAME, ArtFileMgr.getInterfaceArtInfo("APL_ARROW_DOWN").getPath(), 308 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.hide( self.PLOT_LIST_DOWN_NAME )
		else:
			screen.setButtonGFC( "PlotListMinus", u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
			screen.hide( "PlotListMinus" )
			screen.setButtonGFC( "PlotListPlus", u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
			screen.hide( "PlotListPlus" )



## Sevo - Raw Commerce Display - begin
		if (CFG_RAWCOMMERCEDISPLAY):
			screen.addPanel("TradeRouteListBackground", u"", u"", True, False, 10, 247, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
			screen.setStyle("TradeRouteListBackground", "Panel_City_Header_Style" )
			screen.hide("TradeRouteListBackground" )

			screen.setLabel("TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 255, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.hide("TradeRouteListLabel" )

			screen.addPanel("BuildingListBackground", u"", u"", True, False, 10, 377, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
			screen.setStyle("BuildingListBackground", "Panel_City_Header_Style" )
			screen.hide("BuildingListBackground" )

			screen.setLabel("BuildingListLabel", "Background", localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 385, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.hide("BuildingListLabel" )
## Sevo - Raw Commerce Display - end
		else:
			screen.addPanel( "TradeRouteListBackground", u"", u"", True, False, 10, 157, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
			screen.setStyle( "TradeRouteListBackground", "Panel_City_Header_Style" )
			screen.hide( "TradeRouteListBackground" )

			screen.setLabel( "TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 165, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.hide( "TradeRouteListLabel" )

			screen.addPanel( "BuildingListBackground", u"", u"", True, False, 10, 287, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
			screen.setStyle( "BuildingListBackground", "Panel_City_Header_Style" )
			screen.hide( "BuildingListBackground" )

			screen.setLabel( "BuildingListLabel", "Background", localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 295, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.hide( "BuildingListLabel" )
## Sevo - Raw Commerce Display - end (else)

		# *********************************************************************************
		# UNIT INFO ELEMENTS
		# *********************************************************************************

		for i in xrange(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.addDDSGFC( szName, gc.getPromotionInfo(i).getButton(), 180, yResolution - 18, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(i).getActionInfoIndex(), -1 )
			screen.hide( szName )

		# *********************************************************************************
		# SCORES
		# *********************************************************************************

		screen.addPanel( "ScoreBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ScoreBackground" )

		for i in xrange( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, i, -1 )
			screen.hide( szName )
			# Attitude Font
			szPlayerName = "ScoreAttFont" + str(i) + "_"
			for iAtt in xrange(AttitudeTypes.NUM_ATTITUDE_TYPES):
				szName = szPlayerName + str(iAtt)
				screen.addDDSGFC(szName, "Art/Interface/Buttons/AttFonts/AttFontS" + str(iAtt) + ".dds", 0, 0, 14, 14, WidgetTypes.WIDGET_CONTACT_CIV, i, -1)
				screen.hide(szName)
				szName = szName + "WE"
				screen.addDDSGFC(szName, "Art/Interface/Buttons/AttFonts/AttFontS" + str(iAtt) + "WE.dds", 0, 0, 14, 14, WidgetTypes.WIDGET_CONTACT_CIV, i, -1)
				screen.hide(szName)

		# This should be a forced redraw screen
		screen.setForcedRedraw( True )

		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

		szHideList = []

		szHideList.append( "CreateGroup" )
		szHideList.append( "DeleteGroup" )

		# City Tabs
		for i in xrange( g_NumCityTabTypes ):
			szButtonID = "CityTab" + str(i)
			szHideList.append( szButtonID )

		for i in xrange( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			szHideList.append( szButtonID )

		szHideList.append( "Hurry0" )
		szHideList.append( "Hurry1" )

		screen.registerHideList( szHideList, len(szHideList), 0 )

		return 0

	# Will update the screen (every 250 MS)
	def updateScreen(self):

		global g_szTimeText
		global g_iTimeTextCounter
		global g_szOldTimeText

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		self.m_iNumPlotListButtons = (xResolution - iMultiListXOffset) / 34

		# This should recreate the minimap on load games and returns if already exists -JW
		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )

		messageControl = CyMessageControl()

		bShow = False

		# Hide all interface widgets
		interfaceObj = CyInterface()
		iInterfaceState = CyInterface().getShowInterface()

		if (iInterfaceState != InterfaceVisibility.INTERFACE_HIDE_ALL and iInterfaceState != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
			if (gc.getGame().isPaused()):
				# Pause overrides other messages
				acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
				screen.setEndTurnState( "EndTurnText", acOutput )
				bShow = True
			elif (messageControl.GetFirstBadConnection() != -1):
				# Waiting on a bad connection to resolve
				if (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
			else:
				# Flash select messages if no popups are present
				if ( interfaceObj.shouldDisplayReturn() ):
					screen.setEndTurnState("EndTurnText", localText.getText("SYSTEM_RETURN", ()))
					bShow = True
				elif ( interfaceObj.shouldDisplayWaitingOthers() ):
					screen.setEndTurnState("EndTurnText", localText.getText("SYSTEM_WAITING", ()))
					bShow = True
				elif ( interfaceObj.shouldDisplayEndTurn() ):
					screen.setEndTurnState("EndTurnText", localText.getText("SYSTEM_END_TURN", ()))
					bShow = True
				elif ( interfaceObj.shouldDisplayWaitingYou() ):
					screen.setEndTurnState("EndTurnText", localText.getText("SYSTEM_WAITING_FOR_YOU", ()))
					bShow = True

		if ( bShow ):
			screen.showEndTurn( "EndTurnText" )
			if (iInterfaceState == InterfaceVisibility.INTERFACE_SHOW or interfaceObj.isCityScreenUp()):
				screen.moveItem( "EndTurnText", 0, yResolution - 194, -0.1 )
			else:
				screen.moveItem( "EndTurnText", 0, yResolution - 86, -0.1 )
		else:
			screen.hideEndTurn( "EndTurnText" )

		self.updateEndTurnButton()

		if (iInterfaceState != InterfaceVisibility.INTERFACE_HIDE_ALL and iInterfaceState != InterfaceVisibility.INTERFACE_ADVANCED_START):
			# < NJAGCM Start > 
			# Only display the alternating text if the g_bAlternateTimeText is set to True
			if (g_bAlternateTimeText):
				# If clock was just turned on then display the clock text immediately instead of waiting the normal amt of time
				if (CyUserProfile().wasClockJustTurnedOn()):
					g_iTimeTextCounter = g_iAlternatingTime
					CyUserProfile().setClockJustTurnedOn(False)

				if (g_iTimeTextCounter >= (g_iAlternatingTime*2)):	# g_iAlternatingTime seconds
					g_iTimeTextCounter = 0.0
					self.updateTimeText(False)
					screen.setLabel("TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 52, 4, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.show( "TimeText" )
				elif (g_iTimeTextCounter >= g_iAlternatingTime):	# Another g_iAlternatingTime Seconds
					self.updateTimeText(True)
					screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 52, 4, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "TimeText" )

				g_iTimeTextCounter += 0.25
			else:
				self.updateTimeText(g_bShowTurns)
				if (g_szTimeText != g_szOldTimeText):
					screen.setLabel("TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 52, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					g_szOldTimeText = g_szTimeText
				screen.show("TimeText")
			# < NJAGCM End >
		else:
			screen.hide( "TimeText" )

		if (self.CFG_Enabled_APL):
			if (self.bInfoPaneActive):
				tMousePos = interfaceObj.getMousePos()
				if (not ((self.tLastMousePos[0] < tMousePos.x < self.tLastMousePos[2]) and (self.tLastMousePos[1] < tMousePos.y < self.tLastMousePos[3]))):
					self.hideInfoPane()

		return 0

	# Will redraw the interface
	def redraw(self):
		# Check Dirty Bits, see what we need to redraw...
		if (CyInterface().isDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT)):
			# Percent Buttons
			self.updatePercentButtons()
			if (CyInterface().isScreenUp(CvScreenEnums.DOMESTIC_ADVISOR)):
				CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Flag_DIRTY_BIT)):
			# Percent Buttons
			self.updateFlag()
			CyInterface().setDirty(InterfaceDirtyBits.Flag_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT)):
			# Miscellaneous buttons (civics screen, etc)
			self.updateMiscButtons()
			CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT)):
			# Info Pane Dirty Bit
			# This must come before updatePlotListButtons so that the entity widget appears in front of the stats
			self.updateInfoPaneStrings()
			# Plot List Buttons Dirty for Promotions.
			if (not bCompressMode and not CyInterface().getHeadSelectedCity() and not CyEngine().isGlobeviewUp()):
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT)):
			# Plot List Buttons Dirty
			self.updatePlotListButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT)):
			# Selection Buttons Dirty
			self.updateSelectionButtons()
			CityInfoPanelPS.CityInfoPanelPS().hideCityInfoPanelPS()
			if (CyInterface().isScreenUp(CvScreenEnums.DOMESTIC_ADVISOR)):
				CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT)):
			# Research Buttons Dirty
			self.updateResearchButtons()
			CyInterface().setDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT)):
			# Citizen Buttons Dirty
			self.updateCitizenButtons()
			CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT)):
			# Game Data Strings Dirty
			self.updateGameDataStrings()
			TradeResourcePanel.TradeResourcePanel().updateTradeResourcePanels(False)
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT)):
			# Help Dirty bit
			self.updateHelpStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT)):
			# Selection Data Dirty Bit
			self.updateCityScreen()
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) or CyInterface().checkFlashUpdate()):
			# Scores!
			self.updateScoreStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT)):
			# Globeview and Globelayer buttons
			CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
			self.updateGlobeviewButtons()
			TradeResourcePanel.TradeResourcePanel().updateTradeResourcePanelsWithGloveView()

		return 0

	# Will update the percent buttons
	def updatePercentButtons(self):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			screen.hide("IncreasePercent" + str(iI))
			screen.hide("DecreasePercent" + str(iI))

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		bCityScreenUp = CyInterface().isCityScreenUp()

		if ( not bCityScreenUp or ( pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() ) or gc.getGame().isDebugMode() ):
			iCount = 0

			if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
				if (CFG_Show_GreatPerson_Bar and not bCityScreenUp):
					iPercentY = iPercentWithGPBY
				else:
					iPercentY = 50

				for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
					# Intentional offset...
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES

					if (gc.getActivePlayer().isCommerceFlexible(eCommerce) or (bCityScreenUp and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						szString1 = "IncreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString1, u"", "", 70, iPercentY + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
						screen.show(szString1)
						szString2 = "DecreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString2, u"", "", 90, iPercentY + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )
						screen.show(szString2)

						iCount = iCount + 1

						if (gc.getActivePlayer().isCommerceFlexible(eCommerce)):
							screen.enable( szString1, True )
							screen.enable( szString2, True )
						else:
							screen.enable( szString1, False )
							screen.enable( szString2, False )

		return 0

	# Will update the end Turn Button
	def updateEndTurnButton( self ):

		global g_eEndTurnButtonState

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):

			eState = CyInterface().getEndTurnState()

			if ( eState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				screen.showEndTurn( "EndTurnButton" )
			elif ( eState == EndTurnButtonStates.END_TURN_OVER_DARK ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				screen.showEndTurn( "EndTurnButton" )
			elif ( eState == EndTurnButtonStates.END_TURN_GO ):
				screen.setEndTurnState( "EndTurnButton", u"Green" )
				screen.showEndTurn( "EndTurnButton" )
			else:
				screen.hideEndTurn( "EndTurnButton" )

			if ( g_eEndTurnButtonState != eState ):
				g_eEndTurnButtonState = eState

		else:
			screen.hideEndTurn( "EndTurnButton" )

		return 0

	# Update the miscellaneous buttons
	def updateMiscButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.show( "CivilizationFlag" )
			screen.show( "InterfaceHelpButton" )
			screen.show( "MainMenuButton" )
			if (self.CFG_Enabled_APL):
				self.showPlotListButtonObjects()
		else:
			screen.hide( "CivilizationFlag" )
			screen.hide( "InterfaceHelpButton" )
			screen.hide( "MainMenuButton" )
			if (self.CFG_Enabled_APL):
				self.hidePlotListButtonObjects()
				self.hidePlotListButtons()

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.hide( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
			screen.hide("UnitPlacementButton1")
			screen.hide("TradeResourceButton1")
			screen.hide("AlertsLogButton1")
			if (self.CFG_Enabled_APL):
				self.hidePlotListButtonObjects()
				self.hidePlotListButtons()

		elif ( CyInterface().isCityScreenUp() ):
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
			screen.hide("UnitPlacementButton1")
			screen.hide("TradeResourceButton1")
			screen.hide("AlertsLogButton1")
			if (self.CFG_Enabled_APL):
				self.showPlotListButtonObjects()

		elif ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.hide( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
			screen.hide("UnitPlacementButton1")
			screen.show("TradeResourceButton1")
			screen.moveToFront("TradeResourceButton1")
			screen.show("AlertsLogButton1")
			screen.moveToFront("AlertsLogButton1")
			if (self.CFG_Enabled_APL):
				self.hidePlotListButtonObjects()
				self.hidePlotListButtons()

		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
			screen.hide("UnitPlacementButton1")
			screen.hide("TradeResourceButton1")
			screen.hide("AlertsLogButton1")
			if (self.CFG_Enabled_APL):
				self.hidePlotListButtonObjects()
				self.hidePlotListButtons()

		elif ( CyEngine().isGlobeviewUp() ):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
			screen.hide("UnitPlacementButton1")
			screen.show("TradeResourceButton1")
			screen.moveToFront("TradeResourceButton1")
			screen.show("AlertsLogButton1")
			screen.moveToFront("AlertsLogButton1")
			if (self.CFG_Enabled_APL):
				self.hidePlotListButtonObjects()
				self.hidePlotListButtons()

		else:
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
			screen.show("UnitPlacementButton1")
			screen.moveToFront("UnitPlacementButton1")
			screen.show("TradeResourceButton1")
			screen.moveToFront("TradeResourceButton1")
			screen.show("AlertsLogButton1")
			screen.moveToFront("AlertsLogButton1")
			if (self.CFG_Enabled_APL):
				self.showPlotListButtonObjects()

		screen.updateMinimapVisibility()

		return 0

	# Update plot List Buttons
	def updatePlotListButtons(self):
		global listAPLButtons
		global bCompressMode
		global bPrevCompMode
		global listPrevAPLButtons
		global listPrevAPLUpgradeIndicator
		global listPrevAPLHealthBar
		global listPrevAPLSpotIcons
		global bShowWarlordIndicator
		global bShowActionIcons

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		bAtWar = gc.getTeam(gc.getGame().getActiveTeam()).getAtWarCount(False) > 0
		if (self.CFG_Enabled_APL):
			xResolution = self.xResolution
			yResolution = self.yResolution
			if (CFG_Enabled_Compress_Mode and CyInterface().shouldDisplayWaitingOthers() and not bAtWar and CyInterface().getNumVisibleUnits() > 10):
				if (bCompressMode):
					return 0
				else:
					bCompressMode = True
		else:
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()

		bHandled = False
		if ( CyInterface().shouldDisplayUnitModel() and CyEngine().isGlobeviewUp() == false and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
			if ( CyInterface().isCitySelection() ):

				iOrders = CyInterface().getNumOrdersQueued()

				for i in xrange( iOrders ):
					eOrderNodeType = CyInterface().getOrderNodeType(i)
					if (eOrderNodeType  == OrderTypes.ORDER_TRAIN ):
						screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 193, yResolution - 138, 100, 122, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.9, False )
						bHandled = True
						break
					elif ( eOrderNodeType == OrderTypes.ORDER_CONSTRUCT ):
						screen.addBuildingGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 193, yResolution - 138, 100, 122, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.7, False )
						bHandled = True
						break
					elif ( eOrderNodeType == OrderTypes.ORDER_CREATE ):
						if(gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).isSpaceship()):
							modelType = 0
							screen.addSpaceShipWidgetGFC("InterfaceUnitModel", 193, yResolution - 138, 100, 122, CyInterface().getOrderNodeData1(i), modelType, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
						else:
							screen.hide( "InterfaceUnitModel" )
						bHandled = True
						break
					elif ( eOrderNodeType == OrderTypes.ORDER_MAINTAIN ):
						screen.hide( "InterfaceUnitModel" )
						bHandled = True
						break

				if ( not bHandled ):
					screen.hide( "InterfaceUnitModel" )
					bHandled = True

				screen.moveToFront("SelectedCityText")

			elif ( CyInterface().getHeadSelectedUnit() ):
				screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit().getUnitType(), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
				screen.moveToFront("SelectedUnitText")
			else:
				screen.hide( "InterfaceUnitModel" )
		else:
			screen.hide( "InterfaceUnitModel" )

		pPlot = CyInterface().getSelectionPlot()

		for i in xrange(gc.getNumPromotionInfos()):
			screen.moveToFront("PromotionButton" + str(i))

		if (self.CFG_Enabled_APL):
			# if the plot change, reset plot list offset
			if (self.pOldPlot):
				# check if plot has changed
				if (self.pOldPlot.getX() != pPlot.getX()) or (self.pOldPlot.getY() != pPlot.getY()):
					self.pOldPlot = pPlot
					self.iColOffset = 0
					self.iRowOffset = 0
			else:
				# initialization
				self.pOldPlot = pPlot

			if ((self.nAPLGrpMode == self.APL_GRP_GROUPS) and self.bAPLSelectOnly):
				self.bAPLSelectOnly = False

			if (not self.bAPLHide and not self.bAPLSelectOnly):
				self.hidePlotListButtons()

			tempAPLButtonList = []
			tempAPLButtonListappend = tempAPLButtonList.append

			if (pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and not CyEngine().isGlobeviewUp()):

				if (self.bAPLSelectOnly):
					pGetPlayer = gc.getPlayer
					for iCount, (iOwner, iID) in listAPLButtons.items():
						screen.setState("PlotListButton" + str(iCount), pGetPlayer(iOwner).getUnit(iID).IsSelected())

					self.bAPLSelectOnly = False
					self.bAPLHide = False
					return 0
				else:
					listAPLButtons.clear()

				nRow = 0
				nCol = 0
				iVisibleUnits = CyInterface().getNumVisibleUnits()
				MaxCol = self.getMaxCol()
				MaxRow = self.getMaxRow()

				bUpArrow = False
				bDownArrow = False
				bFirstLoop = True
				bLeftArrow = False
				bRightArrow = False

				if (self.sAPLMode == self.APL_MODE_MULTILINE):
					if (self.iRowOffset > 0):
						bDownArrow = True
				elif (self.sAPLMode == self.APL_MODE_STACK_VERT):
					nCol = -self.iColOffset
					if (self.iColOffset > 0):
						bLeftArrow = True
				elif (self.sAPLMode == self.APL_MODE_STACK_HORIZ):
					nRow = -self.iRowOffset
					if (self.iRowOffset > 0):
						bDownArrow = True

				iLastUnitType = UnitTypes.NO_UNIT
				iLastGroupID  = 0
				iCount = 0

				# loop for all units on the plot
				bMultiMode = (self.sAPLMode == self.APL_MODE_MULTILINE)
				bVertMode = (self.sAPLMode == self.APL_MODE_STACK_VERT)
				bHorizMode = (self.sAPLMode == self.APL_MODE_STACK_HORIZ)
				bTypeMode = (self.nAPLGrpMode == self.APL_GRP_UNITTYPE)
				bGrpMode = (self.nAPLGrpMode == self.APL_GRP_GROUPS)
				bPromoMode = (self.nAPLGrpMode == self.APL_GRP_PROMO)
				bUpgradeMode = (self.nAPLGrpMode == self.APL_GRP_UPGRADE)

				if (CyInterface().isCityScreenUp()):
					bPrevCompMode = bCompressMode
					bCompressMode = True
				elif (not bPrevCompMode):
					bCompressMode = bPrevCompMode
					bPrevCompMode = True
				if (CFG_Enabled_Compress_Mode and not CyInterface().isCityScreenUp() and (not (iVisibleUnits > 10)  or bAtWar)):
					bCompressMode = False

				if (bCompressMode):
					global bCompressShow

					self.bAPLHide = False
					bCompressShow = True
					iYOffset = self.yResolution - 179
					ActivePlayer = gc.getGame().getActivePlayer()

					if (self.iRowOffset > 0):
						bDownArrow = True
					UnitTypeCount = dict()
					getUnitTypeHasKey = UnitTypeCount.has_key
					CyInterface().cacheInterfacePlotUnits(pPlot)
					getPlotUnit = CyInterface().getCachedInterfacePlotUnit
					for i in xrange(CyInterface().getNumCachedInterfacePlotUnits()):
						pLoopUnit = getPlotUnit(i)
						if (pLoopUnit):
							iOwner = pLoopUnit.getOwner()
							iUnitType = pLoopUnit.getUnitType()
							if (getUnitTypeHasKey((iOwner, iUnitType))):
								UnitTypeCount[(iOwner, iUnitType)] += 1
							else:
								UnitTypeCount[(iOwner, iUnitType)] = 1

					for iCount, ((iOwner, iUnitType), iUnitCount) in enumerate(UnitTypeCount.items()):
						if (nCol >= MaxCol):
								bRightArrow = True

						nCol = self.getCol(iCount)
						nRow = self.getRow(iCount) - self.iRowOffset
						if ((iCount < iVisibleUnits) and (0 <= nRow < MaxRow)):
							listAPLButtons[iCount] = (iOwner, iUnitType)
							x = 315 + nCol * 36
							y = iYOffset - nRow * 44

							szString = "PlotListButton" + str(iCount)
							# set unit button image
							if (iUnitType != listPrevAPLButtons.get(iCount)):
								screen.changeImageButton(szString, gc.getPlayer(iOwner).getUnitButton(iUnitType))
								listPrevAPLButtons[iCount] = iUnitType

							# check if it is an player unit or not
							screen.enable(szString, (iOwner == ActivePlayer))
							screen.setState(szString, False)
							screen.show(szString)

							# add the number of unit text
							szText = u"<font=1>" + str(iUnitCount) + u"</font>"
							screen.setButtonGFC(szString + "Num", szText,"", x + 22, y + 24, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)

				else:
					CyInterface().cacheInterfacePlotUnits(pPlot)
					self.checkDisplayFilterUnitList(False, False)
					for iCount, (iOwner, iID, iLoopUnitType, iLoopGroupID) in enumerate(self.lFilteredUnitList):

						# multiline view
						if (bMultiMode):
							if (nRow >= MaxRow):
								bUpArrow = True

							nCol = self.getCol(iCount)
							nRow = self.getRow(iCount) - self.iRowOffset
							if ((iCount < iVisibleUnits) and (0 <= nRow < MaxRow)):
								tempAPLButtonListappend((iOwner, iID, nRow, nCol))

						# vertical stack view
						elif (bVertMode):
							if (nCol >= MaxCol):
								bRightArrow = True

							if (bTypeMode):
								if (iLastUnitType != UnitTypes.NO_UNIT):
									if (iLoopUnitType != iLastUnitType):
										nCol += 1
										nRow = 0
									else:
										nRow += 1
										if (nRow >= MaxRow):
											nRow = 0
											nCol += 1
							elif (bGrpMode):
								if (iLastGroupID != 0):
									if (iLoopGroupID != iLastGroupID):
										nCol += 1
										nRow = 0
									else:
										nRow += 1
										if (nRow >= MaxRow):
											nRow = 0
											nCol += 1
							elif (bPromoMode):
								nRow = 0
								if not bFirstLoop:
									nCol += 1
							elif (bUpgradeMode):
								nRow = 0
								if not bFirstLoop:
									nCol += 1

							if ((iCount < iVisibleUnits) and (0 <= nCol < MaxCol)):
								tempAPLButtonListappend((iOwner, iID, nRow, nCol))
								if (bPromoMode):
									self.displayUnitPromos(iOwner, iID, nRow, nCol)
								elif (bUpgradeMode):
									self.displayUnitUpgrades(iOwner, iID, nRow, nCol)

						# horizontal stack view
						elif (bHorizMode):
							if (nRow >= MaxRow):
								bUpArrow = True

							if (bTypeMode):
								if (iLastUnitType != UnitTypes.NO_UNIT):
									if (iLoopUnitType != iLastUnitType):
										nRow += 1
										nCol = 0
									else:
										nCol += 1
										if (nCol >= MaxCol):
											nCol = 0
											nRow += 1
							elif (bGrpMode):
								if (iLastGroupID != 0):
									if (iLoopGroupID != iLastGroupID):
										nRow += 1
										nCol = 0
									else:
										nCol += 1
										if (nCol >= MaxCol):
											nCol = 0
											nRow += 1
							elif (bPromoMode):
								nCol= 0
								if not bFirstLoop:
									nRow += 1
							elif (bUpgradeMode):
								nCol= 0
								if not bFirstLoop:
									nRow += 1

							if ((iCount < iVisibleUnits) and (0 <= nRow < MaxRow)):
								tempAPLButtonListappend((iOwner, iID, nRow, nCol))
								if (bPromoMode):
									self.displayUnitPromos(iOwner, iID, nRow, nCol)
								elif (bUpgradeMode):
									self.displayUnitUpgrades(iOwner, iID, nRow, nCol)

						iLastUnitType	= iLoopUnitType
						iLastGroupID	= iLoopGroupID
						bFirstLoop		= False

					screenShow = screen.show

					self.bAPLHide = False

					iYOffset = self.yResolution - 179#169
					ActivePlayer = gc.getGame().getActivePlayer()
					ActiveTeam = gc.getGame().getActiveTeam()
					UpgradePath = dict()
					szStringTemp = ""
					pGetPlayer = gc.getPlayer
					bPromoEnabled = int(self.CFG_PROMO_INDICATOR_ENABLED) * 2
					hasActivity = self.ActivityIconMap.has_key
					hasAutomate = self.AutomateIconMap.has_key
					hasMission = self.MissionIconMap.has_key

					for (iOwner, iID, nRow, nCol) in tempAPLButtonList:
						iCount = nRow * MaxCol + nCol % MaxCol
						pLoopUnit = pGetPlayer(iOwner).getUnit(iID)
						iLoopUnitType = pLoopUnit.getUnitType()
						listAPLButtons[iCount] = (iOwner, iID)
						x = 315 + nCol * 36
						y = iYOffset - nRow * 44

						# create the button name
						szString = "PlotListButton" + str(iCount)

						# set unit button image
						if (iLoopUnitType != listPrevAPLButtons.get(iCount)):
							screen.changeImageButton(szString, pLoopUnit.getButton())
							listPrevAPLButtons[iCount] = iLoopUnitType

						# check if it is an player unit or not
						screen.enable(szString, (iOwner == ActivePlayer))

						# check if the units is selected
						screen.setState(szString, pLoopUnit.IsSelected())

						screenShow(szString)

						# this if statement and everythign inside, handles the display of the colored buttons in the upper left corner of each unit icon. 
						# Wounded units will get a darker colored button.
						# wounded units -> darker button
						bUnitisWaiting = pLoopUnit.isWaiting()
						if (bUnitisWaiting or (pLoopUnit.getTeam() != ActiveTeam)):
							# fortified
							iState = 1
						elif (pLoopUnit.canMove()):
							iState = 3 - int(pLoopUnit.hasMoved())
						else:
							# unit has no movement points left
							iState = 4
						if (pLoopUnit.isHurt() and self.CFG_WOUNDED_INDICATOR_ENABLED):
							iState += 4

						if (UpgradePath.has_key(iLoopUnitType)):
							bUpgrade = UpgradePath[iLoopUnitType]
						else:
							bUpgrade = mt.checkAnyUpgrade(pLoopUnit)
							UpgradePath[iLoopUnitType] = bUpgrade
						iUpgradePromoState = (self.CFG_UPGRADE_INDICATOR_ENABLED and bUpgrade) + (bPromoEnabled * pLoopUnit.isPromotionReady())
						if (iUpgradePromoState > 0):
							szStringTemp = szString + "Upgrade"
							if (iUpgradePromoState != listPrevAPLUpgradeIndicator.get(iCount)):
								screen.changeDDSGFC(szStringTemp, self.UpgradePromoIconMap[iUpgradePromoState])
								listPrevAPLUpgradeIndicator[iCount] = iUpgradePromoState
							screenShow(szStringTemp)

						if (pLoopUnit.isHasPromotion(self.iPromoLeader) and self.CFG_WARLORD_INDICATOR_ENABLED):
							screen.addDDSGFC(szString + "Warlord", gc.getPromotionInfo(self.iPromoLeader).getButton(), x-4, y+8, 12, 12, WidgetTypes.WIDGET_GENERAL, iCount, -1)
							bShowWarlordIndicator = True

						if (not pLoopUnit.isFighting()):
							# place the health bar
							szStringTemp = szString + "Health"
							fPrevHealth = listPrevAPLHealthBar.get(iCount, -1.0)
							fHealth = float(pLoopUnit.currHitPoints())/pLoopUnit.maxHitPoints()
							if (not (-0.018 < fPrevHealth - fHealth < 0.018)): # (1/28)/2 = 0.018
								screen.setBarPercentage(szStringTemp, InfoBarTypes.INFOBAR_STORED, fHealth)
								listPrevAPLHealthBar[iCount] = fHealth
							screenShow(szStringTemp)

						# display the mission or activity info
						if (self.CFG_MISSION_INFO_ENABLED):
							#szActionIcon = None
							# place the activity info below the unit icon.
							pUnitGroup = pLoopUnit.getGroup()
							if (hasActivity(pUnitGroup.getActivityType())):
								if (pUnitGroup.getActivityType() == ActivityTypes.ACTIVITY_HOLD and pUnitGroup.getAutomateType() ==AutomateTypes.AUTOMATE_RELIGION):
									szActionIcon = self.AutomateIconMap[AutomateTypes.AUTOMATE_RELIGION]
								else:
									szActionIcon = self.ActivityIconMap[pUnitGroup.getActivityType()]
							elif (hasAutomate(pUnitGroup.getAutomateType())):
								szActionIcon = self.AutomateIconMap[pUnitGroup.getAutomateType()]
							elif (pUnitGroup.getLengthMissionQueue() > 0):
								if (hasMission(pUnitGroup.getMissionType(0))):
									# is the mission a "move to" mission
									szActionIcon = self.MissionIconMap[pUnitGroup.getMissionType(0)]
								else:
									szActionIcon = None
								# if nothing of above, but unit is waiting -> unit is fortified
							elif (bUnitisWaiting):
								if (pLoopUnit.isFortifyable()):
									# place "FORT" icon
									szActionIcon = self.OVERLAY_ACTION_FORTIFY
								else:
									szActionIcon = self.OVERLAY_ACTION_SLEEP
							else:
								szActionIcon = None

							if (szActionIcon == None):
								if (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
									if (CGEUtils.CGEUtils().isAutoReconUnit(iID)):
										szActionIcon = self.OVERLAY_ACTION_RECON

							# display the mission icon
							if (szActionIcon != None):
								screen.addDDSGFC(szString + "Action", szActionIcon, x + 4, y + 30, 27, 8, WidgetTypes.WIDGET_GENERAL, iCount, -1)
								bShowActionIcons = True

						# display the colored spot icon
						szStringTemp = szString + "Icon"
						if (listPrevAPLSpotIcons.get(iCount, 0) != iState):
							screen.addDDSGFC(szStringTemp, self.SpotIconState[iState], x-4, y-5, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, iCount, -1)
							#screen.changeDDSGFC(szStringTemp, self.SpotIconState[iState]) slower than addDDS!!
							listPrevAPLSpotIcons[iCount] = iState
						else:
							screenShow(szStringTemp)

				# left/right scroll buttons
				if (bVertMode and (nCol >= MaxCol or self.iColOffset > 0)):
					screen.enable(self.PLOT_LIST_MINUS_NAME, bLeftArrow)
					screen.show(self.PLOT_LIST_MINUS_NAME)
					screen.enable(self.PLOT_LIST_PLUS_NAME, bRightArrow)
					screen.show(self.PLOT_LIST_PLUS_NAME)

				# up/Down scroll buttons
				if ((bMultiMode and (nRow >= MaxRow or (self.iRowOffset > 0))) or \
					(bHorizMode and (nRow >= MaxRow or (self.iRowOffset > 0))) or \
					(bCompressMode and (nRow >= MaxRow or (self.iRowOffset > 0)))):
					screen.enable(self.PLOT_LIST_UP_NAME, bUpArrow)
					screen.show(self.PLOT_LIST_UP_NAME)
					screen.enable(self.PLOT_LIST_DOWN_NAME, bDownArrow)
					screen.show(self.PLOT_LIST_DOWN_NAME)

		else:

			screen.hide( "PlotListMinus" )
			screen.hide( "PlotListPlus" )

			for j in xrange(gc.getMAX_PLOT_LIST_ROWS()):
				#szStringPanel = "PlotListPanel" + str(j)
				#screen.hide(szStringPanel)

				for i in xrange(self.numPlotListButtons()):
					szString = "PlotListButton" + str(j*self.numPlotListButtons()+i)
					screen.hide( szString )

					szStringHealth = szString + "Health"
					screen.hide( szStringHealth )

					szStringIcon = szString + "Icon"
					screen.hide( szStringIcon )

			if ( pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):

				iVisibleUnits = CyInterface().getNumVisibleUnits()
				iCount = -(CyInterface().getPlotListColumn())


				bLeftArrow = False
				bRightArrow = False

				if (CyInterface().isCityScreenUp()):
					iMaxRows = 1
					iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
					iCount += iSkipped
				else:
					iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
					iCount += CyInterface().getPlotListOffset()
					iSkipped = 0

				CyInterface().cacheInterfacePlotUnits(pPlot)
				for i in xrange(CyInterface().getNumCachedInterfacePlotUnits()):
					pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
					if (pLoopUnit):

						if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
							bLeftArrow = True
						elif ((iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
							bRightArrow = True

						if ((iCount >= 0) and (iCount <  self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS())):
							if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()

							elif (pLoopUnit.canMove()):
								if (pLoopUnit.hasMoved()):
									szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
								else:
									szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
							else:
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

							szString = "PlotListButton" + str(iCount)
							screen.changeImageButton( szString, pLoopUnit.getButton() )
							if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
								bEnable = True
							else:
								bEnable = False
							screen.enable(szString, bEnable)

							if (pLoopUnit.IsSelected()):
								screen.setState(szString, True)
							else:
								screen.setState(szString, False)
							screen.show( szString )

							# place the health bar
							if (pLoopUnit.isFighting()):
								bShowHealth = False
							elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
								bShowHealth = pLoopUnit.canAirAttack()
							else:
								bShowHealth = pLoopUnit.canFight()

							if bShowHealth:
								szStringHealth = szString + "Health"
								screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
								if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
									screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
								elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
									screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
								else:
									screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
								screen.show( szStringHealth )

							# Adds the overlay first
							szStringIcon = szString + "Icon"
							screen.changeDDSGFC( szStringIcon, szFileName )
							screen.show( szStringIcon )

						iCount = iCount + 1

				if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
					screen.enable("PlotListMinus", bLeftArrow)
					screen.show( "PlotListMinus" )

					screen.enable("PlotListPlus", bRightArrow)
					screen.show( "PlotListPlus" )

		return 0

	# This will update the flag widget for SP hotseat and dbeugging
	def updateFlag( self ):

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()
			screen.addFlagWidgetGFC( "CivilizationFlag", xResolution - 288, yResolution - 138, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)

	# Will hide and show the selection buttons and their associated buttons
	def updateSelectionButtons( self ):

		global SELECTION_BUTTON_COLUMNS
		global MAX_SELECTION_BUTTONS
		global g_pSelectedUnit

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos
		global g_BottomContIconSize

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if (self.BottomContainerSize != (xResolution, yResolution, g_BottomContIconSize)):
			width = xResolution - (iMultiListXL+iMultiListXR)
			height = 100
			if (g_BottomContIconSize == 34):
				height = 110
			screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, width, height, 4, g_BottomContIconSize, g_BottomContIconSize, TableStyles.TABLE_STYLE_STANDARD )
			self.BottomContainerSize = (xResolution, yResolution, g_BottomContIconSize)
		screen.clearMultiList( "BottomButtonContainer" )
		screen.hide( "BottomButtonContainer" )
		screen.hide("SpyAlertButton1")
		screen.hide("LoadFullButton1")
		screen.hide("AutoReconButton1")
		screen.hide("CancelAutoReconButton1")
		screen.hide("AutoInsertQueueButton1")
		self.hideAutoInsertQueuePanel()

		# All of the hides...
		self.setMinimapButtonVisibility(False)

		screen.hideList( 0 )

		for i in xrange(g_NumEmphasizeInfos):
			screen.hide("Emphasize" + str(i))

		# Hurry button show...
		for i in xrange(g_NumHurryInfos):
			screen.hide("Hurry" + str(i))

		# Conscript Button Show
		screen.hide( "Conscript" )
		screen.hide( "AutomateProduction" )
		screen.hide( "AutomateCitizens" )

		if (not CyEngine().isGlobeviewUp() and pHeadSelectedCity):

			self.setMinimapButtonVisibility(True)

			if ((pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer()) or gc.getGame().isDebugMode()):

				if (self.CityButtonResolution != (xResolution, yResolution)):
					self.CityButtonResolution = (xResolution, yResolution)
					iBtnSX = xResolution - 284

					iBtnX = iBtnSX
					iBtnY = yResolution - 140
					iBtnW = 64
					iBtnH = 30

					# Conscript button
					szText = "<font=1>" + localText.getText("TXT_KEY_DRAFT", ()) + "</font>"
					screen.setButtonGFC( "Conscript", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_CONSCRIPT, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.setStyle( "Conscript", "Button_CityT1_Style" )
					screen.hide( "Conscript" )

					iBtnY += iBtnH
					iBtnW = 32
					iBtnH = 28

					# Hurry Buttons
					screen.setButtonGFC( "Hurry0", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.setStyle( "Hurry0", "Button_CityC1_Style" )
					screen.hide( "Hurry0" )

					iBtnX += iBtnW

					screen.setButtonGFC( "Hurry1", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.setStyle( "Hurry1", "Button_CityC2_Style" )
					screen.hide( "Hurry1" )

					iBtnX = iBtnSX
					iBtnY += iBtnH

					# Automate Production Button
					screen.addCheckBoxGFC( "AutomateProduction", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.setStyle( "AutomateProduction", "Button_CityC3_Style" )

					iBtnX += iBtnW

					# Automate Citizens Button
					screen.addCheckBoxGFC( "AutomateCitizens", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.setStyle( "AutomateCitizens", "Button_CityC4_Style" )

					iBtnY += iBtnH
					iBtnX = iBtnSX

					iBtnW	= 22
					iBtnWa	= 20
					iBtnH	= 24
					iBtnHa	= 27

					# Set Emphasize buttons
					i = 0
					szButtonID = "Emphasize" + str(i)
					screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					szStyle = "Button_CityB" + str(i+1) + "_Style"
					screen.setStyle( szButtonID, szStyle )
					screen.hide( szButtonID )

					i+=1
					szButtonID = "Emphasize" + str(i)
					screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					szStyle = "Button_CityB" + str(i+1) + "_Style"
					screen.setStyle( szButtonID, szStyle )
					screen.hide( szButtonID )

					i+=1
					szButtonID = "Emphasize" + str(i)
					screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					szStyle = "Button_CityB" + str(i+1) + "_Style"
					screen.setStyle( szButtonID, szStyle )
					screen.hide( szButtonID )

					iBtnY += iBtnH

					i+=1
					szButtonID = "Emphasize" + str(i)
					screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					szStyle = "Button_CityB" + str(i+1) + "_Style"
					screen.setStyle( szButtonID, szStyle )
					screen.hide( szButtonID )

					i+=1
					szButtonID = "Emphasize" + str(i)
					screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					szStyle = "Button_CityB" + str(i+1) + "_Style"
					screen.setStyle( szButtonID, szStyle )
					screen.hide( szButtonID )

					i+=1
					szButtonID = "Emphasize" + str(i)
					screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					szStyle = "Button_CityB" + str(i+1) + "_Style"
					screen.setStyle( szButtonID, szStyle )
					screen.hide( szButtonID )
				else:
					screen.show("AutomateProduction")
					screen.show("AutomateCitizens")

				g_pSelectedUnit = 0
				screen.setState( "AutomateCitizens", pHeadSelectedCity.isCitizensAutomated() )
				screen.setState( "AutomateProduction", pHeadSelectedCity.isProductionAutomated() )

				for i in xrange (g_NumEmphasizeInfos):
					szButtonID = "Emphasize" + str(i)
					screen.show( szButtonID )
					if ( pHeadSelectedCity.AI_isEmphasize(i) ):
						screen.setState( szButtonID, True )
					else:
						screen.setState( szButtonID, False )

				# City Tabs
				for i in xrange(g_NumCityTabTypes):
					screen.show("CityTab" + str(i))

				# Hurry button show...
				for i in xrange( g_NumHurryInfos ):
					szButtonID = "Hurry" + str(i)
					screen.show( szButtonID )
					screen.enable( szButtonID, pHeadSelectedCity.canHurry(i, False) )

				# Conscript Button Show
				screen.show( "Conscript" )
				if (pHeadSelectedCity.canConscript()):
					screen.enable( "Conscript", True )
				else:
					screen.enable( "Conscript", False )

				iCount = 0
				iRow = 0
				bFound = False

				CivInfo = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType())
				# Units to construct
				for i in xrange ( g_NumUnitClassInfos ):
					eLoopUnit = CivInfo.getCivilizationUnits(i)

					if (pHeadSelectedCity.canTrain(eLoopUnit, False, True)):
						szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
						screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
						if ( not pHeadSelectedCity.canTrain(eLoopUnit, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, szButton)
						screen.show( "BottomButtonContainer" )

						iCount = iCount + 1
						bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				lWonderClass = []
				# Buildings to construct
				for i in xrange ( g_NumBuildingClassInfos ):
					if (not isLimitedWonderClass(i)):
						eLoopBuilding = CivInfo.getCivilizationBuildings(i)

						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
							screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )
							screen.show( "BottomButtonContainer" )

							iCount = iCount + 1
							bFound = True
					else:
						lWonderClass.append(i)

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Wonders to construct
				for i in lWonderClass:
					eLoopBuilding = CivInfo.getCivilizationBuildings(i)

					if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
						if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )
						screen.show( "BottomButtonContainer" )

						iCount = iCount + 1
						bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Projects
				for i in xrange( g_NumProjectInfos ):
					if (pHeadSelectedCity.canCreate(i, False, True)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProjectInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CREATE, i, -1, False)
						if ( not pHeadSelectedCity.canCreate(i, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getProjectInfo(i).getButton() )
						screen.show( "BottomButtonContainer" )

						iCount = iCount + 1

				# Processes
				for i in xrange( g_NumProcessInfos ):
					if (pHeadSelectedCity.canMaintain(i, False)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProcessInfo(i).getButton(), iRow, WidgetTypes.WIDGET_MAINTAIN, i, -1, False )
						screen.show( "BottomButtonContainer" )

				screen.selectMultiList( "BottomButtonContainer", CyInterface().getCityTabSelectionRow() )

				if (UserPrefs.vistaCheck):
					iCityID = pHeadSelectedCity.getID()
					if (self.iAutoInsertQueueCityID != iCityID):
						self.iAutoInsertQueueCityID = pHeadSelectedCity.getID()
						screen.setState("AutoInsertQueueButton1", False)
						self.AutoInsertProductionQueuePosition = -1

					screen.moveItem("AutoInsertQueueButton1", iMultiListXR - 36, yResolution - 113, 0.0)
					screen.show("AutoInsertQueueButton1")

					if (screen.getCheckBoxState("AutoInsertQueueButton1")):
						self.AutoInsertQueuePanel()

		elif (not CyEngine().isGlobeviewUp() and pHeadSelectedUnit and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

			self.setMinimapButtonVisibility(True)
			self.iAutoInsertQueueCityID = -1

			if (CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION):

				if ( pHeadSelectedUnit.getOwner() == gc.getGame().getActivePlayer() and g_pSelectedUnit != pHeadSelectedUnit ):

					g_pSelectedUnit = pHeadSelectedUnit

					iCount = 0

					##### <written by F> #####
					#東方ユニットが段階すっ飛ばしのアップグレードが出来ないように調整(AIはすっ飛ばしが可能だったりする)
					
					iUnit = pHeadSelectedUnit.getUnitType()
					actions = CyInterface().getActionsToShow()
					#多分このTohoDeltaの値に入っているのはSANAE0
					TohoDelta = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
					SpellDelta = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()+gc.getNumUnitInfos()+gc.getNumReligionInfos()+gc.getNumSpecialistInfos()+gc.getNumBuildingInfos()+gc.getNumControlInfos()+7
					TohoUnitNum = gc.getInfoTypeForString('UNIT_SAGUME6') - gc.getInfoTypeForString('UNIT_SANAE0') + 1
					for i in actions:
						if TohoDelta <= i and i <= TohoDelta + TohoUnitNum - 1:
							continue
						elif  SpellDelta + gc.getInfoTypeForString('SPELLCARD_SANAE1_1') <= i and i <= SpellDelta + gc.getInfoTypeForString('SPELL_KISHINJOU1'):
							continue
						else:
							screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
							screen.show( "BottomButtonContainer" )
							
							if ( not CyInterface().canHandleAction(i, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )
					
							if ( pHeadSelectedUnit.isActionRecommended(i) ):#or gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_PROMOTION ):
								screen.enableMultiListPulse( "BottomButtonContainer", True, 0, iCount )
							else:
								screen.enableMultiListPulse( "BottomButtonContainer", False, 0, iCount )
	
							iCount = iCount + 1
					
					tohoFlag = False
					for k in range(len(TohoUnitList.UpgradeList)):
						sUnit,sTech,iNum = TohoUnitList.UpgradeList[k]
						if iUnit == gc.getInfoTypeForString(sUnit) and gc.getTeam(pHeadSelectedUnit.getTeam()).isHasTech(gc.getInfoTypeForString(sTech)):
							i = TohoDelta + iNum + k
							tohoFlag = True
					
					if tohoFlag == True and pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN'))==False:
						screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						if ( not CyInterface().canHandleAction(i, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )
						
						if ( pHeadSelectedUnit.isActionRecommended(i) ):#or gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_PROMOTION ):
							screen.enableMultiListPulse( "BottomButtonContainer", True, 0, iCount )
						else:
							screen.enableMultiListPulse( "BottomButtonContainer", False, 0, iCount )
	
						iCount = iCount + 1
						
					
					##### </written by F> #####
					
					##### <written by F> #####
					#ここからはスペルに関する記述
					#スペルが使えるようなら、スペルボタンを表示させる
					
					#CvGameUtils.doprint('spell')
					#CvGameUtils.doprint('Num of Action:%i' %(gc.getNumActionInfos()))
					for spell in SpellInfo.getSpells():
						
						i = spell.getActionNumber()
						if ( spell.isVisible(pHeadSelectedUnit) ):
							#CvGameUtils.doprint('Spell Visible, ActionNumber: %i ' %i)
							screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
							screen.show( "BottomButtonContainer" )
							
							#g_checkingActive=True
							#条件を満たしていなければ暗転表示
							if spell.isAbled(pHeadSelectedUnit) == False:
								screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )
							#g_checkingActive=False
							
							iCount = iCount + 1
					
					##### </written by F> #####

					if (CyInterface().canCreateGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), 0, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1, False )

					if (CyInterface().canDeleteGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), 0, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1, False )

					screen.show( "BottomButtonContainer" )

					if (gc.getUnitInfo(pHeadSelectedUnit.getUnitType()).isSpy()):
						screen.setImageButton("SpyAlertButton1", "Art/Interface/Buttons/SpyAlert.dds", xResolution - iMultiListXR, yResolution - 113, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show("SpyAlertButton1")

					#if (pHeadSelectedUnit.cargoSpace() > 0):
					#	screen.setImageButton("LoadFullButton1", "Art/Interface/Buttons/fullload.dds", xResolution - iMultiListXR, yResolution - 113, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					#	screen.show("LoadFullButton1")

					#if (pHeadSelectedUnit.canRecon(pHeadSelectedUnit.plot())): canRecon does not work! Well done, Firaxis!!!
					if (pHeadSelectedUnit.getDomainType() == DomainTypes.DOMAIN_AIR and pHeadSelectedUnit.airRange() != 0 and not gc.getUnitInfo(pHeadSelectedUnit.getUnitType()).isSuicide()):
						screen.addCheckBoxGFC("AutoReconButton1", "Art/Interface/Buttons/auto_recon.dds", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution - iMultiListXR, yResolution - 113, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
						screen.show("AutoReconButton1")
						screen.setImageButton("CancelAutoReconButton1", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), xResolution - iMultiListXR, yResolution - 75, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.enable("CancelAutoReconButton1", CGEUtils.CGEUtils().isAutoReconUnit(pHeadSelectedUnit.getID()))
						screen.show("CancelAutoReconButton1")

		elif (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

			self.setMinimapButtonVisibility(True)
			self.iAutoInsertQueueCityID = -1

		else:
			self.iAutoInsertQueueCityID = -1

		return 0

	# Will update the research buttons
	def updateResearchButtons(self):

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screen.hide("ResearchButtonBackgroundPanel")

		for i in xrange(gc.getNumTechInfos()):
			screen.hide("ResearchButton" + str(i))

		for i in xrange(gc.getNumReligionInfos()):
			screen.hide("ReligionButton" + str(i))

		if (CyInterface().shouldShowResearchButtons() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			iCount = 0
			screen.moveToFront("ResearchButtonBackgroundPanel")

			canResearch = gc.getActivePlayer().canResearch
			for i in xrange(gc.getNumTechInfos()):
				if (canResearch(i, False)):
					if (iCount < 20):
						szName = "ResearchButton" + str(i)

						for j in xrange(gc.getNumReligionInfos()):
							if (gc.getReligionInfo(j).getTechPrereq() == i):
								if not (gc.getGame().isReligionSlotTaken(j)):
									szName = "ReligionButton" + str(j)
									break

						screen.moveToFront(szName)
						screen.show(szName)
						self.setResearchButtonPosition(szName, iCount)

						iCount = iCount + 1

			if (iCount > 0):
				screen.setPanelSize("ResearchButtonBackgroundPanel", 278 + ((screen.getXResolution() - 1024) / 2), -6, 468, 40 + (32 * (iCount / 16)))
				screen.show("ResearchButtonBackgroundPanel")

		return 0

	# Will update the citizen buttons
	def updateCitizenButtons( self ):

		global MAX_CITIZEN_BUTTONS
		global MAX_SUPER_SPECIALIST_BUTTONS
		global MAX_ANGRY_CITIZEN_BUTTONS
		global g_iSuperSpecialistCount
		global g_iAngryCitizensCount
		global CFG_Specialist_Stacker

		if (CFG_Specialist_Stacker):
			bHandled = False

			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

			screen.hide( "SpecialistBackground" )
			screen.hide( "SpecialistLabel" )


			# Find out our resolution
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()

			for i in xrange(g_iSuperSpecialistCount):
				screen.hide("FreeSpecialist" + str(i))

			for i in xrange(g_iAngryCitizensCount):
				screen.hide("AngryCitizen" + str(i))

			for i in xrange(gc.getNumSpecialistInfos()):
				szI = str(i)
				screen.hide("IncreaseSpecialist" + szI)
				screen.hide("DecreaseSpecialist" + szI)
				screen.hide("CitizenDisabledButton" + szI)
				for j in xrange(MAX_CITIZEN_BUTTONS):
					screen.hide("CitizenButton" + str((i * 100) + j))
					screen.hide("CitizenButtonHighlight" + str((i * 100) + j))

			pHeadSelectedCity = CyInterface().getHeadSelectedCity()

			if ( CyInterface().isCityScreenUp() ):
				if (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
					pGetFreeSLCount = pHeadSelectedCity.getFreeSpecialistCount

					currentAngryCitizenCount = pHeadSelectedCity.angryPopulation(0)

					# Set the stackWidth to the original angry citizen spacing amount
					stackWidth = 34

					if (g_bStackAngryCitizens and ANGRY_CITIZEN_STACK_WIDTH > 10):
						stackWidth = SUPER_SPECIALIST_STACK_WIDTH

					if (g_bStackAngryCitizens and g_bDynamicAngryCitizensSpacing and currentAngryCitizenCount > 0):
						stackWidth = 184/currentAngryCitizenCount

					if (not g_bStackAngryCitizens):
						if (pHeadSelectedCity.angryPopulation(0) < MAX_ANGRY_CITIZEN_BUTTONS):
							currentAngryCitizenCount = pHeadSelectedCity.angryPopulation(0)
						else:
							currentAngryCitizenCount = MAX_ANGRY_CITIZEN_BUTTONS

					for i in xrange(currentAngryCitizenCount):
						szName = "AngryCitizen" + str(i)
						screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - 74 - (stackWidth * i), yResolution - 238, 24, 24, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
						screen.show( szName )

					g_iAngryCitizensCount = currentAngryCitizenCount

					currentSuperSpecialistCount = 0

					for i in xrange(gc.getNumSpecialistInfos()):
						if(pGetFreeSLCount(i) > 0):
							if(g_bDisplayUniqueSuperSpecialistsOnly):
								currentSuperSpecialistCount += 1
							else:
								currentSuperSpecialistCount += pGetFreeSLCount(i)

					# Set the stackWidth to the original super specialist spacing amount
					stackWidth = 34

					if(g_bStackSuperSpecialists and SUPER_SPECIALIST_STACK_WIDTH > 10):
						stackWidth = SUPER_SPECIALIST_STACK_WIDTH

					if(g_bStackSuperSpecialists and g_bDynamicSuperSpecialistsSpacing and currentSuperSpecialistCount > 0):
						stackWidth = 184/currentSuperSpecialistCount 

					iCount = 0
					for i in xrange(gc.getNumSpecialistInfos()):
						for j in xrange(pGetFreeSLCount(i)):
							if ((not g_bStackSuperSpecialists) and iCount > MAX_SUPER_SPECIALIST_BUTTONS-1):
								break

							szName = "FreeSpecialist" + str(iCount)
							screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (stackWidth * iCount)), yResolution - 206, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1)
							screen.show( szName )

							iCount += 1

							if(g_bDisplayUniqueSuperSpecialistsOnly):
								break

					g_iSuperSpecialistCount = iCount

					iXShiftVal = 0
					iYShiftVal = 0
					iSpecialistCount = 0

					iXOffset = xResolution - 74
					iYOffset = yResolution - 271

					bShow = (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode())
					bAutomated = pHeadSelectedCity.isCitizensAutomated()
					iTotalPop = pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()
					for i in xrange(gc.getNumSpecialistInfos()):

						if (iSpecialistCount > 6):
							iXShiftVal = 110
							iYShiftVal = (iSpecialistCount % 5) - 1
						else:
							iYShiftVal = iSpecialistCount

						bIsVisible = gc.getSpecialistInfo(i).isVisible()
						if (bIsVisible):
							iSpecialistCount += 1

						iForceSLCount = pHeadSelectedCity.getForceSpecialistCount(i)
						iSLCount = pHeadSelectedCity.getSpecialistCount(i)
						if (bShow):
							if (pHeadSelectedCity.isCitizensAutomated()):
								iNumSpecialist = max(iSLCount, iForceSLCount)
							else:
								iNumSpecialist = iSLCount
							if (pHeadSelectedCity.isSpecialistValid(i, 1) and (bAutomated or iNumSpecialist < iTotalPop)):
								screen.show("IncreaseSpecialist" + str(i))
								screen.show("CitizenDisabledButton" + str(i))

							if (iNumSpecialist > 0):
								screen.hide("CitizenDisabledButton" + str(i))
								screen.show("DecreaseSpecialist" + str(i))

						if (iSLCount < MAX_CITIZEN_BUTTONS):
							iCount = iSLCount
						else:
							iCount = MAX_CITIZEN_BUTTONS

						j = iCount-1

						while (j >= 0):
							szName = "CitizenButton" + str((i * 100) + j)
							if (bIsVisible):
								screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", iXOffset -iXShiftVal - (SPECIALIST_STACK_WIDTH * j), (iYOffset - (26 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
							else:
								screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", iXOffset - (SPECIALIST_STACK_WIDTH * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )

							screen.show( szName )
							szName = "CitizenButtonHighlight" + str((i * 100) + j)
							if (bIsVisible):
								screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), iXOffset - iXShiftVal - (SPECIALIST_STACK_WIDTH * j), (iYOffset - (26 * iYShiftVal)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j )
							else:
								screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), iXOffset - (SPECIALIST_STACK_WIDTH * j), (iYOffset - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j )

							if (iForceSLCount > j and g_bHighlightForcedSpecialists):
								screen.show( szName )
							else:
								screen.hide( szName )

							j -= 1

						if (iCount < 1):
							screen.show("CitizenDisabledButton" + str(i))

				screen.addPanel( "SpecialistBackground", u"", u"", True, False, xResolution - 243, yResolution-460, 230, 30, PanelStyles.PANEL_STYLE_STANDARD )
				screen.setStyle( "SpecialistBackground", "Panel_City_Header_Style" )
				screen.show( "SpecialistBackground" )
				screen.setLabel( "SpecialistLabel", "Background", localText.getText('TXT_SPECIALIST_STACKER_PANEL_LABEL', ()), CvUtil.FONT_CENTER_JUSTIFY, xResolution - 128, yResolution-452, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "SpecialistLabel" )
		else:
			bHandled = False

			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

			# Find out our resolution
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()

			for i in xrange( MAX_CITIZEN_BUTTONS ):
				szName = "FreeSpecialist" + str(i)
				screen.hide( szName )
				szName = "AngryCitizen" + str(i)
				screen.hide( szName )

			for i in xrange( gc.getNumSpecialistInfos() ):
				szName = "IncreaseSpecialist" + str(i)
				screen.hide( szName )
				szName = "DecreaseSpecialist" + str(i)
				screen.hide( szName )
				szName = "CitizenDisabledButton" + str(i)
				screen.hide( szName )
				for j in xrange(MAX_CITIZEN_BUTTONS):
					szName = "CitizenButton" + str((i * 100) + j)
					screen.hide( szName )
					szName = "CitizenButtonHighlight" + str((i * 100) + j)
					screen.hide( szName )

			pHeadSelectedCity = CyInterface().getHeadSelectedCity()

			if ( CyInterface().isCityScreenUp() ):
				if (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
					if ( pHeadSelectedCity.angryPopulation(0) < MAX_CITIZEN_BUTTONS ):
						iCount = pHeadSelectedCity.angryPopulation(0)
					else:
						iCount = MAX_CITIZEN_BUTTONS

					for i in xrange(iCount):
						bHandled = True
						szName = "AngryCitizen" + str(i)
						screen.show( szName )

					iFreeSpecialistCount = 0
					for i in xrange(gc.getNumSpecialistInfos()):
						iFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistCount(i)

					iCount = 0

					bHandled = False

					if (iFreeSpecialistCount > MAX_CITIZEN_BUTTONS):
						for i in xrange(gc.getNumSpecialistInfos()):
							if (pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
								if (iCount < MAX_CITIZEN_BUTTONS):
									szName = "FreeSpecialist" + str(iCount)
									screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 206, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
									screen.show( szName )
									bHandled = true
								iCount += 1

					else:
						for i in xrange(gc.getNumSpecialistInfos()):
							for j in xrange( pHeadSelectedCity.getFreeSpecialistCount(i) ):
								if (iCount < MAX_CITIZEN_BUTTONS):
									szName = "FreeSpecialist" + str(iCount)
									screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 206, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, -1 )
									screen.show( szName )
									bHandled = true

								iCount = iCount + 1

					for i in xrange( gc.getNumSpecialistInfos() ):

						bHandled = False

						if (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode()):

							if (pHeadSelectedCity.isCitizensAutomated()):
								iSpecialistCount = max(pHeadSelectedCity.getSpecialistCount(i), pHeadSelectedCity.getForceSpecialistCount(i))
							else:
								iSpecialistCount = pHeadSelectedCity.getSpecialistCount(i)

							if (pHeadSelectedCity.isSpecialistValid(i, 1) and (pHeadSelectedCity.isCitizensAutomated() or iSpecialistCount < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
								szName = "IncreaseSpecialist" + str(i)
								screen.show( szName )
								szName = "CitizenDisabledButton" + str(i)
								screen.show( szName )

							if iSpecialistCount > 0:
								szName = "CitizenDisabledButton" + str(i)
								screen.hide( szName )
								szName = "DecreaseSpecialist" + str(i)
								screen.show( szName )

						if (pHeadSelectedCity.getSpecialistCount(i) < MAX_CITIZEN_BUTTONS):
							iCount = pHeadSelectedCity.getSpecialistCount(i)
						else:
							iCount = MAX_CITIZEN_BUTTONS

						j = 0
						for j in xrange( iCount ):
							bHandled = True
							szName = "CitizenButton" + str((i * 100) + j)
							screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
							screen.show( szName )
							szName = "CitizenButtonHighlight" + str((i * 100) + j)
							screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j )
							if ( pHeadSelectedCity.getForceSpecialistCount(i) > j ):
								screen.show( szName )
							else:
								screen.hide( szName )

						if ( not bHandled ):
							szName = "CitizenDisabledButton" + str(i)
							screen.show( szName )

		return 0

	# Will update the game data strings
	def updateGameDataStrings( self ):
		global CFG_Combat_Experience_Counter
		global g_iGameTurn
		global g_ShowGameTurnBarColor
		global GPBarText
		global gCombatXPText
		global CFG_Show_TopCultureCities
		global gTopCivCultureText
		global gTopCivCulturePos
		global g_szOldTimeText
		global szGoldText

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "ResearchText" )
		screen.hide( "GoldText" )
		screen.hide( "TimeText" )
		screen.hide( "ResearchBar" )
		screen.hide("CombatXPButton")
		screen.hide("CombatXPText")
		screen.hide("CombatXPBar")
		screen.hide( "EraText" )

		bShift = CyInterface().shiftKey()

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (pHeadSelectedCity):
			ePlayer = pHeadSelectedCity.getOwner()
		else:
			ePlayer = gc.getGame().getActivePlayer()

		if ( ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS() ):
			return 0

		for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			screen.hide("PercentText" + str(iI))
			screen.hide("RateText" + str(iI))

		pPlayer = gc.getPlayer(ePlayer)

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):

			self.updateTimeText(True)
			if (g_szTimeText != g_szOldTimeText):
				screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 52, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				g_szOldTimeText = g_szTimeText
			screen.show( "TimeText" )

			# Percent of commerce
			if (pPlayer.isAlive()):
				iCount = 0
				bNotCityScrUp = not CyInterface().isCityScreenUp()

				if (CFG_Show_GreatPerson_Bar and bNotCityScrUp):
					iPercentY = iPercentWithGPBY
				else:
					iPercentY = 50
					screen.hide("GreatPersonBar")
					screen.hide("GreatPersonBarText")
					GPBarText = u""

				if (self.CommerceText[-1] != iPercentY):
					self.CommerceText[-1] = iPercentY
					for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
						self.CommerceText[iI] = [-1, -1, -1]
				for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
					if (gc.getPlayer(ePlayer).isCommerceFlexible(eCommerce) or (not bNotCityScrUp and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						iValue = pPlayer.getCommercePercent(eCommerce)
						szString = "PercentText" + str(iI)
						bChanged = (self.CommerceText[iI][2] != iCount)
						self.CommerceText[iI][2] = iCount
						if (self.CommerceText[iI][0] != iValue or bChanged):
							szOutText = u"<font=2>%c:%d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), iValue)
							screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 14, iPercentY + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							self.CommerceText[iI][0] = iValue
						screen.show( szString )

						if (bNotCityScrUp):
							iValue = pPlayer.getCommerceRate(CommerceTypes(eCommerce))
							szString = "RateText" + str(iI)
							if (self.CommerceText[iI][1] != iValue or bChanged):
								szOutText = u"<font=2>" + localText.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (iValue, )) + u"</font>"
# CGE-LE - begin
								screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 112, iPercentY + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
# CGE-LE - end
								self.CommerceText[iI][1] = iValue
							screen.show( szString )

						iCount = iCount + 1;

				szText = CyGameTextMgr().getGoldStr(ePlayer)
				if (szGoldText != szText):
					screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 3, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					szGoldText = szText
				screen.show( "GoldText" )

				if (g_bShowEra):
					global g_eraColor
					global g_eraText

					szText = gc.getEraInfo(pPlayer.getCurrentEra()).getDescription() #+ " Era"
					if (g_bShowReflectEraInTurnColor):
						szText = localText.changeTextColor(szText, g_eraColor)
					if (szText != g_eraText):
						screen.setLabel("EraText", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, 266, 4, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						g_eraText = szText
					screen.show("EraText")

				iGameTurn = gc.getGame().getGameTurn()
				iMaxTurn = gc.getGame().getEstimateEndTurn()#gc.getGame().getMaxTurns()
				if (CFG_Show_GameTurn_Bar):
					if (g_iGameTurn != iGameTurn):
						screen.setBarPercentage("GameTurnBar", InfoBarTypes.INFOBAR_STORED, float(iGameTurn)/iMaxTurn)
						if (iGameTurn >= iMaxTurn - 10):
							if (g_ShowGameTurnBarColor != 3):
								screen.setStackedBarColors("GameTurnBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
								g_ShowGameTurnBarColor = 3
						elif (iGameTurn >= iMaxTurn - 100):
							if (g_ShowGameTurnBarColor != 2):
								screen.setStackedBarColors("GameTurnBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
								g_ShowGameTurnBarColor = 2
						else:
							if (g_ShowGameTurnBarColor != 1):
								screen.setStackedBarColors("GameTurnBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
								g_ShowGameTurnBarColor = 1
						g_iGameTurn = iGameTurn
						screen.show("GameTurnBar")

				if (CFG_Combat_Experience_Counter):
					iCombatExp = pPlayer.getCombatExperience()
					iCombarThreshold = pPlayer.greatPeopleThreshold(True)
					szCombatXPText = "%3d/%3d"%(iCombatExp, iCombarThreshold)

					if (gCombatXPText != szCombatXPText):
						screen.setLabel("CombatXPText", "Background", szCombatXPText, CvUtil.FONT_CENTER_JUSTIFY, 221, 20, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
						screen.setBarPercentage("CombatXPBar", InfoBarTypes.INFOBAR_RATE, (float(iCombatExp)/iCombarThreshold))
						gCombatXPText = szCombatXPText

					if (bNotCityScrUp):
						screen.show("CombatXPButton")
						screen.show("CombatXPText")
						screen.show("CombatXPBar")
					else:
						screen.hide("CombatXPButton")
						screen.hide("CombatXPText")
						screen.hide("CombatXPBar")

				if (((pPlayer.calculateGoldRate() != 0) and not (pPlayer.isAnarchy())) or (pPlayer.getGold() != 0)):
					screen.show( "GoldText" )

				if (pPlayer.isAnarchy()):

					szText = localText.getText("INTERFACE_ANARCHY", (pPlayer.getAnarchyTurns(), ))
# >>> CYBERFRONT // text: adjust
#					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 3, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 6, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
# <<< CYBERFRONT
					if (pPlayer.getCurrentResearch() != -1):
						screen.show( "ResearchText" )
					else:
						screen.hide( "ResearchText" )

				elif (pPlayer.getCurrentResearch() != -1):

					szText = CyGameTextMgr().getResearchStr(ePlayer)
# >>> CYBERFRONT // text: adjust
#					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 3, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 6, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
# <<< CYBERFRONT
					screen.show( "ResearchText" )

					researchProgress = gc.getTeam(pPlayer.getTeam()).getResearchProgress(pPlayer.getCurrentResearch())
					overflowResearch = (pPlayer.getOverflowResearch() * pPlayer.calculateResearchModifier(pPlayer.getCurrentResearch()))/100
					researchCost = float(gc.getTeam(pPlayer.getTeam()).getResearchCost(pPlayer.getCurrentResearch()))
					researchRate = pPlayer.calculateResearchRate(-1)

					screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_STORED, float(researchProgress + overflowResearch) / researchCost )
					if ( researchCost >  researchProgress + overflowResearch):
						screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_RATE, float(researchRate) / (researchCost - researchProgress - overflowResearch))
					else:
						screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_RATE, 0.0 )

					screen.show( "ResearchBar" )

				iActPlayer = gc.getGame().getActivePlayer()
				pActPlayer = gc.getPlayer(iActPlayer)

				if (CFG_Show_GreatPerson_Bar and bNotCityScrUp):
					iFastestPerson = 10000000
					iGPNext = pActPlayer.greatPeopleThreshold(False) -1
					pFastestCity = pHeadSelectedCity
					pGetActCity = pActPlayer.getCity

					for iLoopCity in xrange(pActPlayer.getNumCities()):
						pCity = pGetActCity(iLoopCity)
						if (pCity):
							iGPRate = pCity.getGreatPeopleRate()
							if (iGPRate > 0):
								iGPTurns = (iGPNext - pCity.getGreatPeopleProgress() + iGPRate) / iGPRate
								if (iGPTurns < iFastestPerson):
									iFastestPerson = iGPTurns
									pFastestCity = pCity

					if (iFastestPerson < 10000000 and pFastestCity):
						iTotalGPProgress = 0
						lGPList = []
						for iUnit in self.GPUnitList:
							iGPProgress = pFastestCity.getGreatPeopleUnitProgress(iUnit)
							if (iGPProgress > 0):
								lGPList.append((-iGPProgress, iUnit))
							iTotalGPProgress += iGPProgress
						if (iTotalGPProgress == 0):
							szText = u"<font=1>%c: %s(%d)</font>"%(CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pFastestCity.getName(), iFastestPerson)
						else:
							lGPList.sort()
							szText = u"<font=1>%s(%.1f%%): %s(%d)</font>"%(gc.getUnitInfo(lGPList[0][1]).getDescription(), -lGPList[0][0] * 100.0 / iTotalGPProgress, pFastestCity.getName(), iFastestPerson)
						if (GPBarText != szText):
							GPBarText = szText
							screen.setText("GreatPersonBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, 138, 54, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1)
							fGPThreshold = float(gc.getPlayer(pFastestCity.getOwner()).greatPeopleThreshold(False))
							iFirst = float(pFastestCity.getGreatPeopleProgress()) / fGPThreshold
							screen.setBarPercentage("GreatPersonBar", InfoBarTypes.INFOBAR_STORED, iFirst)
							if (iFirst == 1):
								screen.setBarPercentage("GreatPersonBar", InfoBarTypes.INFOBAR_RATE, (float(pFastestCity.getGreatPeopleRate()) / fGPThreshold))
							else:
								screen.setBarPercentage("GreatPersonBar", InfoBarTypes.INFOBAR_RATE, ((float(pFastestCity.getGreatPeopleRate()) / fGPThreshold)) / (1 - iFirst))
							screen.show("GreatPersonBar")

				if (CFG_Show_TopCultureCities):
					if (bNotCityScrUp):
						szText = u""
						CivList = []
						CivListappend = CivList.append
						pActTeam = gc.getTeam(iActPlayer)
						VictoryInfo = gc.getVictoryInfo(gc.getInfoTypeForString("VICTORY_CULTURAL"))
						iNumCulCities = VictoryInfo.getNumCultureCities()
						iLegendary = gc.getCultureLevelInfo(VictoryInfo.getCityCulture()).getSpeedThreshold(gc.getGame().getGameSpeedType())
						for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
							pLoopPlayer = gc.getPlayer(iLoopPlayer)
							if (iLoopPlayer != iActPlayer and pLoopPlayer.isAlive() and not pLoopPlayer.isMinorCiv() and not pLoopPlayer.isBarbarian()):
								if (pActTeam.isHasMet(pLoopPlayer.getTeam())):
									tempCityList = []
									(pLoopCity, iter) = pLoopPlayer.firstCity(False)
									while (pLoopCity):
										tempCityList.append(pLoopCity.getCulture(iLoopPlayer))
										(pLoopCity, iter) = pLoopPlayer.nextCity(iter, False)
									tempCityList.sort()
									tempCityList.reverse()
									iCultureCount = 0
									if (len(tempCityList) > iNumCulCities):
										iNumCity = iNumCulCities
									else:
										iNumCity = len(tempCityList)
									for iCulture in tempCityList[:iNumCity]:
										if (iCulture > iLegendary):
											iCultureCount += iLegendary
										else:
											iCultureCount += iCulture
									CivListappend((iCultureCount, iLoopPlayer))
						CivList.sort()

						if (len(CivList) > 0):
							iTopPlayer = CivList[-1][1]
							pTopPlayer = gc.getPlayer(iTopPlayer)
							CityList = []
							(pLoopCity, iter) = pTopPlayer.firstCity(False)
							while (pLoopCity):
								CityList.append((pLoopCity.getCulture(iTopPlayer), pLoopCity))
								(pLoopCity, iter) = pTopPlayer.nextCity(iter, False)
							CityList.sort()
							CityList.reverse()

							if (len(CityList) > iNumCulCities):
								iNumCity = iNumCulCities
							else:
								iNumCity = len(CityList)
							iRemainTurn = gc.getGame().getEstimateEndTurn() - iGameTurn
							for (iCulture, pLoopCity) in CityList[:iNumCity]:
								iRate = pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)
								iCulPercent = (iCulture*100)/iLegendary
								if (iCulPercent >= 80):
									szCulPercent = u"<color=255,255,0>%d%%</color>"%(iCulPercent)
								else:
									szCulPercent = u"%d%%"%(iCulPercent)
								if (iCulture > iLegendary):
									szText += u", %s: <color=255,0,0>%s</color>"%(pLoopCity.getName(), gc.getCultureLevelInfo(VictoryInfo.getCityCulture()).getText())
								elif (iRate > 0):
									iTurn = ((iLegendary - iCulture) + iRate -1)/iRate
									if (iTurn > iRemainTurn):
										szText += u", %s: %s"%(pLoopCity.getName(), szCulPercent)
									else:
										szText += u", %s: %s(%d)"%(pLoopCity.getName(), szCulPercent, iTurn)
								else:
									szText += u", %s: %s"%(pLoopCity.getName(), szCulPercent)

							szText = u"<font=1>Top %c:"%(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + szText[1:] + "</font>"

						if (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
							yCoord = yResolution - 187
						else:
							yCoord = yResolution - 68
						if (gTopCivCultureText != szText or gTopCivCulturePos != yCoord):
							gTopCivCulturePos = yCoord
							screen.setText("TopCultureCitiesText", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 4, yCoord, -0.4, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
							gTopCivCultureText = szText
					else:
						gTopCivCultureText = u""
						screen.hide("TopCultureCitiesText")
				else:
					gTopCivCultureText = u""
					screen.hide("TopCultureCitiesText")

				if (self.Era != pActPlayer.getCurrentEra()):
					self.Era = pActPlayer.getCurrentEra()
					global listPrevAPLButtons
					listPrevAPLButtons = dict()
		else:
			screen.hide("GameTurnBar")
			screen.hide("GreatPersonBar")
			screen.hide("GreatPersonBarText")
			GPBarText = u""
			screen.hide("TopCultureCitiesText")
			gTopCivCultureText = u""

		return 0

	# < NJAGCM Start >
	def updateTimeText(self, bPrimaryTimeText):

		global g_szTimeText
		global g_eraColor

		ePlayer = gc.getGame().getActivePlayer()
		iGameTurn = gc.getGame().getGameTurn()
		if (gc.getGame().getMaxTurns() == 0):
			iMaxTurn = 0
		else:
			iMaxTurn = gc.getGame().getEstimateEndTurn()
		szIntTime = CyGameTextMgr().getInterfaceTimeStr(ePlayer)
		CurrentEra = gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getType()

		szTimeText = u""

		if(not g_bAlternateTimeText):
			bPrimaryTimeText = True

		if(bPrimaryTimeText):
			if(g_bShowGameCompletedTurns and iMaxTurn > 0):
				szTimeText += u"  " + str(iGameTurn) + u"/" + str(iMaxTurn)
			elif(g_bShowGameCompletedTurns):
				szTimeText += u"  Turn " + str(iGameTurn)

			if(g_bShowGameCompletedPercent and iMaxTurn > 0):
				szTimeText += u"   %2.2f%%" % (100 *(iGameTurn / float(iMaxTurn)))

			if(g_bShowGameClock):
				szTimeText += u" " + getClockText()

			if(g_bShowTurns):
				if(g_bShowReflectEraInTurnColor and g_eraTurnColorDictionary.has_key(CurrentEra)):
					g_eraColor = g_eraTurnColorDictionary[CurrentEra]
					szTimeText += u" " + localText.changeTextColor(szIntTime, g_eraColor)

				else:
					szTimeText += u" " + szIntTime

		else:
			if(g_bAlternateShowGameCompletedTurns and iMaxTurn > 0):
				szTimeText += u"  " + str(iGameTurn) + u"/" + str(iMaxTurn)
			elif(g_bAlternateShowGameCompletedTurns):
				szTimeText += u" Turn " + str(iGameTurn)

			if(g_bAlternateShowGameCompletedPercent and iMaxTurn > 0):
				szTimeText += u"   %2.2f%%" % (100 *(iGameTurn / float(iMaxTurn)))

			if(g_bAlternateShowGameClock):
				szTimeText += u" " + getClockText()

			if(g_bAlternateShowTurns):
				if(g_bShowReflectEraInTurnColor and g_eraTurnColorDictionary.has_key(CurrentEra)):
					g_eraColor = g_eraTurnColorDictionary[CurrentEra]
 					szTimeText += u" " + localText.changeTextColor(szIntTime, g_eraColor)

				else:
					szTimeText += u" " + szIntTime
		g_szTimeText = szTimeText
	# < NJAGCM End  >

	# Will update the selection Data Strings
	def updateCityScreen( self ):

		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS

		global g_iNumTradeRoutes
		global g_iNumBuildings
		global g_iNumLeftBonus
		global g_iNumCenterBonus
		global g_iNumRightBonus

		global CFG_RAWCOMMERCEDISPLAY

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.hide( "PopulationBar" )
		screen.hide( "ProductionBar" )
		screen.hide( "GreatPeopleBar" )
		screen.hide( "CultureBar" )
		screen.hide( "MaintenanceText" )
		screen.hide( "MaintenanceAmountText" )
		screen.hide( "NationalityText" )
		screen.hide( "NationalityBar" )
		screen.hide( "DefenseText" )
		screen.hide( "CityScrollMinus" )
		screen.hide( "CityScrollPlus" )
		screen.hide( "CityNameText" )
		screen.hide( "PopulationText" )
		screen.hide( "PopulationInputText" )
		screen.hide( "HealthText" )
		screen.hide( "ProductionText" )
		screen.hide( "ProductionInputText" )
		screen.hide( "HappinessText" )
		screen.hide( "CultureText" )
		screen.hide( "GreatPeopleText" )
		#screen.hide("NationalWonderText")

## Sevo - Raw Commerce Display - begin
		if (CFG_RAWCOMMERCEDISPLAY):
			screen.hide("MaintenanceTextb")
			screen.hide("MaintenanceTextc")
			screen.hide("MaintenanceTextd")
			screen.hide("MaintenanceTexte")
			screen.hide("MaintenanceTextf")
			screen.hide("MaintenanceTextg")
			screen.hide("MaintenanceTexth")
			screen.hide("MaintenanceTexti")
## Sevo - Raw Commerce Display - end

		for i in xrange(gc.getNumReligionInfos()):
			screen.hide("ReligionHolyCityDDS" + str(i))
			screen.hide("ReligionDDS" + str(i))

		for i in xrange(gc.getNumCorporationInfos()):
			screen.hide("CorporationHeadquarterDDS" + str(i))
			screen.hide("CorporationDDS" + str(i))

		for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			screen.hide("CityPercentText" + str(i))

		screen.addPanel( "BonusPane0", u"", u"", True, False, xResolution - 244, 94, 57, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNL )
		screen.hide( "BonusPane0" )
		screen.addScrollPanel( "BonusBack0", u"", xResolution - 242, 94, 157, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack0" )

		screen.addPanel( "BonusPane1", u"", u"", True, False, xResolution - 187, 94, 68, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNC )
		screen.hide( "BonusPane1" )
		screen.addScrollPanel( "BonusBack1", u"", xResolution - 191, 94, 184, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack1" )

		screen.addPanel( "BonusPane2", u"", u"", True, False, xResolution - 119, 94, 107, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNR )
		screen.hide( "BonusPane2" )
		screen.addScrollPanel( "BonusBack2", u"", xResolution - 125, 94, 205, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack2" )

		screen.hide( "TradeRouteTable" )
		screen.hide( "BuildingListTable" )

		screen.hide( "BuildingListBackground" )
		screen.hide( "TradeRouteListBackground" )
		screen.hide( "BuildingListLabel" )
		screen.hide( "TradeRouteListLabel" )

		for i in xrange(g_iNumLeftBonus):
			screen.hide("LeftBonusItem" + str(i))

		for i in xrange(g_iNumCenterBonus):
			screen.hide("CenterBonusItemLeft" + str(i))
			screen.hide("CenterBonusItemRight" + str(i))

		for i in xrange(g_iNumRightBonus):
			screen.hide("RightBonusItemLeft" + str(i))
			screen.hide("RightBonusItemRight" + str(i))

		if ( CyInterface().isCityScreenUp() ):
			if ( pHeadSelectedCity ):

				screen.show( "InterfaceTopLeftBackgroundWidget" )
				screen.show( "InterfaceTopRightBackgroundWidget" )
				screen.show( "InterfaceCenterLeftBackgroundWidget" )
				screen.show( "CityScreenTopWidget" )
				screen.show( "CityNameBackground" )
				screen.show( "TopCityPanelLeft" )
				screen.show( "TopCityPanelRight" )
				screen.show( "CityScreenAdjustPanel" )
				screen.show( "InterfaceCenterRightBackgroundWidget" )

## Sevo - Raw Commerce Display - begin
				if (CFG_RAWCOMMERCEDISPLAY):
					screen.show("CityScreenAdjustPanelb")
## Sevo - Raw Commerce Display - end

				if ( pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam() ):
					if ( gc.getActivePlayer().getNumCities() > 1 ):
						screen.show( "CityScrollMinus" )
						screen.show( "CityScrollPlus" )

				# Help Text Area
				screen.setHelpTextArea( 390, FontTypes.SMALL_FONT, 0, 0, -2.2, True, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )

				iFoodDifference = pHeadSelectedCity.foodDifference(True)
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True, True)
				iProductionDiffJustFood = (pHeadSelectedCity.getCurrentProductionDifference(False, True) - iProductionDiffNoFood)

				szBuffer = u"<font=4>"

				if (pHeadSelectedCity.isCapital()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
				elif (pHeadSelectedCity.isGovernmentCenter()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))

				if (pHeadSelectedCity.isPower()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))

				szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())

				if (pHeadSelectedCity.isOccupation()):
					szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())

				szBuffer += u"</font>"

				screen.setText( "CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
				screen.setStyle( "CityNameText", "Button_Stone_Style" )
				screen.show( "CityNameText" )

				if ( (iFoodDifference != 0) or not (pHeadSelectedCity.isFoodProduction() ) ):
					if (iFoodDifference > 0):
						szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))
					elif (iFoodDifference < 0):
						szBuffer = localText.getText("INTERFACE_CITY_STARVING", ())
					else:
						szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())

					screen.setLabel( "PopulationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow1Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "PopulationText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "PopulationText" )

				if (not pHeadSelectedCity.isDisorder() and not pHeadSelectedCity.isFoodProduction()):

					szBuffer = u"%d%c - %d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD), gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), pHeadSelectedCity.foodConsumption(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
					screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "PopulationInputText" )

				else:

					szBuffer = u"%d%c" %(iFoodDifference, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
					screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "PopulationInputText" )

				if ((pHeadSelectedCity.badHealth(False) > 0) or (pHeadSelectedCity.goodHealth() >= 0)):
					if (pHeadSelectedCity.healthRate(False, 0) < 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_BAD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False), pHeadSelectedCity.healthRate(False, 0)))
					elif (pHeadSelectedCity.badHealth(False) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD_NO_BAD", (pHeadSelectedCity.goodHealth(), ))

					screen.setLabel( "HealthText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HEALTH, -1, -1 )
					screen.show( "HealthText" )

				if (iFoodDifference < 0):

					if ( pHeadSelectedCity.getFood() + iFoodDifference > 0 ):
						iDeltaFood = pHeadSelectedCity.getFood() + iFoodDifference
					else:
						iDeltaFood = 0
					if ( -iFoodDifference < pHeadSelectedCity.getFood() ):
						iExtraFood = -iFoodDifference
					else:
						iExtraFood = pHeadSelectedCity.getFood()
					iFirst = float(iDeltaFood) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(iDeltaFood) / pHeadSelectedCity.growthThreshold() )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if ( pHeadSelectedCity.growthThreshold() > iDeltaFood):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iExtraFood) / (pHeadSelectedCity.growthThreshold() - iDeltaFood) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)
					
				else:

					iFirst = float(pHeadSelectedCity.getFood()) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(pHeadSelectedCity.getFood()) / pHeadSelectedCity.growthThreshold() )
					if ( pHeadSelectedCity.growthThreshold() >  pHeadSelectedCity.getFood()):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, float(iFoodDifference) / (pHeadSelectedCity.growthThreshold() - pHeadSelectedCity.getFood()) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0 )

				screen.show( "PopulationBar" )

				if (pHeadSelectedCity.getOrderQueueLength() > 0):
					if (pHeadSelectedCity.isProductionProcess()):
						szBuffer = pHeadSelectedCity.getProductionName()
					else:
						szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))

					screen.setLabel( "ProductionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow2Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "ProductionText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "ProductionText" )

				if (pHeadSelectedCity.isProductionProcess()):
					szBuffer = u"%d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				elif (pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0)):
					szBuffer = u"%d%c + %d%c" %(iProductionDiffJustFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				else:
					szBuffer = u"%d%c" %(iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())

				screen.setLabel( "ProductionInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1 )
				screen.show( "ProductionInputText" )

				if ((pHeadSelectedCity.happyLevel() >= 0) or (pHeadSelectedCity.unhappyLevel(0) > 0)):
					if (pHeadSelectedCity.isDisorder()):
						szBuffer = u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
					elif (pHeadSelectedCity.angryPopulation(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_UNHAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0), pHeadSelectedCity.angryPopulation(0)))
					elif (pHeadSelectedCity.unhappyLevel(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY_NO_UNHAPPY", (pHeadSelectedCity.happyLevel(), ))

					screen.setLabel( "HappinessText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HAPPINESS, -1, -1 )
					screen.show( "HappinessText" )

				if (not(pHeadSelectedCity.isProductionProcess())):

					iNeeded = pHeadSelectedCity.getProductionNeeded()
					iStored = pHeadSelectedCity.getProduction()
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_STORED, float(iStored) / iNeeded )
					if iNeeded > iStored:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, float(iProductionDiffNoFood) / (iNeeded - iStored) )
					else:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if iNeeded > iStored + iProductionDiffNoFood:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iProductionDiffJustFood) / (iNeeded - iStored - iProductionDiffNoFood) )
					else:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)

					screen.show( "ProductionBar" )

				iCount = 0

				for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
					eCommerce = (i + 1) % CommerceTypes.NUM_COMMERCE_TYPES

					if ((gc.getPlayer(pHeadSelectedCity.getOwner()).isCommerceFlexible(eCommerce)) or (eCommerce == CommerceTypes.COMMERCE_GOLD)):
						szBuffer = u"%d.%02d %c" %(pHeadSelectedCity.getCommerceRate(eCommerce), pHeadSelectedCity.getCommerceRateTimes100(eCommerce)%100, gc.getCommerceInfo(eCommerce).getChar())

						iHappiness = pHeadSelectedCity.getCommerceHappinessByType(eCommerce)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u", %d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
							else:
								szTempBuffer = u", %d%c" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
							szBuffer = szBuffer + szTempBuffer

						szName = "CityPercentText" + str(iCount)
						screen.setLabel( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 45 + (19 * iCount) + 4, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_COMMERCE_MOD_HELP, eCommerce, -1 )
						screen.show( szName )
						iCount = iCount + 1

				iCount = 0

## Sevo - Raw Commerce Display - begin
				if (CFG_RAWCOMMERCEDISPLAY):
					screen.addTableControlGFC("TradeRouteTable", 3, 10, 277, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
					screen.setStyle("TradeRouteTable", "Table_City_Style" )
					screen.addTableControlGFC("BuildingListTable", 3, 10, 407, 238, yResolution - 631, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
					screen.setStyle("BuildingListTable", "Table_City_Style")
## Sevo - Raw Commerce Display - end
				else:
					screen.addTableControlGFC("TradeRouteTable", 3, 10, 187, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
					screen.setStyle("TradeRouteTable", "Table_City_Style")
					screen.addTableControlGFC("BuildingListTable", 3, 10, 317, 238, yResolution - 541, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
					screen.setStyle("BuildingListTable", "Table_City_Style")
## Sevo - Raw Commerce Display - end (else)

				screen.setTableColumnHeader( "TradeRouteTable", 0, u"", 108 )
				screen.setTableColumnHeader( "TradeRouteTable", 1, u"", 118 )
				screen.setTableColumnHeader( "TradeRouteTable", 2, u"", 10 )
				screen.setTableColumnRightJustify( "TradeRouteTable", 1 )

				screen.setTableColumnHeader("BuildingListTable", 0, u"", 113)#108
				screen.setTableColumnHeader("BuildingListTable", 1, u"", 118)#118
				screen.setTableColumnHeader("BuildingListTable", 2, u"", 5)#10
				screen.setTableColumnRightJustify( "BuildingListTable", 1 )

				screen.show( "BuildingListBackground" )
				screen.show( "TradeRouteListBackground" )
				screen.show( "BuildingListLabel" )
				screen.show( "TradeRouteListLabel" )

				for i in xrange( 3 ):
					screen.show("BonusPane" + str(i))
					screen.show("BonusBack" + str(i))

				iNumBuildings = 0
				for i in xrange(gc.getNumBuildingInfos()):
					iNumHeadCityBuilding = pHeadSelectedCity.getNumBuilding(i)
					if (iNumHeadCityBuilding > 0):

						for k in xrange(iNumHeadCityBuilding):

							szLeftBuffer = gc.getBuildingInfo(i).getDescription()
							szRightBuffer = u""
							bFirst = True

							if (pHeadSelectedCity.getNumActiveBuilding(i) > 0):
								iHealth = pHeadSelectedCity.getBuildingHealth(i)

								if (iHealth != 0):
									if (not  bFirst):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False

									if (iHealth > 0):
										szRightBuffer += u"+%d%c"%(iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
									else:
										szRightBuffer += u"+%d%c"%(-(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

								iHappiness = pHeadSelectedCity.getBuildingHappiness(i)

								if (iHappiness != 0):
									if (not bFirst):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False

									if ( iHappiness > 0 ):
										szRightBuffer += u"+%d%c"%(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
									else:
										szRightBuffer += u"+%d%c"%(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

								for j in xrange( YieldTypes.NUM_YIELD_TYPES):
									iYield = gc.getBuildingInfo(i).getYieldChange(j) + iNumHeadCityBuilding * pHeadSelectedCity.getBuildingYieldChange(gc.getBuildingInfo(i).getBuildingClassType(), j)

									if (iYield != 0):
										if (not  bFirst):
											szRightBuffer = szRightBuffer + ", "
										else:
											bFirst = False

										if ( iYield > 0 ):
											szRightBuffer += u"+%d%c"%(iYield, gc.getYieldInfo(j).getChar())
										else:
											szRightBuffer += u"%d%c"%(iYield, gc.getYieldInfo(j).getChar())

							for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
								iCommerce = pHeadSelectedCity.getBuildingCommerceByBuilding(j, i) / iNumHeadCityBuilding

								if (iCommerce != 0):
									if (not bFirst):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False

									if ( iCommerce > 0 ):
										szRightBuffer += u"+%d%c"%(iCommerce, gc.getCommerceInfo(j).getChar())
									else:
										szRightBuffer += u"%d%c"%(iCommerce, gc.getCommerceInfo(j).getChar())

							screen.appendTableRow( "BuildingListTable" )
							screen.setTableText( "BuildingListTable", 0, iNumBuildings, "<font=1>" + szLeftBuffer + "</font>", gc.getBuildingInfo(i).getButton(), WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
							screen.setTableText( "BuildingListTable", 1, iNumBuildings, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )

							iNumBuildings = iNumBuildings + 1

				if ( iNumBuildings > g_iNumBuildings ):
					g_iNumBuildings = iNumBuildings

				iNumTradeRoutes = 0
## Sevo - Raw Commerce Display - begin
				iNetTradeAmount = 0
## Sevo - Raw Commerce Display - end

				for i in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
					pLoopCity = pHeadSelectedCity.getTradeCity(i)

					if (pLoopCity and pLoopCity.getOwner() >= 0):
						player = gc.getPlayer(pLoopCity.getOwner())
						szLeftBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), pLoopCity.getName() )
						szRightBuffer = u""

						for j in xrange(YieldTypes.NUM_YIELD_TYPES):
							iTradeProfit = pHeadSelectedCity.calculateTradeYield(j, pHeadSelectedCity.calculateTradeProfit(pLoopCity))

							if (iTradeProfit != 0):
								if ( iTradeProfit > 0 ):
									szRightBuffer += u"+%d%c"%(iTradeProfit, gc.getYieldInfo(j).getChar())
								else:
									szRightBuffer += u"%d%c"%(iTradeProfit, gc.getYieldInfo(j).getChar())

						screen.appendTableRow( "TradeRouteTable" )
						screen.setTableText( "TradeRouteTable", 0, iNumTradeRoutes, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "TradeRouteTable", 1, iNumTradeRoutes, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )

						iNumTradeRoutes += 1
## Sevo - Raw Commerce Display - begin
						iNetTradeAmount += iTradeProfit
## Sevo - Raw Commerce Display - end

				if ( iNumTradeRoutes > g_iNumTradeRoutes ):
					g_iNumTradeRoutes = iNumTradeRoutes

				iLeftCount = 0
				iCenterCount = 0
				iRightCount = 0

				for i in xrange(gc.getNumBonusInfos()):
					bHandled = False
					if ( pHeadSelectedCity.hasBonus(i) ):

						iHealth = pHeadSelectedCity.getBonusHealth(i)
						iHappiness = pHeadSelectedCity.getBonusHappiness(i)

						szLeadBuffer = u"<font=1>%c"%(gc.getBonusInfo(i).getChar())

						if (pHeadSelectedCity.getNumBonuses(i) > 1):
							szLeadBuffer += u"(%d)"%(pHeadSelectedCity.getNumBonuses(i))

						szLeadBuffer = szLeadBuffer + "</font>"

						if (iHappiness != 0):
							if (iHappiness > 0):
								szTempBuffer = u"<font=1>+%d%c</font>"%(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
							else:
								szTempBuffer = u"<font=1>+%d%c</font>"%(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

							if (iHealth > 0):
								szTempBuffer += u"<font=1>, +%d%c</font>"%(iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))

							screen.setLabelAt("RightBonusItemLeft" + str(iRightCount), "BonusBack2", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)
							screen.setLabelAt("RightBonusItemRight" + str(iRightCount), "BonusBack2", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 102, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)

							iRightCount = iRightCount + 1

							bHandled = True

						if (iHealth != 0 and not bHandled):
							if ( iHealth > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>"%(iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ))
							else:
								szTempBuffer = u"<font=1>+%d%c</font>"%(-iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

							screen.setLabelAt("CenterBonusItemLeft" + str(iCenterCount), "BonusBack1", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)
							screen.setLabelAt("CenterBonusItemRight" + str(iCenterCount), "BonusBack1", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 62, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)

							iCenterCount = iCenterCount + 1

							bHandled = True

						if ( not bHandled ):
							screen.setLabelAt("LeftBonusItem" + str(iLeftCount), "BonusBack0", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iLeftCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1)

							iLeftCount = iLeftCount + 1

							bHandled = True

				g_iNumLeftBonus = iLeftCount
				g_iNumCenterBonus = iCenterCount
				g_iNumRightBonus = iRightCount

				iMaintenance = pHeadSelectedCity.getMaintenanceTimes100()

				szBuffer = localText.getText("INTERFACE_CITY_MAINTENANCE", ())

				screen.setLabel( "MaintenanceText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 126, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceText" )

## Sevo - Raw Commerce Display - begin
				if (CFG_RAWCOMMERCEDISPLAY):
					szBuffer = localText.getText("TXT_KEY_RCD_PLOT_RAW_COMMERCE", ())
					screen.setLabel( "MaintenanceTextb", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 163, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTextb" )

					szBuffer = localText.getText("TXT_KEY_RCD_TRADE_ROUTES", ())
					screen.setLabel( "MaintenanceTextc", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 183, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTextc" )

					szBuffer = localText.getText("TXT_KEY_RCD_BUILDINGS_AND_SPECIALISTS", ())
					screen.setLabel( "MaintenanceTextd", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 203, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTextd" )

					szBuffer = u"<color=205,180,55,255>%s</color>"%(localText.getText("TXT_KEY_RCD_NET_RAW_COMMERCE", ()))
					screen.setLabel( "MaintenanceTexte", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 223, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTexte" )

					myLittleYield = 0
					# I'd like to get the net plot info, but CyPlot.getYield is all !@#$ up.  It doesn't seem to work at all.
					# Calculate the building & Specialist info instead.
					for ii in xrange(gc.getNumBuildingInfos()):
						if (pHeadSelectedCity.getNumBuilding(ii) != 0):
							myLittleYield += gc.getBuildingInfo(ii).getYieldChange(2)

					# Show Plot Commerces
					szBuffer = u"+%d %c" %(pHeadSelectedCity.getYieldRate(2) - myLittleYield - pHeadSelectedCity.getExtraSpecialistYield(2)-iNetTradeAmount, gc.getYieldInfo(2).getChar())
					screen.setLabel( "MaintenanceTextf", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 163, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTextg" )

					# Show  trade route commerces
					szBuffer = u"+%d %c" %(iNetTradeAmount, gc.getYieldInfo(2).getChar())
					screen.setLabel( "MaintenanceTextg", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 183, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTextf" )

					# Show Modifiers
					szBuffer = u"+%d %c" %(myLittleYield + pHeadSelectedCity.getExtraSpecialistYield(2), gc.getYieldInfo(2).getChar())
					screen.setLabel( "MaintenanceTexth", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 203, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTextf" )

					# Show Total Net Commerce
					szBuffer = u"<color=205,180,55,255>+%d</color> %c" %(pHeadSelectedCity.getYieldRate(2), gc.getYieldInfo(2).getChar())
					screen.setLabel( "MaintenanceTexti", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 223, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "MaintenanceTextg" )
## Sevo - Raw Commerce Display - end

				szBuffer = u"-%d.%02d %c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
				screen.setLabel( "MaintenanceAmountText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 125, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceAmountText" )

				szBuffer = u""

				yCoord = 42
				xOffset = xResolution - 242
				for i in xrange(gc.getNumReligionInfos()):
					xCoord = xOffset + (i * 34)

					bEnable = True

					if (pHeadSelectedCity.isHasReligion(i)):
						if (pHeadSelectedCity.isHolyCityByType(i)):
							screen.show("ReligionHolyCityDDS" + str(i))

						szButton = gc.getReligionInfo(i).getButton()
					else:
						bEnable = False
						szButton = gc.getReligionInfo(i).getButton()

					szName = "ReligionDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				yCoord = 66
				for i in xrange(gc.getNumCorporationInfos()):
					xCoord = xOffset + (i * 34)

					bEnable = True

					if (pHeadSelectedCity.isHasCorporation(i)):
						if (pHeadSelectedCity.isHeadquartersByType(i)):
							screen.show("CorporationHeadquarterDDS" + str(i))
						szButton = gc.getCorporationInfo(i).getButton()
					else:
						bEnable = False
						szButton = gc.getCorporationInfo(i).getButton()

					szName = "CorporationDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				szBuffer = u"%d%% %s" %(pHeadSelectedCity.plot().calculateCulturePercent(pHeadSelectedCity.getOwner()), gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationAdjective(0) )
				screen.setLabel( "NationalityText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 210, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "NationalityText", HitTestTypes.HITTEST_NOHIT )
				screen.show( "NationalityText" )
				iRemainder = 100
				iWhichBar = 0
				for h in range( gc.getMAX_PLAYERS() ):
					if ( gc.getPlayer(h).isAlive() ):
						iPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
						if ( iPercent > 0 ):
							screen.setStackedBarColorsRGB( "NationalityBar", iWhichBar, gc.getPlayer(h).getPlayerTextColorR(), gc.getPlayer(h).getPlayerTextColorG(), gc.getPlayer(h).getPlayerTextColorB(), gc.getPlayer(h).getPlayerTextColorA() )
							if ( iRemainder <= 0):
								screen.setBarPercentage( "NationalityBar", iWhichBar, 0.0 )
							else:
								screen.setBarPercentage( "NationalityBar", iWhichBar, float(iPercent) / iRemainder)
							iRemainder -= iPercent
							iWhichBar += 1
				screen.show( "NationalityBar" )

				iDefenseModifier = pHeadSelectedCity.getDefenseModifier(False)

				if (iDefenseModifier != 0):
					szBuffer = localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))

					if (pHeadSelectedCity.getDefenseDamage() > 0):
						szBuffer += u" (%d%%)"%(((gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage() ) * 100 ) / gc.getMAX_CITY_DEFENSE_DAMAGE())
					screen.setLabel( "DefenseText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 270, 40, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1 )
					screen.show( "DefenseText" )

				if ( pHeadSelectedCity.getCultureLevel != CultureLevelTypes.NO_CULTURELEVEL ):
					iRate = pHeadSelectedCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
					if (iRate%100 == 0):
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), iRate/100))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE_FLOAT", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), u"+%d.%02d" % (iRate/100, iRate%100)))
					if (iRate > 0):
						szBuffer += " %d%s" %((pHeadSelectedCity.getCultureThreshold() * 100.0 - pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner()) + iRate - 1)/iRate, localText.getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()))
					screen.setLabel( "CultureText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 184, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "CultureText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "CultureText" )

				if ((pHeadSelectedCity.getGreatPeopleProgress() > 0) or (pHeadSelectedCity.getGreatPeopleRate() > 0)):
					szBuffer = localText.getText("INTERFACE_CITY_GREATPEOPLE_RATE", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pHeadSelectedCity.getGreatPeopleRate()))

					iGPRate = pHeadSelectedCity.getGreatPeopleRate()
					if (iGPRate > 0):
						szBuffer += " %d%s" %((gc.getPlayer(pHeadSelectedCity.getOwner()).greatPeopleThreshold(False) - pHeadSelectedCity.getGreatPeopleProgress() + iGPRate - 1)/iGPRate, localText.getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()))

					screen.setLabel( "GreatPeopleText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution - 133, yResolution - 180, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "GreatPeopleText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "GreatPeopleText" )

					iFirst = float(pHeadSelectedCity.getGreatPeopleProgress()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) )
					screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) )
					else:
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) ) / ( 1 - iFirst ) )
					screen.show( "GreatPeopleBar" )

				iFirst = float(pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())) / float(100 * pHeadSelectedCity.getCultureThreshold())
				screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_STORED, iFirst )
				if ( iFirst == 1 ):
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) )
				else:
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) ) / ( 1 - iFirst ) )
				screen.show( "CultureBar" )

		else:

			# Help Text Area
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )

			screen.hide( "InterfaceTopLeftBackgroundWidget" )
			screen.hide( "InterfaceTopRightBackgroundWidget" )
			screen.hide( "InterfaceCenterLeftBackgroundWidget" )
			screen.hide( "CityScreenTopWidget" )
			screen.hide( "CityNameBackground" )
			screen.hide( "TopCityPanelLeft" )
			screen.hide( "TopCityPanelRight" )
			screen.hide( "CityScreenAdjustPanel" )
			screen.hide( "InterfaceCenterRightBackgroundWidget" )

## Sevo - Raw Commerce Display - begin
			if (CFG_RAWCOMMERCEDISPLAY):
				screen.hide("CityScreenAdjustPanelb")
## Sevo - Raw Commerce Display - end

			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				self.setMinimapButtonVisibility(True)

		return 0

	# Will update the info pane strings
	def updateInfoPaneStrings( self ):

		iRow = 0

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.addPanel( "SelectedUnitPanel", u"", u"", True, False, 8, yResolution - 140, 280, 130, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitPanel", "Panel_Game_HudStat_Style" )
		screen.hide( "SelectedUnitPanel" )
		screen.hide( "SelectedUnitText" )
		screen.hide( "SelectedUnitLabel" )
		screen.hide( "SelectedCityText" )

		for i in xrange(gc.getNumPromotionInfos()):
			screen.hide("PromotionButton" + str(i))

		if CyEngine().isGlobeviewUp():
			return

		if (pHeadSelectedCity):

			screen.addTableControlGFC( "SelectedCityText", 3, 10, yResolution - 139, 183, 128, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
			screen.setStyle( "SelectedCityText", "Table_EmptyScroll_Style" )
			screen.hide( "SelectedCityText" )
			screen.hide( "SelectedUnitText" )

			iOrders = CyInterface().getNumOrdersQueued()

			screen.setTableColumnHeader( "SelectedCityText", 0, u"", 130 )
			screen.setTableColumnHeader( "SelectedCityText", 1, u"", 45 )
			screen.setTableColumnHeader( "SelectedCityText", 2, u"", 10 )
			screen.setTableColumnRightJustify( "SelectedCityText", 1 )
			screen.setTableNumRows("SelectedCityText", iOrders)

			OrderNodeType = CyInterface().getOrderNodeType
			OederNodeData1 = CyInterface().getOrderNodeData1
			for i in xrange(iOrders):

				iOrderNodeType = OrderNodeType(i)
				szLeftBuffer = u""
				szRightBuffer = u""

				if (iOrderNodeType == OrderTypes.ORDER_TRAIN ):
					szLeftBuffer = gc.getUnitInfo(OederNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(OederNodeData1(i), i)) + ")"

					if (CyInterface().getOrderNodeSave(i)):
						szLeftBuffer = u"*" + szLeftBuffer

				elif (iOrderNodeType == OrderTypes.ORDER_CONSTRUCT ):
					szLeftBuffer = gc.getBuildingInfo(OederNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(OederNodeData1(i), i)) + ")"

				elif (iOrderNodeType == OrderTypes.ORDER_CREATE ):
					szLeftBuffer = gc.getProjectInfo(OederNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(OederNodeData1(i), i)) + ")"

				elif (iOrderNodeType == OrderTypes.ORDER_MAINTAIN ):
					szLeftBuffer = gc.getProcessInfo(OederNodeData1(i)).getDescription()

				screen.setTableText( "SelectedCityText", 0, i, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.setTableText( "SelectedCityText", 1, i, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )

			screen.show( "SelectedCityText" )
			screen.show( "SelectedUnitPanel" )

		elif (pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):

			screen.addTableControlGFC( "SelectedUnitText", 3, 10, yResolution - 109, 183, 102, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
			screen.setStyle( "SelectedUnitText", "Table_EmptyScroll_Style" )
			screen.hide( "SelectedUnitText" )
			screen.hide( "SelectedCityText" )

			screen.setTableColumnHeader( "SelectedUnitText", 0, u"", 100 )
			screen.setTableColumnHeader( "SelectedUnitText", 1, u"", 75 )
			screen.setTableColumnHeader( "SelectedUnitText", 2, u"", 10 )
			screen.setTableColumnRightJustify( "SelectedUnitText", 1 )

			if (CyInterface().mirrorsSelectionGroup()):
				pSelectedGroup = pHeadSelectedUnit.getGroup()
			else:
				pSelectedGroup = 0

			if (CyInterface().getLengthSelectionList() > 1):

				screen.setText( "SelectedUnitLabel", "Background", localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), )), CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )

				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					if (pHeadSelectedUnit):
						for i in xrange(gc.getNumUnitInfos()):
							iCount = CyInterface().countEntities(i)

							if (iCount > 0):
								szRightBuffer = u""

								szLeftBuffer = gc.getUnitInfo(i).getDescription()

								if (iCount > 1):
									szRightBuffer = u"(" + str(iCount) + u")"

								screen.appendTableRow( "SelectedUnitText" )
								screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
								screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
								screen.show( "SelectedUnitText" )
								screen.show( "SelectedUnitPanel" )
								iRow += 1
			else:

				if (pHeadSelectedUnit.getHotKeyNumber() == -1):
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (pHeadSelectedUnit.getName(), ))
				else:
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), pHeadSelectedUnit.getName()))
				if (len(szBuffer) > 60):
					szBuffer = "<font=2>" + szBuffer + "</font>"
				screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )

				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )

					szLeftBuffer = u""
					szRightBuffer = u""

					if (pHeadSelectedUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
						if (pHeadSelectedUnit.airBaseCombatStr() > 0):
							szLeftBuffer = localText.getText("INTERFACE_PANE_AIR_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.airBaseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					else:
						if (pHeadSelectedUnit.canFight()):
							szLeftBuffer = localText.getText("INTERFACE_PANE_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))

					if (szLeftBuffer + szRightBuffer):
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					szLeftBuffer = u""
					szRightBuffer = u""

					if ( (pHeadSelectedUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0 ):
						iDenom = 1
					else:
						iDenom = 0
					iCurrMoves = ((pHeadSelectedUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
					szLeftBuffer = localText.getText("INTERFACE_PANE_MOVEMENT", ())
					if (pHeadSelectedUnit.baseMoves() == iCurrMoves):
						szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
					else:
						szRightBuffer = u"%d/%d%c" %(iCurrMoves, pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )

					screen.appendTableRow( "SelectedUnitText" )
					screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )
					iRow += 1
					
					
					
					
					
					#### <written by F> #####
					
					
					#東方ユニットであればカードアタックレベルを表示
					if pHeadSelectedUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
						#szLeftBuffer = localText.getText("INTERFACE_PANE_EXPERIENCE", ())
						szLeftBuffer = "CA&#12524;&#12505;&#12523;"
						szRightBuffer = u"%d" %(pHeadSelectedUnit.countCardAttackLevel())
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1
					
					
					#東方ユニットであればPower表示
					if pHeadSelectedUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or pHeadSelectedUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
						#szLeftBuffer = localText.getText("INTERFACE_PANE_EXPERIENCE", ())
						szLeftBuffer = "Power"
						szRightBuffer = u"%0.2f" %(pHeadSelectedUnit.getPower())
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1
					
					
					if (pHeadSelectedUnit.getLevel() > 0):

						szLeftBuffer = localText.getText("INTERFACE_PANE_LEVEL", ())
						szRightBuffer = u"%d" %(pHeadSelectedUnit.getLevel())

						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					if ((pHeadSelectedUnit.getExperience() > 0) and not pHeadSelectedUnit.isFighting()):
						szLeftBuffer = localText.getText("INTERFACE_PANE_EXPERIENCE", ())
						szRightBuffer = u"(%d/%d)" %(pHeadSelectedUnit.getExperience(), pHeadSelectedUnit.experienceNeeded())
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					iPromotionCount = 0
					for i in xrange(gc.getNumPromotionInfos()):
						if (pHeadSelectedUnit.isHasPromotion(i)):
							szName = "PromotionButton" + str(i)
							self.setPromotionButtonPosition( szName, iPromotionCount )
							screen.moveToFront( szName )
							screen.show( szName )

							iPromotionCount = iPromotionCount + 1

			if (pSelectedGroup):

				iNodeCount = pSelectedGroup.getLengthMissionQueue()

				if (iNodeCount > 1):
					for i in xrange( iNodeCount ):
						szLeftBuffer = u""
						szRightBuffer = u""

						if (gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild()):
							if (i == 0):
								szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
								szRightBuffer = localText.getText("INTERFACE_CITY_TURNS", (pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0), ))
							else:
								szLeftBuffer = u"%s..." %(gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription())
						else:
							szLeftBuffer = u"%s..." %(gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription())

						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

		return 0

	# Will update the scores
	def updateScoreStrings(self):
		global CFG_CIV_NAME_ON_SCOREBOARD

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.hide("ScoreBackground")

		for szName in self.ScoreAttCache:
			screen.hide(szName)
		self.ScoreAttCache = []

		iWidth = 0
		iCount = 0
		iBtnHeight = 19

		##### <written by F> #####
		#パネルの調整幅
		toho_width = 0
		
		#東方ユニットの最大数を調べる
		for i in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(i)
			iNum = 0
			(loopUnit, iter) = pPlayer.firstUnit(false)
			while( loopUnit ):
				if ( not loopUnit.isDead() ): 
					if loopUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or loopUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
						iNum = iNum + 1
				(loopUnit, iter) = pPlayer.nextUnit(iter, false)
			
			if toho_width < iNum * 16:
				toho_width = iNum * 16

		#一度ユニット表示を全て解除
		for k_temp in range( gc.getNumUnitInfos() ):
			if gc.getUnitInfo(k_temp).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or gc.getUnitInfo(k_temp).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
				szName = "TohoUnitButton" + str(k_temp)
				screen.hide( szName )
		
		##### <written by F> #####

		if ((CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY)):
			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyEngine().isGlobeviewUp() == false):

				i = gc.getMAX_CIV_TEAMS() - 1
				iActivePlayer = gc.getGame().getActivePlayer()
				szActPlayerName = gc.getPlayer(iActivePlayer).getName()
				ActiveTeam = gc.getGame().getActiveTeam()
				pActiveTeam = gc.getTeam(ActiveTeam)
				ActiveCanEspMission = gc.getPlayer(iActivePlayer).canDoEspionageMission
				GetPlayerScore = gc.getGame().getPlayerScore
				IsSpendEspionagePoint = CGEUtils.CGEUtils().isSpendEspionagePoint
				xCoord = xResolution - 12
				if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
					yCoord = yResolution - 206
				else:
					yCoord = yResolution - 88

				bCanShowPower = False
				# See if Espionage allows graph to be shown for each player
				if (gc.getEspionageMissionInfo(self.iSeeDemoMission).isSeeDemographics()):
					bCanShowPower = True

				MetPlayerList = [iPlayer for iPlayer in range(gc.getMAX_CIV_PLAYERS()) if (pActiveTeam.isHasMet(gc.getPlayer(iPlayer).getTeam()) and gc.getPlayer(iPlayer).isAlive() and not gc.getPlayer(iPlayer).isMinorCiv() and iPlayer != iActivePlayer)]

				sMetTeamList = set([iTeam for iTeam in range(gc.getMAX_CIV_TEAMS()) if (pActiveTeam.isHasMet(iTeam)) and gc.getTeam(iTeam).isAlive()])
				sVassalList = set([iTeam for iTeam in sMetTeamList if gc.getTeam(iTeam).isAVassal()])
				sMasterList = set()
				sNotVassalList = sMetTeamList.difference(sVassalList)
				for iTeam in sVassalList:
					sMasterList.update([iLoopTeam for iLoopTeam in sNotVassalList if (gc.getTeam(iTeam).isVassal(iLoopTeam))])
				#iActivePlayerDefPower = gc.getTeam(gc.getPlayer(iActivePlayer).getTeam()).getDefensivePower()
				iActivePlayerDefPower = gc.getPlayer(iActivePlayer).getPower()
				for iLoopPlayer in MetPlayerList:
					if (bCanShowPower and ActiveCanEspMission(0, iLoopPlayer, None, -1)):
						pLoopTeam = gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam())
						if (gc.getPlayer(iLoopPlayer).getTeam() == ActiveTeam or pLoopTeam.isVassal(ActiveTeam) or pLoopTeam.isDefensivePact(ActiveTeam)):
							iActivePlayerDefPower += gc.getPlayer(iLoopPlayer).getPower()
				iChairUN = -1
				iChairUN2 = -1
				iChairPOPE = -1
				if (gc.getGame().canHaveSecretaryGeneral(0)): # VoteSourceTypes.DIPLOVOTE_UN
					iChairUN = gc.getGame().getSecretaryGeneral(0)
				if (gc.getGame().canHaveSecretaryGeneral(1)): # VoteSourceTypes.DIPLOVOTE_UN2
					iChairUN2 = gc.getGame().getSecretaryGeneral(1)
				if (gc.getGame().canHaveSecretaryGeneral(1)): # VoteSourceTypes.DIPLOVOTE_POPE
					iChairPOPE = gc.getGame().getSecretaryGeneral(2)

				tradeData = TradeData()
				tradeData.ItemType = TradeableItems.TRADE_WAR

				while (i > -1):
					eTeam = gc.getGame().getRankTeam(i)

					if (pActiveTeam.isHasMet(eTeam) or gc.getTeam(eTeam).isHuman() or gc.getGame().isDebugMode()):
						j = gc.getMAX_CIV_PLAYERS() - 1
						while (j > -1):
							ePlayer = gc.getGame().getRankPlayer(j)
							pPlayer = gc.getPlayer(ePlayer)
							bPlayerAlive = pPlayer.isAlive()

							if (not CyInterface().isScoresMinimized() or iActivePlayer == ePlayer):
								# < Dead Civ Scoreboard Mod Start >
								bDisplayCivScore = True

								if(g_bHideDeadCivilizations and not bPlayerAlive):
									bDisplayCivScore = False
								# < Dead Civ Scoreboard Mod End >

								if (pPlayer.isEverAlive() and not pPlayer.isMinorCiv()):

									# < Dead Civ Scoreboard Mod Start >
									if (not bDisplayCivScore):
										j -= 1
										continue
									# < Dead Civ Scoreboard Mod End >

									if (pPlayer.getTeam() == eTeam):
										szBuffer = u"<font=2>"

										if (gc.getGame().isGameMultiPlayer()):
											if (not (pPlayer.isTurnActive())):
												szBuffer += u"*"

										pTeam = gc.getTeam(eTeam)
										ePlayerPower = pPlayer.getPower()

										szPlayerName = pPlayer.getName()
										if (CFG_CIV_NAME_ON_SCOREBOARD):
											szPlayerName += u"(" + pPlayer.getCivilizationAdjective(0) + u")"

										szChair = u""
										if (bPlayerAlive):
											if (eTeam in sMasterList):
												szPlayerName = u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR) + szPlayerName
											elif (eTeam in sVassalList):
												if (CFG_MASTER_NAME_ON_SCOREBOARD):
													for iLoopPlayer in sMasterList:
														pLoopPlayer = gc.getPlayer(iLoopPlayer)
														if (pTeam.isVassal(pLoopPlayer.getTeam())):
															szPlayerName += u"%c<color=%d,%d,%d,%d>%s</color>"%(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR), pLoopPlayer.getPlayerTextColorR(), pLoopPlayer.getPlayerTextColorG(), pLoopPlayer.getPlayerTextColorB(), pLoopPlayer.getPlayerTextColorA(), pLoopPlayer.getName())
												else:
													if (pTeam.isVassal(ActiveTeam)):
														szPlayerName = u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR) + szPlayerName
													else:
														szPlayerName = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR) + szPlayerName

											if (eTeam == iChairUN) or (eTeam == iChairUN2):
												szChair += u"%c" % CyGame().getSymbolID(FontSymbols.MAP_CHAR)
											if (eTeam == iChairPOPE):
												szChair += u"%c" % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR)
											szPlayerName = szChair + szPlayerName

										if (not CyInterface().isFlashingPlayer(ePlayer) or CyInterface().shouldFlash(ePlayer)):
											if (ePlayer == iActivePlayer):
												if (ePlayerPower ==  iActivePlayerDefPower):
													szBuffer += u"%d(%d): %s[<color=%d,%d,%d,%d>%s</color>]"%(GetPlayerScore(ePlayer), ePlayerPower, szChair, pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), szActPlayerName)
												else:
													szBuffer += u"%d(%d, D%d): %s[<color=%d,%d,%d,%d>%s</color>]"%(GetPlayerScore(ePlayer), ePlayerPower, iActivePlayerDefPower, szChair, pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), szActPlayerName)
											else:
												szWarPlan = u""
												if (pTeam.getAnyWarPlanCount(True) > 0):
													for iPlayer in MetPlayerList:
														if (iPlayer != ePlayer and pTeam.isHasMet(gc.getPlayer(iPlayer).getTeam())):
															tradeData.iData = iPlayer
															if (pPlayer.getTradeDenial(iActivePlayer, tradeData) == DenialTypes.DENIAL_TOO_MANY_WARS):
																szWarPlan = unichr(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR))
																break
## CGE-LE - Golden Age - begin
												if (pPlayer.getGoldenAgeTurns() > 0):
													szPlayerScore = u"<color=255,191,0>%d</color>"%(GetPlayerScore(ePlayer))
												else:
													szPlayerScore = u"%d"%(GetPlayerScore(ePlayer))
												if (g_bShowDeadTag and not bPlayerAlive):
													szPlayerScore = localText.getText("TXT_DEAD_CIV_SCOREBOARD_DEAD", ())
												elif (bCanShowPower and ActiveCanEspMission(0, ePlayer, None, -1)):
													if (iActivePlayerDefPower < (ePlayerPower * gc.getLeaderHeadInfo(ePlayer).getMaxWarDistantPowerRatio() / 100)):
## CGE-LE - Open Borders Trading - begin
														szPlayerScore += u"%s(<color=255,0,0>%d</color>)"%(szWarPlan, ePlayerPower)
													elif (iActivePlayerDefPower < (ePlayerPower * gc.getLeaderHeadInfo(ePlayer).getMaxWarNearbyPowerRatio() / 100)):
														szPlayerScore += u"%s(<color=255,255,0>%d</color>)"%(szWarPlan, ePlayerPower)
													else:
														szPlayerScore += u"%s(%d)"%(szWarPlan, ePlayerPower)
												else:
													#if (szWarPlan != u""):
													#	szWarPlan = u"(" + szWarPlan + u")"
## CGE-LE - Open Borders Trading - end
													szPlayerScore += u"%s"%(szWarPlan)
## CGE-LE - Golden Age - end
												if(g_bGreyOutDeadCivilizations and not bPlayerAlive):
													szBuffer += u"%s: <color=175,175,175>%s</color>" %(szPlayerScore, szPlayerName)
												else:
													szBuffer += u"%s: <color=%d,%d,%d,%d>%s</color>" %(szPlayerScore, pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), szPlayerName)
										else:
											szBuffer += u"%d(%d): %s" %(GetPlayerScore(ePlayer), ePlayerPower, szPlayerName)

										if (pTeam.isAlive()):
											if (not (pActiveTeam.isHasMet(eTeam))):
												szBuffer += (" ?")
											if (pTeam.isAtWar(ActiveTeam)):
												iColor = gc.getInfoTypeForString("COLOR_RED")
## CGE-LE - Open Borders Trading - begin
#CGE-LEの機能で戦争中のAIが和平可能なら「戦争」の文字が黄色になる
#が、その状態だと他のAIの手一杯表示が消えてしまう副作用が発生するため、元に戻す
#本家CGE-LEが上記手一杯バグに対応したため修正（14/12/28)
												if (self.bHasCGEDLL or self.bHasCGELEDLL):
## CGE-LE - Open Borders Trading - end
													if (pPlayer.AI_isWillingToTalk(iActivePlayer)):
## CGE-LE 1.0.4 - Willing Talk Fix - begin
														willingTalkData = TradeData()
														willingTalkData.ItemType = TradeableItems.TRADE_SURRENDER
														if (pPlayer.canTradeItem(iActivePlayer, willingTalkData, True)):
															iColor = gc.getInfoTypeForString("COLOR_GREEN")
														else:
															willingTalkData.ItemType = TradeableItems.TRADE_PEACE_TREATY
															if (pPlayer.canTradeItem(iActivePlayer, willingTalkData, True)):
## CGE-LE 1.0.4 - Willing Talk Fix - end
																iColor = gc.getInfoTypeForString("COLOR_YELLOW")
												szBuffer += "("  + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), iColor).upper() + ")"
											if (pPlayer.canTradeNetworkWith(iActivePlayer) and (ePlayer != iActivePlayer)):
												szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
											if (pTeam.isOpenBorders(ActiveTeam)):
												szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR))
## CGE-LE - Open Borders Trading - begin
											elif (pPlayer.getTeam() != ActiveTeam and pPlayer.AI_getMemoryCount(iActivePlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT) <= 0):
												tradeOpenBordersData = TradeData()
												tradeOpenBordersData.ItemType = TradeableItems.TRADE_OPEN_BORDERS
												if (pPlayer.canTradeItem(ActiveTeam, tradeOpenBordersData, True)):
													szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))
## CGE-LE - Open Borders Trading - end
											if (pTeam.isDefensivePact(ActiveTeam)):
												szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR))
											if (pPlayer.getStateReligion() != -1):
												if (pPlayer.hasHolyCity(pPlayer.getStateReligion())):
													szBuffer += u"%c" %(gc.getReligionInfo(pPlayer.getStateReligion()).getHolyCityChar())
												else:
													szBuffer += u"%c" %(gc.getReligionInfo(pPlayer.getStateReligion()).getChar())
											iETeamEsp = pTeam.getEspionagePointsAgainstTeam(ActiveTeam)
											iActiveTeamEsp = pActiveTeam.getEspionagePointsAgainstTeam(eTeam)
											if (iETeamEsp < iActiveTeamEsp):
												szBuffer += u"%c"%(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
											if (iActiveTeamEsp != 0):
												if (IsSpendEspionagePoint(eTeam, iETeamEsp)):
## CGE-LE - Open Borders Trading - begin
													szBuffer += u"(<color=255,0,0>%.1f</color>)"%(float(iETeamEsp)/iActiveTeamEsp)
												else:
													szBuffer += u"(%.1f)"%(float(iETeamEsp)/iActiveTeamEsp)
											#elif (ePlayer != iActivePlayer):
											#	szBuffer += u"(-)"
## CGE-LE - Open Borders Trading - end
										bEspionageCanSeeResearch = ActiveCanEspMission(self.iSeeResMission, ePlayer, None, -1)

										if (((pPlayer.getTeam() == ActiveTeam) and (pActiveTeam.getNumMembers() > 1)) or (pTeam.isVassal(ActiveTeam)) or gc.getGame().isDebugMode() or bEspionageCanSeeResearch):
											if (pPlayer.getCurrentResearch() != -1):
												szBuffer += u"-%s (%d)" %(gc.getTechInfo(pPlayer.getCurrentResearch()).getDescription(), pPlayer.getResearchTurnsLeft(pPlayer.getCurrentResearch(), True))
										if (CyGame().isNetworkMultiPlayer()):
											szBuffer += CyGameTextMgr().getNetStats(ePlayer)

										if (pPlayer.isHuman() and CyInterface().isOOSVisible()):
											szBuffer += u" <color=255,0,0>* %s *</color>" %(CyGameTextMgr().getOOSSeeds(ePlayer))

										##### <written by F> #####
										#所持東方ユニットのリスト
										lUnit = []
										(loopUnit, iter) = pPlayer.firstUnit(false)
										while( loopUnit ):
											if ( not loopUnit.isDead() ): 
												if loopUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or loopUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
													if loopUnit.isHasPromotion( gc.getInfoTypeForString('PROMOTION_BUNSHIN') ) == False:
														lUnit.append(loopUnit)
											(loopUnit, iter) = pPlayer.nextUnit(iter, false)

										if (not pPlayer.isHuman() and bPlayerAlive):
## CGE-LE - Open Borders Trading - begin
											szBuffer += u": "
## CGE-LE - Open Borders Trading - end
											szName = "ScoreAttFont" + str(ePlayer) + "_" + str(int(pPlayer.AI_getAttitude(iActivePlayer)))
											if (pPlayer.getWorstEnemyName() == szActPlayerName):
												szName += "WE"
											screen.moveItem(szName, xCoord - 16 - toho_width, yCoord - (iCount * iBtnHeight) + 5, -0.3)
											screen.show(szName)
											self.ScoreAttCache.append(szName)
											xpos = xCoord - 15
										else:
											xpos = xCoord

										#ここから
										szBuffer += u"</font>"

										iBufferWidth = CyInterface().determineWidth(szBuffer)
										if (iBufferWidth  > iWidth):
											iWidth = iBufferWidth

										szName = "ScoreText" + str(ePlayer)
										self.ScoreAttCache.append(szName)

										iWidgetType = WidgetTypes.WIDGET_CONTACT_CIV
										iPlayer = ePlayer
										if (not bPlayerAlive):
											iWidgetType = WidgetTypes.WIDGET_GENERAL
											iPlayer = -1
										if (self.ScoreTextCache[ePlayer] != szBuffer):
											screen.setText(szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xpos - toho_width, yCoord - (iCount * iBtnHeight), -0.3, FontTypes.SMALL_FONT, iWidgetType, iPlayer, -1)
											screen.show(szName)
											self.ScoreTextCache[ePlayer] = szBuffer
										#ここまでは一箇所（toho_width）のみ変更
										else:
											screen.moveItem(szName, xpos - iBufferWidth -4 - toho_width, yCoord - (iCount * iBtnHeight), -0.3)
											screen.show(szName)
										for k_temp in range(len(lUnit)):
											szName = "TohoUnitButton" + str(lUnit[k_temp].getUnitType())
											screen.moveItem(szName,xResolution - 4 - toho_width + k_temp*16 -4, yCoord - (iCount * iBtnHeight) + 1,-0.3)
											screen.show(szName)

										CyInterface().checkFlashReset(ePlayer)

										iCount += 1
							j -= 1
					i -= 1

				if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
					yCoord = yResolution - 186
				else:
					yCoord = yResolution - 68
				screen.setPanelSize( "ScoreBackground", xResolution - 37 - iWidth - toho_width, yCoord - (iBtnHeight * iCount) - 7, iWidth + 28, (iBtnHeight * iCount) + 11 )
				screen.show( "ScoreBackground" )

	# Will update the help Strings
	def updateHelpStrings( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL ):
			screen.setHelpTextString( "" )
		else:
			screen.setHelpTextString( CyInterface().getHelpString() )

		return 0

	# Will set the promotion button position
	def setPromotionButtonPosition( self, szName, iPromotionCount ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		yResolution = screen.getYResolution()

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.moveItem( szName, 266 - (24 * (iPromotionCount / 6)), yResolution - 144 + (24 * (iPromotionCount % 6)), -0.3 )

	# Will set the selection button position
	def setResearchButtonPosition( self, szButtonID, iCount ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		screen.moveItem( szButtonID, 283 + ( ( xResolution - 1024 ) / 2 ) + ( 31 * ( iCount % 16 ) ), 2 + ( 32 * ( iCount / 16 ) ), -0.3 )

	# Will set the selection button position
	def setScoreTextPosition( self, szButtonID, iWhichLine ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			yCoord = yResolution - 180
		else:
			yCoord = yResolution - 88
		screen.moveItem( szButtonID, 996, yCoord - (iWhichLine * 18), -0.3 )

	# Will build the globeview UI
	def updateGlobeviewButtons( self ):
		kInterface = CyInterface()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()
		iCurrentLayerID = kGLM.getCurrentLayerID()

		# Positioning things based on the visibility of the globe
		if kEngine.isGlobeviewUp():
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		else:
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )


		# Set base Y position for the LayerOptions, if we find them
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iGlobeLayerOptionsY_Minimal
		else:
			iY = yResolution - iGlobeLayerOptionsY_Regular

		# Hide the layer options ... all of them
		for i in xrange(20):
			screen.hide("GlobeLayerOption" + str(i))

		# Setup the GlobeLayer panel
		iNumLayers = kGLM.getNumLayers()
		if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
			# set up panel
			if iCurrentLayerID != -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() != 0:
				bHasOptions = True
			else:
				bHasOptions = False
				screen.hide( "ScoreBackground" )

			# set up toggle button
			screen.setState("GlobeToggle", True)

			# Set GlobeLayer indicators correctly
			for i in xrange(kGLM.getNumLayers()):
				screen.setState("GlobeLayer" + str(i), iCurrentLayerID == i )

			# Set up options pane
			if bHasOptions:
				kLayer = kGLM.getLayer(iCurrentLayerID)

				iCurY = iY
				iNumOptions = kLayer.getNumOptions()
				iCurOption = kLayer.getCurrentOption()
				iMaxTextWidth = -1
				for iTmp in xrange(iNumOptions):
					iOption = iTmp # iNumOptions - iTmp - 1
					szName = "GlobeLayerOption" + str(iOption)
					szCaption = kLayer.getOptionName(iOption)
					if(iOption == iCurOption):
						szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
					else:
						szBuffer = "  %s  " % (szCaption)
					iTextWidth = CyInterface().determineWidth( szBuffer )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1 )
					screen.show( szName )

					iCurY -= iGlobeLayerOptionHeight

					if iTextWidth > iMaxTextWidth:
						iMaxTextWidth = iTextWidth

				#make extra space
				iCurY -= iGlobeLayerOptionHeight;
				iPanelWidth = iMaxTextWidth + 32
				iPanelHeight = iY - iCurY
				iPanelX = xResolution - 14 - iPanelWidth
				iPanelY = iCurY
				screen.setPanelSize( "ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
				screen.show( "ScoreBackground" )

		else:
			if iCurrentLayerID != -1:
				kLayer = kGLM.getLayer(iCurrentLayerID)
				if kLayer.getName() == "RESOURCES":
					screen.setState("ResourceIcons", True)
				else:
					screen.setState("ResourceIcons", False)

				if kLayer.getName() == "UNITS":
					screen.setState("UnitIcons", True)
				else:
					screen.setState("UnitIcons", False)
			else:
				screen.setState("ResourceIcons", False)
				screen.setState("UnitIcons", False)

			screen.setState("Grid", CyUserProfile().getGrid())
			screen.setState("BareMap", CyUserProfile().getMap())
			screen.setState("Yields", CyUserProfile().getYields())
			screen.setState("ScoresVisible", CyUserProfile().getScores())

			screen.hide( "InterfaceGlobeLayerPanel" )
			screen.setState("GlobeToggle", False )

	# Update minimap buttons
	def setMinimapButtonVisibility( self, bVisible):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		kInterface = CyInterface()
		kGLM = CyGlobeLayerManager()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( CyInterface().isCityScreenUp() ):
			bVisible = False

		kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
		kGlobeButtons = ["GlobeLayer" + str(i) for i in range(kGLM.getNumLayers())]

		if bVisible:
			if CyEngine().isGlobeviewUp():
				kHide = kMainButtons
				kShow = kGlobeButtons
			else:
				kHide = kGlobeButtons
				kShow = kMainButtons
			screen.show( "GlobeToggle" )

		else:
			kHide = kMainButtons + kGlobeButtons
			kShow = []
			screen.hide( "GlobeToggle" )

		for szButton in kHide:
			screen.hide(szButton)

		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iMinimapButtonsY_Minimal
			iGlobeY = yResolution - iGlobeButtonY_Minimal
		else:
			iY = yResolution - iMinimapButtonsY_Regular
			iGlobeY = yResolution - iGlobeButtonY_Regular

		iBtnX = xResolution - 39
		screen.moveItem("GlobeToggle", iBtnX, iGlobeY, 0.0)

		iBtnAdvance = 28
		iBtnX = iBtnX - len(kShow)*iBtnAdvance - 10
		if len(kShow) > 0:
			for szButton in kShow:
				screen.moveItem(szButton, iBtnX, iY, 0.0)
				screen.moveToFront(szButton)
				screen.show(szButton)
				iBtnX += iBtnAdvance

	def createGlobeviewButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()

		for i in xrange (kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)

			kLayer = kGLM.getLayer(i)
			szStyle = kLayer.getButtonStyle()

			if szStyle == 0 or szStyle == "":
				szStyle = "Button_HUDSmall_Style"

			screen.addCheckBoxGFC( szButtonID, "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_GLOBELAYER, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.setStyle( szButtonID, szStyle )
			screen.hide( szButtonID )


	def createMinimapButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.addCheckBoxGFC( "UnitIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_UNIT_ICONS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "UnitIcons", "Button_HUDGlobeUnit_Style" )
		screen.setState( "UnitIcons", False )
		screen.hide( "UnitIcons" )

		screen.addCheckBoxGFC( "Grid", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GRID).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Grid", "Button_HUDBtnGrid_Style" )
		screen.setState( "Grid", False )
		screen.hide( "Grid" )

		screen.addCheckBoxGFC( "BareMap", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_BARE_MAP).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "BareMap", "Button_HUDBtnClearMap_Style" )
		screen.setState( "BareMap", False )
		screen.hide( "BareMap" )

		screen.addCheckBoxGFC( "Yields", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_YIELDS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Yields", "Button_HUDBtnTileAssets_Style" )
		screen.setState( "Yields", False )
		screen.hide( "Yields" )

		screen.addCheckBoxGFC( "ScoresVisible", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_SCORES).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ScoresVisible", "Button_HUDBtnRank_Style" )
		screen.setState( "ScoresVisible", True )
		screen.hide( "ScoresVisible" )

		screen.addCheckBoxGFC( "ResourceIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RESOURCE_ALL).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ResourceIcons", "Button_HUDBtnResources_Style" )
		screen.setState( "ResourceIcons", False )
		screen.hide( "ResourceIcons" )

		screen.addCheckBoxGFC( "GlobeToggle", "", "", -1, -1, 36, 36, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GLOBELAYER).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "GlobeToggle", "Button_HUDZoom_Style" )
		screen.setState( "GlobeToggle", False )
		screen.hide( "GlobeToggle" )

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		FuncName = inputClass.getFunctionName()
		iNotifyCode = inputClass.getNotifyCode()

		if (self.CFG_Enabled_APL):
			if (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_ON and FuncName.startswith("APL")):
				self.showButtonDescInfoPane(FuncName)
				return 1
			elif (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and FuncName.startswith("APL")):
				self.hideInfoPane()
				return 1

			if  (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_ON) or \
				(iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) or \
				(iNotifyCode == NotifyCode.NOTIFY_CLICKED):
				if (self.MainInterfaceInputMap.has_key(FuncName)):
					return self.MainInterfaceInputMap[FuncName](inputClass)
				elif (self.MainInterfaceInputMap.has_key(FuncName + "1")):
					return self.MainInterfaceInputMap[FuncName + "1"](inputClass)

		if (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_ON):
			if (FuncName == "TradeResourceButton"):
				self.showButtonDescInfoPane("APL_TRADE_RESOURCE_PANEL")
				return 1
			elif (FuncName == "UnitPlacementButton"):
				self.showButtonDescInfoPane("UNIT_PLACEMENT_BUTTON_HELP")
				return 1
			elif (FuncName == "AlertsLogButton"):
				self.showButtonDescInfoPane("ALERTS_LOG_BUTTON_HELP")
				return 1
			elif (FuncName == "SpyAlertButton"):
				self.showButtonDescInfoPane("SPY_ALERT_BUTTON_HELP")
				return 1
		elif (iNotifyCode == NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			if (FuncName == "UnitStatsButton" or FuncName == "TradeResourceButton" or FuncName == "UnitPlacementButton" or FuncName == "AlertsLogButton" or FuncName == "SpyAlertButton" or FuncName == "WinAMPButton" or FuncName == "WinAMPMuteButton"):
				self.hideInfoPane()
				return 1
		elif (iNotifyCode == NotifyCode.NOTIFY_CLICKED):
			if (FuncName == "APLModeSelect"):
				self.showAPLModeSelect()
				return 1
			if (FuncName == "APLGrpModeSelect"):
				self.showAPLGrpModeSelect()
				return 1
			if (FuncName == "TradeResourceButton"):
				TradeResourcePanel.TradeResourcePanel().ToggleTradeResourcePanel()
				return 1
			elif (FuncName == "MonopolyText"):
				getKeyEvent = CvEventInterface.getEventManager()
				if (getKeyEvent.bShift):
					TradeResourcePanel.TradeResourcePanel().showTradeResourcePanelConfig()
					return 1
				elif (getKeyEvent.bAlt):
					#message = "Debug Message: "
					#CyInterface().addImmediateMessage(message,"")
					return 1
				else:
					TradeResourcePanel.TradeResourcePanel().ToggleTradeResourcePanel_Trade()
					return 1
			elif (FuncName == "UnitPlacementButton"):
				CvUnitPlacementScreen.CvUnitPlacementScreen().interfaceScreen()
				return 1
			elif (FuncName == "AlertsLogButton"):
				AlertsLog.AlertsLog().interfaceScreen()
				return 1
			elif (FuncName == "SpyAlertButton"):
				if (CvEventInterface.getEventManager().bShift):
					CGEUtils.CGEUtils().SpyMoveToCity(CyInterface().getHeadSelectedUnit())
				else:
					CGEUtils.CGEUtils().setSpyAlert(CyInterface().getHeadSelectedUnit())
				return 1
			elif (FuncName == "LoadFullButton"):
				CGEUtils.CGEUtils().FullLoadUnits(CyInterface().getHeadSelectedUnit())
				return 1
			elif (FuncName == "AutoReconButton"):
				CGEUtils.CGEUtils().AutoReconSetMode(CyInterface().getHeadSelectedUnit().getID(), CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).getCheckBoxState("AutoReconButton1"))
				return 1
			elif (FuncName == "CancelAutoReconButton"):
				CGEUtils.CGEUtils().cancelAutoReconMode(CyInterface().getHeadSelectedUnit().getID())
				return 1
			elif (FuncName == "AutoInsertQueueButton"):
				self.AutoInsertQueuePanel()
				return 1
			elif (FuncName == "AutoInsertPQUp"):
				self.AutoInsertPQUp()
				return 1
			elif (FuncName == "AutoInsertPQDown"):
				self.AutoInsertPQDown()
				return 1
			elif (FuncName == "AutoInsertPQDelete"):
				self.AutoInsertPQDelete()
				return 1
		elif (iNotifyCode == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (FuncName == "APLModeSelectList"):
				iIndex = inputClass.getData()
				if (iIndex == 0):
					self.sAPLMode = self.APL_MODE_MULTILINE
				elif (iIndex == 1):
					self.sAPLMode = self.APL_MODE_STACK_VERT
				elif (iIndex == 2):
					self.sAPLMode = self.APL_MODE_STACK_HORIZ
				self.hideAPLModeSelect()
				self.setAPLMode()
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				self.hideAPLModeSelect()
				return 1
			if (FuncName == "APLGrpModeSelectList"):
				iIndex = inputClass.getData()
				if (iIndex == 0):
					self.nAPLGrpMode = self.APL_GRP_UNITTYPE
				elif (iIndex == 1):
					self.nAPLGrpMode = self.APL_GRP_GROUPS
				elif (iIndex == 2):
					self.nAPLGrpMode = self.APL_GRP_PROMO
				elif (iIndex == 3):
					self.nAPLGrpMode = self.APL_GRP_UPGRADE
				self.hideAPLGrpModeSelect()
				self.setAPLGrpMode()
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				self.hideAPLGrpModeSelect()
				return 1
			if (FuncName == "AutoInsertQueueSelect"):
				if (CvEventInterface.getEventManager().bShift):
					self.addAutoInsertQueue(inputClass.getData1(), False)
				else:
					self.addAutoInsertQueue(inputClass.getData1(), True)
				return 1
			if (FuncName == "AutoInsertQueueList"):
				self.delAutoInsertQueue(inputClass.getData())
				return 1
			if (FuncName == "AutoInsertProductionQueue"):
				self.AutoInsertProductionQueuePosition = inputClass.getData()
				return 1
		return 0

	def update(self, fDelta):
		return

	# handles the diaplay of the units info pane
	def showButtonDescInfoPane(self, buttonName):
		self.displayInfoPane(u"<font=2>" + localText.getText("TXT_KEY_" + buttonName, ()) + u"</font=2>")

	def hideAutoInsertQueuePanel(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screen.hide("AutoInsertQueueBackground")
		screen.hide("AutoInsertProductionQueue")
		screen.hide("AutoInsertQueueList")
		screen.hide("AutoInsertQueueSelect")
		screen.hide("AutoInsertPQUp")
		screen.hide("AutoInsertPQDown")
		screen.hide("AutoInsertPQDelete")

	def AutoInsertQueuePanel(self):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		screen.hide("AutoInsertQueueBackground")
		screen.hide("AutoInsertProductionQueue")
		screen.hide("AutoInsertQueueList")
		screen.hide("AutoInsertQueueSelect")
		screen.hide("AutoInsertPQUp")
		screen.hide("AutoInsertPQDown")
		screen.hide("AutoInsertPQDelete")

		if (not screen.getCheckBoxState("AutoInsertQueueButton1")):
			return

		iX = iMultiListXR - 68
		iY = self.yResolution - 350

		screen.addPanel("AutoInsertQueueBackground", u"", u"", True, False, iX, iY, 494, 160, PanelStyles.PANEL_STYLE_MAIN)
		screen.show("AutoInsertQueueBackground")
		screen.addTableControlGFC("AutoInsertProductionQueue", 3, iX + 16, iY + 15, 180, 100, False, False, 20, 20, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle("AutoInsertProductionQueue", "Table_City_Style")
		screen.enableSelect("AutoInsertProductionQueue", True)
		screen.setButtonGFC("AutoInsertPQUp", "<font=1>Up</font>", "", iX + 19, iY + 120, 55, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("AutoInsertPQDown", "<font=1>Down</font>", "", iX + 76, iY + 120, 55, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("AutoInsertPQDelete", "<font=1>Delete</font>", "", iX + 134, iY + 120, 60, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setTableColumnHeader("AutoInsertProductionQueue", 0, u"", 130)
		screen.setTableColumnHeader("AutoInsertProductionQueue", 1, u"", 40)
		screen.setTableColumnHeader("AutoInsertProductionQueue", 2, u"", 10)
		screen.addTableControlGFC("AutoInsertQueueList", 1, iX + 201, iY + 15, 175, 130, False, False, 20, 20, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("AutoInsertQueueList", True)
		screen.addMultiListControlGFC("AutoInsertQueueSelect", "", iX + 381, iY + 15, 105, 130, 1, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.clearMultiList("AutoInsertQueueSelect")

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		CivInfo = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType())

		OrderQueue = dict()
		if (SdToolKitAdvanced.sdObjectExists("CGEAutoInsertQueue", pHeadSelectedCity)):
			OrderQueue = SdToolKitAdvanced.sdObjectGetVal("CGEAutoInsertQueue", pHeadSelectedCity, "InsertQueue")

			iCount = 0
			bDelete = False
			for (iBuilding, iTrigger, bTop) in OrderQueue.copy().values():
				if (pHeadSelectedCity.getNumBuilding(iTrigger) > 0 or pHeadSelectedCity.getNumBuilding(iBuilding) > 0):
					del OrderQueue[iBuilding]
					bDelete = True
					continue

				screen.appendTableRow("AutoInsertQueueList")
				if (bTop):
					szArrow = u"\u2191"
				else:
					szArrow = u"\u2193"
				screen.setTableText("AutoInsertQueueList", 0, iCount, u"<font=1>%s: %s%s</font>"%(gc.getBuildingInfo(iBuilding).getDescription(), gc.getBuildingInfo(iTrigger).getDescription(), szArrow), "", WidgetTypes.WIDGET_GENERAL, iBuilding, iTrigger, CvUtil.FONT_LEFT_JUSTIFY)
				iCount += 1

			if (bDelete):
				SdToolKitAdvanced.sdObjectSetVal("CGEAutoInsertQueue", pHeadSelectedCity, "InsertQueue", OrderQueue)

		sBuildingInQueue = set(OrderQueue.keys())
		for i in xrange(pHeadSelectedCity.getOrderQueueLength()):
			tOrder = pHeadSelectedCity.getOrderFromQueue(i)
			if (tOrder.eOrderType == OrderTypes.ORDER_CONSTRUCT):
				sBuildingInQueue.add(tOrder.iData1)
			screen.appendTableRow("AutoInsertProductionQueue")
			szLeftBuffer = ""
			szRightBuffer = ""
			if (tOrder.eOrderType == OrderTypes.ORDER_TRAIN):
				szLeftBuffer = gc.getUnitInfo(tOrder.iData1).getDescription()
				szRightBuffer = "(" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(tOrder.iData1, i)) + ")"

				if (tOrder.bSave):
					szLeftBuffer = u"*" + szLeftBuffer

			elif (tOrder.eOrderType == OrderTypes.ORDER_CONSTRUCT):
				szLeftBuffer = gc.getBuildingInfo(tOrder.iData1).getDescription()
				szRightBuffer = "(" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(tOrder.iData1, i)) + ")"

			elif (tOrder.eOrderType == OrderTypes.ORDER_CREATE):
				szLeftBuffer = gc.getProjectInfo(tOrder.iData1).getDescription()
				szRightBuffer = "(" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(tOrder.iData1, i)) + ")"

			elif (tOrder.eOrderType == OrderTypes.ORDER_MAINTAIN):
				szLeftBuffer = gc.getProcessInfo(tOrder.iData1).getDescription()

			screen.setTableText("AutoInsertProductionQueue", 0, i, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_GENERAL, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("AutoInsertProductionQueue", 1, i, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_GENERAL, i, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		screen.show("AutoInsertProductionQueue")
		if (self.AutoInsertProductionQueuePosition > -1):
			screen.selectRow("AutoInsertProductionQueue", self.AutoInsertProductionQueuePosition, True)

		iCount = 0
		for eLoopBuilding in self.autoInsertcandidates.keys():
			if (eLoopBuilding not in sBuildingInQueue):
				if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
					if (not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False)):
						screen.appendMultiListButton( "AutoInsertQueueSelect", gc.getBuildingInfo(eLoopBuilding).getButton(), 0, WidgetTypes.WIDGET_GENERAL, eLoopBuilding, -1, False )
						screen.show( "AutoInsertQueueSelect" )

						iCount = iCount + 1

	def addAutoInsertQueue(self, iBuilding, bTop):
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (not SdToolKitAdvanced.sdObjectExists("CGEAutoInsertQueue", pHeadSelectedCity)):
			SdToolKitAdvanced.sdObjectInit("CGEAutoInsertQueue", pHeadSelectedCity, {"InsertQueue": {}})

		bResult = SdToolKitAdvanced.sdObjectSetDictVal("CGEAutoInsertQueue", pHeadSelectedCity, "InsertQueue", iBuilding, (iBuilding, self.autoInsertcandidates[iBuilding], bTop))
		if (bResult):
			self.AutoInsertQueuePanel()

	def delAutoInsertQueue(self, iNum):
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (not SdToolKitAdvanced.sdObjectExists("CGEAutoInsertQueue", pHeadSelectedCity)):
			return

		OrderQueue = SdToolKitAdvanced.sdObjectGetVal("CGEAutoInsertQueue", pHeadSelectedCity, "InsertQueue")
		if (len(OrderQueue) < iNum):
			return

		for (iLoop, iBuilding) in enumerate(OrderQueue.copy().keys()):
			if (iLoop == iNum):
				del OrderQueue[iBuilding]
				break

		bResult = SdToolKitAdvanced.sdObjectSetVal("CGEAutoInsertQueue", pHeadSelectedCity, "InsertQueue", OrderQueue)
		if (bResult):
			self.AutoInsertQueuePanel()

	def AutoInsertPQUp(self):
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		iIndex = self.AutoInsertProductionQueuePosition

		if (iIndex < 1 or iIndex >= pHeadSelectedCity.getOrderQueueLength()):
			return

		OrderList = []
		for i in xrange(pHeadSelectedCity.getOrderQueueLength()):
			LoopOrder = pHeadSelectedCity.getOrderFromQueue(i)
			OrderList.append((LoopOrder.eOrderType, LoopOrder.iData1, LoopOrder.iData2, LoopOrder.bSave))
		OrderList[iIndex], OrderList[iIndex -1] = OrderList[iIndex -1], OrderList[iIndex]

		pHeadSelectedCity.clearOrderQueue()
		pushProductionOrder = gc.getGame().cityPushOrder
		for LoopOrder in OrderList:
			#pHeadSelectedCity.pushOrder(LoopOrder.eOrderType, LoopOrder.iData1, LoopOrder.iData2, LoopOrder.bSave, False, True, False)
			#CyInterface().addImmediateMessage("AIPQ Up: %s, %s, %s"%(LoopOrder[0], LoopOrder[1], LoopOrder[3]),"")
			pushProductionOrder(pHeadSelectedCity, LoopOrder[0], LoopOrder[1], LoopOrder[3], True, False)
		self.AutoInsertProductionQueuePosition -= 1
		self.AutoInsertQueuePanel()

	def AutoInsertPQDown(self):
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		iIndex = self.AutoInsertProductionQueuePosition

		if (iIndex < 0 or iIndex >= pHeadSelectedCity.getOrderQueueLength() -1):
			return

		OrderList = []
		for i in xrange(pHeadSelectedCity.getOrderQueueLength()):
			LoopOrder = pHeadSelectedCity.getOrderFromQueue(i)
			OrderList.append((LoopOrder.eOrderType, LoopOrder.iData1, LoopOrder.iData2, LoopOrder.bSave))
		OrderList[iIndex], OrderList[iIndex +1] = OrderList[iIndex +1], OrderList[iIndex]

		pHeadSelectedCity.clearOrderQueue()
		pushProductionOrder = gc.getGame().cityPushOrder
		for LoopOrder in OrderList:
			pushProductionOrder(pHeadSelectedCity, LoopOrder[0], LoopOrder[1], LoopOrder[3], True, False)
		self.AutoInsertProductionQueuePosition += 1
		self.AutoInsertQueuePanel()

	def AutoInsertPQDelete(self):
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		iIndex = self.AutoInsertProductionQueuePosition

		if (iIndex < 0 or iIndex >= pHeadSelectedCity.getOrderQueueLength()):
			return

		pHeadSelectedCity.popOrder(iIndex, False, True)
		self.AutoInsertProductionQueuePosition = -1

	def setCGEOption(self, Section, Key, Value):
		#global variables
		global g_WinAMP
		global CFG_CIV_NAME_ON_SCOREBOARD
		global CFG_MASTER_NAME_ON_SCOREBOARD
		global CFG_RAWCOMMERCEDISPLAY
		global CFG_Combat_Experience_Counter
		global CFG_Unit_Statistics
		global g_bHideDeadCivilizations
		global g_bGreyOutDeadCivilizations
		global g_bShowDeadTag
		global CFG_Specialist_Stacker
		global SPECIALIST_STACK_WIDTH
		global g_bHighlightForcedSpecialists
		global g_bStackSuperSpecialists
		global MAX_SUPER_SPECIALIST_BUTTONS
		global SUPER_SPECIALIST_STACK_WIDTH
		global g_bDisplayUniqueSuperSpecialistsOnly
		global g_bDynamicSuperSpecialistsSpacing
		global g_bStackAngryCitizens
		global MAX_ANGRY_CITIZEN_BUTTONS
		global ANGRY_CITIZEN_STACK_WIDTH
		global g_bDynamicAngryCitizensSpacing
		global g_iSuperSpecialistCount
		global g_iAngryCitizensCount
		global g_bAlternateTimeText
		global g_iAlternatingTime
		global g_bShowTurns
		global g_bShowGameClock
		global g_bShowGameCompletedPercent
		global g_bShowGameCompletedTurns
		global g_bAlternateShowTurns
		global g_bAlternateShowGameClock
		global g_bAlternateShowGameCompletedPercent
		global g_bAlternateShowGameCompletedTurns
		global g_bShowEra
		global g_bShowReflectEraInTurnColor
		global g_eraTurnColorDictionary
		global CFG_Show_GameTurn_Bar
		global CFG_Show_GreatPerson_Bar
		global CFG_Show_TopCultureCities
		global g_BottomContIconSize

		if (Section == "Civ Name"):
			CFG_CIV_NAME_ON_SCOREBOARD = Value
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
		if (Section == "Master Name"):
			CFG_MASTER_NAME_ON_SCOREBOARD = Value
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
		elif (Section == "Combat Experience Counter"):
			CFG_Combat_Experience_Counter = Value
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)
		elif (Section == "Game Turn Bar"):
			CFG_Show_GameTurn_Bar = Value
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)
		elif (Section == "Great Person Bar"):
			CFG_Show_GreatPerson_Bar = Value
			CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)
		elif (Section == "Top Culture Cities"):
			iVC = gc.getInfoTypeForString("VICTORY_CULTURAL")
			if (gc.getGame().isVictoryValid(iVC)):
				victory = gc.getVictoryInfo(iVC)
				if (victory.getCityCulture() != CultureLevelTypes.NO_CULTURELEVEL and victory.getNumCultureCities() > 0):
					CFG_Show_TopCultureCities = Value
					CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)
				else:
					CFG_Show_TopCultureCities = False
		elif (Section == "Winamp GUI"):
			g_WinAMP = Value
		elif (Section == "Dead Civ Scoreboard Mod"):
			if (Key == "Hide Dead Civilizations"):
				g_bHideDeadCivilizations = Value
			elif (Key == "Grey Out Dead Civilizations"):
				g_bGreyOutDeadCivilizations = Value
			elif (Key == "Show Dead Tag"):
				g_bShowDeadTag = Value
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
		elif (Section == "Raw Commerce Display"):
			CFG_RAWCOMMERCEDISPLAY = Value
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			if (CFG_RAWCOMMERCEDISPLAY):
				screen.setPanelSize("TradeRouteListBackground", 10, 228, 238, 30)
				screen.setPanelSize("BuildingListBackground", 10, 358, 238, 30)
			else:
				screen.setPanelSize("TradeRouteListBackground", 10, 138, 238, 30)
				screen.setPanelSize("BuildingListBackground", 10, 268, 238, 30)
		elif (Section == "Specialist Stacker"):
			if (Key == "Enabled"):
				CFG_Specialist_Stacker = Value
			elif (Key == "Specialist Stack Width"):
				SPECIALIST_STACK_WIDTH = Value
			elif (Key == "Highlight Forced Specialists"):
				g_bHighlightForcedSpecialists = Value
			elif (Key == "Stack Super Specialists"):
				g_bStackSuperSpecialists = Value
			elif (Key == "Max Super Specialist Buttons"):
				MAX_SUPER_SPECIALIST_BUTTONS = Value
			elif (Key == "Super Specialist Stack Width"):
				SUPER_SPECIALIST_STACK_WIDTH = Value
			elif (Key == "Display Unique Super Specialists Only"):
				g_bDisplayUniqueSuperSpecialistsOnly = Value
			elif (Key == "Dynamic Super Specialists Spacing"):
				g_bDynamicSuperSpecialistsSpacing = Value
			elif (Key == "Stack Angry Citizens"):
				g_bStackAngryCitizens = Value
			elif (Key == "Max Angry Citizen Buttons"):
				MAX_ANGRY_CITIZEN_BUTTONS = Value
			elif (Key == ""):
				ANGRY_CITIZEN_STACK_WIDTH = Value
			elif (Key == "Dynamic Angry Citizen Spacing"):
				g_bDynamicAngryCitizensSpacing = Value
			elif (Key == "Angry Citizen Stack Width"):
				g_iAngryCitizensCount = Value
		elif (Section == "Not Just Another Game Clock Mod"):
			if (Key == "Alternate Time Text"):
				g_bAlternateTimeText = Value
			elif (Key == "Alternating Time"):
				g_iAlternatingTime = Value
			elif (Key == "Show Turns"):
				g_bShowTurns = Value
			elif (Key == "Show Game Clock"):
				g_bShowGameClock = Value
			elif (Key == "Show Game Completed Percent"):
				g_bShowGameCompletedPercent = Value
			elif (Key == "Show Game Completed Turns"):
				g_bShowGameCompletedTurns =Value
			elif (Key == "Alternate Show Turns"):
				g_bAlternateShowTurns = Value
			elif (Key == "Alternate Show Game Clock"):
				g_bAlternateShowGameClock = Value
			elif (Key == "Alternate Show Game Completed Percent"):
				g_bAlternateShowGameCompletedPercent = Value
			elif (Key == "Alternate Show Game Completed Turns"):
				g_bAlternateShowGameCompletedTurns = Value
			elif (Key == "Show Era"):
				g_bShowEra = Value
				CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)
			elif (Key == "Show Reflect Era In Turn Color"):
				g_bShowReflectEraInTurnColor = Value
			elif (Key.startswith("ERA_")):
				g_eraTurnColorDictionary[Key] = gc.getInfoTypeForString(Value)
		elif (Section == "Unit Statistics Mod"):
			CFG_Unit_Statistics = Value
		elif (Section == "Bottom Container Icon"):
			if (Value):
				g_BottomContIconSize = 34
			else:
				g_BottomContIconSize = 48
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, True)

	def forward(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_NEXTCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_NEXTUNIT)
		
	def back(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_PREVCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_PREVUNIT)
