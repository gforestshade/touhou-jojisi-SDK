## Sid Meier's Civilization 4'
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import sys

##### <written by F> #####
import SpellInfo
import TohoUnitList
import Functions
##### </written by F> #####
import codecs

# globals
gc = CyGlobalContext()
##### <written by F> #####
#デバッグ用print文
#東方叙事詩・統合MOD追記
#原因はよくわからないエラーへの対処。記述部分を流用先のFfH Age of Iceと同一にする
#デバッグ用のため必要になったらコメントアウトを外す
logInited = False
def initLog():
	global logInited
	#helpFile=file("debuglog.txt", "w")
	helpFile=codecs.open('debuglog.txt', 'w', 'shift_jis')
#	sys.stdout=helpFile
	sys.stdout.write("loaded\n")
#	sys.stdout.flush()
	logInited = True
def doprint(str):
	#cd sys.stderr.write(str)
	if not logInited:
		initLog()
	sys.stdout.write(str)
	sys.stdout.write("\n")
#	sys.stdout.flush()
##### </written by F> #####

class CvGameUtils:
	"Miscellaneous game functions"
	def __init__(self): 
		pass
	
	def isVictoryTest(self):
		if ( gc.getGame().getElapsedGameTurns() > 10 ):
			return True
		else:
			return False

	def isVictory(self, argsList):
		eVictory = argsList[0]
		return True

	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]
		return True

	def getExtraCost(self, argsList):
		ePlayer = argsList[0]
		#統合MOD追記
		#紅魔館のユニットコスト減少処理
		pPlayer = gc.getPlayer(ePlayer)
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_KOUMAKAN")) == 1:
			return  -pPlayer.calculateUnitCost() /2
		#統合MOD追記ここまで
		
		#統合MOD追記ここまで
		return 0

	def createBarbarianCities(self):
		return False
		
	def createBarbarianUnits(self):
		return False
		
	def skipResearchPopup(self,argsList):
		ePlayer = argsList[0]
		return False
		
	def showTechChooserButton(self,argsList):
		ePlayer = argsList[0]
		return True

	def getFirstRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		return TechTypes.NO_TECH

	def getSecondRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]
		return TechTypes.NO_TECH
	
	def canRazeCity(self,argsList):
		iRazingPlayer, pCity = argsList
		return True
	
	def canDeclareWar(self,argsList):
		iAttackingTeam, iDefendingTeam = argsList
		#統合MOD追記
		#BC1000年を超えるまでは宣戦布告不可に
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_PEACE_OF_BC1000')):
			iGameTarn = gc.getGame().getGameTurn()
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
				if iGameTarn < 250:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
				if iGameTarn < 120:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_NORMAL'):
				if iGameTarn < 75:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
				if iGameTarn < 50:
					return False
			if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
				if iGameTarn < 43:
					return False
		#統合MOD追記ここまで
		
		return True
	
	def skipProductionPopup(self,argsList):
		pCity = argsList[0]
		return False
		
	def showExamineCityButton(self,argsList):
		pCity = argsList[0]
		return True

	def getRecommendedUnit(self,argsList):
		pCity = argsList[0]
		return UnitTypes.NO_UNIT

	def getRecommendedBuilding(self,argsList):
		pCity = argsList[0]
		return BuildingTypes.NO_BUILDING

	def updateColoredPlots(self):
		return False

	def isActionRecommended(self,argsList):
		pUnit = argsList[0]
		iAction = argsList[1]
		return False

	def unitCannotMoveInto(self,argsList):
		ePlayer = argsList[0]		
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]
		return False

	def cannotHandleAction(self,argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]
		
		##### <written by F> #####
		#全てのアクションがここにきているっぽい？
		#スペルアクションのみを捕まえて実行させる
		
#		doprint('cannotHandleAction In, ActionNumber:%i' %iAction)
		spell = SpellInfo.getSpellFromAction(iAction) #get the spell back from the number
#		doprint("action: %s %i %i %i"  %(gc.getActionInfo(iAction).getButton(),iAction,bTestVisible,CvMainInterface.g_checkingActive))
		if(spell == None):
			return False
		#doprint('This Action is spell, ActionNumber:%i' %iAction)
		#return bTestVisible
#		doprint('1')
		if(bTestVisible):
		#	doprint("spell is not visible")
			return spell.isInvisible()
#		doprint('2')
		#if(CvMainInterface.g_checkingActive):
		#	doprint('g_checkingActive is False')
		#	return spell.isDisabled()
#		doprint('3')
		doprint('Spell cast')
		spell.cast()
		doprint('cannotHandleAction In, ActionNumber:%i' %iAction)
		#for i in range(633):
		#	ActionInfo = gc.getActionInfo(i)
			#pActionInfo = ActionInfo(0)
			#doprint("button: %s" %(pActionInfo.getButton()))
			#doprint("for %i: %s" % (i,str(gc.getActionInfo(i))))
#		return True
		return False
		
		##### </written by F> #####
		
		return False

	def canBuild(self,argsList):
		iX, iY, iBuild, iPlayer = argsList
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()
		pTeam = gc.getTeam(pPlayer.getTeam())

		#統合MOD追記部分

		#AIが地形改善を考慮する際、本来建設出来ない他国UIを考慮に入れているかもしれない
		#なのでシステム上、どう頑張っても自国のUI以外は建設出来ないようにする
		#追記：コード変更。やってる事自体はほぼ同じだが、それぞれのUIの元になる地形改善もNGに。
		#効果があるかどうかは知らん
		
		#（多分書かなくても大丈夫だとは思うが、念の為）テラフォーミング系ダミービルドは全てpython側でNGに
		if gc.getInfoTypeForString('BUILD_TERRAFORM_PLAIN') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TERRAFORM_FLOOD'):
			return 0
		
		#紅魔館の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ENGLAND'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_EIENTEI_FOREST_PRESERVE'):
				return 0
			if gc.getInfoTypeForString('BUILD_HAKUGYOKUROU_QUARRY') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_FARM'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WINERY'):
				return 0

		#白玉楼の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_KOUMAKAN_FARM'):
				return 0
			if gc.getInfoTypeForString('BUILD_NINGENNOSATO_COTTAGE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_QUARRY'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WINDMILL'):
				return 0

		#氷精連合の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_HAKUREIJINJA_PLANTATION'):
				return 0
			if gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FORT') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_LUMBERMILL'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_PASTURE'):
				return 0

		#永遠亭の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_EGYPT'):
			if gc.getInfoTypeForString('BUILD_KOUMAKAN_WINERY') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_KISHINJOU_WINERY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_PLANTATION'):
				return 0

		#妖怪の山の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_HYOUSEIRENGOU_PASTURE'):
				return 0
			if gc.getInfoTypeForString('BUILD_CHIREIDEN_WORKSHOP') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_FORT'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_FARM'):
				return 0

		#博麗神社の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_NINGENNOSATO_WATERMILL'):
				return 0
			if gc.getInfoTypeForString('BUILD_HYOUSEIRENGOU_LUMBERMILL') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_FOREST_PRESERVE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_PLANTATION'):
				return 0

		#地霊殿の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FARM'):
				return 0
			if gc.getInfoTypeForString('BUILD_SEIRENSEN_MINE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WELL'):
				return 0

		#星蓮船の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_RUSSIA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_CHIREIDEN_WELL'):
				return 0
			if gc.getInfoTypeForString('BUILD_SHINREIBYOU_COTTAGE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_MINE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_CAMP'):
				return 0

		#神霊廟の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_SEIRENSEN_CAMP'):
				return 0
			if gc.getInfoTypeForString('BUILD_KISHINJOU_WORKSHOP') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
				return 0
			

		#輝針城の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALI'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_SHINREIBYOU_ROAD'):
				return 0
			if gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_COTTAGE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WINERY'):
				return 0
				
		#月の都の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMERICA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_KISHINJOU_WINERY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_QUARRY'):
				return 0

		#人間の里の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_HAKUGYOKUROU_WINDMILL'):
				return 0
			if gc.getInfoTypeForString('BUILD_HAKUREIJINJA_FOREST_PRESERVE') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0
			if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_RELIGION')) == gc.getInfoTypeForString('CIVIC_PURE_SAKE')) == True:
				iPureSakeValue = self.CheckPureSake(pPlayer, argsList)
				return iPureSakeValue
			if iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WATERMILL'):
				return 0
			
		#蛮族の場合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_BARBARIAN'):
			if gc.getInfoTypeForString('BUILD_EIENTEI_PLANTATION') <= iBuild and iBuild <= gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_QUARRY'):
				return 0

		return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

	def CheckPureSake(self, pPlayer, argsList):
		iX, iY, iBuild, iPlayer = argsList
		pPlot = gc.getMap().plot(iX,iY)
		if pPlayer.getTeam() == pPlot.getTeam():
			#以下全てUIの場合含む
			if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
				#小屋
				if iBuild == gc.getInfoTypeForString('BUILD_NINGENNOSATO_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_NINGENNOSATO_TOWN')):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_SHINREIBYOU_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_SHINREIBYOU_TOWN')):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_TUKI_NO_MIYAKO_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_TUKI_NO_MIYAKO_TOWN')):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_COTTAGE') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_TOWN')):
						return 1
				#農場
				if iBuild == gc.getInfoTypeForString('BUILD_KOUMAKAN_FARM'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_3')):
						if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_4'):
							return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YOUKAINOYAMA_FARM'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FARM'):
						return 1
				#工房
				if iBuild == gc.getInfoTypeForString('BUILD_CHIREIDEN_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_CHIREIDEN_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KISHINJOU_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_WORKSHOP'):
						return 1
			if pPlot.isCity():
				#農場
				if iBuild == gc.getInfoTypeForString('BUILD_KOUMAKAN_FARM'):
					if not (gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM') <= pPlot.getImprovementType() and pPlot.getImprovementType() <= gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_3')):
						if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_4'):
							return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_YOUKAINOYAMA_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YOUKAINOYAMA_FARM'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_FARM'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FARM'):
						return 1
				#工房
				if iBuild == gc.getInfoTypeForString('BUILD_CHIREIDEN_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_CHIREIDEN_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('IMPROVEMENT_KISHINJOU_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KISHINJOU_WORKSHOP'):
						return 1
				elif iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
					if not pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_WORKSHOP'):
						return 1
		
		return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can
		
		#統合MOD追記部分

	def cannotFoundCity(self,argsList):
		iPlayer, iPlotX, iPlotY = argsList
		return False

	def cannotSelectionListMove(self,argsList):
		pPlot = argsList[0]
		bAlt = argsList[1]
		bShift = argsList[2]
		bCtrl = argsList[3]
		return False

	def cannotSelectionListGameNetMessage(self,argsList):
		eMessage = argsList[0]
		iData2 = argsList[1]
		iData3 = argsList[2]
		iData4 = argsList[3]
		iFlags = argsList[4]
		bAlt = argsList[5]
		bShift = argsList[6]
		return False

	def cannotDoControl(self,argsList):
		eControl = argsList[0]
		return False

	def canResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def cannotResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		
		##### <written by F> #####
		#AIが本来研究してはいけないものを研究している気がする
		#文明ごとに、それぞれの文明以外の東方テクは研究できないようにする
		
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		
		#紅魔館のとき
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ENGLAND'):
			if gc.getInfoTypeForString('TECH_HAKUGYOKUROU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#白玉楼
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_AKAIKIRI'):
				return True
			if gc.getInfoTypeForString('TECH_HYOUSEIRENGOU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#氷精連合
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_BORDER_OF_LIFE'):
				return True
			if gc.getInfoTypeForString('TECH_EIENTEI') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#永遠亭
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_EGYPT'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_SIZENNOKYOUI'):
				return True
			if gc.getInfoTypeForString('TECH_YOUKAINOYAMA') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#妖怪の山
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_TUKIKARANOSISHA'):
				return True
			if gc.getInfoTypeForString('TECH_HAKUREIJINJA') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
				
		#白麗神社
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_MORIYANOOUKOKU'):
				return True
			if gc.getInfoTypeForString('TECH_CHIREIDEN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#地霊殿
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_HAKUREIDAIKEKKAI'):
				return True
			if gc.getInfoTypeForString('TECH_SEIRENSEN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#星蓮船
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_RUSSIA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_CHITEINOTAIYOSHINKO'):
				return True
			if gc.getInfoTypeForString('TECH_SHINREIBYOU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#神霊廟
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_TEACHING_OF_MEIREN'):
				return True
			if gc.getInfoTypeForString('TECH_KISHINJOU') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#輝針城
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALI'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_HOSIHURU_SHINREIBYOU'):
				return True
			if gc.getInfoTypeForString('TECH_TUKI_NO_MIYAKO') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#月の都
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMERICA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_MUGENNOTIKARA'):
				return True
			if gc.getInfoTypeForString('TECH_KEINENOIRAI') <= eTech and eTech <= gc.getInfoTypeForString('TECH_KEINENOIRAI'):
				return True
		
		#人間の里
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
			if gc.getInfoTypeForString('TECH_KOUMAKAN') <= eTech and eTech <= gc.getInfoTypeForString('TECH_TUKI_NO_MIYAKO'):
				return True
		
		##### </written by F> #####
		
		return False

	def canDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		
		#統合MOD追記部分
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		pTeam = gc.getTeam(pPlayer.getTeam())
		#指導者わかさぎ姫の場合、光学取得で深海の旧支配者採用可能
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_WAKASAGIHIMELIST')):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_OPTICS')):
				if eCivic == gc.getInfoTypeForString('CIVIC_FAITH_CTHULHU'):
					return True
		
		#集権志向の場合、中世以降に入ると無条件で官僚制採用可能
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CENTRALIZATION')):
			if pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_ANCIENT'):
				if pPlayer.getCurrentEra() != gc.getInfoTypeForString('ERA_CLASSICAL'):
					if eCivic == gc.getInfoTypeForString('CIVIC_BUREAUCRACY'):
						return True
		
		#統合MOD追記部分ここまで
		
		return False

	def cannotDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		
		#統合MOD追記部分
		
		#ピラ処理
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		eTeam = gc.getTeam(pPlayer.getTeam())
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_PYRAMID")) == 1:
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_CHINA'):
				return False

			elif eCivic == gc.getInfoTypeForString('CIVIC_ZYUUSHICHIZYO_KENPOU'):
				return True
		
		#ゴールデン巻き○ソ処理
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_SHWEDAGON_PAYA")) == 1:
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMERICA'):
				return False
			elif eCivic == gc.getInfoTypeForString('CIVIC_PURE_SAKE'):
				return True
		
		#統合MOD追記部分ここまで
		
		return False
		
	def canTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		
		#統合MOD追記部分
		
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eUnitClass = gc.getUnitInfo(eUnit).getUnitClassType()
		#指導者影狼の場合、ニホンオオカミ作成可能処理
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_KAGEROULIST')):
			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_NIHONOOKAMI'):
				return True
		
		#地霊殿建設後、第三の眼作成可能処理
		if pTeam.getProjectCount(gc.getInfoTypeForString("PROJECT_CHIREIDEN")) == 1:
			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_3RDEYE'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_3RDEYE')) < 1:
					return True
		
		#諜報無しオプションの場合、星文明は労働者を作成できるように
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_ESPIONAGE')):
			iCiv = pPlayer.getCivilizationType()
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_RUSSIA'):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_WORKER'):
					return True
		
		#輝針城・雷鼓の呪法-戦の処理
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_A")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_STEEL')):
					if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_KOREAN_HWACHA'):
						return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
				if not (pTeam.isHasTech(gc.getInfoTypeForString('TECH_MILITARY_TRADITION')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUNPOWDER'))):
					if pCity.hasBonus(gc.getInfoTypeForString('BONUS_HORSE')) and pCity.hasBonus(gc.getInfoTypeForString('BONUS_IRON')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_BYZANTINE_CATAPHRACT'):
							return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_RIFLING')):
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_ASSEMBLY_LINE')):
					if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_ENGLISH_REDCOAT'):
						return True
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MILITARY_TRADITION')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
					if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_ADVANCED_FLIGHT')):
						if pCity.hasBonus(gc.getInfoTypeForString('BONUS_HORSE')):
							if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_RUSSIA_COSSACK'):
								return True
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ROBOTICS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
					if pCity.hasBonus(gc.getInfoTypeForString('BONUS_URANIUM')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KISHINJOU_MECH'):
							return True
		
		#間欠泉地下センターを建設した都市では特殊核生産可能に
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CHIKACENTER")):
			if gc.getGame().isNukesValid() == True:
				if pCity.hasBonus(gc.getInfoTypeForString('BONUS_URANIUM')):
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_UTSUHO_2'):
							return True
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CHITEINOTAIYOSHINKO')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_TACTICAL_UTSUHO_2'):
							return True
		
		return False

	def cannotTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		
		#統合MOD追記部分
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eUnitClass = gc.getUnitInfo(eUnit).getUnitClassType()
		
		#輝針城・雷鼓の呪法-戦の処理
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_A")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_CATAPULT'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KNIGHT'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_RIFLING')):
				if eUnitClass == gc.getInfoTypeForString('UNITCLASS_RIFLEMAN'):
					return True
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MILITARY_TRADITION')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
					if eUnitClass == gc.getInfoTypeForString('UNITCLASS_CAVALRY'):
						return True
		
		#「魔力の回収期」取得で小人調査兵団を作成不可能に
		#マルチ補正オプション時も作成不可に
		if pTeam.isHasTech(gc.getInfoTypeForString('TECH_KAISYUUKI')) or gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_KOBITO_TYOUSAHEIDAN'):
				return True
		
		#間欠泉地下センターを建設した都市では通常核をリストから除くように
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CHIKACENTER")):
			if gc.getGame().isNukesValid() == True:
				if pCity.hasBonus(gc.getInfoTypeForString('BONUS_URANIUM')):
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_ICBM'):
							return True
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_CHITEINOTAIYOSHINKO')):
						if eUnitClass == gc.getInfoTypeForString('UNITCLASS_TACTICAL_NUKE'):
							return True
		
		#複数所属指導者は自身の東方ユニットの優先生産権を持つ
		for i in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(i)
			iCiv = pPlayer.getCivilizationType()
		
		#萃香の処理
		#「博麗神社の萃香」が同じ星にいる場合、妖怪の山では萃香生産禁止
			if eUnit == gc.getInfoTypeForString('UNIT_SUIKA0_YOUKAI'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUIKA')) == True:
					return True
		#「妖怪の山の萃香」が同じ星にいる場合、博麗神社では萃香生産禁止
			if eUnit == gc.getInfoTypeForString('UNIT_SUIKA0'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SUIKA')) == True:
					return True
		
		#紫の処理
		#「白玉楼の紫」が同じ星にいる場合、博麗神社では紫生産禁止
			if eUnit == gc.getInfoTypeForString('UNIT_YUKARI0_HAKUREI'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUKARI')) == True:
					return True
		#「博麗神社の紫」が同じ星にいる場合、白玉楼では紫生産禁止
			if eUnit == gc.getInfoTypeForString('UNIT_YUKARI0'):
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN')) == True and (pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_YUKARI')) == True:
					return True
		
		return False

	def canConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		
		#統合MOD追記部分
		
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
		
		# 作成中の建造物はグレーアウト
		if not bTestVisible and not bContinue:
			if pCity.getFirstBuildingOrder(eBuilding) != -1:
				return False

		#輝針城・雷鼓の呪法-内の処理
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_B")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):
				if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_GROCER')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_PERSIAN_APOTHECARY'):
							return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ENGINEERING')):
				obsoleteTech = gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_KISHINJOU_SPANISH_CITADEL")).getObsoleteTech()
				if ( pTeam.isHasTech(obsoleteTech) == false or obsoleteTech == -1 ):
					if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_WALL_ISSUN')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_CASTLE')):
							if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL')):
								if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_SPANISH_CITADEL'):
									return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ECONOMICS')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_HARBOR')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_CUSTOM_HOUSE')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA')):
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_PORTUGAL_FEITORIA'):
								return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ASSEMBLY_LINE')):
				if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_FACTORY')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_GERMAN_ASSEMBLY_PLANT'):
							return True
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_COAL_PLANT')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT')):
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_JAPANESE_SHALE_PLANT'):
								return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_REFRIGERATION')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_SUPERMARKET')):
						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL')):
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_AMERICAN_MALL'):
								return True
			#ちゃんと水力/原発を作成可能に
			#ついでに工業団地も
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_INDUSTRIALISM')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_INDUSTRIAL_PARK')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_INDUSTRIAL_PARK'):
							return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_PLASTICS')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_HYDRO_PLANT')):
						pPlot = pCity.plot()
						if pPlot.isRiver ():
							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_HYDRO_PLANT'):
								return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_FISSION')):
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_NUCLEAR_PLANT')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_NUCLEAR_PLANT'):
							return True
			
		
		#弁々はモニュメントの代わりにステラ作成可能
# 		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_BENBENLIST")):
# 			obsoleteTech = gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_KISHINJOU_ETHIOPIAN_STELE")).getObsoleteTech()
# 			if ( pTeam.isHasTech(obsoleteTech) == false or obsoleteTech == -1 ):
# 				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM')):
# 					if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_OBELISK')):
# 						if not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_ETHIOPIAN_STELE')):
# 							if eBuilding == gc.getInfoTypeForString('BUILDING_KISHINJOU_ETHIOPIAN_STELE'):
# # #							if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_KISHINJOU_ETHIOPIAN_STELE'):
# 								return True
		
		#社会制度変更決議無しオプション時は特殊国連建設可能に
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_CIVIC_CHANGE_RESOLUTION')):
			if gc.getGame().isVictoryValid(gc.getInfoTypeForString('VICTORY_DIPLOMATIC')) == True:
				if CyGame().getBuildingClassCreatedCount(gc.getInfoTypeForString("BUILDINGCLASS_UNITED_NATIONS_OPTION")) == 0:
					if pTeam.isHasTech(gc.getInfoTypeForString('TECH_MASS_MEDIA')):
						if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_UNITED_NATIONS_OPTION'):
							return True
		
		return False

	def cannotConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		
		#統合MOD追記部分
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
	
		#蛮族は固有建造物を建設できないように
		#XMLでも出来なくはないが、多分こっちで指定する方が簡単だ
		
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BARBARIAN'):
			if gc.getInfoTypeForString('BUILDING_MONBAN') <= eBuilding and eBuilding <= gc.getInfoTypeForString('BUILDING_MAGIC_STORM'):
				return True
	
		#輝針城・雷鼓の呪法-内の処理
		#「戦」を建設出来なくなる処理も同時に
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_B")) == 1:
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_GROCER'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ENGINEERING')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CASTLE'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ECONOMICS')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CUSTOM_HOUSE'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ASSEMBLY_LINE')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_FACTORY'):
					return True
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_COAL_PLANT'):
					return True
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_REFRIGERATION')):
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_SUPERMARKET'):
					return True
					
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_A'):
				return True
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_B'):
				return True
		
		#輝針城・雷鼓の呪法-内を戦争等で失ってしまった場合などの処理
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_GROCER'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CASTLE'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_CUSTOM_HOUSE'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_FACTORY'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_COAL_PLANT'):
				return True
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_SUPERMARKET'):
				return True
		
		#輝針城・雷鼓の呪法-戦の処理
		if pPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_A")) == 1:
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_B'):
				return True
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_A'):
				return True
		
		#弁々はノーマルモニュ作成不可
		# if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_BENBENLIST")):
		# 	if eBuilding == gc.getInfoTypeForString('BUILDING_OBELISK'):
		# 		return True
		
		#陰陽寮（×）が都市に存在している場合、陰陽寮（○）は作成不可
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_ONMYOURYOU2')):
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_ONMYOURYOU1'):
				return True
		
		#道教を採用していない場合、陰陽寮建設不可
		if (pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_FAITH')) == gc.getInfoTypeForString('CIVIC_FAITH_TAOISM')) == False:
			if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_ONMYOURYOU1'):
				return True
		
		#社会制度変更決議無しオプション時は通常国連建設不可に
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_CIVIC_CHANGE_RESOLUTION')):
			if gc.getGame().isVictoryValid(gc.getInfoTypeForString('VICTORY_DIPLOMATIC')) == True:
				if eBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_UNITED_NATIONS'):
					return True
		
		return False

	def canCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def cannotCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		
		#統合MOD追記部分
		#永久同盟オプション時、プロジェクト地霊殿は作成不可に
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_PERMANENT_ALLIANCES')):
			if eProject == gc.getInfoTypeForString('PROJECT_CHIREIDEN'):
				return True
		
		#マンハッタン禁止オプション時、マンハッタン計画作成不可に
		
		if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_NO_MANHATTAN')):
			if eProject == gc.getInfoTypeForString('PROJECT_MANHATTAN_PROJECT'):
				return True
		
		return False

	def canMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		
		#「片翼の白鷲」がある都市は諜報ポイント生産が可能
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KATAYOKU')):
			if eProcess == gc.getInfoTypeForString('PROCESS_KATAYOKU_SPY'):
				return True
		
		return False

	def cannotMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def AI_chooseTech(self,argsList):
		ePlayer = argsList[0]
		bFree = argsList[1]
		
		##### <written by F> #####
		#東方テクを優先取得させる
		
		if bFree == False:
			pTeam = gc.getTeam(gc.getPlayer(ePlayer).getTeam())
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_METAL_CASTING')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')) == False:
				return gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GUNPOWDER')) and pTeam.isHasTech(gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')) == False:
				return gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')
		
		##### </written by F> #####
		
		return TechTypes.NO_TECH

	def AI_chooseProduction(self,argsList):
		pCity = argsList[0]
		
		##### <written by F> #####
		#どうもＡＩはユニット０を作りたがらないので、強制的に作らせる
		
		#doprint("AI_TEst")
		List = []
		for sTohoUnit in TohoUnitList.TohoUnitList0:
			#doprint("can AI Create %s" %sTohoUnit)
			if pCity.canTrain(gc.getInfoTypeForString(sTohoUnit),false,false):
				List.append(sTohoUnit)
		if len(List) > 0:
			iNum = gc.getGame().getSorenRandNum(len(List), "choose toho unit")
			iUnit = CvUtil.findInfoTypeNum(gc.getUnitInfo,gc.getNumUnitInfos(),List[iNum])
			pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnit, -1, False, False, False, True)
			#doprint("AI_Created:%s" %sTohoUnit)
			
			return True
		
		##### </written by F> #####
		
		return False

	def AI_unitUpdate(self,argsList):
		pUnit = argsList[0]
		return False

	def AI_doWar(self,argsList):
		eTeam = argsList[0]
		return False

	def AI_doDiplo(self,argsList):
		ePlayer = argsList[0]
		return False

	def calculateScore(self,argsList):
		ePlayer = argsList[0]
		bFinal = argsList[1]
		bVictory = argsList[2]
		
		iPopulationScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getPopScore(), gc.getGame().getInitPopulation(), gc.getGame().getMaxPopulation(), gc.getDefineINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
		iLandScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getLandScore(), gc.getGame().getInitLand(), gc.getGame().getMaxLand(), gc.getDefineINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
		iTechScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getTechScore(), gc.getGame().getInitTech(), gc.getGame().getMaxTech(), gc.getDefineINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
		iWondersScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getWondersScore(), gc.getGame().getInitWonders(), gc.getGame().getMaxWonders(), gc.getDefineINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)
		return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)

	def doHolyCity(self):
		return False

	def doHolyCityTech(self,argsList):
		eTeam = argsList[0]
		ePlayer = argsList[1]
		eTech = argsList[2]
		bFirst = argsList[3]
		return False

	def doGold(self,argsList):
		ePlayer = argsList[0]
		return False

	def doResearch(self,argsList):
		ePlayer = argsList[0]
		return False

	def doGoody(self,argsList):
		ePlayer = argsList[0]
		pPlot = argsList[1]
		pUnit = argsList[2]
		return False

	def doGrowth(self,argsList):
		pCity = argsList[0]
		return False

	def doProduction(self,argsList):
		pCity = argsList[0]
		return False

	def doCulture(self,argsList):
		pCity = argsList[0]
		return False

	def doPlotCulture(self,argsList):
		pCity = argsList[0]
		bUpdate = argsList[1]
		ePlayer = argsList[2]
		iCultureRate = argsList[3]
		return False

	def doReligion(self,argsList):
		pCity = argsList[0]
		return False

	def cannotSpreadReligion(self,argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList[0]
		return False

	def doGreatPeople(self,argsList):
		pCity = argsList[0]
		return False

	def doMeltdown(self,argsList):
		pCity = argsList[0]
		return False
	
	def doReviveActivePlayer(self,argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]
		return False
	
	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot = argsList[0]
		pUnit = argsList[1]
		
		iPillageGold = 0
		iPillageGold = CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2")

		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100
		
		return iPillageGold
	
	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"
		
		pOldCity = argsList[0]
		
		iCaptureGold = 0
		
		iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")

		if (gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0):
			iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")
		
		return iCaptureGold
	
	def citiesDestroyFeatures(self,argsList):
		iX, iY= argsList
		return True
		
	def canFoundCitiesOnWater(self,argsList):
		iX, iY= argsList
		return False
		
	def doCombat(self,argsList):
		pSelectionGroup, pDestPlot = argsList
		return False

	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1 #return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system
		
		return iConscriptUnitType

	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1 # Any value besides -1 will be used
		
		return iFoundValue
		
	def canPickPlot(self, argsList):
		pPlot = argsList[0]
		return true
		
	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		pPlayer = gc.getPlayer(iPlayer)
		
		#統合MOD追記部分
		#純狐の志向で白兵コスト-15%
		iMod = 100
		iUnitCombatType = gc.getUnitInfo(iUnit).getUnitCombatType()
		
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_JUNKOLIST')):
			if iUnitCombatType == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
				iMod -= 15
		
		return iMod
		
		iCostMod = -1 # Any value > 0 will be used
		
		return iCostMod

	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCityID)
		
		#統合MOD追記部分
		#雷鼓の呪法コスト増加処理
		iMod = 100
		iBuildingClass = gc.getBuildingInfo(iBuilding).getBuildingClassType()
		
		if iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_A'):
			if pPlayer.getMysteryiumFlag() >= 1:
				iMod += 50*(pPlayer.getMysteryiumFlag())
		
		if iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_RAIKO_MAGIC_B'):
			if pPlayer.getMysteryiumFlag() >= 1:
				iMod += 50*(pPlayer.getMysteryiumFlag())
		
		#集権志向持ちは首都の一般建造物＆国家遺産コスト25%割引
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_CENTRALIZATION')):
			eBuildingInfo = gc.getBuildingInfo(iBuilding)
			if not isWorldWonderClass(eBuildingInfo.getBuildingClassType()):
				if pCity.isCapital():
					iMod -= 25
		
		#統合MOD追記部分ここまで
		return iMod
		
		iCostMod = -1 # Any value > 0 will be used
		
		return iCostMod
		
	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList
		
		bCanUpgradeAnywhere = 0
		
		return bCanUpgradeAnywhere
		
	def getWidgetHelp(self, argsList):
		eWidgetType, iData1, iData2, bOption = argsList
## Platypedia ##
		if eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 6781:
				if iData2 == -2:
					return CyTranslator().getText("TXT_KEY_PEDIA_ALL_GROUPS", ())
				elif iData2 == -1:
					return CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ())
				else:
					return gc.getUnitCombatInfo(iData2).getDescription()
			elif iData1 == 6782:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
			elif iData1 == 6783:
				return CyTranslator().getText("TXT_KEY_MISC_RIVERS", ())
			elif iData1 == 6785:
				return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
			elif iData1 == 6786:
				return gc.getVictoryInfo(iData2).getDescription()
			elif iData1 == 6787:
				return gc.getProcessInfo(iData2).getDescription()
			elif iData1 == 6788:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getRouteInfo(iData2).getDescription()
			elif iData1 == 6789:
				return gc.getTraitInfo(iData2).getDescription()
			elif iData1 == 6791:
				return gc.getCultureLevelInfo(iData2).getDescription()
			elif iData1 == 6792:
				return gc.getGameSpeedInfo(iData2).getDescription()
			elif iData1 == 6793:
				return gc.getHandicapInfo(iData2).getDescription()
			elif iData1 == 6795:
				return gc.getEraInfo(iData2).getDescription()
			elif iData1 == 6796:
				if iData2 == 999:
					return CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return gc.getUpkeepInfo(iData2).getDescription()
			elif iData1 == 6797:
				return gc.getWorldInfo(iData2).getDescription()
## Tech Help Text ##
			elif iData1 == 7800:
				return gc.getTechInfo(iData2).getHelp()
## Religion Widget Text##
			elif iData1 == 7869:
				return CyGameTextMgr().parseReligionInfo(iData2, False)
## Building Widget Text##
			elif iData1 == 7870:
				return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
## Ultrapack ##
		return u""
		
	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList
		
		##### <written by F> #####
		#東方ユニットたちのＵＧ費用
		#処理のたびにいちいちリストを再定義するのもあほらしいので、
		#今後の更新でTohoUnitList.pyの方にリストを移す予定。
		pPlayer = gc.getPlayer(iPlayer)
		pUnit = pPlayer.getUnit(iUnitID)
		
		if gc.getInfoTypeForString('UNIT_SANAE0') <=  iUnitTypeUpgrade and iUnitTypeUpgrade <= gc.getInfoTypeForString('UNIT_SAGUME6') and ( gc.getInfoTypeForString('UNITCOMBAT_BOSS') == pUnit.getUnitCombatType() or gc.getInfoTypeForString('UNITCOMBAT_STANDBY') == pUnit.getUnitCombatType()):
		
			#アップグレードコストのリスト　ここの数字をいじればＵＧコストが変更可能
			#以下のコストは、「そのユニットになるのに必要な金額」であり、
			#各ユニットの0番目にはＵＧできないのでコスト-1となっている
			#ＡＩの場合段階飛ばしＵＧによりＵＧコストが割安となってしまうのだが、
			#まぁ資金不足でＵＧできなくなっても困るし、とりあえず現状はハンデということで放置
			#キャラクターマークによるＵＧ金額補正は無視され、こちらの金額が優先される模様
			CostList = [
						-1,  20,  20,  25,  40,  60, 90,   #早苗
						-1,  20,  20,  25,  40,  60, 90,   #レミリア
						-1,  20,  20,  25,  40,  60, 90,   #ちぇん
						-1,  20,  20,  25,  40,  60, 90,   #リグル
						-1,  20,  20,  25,  40,  60, 90,   #てゐ
						-1,  30,  20,  25,  40,  60, 90,   #にとり
						-1,  20,  20,  25,  40,  60, 90,   #魔理沙
						-1,  20,  20,  25,  40,  60, 90,   #フラン
						-1,  20,  20,  25,  40,  60, 90,   #ようむ
						-1,  20,  20,  25,  40,  60, 90,   #チルノ
						-1,  20,  20,  25,  40,  60, 90,   #えーりん
						-1,  30,  20,  25,  40,  60, 90,   #諏訪子
						-1,  20,  20,  25,  40,  60, 90,   #アリス
						-1,  30,  40,  50,  60,  70, 100,   #もこ
						-1,  30,  40,  50,  60,  70, 100,   #けーね
						-1,  20,  20,  25,  40,  60, 90,   #パルスィ
						-1,  20,  20,  25,  40,  60, 90,   #ゆぎ
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #きもけーね　実際にＵＧは出来ないが、便宜上リストに登録
						-1,  20,  20,  25,  40,  60, 90,   #咲夜
						-1,  20,  20,  25,  40,  60, 90,   #ゆゆこ
						-1,  20,  20,  25,  40,  60, 90,   #ルーミア
						-1,  20,  20,  25,  40,  60, 90,   #神奈子
						-1,  20,  20,  25,  40,  60, 90,   #霊夢
						-1,  30,  40,  50,  60,  70, 100,   #ゆうか
						-1,  20,  20,  25,  40,  60, 90,   #メディ
						-1,  20,  20,  25,  40,  60, 90,   #こいし
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #透明こいし　これも同様
						-1,  20,  20,  25,  40,  60, 90,   #ぱちゅりー
						-1,  30,  20,  25,  40,  60, 90,   #らん
						-1,  20,  20,  25,  40,  60, 90,   #うどんげ
						-1,  20,  20,  25,  40,  60, 90,   #いくさーん
						-1,  20,  20,  25,  40,  60, 90,   #さとり
						-1,  20,  20,  25,  40,  60, 90,   #ミスティア
						-1,  20,  20,  25,  40,  60, 90,   #すいか
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #すいか大
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #ちびすいか
						-1,  20,  20,  25,  40,  60, 90,   #山すいか
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #山すいか大
						-1,  -1,  -1,  -1,  -1,  -1,  -1,   #山ちびすいか
						-1,  30,  40,  50,  60,  70, 100,   #小町
						-1,  20,  20,  25,  40,  60, 90,   #スーさん付きめらんこ
						-1,  20,  20,  25,  40,  60, 90,   #めーりん
						-1,  30,  20,  25,  40,  60, 90,   #ゆかりん
						-1,  30,  20,  25,  40,  60, 90,   #神社ゆかりん
						-1,  20,  20,  25,  40,  60, 90,   #かぐや
						-1,  20,  20,  25,  40,  60, 90,   #てんこ
						-1,  20,  20,  25,  40,  60, 90,   #おりん
						-1,  20,  20,  25,  40,  60, 90,   #ねこおりん
						-1,  20,  20,  25,  40,  60, 90,   #レティ
						-1,  20,  20,  25,  40,  60, 90,   #みま
						-1,  30,  40,  50,  60,  70, 100,   #えいき
						-1,  20,  20,  25,  40,  60, 90,   #なず
						-1,  20,  20,  25,  40,  60, 90,   #小傘
						-1,  20,  20,  25,  40,  60, 90,   #一輪
						-1,  20,  20,  25,  40,  60, 90,   #みっちゃん
						-1,  20,  20,  25,  40,  60, 90,   #星
						-1,  30,  40,  50,  60,  70, 100,   #ひじりん
						-1,  20,  20,  25,  40,  60, 90,   #ぬえっち
						-1,  20,  20,  25,  40,  60, 90,   #芳香
						-1,  30,  20,  25,  40,  60, 90,   #青娥
						-1,  20,  20,  25,  40,  60, 90,   #屠自古
						-1,  20,  20,  25,  40,  60, 90,   #布都
						-1,  20,  20,  25,  40,  60, 90,   #神子
						-1,  20,  20,  25,  40,  60, 90,   #八橋
						-1,  20,  20,  25,  40,  60, 90,   #べんべん
						-1,  20,  20,  25,  40,  60, 90,   #正邪
						-1,  20,  20,  25,  40,  60, 90,   #しんみょうまる
						-1,  30,  40,  50,  60,  70, 100,   #雷鼓
						-1,  40,  60,  80,  100,  150, 200,   #依姫※他東方ユニットよりUG費高め
						-1,  40,  60,  80,  100,  150, 200,   #豊姫※他東方ユニットよりUG費高め
						-1,  20,  20,  25,  40,  60, 90,   #せーらん
						-1,  20,  20,  25,  40,  60, 90,   #おりんご
						-1,  20,  20,  25,  40,  60, 90,   #どれみ
						-1,  20,  20,  25,  40,  60, 90,   #サグメ
						]
			
			#時代ごとのＵＧコスト補正　数字は％表記で、後半の時代ほど高額になる
			#一応設定したけど未来まで行くことは多分無いんじゃないかな・・・
			EraCorrectList = [
								100,  #古代
								120,  #古典
								150,  #中世
								200,  #ルネサンス
								300,  #工業化
								500,  #現代
								800,  #未来
							]
			
			#ゲーム速度ごとのＵＧコスト補正　％表記
			#一般ユニットはハンマー数が基準になっているので問題ないのだが、このままだと速度に関係なく一律になるため
			GameSpeedList = [
								200,  #マラソン
								150,  #優雅
								100,  #普通
								 67,  #迅速
								 50,  #天狗
							]
			
			#昇進によるＵＧコスト補正
			#とりあえず基本操作で10％、教練で5％の割引
			PromotionList = [
								['PROMOTION_TOHO_COMBAT1',10],
								['PROMOTION_TOHO_COMBAT2',10],
								['PROMOTION_TOHO_COMBAT3',10],
								['PROMOTION_TOHO_COMBAT4',10],
								['PROMOTION_TOHO_COMBAT5',10],
								['PROMOTION_TOHO_COMBAT6',10],
								['PROMOTION_TOHO_DRILL1',5],
								['PROMOTION_TOHO_DRILL2',5],
								['PROMOTION_TOHO_DRILL3',5],
								['PROMOTION_TOHO_DRILL4',5],
							]
			iNumPromotionCost = 100
			for i in range(len(PromotionList)):
				if pUnit.isHasPromotion(gc.getInfoTypeForString(PromotionList[i][0])):
					iNumPromotionCost = iNumPromotionCost - PromotionList[i][1]
			
			
			iLose = pUnit.getNumLoseCount()
			if iLose > 5:
				iLose = 5
			iNum = iUnitTypeUpgrade - gc.getInfoTypeForString('UNIT_SANAE0')
			iEra = pPlayer.getCurrentEra()
			iSpeed = gc.getGame().getGameSpeedType()
			
			
			lastUGCost =  CostList[iNum] * EraCorrectList[iEra] * GameSpeedList[iSpeed] * (120**iLose) / (100**iLose) / 100 * iNumPromotionCost / 100 / 100
			
			
			#AI強化モードによる補正
			if pPlayer.isHuman() == False and gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_STRONG_AI')):
				lastUGCost = lastUGCost * TohoUnitList.UGCostList[Functions.getHandicap()] / 100
			if lastUGCost<0:
				lastUGCost = 1
				
			return lastUGCost
		
		#上海のＵＧコスト
		elif gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1') <=  iUnitTypeUpgrade and iUnitTypeUpgrade <= gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL6') and gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1') <=  pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL6'):
			#東方ユニットと違い、通常のユニットと同じような計算式　以下のリストはハンマーコスト
			ShanghaiCost = [
								30,
								40,
								60,
								80,
								110,
								140,
							]
			
			#ゲーム速度ごとのハンマーコスト補正　％表記
			GameSpeedList = [
								200,  #マラソン
								150,  #優雅
								100,  #普通
								 67,  #迅速
								 50,  #天狗
							]
			
			#doprint('Shanghai Numberr: %i \n' %(pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1')))
						
			DisHummer = ShanghaiCost[iUnitTypeUpgrade - gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1')] - ShanghaiCost[pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1')]
			if pPlayer.isHuman() == False :
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100 * TohoUnitList.UGCostList[Functions.getHandicap()] / 100
			else:
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100
		
		#蓬莱のＵＧコスト
		elif gc.getInfoTypeForString('UNIT_HOURAI_DOLL1') <=  iUnitTypeUpgrade and iUnitTypeUpgrade <= gc.getInfoTypeForString('UNIT_HOURAI_DOLL6') and gc.getInfoTypeForString('UNIT_HOURAI_DOLL1') <=  pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_HOURAI_DOLL6'):
			#東方ユニットと違い、通常のユニットと同じような計算式　以下のリストはハンマーコスト
			HOURAICost = [
								30,
								40,
								60,
								80,
								110,
								140,
							]
			
			#ゲーム速度ごとのハンマーコスト補正　％表記
			GameSpeedList = [
								200,  #マラソン
								150,  #優雅
								100,  #普通
								 67,  #迅速
								 50,  #天狗
							]
			
			#doprint('HOURAI Numberr: %i \n' %(pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_HOURAI_DOLL1')))
						
			DisHummer = HOURAICost[iUnitTypeUpgrade - gc.getInfoTypeForString('UNIT_HOURAI_DOLL1')] - HOURAICost[pUnit.getUnitType() - gc.getInfoTypeForString('UNIT_HOURAI_DOLL1')]
			if pPlayer.isHuman() == False :
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100 * TohoUnitList.UGCostList[Functions.getHandicap()] / 100
			else:
				return 20 + DisHummer * 3 * GameSpeedList[gc.getGame().getGameSpeedType()] / 100
		
		##### </written by F> #####
		
		return -1	# Any value 0 or above will be used
	
	def getExperienceNeeded(self, argsList):
		# use this function to set how much experience a unit needs
		iLevel, iOwner = argsList
		
		iExperienceNeeded = 0

		# regular epic game experience		
		iExperienceNeeded = iLevel * iLevel + 1

		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if (0 != iModifier):
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP
			
		return iExperienceNeeded
		