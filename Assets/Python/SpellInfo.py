 # -*- coding: cp932 -*- 

##### <written by F> #####
#スペルの挙動についての記述
#基本的にFfH Age of Iceのをそのまま流用しているので、使ってない関数などがいっぱいある

from CvPythonExtensions import *
from PyHelpers import *
import CvGameUtils
import Popup as PyPopup
import PyHelpers
import TohoUnitList
import Functions
import math

LevelBaseNum = [0,1,2,3,4,5,6,8,10,13,18,24,32]
for i in range(13,256):
	LevelBaseNum.append(32)

SummonBaseNum = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,10,11,12,14,16,18,20,24,]
for i in range(26,256):
	SummonBaseNum.append(24)

AISpellCastBaseNum = 20.0

RangeList0 = [[0,0],]

RangeList1 = [	[-1,-1],[ 0,-1],[ 1,-1],
				[-1, 0],        [ 1, 0],
				[-1, 1],[ 0, 1],[ 1, 1], ]
				
RangeList2 = [	[-2,-2],[-1,-2],[ 0,-2],[ 1,-2],[ 2,-2],
				[-2,-1],[-1,-1],[ 0,-1],[ 1,-1],[ 2,-1],
				[-2, 0],[-1, 0],        [ 1, 0],[ 2, 0],
				[-2, 1],[-1, 1],[ 0, 1],[ 1, 1],[ 2, 1],
				[-2, 2],[-1, 2],[ 0, 2],[ 1, 2],[ 2, 2], ]

RangeList3 = [	[-3,-3],[-2,-3],[ -1,-3],[ 0,-3],[ 1,-3],[2,-3],[3,-3],
				[-3,-2],[-2,-2],[ -1,-2],[ 0,-2],[ 1,-2],[2,-2],[3,-2],
				[-3,-1],[-2,-1],[ -1,-1],[ 0,-1],[ 1,-1],[2,-1],[3,-1],
				[-3, 0],[-2, 0],[ -1, 0],        [ 1, 0],[2, 0],[3, 0],
				[-3, 1],[-2, 1],[ -1, 1],[ 0, 1],[ 1, 1],[2, 1],[3, 1],
				[-3, 2],[-2, 2],[ -1, 2],[ 0, 2],[ 1, 2],[2, 2],[3, 2],
				[-3, 3],[-2, 3],[ -1, 3],[ 0, 3],[ 1, 3],[2, 3],[3, 3], ]

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

#global SpellCaster

ACTION_NUMBER = -1
spellAction = {}

def tempIsAISpellCast(caster):
	return 0;

class SpellInfo: #storage class for all the stuff describing a spell. Makes lots of use of passing functions around, probably a bad idea.
	def __init__(self,name,cannotCastFunc,spellFunc,isAISpellCastFunc = tempIsAISpellCast,helpTextFunc = None,cost = 0,sCAL=0,eCAL=255):
		" void - (string name(must correspond to a CvActionInfo's name),bool func(bool bTestVisible,pUnit) cannotCastFunc, void func() spellFunc)"
		CvGameUtils.doprint("for %s: %i" % (name,gc.getInfoTypeForString(name)))
		CvGameUtils.doprint("for %s: %s" % (name,str(gc.getAutomateInfo(gc.getInfoTypeForString(name)))))
		#whee, no getActionInfoIndex on Automate info, so we do this the ugly way
		delta = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()+gc.getNumUnitInfos()+gc.getNumReligionInfos()+gc.getNumSpecialistInfos()+gc.getNumBuildingInfos()+gc.getNumControlInfos()+7
		#delta = 575
		self.__action = gc.getInfoTypeForString(name) +delta
		self.__name = name
		self.__cannotCastFunc = cannotCastFunc
		self.__spellFunc = spellFunc
		self.__helpTextFunc = helpTextFunc
		self.__isAISpellCastFunc = isAISpellCastFunc
		self.__cost = cost
		self.__sCAL = sCAL
		self.__eCAL = eCAL
		spellAction[self.__action]=self
	def getName(self):
		return self.__name
	def getActionNumber(self):
		return self.__action
	def getCannotCastFunction(self):
		return self.__cannotCastFunc
	def getSpellFunction(self):
		return self.__spellFunc
	def isAbled(self,caster):
		return self.__cannotCastFunc(False,caster,self.__sCAL,self.__eCAL,self.__cost)
	def isInvisible(self):
		return self.__cannotCastFunc(True)
	def isVisible(self,caster):
		return self.__cannotCastFunc(True,caster,self.__sCAL,self.__eCAL,self.__cost)
	def cast(self,caster):
		return self.__spellFunc(caster,self.__cost)
	def __str__(self):
		return self.__name
	def estimate(self,caster):
		return self.__isAISpellCastFunc(caster)
	def getCost(self):
		return self.__cost
	def getHelpText(self, szText, caster, CAL):
		if self.__helpTextFunc :
			return self.__helpTextFunc(szText, caster, CAL)
		return 0

gc = CyGlobalContext()



spells = None #done in onInit - problem is that promotions need to be loaded

def init_force():
	global spells
	spells = [ #これ全部スペルだってんだからおそろしい
	SpellInfo("SPELLCARD_SANAE1_1",req_SANAE1,spellcard_SANAE1,spellcard_SANAE1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_SANAE1_2",req_SANAE1,spellcard_SANAE1,spellcard_SANAE1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_SANAE1_3",req_SANAE1,spellcard_SANAE1,spellcard_SANAE1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_SANAE1_4",req_SANAE1,spellcard_SANAE1,spellcard_SANAE1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_SANAE1_5",req_SANAE1,spellcard_SANAE1,spellcard_SANAE1_Estimate,None,1.0,16,19),
	SpellInfo("SPELLCARD_SANAE1_6",req_SANAE1,spellcard_SANAE1,spellcard_SANAE1_Estimate,None,1.0,20,23),
	SpellInfo("SPELLCARD_SANAE1_7",req_SANAE1,spellcard_SANAE1,spellcard_SANAE1_Estimate,None,1.0,24,255),
	SpellInfo("SPELLCARD_REMILIA1_1",req_REMILIA1,spellcard_REMILIA1,spellcard_REMILIA1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_REMILIA1_2",req_REMILIA1,spellcard_REMILIA1,spellcard_REMILIA1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_CHEN1_1",req_CHEN1,spellcard_CHEN1,spellcard_CHEN1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_CHEN1_2",req_CHEN1,spellcard_CHEN1,spellcard_CHEN1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_CHEN1_3",req_CHEN1,spellcard_CHEN1,spellcard_CHEN1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_CHEN1_4",req_CHEN1,spellcard_CHEN1,spellcard_CHEN1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_CHEN1_5",req_CHEN1,spellcard_CHEN1,spellcard_CHEN1_Estimate,None,1.0,16,19),
	SpellInfo("SPELLCARD_CHEN1_6",req_CHEN1,spellcard_CHEN1,spellcard_CHEN1_Estimate,None,1.0,20,255),
	SpellInfo("SPELLCARD_WRIGGLE1_1",req_WRIGGLE1,spellcard_WRIGGLE1,spellcard_WRIGGLE1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_WRIGGLE1_2",req_WRIGGLE1,spellcard_WRIGGLE1,spellcard_WRIGGLE1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_TEWI1_1",req_TEWI1,spellcard_TEWI1,spellcard_TEWI1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_TEWI1_2",req_TEWI1,spellcard_TEWI1,spellcard_TEWI1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_TEWI1_3",req_TEWI1,spellcard_TEWI1,spellcard_TEWI1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_TEWI1_4",req_TEWI1,spellcard_TEWI1,spellcard_TEWI1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_NITORI1_1",req_NITORI1,spellcard_NITORI1,spellcard_NITORI1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_NITORI1_2",req_NITORI1,spellcard_NITORI1,spellcard_NITORI1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_NITORI1_3",req_NITORI1,spellcard_NITORI1,spellcard_NITORI1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_NITORI1_4",req_NITORI1,spellcard_NITORI1,spellcard_NITORI1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_MARISA1_1",req_MARISA1,spellcard_MARISA1,spellcard_MARISA1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_MARISA1_2",req_MARISA1,spellcard_MARISA1,spellcard_MARISA1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_FLAN1_1",req_FLAN1,spellcard_FLAN1,spellcard_FLAN1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_FLAN1_2",req_FLAN1,spellcard_FLAN1,spellcard_FLAN1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_FLAN1_3",req_FLAN1,spellcard_FLAN1,spellcard_FLAN1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_FLAN1_4",req_FLAN1,spellcard_FLAN1,spellcard_FLAN1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_FLAN1_5",req_FLAN1,spellcard_FLAN1,spellcard_FLAN1_Estimate,None,1.0,16,19),
	SpellInfo("SPELLCARD_FLAN1_6",req_FLAN1,spellcard_FLAN1,spellcard_FLAN1_Estimate,None,1.0,20,23),
	SpellInfo("SPELLCARD_FLAN1_7",req_FLAN1,spellcard_FLAN1,spellcard_FLAN1_Estimate,None,1.0,24,255),
	SpellInfo("SPELLCARD_YOUMU1_1",req_YOUMU1,spellcard_YOUMU1,spellcard_YOUMU1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_YOUMU1_2",req_YOUMU1,spellcard_YOUMU1,spellcard_YOUMU1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_YOUMU1_3",req_YOUMU1,spellcard_YOUMU1,spellcard_YOUMU1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_CIRNO1_1",req_CIRNO1,spellcard_CIRNO1,spellcard_CIRNO1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_CIRNO1_2",req_CIRNO1,spellcard_CIRNO1,spellcard_CIRNO1_Estimate,None,1.0,4,255),
	SpellInfo("SPELLCARD_EIRIN1_1",req_EIRIN1,spellcard_EIRIN1,spellcard_EIRIN1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_EIRIN1_2",req_EIRIN1,spellcard_EIRIN1,spellcard_EIRIN1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_EIRIN1_3",req_EIRIN1,spellcard_EIRIN1,spellcard_EIRIN1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_EIRIN1_4",req_EIRIN1,spellcard_EIRIN1,spellcard_EIRIN1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_SUWAKO1_1",req_SUWAKO1,spellcard_SUWAKO1,spellcard_SUWAKO1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_ALICE1_1",req_ALICE1,spellcard_ALICE1,spellcard_ALICE1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_ALICE1_2",req_ALICE1,spellcard_ALICE1,spellcard_ALICE1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_ALICE1_3",req_ALICE1,spellcard_ALICE1,spellcard_ALICE1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_ALICE1_4",req_ALICE1,spellcard_ALICE1,spellcard_ALICE1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_ALICE1_5",req_ALICE1,spellcard_ALICE1,spellcard_ALICE1_Estimate,None,1.0,16,19),
	SpellInfo("SPELLCARD_ALICE1_6",req_ALICE1,spellcard_ALICE1,spellcard_ALICE1_Estimate,None,1.0,20,255),
	SpellInfo("SPELLCARD_MOKOU1_1",req_MOKOU1,spellcard_MOKOU1,spellcard_MOKOU1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_KEINE1_1",req_KEINE1,spellcard_KEINE1,spellcard_KEINE1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_KEINE1_2",req_KEINE1,spellcard_KEINE1,spellcard_KEINE1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_KEINE1_3",req_KEINE1,spellcard_KEINE1,spellcard_KEINE1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_KEINE1_4",req_KEINE1,spellcard_KEINE1,spellcard_KEINE1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_KEINE1_5",req_KEINE1,spellcard_KEINE1,spellcard_KEINE1_Estimate,None,1.0,16,19),
	SpellInfo("SPELLCARD_KEINE1_6",req_KEINE1,spellcard_KEINE1,spellcard_KEINE1_Estimate,None,1.0,20,255),
	SpellInfo("SPELLCARD_HAKUTAKUKEINE1_1",req_HAKUTAKUKEINE1,spellcard_HAKUTAKUKEINE1,spellcard_HAKUTAKUKEINE1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_PARSEE1_1",req_PARSEE1,spellcard_PARSEE1,spellcard_PARSEE1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_PARSEE1_2",req_PARSEE1,spellcard_PARSEE1,spellcard_PARSEE1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_YUGI1_1",req_YUGI1,spellcard_YUGI1,spellcard_YUGI1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_SAKUYA1_1",req_SAKUYA1,spellcard_SAKUYA1,spellcard_SAKUYA1_Estimate,None,1.0,1,6),
	SpellInfo("SPELLCARD_SAKUYA1_2",req_SAKUYA1,spellcard_SAKUYA1,spellcard_SAKUYA1_Estimate,None,1.0,7,11),
	SpellInfo("SPELLCARD_SAKUYA1_3",req_SAKUYA1,spellcard_SAKUYA1,spellcard_SAKUYA1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_SAKUYA1_4",req_SAKUYA1,spellcard_SAKUYA1,spellcard_SAKUYA1_Estimate,None,1.0,16,255),
	SpellInfo("SPELLCARD_YUYUKO1_1",req_YUYUKO1,spellcard_YUYUKO1,spellcard_YUYUKO1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_YUYUKO1_2",req_YUYUKO1,spellcard_YUYUKO1,spellcard_YUYUKO1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_YUYUKO1_3",req_YUYUKO1,spellcard_YUYUKO1,spellcard_YUYUKO1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_YUYUKO1_4",req_YUYUKO1,spellcard_YUYUKO1,spellcard_YUYUKO1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_RUMIA1_1",req_RUMIA1,spellcard_RUMIA1,spellcard_RUMIA1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_MEDICIN1_1",req_MEDICIN1,spellcard_MEDICIN1,spellcard_MEDICIN1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_MEDICIN1_2",req_MEDICIN1,spellcard_MEDICIN1,spellcard_MEDICIN1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_MEDICIN1_3",req_MEDICIN1,spellcard_MEDICIN1,spellcard_MEDICIN1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_MEDICIN1_4",req_MEDICIN1,spellcard_MEDICIN1,spellcard_MEDICIN1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_KANAKO1_1",req_KANAKO1,spellcard_KANAKO1,spellcard_KANAKO1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_KANAKO1_2",req_KANAKO1,spellcard_KANAKO1,spellcard_KANAKO1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_REIMU1_1",req_REIMU1,spellcard_REIMU1,spellcard_REIMU1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_YUKA1_1",req_YUKA1,spellcard_YUKA1,spellcard_YUKA1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_KOISHI1_1",req_KOISHI1,spellcard_KOISHI1,spellcard_KOISHI1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_PATCHOULI1_1",req_PATCHOULI1,spellcard_PATCHOULI1,spellcard_PATCHOULI1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_PATCHOULI2_1",req_PATCHOULI1,spellcard_PATCHOULI2,spellcard_PATCHOULI2_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_RAN1_1",req_RAN1,spellcard_RAN1,spellcard_RAN1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_RAN1_2",req_RAN1,spellcard_RAN1,spellcard_RAN1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_RAN1_3",req_RAN1,spellcard_RAN1,spellcard_RAN1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_RAN1_4",req_RAN1,spellcard_RAN1,spellcard_RAN1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_REISEN1_1",req_REISEN1,spellcard_REISEN1,spellcard_REISEN1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_REISEN1_2",req_REISEN1,spellcard_REISEN1,spellcard_REISEN1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_IKU1_1",req_IKU1,spellcard_IKU1,spellcard_IKU1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_IKU1_2",req_IKU1,spellcard_IKU1,spellcard_IKU1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_IKU1_3",req_IKU1,spellcard_IKU1,spellcard_IKU1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_IKU1_4",req_IKU1,spellcard_IKU1,spellcard_IKU1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_SATORI1_1",req_SATORI1,spellcard_SATORI1,spellcard_SATORI1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_SATORI1_2",req_SATORI1,spellcard_SATORI1,spellcard_SATORI1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_SATORI1_3",req_SATORI1,spellcard_SATORI1,spellcard_SATORI1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_SATORI1_4",req_SATORI1,spellcard_SATORI1,spellcard_SATORI1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_SATORI1_5",req_SATORI1,spellcard_SATORI1,spellcard_SATORI1_Estimate,None,1.0,16,255),
	SpellInfo("SPELLCARD_MYSTIA1_1",req_MYSTIA1,spellcard_MYSTIA1,spellcard_MYSTIA1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_MYSTIA1_2",req_MYSTIA1,spellcard_MYSTIA1,spellcard_MYSTIA1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_MYSTIA1_3",req_MYSTIA1,spellcard_MYSTIA1,spellcard_MYSTIA1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_SUIKA1_1",req_SUIKA1,spellcard_SUIKA1,spellcard_SUIKA1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_SUIKA1_2",req_SUIKA1,spellcard_SUIKA1,spellcard_SUIKA1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_SUIKA1_3",req_SUIKA1,spellcard_SUIKA1,spellcard_SUIKA1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_SUIKA1_4",req_SUIKA1,spellcard_SUIKA1,spellcard_SUIKA1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_KOMACHI1_1",req_KOMACHI1,spellcard_KOMACHI1,spellcard_KOMACHI1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_MEIRIN1_1",req_MEIRIN1,spellcard_MEIRIN1,spellcard_MEIRIN1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_MEIRIN1_2",req_MEIRIN1,spellcard_MEIRIN1,spellcard_MEIRIN1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_YUKARI1_1",req_YUKARI1,spellcard_YUKARI1,spellcard_YUKARI1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_YUKARI1_2",req_YUKARI1,spellcard_YUKARI1,spellcard_YUKARI1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_KAGUYA1_1",req_KAGUYA1,spellcard_KAGUYA1,spellcard_KAGUYA1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_KAGUYA1_2",req_KAGUYA1,spellcard_KAGUYA1,spellcard_KAGUYA1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_KAGUYA1_3",req_KAGUYA1,spellcard_KAGUYA1,spellcard_KAGUYA1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_KAGUYA1_4",req_KAGUYA1,spellcard_KAGUYA1,spellcard_KAGUYA1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_TENSHI1_1",req_TENSHI1,spellcard_TENSHI1,spellcard_TENSHI1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_TENSHI1_2",req_TENSHI1,spellcard_TENSHI1,spellcard_TENSHI1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_TENSHI1_3",req_TENSHI1,spellcard_TENSHI1,spellcard_TENSHI1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_RIN1_1",req_RIN1,spellcard_RIN1,spellcard_RIN1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_RIN1_2",req_RIN1,spellcard_RIN1,spellcard_RIN1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_LETTY1_1",req_LETTY1,spellcard_LETTY1,spellcard_LETTY1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_MIMA1_1",req_MIMA1,spellcard_MIMA1,spellcard_MIMA1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_EIKI1_1",req_EIKI1,spellcard_EIKI1,spellcard_EIKI1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_NAZRIN1_1",req_NAZRIN1,spellcard_NAZRIN1,spellcard_NAZRIN1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_NAZRIN1_2",req_NAZRIN1,spellcard_NAZRIN1,spellcard_NAZRIN1_Estimate,None,1.0,8,15),
	SpellInfo("SPELLCARD_NAZRIN1_3",req_NAZRIN1,spellcard_NAZRIN1,spellcard_NAZRIN1_Estimate,None,1.0,16,255),
	SpellInfo("SPELLCARD_KOGASA1_1",req_KOGASA1,spellcard_KOGASA1,spellcard_KOGASA1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_KOGASA1_2",req_KOGASA1,spellcard_KOGASA1,spellcard_KOGASA1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_KOGASA1_3",req_KOGASA1,spellcard_KOGASA1,spellcard_KOGASA1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_ICHIRIN1_1",req_ICHIRIN1,spellcard_ICHIRIN1,spellcard_ICHIRIN1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_ICHIRIN1_2",req_ICHIRIN1,spellcard_ICHIRIN1,spellcard_ICHIRIN1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_ICHIRIN1_3",req_ICHIRIN1,spellcard_ICHIRIN1,spellcard_ICHIRIN1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_MINAMITSU1_1",req_MINAMITSU1,spellcard_MINAMITSU1,spellcard_MINAMITSU1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_MINAMITSU1_2",req_MINAMITSU1,spellcard_MINAMITSU1,spellcard_MINAMITSU1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_MINAMITSU1_3",req_MINAMITSU1,spellcard_MINAMITSU1,spellcard_MINAMITSU1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_SYOU1_1",req_SYOU1,spellcard_SYOU1,spellcard_SYOU1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_SYOU1_2",req_SYOU1,spellcard_SYOU1,spellcard_SYOU1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_BYAKUREN1_1",req_BYAKUREN1,spellcard_BYAKUREN1,spellcard_BYAKUREN1_Estimate,None,1.0,1,3),
	SpellInfo("SPELLCARD_BYAKUREN1_2",req_BYAKUREN1,spellcard_BYAKUREN1,spellcard_BYAKUREN1_Estimate,None,1.0,4,7),
	SpellInfo("SPELLCARD_BYAKUREN1_3",req_BYAKUREN1,spellcard_BYAKUREN1,spellcard_BYAKUREN1_Estimate,None,1.0,8,11),
	SpellInfo("SPELLCARD_BYAKUREN1_4",req_BYAKUREN1,spellcard_BYAKUREN1,spellcard_BYAKUREN1_Estimate,None,1.0,12,15),
	SpellInfo("SPELLCARD_BYAKUREN1_5",req_BYAKUREN1,spellcard_BYAKUREN1,spellcard_BYAKUREN1_Estimate,None,1.0,16,19),
	SpellInfo("SPELLCARD_BYAKUREN1_6",req_BYAKUREN1,spellcard_BYAKUREN1,spellcard_BYAKUREN1_Estimate,None,1.0,20,255),
	SpellInfo("SPELLCARD_NUE1_1",req_NUE1,spellcard_NUE1,spellcard_NUE1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_YOSHIKA1_1",req_YOSHIKA1,spellcard_YOSHIKA1,spellcard_YOSHIKA1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_YOSHIKA1_2",req_YOSHIKA1,spellcard_YOSHIKA1,spellcard_YOSHIKA1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_SEIGA1_1",req_SEIGA1,spellcard_SEIGA1,spellcard_SEIGA1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_SEIGA1_2",req_SEIGA1,spellcard_SEIGA1,spellcard_SEIGA1_Estimate,None,1.0,8,15),
	SpellInfo("SPELLCARD_SEIGA1_3",req_SEIGA1,spellcard_SEIGA1,spellcard_SEIGA1_Estimate,None,1.0,16,255),
	SpellInfo("SPELLCARD_TOJIKO1_1",req_TOJIKO1,spellcard_TOJIKO1,spellcard_TOJIKO1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_TOJIKO1_2",req_TOJIKO1,spellcard_TOJIKO1,spellcard_TOJIKO1_Estimate,None,1.0,8,255),
	SpellInfo("SPELLCARD_FUTO1_1",req_FUTO1,spellcard_FUTO1,spellcard_FUTO1_Estimate,help_FUTO1,1.0,1,11),
	SpellInfo("SPELLCARD_FUTO1_2",req_FUTO1,spellcard_FUTO1,spellcard_FUTO1_Estimate,help_FUTO1,1.0,12,255),
	SpellInfo("SPELLCARD_MIMIMIKO1_1",req_MIMIMIKO1,spellcard_MIMIMIKO1,spellcard_MIMIMIKO1_Estimate,None,1.0,1,15),
	SpellInfo("SPELLCARD_MIMIMIKO1_2",req_MIMIMIKO1,spellcard_MIMIMIKO1,spellcard_MIMIMIKO1_Estimate,None,1.0,16,255),
	SpellInfo("SPELLCARD_YATUHASHI1_1",req_YATUHASHI1,spellcard_YATUHASHI1,spellcard_YATUHASHI1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_BENBEN1_1",req_BENBEN1,spellcard_BENBEN1,spellcard_BENBEN1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_SEIJA1_1",req_SEIJA1,spellcard_SEIJA1,spellcard_SEIJA1_Estimate,None,1.0,1,11),
	SpellInfo("SPELLCARD_SEIJA1_2",req_SEIJA1,spellcard_SEIJA1,spellcard_SEIJA1_Estimate,None,1.0,12,255),
	SpellInfo("SPELLCARD_SHINMYOUMARU1_1",req_SHINMYOUMARU1,spellcard_SHINMYOUMARU1,spellcard_SHINMYOUMARU1_Estimate,help_SHINMYOUMARU1,1.0,1,7),
	SpellInfo("SPELLCARD_SHINMYOUMARU1_2",req_SHINMYOUMARU1,spellcard_SHINMYOUMARU1,spellcard_SHINMYOUMARU1_Estimate,help_SHINMYOUMARU1,1.0,8,15),
	SpellInfo("SPELLCARD_SHINMYOUMARU1_3",req_SHINMYOUMARU1,spellcard_SHINMYOUMARU1,spellcard_SHINMYOUMARU1_Estimate,help_SHINMYOUMARU1,1.0,16,255),
	SpellInfo("SPELLCARD_RAIKO1_1",req_RAIKO1,spellcard_RAIKO1,spellcard_RAIKO1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_YORIHIME1_1",req_YORIHIME1,spellcard_YORIHIME1,spellcard_YORIHIME1_Estimate,help_YORIHIME1,3.0,1,255),
	SpellInfo("SPELLCARD_YORIHIME2_1",req_YORIHIME2,spellcard_YORIHIME2,spellcard_YORIHIME2_Estimate,help_YORIHIME2,1.0,1,255),
	SpellInfo("SPELLCARD_YORIHIME3_1",req_YORIHIME3,spellcard_YORIHIME3,spellcard_YORIHIME3_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_TOYOHIME1_1",req_TOYOHIME1,spellcard_TOYOHIME1,spellcard_TOYOHIME1_Estimate,None,1.0,1,255),
	SpellInfo("SPELLCARD_SEIRAN1_1",req_SEIRAN1,spellcard_SEIRAN1,spellcard_SEIRAN1_Estimate,None,1.0,1,7),
	SpellInfo("SPELLCARD_SEIRAN1_2",req_SEIRAN1,spellcard_SEIRAN1,spellcard_SEIRAN1_Estimate,None,1.0,8,15),
	SpellInfo("SPELLCARD_SEIRAN1_3",req_SEIRAN1,spellcard_SEIRAN1,spellcard_SEIRAN1_Estimate,None,1.0,16,255),
	SpellInfo("SPELLCARD_RINGO1_1",req_RINGO1,spellcard_RINGO1,tempIsAISpellCast,help_RINGO1,1.0,1,11),
	SpellInfo("SPELLCARD_RINGO1_2",req_RINGO1,spellcard_RINGO1,tempIsAISpellCast,help_RINGO1,1.0,12,255),
	SpellInfo("SPELLCARD_DOREMY1_1",req_DOREMY1,spellcard_DOREMY1,spellcard_DOREMY1_Estimate,help_DOREMY1,1.0,1,255),
	SpellInfo("SPELLCARD_SAGUME1_1",req_SAGUME1,spellcard_SAGUME1,spellcard_SAGUME1_Estimate,None,1.0,1,14),
	SpellInfo("SPELLCARD_SAGUME1_2",req_SAGUME1,spellcard_SAGUME1,spellcard_SAGUME1_Estimate,None,1.0,15,255),
	
	
	SpellInfo("SPELL_SANAE_EXTRA1",req_SANAE_EXTRA1,spell_SANAE_EXTRA1),#                          ここからスペル
	SpellInfo("SPELL_SANAE_PHANTASM1",req_SANAE_PHANTASM1,spell_SANAE_PHANTASM1),
	SpellInfo("SPELL_REMILIA_EXTRA1",req_REMILIA_EXTRA1,spell_REMILIA_EXTRA1),
	SpellInfo("SPELL_REMILIA_PHANTASM1",req_REMILIA_PHANTASM1,spell_REMILIA_PHANTASM1,tempIsAISpellCast,None,0.15,1,255),
	SpellInfo("SPELL_CHEN_EXTRA1",req_CHEN_EXTRA1,spell_CHEN_EXTRA1),
	SpellInfo("SPELL_CHEN_PHANTASM1",req_CHEN_PHANTASM1,spell_CHEN_PHANTASM1),
	SpellInfo("SPELL_WRIGGLE_EXTRA1",req_WRIGGLE_EXTRA1,spell_WRIGGLE_EXTRA1),
	SpellInfo("SPELL_WRIGGLE_PHANTASM1",req_WRIGGLE_PHANTASM1,spell_WRIGGLE_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_TEWI_EXTRA1",req_TEWI_EXTRA1,spell_TEWI_EXTRA1),
	SpellInfo("SPELL_TEWI_PHANTASM1",req_TEWI_PHANTASM1,spell_TEWI_PHANTASM1),
	SpellInfo("SPELL_TEWI_PHANTASM2",req_TEWI_PHANTASM2,spell_TEWI_PHANTASM2,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_NITORI_EXTRA1",req_NITORI_EXTRA1,spell_NITORI_EXTRA1),
	SpellInfo("SPELL_NITORI_PHANTASM1",req_NITORI_PHANTASM1,spell_NITORI_PHANTASM1),
	SpellInfo("SPELL_MARISA_EXTRA1",req_MARISA_EXTRA1,spell_MARISA_EXTRA1),
	SpellInfo("SPELL_MARISA_PHANTASM1",req_MARISA_PHANTASM1,spell_MARISA_PHANTASM1),
	SpellInfo("SPELL_FLAN_EXTRA1",req_FLAN_EXTRA1,spell_FLAN_EXTRA1),
	SpellInfo("SPELL_FLAN_PHANTASM1",req_FLAN_PHANTASM1,spell_FLAN_PHANTASM1,tempIsAISpellCast,None,0.15,1,255),
	SpellInfo("SPELL_FLAN_PHANTASM2",req_FLAN_PHANTASM2,spell_FLAN_PHANTASM2),
	SpellInfo("SPELL_YOUMU_EXTRA1",req_YOUMU_EXTRA1,spell_YOUMU_EXTRA1),
	SpellInfo("SPELL_YOUMU_PHANTASM1",req_YOUMU_PHANTASM1,spell_YOUMU_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_CIRNO_EXTRA1",req_CIRNO_EXTRA1,spell_CIRNO_EXTRA1),
	SpellInfo("SPELL_CIRNO_PHANTASM1",req_CIRNO_PHANTASM1,spell_CIRNO_PHANTASM1),
	SpellInfo("SPELL_EIRIN_EXTRA1",req_EIRIN_EXTRA1,spell_EIRIN_EXTRA1),
	SpellInfo("SPELL_EIRIN_PHANTASM1",req_EIRIN_PHANTASM1,spell_EIRIN_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_SUWAKO_EXTRA1",req_SUWAKO_EXTRA1,spell_SUWAKO_EXTRA1),
	SpellInfo("SPELL_SUWAKO_PHANTASM1",req_SUWAKO_PHANTASM1,spell_SUWAKO_PHANTASM1),
	SpellInfo("SPELL_ALICE_EXTRA1",req_ALICE_EXTRA1,spell_ALICE_EXTRA1),
	SpellInfo("SPELL_ALICE_PHANTASM1",req_ALICE_PHANTASM1,spell_ALICE_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_MOKOU_EXTRA1",req_MOKOU_EXTRA1,spell_MOKOU_EXTRA1),
	SpellInfo("SPELL_MOKOU_PHANTASM1",req_MOKOU_PHANTASM1,spell_MOKOU_PHANTASM1),
	SpellInfo("SPELL_KEINE_EXTRA1",req_KEINE_EXTRA1,spell_KEINE_EXTRA1),
	SpellInfo("SPELL_KEINE_PHANTASM1",req_KEINE_PHANTASM1,spell_KEINE_PHANTASM1),
	SpellInfo("SPELL_HAKUTAKUKEINE_EXTRA1",req_HAKUTAKUKEINE_EXTRA1,spell_HAKUTAKUKEINE_EXTRA1),
	SpellInfo("SPELL_HAKUTAKUKEINE_PHANTASM1",req_HAKUTAKUKEINE_PHANTASM1,spell_HAKUTAKUKEINE_PHANTASM1),
	SpellInfo("SPELL_PARSEE_EXTRA1",req_PARSEE_EXTRA1,spell_PARSEE_EXTRA1),
	SpellInfo("SPELL_PARSEE_PHANTASM1",req_PARSEE_PHANTASM1,spell_PARSEE_PHANTASM1),
	SpellInfo("SPELL_YUGI_EXTRA1",req_YUGI_EXTRA1,spell_YUGI_EXTRA1),
	SpellInfo("SPELL_YUGI_PHANTASM1",req_YUGI_PHANTASM1,spell_YUGI_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_SAKUYA_EXTRA1",req_SAKUYA_EXTRA1,spell_SAKUYA_EXTRA1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_SAKUYA_PHANTASM1",req_SAKUYA_PHANTASM1,spell_SAKUYA_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_YUYUKO_EXTRA1",req_YUYUKO_EXTRA1,spell_YUYUKO_EXTRA1),
	SpellInfo("SPELL_YUYUKO_PHANTASM1",req_YUYUKO_PHANTASM1,spell_YUYUKO_PHANTASM1),
	SpellInfo("SPELL_RUMIA_EXTRA1",req_RUMIA_EXTRA1,spell_RUMIA_EXTRA1),
	SpellInfo("SPELL_RUMIA_PHANTASM1",req_RUMIA_PHANTASM1,spell_RUMIA_PHANTASM1),
	SpellInfo("SPELL_MEDICIN_EXTRA1",req_MEDICIN_EXTRA1,spell_MEDICIN_EXTRA1),
	SpellInfo("SPELL_MEDICIN_PHANTASM1",req_MEDICIN_PHANTASM1,spell_MEDICIN_PHANTASM1),
	SpellInfo("SPELL_KANAKO_EXTRA1",req_KANAKO_EXTRA1,spell_KANAKO_EXTRA1),
	SpellInfo("SPELL_KANAKO_PHANTASM1",req_KANAKO_PHANTASM1,spell_KANAKO_PHANTASM1),
	SpellInfo("SPELL_REIMU_EXTRA1",req_REIMU_EXTRA1,spell_REIMU_EXTRA1),
	SpellInfo("SPELL_REIMU_PHANTASM1",req_REIMU_PHANTASM1,spell_REIMU_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_YUKA_EXTRA1",req_YUKA_EXTRA1,spell_YUKA_EXTRA1),
	SpellInfo("SPELL_YUKA_PHANTASM1",req_YUKA_PHANTASM1,spell_YUKA_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_KOISHI_EXTRA1",req_KOISHI_EXTRA1,spell_KOISHI_EXTRA1),
	SpellInfo("SPELL_KOISHI_PHANTASM1",req_KOISHI_PHANTASM1,spell_KOISHI_PHANTASM1),
	SpellInfo("SPELL_KOISHI_SKILL1",req_KOISHI_SKILL1,spell_KOISHI_SKILL1),         
	SpellInfo("SPELL_KOISHI_SKILL2",req_KOISHI_SKILL2,spell_KOISHI_SKILL2),
	SpellInfo("SPELL_PATCHOULI_EXTRA1",req_PATCHOULI_EXTRA1,spell_PATCHOULI_EXTRA1),
	SpellInfo("SPELL_PATCHOULI_EXTRA2",req_PATCHOULI_EXTRA2,spell_PATCHOULI_EXTRA2),
	SpellInfo("SPELL_PATCHOULI_PHANTASM1",req_PATCHOULI_PHANTASM1,spell_PATCHOULI_PHANTASM1),
	SpellInfo("SPELL_PATCHOULI_PHANTASM2",req_PATCHOULI_PHANTASM2,spell_PATCHOULI_PHANTASM2),
	SpellInfo("SPELL_PATCHOULI_PHANTASM3",req_PATCHOULI_PHANTASM3,spell_PATCHOULI_PHANTASM3),
	SpellInfo("SPELL_RAN_EXTRA1",req_RAN_EXTRA1,spell_RAN_EXTRA1),
	SpellInfo("SPELL_RAN_PHANTASM1",req_RAN_PHANTASM1,spell_RAN_PHANTASM1),
	SpellInfo("SPELL_REISEN_EXTRA1",req_REISEN_EXTRA1,spell_REISEN_EXTRA1),
	SpellInfo("SPELL_REISEN_PHANTASM1",req_REISEN_PHANTASM1,spell_REISEN_PHANTASM1),
	SpellInfo("SPELL_IKU_EXTRA1",req_IKU_EXTRA1,spell_IKU_EXTRA1),
	SpellInfo("SPELL_IKU_PHANTASM1",req_IKU_PHANTASM1,spell_IKU_PHANTASM1),
	SpellInfo("SPELL_SATORI_EXTRA1",req_SATORI_EXTRA1,spell_SATORI_EXTRA1),
	SpellInfo("SPELL_SATORI_PHANTASM1",req_SATORI_PHANTASM1,spell_SATORI_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_MYSTIA_EXTRA1",req_MYSTIA_EXTRA1,spell_MYSTIA_EXTRA1),
	SpellInfo("SPELL_MYSTIA_PHANTASM1",req_MYSTIA_PHANTASM1,spell_MYSTIA_PHANTASM1),
	SpellInfo("SPELL_SUIKA_EXTRA1",req_SUIKA_EXTRA1,spell_SUIKA_EXTRA1),
	SpellInfo("SPELL_SUIKA_PHANTASM1",req_SUIKA_PHANTASM1,spell_SUIKA_PHANTASM1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_KOMACHI_EXTRA1",req_KOMACHI_EXTRA1,spell_KOMACHI_EXTRA1),
	SpellInfo("SPELL_KOMACHI_PHANTASM1",req_KOMACHI_PHANTASM1,spell_KOMACHI_PHANTASM1),
	SpellInfo("SPELL_MEIRIN_EXTRA1",req_MEIRIN_EXTRA1,spell_MEIRIN_EXTRA1,tempIsAISpellCast,None,0.0,1,255),
	SpellInfo("SPELL_MEIRIN_PHANTASM1",req_MEIRIN_PHANTASM1,spell_MEIRIN_PHANTASM1),
	SpellInfo("SPELL_YUKARI_EXTRA1",req_YUKARI_EXTRA1,spell_YUKARI_EXTRA1),
	SpellInfo("SPELL_YUKARI_PHANTASM1",req_YUKARI_PHANTASM1,spell_YUKARI_PHANTASM1),
	SpellInfo("SPELL_YUKARI_PHANTASM2",req_YUKARI_PHANTASM2,spell_YUKARI_PHANTASM2,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_YUKARI_PHANTASM3",req_YUKARI_PHANTASM3,spell_YUKARI_PHANTASM3),
	SpellInfo("SPELL_KAGUYA_EXTRA1",req_KAGUYA_EXTRA1,spell_KAGUYA_EXTRA1),
	SpellInfo("SPELL_KAGUYA_EXTRA2",req_KAGUYA_EXTRA2,spell_KAGUYA_EXTRA2),
	SpellInfo("SPELL_KAGUYA_EXTRA3",req_KAGUYA_EXTRA3,spell_KAGUYA_EXTRA3),
	SpellInfo("SPELL_KAGUYA_EXTRA4",req_KAGUYA_EXTRA4,spell_KAGUYA_EXTRA4),
	SpellInfo("SPELL_KAGUYA_EXTRA5",req_KAGUYA_EXTRA5,spell_KAGUYA_EXTRA5),
	SpellInfo("SPELL_KAGUYA_PHANTASM1",req_KAGUYA_PHANTASM1,spell_KAGUYA_PHANTASM1),
	SpellInfo("SPELL_KAGUYA_PHANTASM2",req_KAGUYA_PHANTASM2,spell_KAGUYA_PHANTASM2),
	SpellInfo("SPELL_KAGUYA_PHANTASM3",req_KAGUYA_PHANTASM3,spell_KAGUYA_PHANTASM3),
	SpellInfo("SPELL_KAGUYA_PHANTASM4",req_KAGUYA_PHANTASM4,spell_KAGUYA_PHANTASM4,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_TENSHI_EXTRA1",req_TENSHI_EXTRA1,spell_TENSHI_EXTRA1),
	SpellInfo("SPELL_TENSHI_PHANTASM1",req_TENSHI_PHANTASM1,spell_TENSHI_PHANTASM1),
	SpellInfo("SPELL_RIN_EXTRA1",req_RIN_EXTRA1,spell_RIN_EXTRA1),
	SpellInfo("SPELL_RIN_TO_CAT",req_SPELL_RIN_TO_CAT,spell_SPELL_RIN_TO_CAT),
	SpellInfo("SPELL_RIN_TO_RIN",req_SPELL_RIN_TO_RIN,spell_SPELL_RIN_TO_RIN),
	SpellInfo("SPELL_RIN_PHANTASM1",req_RIN_PHANTASM1,spell_RIN_PHANTASM1),
	SpellInfo("SPELL_LETTY_EXTRA1",req_LETTY_EXTRA1,spell_LETTY_EXTRA1),
	SpellInfo("SPELL_LETTY_PHANTASM1",req_LETTY_PHANTASM1,spell_LETTY_PHANTASM1),
	SpellInfo("SPELL_MIMA_EXTRA1",req_MIMA_EXTRA1,spell_MIMA_EXTRA1),
	SpellInfo("SPELL_MIMA_PHANTASM1",req_MIMA_PHANTASM1,spell_MIMA_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_EIKI_EXTRA1",req_EIKI_EXTRA1,spell_EIKI_EXTRA1),
	SpellInfo("SPELL_EIKI_PHANTASM1",req_EIKI_PHANTASM1,spell_EIKI_PHANTASM1,tempIsAISpellCast,help_EIKI_PHANTASM1,0.15,1,255),
	SpellInfo("SPELL_NAZRIN_EXTRA1",req_NAZRIN_EXTRA1,spell_NAZRIN_EXTRA1),
	SpellInfo("SPELL_NAZRIN_PHANTASM1",req_NAZRIN_PHANTASM1,spell_NAZRIN_PHANTASM1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_KOGASA_EXTRA1",req_KOGASA_EXTRA1,spell_KOGASA_EXTRA1),
	SpellInfo("SPELL_KOGASA_PHANTASM1",req_KOGASA_PHANTASM1,spell_KOGASA_PHANTASM1),
	SpellInfo("SPELL_ICHIRIN_SKILL1",req_ICHIRIN_SKILL1,spell_ICHIRIN_SKILL1),
	SpellInfo("SPELL_ICHIRIN_EXTRA1",req_ICHIRIN_EXTRA1,spell_ICHIRIN_EXTRA1),
	SpellInfo("SPELL_ICHIRIN_PHANTASM1",req_ICHIRIN_PHANTASM1,spell_ICHIRIN_PHANTASM1),
	SpellInfo("SPELL_MINAMITSU_EXTRA1",req_MINAMITSU_EXTRA1,spell_MINAMITSU_EXTRA1),
	SpellInfo("SPELL_MINAMITSU_PHANTASM1",req_MINAMITSU_PHANTASM1,spell_MINAMITSU_PHANTASM1),
	SpellInfo("SPELL_SYOU_EXTRA1",req_SYOU_EXTRA1,spell_SYOU_EXTRA1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_SYOU_PHANTASM1",req_SYOU_PHANTASM1,spell_SYOU_PHANTASM1),
	SpellInfo("SPELL_BYAKUREN_SKILL1",req_BYAKUREN_SKILL1,spell_BYAKUREN_SKILL1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_BYAKUREN_EXTRA1",req_BYAKUREN_EXTRA1,spell_BYAKUREN_EXTRA1),
	SpellInfo("SPELL_BYAKUREN_PHANTASM1",req_BYAKUREN_PHANTASM1,spell_BYAKUREN_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_NUE_EXTRA1",req_NUE_EXTRA1,spell_NUE_EXTRA1),
	SpellInfo("SPELL_NUE_PHANTASM1",req_NUE_PHANTASM1,spell_NUE_PHANTASM1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_YOSHIKA_EXTRA1",req_YOSHIKA_EXTRA1,spell_YOSHIKA_EXTRA1,tempIsAISpellCast,None,0.15,1,255),
	SpellInfo("SPELL_YOSHIKA_PHANTASM1",req_YOSHIKA_PHANTASM1,spell_YOSHIKA_PHANTASM1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_SEIGA_EXTRA1",req_SEIGA_EXTRA1,spell_SEIGA_EXTRA1),
	SpellInfo("SPELL_SEIGA_PHANTASM1",req_SEIGA_PHANTASM1,spell_SEIGA_PHANTASM1),
	SpellInfo("SPELL_TOJIKO_EXTRA1",req_TOJIKO_EXTRA1,spell_TOJIKO_EXTRA1),
	SpellInfo("SPELL_TOJIKO_PHANTASM1",req_TOJIKO_PHANTASM1,spell_TOJIKO_PHANTASM1),
	SpellInfo("SPELL_FUTO_EXTRA1",req_FUTO_EXTRA1,spell_FUTO_EXTRA1),
	SpellInfo("SPELL_FUTO_PHANTASM1",req_FUTO_PHANTASM1,spell_FUTO_PHANTASM1),
	SpellInfo("SPELL_MIMIMIKO_EXTRA1",req_MIMIMIKO_EXTRA1,spell_MIMIMIKO_EXTRA1),
	SpellInfo("SPELL_MIMIMIKO_PHANTASM1",req_MIMIMIKO_PHANTASM1,spell_MIMIMIKO_PHANTASM1),
	SpellInfo("SPELL_YATUHASHI_EXTRA1",req_YATUHASHI_EXTRA1,spell_YATUHASHI_EXTRA1),
	SpellInfo("SPELL_YATUHASHI_PHANTASM1",req_YATUHASHI_PHANTASM1,spell_YATUHASHI_PHANTASM1),
	SpellInfo("SPELL_BENBEN_EXTRA1",req_BENBEN_EXTRA1,spell_BENBEN_EXTRA1),
	SpellInfo("SPELL_BENBEN_PHANTASM1",req_BENBEN_PHANTASM1,spell_BENBEN_PHANTASM1),
	SpellInfo("SPELL_SEIJA_EXTRA1",req_SEIJA_EXTRA1,spell_SEIJA_EXTRA1,tempIsAISpellCast,None,0.10,1,255),
	SpellInfo("SPELL_SEIJA_PHANTASM1",req_SEIJA_PHANTASM1,spell_SEIJA_PHANTASM1),
	SpellInfo("SPELL_SHINMYOUMARU_EXTRA1",req_SHINMYOUMARU_EXTRA1,spell_SHINMYOUMARU_EXTRA1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_SHINMYOUMARU_PHANTASM1",req_SHINMYOUMARU_PHANTASM1,spell_SHINMYOUMARU_PHANTASM1,tempIsAISpellCast,None,0.15,1,255),
	SpellInfo("SPELL_RAIKO_EXTRA1",req_RAIKO_EXTRA1,spell_RAIKO_EXTRA1,tempIsAISpellCast,None,0.15,1,255),
	SpellInfo("SPELL_RAIKO_PHANTASM1",req_RAIKO_PHANTASM1,spell_RAIKO_PHANTASM1),
	SpellInfo("SPELL_RAIKO_PHANTASM2",req_RAIKO_PHANTASM2,spell_RAIKO_PHANTASM2),
	SpellInfo("SPELL_YORIHIME_SKILL1",req_YORIHIME_SKILL1,spell_YORIHIME_SKILL1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_YORIHIME_EXTRA1",req_YORIHIME_EXTRA1,spell_YORIHIME_EXTRA1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_YORIHIME_EXTRA2",req_YORIHIME_EXTRA2,spell_YORIHIME_EXTRA2,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_YORIHIME_EXTRA3",req_YORIHIME_EXTRA3,spell_YORIHIME_EXTRA3,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_YORIHIME_PHANTASM1",req_YORIHIME_PHANTASM1,spell_YORIHIME_PHANTASM1,tempIsAISpellCast,help_YORIHIME_PHANTASM1,0.50,1,255),
	SpellInfo("SPELL_YORIHIME_PHANTASM2",req_YORIHIME_PHANTASM2,spell_YORIHIME_PHANTASM2),
	SpellInfo("SPELL_YORIHIME_PHANTASM3",req_YORIHIME_PHANTASM3,spell_YORIHIME_PHANTASM3,tempIsAISpellCast,help_YORIHIME_PHANTASM3,0.50,1,255),
	SpellInfo("SPELL_TOYOHIME_EXTRA1",req_TOYOHIME_EXTRA1,spell_TOYOHIME_EXTRA1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_TOYOHIME_EXTRA2",req_TOYOHIME_EXTRA2,spell_TOYOHIME_EXTRA2),
	SpellInfo("SPELL_TOYOHIME_SKILL1",req_TOYOHIME_SKILL1,spell_TOYOHIME_SKILL1),
	SpellInfo("SPELL_TOYOHIME_PHANTASM1",req_TOYOHIME_PHANTASM1,spell_TOYOHIME_PHANTASM1),
	SpellInfo("SPELL_SEIRAN_EXTRA1",req_SEIRAN_EXTRA1,spell_SEIRAN_EXTRA1,tempIsAISpellCast,help_SEIRAN_EXTRA1,0.10,1,255),
	SpellInfo("SPELL_SEIRAN_PHANTASM1",req_SEIRAN_PHANTASM1,spell_SEIRAN_PHANTASM1,tempIsAISpellCast,None,0.30,1,255),
	SpellInfo("SPELL_RINGO_EXTRA1",req_RINGO_EXTRA1,spell_RINGO_EXTRA1,tempIsAISpellCast,None,0.15,1,255),
	SpellInfo("SPELL_RINGO_PHANTASM1",req_RINGO_PHANTASM1,spell_RINGO_PHANTASM1,tempIsAISpellCast,None,0.50,1,255),
	SpellInfo("SPELL_DOREMY_EXTRA1",req_DOREMY_EXTRA1,spell_DOREMY_EXTRA1),
	SpellInfo("SPELL_DOREMY_PHANTASM1",req_DOREMY_PHANTASM1,spell_DOREMY_PHANTASM1),
	SpellInfo("SPELL_SAGUME_EXTRA1",req_SAGUME_EXTRA1,spell_SAGUME_EXTRA1,tempIsAISpellCast,help_SAGUME_EXTRA1,0.15,1,255),
	SpellInfo("SPELL_SAGUME_PHANTASM1",req_SAGUME_PHANTASM1,spell_SAGUME_PHANTASM1),
	
	SpellInfo("SPELL_GET_HOURAINOKUSURI_EASY",req_GET_HOURAINOKUSURI_EASY,spell_GET_HOURAINOKUSURI_EASY,spell_GET_HOURAINOKUSURI_Estimate),#              以下アイテム
	SpellInfo("SPELL_GET_HOURAINOKUSURI_NORMAL",req_GET_HOURAINOKUSURI_NORMAL,spell_GET_HOURAINOKUSURI_NORMAL,spell_GET_HOURAINOKUSURI_Estimate),#        統合追記：その他雑多スペルも含む
	SpellInfo("SPELL_GET_HOURAINOKUSURI_HARD",req_GET_HOURAINOKUSURI_HARD,spell_GET_HOURAINOKUSURI_HARD,spell_GET_HOURAINOKUSURI_Estimate),
	SpellInfo("SPELL_GET_HOURAINOKUSURI_LUNATIC",req_GET_HOURAINOKUSURI_LUNATIC,spell_GET_HOURAINOKUSURI_LUNATIC,spell_GET_HOURAINOKUSURI_Estimate),
	SpellInfo("SPELL_GET_MYSTERYIUM",req_GET_MYSTERYIUM,spell_GET_MYSTERYIUM),
	SpellInfo("SPELL_GET_GREATE_PERSON",req_GET_GREATE_PERSON,spell_GET_GREATE_PERSON),
	SpellInfo("SPELL_BUILD_MEIRENJI",req_BUILD_MEIRENJI,spell_BUILD_MEIRENJI),
	SpellInfo("SPELL_POWERUP_COMBAT",req_POWERUP_COMBAT,spell_POWERUP_COMBAT),
	SpellInfo("SPELL_POWERUP_STG",req_POWERUP_STG,spell_POWERUP_STG),
	SpellInfo("SPELL_POWERUP_CAL",req_POWERUP_CAL,spell_POWERUP_CAL),
	SpellInfo("SPELL_SPECIAL_TAMEUTI",req_SPECIAL_TAMEUTI,spell_SPECIAL_TAMEUTI),#以下特殊スペル系列
	SpellInfo("SPELL_SPECIAL_HIGHSPEEDMOVE",req_SPECIAL_HIGHSPEEDMOVE,spell_SPECIAL_HIGHSPEEDMOVE),
	SpellInfo("SPELL_SPECIAL_AURIC",req_SPECIAL_AURIC,spell_SPECIAL_AURIC),
	SpellInfo("SPELL_SPECIAL_HALLOWEEN_FEVER",req_SPECIAL_HALLOWEEN_FEVER,spell_SPECIAL_HALLOWEEN_FEVER),
	SpellInfo("SPELL_SPECIAL_DANGO_FEVER",req_SPECIAL_DANGO_FEVER,spell_SPECIAL_DANGO_FEVER),
	SpellInfo("SPELL_SPECIAL_TANTIGATA_KIRAI_1_1",req_SPECIAL_TANTIGATA_KIRAI_1_1,spell_SPECIAL_TANTIGATA_KIRAI_1_1),
	SpellInfo("SPELL_SPECIAL_TANTIGATA_KIRAI_1_2",req_SPECIAL_TANTIGATA_KIRAI_1_2,spell_SPECIAL_TANTIGATA_KIRAI_1_2),
	SpellInfo("SPELL_SPECIAL_TANTIGATA_KIRAI_2",req_SPECIAL_TANTIGATA_KIRAI_2,spell_SPECIAL_TANTIGATA_KIRAI_2),
	SpellInfo("SPELL_SPECIAL_TANTIGATA_KIRAI_3",req_SPECIAL_TANTIGATA_KIRAI_3,spell_SPECIAL_TANTIGATA_KIRAI_3),
	SpellInfo("SPELL_SPECIAL_JIBAKU",req_SPECIAL_JIBAKU,spell_SPECIAL_JIBAKU),
	SpellInfo("SPELL_TERRAFORM_PLAIN",req_TERRAFORM_PLAIN,spell_TERRAFORM_PLAIN,spell_TERRAFORM_PLAIN_Estimate), #以下テラフォーミング系
	SpellInfo("SPELL_TERRAFORM_PLAIN_NO_SACRIFICE",req_TERRAFORM_PLAIN_NO_SACRIFICE,spell_TERRAFORM_PLAIN_NO_SACRIFICE,spell_TERRAFORM_PLAIN_Estimate),
	SpellInfo("SPELL_TERRAFORM_GRASS",req_TERRAFORM_GRASS,spell_TERRAFORM_GRASS,spell_TERRAFORM_GRASS_Estimate),
	SpellInfo("SPELL_TERRAFORM_GRASS_NO_SACRIFICE",req_TERRAFORM_GRASS_NO_SACRIFICE,spell_TERRAFORM_GRASS_NO_SACRIFICE,spell_TERRAFORM_GRASS_Estimate),
	SpellInfo("SPELL_TERRAFORM_HILL",req_TERRAFORM_HILL,spell_TERRAFORM_HILL),
	SpellInfo("SPELL_TERRAFORM_HILL_NO_SACRIFICE",req_TERRAFORM_HILL_NO_SACRIFICE,spell_TERRAFORM_HILL_NO_SACRIFICE),
	SpellInfo("SPELL_TERRAFORM_FLATLAND",req_TERRAFORM_FLATLAND,spell_TERRAFORM_FLATLAND),
	SpellInfo("SPELL_TERRAFORM_FLATLAND_NO_SACRIFICE",req_TERRAFORM_FLATLAND_NO_SACRIFICE,spell_TERRAFORM_FLATLAND_NO_SACRIFICE),
	SpellInfo("SPELL_TERRAFORM_FOREST",req_TERRAFORM_FOREST,spell_TERRAFORM_FOREST),
	SpellInfo("SPELL_TERRAFORM_LANDFILL",req_TERRAFORM_LANDFILL,spell_TERRAFORM_LANDFILL),
	SpellInfo("SPELL_TERRAFORM_CRUSHICE",req_TERRAFORM_CRUSHICE,spell_TERRAFORM_CRUSHICE),
	SpellInfo("SPELL_TERRAFORM_OCEANIZATION",req_TERRAFORM_OCEANIZATION,spell_TERRAFORM_OCEANIZATION),
	SpellInfo("SPELL_TERRAFORM_FLOOD",req_TERRAFORM_FLOOD,spell_TERRAFORM_FLOOD),
	
	SpellInfo("SPELL_NINGENNOSATO1",req_NINGENNOSATO1,spell_NINGENNOSATO1), #以下・世界魔法
	SpellInfo("SPELL_HYOUSEIRENGOU1",req_HYOUSEIRENGOU1,spell_HYOUSEIRENGOU1), 
	SpellInfo("SPELL_KISHINJOU1",req_KISHINJOU1,spell_KISHINJOU1), 
	
	]
	
	
	CvGameUtils.doprint('SpellInfo Init success!')
	ActionNumber = spells[0].getActionNumber()
	CvGameUtils.doprint('ActionNumber:%i' %ActionNumber)
	#CvGameUtils.doprint("for %s" %str(gc.getAutomateInfo(ActionNumber)))

def init():
	global spells
	if not spells:
		init_force()

def getSpellFromAction(action):
	return spellAction.get(action)

def getSpells():
	return spells


# for 統合叙事詩 17.06
# Civilopedia用UNIT KeyとSPELL KeyとHELP Keyの対応付けリスト
# CvPediaTohoUnit.pyからおひっこし
# AutomateInfos.xmlに書いてるので重複だが、ゲーム中しかAutomateInfosを参照できないので
# ぺでぃあからの参照用にやむなく別に置くしかない
### すごく悩んだけど、結局SP・EX・PHの表記法を統一。
### 括弧がさらに増え、文字数がすごいことに。読み辛さ三倍増。編集し辛さ五倍増。つらたん。
### TohoUnitList.py に置いてあるほうが違和感がない気もする。機能的にはどっちでもまったく変わらないので作者様の判断待ち。
TohoUnitSpellHelpList = [
	[ 'UNIT_SANAE1' , [
		[ [1,3,'SPELLCARD_SANAE1_1',
		   'TXT_KEY_SPELLCARD_SANAE1_1',
		   'TXT_KEY_SPELLCARD_SANAE1_1_HELP'],
		  [4,7,'SPELLCARD_SANAE1_1',
		   'TXT_KEY_SPELLCARD_SANAE1_1',
		   'TXT_KEY_SPELLCARD_SANAE1_2_HELP'],
		  [8,11,'SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_3_HELP'],
		  [12,15,'SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_4_HELP'],
		  [16,19,'SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_5_HELP'],
		  [20,23,'SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_6_HELP'],
		  [24,255,'SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_2',
		   'TXT_KEY_SPELLCARD_SANAE1_7_HELP'],],
		[ [1,255,'SPELL_SANAE_EXTRA1',
		   'TXT_KEY_SPELL_SANAE_EXTRA1',
		   'TXT_KEY_SPELL_SANAE_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SANAE_PHANTASM1',
		   'TXT_KEY_SPELL_SANAE_PHANTASM1',
		   'TXT_KEY_SPELL_SANAE_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_REMILIA1' , [
		[ [1,7,'SPELLCARD_REMILIA1_1',
		   'TXT_KEY_SPELLCARD_REMILIA1_1',
		   'TXT_KEY_SPELLCARD_REMILIA1_1_HELP'],
		  [8,255,'SPELLCARD_REMILIA1_2',
		   'TXT_KEY_SPELLCARD_REMILIA1_2',
		   'TXT_KEY_SPELLCARD_REMILIA1_1_HELP'], ],
		[ [1,255,'SPELL_REMILIA_EXTRA1',
		   'TXT_KEY_SPELL_REMILIA_EXTRA1',
		   'TXT_KEY_SPELL_REMILIA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_REMILIA_PHANTASM1',
		   'TXT_KEY_SPELL_REMILIA_PHANTASM1',
		   'TXT_KEY_SPELL_REMILIA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_CHEN1' , [
		[ [1,3,'SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_1_HELP'],
		  [4,7,'SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_2_HELP'],
		  [8,11,'SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_3_HELP'],
		  [12,15,'SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_4_HELP'],
		  [16,19,'SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_5_HELP'],
		  [20,255,'SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_1',
		   'TXT_KEY_SPELLCARD_CHEN1_6_HELP'], ],
		[ [1,255,'SPELL_CHEN_EXTRA1',
		   'TXT_KEY_SPELL_CHEN_EXTRA1',
		   'TXT_KEY_SPELL_CHEN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_CHEN_PHANTASM1',
		   'TXT_KEY_SPELL_CHEN_PHANTASM1',
		   'TXT_KEY_SPELL_CHEN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_WRIGGLE1' , [
		[ [1,7,'SPELLCARD_WRIGGLE1_1',
		   'TXT_KEY_SPELLCARD_WRIGGLE1_1',
		   'TXT_KEY_SPELLCARD_WRIGGLE1_1_HELP'],
		  [8,255,'SPELLCARD_WRIGGLE1_2',
		   'TXT_KEY_SPELLCARD_WRIGGLE1_2',
		   'TXT_KEY_SPELLCARD_WRIGGLE1_1_HELP'], ],
		[ [1,255,'SPELL_WRIGGLE_EXTRA1',
		   'TXT_KEY_SPELL_WRIGGLE_EXTRA1',
		   'TXT_KEY_SPELL_WRIGGLE_EXTRA1_HELP',],],
		[ [1,255,'SPELL_WRIGGLE_PHANTASM1',
		   'TXT_KEY_SPELL_WRIGGLE_PHANTASM1',
		   'TXT_KEY_SPELL_WRIGGLE_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_TEWI1' , [
		[ [1,3,'SPELLCARD_TEWI1_1',
		   'TXT_KEY_SPELLCARD_TEWI1_1',
		   'TXT_KEY_SPELLCARD_TEWI1_1_HELP'],
		  [4,7,'SPELLCARD_TEWI1_1',
		   'TXT_KEY_SPELLCARD_TEWI1_1',
		   'TXT_KEY_SPELLCARD_TEWI1_2_HELP'],
		  [8,11,'SPELLCARD_TEWI1_1',
		   'TXT_KEY_SPELLCARD_TEWI1_1',
		   'TXT_KEY_SPELLCARD_TEWI1_3_HELP'],
		  [12,255,'SPELLCARD_TEWI1_2',
		   'TXT_KEY_SPELLCARD_TEWI1_2',
		   'TXT_KEY_SPELLCARD_TEWI1_4_HELP'], ],
		[ [1,255,'SPELL_TEWI_EXTRA1',
		   'TXT_KEY_SPELL_TEWI_EXTRA1',
		   'TXT_KEY_SPELL_TEWI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_TEWI_PHANTASM1',
		   'TXT_KEY_SPELL_TEWI_PHANTASM1',
		   'TXT_KEY_SPELL_TEWI_PHANTASM1_HELP',],
		  [1,255,'SPELL_TEWI_PHANTASM2',
		   'TXT_KEY_SPELL_TEWI_PHANTASM2',
		   'TXT_KEY_SPELL_TEWI_PHANTASM2_HELP',],], ], ],
	[ 'UNIT_NITORI1' , [
		[ [1,3,'SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_1_HELP'],
		  [4,7,'SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_2_HELP'],
		  [8,11,'SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_3_HELP'],
		  [12,255,'SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_1',
		   'TXT_KEY_SPELLCARD_NITORI1_4_HELP'], ],
		[ [1,255,'SPELL_NITORI_EXTRA1',
		   'TXT_KEY_SPELL_NITORI_EXTRA1',
		   'TXT_KEY_SPELL_NITORI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_NITORI_PHANTASM1',
		   'TXT_KEY_SPELL_NITORI_PHANTASM1',
		   'TXT_KEY_SPELL_NITORI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MARISA1' , [
		[ [1,7,'SPELLCARD_MARISA1_1',
		   'TXT_KEY_SPELLCARD_MARISA1_1',
		   'TXT_KEY_SPELLCARD_MARISA1_1_HELP'],
		  [8,255,'SPELLCARD_MARISA1_1',
		   'TXT_KEY_SPELLCARD_MARISA1_1',
		   'TXT_KEY_SPELLCARD_MARISA1_2_HELP'], ],
		[ [1,255,'SPELL_MARISA_EXTRA1',
		   'TXT_KEY_SPELL_MARISA_EXTRA1',
		   'TXT_KEY_SPELL_MARISA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_MARISA_PHANTASM1',
		   'TXT_KEY_SPELL_MARISA_PHANTASM1',
		   'TXT_KEY_SPELL_MARISA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_FLAN1' , [
		[ [1,3,'SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1_HELP'],
		  [4,7,'SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_2_HELP'],
		  [8,11,'SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_3_HELP'],
		  [12,15,'SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_4_HELP'],
		  [16,19,'SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_5_HELP'],
		  [20,23,'SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_6_HELP'],
		  [24,255,'SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_1',
		   'TXT_KEY_SPELLCARD_FLAN1_7_HELP'], ],
		[ [1,255,'SPELL_FLAN_EXTRA1',
		   'TXT_KEY_SPELL_FLAN_EXTRA1',
		   'TXT_KEY_SPELL_FLAN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_FLAN_PHANTASM1',
		   'TXT_KEY_SPELL_FLAN_PHANTASM1',
		   'TXT_KEY_SPELL_FLAN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_YOUMU1' , [
		[ [1,7,'SPELLCARD_YOUMU1_1',
		   'TXT_KEY_SPELLCARD_YOUMU1_1',
		   'TXT_KEY_SPELLCARD_YOUMU1_1_HELP'],
		  [8,11,'SPELLCARD_YOUMU1_2',
		   'TXT_KEY_SPELLCARD_YOUMU1_2',
		   'TXT_KEY_SPELLCARD_YOUMU1_1_HELP'],
		  [12,255,'SPELLCARD_YOUMU1_2',
		   'TXT_KEY_SPELLCARD_YOUMU1_2',
		   'TXT_KEY_SPELLCARD_YOUMU1_2_HELP'], ],
		[ [1,255,'SPELL_YOUMU_EXTRA1',
		   'TXT_KEY_SPELL_YOUMU_EXTRA1',
		   'TXT_KEY_SPELL_YOUMU_EXTRA1_HELP',],],
		[ [1,255,'SPELL_YOUMU_PHANTASM1',
		   'TXT_KEY_SPELL_YOUMU_PHANTASM1',
		   'TXT_KEY_SPELL_YOUMU_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_CIRNO1' , [
		[ [1,3,'SPELLCARD_CIRNO1_1',
		   'TXT_KEY_SPELLCARD_CIRNO1_1',
		   'TXT_KEY_SPELLCARD_CIRNO1_1_HELP'],
		  [4,255,'SPELLCARD_CIRNO1_2',
		   'TXT_KEY_SPELLCARD_CIRNO1_2',
		   'TXT_KEY_SPELLCARD_CIRNO1_2_HELP'], ],
		[ [1,255,'SPELL_CIRNO_EXTRA1',
		   'TXT_KEY_SPELL_CIRNO_EXTRA1',
		   'TXT_KEY_SPELL_CIRNO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_CIRNO_PHANTASM1',
		   'TXT_KEY_SPELL_CIRNO_PHANTASM1',
		   'TXT_KEY_SPELL_CIRNO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_EIRIN1' , [
		[ [1,3,'SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_1_HELP'],
		  [4,7,'SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_2_HELP'],
		  [8,11,'SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_3_HELP'],
		  [12,255,'SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_1',
		   'TXT_KEY_SPELLCARD_EIRIN1_4_HELP'], ],
		[ [1,255,'SPELL_EIRIN_EXTRA1',
		   'TXT_KEY_SPELL_EIRIN_EXTRA1',
		   'TXT_KEY_SPELL_EIRIN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_EIRIN_PHANTASM1',
		   'TXT_KEY_SPELL_EIRIN_PHANTASM1',
		   'TXT_KEY_SPELL_EIRIN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SUWAKO1' , [
		[ [1,255,'SPELLCARD_SUWAKO1_1',
		   'TXT_KEY_SPELLCARD_SUWAKO1_1',
		   'TXT_KEY_SPELLCARD_SUWAKO1_1_HELP'], ],
		[ [1,255,'SPELL_SUWAKO_EXTRA1',
		   'TXT_KEY_SPELL_SUWAKO_EXTRA1',
		   'TXT_KEY_SPELL_SUWAKO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SUWAKO_PHANTASM1',
		   'TXT_KEY_SPELL_SUWAKO_PHANTASM1',
		   'TXT_KEY_SPELL_SUWAKO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_ALICE1' , [
		[ [1,3,'SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_1_HELP'],
		  [4,7,'SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_2_HELP'],
		  [8,11,'SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_3_HELP'],
		  [12,15,'SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_4_HELP'],
		  [16,19,'SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_5_HELP'],
		  [20,255,'SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_1',
		   'TXT_KEY_SPELLCARD_ALICE1_6_HELP'], ],
		[ [1,255,'SPELL_ALICE_EXTRA1',
		   'TXT_KEY_SPELL_ALICE_EXTRA1',
		   'TXT_KEY_SPELL_ALICE_EXTRA1_HELP',],],
		[ [1,255,'SPELL_ALICE_PHANTASM1',
		   'TXT_KEY_SPELL_ALICE_PHANTASM1',
		   'TXT_KEY_SPELL_ALICE_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MOKOU1' , [
		[ [1,255,'SPELLCARD_MOKOU1_1',
		   'TXT_KEY_SPELLCARD_MOKOU1_1',
		   'TXT_KEY_SPELLCARD_MOKOU1_1_HELP'], ],
		[ ['SPELL_MOKOU_EXTRA1',
		   'TXT_KEY_SPELL_MOKOU_EXTRA1',
		   'TXT_KEY_SPELL_MOKOU_EXTRA1_HELP',],],
		[ ['SPELL_MOKOU_PHANTASM1',
		   'TXT_KEY_SPELL_MOKOU_PHANTASM1',
		   'TXT_KEY_SPELL_MOKOU_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_KEINE1' , [
		[ [1,3,'SPELLCARD_KEINE1_1',
		   'TXT_KEY_SPELLCARD_KEINE1_1',
		   'TXT_KEY_SPELLCARD_KEINE1_1_HELP'],
		  [4,7,'SPELLCARD_KEINE1_1',
		   'TXT_KEY_SPELLCARD_KEINE1_1',
		   'TXT_KEY_SPELLCARD_KEINE1_2_HELP'],
		  [8,11,'SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_3_HELP'],
		  [12,15,'SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_4_HELP'],
		  [16,19,'SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_5_HELP'],
		  [20,255,'SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_2',
		   'TXT_KEY_SPELLCARD_KEINE1_6_HELP'], ],
		[ [1,255,'SPELL_KEINE_EXTRA1',
		   'TXT_KEY_SPELL_KEINE_EXTRA1',
		   'TXT_KEY_SPELL_KEINE_EXTRA1_HELP',],],
		[ [1,255,'SPELL_KEINE_PHANTASM1',
		   'TXT_KEY_SPELL_KEINE_PHANTASM1',
		   'TXT_KEY_SPELL_KEINE_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_PARSEE1' , [
		[ [1,7,'SPELLCARD_PARSEE1_1',
		   'TXT_KEY_SPELLCARD_PARSEE1_1',
		   'TXT_KEY_SPELLCARD_PARSEE1_1_HELP'],
		  [8,255,'SPELLCARD_PARSEE1_2',
		   'TXT_KEY_SPELLCARD_PARSEE1_2',
		   'TXT_KEY_SPELLCARD_PARSEE1_1_HELP'], ],
		[ [1,255,'SPELL_PARSEE_EXTRA1',
		   'TXT_KEY_SPELL_PARSEE_EXTRA1',
		   'TXT_KEY_SPELL_PARSEE_EXTRA1_HELP',],],
		[ [1,255,'SPELL_PARSEE_PHANTASM1',
		   'TXT_KEY_SPELL_PARSEE_PHANTASM1',
		   'TXT_KEY_SPELL_PARSEE_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_YUGI1' , [
		[ [1,255,'SPELLCARD_YUGI1_1',
		   'TXT_KEY_SPELLCARD_YUGI1_1',
		   'TXT_KEY_SPELLCARD_YUGI1_1_HELP'], ],
		[ [1,255,'SPELL_YUGI_EXTRA1',
		   'TXT_KEY_SPELL_YUGI_EXTRA1',
		   'TXT_KEY_SPELL_YUGI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_YUGI_PHANTASM1',
		   'TXT_KEY_SPELL_YUGI_PHANTASM1',
		   'TXT_KEY_SPELL_YUGI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_HAKUTAKUKEINE1' , [
		[ [1,255,'SPELLCARD_HAKUTAKUKEINE1_1',
		   'TXT_KEY_SPELLCARD_HAKUTAKUKEINE1_1',
		   'TXT_KEY_SPELLCARD_HAKUTAKUKEINE1_1_HELP'], ],
		[ [1,255,'SPELL_HAKUTAKUKEINE_EXTRA1',
		   'TXT_KEY_SPELL_HAKUTAKUKEINE_EXTRA1',
		   'TXT_KEY_SPELL_HAKUTAKUKEINE_EXTRA1_HELP',],],
		[ [1,255,'SPELL_HAKUTAKUKEINE_PHANTASM1',
		   'TXT_KEY_SPELL_HAKUTAKUKEINE_PHANTASM1',
		   'TXT_KEY_SPELL_HAKUTAKUKEINE_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SAKUYA1' , [
		[ [1,6,'SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_1_HELP'],
		  [7,11,'SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_2_HELP'],
		  [12,15,'SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_3_HELP'],
		  [16,255,'SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_1',
		   'TXT_KEY_SPELLCARD_SAKUYA1_4_HELP'], ],
		[ [1,255,'SPELL_SAKUYA_EXTRA1',
		   'TXT_KEY_SPELL_SAKUYA_EXTRA1',
		   'TXT_KEY_SPELL_SAKUYA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SAKUYA_PHANTASM1',
		   'TXT_KEY_SPELL_SAKUYA_PHANTASM1',
		   'TXT_KEY_SPELL_SAKUYA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_YUYUKO1' , [
		[ [1,3,'SPELLCARD_YUYUKO1_1',
		   'TXT_KEY_SPELLCARD_YUYUKO1_1',
		   'TXT_KEY_SPELLCARD_YUYUKO1_1_HELP'],
		  [4,7,'SPELLCARD_YUYUKO1_2',
		   'TXT_KEY_SPELLCARD_YUYUKO1_2',
		   'TXT_KEY_SPELLCARD_YUYUKO1_1_HELP'],
		  [8,11,'SPELLCARD_YUYUKO1_3',
		   'TXT_KEY_SPELLCARD_YUYUKO1_3',
		   'TXT_KEY_SPELLCARD_YUYUKO1_1_HELP'],
		  [12,255,'SPELLCARD_YUYUKO1_4',
		   'TXT_KEY_SPELLCARD_YUYUKO1_4',
		   'TXT_KEY_SPELLCARD_YUYUKO1_1_HELP'], ],
		[ [1,255,'SPELL_YUYUKO_EXTRA1',
		   'TXT_KEY_SPELL_YUYUKO_EXTRA1',
		   'TXT_KEY_SPELL_YUYUKO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_YUYUKO_PHANTASM1',
		   'TXT_KEY_SPELL_YUYUKO_PHANTASM1',
		   'TXT_KEY_SPELL_YUYUKO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_RUMIA1' , [
		[ [1,255,'SPELLCARD_RUMIA1_1',
		   'TXT_KEY_SPELLCARD_RUMIA1_1',
		   'TXT_KEY_SPELLCARD_RUMIA1_1_HELP'], ],
		[ [1,255,'SPELL_RUMIA_EXTRA1',
		   'TXT_KEY_SPELL_RUMIA_EXTRA1',
		   'TXT_KEY_SPELL_RUMIA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_RUMIA_PHANTASM1',
		   'TXT_KEY_SPELL_RUMIA_PHANTASM1',
		   'TXT_KEY_SPELL_RUMIA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MEDICIN1' , [
		[ [1,3,'SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_1_HELP'],
		  [4,7,'SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_2_HELP'],
		  [8,11,'SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_3_HELP'],
		  [12,255,'SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_4_HELP'], ],
		[ [1,255,'SPELL_MEDICIN_EXTRA1',
		   'TXT_KEY_SPELL_MEDICIN_EXTRA1',
		   'TXT_KEY_SPELL_MEDICIN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_MEDICIN_PHANTASM1',
		   'TXT_KEY_SPELL_MEDICIN_PHANTASM1',
		   'TXT_KEY_SPELL_MEDICIN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_KANAKO1' , [
		[ [1,7,'SPELLCARD_KANAKO1_1',
		   'TXT_KEY_SPELLCARD_KANAKO1_1',
		   'TXT_KEY_SPELLCARD_KANAKO1_1_HELP'],
		  [8,255,'SPELLCARD_KANAKO1_2',
		   'TXT_KEY_SPELLCARD_KANAKO1_2',
		   'TXT_KEY_SPELLCARD_KANAKO1_1_HELP'], ],
		[ [1,255,'SPELL_KANAKO_EXTRA1',
		   'TXT_KEY_SPELL_KANAKO_EXTRA1',
		   'TXT_KEY_SPELL_KANAKO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_KANAKO_PHANTASM1',
		   'TXT_KEY_SPELL_KANAKO_PHANTASM1',
		   'TXT_KEY_SPELL_KANAKO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_REIMU1' , [
		[ [1,255,'SPELLCARD_REIMU1_1',
		   'TXT_KEY_SPELLCARD_REIMU1_1',
		   'TXT_KEY_SPELLCARD_REIMU1_1_HELP'], ],
		[ [1,255,'SPELL_REIMU_EXTRA1',
		   'TXT_KEY_SPELL_REIMU_EXTRA1',
		   'TXT_KEY_SPELL_REIMU_EXTRA1_HELP',],],
		[ [1,255,'SPELL_REIMU_PHANTASM1',
		   'TXT_KEY_SPELL_REIMU_PHANTASM1',
		   'TXT_KEY_SPELL_REIMU_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_YUKA1' , [
		[ [1,255,'SPELLCARD_YUKA1_1',
		   'TXT_KEY_SPELLCARD_YUKA1_1',
		   'TXT_KEY_SPELLCARD_YUKA1_1_HELP'], ],
		[ [1,255,'SPELL_YUKA_EXTRA1',
		   'TXT_KEY_SPELL_YUKA_EXTRA1',
		   'TXT_KEY_SPELL_YUKA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_YUKA_PHANTASM1',
		   'TXT_KEY_SPELL_YUKA_PHANTASM1',
		   'TXT_KEY_SPELL_YUKA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_KOISHI1' , [
		[ [1,255,'SPELLCARD_KOISHI1_1',
		   'TXT_KEY_SPELLCARD_KOISHI1_1',
		   'TXT_KEY_SPELLCARD_KOISHI1_1_HELP'], ],
		[ [1,255,'SPELL_KOISHI_EXTRA1',
		   'TXT_KEY_SPELL_KOISHI_EXTRA1',
		   'TXT_KEY_SPELL_KOISHI_EXTRA1_HELP',],
		  [1,255,'SPELL_KOISHI_SKILL1',
		   'TXT_KEY_SPELL_KOISHI_SKILL1',
		   'TXT_KEY_SPELL_KOISHI_SKILL1_HELP',], ],
		[ [1,255,'SPELL_KOISHI_PHANTASM1',
		   'TXT_KEY_SPELL_KOISHI_PHANTASM1',
		   'TXT_KEY_SPELL_KOISHI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_KOISHI_FADE1' , [
		[    ],
		[ [1,255,'SPELL_KOISHI_EXTRA1',
		   'TXT_KEY_SPELL_KOISHI_EXTRA1',
		   'TXT_KEY_SPELL_KOISHI_EXTRA1_HELP',],
		  [1,255,'SPELL_KOISHI_SKILL2',
		   'TXT_KEY_SPELL_KOISHI_SKILL2',
		   'TXT_KEY_SPELL_KOISHI_SKILL2_HELP',], ],
		[ [1,255,'SPELL_KOISHI_PHANTASM1',
		   'TXT_KEY_SPELL_KOISHI_PHANTASM1',
		   'TXT_KEY_SPELL_KOISHI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_PATCHOULI1' ,[
		[ [1,255,'SPELLCARD_PATCHOULI1_1',
		   'TXT_KEY_SPELLCARD_PATCHOULI1_1',
		   'TXT_KEY_SPELLCARD_PATCHOULI1_1_HELP'],
		  [1,255,'SPELLCARD_PATCHOULI2_1',
		   'TXT_KEY_SPELLCARD_PATCHOULI2_1',
		   'TXT_KEY_SPELLCARD_PATCHOULI2_1_HELP'], ],
		[ [1,255,'SPELL_PATCHOULI_EXTRA1',
		   'TXT_KEY_SPELL_PATCHOULI_EXTRA1',
		   'TXT_KEY_SPELL_PATCHOULI_EXTRA1_HELP',],
		  [1,255,'SPELL_PATCHOULI_EXTRA2',
		   'TXT_KEY_SPELL_PATCHOULI_EXTRA2',
		   'TXT_KEY_SPELL_PATCHOULI_EXTRA2_HELP',], ],
		[ [1,255,'SPELL_PATCHOULI_PHANTASM1',
		   'TXT_KEY_SPELL_PATCHOULI_PHANTASM1',
		   'TXT_KEY_SPELL_PATCHOULI_PHANTASM1_HELP',],
		  [1,255,'SPELL_PATCHOULI_PHANTASM2',
		   'TXT_KEY_SPELL_PATCHOULI_PHANTASM2',
		   'TXT_KEY_SPELL_PATCHOULI_PHANTASM2_HELP',],
		  [1,255,'SPELL_PATCHOULI_PHANTASM3',
		   'TXT_KEY_SPELL_PATCHOULI_PHANTASM3',
		   'TXT_KEY_SPELL_PATCHOULI_PHANTASM3_HELP',],], ], ],
	[ 'UNIT_RAN1' , [
		[ [1,3,'SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_1_HELP'],
		  [4,7,'SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_2_HELP'],
		  [8,11,'SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_3_HELP'],
		  [12,255,'SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_1',
		   'TXT_KEY_SPELLCARD_RAN1_4_HELP'], ],
		[ [1,255,'SPELL_RAN_EXTRA1',
		   'TXT_KEY_SPELL_RAN_EXTRA1',
		   'TXT_KEY_SPELL_RAN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_RAN_PHANTASM1',
		   'TXT_KEY_SPELL_RAN_PHANTASM1',
		   'TXT_KEY_SPELL_RAN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_REISEN1' , [
		[ [1,7,'SPELLCARD_REISEN1_1',
		   'TXT_KEY_SPELLCARD_REISEN1_1',
		   'TXT_KEY_SPELLCARD_REISEN1_1_HELP'],
		  [8,255,'SPELLCARD_REISEN1_2',
		   'TXT_KEY_SPELLCARD_REISEN1_2',
		   'TXT_KEY_SPELLCARD_REISEN1_1_HELP'], ],
		[ ['SPELL_REISEN_EXTRA1',
		   'TXT_KEY_SPELL_REISEN_EXTRA1',
		   'TXT_KEY_SPELL_REISEN_EXTRA1_HELP',],],
		[ ['SPELL_REISEN_PHANTASM1',
		   'TXT_KEY_SPELL_REISEN_PHANTASM1',
		   'TXT_KEY_SPELL_REISEN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_IKU1' , [
		[ [1,3,'SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_1_HELP'],
		  [4,7,'SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_2_HELP'],
		  [8,11,'SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_3_HELP'],
		  [12,255,'SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_1',
		   'TXT_KEY_SPELLCARD_IKU1_4_HELP'], ],
		[ [1,255,'SPELL_IKU_EXTRA1',
		   'TXT_KEY_SPELL_IKU_EXTRA1',
		   'TXT_KEY_SPELL_IKU_EXTRA1_HELP',],],
		[ [1,255,'SPELL_IKU_PHANTASM1',
		   'TXT_KEY_SPELL_IKU_PHANTASM1',
		   'TXT_KEY_SPELL_IKU_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SATORI1' , [
		[ [1,3,'SPELLCARD_SATORI1_1',
		   'TXT_KEY_SPELLCARD_SATORI1_1',
		   'TXT_KEY_SPELLCARD_SATORI1_1_HELP'],
		  [4,7,'SPELLCARD_SATORI1_1',
		   'TXT_KEY_SPELLCARD_SATORI1_1',
		   'TXT_KEY_SPELLCARD_SATORI1_2_HELP'],
		  [8,11,'SPELLCARD_SATORI1_2',
		   'TXT_KEY_SPELLCARD_SATORI1_2',
		   'TXT_KEY_SPELLCARD_SATORI1_3_HELP'],
		  [12,15,'SPELLCARD_SATORI1_2',
		   'TXT_KEY_SPELLCARD_SATORI1_2',
		   'TXT_KEY_SPELLCARD_SATORI1_4_HELP'],
		  [16,255,'SPELLCARD_SATORI1_2',
		   'TXT_KEY_SPELLCARD_SATORI1_2',
		   'TXT_KEY_SPELLCARD_SATORI1_5_HELP'], ],
		[ [1,255,'SPELL_SATORI_EXTRA1',
		   'TXT_KEY_SPELL_SATORI_EXTRA1',
		   'TXT_KEY_SPELL_SATORI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SATORI_PHANTASM1',
		   'TXT_KEY_SPELL_SATORI_PHANTASM1',
		   'TXT_KEY_SPELL_SATORI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MYSTIA1' , [
		[ [1,7,'SPELLCARD_MYSTIA1_1',
		   'TXT_KEY_SPELLCARD_MYSTIA1_1',
		   'TXT_KEY_SPELLCARD_MYSTIA1_1_HELP'],
		  [8,11,'SPELLCARD_MYSTIA1_2',
		   'TXT_KEY_SPELLCARD_MYSTIA1_2',
		   'TXT_KEY_SPELLCARD_MYSTIA1_1_HELP'],
		  [12,255,'SPELLCARD_MYSTIA1_2',
		   'TXT_KEY_SPELLCARD_MYSTIA1_2',
		   'TXT_KEY_SPELLCARD_MYSTIA1_2_HELP'], ],
		[ [1,255,'SPELL_MYSTIA_EXTRA1',
		   'TXT_KEY_SPELL_MYSTIA_EXTRA1',
		   'TXT_KEY_SPELL_MYSTIA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_MYSTIA_PHANTASM1',
		   'TXT_KEY_SPELL_MYSTIA_PHANTASM1',
		   'TXT_KEY_SPELL_MYSTIA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SUIKA1' , [
		[ [1,3,'SPELLCARD_SUIKA1_1',
		   'TXT_KEY_SPELLCARD_SUIKA1_1',
		   'TXT_KEY_SPELLCARD_SUIKA1_1_HELP'],
		  [4,7,'SPELLCARD_SUIKA1_1',
		   'TXT_KEY_SPELLCARD_SUIKA1_1',
		   'TXT_KEY_SPELLCARD_SUIKA1_2_HELP'],
		  [8,11,'SPELLCARD_SUIKA1_2',
		   'TXT_KEY_SPELLCARD_SUIKA1_2',
		   'TXT_KEY_SPELLCARD_SUIKA1_3_HELP'],
		  [12,255,'SPELLCARD_SUIKA1_2',
		   'TXT_KEY_SPELLCARD_SUIKA1_2',
		   'TXT_KEY_SPELLCARD_SUIKA1_4_HELP'], ],
		[ [1,255,'SPELL_SUIKA_EXTRA1',
		   'TXT_KEY_SPELL_SUIKA_EXTRA1',
		   'TXT_KEY_SPELL_SUIKA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SUIKA_PHANTASM1',
		   'TXT_KEY_SPELL_SUIKA_PHANTASM1',
		   'TXT_KEY_SPELL_SUIKA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SUIKA_BIG1' ,  [   [ ], [ ],  [ ],   ],   ],
	[ 'UNIT_SUIKA_SMALL1' , [    [  ], [ ],  [ ],   ],   ],
	[ 'UNIT_KOMACHI1' , [
		[ [1,255,'SPELLCARD_KOMACHI1_1',
		   'TXT_KEY_SPELLCARD_KOMACHI1_1',
		   'TXT_KEY_SPELLCARD_KOMACHI1_1_HELP'], ],
		[ [1,255,'SPELL_KOMACHI_EXTRA1',
		   'TXT_KEY_SPELL_KOMACHI_EXTRA1',
		   'TXT_KEY_SPELL_KOMACHI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_KOMACHI_PHANTASM1',
		   'TXT_KEY_SPELL_KOMACHI_PHANTASM1',
		   'TXT_KEY_SPELL_KOMACHI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MEDICINwithSU1' , [
		[ [1,3,'SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_1_HELP'],
		  [4,7,'SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_1',
		   'TXT_KEY_SPELLCARD_MEDICIN1_2_HELP'],
		  [8,11,'SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_3_HELP'],
		  [12,255,'SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_2',
		   'TXT_KEY_SPELLCARD_MEDICIN1_4_HELP'], ],
		[ ['SPELL_MEDICIN_EXTRA1',
		   'TXT_KEY_SPELL_MEDICIN_EXTRA1',
		   'TXT_KEY_SPELL_MEDICIN_EXTRA1_HELP',],],
		[ ['SPELL_MEDICIN_PHANTASM1',
		   'TXT_KEY_SPELL_MEDICIN_PHANTASM1',
		   'TXT_KEY_SPELL_MEDICIN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MEIRIN1' , [
		[ [1,7,'SPELLCARD_MEIRIN1_1',
		   'TXT_KEY_SPELLCARD_MEIRIN1_1',
		   'TXT_KEY_SPELLCARD_MEIRIN1_1_HELP'],
		  [8,255,'SPELLCARD_MEIRIN1_2',
		   'TXT_KEY_SPELLCARD_MEIRIN1_2',
		   'TXT_KEY_SPELLCARD_MEIRIN1_1_HELP'], ],
		[ [1,255,'SPELL_MEIRIN_EXTRA1',
		   'TXT_KEY_SPELL_MEIRIN_EXTRA1',
		   'TXT_KEY_SPELL_MEIRIN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_MEIRIN_PHANTASM1',
		   'TXT_KEY_SPELL_MEIRIN_PHANTASM1',
		   'TXT_KEY_SPELL_MEIRIN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_YUKARI1' , [
		[ [1,7,'SPELLCARD_YUKARI1_1',
		   'TXT_KEY_SPELLCARD_YUKARI1_1',
		   'TXT_KEY_SPELLCARD_YUKARI1_1_HELP'],
		  [8,255,'SPELLCARD_YUKARI1_2',
		   'TXT_KEY_SPELLCARD_YUKARI1_2',
		   'TXT_KEY_SPELLCARD_YUKARI1_1_HELP'], ],
		[ [1,255,'SPELL_YUKARI_EXTRA1',
		   'TXT_KEY_SPELL_YUKARI_EXTRA1',
		   'TXT_KEY_SPELL_YUKARI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_YUKARI_PHANTASM1',
		   'TXT_KEY_SPELL_YUKARI_PHANTASM1',
		   'TXT_KEY_SPELL_YUKARI_PHANTASM1_HELP',],
		  [1,255,'SPELL_YUKARI_PHANTASM2',
		   'TXT_KEY_SPELL_YUKARI_PHANTASM2',
		   'TXT_KEY_SPELL_YUKARI_PHANTASM2_HELP',],
		  [1,255,'SPELL_YUKARI_PHANTASM3',
		   'TXT_KEY_SPELL_YUKARI_PHANTASM3',
		   'TXT_KEY_SPELL_YUKARI_PHANTASM3_HELP',],], ], ],
	[ 'UNIT_KAGUYA1' , [
		[ [1,3,'SPELLCARD_KAGUYA1_1',
		   'TXT_KEY_SPELLCARD_KAGUYA1_1',
		   'TXT_KEY_SPELLCARD_KAGUYA1_1_HELP'],
		  [4,7,'SPELLCARD_KAGUYA1_2',
		   'TXT_KEY_SPELLCARD_KAGUYA1_2',
		   'TXT_KEY_SPELLCARD_KAGUYA1_1_HELP'],
		  [8,11,'SPELLCARD_KAGUYA1_3',
		   'TXT_KEY_SPELLCARD_KAGUYA1_3',
		   'TXT_KEY_SPELLCARD_KAGUYA1_1_HELP'],
		  [12,255,'SPELLCARD_KAGUYA1_4',
		   'TXT_KEY_SPELLCARD_KAGUYA1_4',
		   'TXT_KEY_SPELLCARD_KAGUYA1_1_HELP'], ],
		[ [1,255,'SPELL_KAGUYA_EXTRA1',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA1',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA1_HELP',],
		  [1,255,'SPELL_KAGUYA_EXTRA2',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA2',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA2_HELP',],
		  [1,255,'SPELL_KAGUYA_EXTRA3',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA3',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA3_HELP',],
		  [1,255,'SPELL_KAGUYA_EXTRA4',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA4',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA4_HELP',],
		  [1,255,'SPELL_KAGUYA_EXTRA5',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA5',
		   'TXT_KEY_SPELL_KAGUYA_EXTRA5_HELP',], ],
		[ [1,255,'SPELL_KAGUYA_PHANTASM1',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM1',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM1_HELP',],
		  [1,255,'SPELL_KAGUYA_PHANTASM2',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM2',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM2_HELP',],
		  [1,255,'SPELL_KAGUYA_PHANTASM3',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM3',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM3_HELP',],
		  [1,255,'SPELL_KAGUYA_PHANTASM4',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM4',
		   'TXT_KEY_SPELL_KAGUYA_PHANTASM4_HELP',], ], ], ],
	[ 'UNIT_TENSHI1' ,[
		[ [1,7,'SPELLCARD_TENSHI1_1',
		   'TXT_KEY_SPELLCARD_TENSHI1_1',
		   'TXT_KEY_SPELLCARD_TENSHI1_1_HELP'],
		  [8,11,'SPELLCARD_TENSHI1_2',
		   'TXT_KEY_SPELLCARD_TENSHI1_2',
		   'TXT_KEY_SPELLCARD_TENSHI1_1_HELP'],
		  [12,255,'SPELLCARD_TENSHI1_3',
		   'TXT_KEY_SPELLCARD_TENSHI1_3',
		   'TXT_KEY_SPELLCARD_TENSHI1_1_HELP'], ],
		[ [1,255,'SPELL_TENSHI_EXTRA1',
		   'TXT_KEY_SPELL_TENSHI_EXTRA1',
		   'TXT_KEY_SPELL_TENSHI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_TENSHI_PHANTASM1',
		   'TXT_KEY_SPELL_TENSHI_PHANTASM1',
		   'TXT_KEY_SPELL_TENSHI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_RIN1' ,[
		[ [1,7,'SPELLCARD_RIN1_1',
		   'TXT_KEY_SPELLCARD_RIN1_1',
		   'TXT_KEY_SPELLCARD_RIN1_1_HELP'],
		  [8,255,'SPELLCARD_RIN1_2',
		   'TXT_KEY_SPELLCARD_RIN1_2',
		   'TXT_KEY_SPELLCARD_RIN1_1_HELP'], ],
		[ [1,255,'SPELL_RIN_TO_CAT',
		   'TXT_KEY_SPELL_RIN_TO_CAT',
		   'TXT_KEY_SPELL_RIN_TO_CAT_HELP',],],
		[ [1,255,'SPELL_RIN_PHANTASM1',
		   'TXT_KEY_SPELL_RIN_PHANTASM1',
		   'TXT_KEY_SPELL_RIN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_RIN_CATMODE1' , [
		[    ],
		[ [1,255,'SPELL_RIN_TO_RIN',
		   'TXT_KEY_SPELL_RIN_TO_RIN',
		   'TXT_KEY_SPELL_RIN_TO_RIN_HELP',],],
		[ ],   ],   ],
	[ 'UNIT_LETTY1' , [
		[ [1,255,'SPELLCARD_LETTY1_1',
		   'TXT_KEY_SPELLCARD_LETTY1_1',
		   'TXT_KEY_SPELLCARD_LETTY1_1_HELP'], ],
		[ [1,255,'SPELL_LETTY_EXTRA1',
		   'TXT_KEY_SPELL_LETTY_EXTRA1',
		   'TXT_KEY_SPELL_LETTY_EXTRA1_HELP',],],
		[ [1,255,'SPELL_LETTY_PHANTASM1',
		   'TXT_KEY_SPELL_LETTY_PHANTASM1',
		   'TXT_KEY_SPELL_LETTY_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MIMA1' , [
		[ [1,255,'SPELLCARD_MIMA1_1',
		   'TXT_KEY_SPELLCARD_MIMA1_1',
		   'TXT_KEY_SPELLCARD_MIMA1_1_HELP'], ],
		[ [1,255,'SPELL_MIMA_EXTRA1',
		   'TXT_KEY_SPELL_MIMA_EXTRA1',
		   'TXT_KEY_SPELL_MIMA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_MIMA_PHANTASM1',
		   'TXT_KEY_SPELL_MIMA_PHANTASM1',
		   'TXT_KEY_SPELL_MIMA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_EIKI1' , [
		[ [1,255,'SPELLCARD_EIKI1_1',
		   'TXT_KEY_SPELLCARD_EIKI1_1',
		   'TXT_KEY_SPELLCARD_EIKI1_1_HELP'], ],
		[ [1,255,'SPELL_EIKI_EXTRA1',
		   'TXT_KEY_SPELL_EIKI_EXTRA1',
		   'TXT_KEY_SPELL_EIKI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_EIKI_PHANTASM1',
		   'TXT_KEY_SPELL_EIKI_PHANTASM1',
		   'TXT_KEY_SPELL_EIKI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_NAZRIN1' , [
		[ [1,7,'SPELLCARD_NAZRIN1_1',
		   'TXT_KEY_SPELLCARD_NAZRIN1_1',
		   'TXT_KEY_SPELLCARD_NAZRIN1_1_HELP'],
		  [8,15,'SPELLCARD_NAZRIN1_2',
		   'TXT_KEY_SPELLCARD_NAZRIN1_2',
		   'TXT_KEY_SPELLCARD_NAZRIN1_2_HELP'],
		  [16,255,'SPELLCARD_NAZRIN1_3',
		   'TXT_KEY_SPELLCARD_NAZRIN1_3',
		   'TXT_KEY_SPELLCARD_NAZRIN1_3_HELP'],   ],
		[ [1,255,'SPELL_NAZRIN_EXTRA1',
		   'TXT_KEY_SPELL_NAZRIN_EXTRA1',
		   'TXT_KEY_SPELL_NAZRIN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_NAZRIN_PHANTASM1',
		   'TXT_KEY_SPELL_NAZRIN_PHANTASM1',
		   'TXT_KEY_SPELL_NAZRIN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_KOGASA1' , [
		[ [1,7,'SPELLCARD_KOGASA1_1',
		   'TXT_KEY_SPELLCARD_KOGASA1_1',
		   'TXT_KEY_SPELLCARD_KOGASA1_1_HELP'],
		  [8,11,'SPELLCARD_KOGASA1_2',
		   'TXT_KEY_SPELLCARD_KOGASA1_2',
		   'TXT_KEY_SPELLCARD_KOGASA1_1_HELP'],
		  [12,255,'SPELLCARD_KOGASA1_3',
		   'TXT_KEY_SPELLCARD_KOGASA1_3',
		   'TXT_KEY_SPELLCARD_KOGASA1_1_HELP'],   ],
		[ [1,255,'SPELL_KOGASA_EXTRA1',
		   'TXT_KEY_SPELL_KOGASA_EXTRA1',
		   'TXT_KEY_SPELL_KOGASA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_KOGASA_PHANTASM1',
		   'TXT_KEY_SPELL_KOGASA_PHANTASM1',
		   'TXT_KEY_SPELL_KOGASA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_ICHIRIN1' , [
		[ [1,7,'SPELLCARD_ICHIRIN1_1',
		   'TXT_KEY_SPELLCARD_ICHIRIN1_1',
		   'TXT_KEY_SPELLCARD_ICHIRIN1_1_HELP'],
		  [8,11,'SPELLCARD_ICHIRIN1_2',
		   'TXT_KEY_SPELLCARD_ICHIRIN1_2',
		   'TXT_KEY_SPELLCARD_ICHIRIN1_1_HELP'],
		  [12,255,'SPELLCARD_ICHIRIN1_3',
		   'TXT_KEY_SPELLCARD_ICHIRIN1_3',
		   'TXT_KEY_SPELLCARD_ICHIRIN1_1_HELP'],   ],
		[ [1,255,'SPELL_ICHIRIN_EXTRA1',
		   'TXT_KEY_SPELL_ICHIRIN_EXTRA1',
		   'TXT_KEY_SPELL_ICHIRIN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_ICHIRIN_PHANTASM1',
		   'TXT_KEY_SPELL_ICHIRIN_PHANTASM1',
		   'TXT_KEY_SPELL_ICHIRIN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MINAMITSU1' , [
		[ [1,3,'SPELLCARD_MINAMITSU1_1',
		   'TXT_KEY_SPELLCARD_MINAMITSU1_1',
		   'TXT_KEY_SPELLCARD_MINAMITSU1_1_HELP'],
		  [4,7,'SPELLCARD_MINAMITSU1_2',
		   'TXT_KEY_SPELLCARD_MINAMITSU1_2',
		   'TXT_KEY_SPELLCARD_MINAMITSU1_1_HELP'],
		  [8,255,'SPELLCARD_MINAMITSU1_3',
		   'TXT_KEY_SPELLCARD_MINAMITSU1_3',
		   'TXT_KEY_SPELLCARD_MINAMITSU1_1_HELP'],   ],
		[ [1,255,'SPELL_MINAMITSU_EXTRA1',
		   'TXT_KEY_SPELL_MINAMITSU_EXTRA1',
		   'TXT_KEY_SPELL_MINAMITSU_EXTRA1_HELP',],],
		[ [1,255,'SPELL_MINAMITSU_PHANTASM1',
		   'TXT_KEY_SPELL_MINAMITSU_PHANTASM1',
		   'TXT_KEY_SPELL_MINAMITSU_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SYOU1' , [
		[ [1,7,'SPELLCARD_SYOU1_1',
		   'TXT_KEY_SPELLCARD_SYOU1_1',
		   'TXT_KEY_SPELLCARD_SYOU1_1_HELP'],
		  [8,255,'SPELLCARD_SYOU1_2',
		   'TXT_KEY_SPELLCARD_SYOU1_2',
		   'TXT_KEY_SPELLCARD_SYOU1_1_HELP'],   ],
		[ [1,255,'SPELL_SYOU_EXTRA1',
		   'TXT_KEY_SPELL_SYOU_EXTRA1',
		   'TXT_KEY_SPELL_SYOU_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SYOU_PHANTASM1',
		   'TXT_KEY_SPELL_SYOU_PHANTASM1',
		   'TXT_KEY_SPELL_SYOU_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_BYAKUREN1' , [
		[ [1,3,'SPELLCARD_BYAKUREN1_1',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_1',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_1_HELP'],
		  [4,7,'SPELLCARD_BYAKUREN1_2',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_2',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_2_HELP'],
		  [8,11,'SPELLCARD_BYAKUREN1_3',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_3',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_3_HELP'],
		  [12,15,'SPELLCARD_BYAKUREN1_4',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_4',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_4_HELP'],
		  [16,19,'SPELLCARD_BYAKUREN1_5',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_5',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_5_HELP'],
		  [20,255,'SPELLCARD_BYAKUREN1_6',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_6',
		   'TXT_KEY_SPELLCARD_BYAKUREN1_6_HELP'],    ],
		[ [1,255,'SPELL_BYAKUREN_EXTRA1',
		   'TXT_KEY_SPELL_BYAKUREN_EXTRA1',
		   'TXT_KEY_SPELL_BYAKUREN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_BYAKUREN_PHANTASM1',
		   'TXT_KEY_SPELL_BYAKUREN_PHANTASM1',
		   'TXT_KEY_SPELL_BYAKUREN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_NUE1' , [
		[ [1,255,'SPELLCARD_NUE1_1',
		   'TXT_KEY_SPELLCARD_NUE1_1',
		   'TXT_KEY_SPELLCARD_NUE1_1_HELP'], ],
		[ [1,255,'SPELL_NUE_EXTRA1',
		   'TXT_KEY_SPELL_NUE_EXTRA1',
		   'TXT_KEY_SPELL_NUE_EXTRA1_HELP',],],
		[ [1,255,'SPELL_NUE_PHANTASM1',
		   'TXT_KEY_SPELL_NUE_PHANTASM1',
		   'TXT_KEY_SPELL_NUE_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_YOSHIKA1' , [
		[ [1,7,'SPELLCARD_YOSHIKA1_1',
		   'TXT_KEY_SPELLCARD_YOSHIKA1_1',
		   'TXT_KEY_SPELLCARD_YOSHIKA1_1_HELP'],
		  [8,255,'SPELLCARD_YOSHIKA1_2',
		   'TXT_KEY_SPELLCARD_YOSHIKA1_2',
		   'TXT_KEY_SPELLCARD_YOSHIKA1_1_HELP'],    ],
		[ [1,255,'SPELL_YOSHIKA_EXTRA1',
		   'TXT_KEY_SPELL_YOSHIKA_EXTRA1',
		   'TXT_KEY_SPELL_YOSHIKA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_YOSHIKA_PHANTASM1',
		   'TXT_KEY_SPELL_YOSHIKA_PHANTASM1',
		   'TXT_KEY_SPELL_YOSHIKA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SEIGA1' , [
		[ [1,255,'SPELLCARD_SEIGA1_1',
		   'TXT_KEY_SPELLCARD_SEIGA1_1',
		   'TXT_KEY_SPELLCARD_SEIGA1_1_HELP'],    ],
		[ [1,255,'SPELL_SEIGA_EXTRA1',
		   'TXT_KEY_SPELL_SEIGA_EXTRA1',
		   'TXT_KEY_SPELL_SEIGA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SEIGA_PHANTASM1',
		   'TXT_KEY_SPELL_SEIGA_PHANTASM1',
		   'TXT_KEY_SPELL_SEIGA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_TOJIKO1' , [
		[ [1,7,'SPELLCARD_TOJIKO1_1',
		   'TXT_KEY_SPELLCARD_TOJIKO1_1',
		   'TXT_KEY_SPELLCARD_TOJIKO1_1_HELP'],
		  [8,255,'SPELLCARD_TOJIKO1_2',
		   'TXT_KEY_SPELLCARD_TOJIKO1_2',
		   'TXT_KEY_SPELLCARD_TOJIKO1_2_HELP'],    ],
		[ [1,255,'SPELL_TOJIKO_EXTRA1',
		   'TXT_KEY_SPELL_TOJIKO_EXTRA1',
		   'TXT_KEY_SPELL_TOJIKO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_TOJIKO_PHANTASM1',
		   'TXT_KEY_SPELL_TOJIKO_PHANTASM1',
		   'TXT_KEY_SPELL_TOJIKO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_FUTO1' , [
		[ [1,11,'SPELLCARD_FUTO1_1',
		   'TXT_KEY_SPELLCARD_FUTO1_1',
		   'TXT_KEY_SPELLCARD_FUTO1_1_HELP'],
		  [12,255,'SPELLCARD_FUTO1_2',
		   'TXT_KEY_SPELLCARD_FUTO1_2',
		   'TXT_KEY_SPELLCARD_FUTO1_2_HELP'],    ],
		[ [1,255,'SPELL_FUTO_EXTRA1',
		   'TXT_KEY_SPELL_FUTO_EXTRA1',
		   'TXT_KEY_SPELL_FUTO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_FUTO_PHANTASM1',
		   'TXT_KEY_SPELL_FUTO_PHANTASM1',
		   'TXT_KEY_SPELL_FUTO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_MIMIMIKO1' , [
		[ [1,15,'SPELLCARD_MIMIMIKO1_1',
		   'TXT_KEY_SPELLCARD_MIMIMIKO1_1',
		   'TXT_KEY_SPELLCARD_MIMIMIKO1_1_HELP'],
		  [16,255,'SPELLCARD_MIMIMIKO1_2',
		   'TXT_KEY_SPELLCARD_MIMIMIKO1_2',
		   'TXT_KEY_SPELLCARD_MIMIMIKO1_2_HELP'],    ],
		[ [1,255,'SPELL_MIMIMIKO_EXTRA1',
		   'TXT_KEY_SPELL_MIMIMIKO_EXTRA1',
		   'TXT_KEY_SPELL_MIMIMIKO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_MIMIMIKO_PHANTASM1',
		   'TXT_KEY_SPELL_MIMIMIKO_PHANTASM1',
		   'TXT_KEY_SPELL_MIMIMIKO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_YATUHASHI1' , [
		[ [1,255,'SPELLCARD_YATUHASHI1_1',
		   'TXT_KEY_SPELLCARD_YATUHASHI1_1',
		   'TXT_KEY_SPELLCARD_YATUHASHI1_1_HELP'],    ],
		[ [1,255,'SPELL_YATUHASHI_EXTRA1',
		   'TXT_KEY_SPELL_YATUHASHI_EXTRA1',
		   'TXT_KEY_SPELL_YATUHASHI_EXTRA1_HELP',],],
		[ [1,255,'SPELL_YATUHASHI_PHANTASM1',
		   'TXT_KEY_SPELL_YATUHASHI_PHANTASM1',
		   'TXT_KEY_SPELL_YATUHASHI_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_BENBEN1' , [
		[ [1,255,'SPELLCARD_BENBEN1_1',
		   'TXT_KEY_SPELLCARD_BENBEN1_1',
		   'TXT_KEY_SPELLCARD_BENBEN1_1_HELP'],    ],
		[ [1,255,'SPELL_BENBEN_EXTRA1',
		   'TXT_KEY_SPELL_BENBEN_EXTRA1',
		   'TXT_KEY_SPELL_BENBEN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_BENBEN_PHANTASM1',
		   'TXT_KEY_SPELL_BENBEN_PHANTASM1',
		   'TXT_KEY_SPELL_BENBEN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SEIJA1' , [
		[ [1,11,'SPELLCARD_SEIJA1_1',
		   'TXT_KEY_SPELLCARD_SEIJA1_1',
		   'TXT_KEY_SPELLCARD_SEIJA1_1_HELP'],
		  [12,255,'SPELLCARD_SEIJA1_2',
		   'TXT_KEY_SPELLCARD_SEIJA1_2',
		   'TXT_KEY_SPELLCARD_SEIJA1_2_HELP'],    ],
		[ [1,255,'SPELL_SEIJA_EXTRA1',
		   'TXT_KEY_SPELL_SEIJA_EXTRA1',
		   'TXT_KEY_SPELL_SEIJA_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SEIJA_PHANTASM1',
		   'TXT_KEY_SPELL_SEIJA_PHANTASM1',
		   'TXT_KEY_SPELL_SEIJA_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SHINMYOUMARU1' , [
		[ [1,7,'SPELLCARD_SHINMYOUMARU1_1',
		   'TXT_KEY_SPELLCARD_SHINMYOUMARU1_1',
		   'TXT_KEY_SPELLCARD_SHINMYOUMARU1_1_HELP'],
		  [8,15,'SPELLCARD_SHINMYOUMARU1_1',
		   'TXT_KEY_SPELLCARD_SHINMYOUMARU1_1',
		   'TXT_KEY_SPELLCARD_SHINMYOUMARU1_2_HELP'],
		  [16,255,'SPELLCARD_SHINMYOUMARU1_2',
		   'TXT_KEY_SPELLCARD_SHINMYOUMARU1_2',
		   'TXT_KEY_SPELLCARD_SHINMYOUMARU1_3_HELP'],    ],
		[ [1,255,'SPELL_SHINMYOUMARU_EXTRA1',
		   'TXT_KEY_SPELL_SHINMYOUMARU_EXTRA1',
		   'TXT_KEY_SPELL_SHINMYOUMARU_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SHINMYOUMARU_PHANTASM1',
		   'TXT_KEY_SPELL_SHINMYOUMARU_PHANTASM1',
		   'TXT_KEY_SPELL_SHINMYOUMARU_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_RAIKO1' , [
		[ [1,255,'SPELLCARD_RAIKO1_1',
		   'TXT_KEY_SPELLCARD_RAIKO1_1',
		   'TXT_KEY_SPELLCARD_RAIKO1_1_HELP'],    ],
		[ [1,255,'SPELL_RAIKO_EXTRA1',
		   'TXT_KEY_SPELL_RAIKO_EXTRA1',
		   'TXT_KEY_SPELL_RAIKO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_RAIKO_PHANTASM1',
		   'TXT_KEY_SPELL_RAIKO_PHANTASM1',
		   'TXT_KEY_SPELL_RAIKO_PHANTASM1_HELP',],
		  [1,255,'SPELL_RAIKO_PHANTASM2',
		   'TXT_KEY_SPELL_RAIKO_PHANTASM2',
		   'TXT_KEY_SPELL_RAIKO_PHANTASM2_HELP',],], ], ],
	[ 'UNIT_YORIHIME1' , [
		[ [1,255,'SPELLCARD_YORIHIME1_1',
		   'TXT_KEY_SPELLCARD_YORIHIME1_1',
		   'TXT_KEY_SPELLCARD_YORIHIME1_1_HELP'],
		  [1,255,'SPELLCARD_YORIHIME2_1',
		   'TXT_KEY_SPELLCARD_YORIHIME2_1',
		   'TXT_KEY_SPELLCARD_YORIHIME2_1_HELP'],
		  [1,255,'SPELLCARD_YORIHIME3_1',
		   'TXT_KEY_SPELLCARD_YORIHIME3_1',
		   'TXT_KEY_SPELLCARD_YORIHIME3_1_HELP'],    ],
		[ [1,255,'SPELL_YORIHIME_EXTRA1',
		   'TXT_KEY_SPELL_YORIHIME_EXTRA1',
		   'TXT_KEY_SPELL_YORIHIME_EXTRA1_HELP',],
		  [1,255,'SPELL_YORIHIME_EXTRA2',
		   'TXT_KEY_SPELL_YORIHIME_EXTRA2',
		   'TXT_KEY_SPELL_YORIHIME_EXTRA2_HELP',],
		  [1,255,'SPELL_YORIHIME_EXTRA3',
		   'TXT_KEY_SPELL_YORIHIME_EXTRA3',
		   'TXT_KEY_SPELL_YORIHIME_EXTRA3_HELP',], ],
		[ [1,255,'SPELL_YORIHIME_PHANTASM1',
		   'TXT_KEY_SPELL_YORIHIME_PHANTASM1',
		   'TXT_KEY_SPELL_YORIHIME_PHANTASM1_HELP',],
		  [1,255,'SPELL_YORIHIME_PHANTASM2',
		   'TXT_KEY_SPELL_YORIHIME_PHANTASM2',
		   'TXT_KEY_SPELL_YORIHIME_PHANTASM2_HELP',],
		  [1,255,'SPELL_YORIHIME_PHANTASM3',
		   'TXT_KEY_SPELL_YORIHIME_PHANTASM3',
		   'TXT_KEY_SPELL_YORIHIME_PHANTASM3_HELP',], ], ], ],
	[ 'UNIT_TOYOHIME1' , [
		[ [1,255,'SPELLCARD_TOYOHIME1_1',
		   'TXT_KEY_SPELLCARD_TOYOHIME1_1',
		   'TXT_KEY_SPELLCARD_TOYOHIME1_1_HELP'],    ],
		[ [1,255,'SPELL_TOYOHIME_EXTRA1',
		   'TXT_KEY_SPELL_TOYOHIME_EXTRA1',
		   'TXT_KEY_SPELL_TOYOHIME_EXTRA1_HELP',],
		  [1,255,'SPELL_TOYOHIME_EXTRA2',
		   'TXT_KEY_SPELL_TOYOHIME_EXTRA2',
		   'TXT_KEY_SPELL_TOYOHIME_EXTRA2_HELP',], ],
		[ [1,255,'SPELL_TOYOHIME_PHANTASM1',
		   'TXT_KEY_SPELL_TOYOHIME_PHANTASM1',
		   'TXT_KEY_SPELL_TOYOHIME_PHANTASM1_HELP',], ], ], ],
	[ 'UNIT_SEIRAN1' , [
		[ [1,7,'SPELLCARD_SEIRAN1_1',
		   'TXT_KEY_SPELLCARD_SEIRAN1_1',
		   'TXT_KEY_SPELLCARD_SEIRAN1_1_HELP'],
		  [8,15,'SPELLCARD_SEIRAN1_1',
		   'TXT_KEY_SPELLCARD_SEIRAN1_1',
		   'TXT_KEY_SPELLCARD_SEIRAN1_2_HELP'],
		  [16,255,'SPELLCARD_SEIRAN1_1',
		   'TXT_KEY_SPELLCARD_SEIRAN1_1',
		   'TXT_KEY_SPELLCARD_SEIRAN1_3_HELP'],    ],
		[ [1,255,'SPELL_SEIRAN_EXTRA1',
		   'TXT_KEY_SPELL_SEIRAN_EXTRA1',
		   'TXT_KEY_SPELL_SEIRAN_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SEIRAN_PHANTASM1',
		   'TXT_KEY_SPELL_SEIRAN_PHANTASM1',
		   'TXT_KEY_SPELL_SEIRAN_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_RINGO1' , [
		[ [1,11,'SPELLCARD_RINGO1_1',
		   'TXT_KEY_SPELLCARD_RINGO1_1',
		   'TXT_KEY_SPELLCARD_RINGO1_1_HELP'],
		  [12,255,'SPELLCARD_RINGO1_2',
		   'TXT_KEY_SPELLCARD_RINGO1_2',
		   'TXT_KEY_SPELLCARD_RINGO1_2_HELP'],    ],
		[ [1,255,'SPELL_RINGO_EXTRA1',
		   'TXT_KEY_SPELL_RINGO_EXTRA1',
		   'TXT_KEY_SPELL_RINGO_EXTRA1_HELP',],],
		[ [1,255,'SPELL_RINGO_PHANTASM1',
		   'TXT_KEY_SPELL_RINGO_PHANTASM1',
		   'TXT_KEY_SPELL_RINGO_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_DOREMY1' , [
		[ [1,255,'SPELLCARD_DOREMY1_1',
		   'TXT_KEY_SPELLCARD_DOREMY1_1',
		   'TXT_KEY_SPELLCARD_DOREMY1_1_HELP'],    ],
		[ [1,255,'SPELL_DOREMY_EXTRA1',
		   'TXT_KEY_SPELL_DOREMY_EXTRA1',
		   'TXT_KEY_SPELL_DOREMY_EXTRA1_HELP',],],
		[ [1,255,'SPELL_DOREMY_PHANTASM1',
		   'TXT_KEY_SPELL_DOREMY_PHANTASM1',
		   'TXT_KEY_SPELL_DOREMY_PHANTASM1_HELP',],], ], ],
	[ 'UNIT_SAGUME1' , [
		[ [1,15,'SPELLCARD_SAGUME1_1',
		   'TXT_KEY_SPELLCARD_SAGUME1_1',
		   'TXT_KEY_SPELLCARD_SAGUME1_1_HELP'],
		  [15,255,'SPELLCARD_SAGUME1_2',
		   'TXT_KEY_SPELLCARD_SAGUME1_2',
		   'TXT_KEY_SPELLCARD_SAGUME1_2_HELP'],    ],
		[ [1,255,'SPELL_SAGUME_EXTRA1',
		   'TXT_KEY_SPELL_SAGUME_EXTRA1',
		   'TXT_KEY_SPELL_SAGUME_EXTRA1_HELP',],],
		[ [1,255,'SPELL_SAGUME_PHANTASM1',
		   'TXT_KEY_SPELL_SAGUME_PHANTASM1',
		   'TXT_KEY_SPELL_SAGUME_PHANTASM1_HELP',],], ], ],
]

# Civilopedia用スペルとヘルプテキスト関数の対応表
### こっちはこのファイルに書かれている必要がある
SpellToHelpfuncList = None 

def init_helpfunclist():
	global SpellToHelpfuncList
	SpellToHelpfuncList = [
		["SPELLCARD_FUTO1_1",help_FUTO1],
		["SPELLCARD_FUTO1_2",help_FUTO1],
		["SPELLCARD_SHINMYOUMARU1_1",help_SHINMYOUMARU1],
		["SPELLCARD_SHINMYOUMARU1_2",help_SHINMYOUMARU1],
		["SPELLCARD_SHINMYOUMARU1_3",help_SHINMYOUMARU1],
		["SPELLCARD_YORIHIME1_1",help_YORIHIME1],
		["SPELLCARD_YORIHIME2_1",help_YORIHIME2],
		["SPELLCARD_RINGO1_1",help_RINGO1],
		["SPELLCARD_RINGO1_2",help_RINGO1],
		["SPELLCARD_DOREMY1_1",help_DOREMY1],
		["SPELL_EIKI_PHANTASM1",help_EIKI_PHANTASM1],
		["SPELL_YORIHIME_PHANTASM1",help_YORIHIME_PHANTASM1],
		["SPELL_YORIHIME_PHANTASM3",help_YORIHIME_PHANTASM3],
		["SPELL_SEIRAN_EXTRA1",help_SEIRAN_EXTRA1],
		["SPELL_SAGUME_EXTRA1",help_SAGUME_EXTRA1],
	]


#早苗
def req_SANAE1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SANAE1','UNIT_SANAE6',cost)


def spellcard_SANAE1(caster,cost):

	if caster.plot().isCity():

		CAL = caster.countCardAttackLevel()
		Functions.changeDamage(RangeList0,caster,-CAL*3,-CAL*3,100,True,True,True,True,-1,False,True,True,True,-1,True,0)

		if CAL >= 1:
			Functions.setPromotion(RangeList0,caster,'PROMOTION_CITY_GARRISON1',True,100,True,False,False,-1,False,True,True,True,-1,True)
		if CAL >= 4:
			Functions.setPromotion(RangeList0,caster,'PROMOTION_CITY_GARRISON2',True,100,True,False,False,-1,False,True,True,True,-1,True)
		if CAL >= 8:
			Functions.setPromotion(RangeList0,caster,'PROMOTION_CITY_GARRISON3',True,100,True,False,False,-1,False,True,True,True,-1,True)
			Functions.setPromotion(RangeList0,caster,'PROMOTION_SHOOTING_TECHNIQUE1',True,100,True,False,False,-1,False,True,True,True,-1,True)
		if CAL >= 12:
			Functions.setPromotion(RangeList0,caster,'PROMOTION_DRILL1',True,100,True,False,False,-1,False,True,True,True,-1,True)
			Functions.setPromotion(RangeList0,caster,'PROMOTION_SHOOTING_TECHNIQUE2',True,100,True,False,False,-1,False,True,True,True,-1,True)
		if CAL >= 16:
			Functions.setPromotion(RangeList0,caster,'PROMOTION_DRILL2',True,100,True,False,False,-1,False,True,True,True,-1,True)
			Functions.setPromotion(RangeList0,caster,'PROMOTION_SHOOTING_TECHNIQUE3',True,100,True,False,False,-1,False,True,True,True,-1,True)
		if CAL >= 20:
			Functions.setPromotion(RangeList0,caster,'PROMOTION_DRILL3',True,100,True,False,False,-1,False,True,True,True,-1,True)
		if CAL >= 24:
			Functions.setPromotion(RangeList0,caster,'PROMOTION_DRILL4',True,100,True,False,False,-1,False,True,True,True,-1,True)
			
			
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)
		#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELLCARD'),False )

		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False
		

def spellcard_SANAE1_Estimate(caster):

	estimatePoint = 0
	
	if caster.plot().isCity() and Functions.isWar(caster.getOwner()):
		pPlot = caster.plot()
		count = 0
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getTeam() == caster.getTeam() and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				count = count + 1
		estimatePoint = count

	return estimatePoint




#レミリア
def req_REMILIA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_REMILIA1','UNIT_REMILIA6',cost)
	
def spellcard_REMILIA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	RangeList = [ [-1,0],[1,0],[0,1],[0,-1], ]
	Functions.changeDamage(RangeList,caster,15+CAL*3,15+CAL*3,0,True,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList,caster,(15+CAL*3)/2,(15+CAL*3)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0)
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELLCARD'),False )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_REMILIA1_Estimate(caster):
	
	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	RangeList = [ [-1,0],[1,0],[0,1],[0,-1], ]
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,15+CAL*3,15+CAL*3,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,(15+CAL*3)/2,(15+CAL*3)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	#print "CAL:%d" %CAL
	#print "estimate point1:%d" %estimatePoint
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (15+CAL*3)) * 100
	
	if estimatePoint < 50:
		estimatePoint = 0
	
	#print "estimate point2:%d" %estimatePoint
	
	return estimatePoint






#ちぇん
def req_CHEN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_CHEN1','UNIT_CHEN6',cost)

def spellcard_CHEN1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	if CAL <= 3:
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AKAONI_EASY'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AOONI_EASY'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	elif CAL <= 7:
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AKAONI_NORMAL'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AOONI_NORMAL'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	elif CAL <=11:
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AKAONI_HARD'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AOONI_HARD'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AKAONI_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AOONI_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	if CAL >= 4:
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'),True)
	if CAL >= 8:
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT2'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT2'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT3'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT3'),True)
	if CAL >= 12:
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT4'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT4'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT5'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT5'),True)
	if CAL >= 16:
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL1'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL1'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL2'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL2'),True)
	if CAL >= 20:
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL3'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL3'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL4'),True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL4'),True)
		
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_CHEN1_Estimate(caster):
	
	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = 100
	
	return estimatePoint
	



#リグル
def req_WRIGGLE1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_WRIGGLE1','UNIT_WRIGGLE6',cost)
	

def spellcard_WRIGGLE1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]*2):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LITTLE_BUG'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setSpecialNumber(CAL*3-1)
		
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def spellcard_WRIGGLE1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = 100
	
	return estimatePoint




#てゐ
def req_TEWI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_TEWI1','UNIT_TEWI6',cost)
	

def spellcard_TEWI1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_EASY',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_NORMAL',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_HARD',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_LUNATIC',False,100,True,True,True,-1,True,True,True,True,-1,True)

	if CAL <= 3:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_EASY',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 7:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_NORMAL',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 11:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_HARD',True,100,True,False,False,-1,False,True,True,True,-1,True)
	else:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_OMAMORI_LUNATIC',True,100,True,False,False,-1,False,True,True,True,-1,True)
	
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
			pUnit = pUnit
		else:
			if pUnit.getTeam() == caster.getTeam():
				pUnit.changeMoves(-CAL*50/8)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_TEWI1_Estimate(caster):
	return 0

	estimatePoint = 0
	
	if Functions.isWar(caster.getOwner()):
		pPlot = caster.plot()
		count = 0
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getTeam() == caster.getTeam() and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				count = count + 1
		estimatePoint = count

	return estimatePoint





#にとり
def req_NITORI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_NITORI1','UNIT_NITORI6',cost)


def spellcard_NITORI1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]):
		if CAL <= 3:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_EASY'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL <= 7:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_NORMAL'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL <=11:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_HARD'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_NITORI1_Estimate(caster):
	return 100
	



#まりさ
def req_MARISA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MARISA1','UNIT_MARISA6',cost)
	

def spellcard_MARISA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	RangeList = []
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pPlot.getPlotCity().changeDefenseDamage(CAL*7+50)
					RangeList.append([iX,iY])
	if CAL >= 8:
		Functions.changeDamage(RangeList,caster,(CAL-8)*5,(CAL-8)*5,0,True,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList,caster,(CAL-8)*5/2,(CAL-8)*5/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_MARISA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					if pTeam.isAtWar( pCity.getTeam() ):
						estimatePoint = 100 - pCity.getDefenseDamage

	return estimatePoint



#フラン
def req_FLAN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_FLAN1','UNIT_FLAN6',cost)
	

def spellcard_FLAN1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(3):
		newUnit1 = pPlayer.initUnit(caster.getUnitType(), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLITZ'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FLAN_SKILL1'),True)
		
		if CAL >= 4:
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT1'),True)
		if CAL >= 8:
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT2'),True)
		if CAL >= 12:
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT3'),True)
		if CAL >= 16:
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT4'),True)
		if CAL >= 20:
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT5'),True)
		if CAL >= 24:
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT6'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LAEVATEINN')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAEVATEINN'),True)
		
		newUnit1.changeDamage(75-CAL*5,caster.getOwner())
		newUnit1.setSinraDelayTurn(1000)
		
		if CAL<12:
			newUnit1.changeMoves(100)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_LAEVATEINN'),False)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_FLAN1_Estimate(caster):

	pTeam = gc.getTeam(caster.getTeam())
	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	count = 0
	
	if Functions.isWar(caster.getOwner()):
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					for i in range(pPlot.getNumUnits()):
						if pTeam.isAtWar( pPlot.getUnit(i).getTeam() ):
							count = count + 1
	
	estimatePoint = count * 5
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint




#ようむ
def req_YOUMU1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YOUMU1','UNIT_YOUMU6',cost)


def spellcard_YOUMU1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]):
		newUnit1 = pPlayer.initUnit(caster.getUnitType(), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'),True)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_YOUMU_SKILL1'),True)
		newUnit1.setSinraDelayTurn(1000)
		
		if CAL<12:
			newUnit1.changeMoves(100)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_YOUMU1_Estimate(caster):

	pTeam = gc.getTeam(caster.getTeam())
	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	count = 0
	
	if Functions.isWar(caster.getOwner()):
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					for i in range(pPlot.getNumUnits()):
						if pTeam.isAtWar( pPlot.getUnit(i).getTeam() ):
							count = count + 1
	
	estimatePoint = count * 4
	if estimatePoint < 40:
		estimatePoint = 0
	
	return estimatePoint




#ちるの
def req_CIRNO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_CIRNO1','UNIT_CIRNO6',cost)


def spellcard_CIRNO1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	if CAL>=4:
	
		Functions.changeDamage(RangeList1,caster,5+CAL*2,5+CAL*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList1,caster,(5+CAL*2)/2,(5+CAL*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		
		Functions.setPromotion(RangeList1,caster,'PROMOTION_FREEZE',True,100+CAL*5,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_CIRNO1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,5+CAL*2,5+CAL*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,(5+CAL*2)/2,(5+CAL*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (5+CAL*2)) * 100
	
	return estimatePoint




#えーりん
def req_EIRIN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_EIRIN1','UNIT_EIRIN6',cost)


def spellcard_EIRIN1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]):
		if CAL<=3:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_EASY'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL<=7:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_NORMAL'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL<=11:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_HARD'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_EIRIN1_Estimate(caster):

	estimatePoint = 0
	
	if caster.plot().isCity() and Functions.isWar(caster.getOwner()):
		estimatePoint = 200

	return estimatePoint



#すわこ
def req_SUWAKO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SUWAKO1','UNIT_SUWAKO6',cost)


def spellcard_SUWAKO1(caster,cost):
	
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	gc.getGame().setPlotExtraYield(iX,iY,0,(CAL+4)/8)
	gc.getGame().setPlotExtraYield(iX,iY,1,(CAL+4)/8+1)
	gc.getGame().setPlotExtraYield(iX,iY,2,CAL/4+1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_SUWAKO1_Estimate(caster):

	estimatePoint = 0
	
	if caster.plot().isCity():
		estimatePoint = 20
		if caster.plot().getPlotCity().isCapital():
			estimatePoint = 1000

	return estimatePoint





#アリス
def req_ALICE1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_ALICE1','UNIT_ALICE6',cost)
	

def spellcard_ALICE1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]):
		if gc.getGame().getSorenRandNum(100,"Alice SpellCard") < 50:
			if CAL<=3:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=7:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL2'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=11:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL3'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=15:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL4'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=19:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL5'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			else:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL6'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			if CAL<=3:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAI_DOLL1'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=7:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAI_DOLL2'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=11:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAI_DOLL3'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=15:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAI_DOLL4'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif CAL<=19:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAI_DOLL5'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			else:
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HOURAI_DOLL6'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_ALICE1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = 100
	
	return estimatePoint
	
	


#もこ
def req_MOKOU1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MOKOU1','UNIT_MOKOU6',cost)
	

def spellcard_MOKOU1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	RangeList = []
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
				
					if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getPlotCity().getTeam()): #戦争相手なら
						RangeList.append([iX,iY])
					else:
						pPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
						pPlot.setTerrainType(gc.getInfoTypeForString("TERRAIN_PLAINS"),True,True)
						gc.getGame().setPlotExtraYield(caster.getX()+iX,caster.getY()+iY,1,CAL/8+1)

	Functions.changeDamage(RangeList,caster,15+CAL*2,15+CAL*2,0,True,True,True,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList,caster,(15+CAL*2)/2,(15+CAL*2)/2,0,True,True,True,True,-1,True,False,True,True,-1,False,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_MOKOU1_Estimate(caster):
	
	estimatePoint = 0
	
	if caster.plot().isCity():
		estimatePoint = 10
		if caster.plot().getPlotCity().isCapital():
			estimatePoint = 15
	
	else:
		CAL = caster.countCardAttackLevel()
		pTeam = gc.getTeam(caster.getTeam())
		count =0
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					if pPlot.isCity():
						for i in range(pPlot.getNumUnits()):
							if pTeam.isAtWar( pPlot.getUnit(i).getTeam() ):
								count = count + 1
		estimatePoint = count * 5
		
		if estimatePoint < 50:
			estimatePoint = 0

	return estimatePoint




#けーね
def req_KEINE1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_KEINE1','UNIT_KEINE6',cost)
	

def spellcard_KEINE1(caster,cost):

	CAL = caster.countCardAttackLevel()

	if CAL <= 3:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_REKISHI1',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 7:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_REKISHI2',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 11:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_REKISHI3',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 15:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_REKISHI4',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 19:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_REKISHI5',True,100,True,False,False,-1,False,True,True,True,-1,True)
	else:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_REKISHI6',True,100,True,False,False,-1,False,True,True,True,-1,True)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_KEINE1_Estimate(caster):

	estimatePoint = 0
	
	if Functions.isWar(caster.getOwner()):
		pPlot = caster.plot()
		count = 0
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getTeam() == caster.getTeam() and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				count = count + 1
		estimatePoint = count

	return estimatePoint




#きもけーね
def req_HAKUTAKUKEINE1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_HAKUTAKUKEINE1','UNIT_HAKUTAKUKEINE6',cost)

def spellcard_HAKUTAKUKEINE1(caster,cost):

	CAL = caster.countCardAttackLevel()
	UnitList = []
	pPlot = caster.plot()
	
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_BOSS") and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
			UnitList.append(pPlot.getUnit(i))
	
	if len(UnitList) > 0:
		TotalExperience = CAL*CAL*3/2
		index = 0
		for i in range(TotalExperience):
			UnitList[index].changeExperience(1,-1,False,False,False)
			index = index + 1
			if index >= len(UnitList):
				index = 0
			
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)

		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True

	return False


def spellcard_HAKUTAKUKEINE1_Estimate(caster):

	estimatePoint = 0
	
	if Functions.isWar(caster.getOwner()):
		pPlot = caster.plot()
		count = 0
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getTeam() == caster.getTeam() and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				count = count + 1
		estimatePoint = count

	return estimatePoint




#パルスィ
def req_PARSEE1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_PARSEE1','UNIT_PARSEE6',cost)
	

def spellcard_PARSEE1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GREENEYEDMONSTER'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GREENEYEDMONSTER'),True)
		newUnit1.setSpecialNumber(CAL-1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_PARSEE1_Estimate(caster):

	pTeam = gc.getTeam(caster.getTeam())
	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	count = 0
	
	if Functions.isWar(caster.getOwner()):
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					for i in range(pPlot.getNumUnits()):
						if pTeam.isAtWar( pPlot.getUnit(i).getTeam() ):
							count = count + 1
	
	estimatePoint = count * 5
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint





#勇儀
def req_YUGI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YUGI1','UNIT_YUGI6',cost)


def spellcard_YUGI1(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	Functions.changeDamage(RangeList1,caster,0,CAL*7,1,True,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,0,(CAL*7)/2,1,True,False,False,True,-1,True,False,True,True,-1,False,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL_OEYAMA'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_YUGI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,0,CAL*7,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,0,(CAL*7)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*4)) * 100
	
	if estimatePoint < 20:
		estimatePoint = 0
	
	return estimatePoint






#咲夜
def req_SAKUYA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SAKUYA1','UNIT_SAKUYA6',cost)
	
def spellcard_SAKUYA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	if CAL <= 5:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_EASY',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SAKUYA_SKILL1')):
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_EASY',True,100,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		else:
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_EASY',True,50,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	elif CAL <= 11:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_NORMAL',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SAKUYA_SKILL1')):
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_NORMAL',True,100,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		else:
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_NORMAL',True,50,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	elif CAL <= 15:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_HARD',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SAKUYA_SKILL1')):
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_HARD',True,100,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		else:
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_HARD',True,50,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	else:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_LUNATIC',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SAKUYA_SKILL1')):
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_LUNATIC',True,100,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		else:
			Functions.setPromotion(RangeList1,caster,'PROMOTION_THEWORLD_LUNATIC',True,50,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_SAKUYA1_Estimate(caster):
	
	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,20+CAL*3,20+CAL*3,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,(20+CAL*3)/2,(20+CAL*3)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (20+CAL*3)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint





#ゆゆこ
def req_YUYUKO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YUYUKO1','UNIT_YUYUKO6',cost)
	
def spellcard_YUYUKO1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())

	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				for i in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					if caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == True:
						if pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY') and pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
							if gc.getGame().getSorenRandNum(100, "spellcard cast") < CAL*2:
								pUnit.changeDamage(100,caster.getOwner())
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_YUYUKO1_Estimate(caster):

	pTeam = gc.getTeam(caster.getTeam())
	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	count = 0
	
	if Functions.isWar(caster.getOwner()):
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					for i in range(pPlot.getNumUnits()):
						if pTeam.isAtWar( pPlot.getUnit(i).getTeam() ):
							count = count + 1
	
	estimatePoint = count * 4
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint




#ルーミア
def req_RUMIA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_RUMIA1','UNIT_RUMIA6',cost)
	

def spellcard_RUMIA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	Functions.changeDamage(RangeList1,caster,0,CAL*5,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,0,(CAL*5)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_KURAYAMI',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_KURAYAMI',True,50,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_RUMIA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,0,CAL*5,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,0,(CAL*5)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
	return estimatePoint






#メディスン
def req_MEDICIN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MEDICIN1','UNIT_MEDICIN6',cost) or Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MEDICINwithSU1','UNIT_MEDICINwithSU6',cost)
	

def spellcard_MEDICIN1(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	if CAL >= 1:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON1',True,100+CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON1',True,50+CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	if CAL >= 4:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON2',True,100+CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON2',True,50+CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	if CAL >= 8:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON3',True,100+CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON3',True,50+CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	if CAL >= 12:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON4',True,100+CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON4',True,50+CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def spellcard_MEDICIN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,100,100,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,100,100,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (100)) * 100
	
	if estimatePoint < 25:
		estimatePoint = 0
	
	return estimatePoint





#神奈子
def req_KANAKO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_KANAKO1','UNIT_KANAKO6',cost)
	

def spellcard_KANAKO1(caster,cost):

	if caster.plot().isCity() and caster.plot().getPlotType() == PlotTypes.PLOT_HILLS:

		CAL = caster.countCardAttackLevel()
		
		Functions.changeDamage(RangeList2,caster,5+CAL*3,5+CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList2,caster,(5+CAL*3)/2,(5+CAL*3)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)

		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)

		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False

def spellcard_KANAKO1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList2,caster,5+CAL*3,5+CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList2,caster,(5+CAL*3)/2,(5+CAL*3)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (5+CAL*3)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint







#れいむ
def req_REIMU1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_REIMU1','UNIT_REIMU6',cost)
	
def spellcard_REIMU1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	RangeList = []
	
	Top = -CAL
	Bottom = CAL+1
	Left = -CAL
	Right = CAL+1
	
	for iX in range(Left,Right):
		for iY in range(Top,Bottom):
			RangeList.append([iX,iY])
	
	Functions.changeDamage(RangeList1,caster,10+CAL*2,10+CAL*2,0,True,False,False,True,-1,False,True,True,True,-1,False,0)
	
	Functions.setPromotion(RangeList,caster,'PROMOTION_SPELL_CASTED',True,100,False,True,True,-1,True,False,True,True,-1,True,1)
	Functions.setPromotion(RangeList,caster,'PROMOTION_CHARM',True,100,False,True,True,-1,True,False,False,True,-1,True,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def spellcard_REIMU1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,10+CAL*2,10+CAL*2,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (10+CAL*2)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint




#ゆうか
def req_YUKA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YUKA1','UNIT_YUKA6',cost)
	

def spellcard_YUKA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pPlot.getPlotCity().changeDefenseDamage(CAL*4)
					
	Functions.changeDamage(RangeList1,caster,CAL*4,CAL*4,0,True,False,True,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,CAL*4/2,CAL*4/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def spellcard_YUKA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*4,CAL*4,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*4/2,CAL*4/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*4)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint
	
	




#こいし
def req_KOISHI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_KOISHI1','UNIT_KOISHI6',cost)

def spellcard_KOISHI1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	RangeList = [ [-1,2,],[1,2],[-2,1],[-1,1],[0,1],[1,1],[2,1],[-2,0],[-1,0],[1,0],[2,0],[-1,-1],[0,-1],[1,-1],[0,-2], ]
	
	Functions.changeDamage(RangeList,caster,10+CAL*3/2,10+CAL*3/2,0,True,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList,caster,(10+CAL*3/2)/2,(10+CAL*3/2)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0)
	
	Functions.setPromotion(RangeList,caster,'PROMOTION_CHARM',True,15+CAL*3,False,False,True,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList,caster,'PROMOTION_CHARM',True,(15+CAL*3)/2,False,False,True,-1,True,False,True,True,-1,True,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	if CAL >= 12:
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL_big_heart'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_KOISHI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	RangeList = [ [-1,2,],[1,2],[-2,1],[-1,1],[0,1],[1,1],[2,1],[-2,0],[-1,0],[1,0],[2,0],[-1,-1],[0,-1],[1,-1],[0,-2], ]
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,10+CAL*3/2,10+CAL*3/2,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,(10+CAL*3/2)/2,(10+CAL*3/2)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (10+CAL*3/2)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint






#ぱちゅりー
def req_PATCHOULI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_PATCHOULI1','UNIT_PATCHOULI6',cost)
	

def spellcard_PATCHOULI1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	Level = caster.getLevel()
	RangeList = []
	
	Top = -Level
	Bottom = Level+1
	Left = -Level
	Right = Level+1
	
	for iX in range(Left,Right):
		for iY in range(Top,Bottom):
			RangeList.append([iX,iY])
	
	Functions.changeDamage(RangeList,caster,5+CAL*3,5+CAL*3,0,True,False,False,True,-1,False,True,True,True,-1,False,1)
	Functions.changeDamage(RangeList,caster,(5+CAL*3)/2,(5+CAL*3)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_PATCHOULI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	Level = caster.getLevel()
	RangeList = []
	
	Top = -Level
	Bottom = Level+1
	Left = -Level
	Right = Level+1
	
	for iX in range(Left,Right):
		for iY in range(Top,Bottom):
			RangeList.append([iX,iY])
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,5+CAL*3,5+CAL*3,0,True,False,False,True,-1,False,True,True,True,-1,False,1,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,(5+CAL*3)/2,(5+CAL*3)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,1,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (5+CAL*3)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint
	



def req_PATCHOULI2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_PATCHOULI1','UNIT_PATCHOULI6',cost)
	

def spellcard_PATCHOULI2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	Level = caster.getLevel()
	RangeList = []
	
	Top = -Level
	Bottom = Level+1
	Left = -Level
	Right = Level+1
	
	for iX in range(Left,Right):
		for iY in range(Top,Bottom):
			RangeList.append([iX,iY])
	
	Functions.changeDamage(RangeList,caster,-(5+CAL*3),-(5+CAL*3),100,False,True,True,False,-1,True,True,True,True,-1,True,1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_PATCHOULI2_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	Level = caster.getLevel()
	RangeList = []
	
	Top = -Level
	Bottom = Level+1
	Left = -Level
	Right = Level+1
	
	for iX in range(Left,Right):
		for iY in range(Top,Bottom):
			RangeList.append([iX,iY])
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,-(5+CAL*3),-(5+CAL*3),100,False,True,True,False,-1,True,True,True,True,-1,True,1,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (5+CAL*3)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint







#らん
def req_RAN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_RAN1','UNIT_RAN6',cost)


def spellcard_RAN1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		
		if CAL <= 3:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ANALYZER_EASY'),1)
		elif CAL <= 7:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ANALYZER_NORMAL'),1)
		elif CAL <= 11:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ANALYZER_HARD'),1)
		else:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ANALYZER_LUNATIC'),1)
		
	
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False

def spellcard_RAN1_Estimate(caster):

	estimatePoint = 0
	
	if caster.plot().isCity():
		estimatePoint = 10
		if caster.plot().getPlotCity().isCapital():
			estimatePoint = 15

	return estimatePoint





#うどんげ
def req_REISEN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_REISEN1','UNIT_REISEN6',cost)


def spellcard_REISEN1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_MADNESS',True,25+CAL*15/2,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_REISEN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,100,100,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (100)) * 100
	
	if estimatePoint < 25:
		estimatePoint = 0
	
	return estimatePoint





#いく
def req_IKU1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_IKU1','UNIT_IKU6',cost)
	

def spellcard_IKU1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	CityList = []
	pTeam = gc.getTeam(caster.getTeam())
	BuildingList = []
	
	if CAL >= 1:
		BuildingList.append('BUILDING_BARRACKS')
		BuildingList.append('BUILDING_LIBRARY')
		BuildingList.append('BUILDING_GRANARY')
		BuildingList.append('BUILDING_ARABIAN_MADRASSA')
	if CAL >= 4:
		BuildingList.append('BUILDING_AQUEDUCT')
		BuildingList.append('BUILDING_COURTHOUSE')
		BuildingList.append('BUILDING_COLOSSEUM')
		BuildingList.append('BUILDING_THEATRE')
	if CAL >= 8:
		BuildingList.append('BUILDING_FORGE')
		BuildingList.append('BUILDING_MARKET')
		BuildingList.append('BUILDING_GROCER')
	if CAL >= 12:
		BuildingList.append('BUILDING_BANK')
		BuildingList.append('BUILDING_UNIVERSITY')
		BuildingList.append('BUILDING_OBSERVATORY')
		BuildingList.append('BUILDING_KOREAN_SEOWON')
	
	for i in range(TohoCivList.iMaxPlayer): 
		pPlayer = gc.getPlayer(i)
		if pPlayer.isBarbarian() == False and pPlayer.isAlive() == True and pTeam.isAtWar(pPlayer.getTeam()) == True:
			py = PyPlayer(i)
			for pPyCity in py.getCityList():
				pCity = pPlayer.getCity(pPyCity.getID())
				CityList.append(pCity)
				
	if len(CityList) > 0:
		for i in range(CAL/4+1):
			CityNum = gc.getGame().getSorenRandNum(len(CityList), "Iku Spell Card")
			CityBuildingList = []
			for j in range(len(BuildingList)):
				if CityList[CityNum].getNumRealBuilding(gc.getInfoTypeForString(BuildingList[j])):
					CityBuildingList.append(BuildingList[j])
			if len(CityBuildingList) > 0: #壊せる建物があれば
				BuildingNum = gc.getGame().getSorenRandNum(len(CityBuildingList), "Iku Spell Card2")
				CityList[CityNum].setNumRealBuilding(gc.getInfoTypeForString(CityBuildingList[BuildingNum]),0)
				#～文明の～都市にある～が雷により破壊されました！
				#CyInterface().addImmediateMessage(gc.getCivilizationInfo(CityList[CityNum].getOwner()).getDescription() + "&#12398;" + CityList[CityNum].getName() + "&#12395;&#12354;&#12427;" + gc.getBuildingInfo(gc.getInfoTypeForString(CityBuildingList[BuildingNum])).getDescription() + "&#12364;&#38647;&#12395;&#12424;&#12426;&#30772;&#22730;&#12373;&#12428;&#12414;&#12375;&#12383;&#65281;","")	#～都市にある～が雷により破壊されました！
				CyInterface().addImmediateMessage(CityList[CityNum].getName() + "&#12395;&#12354;&#12427;" + gc.getBuildingInfo(gc.getInfoTypeForString(CityBuildingList[BuildingNum])).getDescription() + "&#12364;&#38647;&#12395;&#12424;&#12426;&#30772;&#22730;&#12373;&#12428;&#12414;&#12375;&#12383;&#65281;","")
				
			else:   #なければ人口減少
				if CityList[CityNum].getPopulation() > 3:
					CityList[CityNum].changePopulation(-2)
				else:
					CityList[CityNum].setPopulation(1)
				#都市の人口が雷により減少しました！
				CyInterface().addImmediateMessage(CityList[CityNum].getName() + "&#12398;&#20154;&#21475;&#12364;&#38647;&#12395;&#12424;&#12426;&#28187;&#23569;&#12375;&#12414;&#12375;&#12383;&#65281;","")
			
			#AIが相手ならばさらに反乱が発生
			if CityList[CityNum].isHuman() == False:
				CityList[CityNum].changeOccupationTimer( 1 )
			
			
			#雷が落ちた都市で発生するエフェクト
			point = CityList[CityNum].plot().getPoint()
			CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_IKUTHUNDER'),point)
			CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

				
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_IKUTHUNDER'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False


def spellcard_IKU1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = 25
	
	return estimatePoint




#さとり
def req_SATORI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SATORI1','UNIT_SATORI6',cost)

def spellcard_SATORI1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	if CAL <= 3:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_TERRIBLE_SOUVEBNIR1',True,100,True,False,False,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
	elif CAL <= 7:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_TERRIBLE_SOUVEBNIR2',True,100,True,False,False,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
	elif CAL <= 11:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_TERRIBLE_SOUVEBNIR3',True,100,True,False,False,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
	elif CAL <= 15:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_TERRIBLE_SOUVEBNIR4',True,100,True,False,False,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
	else:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_TERRIBLE_SOUVEBNIR5',True,100,True,False,False,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_SATORI1_Estimate(caster):

	estimatePoint = 0
	
	if Functions.isWar(caster.getOwner()):
		pPlot = caster.plot()
		count = 0
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getTeam() == caster.getTeam() and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				count = count + 1
		estimatePoint = count

	return estimatePoint




#ミスティア
def req_MYSTIA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MYSTIA1','UNIT_MYSTIA6',cost)


def spellcard_MYSTIA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_TORIME',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_TORIME',True,50,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	
	Functions.changeDamage(RangeList1,caster,CAL,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,CAL/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
	
	if CAL >= 12:
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					if pPlot.isCity():
						pPlot.getPlotCity().changeOccupationTimer( (CAL-12)/4 +1 )
						
						#反乱の起きた都市でエフェクト発生
						point = pPlot.getPoint()
						CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_LIVE'),point)
						CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_LIVE'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_MYSTIA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*2)) * 100
	
	return estimatePoint
	



#すいか
def req_SUIKA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SUIKA1','UNIT_SUIKA6',cost) or Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SUIKA1_YOUKAI','UNIT_SUIKA6_YOUKAI',cost)
	

def spellcard_SUIKA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	if caster.isHuman() == False:
		Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0)
	
	else:
		pPlayer = gc.getPlayer(caster.getOwner())
		iCiv = pPlayer.getCivilizationType()
		
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN'):
			if gc.getInfoTypeForString("UNIT_SUIKA1") <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString("UNIT_SUIKA6"):
				TransformUnit = caster.getUnitType() - gc.getInfoTypeForString("UNIT_SUIKA1") + gc.getInfoTypeForString("UNIT_SUIKA_BIG1")
				newUnit1 = gc.getPlayer(caster.getOwner()).initUnit(TransformUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
				newUnit1.convert(caster)
				caster = newUnit1
		
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_SPAIN'):
			if gc.getInfoTypeForString("UNIT_SUIKA1_YOUKAI") <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString("UNIT_SUIKA6_YOUKAI"):
				TransformUnit = caster.getUnitType() - gc.getInfoTypeForString("UNIT_SUIKA1_YOUKAI") + gc.getInfoTypeForString("UNIT_SUIKA_BIG1_YOUKAI")
				newUnit1 = gc.getPlayer(caster.getOwner()).initUnit(TransformUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
				newUnit1.convert(caster)
				caster = newUnit1
	
		if CAL <= 3:
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_EASY'),True )
		elif CAL <= 7:
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_NORMAL'),True )
		elif CAL <= 11:
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_HARD'),True )
		else:
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_MISSING_POWER_LUNATIC'),True )
		caster.setNumTransformTime(CAL/8+2)
		#caster.changeMoves(-100)
	
		#caster.changeDamage(-100,caster.getOwner())
		caster.changeDamage( -caster.getDamage()/2  ,caster.getOwner())
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	caster.setNumCastSpellCard( caster.getNumCastSpellCard() + 1 )
	
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_SUIKA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if caster.isHuman() == False:
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
	
		estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
		if estimatePoint < 35:
			estimatePoint = 0
	
	else:
		pTeam = gc.getTeam(caster.getTeam())
		count = 0
		if Functions.isWar(caster.getOwner()):
			for iX in range(-1,2):
				for iY in range(-1,2):
					if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
						pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
						for i in range(pPlot.getNumUnits()):
							if pTeam.isAtWar( pPlot.getUnit(i).getTeam() ):
								count = count + 1
	
		estimatePoint = count * 5
		if estimatePoint < 30:
			estimatePoint = 0
	
	return estimatePoint




#こまち
def req_KOMACHI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_KOMACHI1','UNIT_KOMACHI6',cost)

def spellcard_KOMACHI1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iWidth = gc.getMap().getGridWidth()
	iHeight = gc.getMap().getGridHeight()
	RangeList = []
	
	for iX in range(iWidth):
		for iY in range(iHeight):
			RangeList.append([iX - caster.getX(),iY - caster.getY()])
	
	Functions.changeDamage(RangeList,caster,CAL*2,CAL*2,25,False,False,False,True,-1,False,True,True,True,-1,False,0,1,False,True)
	Functions.changeDamage(RangeList,caster,CAL,CAL,25,False,False,False,True,-1,True,False,True,True,-1,False,0,1,False,True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	caster.setNumSpellCardBreakTime( 2 )
	
	return True

def spellcard_KOMACHI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	iWidth = gc.getMap().getGridWidth()
	iHeight = gc.getMap().getGridHeight()
	RangeList = []
	
	for iX in range(iWidth):
		for iY in range(iHeight):
			RangeList.append([iX - caster.getX(),iY - caster.getY()])
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,int(CAL*(1+CAL*0.05)),int(CAL*(1+CAL*0.05)),0,False,False,False,True,-1,False,True,True,True,-1,False,0,1,True,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,int(CAL*(1+CAL*0.05)/2),int(CAL*(1+CAL*0.05)/2),0,False,False,False,True,-1,True,False,True,True,-1,False,0,1,True,True)
	
	estimatePoint = estimatePoint / (50.0 * (int(CAL*(1+CAL*0.05)))) * 100
	
	if estimatePoint < 40:
		estimatePoint = 0
	
	return estimatePoint





#めーりん
def req_MEIRIN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MEIRIN1','UNIT_MEIRIN6',cost)


def spellcard_MEIRIN1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL*2,CAL*5,0,True,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,CAL*2/2,CAL*5/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0)
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_NIJIIRONOHANABATAKE')): #すでに花畑があれば強化する
			pCity.setBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , pCity.getBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') ) + 1 )
			pCity.setBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , pCity.getBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') ) + 1 )
		else:
			pCity = pPlot.getPlotCity()
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_NIJIIRONOHANABATAKE'),1)
			pCity.setFlowerGardenTurn(10)
			pCity.setBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , 1 )
			pCity.setBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , 1 )
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_MEIRIN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*2,CAL*5,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*2/2,CAL*5/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*4)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint
	



#ゆかりん
def req_YUKARI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YUKARI1','UNIT_YUKARI6',cost) or Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YUKARI1_HAKUREI','UNIT_YUKARI6_HAKUREI',cost)
	

def spellcard_YUKARI1(caster,cost):


	CAL = caster.countCardAttackLevel()

	Functions.setPromotion(RangeList1,caster,'PROMOTION_DANMAKUKEKKAI',True,100,False,False,True,-1,True,True,True,True,-1,True,0,2,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_STAN',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_YUKARI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,100,100,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (100)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint





#
def req_KAGUYA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_KAGUYA1','UNIT_KAGUYA6',cost)


def spellcard_KAGUYA1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_EIYAGAESI) == True and caster.isHuman() == False:
		Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0)
	
	else:
		for i in range(TohoCivList.iMaxPlayer):
			pPlayer = gc.getPlayer(i)
			if pPlayer.isBarbarian() == False and pPlayer.isAlive() == True and caster.getTeam() != pPlayer.getTeam():
				AnarchyNum = CAL*8
				AnarchySum = 0
				while AnarchyNum > 100:
					pPlayer.changeAnarchyTurns(1)
					AnarchyNum -= 100
					AnarchySum +=1
				if gc.getGame().getSorenRandNum(100, "Kaguya Spell Card") < AnarchyNum:
					pPlayer.changeAnarchyTurns(1)
					AnarchySum+=1
				if AnarchySum > 0:
					CyInterface().addImmediateMessage(pPlayer.getName() + "&#12364;" + str(AnarchySum) + "&#12479;&#12540;&#12531;&#12398;&#38291;&#27704;&#36960;&#12398;&#26178;&#38291;&#12434;&#21051;&#12415;&#12414;&#12377;&#12290;","")
		
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_KAGUYA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_EIYAGAESI) == False:
		if Functions.isWar(caster.getOwner()):
			estimatePoint = 30
		else:
			estimatePoint = 5
	
		return estimatePoint
	
	else:
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
	
		estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
		if estimatePoint < 35:
			estimatePoint = 0
	
		return estimatePoint
	
	


#てんこ
def req_TENSHI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_TENSHI1','UNIT_TENSHI6',cost)

def spellcard_TENSHI1(caster,cost):

	RangeList = []
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					if pTeam.isAtWar( pCity.getTeam() ):
						iDamage = CAL*2 + gc.getGame().getSorenRandNum(CAL*2,"Tenshi Spell Card")
						pPlot.getPlotCity().changeDefenseDamage(iDamage)
						
						pPlot.getPlotCity().setNumRealBuilding(gc.getInfoTypeForString('BUILDING_WALLS'),0)
						pPlot.getPlotCity().setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CASTLE'),0)
						pPlot.getPlotCity().setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BUNKER'),0)
						pPlot.getPlotCity().setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BOMB_SHELTER'),0)
						
						pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
						
						RangeList.append([iX,iY])
				if pPlot.getPlotType() == PlotTypes.PLOT_PEAK:
					pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
	
	Functions.changeDamage(RangeList,caster,CAL*2,CAL*4,0,True,True,True,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList,caster,(CAL*2)/2,(CAL*4)/2,0,True,True,True,True,-1,True,False,True,True,-1,False,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_TENSHI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	RangeList = []
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					if pTeam.isAtWar( pCity.getTeam() ):
						estimatePoint = 100 - pCity.getDefenseDamage
						RangeList.append([iX,iY])
						tempNum = Functions.changeDamage(RangeList,caster,(CAL-8)*5,(CAL-8)*5,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
						estimatePoint = estimatePoint + (  tempNum / (AISpellCastBaseNum * (CAL-8)*8 ) * 100  )

	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint



#おりん
def req_RIN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_RIN1','UNIT_RIN6',cost)

def spellcard_RIN1(caster,cost):

	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	iNumUnit = 1 #log(0)になると－infになってしまい、それを回避するため
	
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIEFAIRY')):
			iNumUnit += 1
	iDamage = int(CAL*2 * ( math.log(iNumUnit,10) + 1 ) )
	
	Functions.changeDamage(RangeList1,caster,iDamage,iDamage,0,True,False,False,True,-1,False,True,True,True,-1,True,0)
	Functions.changeDamage(RangeList1,caster,iDamage/2,iDamage/2,0,True,False,False,True,-1,True,False,True,True,-1,True,0)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_RIN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	iNumUnit = 1 #log(0)になると－infになってしまい、それを回避するため
	
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIEFAIRY')):
			iNumUnit += 1
	iDamage = int(CAL*2 * ( math.log(iNumUnit,10) + 1 ) )
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,iDamage,iDamage,0,True,False,False,True,-1,False,True,True,True,-1,True,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,iDamage/2,iDamage/2,0,True,False,False,True,-1,True,False,True,True,-1,True,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (iDamage)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint



#レティ
def req_LETTY1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_LETTY1','UNIT_LETTY6',cost)
	

def spellcard_LETTY1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL*2,CAL*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,(CAL*2)/2,(CAL*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_FROST',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_FROST',True,50,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_LETTY1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*2,CAL*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,(CAL*2)/2,(CAL*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*2)) * 100
	
	return estimatePoint



#みま
def req_MIMA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MIMA1','UNIT_MIMA6',cost)

def spellcard_MIMA1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,False,False,False,True,-1,True,True,True,True,-1,True,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_MIMA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,False,False,False,True,-1,True,True,True,True,-1,True,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint




#えいき
def req_EIKI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_EIKI1','UNIT_EIKI6',cost)


def spellcard_EIKI1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	
	Functions.changeDamage(RangeList1,caster,50,50,1,False,False,True,True,-1,True,True,True,True,-1,True,0,3)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_SPELL_CASTED',True,100,False,True,True,-1,True,True,True,True,-1,False,0,5)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_EIKI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,50,50,1,False,False,True,True,-1,True,True,True,True,-1,True,0,3,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (20)) * 100
	
	if estimatePoint < 10:
		estimatePoint = 0
	
	return estimatePoint










def req_NAZRIN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_NAZRIN1','UNIT_NAZRIN6',cost)


def spellcard_NAZRIN1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL*2,CAL*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,CAL,CAL,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
	
	MetalList = ['BONUS_COPPER','BONUS_SILVER']
	if CAL >= 8:
		MetalList.append('BONUS_IRON')
		MetalList.append('BONUS_GOLD')
	if CAL >= 16:
		MetalList.append('BONUS_ALUMINUM')
	
	if caster.plot().getTeam() == caster.getTeam() and caster.plot().getPlotType() != PlotTypes.PLOT_OCEAN:
		metal = gc.getGame().getSorenRandNum(len(MetalList),"nazrin spell card")
		caster.plot().setBonusType(gc.getInfoTypeForString(MetalList[metal]))
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_NAZRIN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		if caster.plot().getTeam() == caster.getTeam() and caster.plot().getPlotType() != PlotTypes.PLOT_OCEAN:
			if caster.plot().getBonusType(caster.getTeam()) == -1:
				estimatePoint = 5
	else:
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*2,CAL*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL,CAL,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
		
		estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*2)) * 100
		
		if estimatePoint < 30:
			estimatePoint = 0
	
	return estimatePoint











def req_KOGASA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_KOGASA1','UNIT_KOGASA6',cost)


def spellcard_KOGASA1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL*2,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,CAL*2/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_HEAVY_RAIN',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_KOGASA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*2,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*2/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
	return estimatePoint










def req_ICHIRIN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_ICHIRIN1','UNIT_ICHIRIN6',cost)


def spellcard_ICHIRIN1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	limit = 100 - CAL*3
	
	Functions.changeDamage(RangeList1,caster,100,100,limit,False,False,False,True,-1,True,True,True,True,-1,True,0)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_SPELL_CASTED',True,100,False,True,True,-1,True,True,True,True,-1,False,0,5)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_ICHIRIN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	limit = 100 - CAL*3
	if limit < 0:
		limit = 0
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,100,100,limit,False,False,False,True,-1,True,True,True,True,-1,True,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (100-limit)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint










def req_MINAMITSU1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MINAMITSU1','UNIT_MINAMITSU6',cost)


def spellcard_MINAMITSU1(caster,cost):

	CAL = caster.countCardAttackLevel()
	RangeList = []
	
	for iX in range(-5,6):
		for iY in range(-5,6):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				RangeList.append([iX,iY])
	
	Functions.changeDamage(RangeList,caster,CAL*4,CAL*4,0,False,False,False,True,-1,False,True,True,True,-1,False,0,5)
	
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pPlot.getPlotCity().changeDefenseDamage(CAL*5)
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_MINAMITSU1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	RangeList = []
	pTeam = gc.getTeam(caster.getTeam())
	
	for iX in range(-5,6):
		for iY in range(-5,6):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				RangeList.append([iX,iY])
	
	Functions.changeDamage(RangeList,caster,CAL*4,CAL*4,0,False,False,False,True,-1,False,True,True,True,-1,False,0,5)
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,CAL*4,CAL*4,0,False,False,False,True,-1,False,True,True,True,-1,False,0,5,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*4)) * 100
	
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					if pTeam.isAtWar( pCity.getTeam() ):
						estimatePoint = (estimatePoint + ( 100 - pCity.getDefenseDamage ))
	
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint










def req_SYOU1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SYOU1','UNIT_SYOU6',cost)


def spellcard_SYOU1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_ABSOLUTE_JUSTICE')) < 1:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ABSOLUTE_JUSTICE'),1)
		
		iNumHappy = pCity.getBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_ABSOLUTE_JUSTICE') )
		iNumGold = pCity.getBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_ABSOLUTE_JUSTICE'),0)
		
		pCity.setBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_ABSOLUTE_JUSTICE') , iNumHappy + CAL/4 + 1 )
		pCity.setBuildingCommerceChange(gc.getInfoTypeForString('BUILDINGCLASS_ABSOLUTE_JUSTICE'),0 , iNumGold + CAL/2 + 3)
	
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False
	
def spellcard_SYOU1_Estimate(caster):

	estimatePoint = 0
	
	if caster.plot().isCity():
		estimatePoint = 20
		if caster.plot().getPlotCity().isCapital():
			estimatePoint = 1000

	return estimatePoint










def req_BYAKUREN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_BYAKUREN1','UNIT_BYAKUREN6',cost)


def spellcard_BYAKUREN1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL1',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL2',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL3',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL4',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL5',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL6',False,100,True,True,True,-1,True,True,True,True,-1,True)

	if CAL <= 3:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL1',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 7:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL2',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 11:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL3',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 15:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL4',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 19:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL5',True,100,True,False,False,-1,False,True,True,True,-1,True)
	else:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_AIR_SCROLL6',True,100,True,False,False,-1,False,True,True,True,-1,True)
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_BYAKUREN1_Estimate(caster):

	estimatePoint = 0
	
	if Functions.isWar(caster.getOwner()):
		pPlot = caster.plot()
		count = 0
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getTeam() == caster.getTeam() and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				count = count + 1
		estimatePoint = count

	return estimatePoint










def req_NUE1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_NUE1','UNIT_NUE6',cost)


def spellcard_NUE1(caster,cost):

	CAL = caster.countCardAttackLevel()
	pPlayer = gc.getPlayer(caster.getOwner())
	
	if CAL < 2:
		CAL = 2
	
	#UFO登場
	for i in range(SummonBaseNum[CAL]):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString( 'UNIT_RED_UFO' ), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setSpecialNumber( CAL*2/3-1 )
		#戦闘力更新用
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
	
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString( 'UNIT_BLUE_UFO' ), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString( 'UNIT_GREEN_UFO' ), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_NUE1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = 30
	
	return estimatePoint








#芳香

def req_YOSHIKA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YOSHIKA1','UNIT_YOSHIKA6',cost)

def spellcard_YOSHIKA1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,CAL/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		
	Functions.setPromotion(RangeList1,caster,'PROMOTION_ZOMBIE_POISON',True,CAL*8,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_YOSHIKA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL,CAL*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,(CAL)/2,(CAL*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*2)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint








#青娥

def req_SEIGA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SEIGA1','UNIT_SEIGA6',cost)

def spellcard_SEIGA1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_KYOURAN1',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_KYOURAN2',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_KYOURAN3',False,100,True,True,True,-1,True,True,True,True,-1,True)
	
	if CAL <= 7:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_KYOURAN1',True,100,True,False,False,-1,False,True,True,True,-1,True)
	elif CAL <= 15:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_KYOURAN2',True,100,True,False,False,-1,False,True,True,True,-1,True)
	else:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_KYOURAN3',True,100,True,False,False,-1,False,True,True,True,-1,True)
		
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					if caster.isHuman():
						pPlot.getPlotCity().changeOccupationTimer(1)
					else:
						pPlot.getPlotCity().changeDefenseDamage(150)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_SEIGA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	
	for iX in range(-1,2):
		for iY in range(-1,2):
			if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
				pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					if pTeam.isAtWar( pCity.getTeam() ):
						if caster.isHuman():
							pCity.changeOccupationTimer(1)
						else:
							pCity.changeDefenseDamage(150)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*2)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0

	return estimatePoint









#屠自古

def req_TOJIKO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_TOJIKO1','UNIT_TOJIKO6',cost)

def spellcard_TOJIKO1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,0,CAL*4,0,False,False,False,True,-1,True,True,True,True,-1,True,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_TOJIKO1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,0,CAL*4,0,False,False,False,True,-1,True,True,True,True,-1,True,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*4)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint








#布都

def req_FUTO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_FUTO1','UNIT_FUTO6',cost)

def spellcard_FUTO1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	if caster.isHuman() == False:
		Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0)
	
	else:
		if caster.plot().getTeam() == caster.getTeam():
			for iX in range(-1,2):
				for iY in range(-1,2):
					if CAL <= 11:
						if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
							pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
							if pPlot.getPlotType() == PlotTypes.PLOT_PEAK:
								pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_RYUMYAKU'))
					else:
						if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
							pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
							if pPlot.getPlotType() == PlotTypes.PLOT_PEAK:
								pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_RYUMYAKU'))
							if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RYUMYAKU'):
								gc.getGame().setPlotExtraYield(pPlot.getX(),pPlot.getY(),1,CAL/12)
			iX = caster.getX()
			iY = caster.getY()
			gc.getGame().setPlotExtraYield(iX,iY,2,CAL/10+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_FUTO1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if caster.isHuman() == False:
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
	
		estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
		if estimatePoint < 35:
			estimatePoint = 0
	
	else:
		if caster.plot().isCity():
			estimatePoint = 20
			if caster.plot().getPlotCity().isCapital():
				estimatePoint = 1000
	
	return estimatePoint

def help_FUTO1(szText, caster, CAL):

	CvGameUtils.doprint(szText)
	if szText == "001":
		return CAL/12
	if szText == "002":
		return CAL/10+1





#神子

def req_MIMIMIKO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_MIMIMIKO1','UNIT_MIMIMIKO6',cost)

def spellcard_MIMIMIKO1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_ATUMARU_SHINREI1',False,100,True,True,True,-1,True,True,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_ATUMARU_SHINREI2',False,100,True,True,True,-1,True,True,True,True,-1,True)
	
	if CAL <= 15:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_ATUMARU_SHINREI1',True,100,True,False,False,-1,False,True,True,True,-1,True)
	else:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_ATUMARU_SHINREI2',True,100,True,False,False,-1,False,True,True,True,-1,True)
	
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	
	pPlayer.changeGoldenAgeTurns( CAL/8 + 1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_MIMIMIKO1_Estimate(caster):
	
	estimatePoint = 0
	
	if Functions.isWar(caster.getOwner()):
		pPlot = caster.plot()
		count = 0
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getTeam() == caster.getTeam() and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				count = count + 1
		estimatePoint = count

	return estimatePoint

#八橋

def req_YATUHASHI1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YATUHASHI1','UNIT_YATUHASHI6',cost)

def spellcard_YATUHASHI1(caster,cost):

	CALA = caster.countCardAttackLevel()
	pPlot = caster.plot()

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if gc.getInfoTypeForString('UNIT_BENBEN1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_BENBEN6'):
			if caster.getTeam() == pPlot.getUnit(i).getTeam():
				break

	if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BENBEN')):
		#以下、弁々がいる場合の処理
		if (pUnit.getPower()>=cost) and (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')) == False):
			CALB = pUnit.countCardAttackLevel()
			spelldam = (CALA + CALB)/2
			#周囲2マス内に都市がある場合、文化防御を減少させる
			for iX in range(-2,3):
				for iY in range(-2,3):
					if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
						pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
						if pPlot.isCity():
							pPlot.getPlotCity().changeDefenseDamage(150)
			#ダメージ処理。威力は八橋と弁々のCALを足して2で割った数で変動
			Functions.changeDamage(RangeList2,caster,spelldam*4,spelldam*8,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
			Functions.changeDamage(RangeList2,caster,(spelldam*4)/2,(spelldam*8)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
			
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			caster.setPower(caster.getPower()-cost)
			pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			pUnit.setPower(pUnit.getPower()-cost)
			pUnit.setNumAcquisSpellPromotion(pUnit.getNumAcquisSpellPromotion()+1)
		
		else:
			#弁々は居るが、向こうが撃てる状況ではない場合の処理
			Functions.changeDamage(RangeList1,caster,CALA,CALA*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
			Functions.changeDamage(RangeList1,caster,CALA/2,(CALA*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			caster.setPower(caster.getPower()-cost)
		
	else:
		#弁々が居ない場合の処理
		Functions.changeDamage(RangeList1,caster,CALA,CALA*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList1,caster,CALA/2,(CALA*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_YATUHASHI1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,False,False,False,True,-1,True,True,True,True,-1,True,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint

#べんべん

def req_BENBEN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_BENBEN1','UNIT_BENBEN6',cost)

def spellcard_BENBEN1(caster,cost):

	CALB = caster.countCardAttackLevel()
	pPlot = caster.plot()

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if gc.getInfoTypeForString('UNIT_YATUHASHI1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_YATUHASHI6'):
			if caster.getTeam() == pPlot.getUnit(i).getTeam():
				break

	if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATUHASHI')):
		#以下、八橋がいる場合の処理
		if (pUnit.getPower()>=cost) and (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')) == False):
			CALA = pUnit.countCardAttackLevel()
			spelldam = (CALA + CALB)/2
			#周囲2マス内に都市がある場合、文化防御を減少させる
			for iX in range(-2,3):
				for iY in range(-2,3):
					if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
						pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
						if pPlot.isCity():
							pPlot.getPlotCity().changeDefenseDamage(150)
			#ダメージ処理。威力は八橋と弁々のCALを足して2で割った数で変動
			Functions.changeDamage(RangeList2,caster,spelldam*4,spelldam*8,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
			Functions.changeDamage(RangeList2,caster,(spelldam*4)/2,(spelldam*8)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
			
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			caster.setPower(caster.getPower()-cost)
			pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			pUnit.setPower(pUnit.getPower()-cost)
			pUnit.setNumAcquisSpellPromotion(pUnit.getNumAcquisSpellPromotion()+1)
		
		else:
			#八橋は居るが、向こうが撃てる状況ではない場合の処理
			Functions.changeDamage(RangeList1,caster,CALB,CALB*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
			Functions.changeDamage(RangeList1,caster,CALB/2,(CALB*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			caster.setPower(caster.getPower()-cost)
		
	else:
		#八橋が居ない場合の処理
		Functions.changeDamage(RangeList1,caster,CALB,CALB*2,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList1,caster,CALB/2,(CALB*2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_BENBEN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,False,False,False,True,-1,True,True,True,True,-1,True,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint

#正邪

def req_SEIJA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SEIJA1','UNIT_SEIJA6',cost)

def spellcard_SEIJA1(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	if CAL <= 11:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_SOUSA_HANTEN_A',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_SOUSA_HANTEN_B',True,100,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	else:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_SOUSA_HANTEN_A',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_JOUGE_HANTEN_A',True,100,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_SOUSA_HANTEN_B',True,100,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_JOUGE_HANTEN_B',True,100,False,False,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					if pPlot.isCity():
						pPlot.getPlotCity().changeOccupationTimer( CAL/6 )
						
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_SEIJA1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,20+CAL*3,20+CAL*3,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,(20+CAL*3)/2,(20+CAL*3)/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (20+CAL*3)) * 100
	
	if estimatePoint < 30:
		estimatePoint = 0
	
	return estimatePoint

#しんみょうまる

def req_SHINMYOUMARU1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SHINMYOUMARU1','UNIT_SHINMYOUMARU6',cost)

def spellcard_SHINMYOUMARU1(caster,cost):

	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()

	#AIの場合はケロちゃんと同等の効果に
	#ただしその場合も効力自体はケロちゃんの下位互換
	if caster.isHuman():
		if caster.plot().getTeam() == caster.getTeam():
			gc.getGame().setPlotExtraYield(iX,iY,0,CAL/16)
			gc.getGame().setPlotExtraYield(iX,iY,1,CAL/12)
			gc.getGame().setPlotExtraYield(iX,iY,2,CAL/8)
			if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_COAST') and \
			pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_OCEAN') and \
			caster.plot().isCity() == False:
				if CAL <= 7:
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KARIGURASHI_CAL1to7'))
				elif CAL <= 15:
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KARIGURASHI_CAL8to15'))
				else:
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KARIGURASHI_CAL16over'))
			else:
				return FALSE
	else:
		gc.getGame().setPlotExtraYield(iX,iY,0,CAL/10)
		gc.getGame().setPlotExtraYield(iX,iY,1,CAL/8)
		gc.getGame().setPlotExtraYield(iX,iY,2,CAL/6+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

### ここにこれを書けたらうれしくないかなって
### Pythonで書ける式ならなんでも出せる、なんならスペル本体から計算式をコピペしたっていい
### casterを取ってはいるが、ゲーム中でない場合(ペディア経由)は中身がNoneなのできをつける
### ゲーム外経由でもCALは渡ってくるので、計算に使える
### SpellListの評価値関数と消費Powerの間に名前を入れて、
### 説明に[p***]と書いておくと、***の部分がszTextに渡ってくる
### この機能いらない場合はNoneを入れる、その場合でもデフォルトの置換・古い置換はいままでどおりはたらく
### TODO: いっそ数字だけじゃなくて文字列も返せるようにしてしまってはどうか
def help_SHINMYOUMARU1(szText, caster, CAL):

	CvGameUtils.doprint(szText)
	if szText == "001":
		return CAL/16
	if szText == "002":
		return CAL/12
	if szText == "003":
		return CAL/8

def spellcard_SHINMYOUMARU1_Estimate(caster):

	estimatePoint = 0
	
	if caster.plot().isCity():
		estimatePoint = 20
		if caster.plot().getPlotCity().isCapital():
			estimatePoint = 1000

	return estimatePoint

#雷鼓

def req_RAIKO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_RAIKO1','UNIT_RAIKO6',cost)

def spellcard_RAIKO1(caster,cost):

	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = caster.plot()
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	TAIKOFlag = False
	TYUUSEIFlag = False
	KINDAIFlag = False
	GENDAIFlag = False
	
	#時代によって沸かせるユニットや計算式を変動させる
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TAIKO')
		iNumCityCountKOU = 3
		TAIKOFlag = True
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TYUUSEI')
		iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_TYUUSEI')
		iNumCityCountKOU = 5
		iNumCityCountOTU = 8
		TYUUSEIFlag = True
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL'):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_KINDAI')
		iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_KINDAI')
		iNumCityCountKOU = 5
		iNumCityCountOTU = 8
		KINDAIFlag = True
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_RAIKOONLY')
		iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_RAIKOONLY')
		iNumCityCountKOU = 5
		iNumCityCountOTU = 8
		GENDAIFlag = True
	
	if caster.plot().getTeam() == caster.getTeam():
		if pPlot.isCity():
			pCity = pPlot.getPlotCity()
			if TAIKOFlag == True:
				iNumKOU = pCity.getPopulation() / iNumCityCountKOU
				if iNumKOU > 2:
					iNumKOU = 2
				iNumOTU = 0
		
			elif TYUUSEIFlag == True:
				iNumKOU = pCity.getPopulation() / iNumCityCountKOU
				if iNumKOU < 1:
					iNumKOU = 1
				if iNumKOU > 3:
					iNumKOU = 3

				iNumOTU = pCity.getPopulation() / iNumCityCountOTU
				if iNumOTU < 1:
					iNumOTU = 0
				if iNumOTU > 1:
					iNumOTU = 1
		
			elif KINDAIFlag == True:
				iNumKOU = pCity.getPopulation() / iNumCityCountKOU
				if iNumKOU < 1:
					iNumKOU = 1
				if iNumKOU > 3:
					iNumKOU = 3
			
				iNumOTU = pCity.getPopulation() / iNumCityCountOTU
				if iNumOTU < 1:
					iNumOTU = 1
				if iNumOTU > 3:
					iNumOTU = 3
			
			else:
				iNumKOU = pCity.getPopulation() / iNumCityCountKOU
				if iNumKOU < 1:
					iNumKOU = 1
				if iNumKOU > 3:
					iNumKOU = 3
			
				iNumOTU = pCity.getPopulation() / iNumCityCountOTU
				if iNumOTU < 1:
					iNumOTU = 1
				if iNumOTU > 3:
					iNumOTU = 3
		
			if iNumKOU >= 1:
				for i in range(iNumKOU):
					newUnit = pPlayer.initUnit(iUnitKOU, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if iNumOTU >= 1:
				for i in range(iNumOTU):
					newUnit = pPlayer.initUnit(iUnitOTU, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	iRaikoRocketNum = SummonBaseNum[CAL/2]
	if iRaikoRocketNum < 1:
		iRaikoRocketNum = 1
	if iRaikoRocketNum > 5:
		iRaikoRocketNum = 5
	
	for i in range(iRaikoRocketNum):
		if CAL<=4:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RAIKO_ROCKET_TYPE1'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL<=9:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RAIKO_ROCKET_TYPE2'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL<=15:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RAIKO_ROCKET_TYPE3'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RAIKO_ROCKET_TYPE4'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_RAIKO1_Estimate(caster):

	estimatePoint = 0
	
	if caster.plot().isCity():
		estimatePoint = 10
		if caster.plot().getPlotCity().isCapital():
			estimatePoint = 15
	
	else:
		CAL = caster.countCardAttackLevel()
		pTeam = gc.getTeam(caster.getTeam())
		count =0
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					if pPlot.isCity():
						for i in range(pPlot.getNumUnits()):
							if pTeam.isAtWar( pPlot.getUnit(i).getTeam() ):
								count = count + 1
		estimatePoint = count * 5
		
		if estimatePoint < 50:
			estimatePoint = 0

	return estimatePoint

#よりひめ

def req_YORIHIME1(bTestVisible,caster,sCAL,eCAL,cost):
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_YORIHIME1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_YORIHIME6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
			if caster.getPower() >= cost:
				if gc.getPlayer(caster.getOwner()).getAmenouzumeFlag() == 1:
					return True
	return False

def spellcard_YORIHIME1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = caster.plot()
	RangeList = []
	sokushiUnits = []
	
	if pPlayer.getAmenouzumeFlag() == 1:
		iWidth = gc.getMap().getGridWidth()
		iHeight = gc.getMap().getGridHeight()
		for iX in range(iWidth):
			for iY in range(iHeight):
				RangeList.append([iX - caster.getX(),iY - caster.getY()])
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					if caster.getTeam() != pCity.getTeam() and pTeam.isAtWar(pCity.getTeam()) == True:
						pCity.changeDefenseDamage(500)
		
		Functions.changeDamage(RangeList,caster,-100,-100,100,False,True,False,False,-1,True,True,True,True,-1,True,1)
		Functions.changeDamage(RangeList,caster,CAL*3,CAL*6,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList,caster,(CAL*3)/2,(CAL*6)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)

		for iX in range(iWidth):
			for iY in range(iHeight):
				pPlot = gc.getMap().plot(iX,iY)
				for i in range(pPlot.getNumUnits()):
					pTeam = gc.getTeam(caster.getTeam())
					pUnit = pPlot.getUnit(i)
					if caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == True:
						if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
							if (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REMILIA')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FLAN')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YOUMU')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YUYUKO')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIMA')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MINAMITSU')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YOSHIKA')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOJIKO')) ):
								sokushiUnits.append(pUnit)
						else:
							if (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ZOMBIEFAIRY')) or
								pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KYONSHII')) ):
								sokushiUnits.append(pUnit)
		for pUnit in sokushiUnits:
			pUnit.changeDamage(100, pUnit.getOwner())

		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setPower(caster.getPower()-cost)
		pPlayer.setAmenouzumeFlag(0)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_YORIHIME1_Estimate(caster):


	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iWidth = gc.getMap().getGridWidth()
	iHeight = gc.getMap().getGridHeight()
	RangeList = []
	
	for iX in range(iWidth):
		for iY in range(iHeight):
			RangeList.append([iX - caster.getX(),iY - caster.getY()])
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,int(CAL*(1+CAL*0.05)),int(CAL*(1+CAL*0.15)),0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList,caster,int(CAL*(1+CAL*0.05)/2),int(CAL*(1+CAL*0.15)/2),0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (50.0 * (int(CAL*(1+CAL*0.05)))) * 100
	
	if estimatePoint < 50:
		estimatePoint = 0
	if pPlayer.getAmenouzumeFlag() == 0:
		estimatePoint = 0
	
	return estimatePoint

def help_YORIHIME1(szText, caster, CAL):

	CvGameUtils.doprint(szText)
	if szText == "001":
		return CAL*3
	if szText == "002":
		return CAL*6
	if szText == "CAUama":
		if caster:
			iPlayer = caster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.getAmenouzumeFlag() == 1:
				return u""
			else:
				return u"降神『天宇受賣命』の使用が必要"
		else:
			return u""

def req_YORIHIME2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spellcard_YORIHIME2(caster,cost):

	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList3,caster,3+CAL,10+CAL*5/2,1,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList3,caster,(3+CAL)/2,(10+CAL*5/2)/2,1,False,False,False,True,-1,True,False,True,True,-1,False,0)

	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def spellcard_YORIHIME2_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList3,caster,3+CAL,10+CAL*5/2,0,False,False,False,True,-1,False,True,True,True,-1,False,0,0,True)
	estimatePoint = estimatePoint + Functions.changeDamage(RangeList3,caster,(3+CAL)/2,(10+CAL*5/2)/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0,0,True)
	
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (6+CAL*2)) * 100
	
	if estimatePoint < 40:
		estimatePoint = 0
	
	return estimatePoint

def help_YORIHIME2(szText, caster, CAL):

	CvGameUtils.doprint(szText)
	if szText == "001":
		return 3+CAL
	if szText == "002":
		return 10+CAL*5/2

def req_YORIHIME3(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spellcard_YORIHIME3(caster,cost):
	
	SigenList = ['BONUS_HORSE','BONUS_COW','BONUS_SILK']
	pPlot = caster.plot()
	iBonus = pPlot.getBonusType(caster.getTeam())
	
	if pPlot.getTeam() == caster.getTeam() and pPlot.getPlotType() != PlotTypes.PLOT_OCEAN:
		for i in range(len(SigenList)):
			if iBonus == gc.getInfoTypeForString(SigenList[i]):
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_RICE'))
				pPlot.setImprovementType(-1)
				caster.setPower(caster.getPower() - cost)
				break
			elif iBonus == -1:
				sigen = gc.getGame().getSorenRandNum(len(SigenList),"yorihime spell card")
				pPlot.setBonusType(gc.getInfoTypeForString(SigenList[sigen]))
				pPlot.setImprovementType(-1)
				caster.setPower(caster.getPower() - cost)
				break
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_YORIHIME3_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	SigenList = ['BONUS_HORSE','BONUS_COW','BONUS_SILK']
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iBonus = pPlot.getBonusType(caster.getTeam())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
	
	for i in range(iNumTeam):
		ppTeam = gc.getTeam(i)
		if ppTeam.isBarbarian() == False:
			if not pTeam.isAtWar(i):
				estimatePoint = estimatePoint + 100
	
	if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
		estimatePoint = estimatePoint + 50
	
	if iBonus == gc.getInfoTypeForString('BONUS_SILK'):
		estimatePoint = estimatePoint + 50
	
	if pPlot.getImprovementType() != -1:
		estimatePoint = estimatePoint - 50
	
	if estimatePoint < 110:
		estimatePoint = 0
	
	return estimatePoint



#姉の方

def req_TOYOHIME1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_TOYOHIME1','UNIT_TOYOHIME6',cost)

def spellcard_TOYOHIME1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	if CAL <= 7:
		Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
	elif CAL <= 15:
		Functions.changeDamage(RangeList2,caster,CAL*3,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList2,caster,CAL*3/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getTeam()):
			if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_GRASS'):
				pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			pPlot.setFeatureType(-1, 0)
			pPlot.resetFeatureModel()
			pPlot.setImprovementType(-1)
	elif CAL <= 19:
		Functions.changeDamage(RangeList3,caster,CAL*3,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList3,caster,CAL*3/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getTeam()):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_DESERT'),True,True)
			pPlot.setFeatureType(-1, 0)
			pPlot.resetFeatureModel()
			pPlot.setImprovementType(-1)
	else:
		Functions.changeDamage(RangeList3,caster,CAL*3,CAL*3,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
		Functions.changeDamage(RangeList3,caster,CAL*3/2,CAL*3/2,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getTeam()):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_DESERT'),True,True)
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FALLOUT'),1)
			pPlot.resetFeatureModel()
			pPlot.setImprovementType(-1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_TOYOHIME1_Estimate(caster):


	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	if CAL <= 8:
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
	elif CAL <= 16:
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList2,caster,CAL*2,CAL*2,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList2,caster,CAL,CAL,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
		if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getTeam()):
			estimatePoint = +5
	else:
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList3,caster,CAL,CAL,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
		estimatePoint = estimatePoint + Functions.changeDamage(RangeList3,caster,CAL/2,CAL/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
		if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getTeam()):
			estimatePoint = +5
	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
	
	if estimatePoint < 40:
		estimatePoint = 0
	
	return estimatePoint

#せーらん

def req_SEIRAN1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SEIRAN1','UNIT_SEIRAN6',cost)

def spellcard_SEIRAN1(caster,cost):
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV1',False,100,True,False,False,-1,True,False,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV2_TURN1',False,100,True,False,False,-1,True,False,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV2_TURN2',False,100,True,False,False,-1,True,False,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV3_TURN1',False,100,True,False,False,-1,True,False,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV3_TURN2',False,100,True,False,False,-1,True,False,True,True,-1,True)
	Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV3_TURN3',False,100,True,False,False,-1,True,False,True,True,-1,True)
	
	
	if CAL <= 8:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV1',True,100,True,False,False,-1,True,False,True,True,-1,True,0,0,False,False,-1,+1)
	elif CAL <= 16:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV2_TURN2',True,100,True,False,False,-1,True,False,True,True,-1,True,0,0,False,False,-1,+1)
	else:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_LUNATICGUN_LV3_TURN3',True,100,True,False,False,-1,True,False,True,True,-1,True,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_SEIRAN1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = estimatePoint + 30
	
	for iiX in range(iX-2,iX+3):
		for iiY in range(iY-2,iY+3):
			pPlot = gc.getMap().plot(iiX,iiY)
			pUnit = pPlot.getUnit(i)
			if caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == True:
				estimatePoint = estimatePoint + pUnit
	
	if estimatePoint < 35:
		estimatePoint = 0
	
	return estimatePoint

#おりんご

def req_RINGO1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_RINGO1','UNIT_RINGO6',cost)

def spellcard_RINGO1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	setFever = (CAL/4)+1
	
	UnitList = []
	iNumUnit = pPlot.getNumUnits()
	for i in range(iNumUnit):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_WORKER'):
			if pUnit.getTeam() == caster.getTeam():
				if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER')) or \
				not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER')):
					UnitList.append(pUnit)
	
	if len(UnitList) != 0:
		iLoopNum = setFever
		if iLoopNum > len(UnitList):
			iLoopNum = len(UnitList)
		for i in range(iLoopNum):
			iRandNum = gc.getGame().getSorenRandNum(len(UnitList),"Ringo Spell")
			pUnit = UnitList.pop(iRandNum)
			if CAL <= 11:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),True)
			else:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#def spellcard_RINGO1_Estimate(caster):
#
#	ちょっと扱いに悩んでいるためひとまずコメントアウト
#	
#	estimatePoint = 0
#	CAL = caster.countCardAttackLevel()
#	
#	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3,CAL*3,0,True,False,True,True,-1,False,True,True,True,-1,False,0,0,True)
#	estimatePoint = estimatePoint + Functions.changeDamage(RangeList1,caster,CAL*3/2,CAL*3/2,0,True,False,True,True,-1,True,False,True,True,-1,False,0,0,True)
#	
#	estimatePoint = estimatePoint / (AISpellCastBaseNum * (CAL*3)) * 100
#	
#	if estimatePoint < 35:
#		estimatePoint = 0
#	
#	return estimatePoint

def help_RINGO1(szText, caster, CAL):

	CvGameUtils.doprint(szText)
	if szText == "001":
		return (CAL/4)+1

#どれみ

def req_DOREMY1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_DOREMY1','UNIT_DOREMY6',cost)

def spellcard_DOREMY1(caster,cost):

	CAL = caster.countCardAttackLevel()
	pPlayer = gc.getPlayer(caster.getOwner())
	pMap = gc.getMap()
	iWidth = pMap.getGridWidth()
	iHeight = pMap.getGridHeight()
	
	CombatBase = CAL
	CombatYith = CombatBase
	CombatShub = CombatBase*2/3
	CombatSpiral = CombatBase*4/5
	Summon = CAL/4
	
	if Summon > 20:#WBでも入れない限りこの条件満たさないだろうけど、まあ一応
		Summon = 20
	if Summon < 1:
		Summon = 1
	if CombatBase > 32:
		CombatBase = 32
	if CombatYith < 2:
		CombatYith = 2
	if CombatShub < 2:
		CombatShub = 2
	if CombatSpiral < 2:
		CombatSpiral = 2
	
	for iX in range(iWidth):
		for iY in range(iHeight):
			pPlot = gc.getMap().plot(iX,iY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_GREAT_RACE_OF_YITH'):
					pUnit.setSpecialNumber(CombatYith -1)
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_SHUB-NIGGURATH'):
					pUnit.setSpecialNumber(CombatShub -1)
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_SPIRAL_KING'):
					pUnit.setSpecialNumber(CombatSpiral -1)
				#戦闘力更新用
				pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
				pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
	
	#イスの偉大なる種族
	for i in range(SummonBaseNum[Summon +1]):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString( 'UNIT_GREAT_RACE_OF_YITH' ), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setSpecialNumber( CombatYith-1 )
		#戦闘力更新用
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
	
	#シュブ＝ニグラス
	for i in range(SummonBaseNum[Summon -1]):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString( 'UNIT_SHUB-NIGGURATH' ), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setSpecialNumber( CombatShub-1 )
		#戦闘力更新用
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
	
	#螺旋の王
	for i in range(SummonBaseNum[Summon -1]):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString( 'UNIT_SPIRAL_KING' ), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setSpecialNumber( CombatSpiral-1 )
		#戦闘力更新用
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def spellcard_DOREMY1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = 100
	
	return estimatePoint

def help_DOREMY1(szText, caster, CAL):

	CombatBase = CAL
	CombatYith = CombatBase
	CombatShub = CombatBase*2/3
	CombatSpiral = CombatBase*4/5
	Summon = CAL/4
	
	if Summon > 20:
		Summon = 20
	if Summon < 1:
		Summon = 1
	if CombatBase > 32:
		CombatBase = 32
	if CombatYith < 2:
		CombatYith = 2
	if CombatShub < 2:
		CombatShub = 2
	if CombatSpiral < 2:
		CombatSpiral = 2

	CvGameUtils.doprint(szText)
	if szText == "001":
		return ( CombatShub )
	if szText == "010":
		return (Summon -1)
	if szText == "002":
		return ( CombatYith )
	if szText == "020":
		return (Summon +1)
	if szText == "003":
		return ( CombatSpiral )
	if szText == "030":
		return (Summon -1)

#さぐめ

def req_SAGUME1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_SpellCard(bTestVisible,caster,sCAL,eCAL,'UNIT_SAGUME1','UNIT_SAGUME6',cost)

def spellcard_SAGUME1(caster,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]):
		if CAL<=7:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_1'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL<=14:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_2'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif CAL<=20:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_3'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_4'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spellcard_SAGUME1_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	
	if Functions.isWar(caster.getOwner()):
		estimatePoint = 100
	
	return estimatePoint



#ここからスペル


#蓬莱の薬を取得
def req_GET_HOURAINOKUSURI_EASY(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_EASY') and pUnit.getDamage()==0:
			TohoFlag = False
			iiUnit = caster.getUnitType()
			for sTohoUnit in TohoUnitList.TohoUnitList:
				if iiUnit == gc.getInfoTypeForString(sTohoUnit):
					TohoFlag = True
			if TohoFlag == False:
				return True
	
	return False

def spell_GET_HOURAINOKUSURI_EASY(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_EASY') and pUnit.getDamage()==0:
			pUnit.changeDamage(100,iPlayer)
			caster.changeDamage(-65,iPlayer)
			break
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	

def req_GET_HOURAINOKUSURI_NORMAL(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_NORMAL') and pUnit.getDamage()==0:
			TohoFlag = False
			iiUnit = caster.getUnitType()
			for sTohoUnit in TohoUnitList.TohoUnitList:
				if iiUnit == gc.getInfoTypeForString(sTohoUnit):
					TohoFlag = True
			if TohoFlag == False:
				return True
	
	return False

def spell_GET_HOURAINOKUSURI_NORMAL(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_NORMAL') and pUnit.getDamage()==0:
			pUnit.changeDamage(100,iPlayer)
			caster.changeDamage(-100,iPlayer)
			break
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def req_GET_HOURAINOKUSURI_HARD(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_HARD') and pUnit.getDamage()==0:
			TohoFlag = False
			iiUnit = caster.getUnitType()
			for sTohoUnit in TohoUnitList.TohoUnitList:
				if iiUnit == gc.getInfoTypeForString(sTohoUnit):
					TohoFlag = True
			if TohoFlag == False:
				return True
	
	return False

def spell_GET_HOURAINOKUSURI_HARD(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_HARD') and pUnit.getDamage()==0:
			pUnit.changeDamage(100,iPlayer)
			caster.changeDamage(-100,iPlayer)
			caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MARCH'),True)
			break
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def req_GET_HOURAINOKUSURI_LUNATIC(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_LUNATIC') and pUnit.getDamage()==0:
			TohoFlag = False
			iiUnit = caster.getUnitType()
			for sTohoUnit in TohoUnitList.TohoUnitList:
				if iiUnit == gc.getInfoTypeForString(sTohoUnit):
					TohoFlag = True
			if TohoFlag == False:
				return True
	
	return False

def spell_GET_HOURAINOKUSURI_LUNATIC(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HOURAINOKUSURI_LUNATIC') and pUnit.getDamage()==0:
			pUnit.changeDamage(100,iPlayer)
			caster.changeDamage(-100,iPlayer)
			caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MARCH'),True)
			caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REVIVAL'),True)
			break
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def spell_GET_HOURAINOKUSURI_Estimate(caster):

	if caster.baseMoves() <= 0:
		return 0

	if caster.getDamage()>50:
		return 1000
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_REVIVAL')) == False:
		return 1000
		






#ミステリウムを拾う
def req_GET_MYSTERYIUM(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_MYSTERYIUM') and pUnit.getDamage()==0:
			return True
	
	return False

def spell_GET_MYSTERYIUM(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	py = PyPlayer(iPlayer)
	iX = caster.getX()
	iY = caster.getY()
	
	print "OKKK"
	
	pPlot = gc.getMap().plot(iX,iY)
	UnitNum = pPlot.getNumUnits()
	for iUnit in range(UnitNum):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_MYSTERYIUM') and pUnit.getDamage()==0:
			pUnit.changeDamage(100,iPlayer)
			
			BonusList = []
			if pPlayer.getMysteryiumFlag() == 0:
				if caster.getUnitType() == gc.getInfoTypeForString('UNIT_PROPHET'):
					for i in range(2):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_JEWISH_MISSIONARY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHRISTIAN_MISSIONARY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ISLAMIC_MISSIONARY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HINDU_MISSIONARY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_BUDDHIST_MISSIONARY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CONFUCIAN_MISSIONARY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TAOIST_MISSIONARY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)
					caster.changeDamage(100,iPlayer)
					
				if caster.getUnitType() == gc.getInfoTypeForString('UNIT_ARTIST'):
					BonusList.append(['BUILDING_PALACE','BUILDINGCLASS_PALACE',1,0,12])
					BonusList.append(['BUILDING_PALACE','BUILDINGCLASS_PALACE',1,2,12])
					pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)
					caster.changeDamage(100,iPlayer)
					#CyInterface().addImmediateMessage("&#12362;&#12420;&#12289;" + pPlayer.getCivilizationDescription(iPlayer) + "&#12398;" + gc.getBuildingInfo(gc.getInfoTypeForString('BUILDING_PALACE')).getDescription() + "&#12398;&#27096;&#23376;&#12364;&#8230;&#65311;" ,"")
					
				if caster.getUnitType() == gc.getInfoTypeForString('UNIT_SCIENTIST'):
					pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength())
					pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)
					caster.changeDamage(100,iPlayer)
					
				if caster.getUnitType() == gc.getInfoTypeForString('UNIT_MERCHANT'):
					BonusList.append(['BUILDING_PALACE','BUILDINGCLASS_PALACE',1,0,20])
					pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)
					caster.changeDamage(100,iPlayer)
					#CyInterface().addImmediateMessage("&#12362;&#12420;&#12289;" + pPlayer.getCivilizationDescription(iPlayer) + "&#12398;" + gc.getBuildingInfo(gc.getInfoTypeForString('BUILDING_PALACE')).getDescription() + "&#12398;&#27096;&#23376;&#12364;&#8230;&#65311;" ,"")
				
				if caster.getUnitType() == gc.getInfoTypeForString('UNIT_ENGINEER'):
					pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength())
					pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)
					caster.changeDamage(100,iPlayer)
					
				if caster.getUnitType() == gc.getInfoTypeForString('UNIT_GREAT_SPY'):
					for i in range(10):
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SPY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MORALE'),True)
						newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SENTRY'),True)
					BonusList.append(['BUILDING_PALACE','BUILDINGCLASS_PALACE',1,3,10])
					pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)
					caster.changeDamage(100,iPlayer)
					#CyInterface().addImmediateMessage("&#12362;&#12420;&#12289;" + pPlayer.getCivilizationDescription(iPlayer) + "&#12398;" + gc.getBuildingInfo(gc.getInfoTypeForString('BUILDING_PALACE')).getDescription() + "&#12398;&#27096;&#23376;&#12364;&#8230;&#65311;" ,"")
				
			
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_LEADER') ):
				caster.changeExperience(5,-1,False,False,False)
			elif caster.getUnitType() == gc.getInfoTypeForString('UNIT_SPY'):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MORALE'),True)
			elif caster.getUnitType() == gc.getInfoTypeForString('UNIT_SCOUT') or caster.getUnitType() == gc.getInfoTypeForString('UNIT_EXPLORER'):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SENTRY'),True)
			elif gc.getInfoTypeForString('UNIT_NITORI0') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_NITORI6'):
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_KAPPA_ROBOT_LUNATIC'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			elif gc.getInfoTypeForString('UNIT_MARISA0') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_MARISA6'):
				BonusList.append(['BUILDING_KIRISAMEMAHOUTEN','BUILDINGCLASS_KIRISAMEMAHOUTEN',1,0,1])
			elif gc.getInfoTypeForString('UNIT_PATCHOULI0') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_PATCHOULI6'):
				caster.changeExperience(3,-1,False,False,False)
			elif gc.getInfoTypeForString('UNIT_CHEN0') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_CHEN6'):
				caster.changeDamage(20,iPlayer)
			elif gc.getInfoTypeForString('UNIT_KEINE0') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KEINE6'):
				BonusList.append(['BUILDING_TERAKOYA','BUILDINGCLASS_TERAKOYA',1,1,1])
			else:
				caster.changeExperience(1,-1,False,False,False)
			
			bFlag = False
			for i in range(len(BonusList)):
				for pPyCity in py.getCityList():
					pCity = pPlayer.getCity(pPyCity.getID())
					if pCity.isHasBuilding(gc.getInfoTypeForString(BonusList[i][0])):
						if BonusList[i][2] == 0:
							iBonusNum = pCity.getBuildingYieldChange(gc.getInfoTypeForString(BonusList[i][1]),BonusList[i][3])
							pCity.setBuildingYieldChange(gc.getInfoTypeForString(BonusList[i][1]),BonusList[i][3],BonusList[i][4] + iBonusNum )
						else:
							iBonusNum = pCity.getBuildingCommerceChange(gc.getInfoTypeForString(BonusList[i][1]),BonusList[i][3])
							pCity.setBuildingCommerceChange(gc.getInfoTypeForString(BonusList[i][1]),BonusList[i][3],BonusList[i][4] + iBonusNum )
						bFlag = True
			
			if bFlag:
				CyInterface().addImmediateMessage("&#12362;&#12420;&#12289;" + pPlayer.getCivilizationDescription(iPlayer) + "&#12398;" + gc.getBuildingInfo(gc.getInfoTypeForString(BonusList[0][0])).getDescription() + "&#12398;&#27096;&#23376;&#12364;&#8230;&#65311;" ,"")
			
			break
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True




#偉人を吸い出す
def req_GET_GREATE_PERSON(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_RAINBOW_UFO'):
			return True
		else:
			return False
	
	else:
	
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			pPlot = caster.plot()
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				if pCity.getNumGreatPeople() > 0:
					if pCity.getTeam() == caster.getTeam():
						if pCity.getOccupationTimer() == 0:
							return True
			
	return False

def spell_GET_GREATE_PERSON(caster,cost):

	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	
	for i in range(7,14):
		peopleNum = pCity.getFreeSpecialistCount(i)
		if peopleNum > 0:
			pCity.setFreeSpecialistCount(i,peopleNum-1)
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PROPHET') + i-7, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			break

	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True





#命蓮寺の建設
def req_BUILD_MEIRENJI(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_SEIRENSEN'):
			return True
		else:
			return False
	
	else:
	
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			pPlot = caster.plot()
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				if pCity.getTeam() == caster.getTeam():
					if pCity.getOccupationTimer() == 0:
						return True
			
	return False

def spell_BUILD_MEIRENJI(caster,cost):

	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI1'),1)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI2'),1)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI3'),1)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI4'),1)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI5'),1)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MEIRENJI6'),1)
	
	caster.changeDamage(100,caster.getOwner())
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True









#俺の嫁システムによる強化
def req_POWERUP_COMBAT(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumMyLove()>0 and caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
		return True
	
	return False

def spell_POWERUP_COMBAT(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	caster.setNumPowerUp( 1 , caster.getNumPowerUp(1) + 1 )
	pPlayer.setNumMyLove( pPlayer.getNumMyLove() - 1 )
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_POWERUP_STG(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumMyLove()>0 and caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
		return True
	
	return False

def spell_POWERUP_STG(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	caster.setNumPowerUp( 2 , caster.getNumPowerUp(2) + 1 )
	pPlayer.setNumMyLove( pPlayer.getNumMyLove() - 1 )
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True



def req_POWERUP_CAL(bTestVisible,caster,sCAL,eCAL,cost):

	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumMyLove()>0 and caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
		return True
	
	return False

def spell_POWERUP_CAL(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	caster.setNumPowerUp( 3 , caster.getNumPowerUp(3) + 1 )
	pPlayer.setNumMyLove( pPlayer.getNumMyLove() - 1 )
	
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#シューティングオプション

def req_SPECIAL_TAMEUTI(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHOOTING_OPTION_TAMEUTI')):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_TAME_KANRYOU') ) == False:
				if caster.canMove():
					return True
	
	return False
	
def spell_SPECIAL_TAMEUTI(caster,cost):
	
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TAMETYUU'),True)
	caster.setNumTurnPromo(caster.getNumTurnPromo() +1)
	caster.finishMoves()
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_SPECIAL_HIGHSPEEDMOVE(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHOOTING_OPTION_HIGHSPEEDMOVE')):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			return True
	
	return False

def spell_SPECIAL_HIGHSPEEDMOVE(caster,cost):
	
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HIGHSPEEDMOVE')):
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_HIGHSPEEDMOVE'),False )
	else:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_HIGHSPEEDMOVE'),True )
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True



#早苗スペル
def req_SANAE_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SANAE1','UNIT_SANAE6',cost)

def spell_SANAE_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	iBonus = pPlot.getBonusType(caster.getTeam())
	BonusList = ['BONUS_BANANA','BONUS_CORN','BONUS_RICE','BONUS_WHEAT','BONUS_SPICES','BONUS_SUGAR',
				 'BONUS_WINE','BONUS_SILK','BONUS_INCENSE','BONUS_DYE',]
	for i in range(len(BonusList)):
		if iBonus == gc.getInfoTypeForString(BonusList[i]):
			iRandNum = gc.getGame().getSorenRandNum(100, "SANAE SKILL EXTRA")
			if iRandNum < 10:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_CORN'))
			elif iRandNum < 20:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_RICE'))
			elif iRandNum < 30:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_WHEAT'))
			elif iRandNum < 40:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_SPICES'))
			elif iRandNum < 50:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_SUGAR'))
			else:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_BANANA'))
			pPlot.setImprovementType(-1)
			break
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	

def req_SANAE_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SANAE1','UNIT_SANAE6',cost)


def spell_SANAE_PHANTASM1(caster,cost):

	pPlot = caster.plot()
	
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_OASIS'):
		if gc.getGame().getSorenRandNum(100, "SANAE SKILL PHANTASM1") < 10:
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_OASIS'),1)
			pPlot.resetFeatureModel()
		else:
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
		if gc.getGame().getSorenRandNum(100, "SANAE SKILL PHANTASM2") < 10:
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
		else:
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
	
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
		if pPlot.isFreshWater():
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_TUNDRA'),True,True)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	



#レミリアスペル
def req_REMILIA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_REMILIA1','UNIT_REMILIA6',cost)

def spell_REMILIA_EXTRA1(caster,cost):
	
	newUnit1 = gc.getPlayer(caster.getOwner()).initUnit(gc.getInfoTypeForString("UNIT_BAT"), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ILLUSION"),True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_REMILIA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_REMILIA1','UNIT_REMILIA6',cost)

def spell_REMILIA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_NEKKYOU',True,100,True,False,False,-1,False,True,True,True,-1,True,0,1,False,False,-1,+1)
	
	caster.setPower(caster.getPower() - cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True




#橙スペル
def req_CHEN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_CHEN1','UNIT_CHEN6',cost)

def spell_CHEN_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_NEKOKESSHA'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_CHEN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_CHEN1','UNIT_CHEN6',cost)

def spell_CHEN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if gc.getInfoTypeForString('UNIT_RAN1') <= pUnit.getUnitType() and  pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_RAN6'):
			pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
			pUnit.changeDamage(-CAL-pUnit.countCardAttackLevel(),caster.getOwner())
			pUnit.changeMoves(-100)
			caster.changeDamage(-100,caster.getOwner())
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#リグルスペル
def req_WRIGGLE_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_WRIGGLE1','UNIT_WRIGGLE6',cost)

def spell_WRIGGLE_EXTRA1(caster,cost):
	
	iWidth = gc.getMap().getGridWidth()
	iHeight = gc.getMap().getGridHeight()
	RangeList = []
	
	for iX in range(iWidth):
		for iY in range(iHeight):
			RangeList.append([iX - caster.getX(),iY - caster.getY()])
	
	Functions.setPromotion(RangeList,caster,'PROMOTION_HOTARUNOHIKARI',True,100,True,False,False,-1,True,True,True,True,-1,True,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_WRIGGLE_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_WRIGGLE1','UNIT_WRIGGLE6',cost)

def spell_WRIGGLE_PHANTASM1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(SummonBaseNum[CAL]):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FIRE_FLY'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'),True)
		newUnit1.setSpecialNumber(CAL-1)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
	



#てゐスペル
def req_TEWI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_TEWI1','UNIT_TEWI6',cost)

def spell_TEWI_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MOUKEBANASHI'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def req_TEWI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_TEWI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_TEWI6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
			if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')) and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
				py = PyPlayer(caster.getOwner()) #すでにトラップユニットが居ないかを探す
				TrapNum = 0
				for pUnit in py.getUnitList():
					if gc.getInfoTypeForString('UNIT_TRAP') == pUnit.getUnitType():
						TrapNum = TrapNum+1
				if gc.getPlayer(caster.getOwner()).getNumCities() > TrapNum:
					if caster.getNumSpellPhantasmBreakTime() <= 0:
						return True
				
	return False

def spell_TEWI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	
	if caster.plot().getTeam() == caster.getTeam():
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_TRAP"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		iNumBreakTime = 3
		#ゲーム速度による変化
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
			iNumBreakTime = iNumBreakTime * 100 / 50
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
			iNumBreakTime = iNumBreakTime * 100 / 75
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
			iNumBreakTime = iNumBreakTime * 100 / 125
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
			iNumBreakTime = iNumBreakTime * 100 / 150
		caster.setNumSpellPhantasmBreakTime(iNumBreakTime)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	#point = caster.plot().getPoint()
	#CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	#CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_TEWI_PHANTASM2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_TEWI1','UNIT_TEWI6',cost)

def spell_TEWI_PHANTASM2(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity() == False:
		if pPlot.getTeam() == caster.getTeam():
			if pPlot.getBonusType(caster.getTeam()) == -1:
				if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_COAST') and pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_OCEAN'):
					if pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_OASIS'):
						pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_JUNGLE'),1)
						pPlot.setImprovementType(-1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	
	return True




#にとりスペル
def req_NITORI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_NITORI1','UNIT_NITORI6',cost)

def spell_NITORI_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_NITORIKYOUIKU'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_NITORI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_NITORI1','UNIT_NITORI6',cost)

def spell_NITORI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
			pPlot.getUnit(i).setHasPromotion(gc.getInfoTypeForString('PROMOTION_BARRAGE1'),True)
			pPlot.getUnit(i).setHasPromotion(gc.getInfoTypeForString('PROMOTION_MORALE'),True)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True








#魔理沙スペル
def req_MARISA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MARISA1','UNIT_MARISA6',cost)

def spell_MARISA_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_LIBRARY')):
			if gc.getPlayer(caster.getOwner()).getGold() >= caster.getExperience()/2:
				gc.getPlayer(caster.getOwner()).changeGold(-caster.getExperience()/2)
				caster.changeExperience(1,-1,False,False,False)
				if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_DAITOSHOKAN')):
					caster.changeExperience(1,-1,False,False,False)
			
				caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
				
				point = caster.plot().getPoint()
				CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
				CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
				
				return True
	
	return False
	
	
def req_MARISA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MARISA1','UNIT_MARISA6',cost)

def spell_MARISA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_CHARM',True,100,True,True,True,-1,True,False,True,True,-1,True,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_CHARM',True,CAL,False,False,True,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#フランスペル
def req_FLAN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_FLAN1','UNIT_FLAN6',cost)

def spell_FLAN_EXTRA1(caster,cost):
	
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LAEVATEINN'),True)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL_WEAKPOINT'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_FLAN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_FLAN1','UNIT_FLAN6',cost)

def spell_FLAN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	RangeList = RangeList2[:]
	RangeList.append([0,0])
	Functions.changeDamage(RangeList,caster,10,50,0,False,True,True,True,-1,False,True,True,True,-1,False,0,0,False,True)
	Functions.changeDamage(RangeList,caster,5,25,10,False,True,True,True,-1,True,False,True,True,-1,False,0,0,False,True)
	
	caster.setPower(caster.getPower() - cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL_WEAKPOINT_BIG'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_FLAN_PHANTASM2(bTestVisible,caster,sCAL,eCAL,cost):
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_FLAN1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_FLAN6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FLAN')):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if gc.getPlayer(caster.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_FLANLIST')):
					return True
	return False

def spell_FLAN_PHANTASM2(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		if pPlot.getPlotCity().getOwner() == caster.getOwner():
			
			#フランにより都市が破壊されました！
			CyInterface().addImmediateMessage("&#12501;&#12521;&#12531;&#12395;&#12424;&#12426;" + pPlot.getPlotCity().getName() + "&#12364;&#30772;&#22730;&#12373;&#12428;&#12414;&#12375;&#12383;&#65281;","")
			
			newUnitOwner = gc.getBARBARIAN_PLAYER()
			if pPlot.getPlotCity().getOriginalOwner() != pPlot.getPlotCity().getOwner(): #他人の都市を奪って破壊した場合、その持ち主が生きていればそのユニットが現われる
				if gc.getPlayer(pPlot.getPlotCity().getOriginalOwner()).isAlive():
					newUnitOwner = pPlot.getPlotCity().getOriginalOwner()
			
			pPlayer = gc.getPlayer(caster.getOwner())
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT'):
				iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL'):
				iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL'):
				iUnit = gc.getInfoTypeForString('UNIT_MACEMAN')
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE'):
				iUnit = gc.getInfoTypeForString('UNIT_MUSKETMAN')
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL'):
				iUnit = gc.getInfoTypeForString('UNIT_RIFLEMAN')
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN'):
				iUnit = gc.getInfoTypeForString('UNIT_INFANTRY')
			if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE'):
				iUnit = gc.getInfoTypeForString('UNIT_MECHANIZED_INFANTRY')
			
			pop = pPlot.getPlotCity().getPopulation()
			iX = pPlot.getPlotCity().getX()
			iY = pPlot.getPlotCity().getY()
			pPlot.getPlotCity().kill()	
			for i in range(pop):
				newUnit1 = gc.getPlayer(newUnitOwner).initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
			
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL_WEAKPOINT_BIG'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True




#妖夢スペル
def req_YOUMU_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YOUMU1','UNIT_YOUMU6',cost)

def spell_YOUMU_EXTRA1(caster,cost):
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_KONPAKUNOOSHIE',True,100,True,False,False,-1,False,True,True,True,-1,True)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_YOUMU_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YOUMU1','UNIT_YOUMU6',cost)

def spell_YOUMU_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iX = caster.getX()
	iY = caster.getY()
	UnitList = []
	
	for iiX in range(iX-1,iX+2):
		for iiY in range(iY-1,iY+2):
			if iiX!=iX or iiY!=iY:
				if Functions.isPlot(iiX,iiY):
					pPlot = gc.getMap().plot(iiX,iiY)
					for i in range(pPlot.getNumUnits()):
						if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
							if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getUnit(i).getTeam()) == True:
								UnitList.append(pPlot.getUnit(i))
								
	if len(UnitList) != 0:
		for i in range(CAL):
			UnitNum = gc.getGame().getSorenRandNum(len(UnitList),"YOUMU Phantasm")
			iDamage = (100 - UnitList[UnitNum].getDamage()) * 20 / 100
			UnitList[UnitNum].changeDamage(iDamage,caster.getOwner())
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower() - cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#チルノスペル
def req_CIRNO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_CIRNO1','UNIT_CIRNO6',cost)

def spell_CIRNO_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_YOUSEIOUKOKU'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_CIRNO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_CIRNO1','UNIT_CIRNO6',cost)

def spell_CIRNO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	for iiX in range(iX-1,iX+2):
		for iiY in range(iY-1,iY+2):
			if Functions.isPlot(iiX,iiY):
				pPlot = gc.getMap().plot(iiX,iiY)
				#資源があるか、ユニットの居るところは凍らないように
				if pPlot.getNumUnits() == 0 and pPlot.getBonusType(caster.getTeam()) == -1 :
					if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN'):
						pPlot.setOriginalTerrain(pPlot.getTerrainType())
						pPlot.setOriginalBounu( pPlot.getBonusType(caster.getTeam()) )
						pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_SNOW'),True,True)
						pPlot.setFeatureType (gc.getInfoTypeForString('FEATURE_ICEDSEA'),1)
						pPlot.setNumCirnoFreeze(3)
						
					#凍らせなおし
				 	if pPlot.getNumCirnoFreeze()>0:
				 		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_SNOW'),True,True)
						pPlot.setFeatureType (gc.getInfoTypeForString('FEATURE_ICEDSEA'),1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#えーりんスペル
def req_EIRIN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_EIRIN1','UNIT_EIRIN6',cost)

def spell_EIRIN_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SHINYAKUJIKKENNJO'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_EIRIN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_EIRIN1','UNIT_EIRIN6',cost)

def spell_EIRIN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	Functions.changeDamage(RangeList0,caster,-CAL*2,-CAL*2,100,False,True,True,True,-1,True,True,True,True,-1,True,0)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_OUKAKEKKAI'),True )
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#諏訪子スペル
def req_SUWAKO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SUWAKO1','UNIT_SUWAKO6',cost)

def spell_SUWAKO_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUWABUNSHA'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_SUWAKO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SUWAKO1','UNIT_SUWAKO6',cost)

def spell_SUWAKO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getOwner() != caster.getOwner() and pCity.getTeam() == caster.getTeam():
			pCity.changeCulture(pCity.getOwner(),CAL*CAL,True)
		else:
			pCity.changeCulture(caster.getOwner(),CAL*CAL,True)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#アリススペル
def req_ALICE_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_ALICE1','UNIT_ALICE6',cost)

def spell_ALICE_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LITTLE_LEGION'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_ALICE_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_ALICE1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_ALICE6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ALICE_SKILL1')):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				#if gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
				return True
	return False

def spell_ALICE_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if ( ( gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_SHANGHAI_DOLL6') ) or
			 ( gc.getInfoTypeForString('UNIT_HOURAI_DOLL1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_HOURAI_DOLL6') ) ):
			pUnit.changeDamage(-CAL*2,caster.getOwner())
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DOLLS_WAR'),True)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#もこスペル
def req_MOKOU_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MOKOU1','UNIT_MOKOU6',cost)

def spell_MOKOU_EXTRA1(caster,cost):
	
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = caster.plot()
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_TUNDRA'),True,True)
			
	elif pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
		if gc.getGame().getSorenRandNum(100, "MOKOU SKILL PHANTASM2") < 15:
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
		else:
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
	
	for iiX in range(iX-1,iX+2):
		for iiY in range(iY-1,iY+2):
			pPlot = gc.getMap().plot(iiX,iiY)
			if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_ICE'):
				pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_NONE'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_MOKOU_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MOKOU1','UNIT_MOKOU6',cost)

def spell_MOKOU_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KENKOUKAN'),1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#けーねスペル
def req_KEINE_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_KEINE1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KEINE6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_EXTRA')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KEINE_SKILL1')):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')):
				return True
	return False

def spell_KEINE_EXTRA1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	#きもくなれる
	RevivalUnit = caster.getUnitType() - gc.getInfoTypeForString("UNIT_KEINE1") + gc.getInfoTypeForString("UNIT_HAKUTAKUKEINE1")
	newUnit1 = pPlayer.initUnit(RevivalUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.convert(caster)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KEINE'),False)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HAKUTAKUKEINE'),True)
	newUnit1.finishMoves()
			
	newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_KEINE_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_KEINE1','UNIT_KEINE6',cost)

def spell_KEINE_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TERAKOYA'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#きもけーねスペル
def req_HAKUTAKUKEINE_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_HAKUTAKUKEINE1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_HAKUTAKUKEINE6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_EXTRA')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KEINE_SKILL1')):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2')):
				return True
	return False
def spell_HAKUTAKUKEINE_EXTRA1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	#ふつうになれる
	RevivalUnit = caster.getUnitType() - gc.getInfoTypeForString("UNIT_HAKUTAKUKEINE1") + gc.getInfoTypeForString("UNIT_KEINE1")
	newUnit1 = pPlayer.initUnit(RevivalUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.convert(caster)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HAKUTAKUKEINE'),False)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KEINE'),True)
	newUnit1.finishMoves()
			
	newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_HAKUTAKUKEINE_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_HAKUTAKUKEINE1','UNIT_HAKUTAKUKEINE6',cost)

def spell_HAKUTAKUKEINE_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	UnitList = []
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS')  and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
			UnitList.append(pPlot.getUnit(i))
	
	if len(UnitList) != 0:
		iLoopNum = SummonBaseNum[CAL]
		if iLoopNum > len(UnitList):
			iLoopNum = len(UnitList)
		for i in range(iLoopNum):
			iRandNum = gc.getGame().getSorenRandNum(len(UnitList),"HAKUTAKUKEINE Spell")
			pUnit = UnitList.pop(iRandNum)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_REKISHI1'),True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#パルスィスペル
def req_PARSEE_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_PARSEE1','UNIT_PARSEE6',cost)

def spell_PARSEE_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SHITTO'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_PARSEE_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_PARSEE1','UNIT_PARSEE6',cost)

def spell_PARSEE_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DAISHITTO'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#勇儀スペル
def req_YUGI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YUGI1','UNIT_YUGI6',cost)

def spell_YUGI_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ONINOENKAI'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_YUGI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YUGI1','UNIT_YUGI6',cost)

def spell_YUGI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iMove = CAL/8
	if iMove==0:
		iMove=1
	
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS')  and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
			pPlot.getUnit(i).changeMoves(-50*iMove)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#咲夜スペル
def req_SAKUYA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SAKUYA1','UNIT_SAKUYA6',cost)

def spell_SAKUYA_EXTRA1(caster,cost):
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_SPELL_CASTED',False,100,True,True,False,-1,True,False,True,True,-1,True)
			
	caster.setPower(caster.getPower() - cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_SAKUYA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_SAKUYA1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_SAKUYA6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SAKUYA_SKILL1')):
			if caster.getPower()>=cost:
				if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
					return True
	return False

def spell_SAKUYA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iX = caster.getX()
	iY = caster.getY()
	
	UnitList = []
	for iiX in range(iX-1,iX+2):
		for iiY in range(iY-1,iY+2):
			if iiX!=iX or iiY!=iY:
				if Functions.isPlot(iiX,iiY):
					pPlot = gc.getMap().plot(iiX,iiY)
					for i in range(pPlot.getNumUnits()):
						if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
							if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getUnit(i).getTeam()) == True:
								UnitList.append(pPlot.getUnit(i))
							
	Knife = int(CAL * (1.5 + 0.1*caster.getLevel()))
	while Knife>0:
		if len(UnitList) > 0:
			iRandNum = gc.getGame().getSorenRandNum(len(UnitList),"sakuya Spell")
			while (UnitList[iRandNum].getDamage() < 100 and Knife > 0):
				Knife = Knife - 1
				UnitList[iRandNum].changeDamage(10,caster.getOwner())
			if UnitList[iRandNum].getDamage() >= 100:
				del UnitList[iRandNum]
		else:
			break
	
	caster.setPower(caster.getPower() - cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#ゆゆこスペル
def req_YUYUKO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YUYUKO1','UNIT_YUYUKO6',cost)

def spell_YUYUKO_EXTRA1(caster,cost):
	
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	YoumuList = [gc.getInfoTypeForString("UNIT_YOUMU1"),gc.getInfoTypeForString("UNIT_YOUMU2"),gc.getInfoTypeForString("UNIT_YOUMU3"),
				gc.getInfoTypeForString("UNIT_YOUMU4"),gc.getInfoTypeForString("UNIT_YOUMU5"),gc.getInfoTypeForString("UNIT_YOUMU6"),]
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		for iUnit in YoumuList:
			if pUnit.getUnitType() == iUnit:
				pUnit.setXY(iX,iY,False,True,True)
				if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BUNSHIN')) == False:
					pUnit.changeDamage(-20,iPlayer)
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_YUYUKO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YUYUKO1','UNIT_YUYUKO6',cost)

def spell_YUYUKO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_HANAMI'),1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#ルーミアスペル
def req_RUMIA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_RUMIA1','UNIT_RUMIA6',cost)

def spell_RUMIA_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_JUSSINHOU'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_RUMIA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_RUMIA1','UNIT_RUMIA6',cost)

def spell_RUMIA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_KURAYAMI',True,CAL*10,False,True,True,-1,True,True,True,True,-1,False,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#メディスペル
def req_MEDICIN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MEDICIN1','UNIT_MEDICIN6',cost) or Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MEDICINwithSU1','UNIT_MEDICINwithSU6',cost)

def spell_MEDICIN_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_MUMEINOOKA')) > 0: 
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUZURAN'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_MEDICIN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MEDICIN1','UNIT_MEDICIN6',cost) or Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MEDICINwithSU1','UNIT_MEDICINwithSU6',cost)

def spell_MEDICIN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON1',True,CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON2',True,CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON3',True,CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON4',True,CAL*2,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON1',True,CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON2',True,CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON3',True,CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
	Functions.setPromotion(RangeList1,caster,'PROMOTION_POISON4',True,CAL,False,True,True,-1,True,False,True,True,-1,False,0,0,False,False,-1,+1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#かなこスペル
def req_KANAKO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KANAKO1','UNIT_KANAKO6',cost)

def spell_KANAKO_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_YASAKABUNSHA'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_KANAKO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_KANAKO1','UNIT_KANAKO6',cost)

def spell_KANAKO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.getPlotType() == PlotTypes.PLOT_HILLS:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_YAMANOSINKOU',True,100,True,False,False,-1,False,True,True,True,-1,True)
			
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True

	return False






#れいむスペル
def req_REIMU_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_REIMU1','UNIT_REIMU6',cost)

def spell_REIMU_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUMIYOSISANSHIN'),1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_REIMU_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_REIMU1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_REIMU6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if caster.getNumSpellPhantasmBreakTime() <= 0:
					return True
	return False
	

def spell_REIMU_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	
	iNumAlivePlayer = 0
	for i in range(TohoCivList.iMaxPlayer):
		ppPlayer = gc.getPlayer(i)
		#CvGameUtils.doprint("%d\n" %i)
		if ppPlayer.isBarbarian() == False and ppPlayer.isAlive() == True and pPlayer.getTeam() != ppPlayer.getTeam():
			iNumGold = ppPlayer.getGold()/10
			ppPlayer.changeGold(-iNumGold)
			pPlayer.changeGold(iNumGold)
			iNumAlivePlayer = iNumAlivePlayer + 1
	
	iNumBreakTime = iNumAlivePlayer+1
	#ゲーム速度による変化
	if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
		iNumBreakTime = iNumBreakTime * 100 / 50
	if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
		iNumBreakTime = iNumBreakTime * 100 / 75
	if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
		iNumBreakTime = iNumBreakTime * 100 / 125
	if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
		iNumBreakTime = iNumBreakTime * 100 / 150
	caster.setNumSpellPhantasmBreakTime(iNumBreakTime)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	#霊夢により盛大な例大祭が開催されました
	CyInterface().addImmediateMessage("&#38666;&#22818;&#12395;&#12424;&#12426;&#30427;&#22823;&#12394;&#20363;&#22823;&#31085;&#12364;&#38283;&#20652;&#12373;&#12428;&#12414;&#12375;&#12383;","")

	
	return True









#ゆうかスペル
def req_YUKA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YUKA1','UNIT_YUKA6',cost)

def spell_YUKA_EXTRA1(caster,cost):
	
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	
	pPlot = caster.plot()
	iNumUnit = pPlot.getNumUnits()
	UnitList = []
	
	for i in range(iNumUnit):
		if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
			if caster.getTeam() == pPlot.getUnit(i).getTeam(): #東方ユニットでなく、同じチームであれば
				UnitList.append(i)
	
	if len(UnitList)>0:
		pUnit = pPlot.getUnit( UnitList[ gc.getGame().getSorenRandNum(len(UnitList), "yuuka to asobu") ] )
		iDamage = gc.getGame().getSorenRandNum(51, "yuuka to asobu 2") + 60
		pUnit.changeDamage(iDamage,iPlayer)
		pUnit.changeExperience(10,-1,False,False,False)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_YUKA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_YUKA1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_YUKA6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')) and caster.getPower()>=cost:
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if caster.getNumSpellPhantasmBreakTime() <= 0:
					return True
		if caster.getSpecialNumber() > 0:
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				return True
	return False
	

def spell_YUKA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.getBonusType(caster.getTeam()) == -1:
		if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_COAST') and pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_OCEAN'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_SUNFLOWER'),1)
			pPlot.setImprovementType(-1)
			
			
			if caster.getSpecialNumber() > 0:
				caster.setSpecialNumber(caster.getSpecialNumber()-1)
			else:
				caster.setPower(caster.getPower()-cost)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	
	return True









#こいしスペル
def req_KOISHI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_KOISHI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KOISHI6'):
			return True
		if gc.getInfoTypeForString('UNIT_KOISHI_FADE1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KOISHI_FADE6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MODE_EXTRA")):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
					return True
	return False

def spell_KOISHI_EXTRA1(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MUISHIKINOROUDOU'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_KOISHI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_KOISHI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KOISHI6'):
			return True
		if gc.getInfoTypeForString('UNIT_KOISHI_FADE1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KOISHI_FADE6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MODE_PHANTASM")):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3')):
					return True
	return False


def spell_KOISHI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getTeam() != caster.getTeam():
			iNum = int( 100 * (1.3**(CAL-16))  )
			gc.getTeam(caster.getOwner()).changeEspionagePointsAgainstTeam(pCity.getTeam(),iNum) 
			
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	pPlot = caster.plot()
	point = pPlot.getPoint()
	
	return True
	





def req_KOISHI_SKILL1(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_KOISHI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KOISHI6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MODE_PHANTASM")) or caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_KOISHI_SKILL1")):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				return True
	return False

def spell_KOISHI_SKILL1(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	#不可視状態になれる
	if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI1"):
		RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI_FADE1")
	if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI2"):
		RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI_FADE2")
	if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI3"):
		RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI_FADE3")
	if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI4"):
		RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI_FADE4")
	if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI5"):
		RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI_FADE5")
	if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI6"):
		RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI_FADE6")
	iExperience = caster.getExperience()
	iLevel = caster.getLevel()
	newUnit1 = pPlayer.initUnit(RevivalUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	newUnit1.changeExperience(iExperience,-1,false,false,false)
	newUnit1.changeLevel(iLevel-1)
	
	#もともと持っていた昇進をそのまま移行させる
	PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
	PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
	PromotionNum = PromotionEnd - PromotionStart
	
	for iPromotion in range(PromotionNum):
		if caster.isHasPromotion(iPromotion):
			newUnit1.setHasPromotion(iPromotion,True)
	
	newUnit1.convert(caster)
	newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SUBCONSCIOUS'),True )
	newUnit1.finishMoves()
	
	
	newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	pPlot = newUnit1.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True



def req_KOISHI_SKILL2(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_KOISHI_FADE1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KOISHI_FADE6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MODE_PHANTASM")) or caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_KOISHI_SKILL1")):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				return True
	return False

def spell_KOISHI_SKILL2(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	#可視状態になれる　ただし、同じマスに敵対ユニットが居る場合は不可
	pTeam = gc.getTeam(caster.getTeam())
	UnitFlag = False
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		if pTeam.isAtWar(pPlot.getUnit(i).getTeam()):
			UnitFlag = True
	
	if UnitFlag == False:
		if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE1"):
			RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI1")
		if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE2"):
			RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI")
		if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE3"):
			RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI3")
		if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE4"):
			RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI4")
		if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE5"):
			RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI5")
		if caster.getUnitType() == gc.getInfoTypeForString("UNIT_KOISHI_FADE6"):
			RevivalUnit = gc.getInfoTypeForString("UNIT_KOISHI6")
		iExperience = caster.getExperience()
		iLevel = caster.getLevel()
		newUnit1 = pPlayer.initUnit(RevivalUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		newUnit1.changeExperience(iExperience,-1,false,false,false)
		newUnit1.changeLevel(iLevel-1)
		
		#もともと持っていた昇進をそのまま移行させる
		PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
		PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
		PromotionNum = PromotionEnd - PromotionStart
		
		for iPromotion in range(PromotionNum):
			if caster.isHasPromotion(iPromotion):
				newUnit1.setHasPromotion(iPromotion,True)
		
		newUnit1.convert(caster)
		newUnit1.finishMoves()
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SUBCONSCIOUS'),False )
		
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		pPlot = newUnit1.plot()
		point = pPlot.getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False





#パチュリー
def req_PATCHOULI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_PATCHOULI1','UNIT_PATCHOULI6',cost)

def spell_PATCHOULI_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL,CAL,50,True,False,False,True,-1,False,True,True,True,-1,False,0,0,False,True)
	Functions.changeDamage(RangeList1,caster,CAL/2,CAL/2,50,True,False,False,True,-1,True,False,True,True,-1,False,0,0,False,True)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True


def req_PATCHOULI_EXTRA2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_PATCHOULI1','UNIT_PATCHOULI6',cost)

def spell_PATCHOULI_EXTRA2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList0,caster,-CAL,-CAL,100,False,True,True,False,-1,True,True,True,True,-1,True,0)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_PATCHOULI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_PATCHOULI1','UNIT_PATCHOULI6',cost)

def spell_PATCHOULI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	#if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_OASIS') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
	#統合MOD追記
	#オアシス及び氾濫源でも発動を許可
	#氷原はツンドラに変化
	#及び、きれいな水判定を除去
	#そして、power0.5と引き換えにオアシスに花壇強制設置
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT'):
		#if pPlot.isFreshWater():
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
		#if pPlot.isFreshWater():
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
	
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_TUNDRA'),True,True)
	
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS') and pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
		cost = 0.5
		if caster.getPower()>=cost:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM'))
			caster.setPower(caster.getPower() - cost)
	
	#統合MOD追記ここまで
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_PATCHOULI_PHANTASM2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_PATCHOULI1','UNIT_PATCHOULI6',cost)

def spell_PATCHOULI_PHANTASM2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_SYLPHAEHORN',True,100,True,True,True,-1,True,True,True,True,-1,True,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	

	
def req_PATCHOULI_PHANTASM3(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_PATCHOULI1','UNIT_PATCHOULI6',cost)

def spell_PATCHOULI_PHANTASM3(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_BARRIER',True,100,True,True,True,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True




#藍
def req_RAN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_RAN1','UNIT_RAN6',cost)

def spell_RAN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	newUnit1 = gc.getPlayer(caster.getOwner()).initUnit(gc.getInfoTypeForString('UNIT_ZENKI'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = gc.getPlayer(caster.getOwner()).initUnit(gc.getInfoTypeForString('UNIT_GOKI'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_RAN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_RAN1','UNIT_RAN6',cost)

def spell_RAN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if gc.getInfoTypeForString('UNIT_CHEN1') <= pUnit.getUnitType() and  pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_CHEN6'):
			pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
			pUnit.changeDamage(-50,caster.getOwner())
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SHIKINOSHIKI"),True)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#うどんげ
def req_REISEN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_REISEN1','UNIT_REISEN6',cost)

def spell_REISEN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity() and caster.getTeam() != pPlot.getPlotCity().getTeam():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GYOUSHOU'),1)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_REISEN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_REISEN1','UNIT_REISEN6',cost)

def spell_REISEN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_REIGETUSAI'),1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#いく
def req_IKU_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_IKU1','UNIT_IKU6',cost)

def spell_IKU_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getTeam() == caster.getTeam() and pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FAIR_WIND'),True)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_IKU_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_IKU1','UNIT_IKU6',cost)

def spell_IKU_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_WEATHER_REPORT'),1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#さとり
def req_SATORI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SATORI1','UNIT_SATORI6',cost)

def spell_SATORI_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SATORIHOUSE'),1)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_SATORI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SATORI1','UNIT_SATORI6',cost)

def spell_SATORI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	YumiFlag = False
	HakuheiFlag = False
	KiheiFlag = False
	HeikiFlag = False
	KakiFlag = False
	SoukouFlag = False
	
	for iX in range(caster.getX()-1,caster.getX()+2):
		for iY in range(caster.getY()-1,caster.getY()+2):
			if Functions.isPlot(iX,iY):
				pPlot = gc.getMap().plot(iX,iY);
				for i in range(pPlot.getNumUnits()):
					if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getUnit(i).getTeam()):
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
							YumiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
							HakuheiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MOUNTED'):
							KiheiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
							HeikiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN'):
							KakiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARMOR'):
							SoukouFlag = True
	
	if YumiFlag and CAL>=1:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_COVER',True,100,True,False,False,-1,False,True,True,True,-1,True)
	if HakuheiFlag and CAL>=4:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_SHOCK',True,100,True,False,False,-1,False,True,True,True,-1,True)
	if KiheiFlag and CAL>=8:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_FORMATION',True,100,True,False,False,-1,False,True,True,True,-1,True)
	if HeikiFlag and CAL>=8:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_CHARGE',True,100,True,False,False,-1,False,True,True,True,-1,True)
	if KakiFlag and CAL>=12:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_PINCH',True,100,True,False,False,-1,False,True,True,True,-1,True)
	if SoukouFlag and CAL>=16:
		Functions.setPromotion(RangeList0,caster,'PROMOTION_AMBUSH',True,100,True,False,False,-1,False,True,True,True,-1,True)
	
	if CAL >= 16:
		pPlot = caster.plot()
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN'):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INTERCEPTION1'),True)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#ミスティア
def req_MYSTIA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MYSTIA1','UNIT_MYSTIA6',cost)

def spell_MYSTIA_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_YATAI'),1)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_MYSTIA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MYSTIA1','UNIT_MYSTIA6',cost)

def spell_MYSTIA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_MYSTIA_FANCLUB'),1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True




#すいか
def req_SUIKA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SUIKA1','UNIT_SUIKA6',cost) or Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SUIKA1_YOUKAI','UNIT_SUIKA6_YOUKAI',cost)

def spell_SUIKA_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SHUEN'),1)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_SUIKA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SUIKA1','UNIT_SUIKA6',cost) or Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SUIKA1_YOUKAI','UNIT_SUIKA6_YOUKAI',cost)

def spell_SUIKA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	UnitList = []
	
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		UnitList.append(pPlot.getUnit(i).getUnitType())
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		for i in range(len(UnitList)):
			if pUnit.getUnitType() == UnitList[i]:
				pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
				break
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True




#小町
def req_KOMACHI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KOMACHI1','UNIT_KOMACHI6',cost)

def spell_KOMACHI_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SIGOTONOKOKOROE'),1)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True

	
	
def req_KOMACHI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_KOMACHI1','UNIT_KOMACHI6',cost)

def spell_KOMACHI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iX = caster.getX()
	iY = caster.getY()
	
	UnitList = []
	for iiX in range(iX-1,iX+2):
		for iiY in range(iY-1,iY+2):
			if iiX!=iX or iiY!=iY:
				if Functions.isPlot(iiX,iiY):
					pPlot = gc.getMap().plot(iiX,iiY)
					for i in range(pPlot.getNumUnits()):
						if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
							if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getUnit(i).getTeam()) == True:
								UnitList.append(pPlot.getUnit(i))
	
	if len(UnitList) > 0:
		iDamage = int( gc.getPlayer(caster.getOwner()).getGold() * CAL * 0.05 )
		gc.getPlayer(caster.getOwner()).setGold(0)
		
		iUnit = 0
		while iDamage>0 and len(UnitList)>0:
			
			UnitList[iUnit].changeDamage(1,caster.getOwner())
			if UnitList[iUnit].getDamage() >= 100:
				del UnitList[iUnit]
			else:
				iUnit = iUnit + 1
			if iUnit >= len(UnitList):
				iUnit = 0
			iDamage = iDamage - 1
			
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
		
	return False








#スペル
def req_MEIRIN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MEIRIN1','UNIT_MEIRIN6',cost)

def spell_MEIRIN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	#統合MOD追記部分
	#都市への効力はコメントアウトにて陳腐化
	#if pPlot.isCity():
	#	pCity = pPlot.getPlotCity()
	#	if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_NIJIIRONOHANABATAKE')): #すでに花畑があれば
	#		if pCity.getBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') ) < 1:
	#			pCity.setBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE'),1)
	#		if pCity.getBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') ) < 1:
	#			pCity.setBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE'),1 )
	#	else:
	#		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_NIJIIRONOHANABATAKE'),1)
	#		pCity.setFlowerGardenTurn(10)
	#		pCity.setBuildingHappyChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , 1 )
	#		pCity.setBuildingHealthChange( gc.getInfoTypeForString('BUILDINGCLASS_NIJIIRONOHANABATAKE') , 1 )

	#統合MOD追記部分
	#花壇があれば強制成長させる
	
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM'):
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_2'))
	
	elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_2'):
		cost = 0.1
		if caster.getPower()>=cost:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_3'))
			caster.setPower(caster.getPower() - cost)
	
	elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_3'):
		cost = 0.3
		if caster.getPower()>=cost:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_KOUMAKAN_FARM_4'))
			caster.setPower(caster.getPower() - cost)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_MEIRIN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MEIRIN1','UNIT_MEIRIN6',cost)

def spell_MEIRIN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_NAIKIKOU1',True,100,True,False,False,-1,True,True,True,True,-1,True)
	Functions.changeDamage(RangeList0,caster,-CAL/2,-CAL/2,100,False,True,False,False,-1,True,True,True,True,-1,True,0,2)
	
	caster.setPower(caster.getPower() - cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#スペル
def req_YUKARI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YUKARI1','UNIT_YUKARI6',cost) or Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YUKARI1_HAKUREI','UNIT_YUKARI6_HAKUREI',cost)

def spell_YUKARI_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		iCiv = caster.getCivilizationType()
		#白玉楼・紫の場合、藍召喚
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_FRANCE'):
			if gc.getInfoTypeForString('UNIT_RAN1') <= pUnit.getUnitType() and  pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_RAN6'):
				pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
				pUnit.changeMoves(-100)
				pUnit.setNumCombatCombo(0)
		#博麗神社・紫の場合、霊夢召喚
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_JAPAN'):
			if gc.getInfoTypeForString('UNIT_REIMU1') <= pUnit.getUnitType() and  pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_REIMU6'):
				pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
				pUnit.changeMoves(-100)
				pUnit.setNumCombatCombo(0)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_YUKARI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_YUKARI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_YUKARI6'):
			return True
		if gc.getInfoTypeForString('UNIT_YUKARI1_HAKUREI') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_YUKARI6_HAKUREI'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
			if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')) and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
				Flag = True
				py = PyPlayer(caster.getOwner()) #すでにスキマユニットが居ないかを探す
				for pUnit in py.getUnitList():
					if gc.getInfoTypeForString('UNIT_SUKIMA') == pUnit.getUnitType():
						Flag = False
				return Flag
	return False

	
	

def spell_YUKARI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	newUnit1 = gc.getPlayer(caster.getOwner()).initUnit(gc.getInfoTypeForString('UNIT_SUKIMA'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_YUKARI_PHANTASM2(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_YUKARI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_YUKARI6'):
			return True
		if gc.getInfoTypeForString('UNIT_YUKARI1_HAKUREI') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_YUKARI6_HAKUREI'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False and caster.getPower() >= cost:
			if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')) and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
				Flag = False
				py = PyPlayer(caster.getOwner()) #すでにスキマユニットが居ないかを探す
				for pUnit in py.getUnitList():
					if gc.getInfoTypeForString('UNIT_SUKIMA') == pUnit.getUnitType():
						#敵対ユニットが居ないかのチェック
						pTeam = gc.getTeam(caster.getTeam())
						for k in range(pUnit.plot().getNumUnits()):
							if pTeam.isAtWar(pUnit.plot().getUnit(k).getTeam()):
								return False
						Flag = True
				return Flag
	return False


def spell_YUKARI_PHANTASM2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	point1 = caster.plot().getPoint()
	
	py = PyPlayer(caster.getOwner()) #スキマユニットを探す
	for pUnit in py.getUnitList():
		if gc.getInfoTypeForString('UNIT_SUKIMA') == pUnit.getUnitType():
			SukimaUnit = pUnit
	
	#スキマユニットの居る場所にCAL人数をワープ
	pPlot = caster.plot()
	UnitList = []
	WarpUnitList = []
	WarpUnitList.append(caster)
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).getID() != caster.getID():
			UnitList.append( pPlot.getUnit(i) )
	while len(WarpUnitList) < CAL and len(UnitList) > 0:
		UnitNum = gc.getGame().getSorenRandNum(len(UnitList), "sukima warp")
		WarpUnitList.append(UnitList[UnitNum])
		del UnitList[UnitNum]
	for pUnit in WarpUnitList:
		pUnit.setXY(SukimaUnit.getX(),SukimaUnit.getY(),False,True,True)
		pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		#pUnit.finishMoves()
	
	SukimaUnit.changeDamage(100,caster.getOwner())
	
	caster.setPower(caster.getPower() - cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point2 = caster.plot().getPoint()
	
	#移動前の場所で発生するエフェクト
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point1)
	CyAudioGame().Play3DSound("AS3D_spell_use",point1.x,point1.y,point1.z)
	
	#移動後の場所で発生するエフェクト
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point2)
	CyAudioGame().Play3DSound("AS3D_spell_use",point2.x,point2.y,point2.z)
	
	return True


def req_YUKARI_PHANTASM3(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YUKARI1','UNIT_YUKARI6',cost) or Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YUKARI1_HAKUREI','UNIT_YUKARI6_HAKUREI',cost)

def spell_YUKARI_PHANTASM3(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlayer = gc.getPlayer(caster.getOwner())

	if gc.getPlayer(caster.getOwner()).getGold() >= CAL:
		if caster.plot().getTeam() == caster.getTeam():
			
			RandNum = gc.getGame().getSorenRandNum(100, "Yukari Phantasm 3") 
			if RandNum < 1: #偉人召喚
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PROPHET') + gc.getGame().getSorenRandNum(7, "Yukari Phantasm 3"), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			else:
				
				#召喚可能なリストの作成
				UnitList = []
				for i in range( gc.getNumUnitInfos() ):
					if gc.getUnitInfo(i).getDomainType() == gc.getInfoTypeForString('DOMAIN_LAND'):
						if (
							gc.getUnitInfo(i).getCombat() <= CAL and
							gc.getUnitInfo(i).getCombat() > 0 and
							gc.getUnitInfo(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS') and
							gc.getUnitInfo(i).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY') and
							gc.getUnitInfo(i).getUnitCombatType() != gc.getInfoTypeForString('NONE') 
						):
							UnitList.append(i)
				SummonUnit = gc.getGame().getSorenRandNum(len(UnitList), "Yukari Phantasm 3")
				
				if RandNum < 31: #味方ユニット召喚
					newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SANAE0') + UnitList[SummonUnit], caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				else: #蛮族召喚
			
					plotX = caster.getX()
					plotY = caster.getY()
					#周囲１マスで空いてる場所を探す、なければ消滅
					ClearPlotList = []
					for iX in range(plotX-1,plotX+2):
						for iY in range(plotY-1,plotY+2):
							if gc.getMap().plot(iX,iY).getNumUnits() == 0:
								ClearPlotList.append([iX,iY])
								
					if len(ClearPlotList)!=0:
						iNum = gc.getGame().getSorenRandNum(len(ClearPlotList), "create barbarian plot")
						iiX = ClearPlotList[iNum][0]
						iiY = ClearPlotList[iNum][1]
						newUnit1 = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(gc.getInfoTypeForString('UNIT_SANAE0') + UnitList[SummonUnit], iiX, iiY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
			gc.getPlayer(caster.getOwner()).changeGold(-CAL)
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			
			point = caster.plot().getPoint()
			CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
			CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
			
			return True
			
	return False
	
	
	



#かぐやスペル
def req_KAGUYA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList1,caster,CAL,CAL,0,True,False,False,True,-1,False,True,True,True,-1,False,0,0,False,True)
	Functions.changeDamage(RangeList1,caster,CAL/2,CAL/2,0,True,False,False,True,-1,True,False,True,True,-1,False,0,0,False,True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_KAGUYA_EXTRA2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_EXTRA2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pPlot.getPlotCity().changeDefenseDamage(-CAL*5)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_KAGUYA_EXTRA3(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_EXTRA3(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_HINEZUMINOKAWAGOROMO',True,100,True,True,True,-1,True,True,True,True,-1,True,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_KAGUYA_EXTRA4(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_EXTRA4(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList0,caster,-CAL,-CAL,100,False,True,True,False,-1,True,True,True,True,-1,True,0)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_KAGUYA_EXTRA5(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_EXTRA5(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TAMANOEDA'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True



	
def req_KAGUYA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KINKAKUJI'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_KAGUYA_PHANTASM2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_PHANTASM2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	iX = gc.getGame().getSorenRandNum(gc.getMap().getGridWidth(),"kaguya phantasm")
	iY = gc.getGame().getSorenRandNum(gc.getMap().getGridWidth(),"kaguya phantasm")
	
	while gc.getMap().plot(iX,iY).isCity(): #都市がある増すだったらやりなおし
		iX = gc.getGame().getSorenRandNum(gc.getMap().getGridWidth(),"kaguya phantasm")
		iY = gc.getGame().getSorenRandNum(gc.getMap().getGridWidth(),"kaguya phantasm")
	
	pPlot = gc.getMap().plot(iX,iY)
	pPlot.setPlotType(PlotTypes.PLOT_PEAK,True,True)
	pPlot.setBonusType(-1)
	pPlot.setImprovementType(-1)
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getDamage() < 99:
			pUnit.changeDamage(  (100-pUnit.getDamage())/2  ,caster.getOwner())
	
	CyInterface().addImmediateMessage("&#19990;&#30028;&#12398;&#12393;&#12371;&#12363;&#12391;&#28779;&#23665;&#12364;&#22132;&#28779;&#12375;&#12414;&#12375;&#12383;","")
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	point2 = gc.getMap().plot(iX,iY).getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point2)
	CyAudioGame().Play3DSound("AS3D_spell_use",point2.x,point2.y,point2.z)
	
	return True


def req_KAGUYA_PHANTASM3(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_KAGUYA1','UNIT_KAGUYA6',cost)

def spell_KAGUYA_PHANTASM3(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ILMENITEFORGE'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_KAGUYA_PHANTASM4(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_KAGUYA1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_KAGUYA6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False and caster.getPower() >= cost:
				if caster.getNumSpellPhantasmBreakTime() <= 0:
					return True
	return False

def spell_KAGUYA_PHANTASM4(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MYSTERYIUM'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	#iNumBreakTime = 3
	#ゲーム速度による変化
	#if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
	#	iNumBreakTime = iNumBreakTime * 100 / 50
	#if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
	#	iNumBreakTime = iNumBreakTime * 100 / 75
	#if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
	#	iNumBreakTime = iNumBreakTime * 100 / 125
	#if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
	#	iNumBreakTime = iNumBreakTime * 100 / 150
	#	
	#caster.setNumSpellPhantasmBreakTime(iNumBreakTime)
	
	caster.setPower(caster.getPower() - cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#スペル
def req_TENSHI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_TENSHI1','UNIT_TENSHI6',cost)

def spell_TENSHI_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	YumiFlag = False
	HakuheiFlag = False
	KiheiFlag = False
	HeikiFlag = False
	KakiFlag = False
	SoukouFlag = False
	TohoFlag= False
	
	for iX in range(caster.getX()-1,caster.getX()+2):
		for iY in range(caster.getY()-1,caster.getY()+2):
			if Functions.isPlot(iX,iY):
				pPlot = gc.getMap().plot(iX,iY);
				for i in range(pPlot.getNumUnits()):
					if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getUnit(i).getTeam()):
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
							YumiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
							HakuheiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MOUNTED'):
							KiheiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
							HeikiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN'):
							KakiFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARMOR'):
							SoukouFlag = True
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
							TohoFlag = True
	
	if YumiFlag and CAL>=1:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COVER'),True)
	if TohoFlag and CAL>=1:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ANTI_BOSS1'),True)
	if HakuheiFlag and CAL>=4:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_SHOCK'),True)
	if KiheiFlag and CAL>=8:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_FORMATION'),True)
	if HeikiFlag and CAL>=8:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_CHARGE'),True)
	if KakiFlag and CAL>=12:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_PINCH'),True)
	if SoukouFlag and CAL>=16:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_AMBUSH'),True)
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_TENSHI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_TENSHI1','UNIT_TENSHI6',cost)

def spell_TENSHI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	if caster.plot().getTeam() == caster.getTeam() and caster.plot().getPlotType() != PlotTypes.PLOT_OCEAN:
		caster.plot().setPlotType(PlotTypes.PLOT_HILLS,True,True)
		if caster.plot().isCity():
			caster.plot().getPlotCity().setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KANAMEISHI'),1)
			
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True

	return False





#おりんスペル
def req_RIN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return False #Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_RIN1','UNIT_RIN6',cost)

def spell_RIN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	#未使用スペル枠
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_RIN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_RIN1','UNIT_RIN6',cost)

def spell_RIN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_ZOMBIEFAIRY',True,100,True,True,False,-1,True,True,True,True,-1,True,0,3)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_SPELL_RIN_TO_CAT(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_RIN1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_RIN6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_EXTRA')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RIN_SKILL1')):
			if caster.getPower()>=cost:
				if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
					return True
	return False

def spell_SPELL_RIN_TO_CAT(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	#猫化
	RevivalUnit = caster.getUnitType() - gc.getInfoTypeForString("UNIT_RIN1") + gc.getInfoTypeForString("UNIT_RIN_CATMODE1")
	newUnit1 = pPlayer.initUnit(RevivalUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.convert(caster)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CATMODE'),True)
	
	newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_SPELL_RIN_TO_RIN(bTestVisible,caster,sCAL,eCAL,cost):
	
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_RIN_CATMODE1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_RIN_CATMODE6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_EXTRA')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RIN_SKILL1')):
			if caster.getPower()>=cost:
				if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
					return True
	return False


def spell_SPELL_RIN_TO_RIN(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	
	#猫耳化
	RevivalUnit = caster.getUnitType() - gc.getInfoTypeForString("UNIT_RIN_CATMODE1") + gc.getInfoTypeForString("UNIT_RIN1")
	newUnit1 = pPlayer.initUnit(RevivalUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.convert(caster)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CATMODE'),False)
	
	newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
	



#スペル
def req_LETTY_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_LETTY1','UNIT_LETTY6',cost)

def spell_LETTY_EXTRA1(caster,cost):
	
	if caster.plot().getTeam() == caster.getTeam():
		CAL = caster.countCardAttackLevel()
									
		#地形が順番に変化
		pPlot = caster.plot()
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
			#pPlot.setFeatureType (gc.getInfoTypeForString('FEATURE_SNOWMAN'),1)
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_SNOWMAN'))
		elif pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_SNOW'),True,True)
		elif pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_TUNDRA'),True,True)
		elif pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_GRASS') or pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
		
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	return False
	
	
def req_LETTY_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_LETTY1','UNIT_LETTY6',cost)

def spell_LETTY_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	RangeList = []
	for x in range(-CAL/4,CAL/4+2):
		for y in range(-CAL/4-1,CAL/4+2):
			RangeList.append([x,y])
			
	Functions.setPromotion(RangeList,caster,'PROMOTION_FROST',True,CAL,False,False,True,-1,False,True,True,True,-1,False,0,4,False,False,-1,+1)
	Functions.setPromotion(RangeList,caster,'PROMOTION_FROST',True,CAL/2,False,False,True,-1,True,False,True,True,-1,False,0,4,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#スペル
def req_MIMA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MIMA1','UNIT_MIMA6',cost)

def spell_MIMA_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_HAKUREIJINJANOONRYOU'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_MIMA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MIMA1','UNIT_MIMA6',cost)

def spell_MIMA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	RangeList = []
	for x in range(-CAL/4,CAL/4+2):
		for y in range(-CAL/4-1,CAL/4+2):
			RangeList.append([x,y])
			
	Functions.setPromotion(RangeList,caster,'PROMOTION_KUONNOYUME',True,CAL,False,False,True,-1,False,True,True,True,-1,False,0,4,False,False,-1,+1)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#
def req_EIKI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_EIKI1','UNIT_EIKI6',cost)

def spell_EIKI_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_RAKUENNOSAIKOUSAI'),1)	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_EIKI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_EIKI1','UNIT_EIKI6',cost)

def spell_EIKI_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	UnitList = []
	iNumUnit = pPlot.getNumUnits()
	for i in range(iNumUnit):
		pUnit = pPlot.getUnit(i)
		if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_BOSS") and pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
			if pUnit.getTeam() == caster.getTeam():
				if (pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_WHITE")) == False) and (pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_BLACK")) == False):
					UnitList.append(pUnit)
	
	if len(UnitList) != 0:
		iLoopNum = CAL/3+1
		if iLoopNum > len(UnitList):
			iLoopNum = len(UnitList)
		for i in range(iLoopNum):
			iRandNum = gc.getGame().getSorenRandNum(len(UnitList),"eiki Phantasm Spell")
			pUnit = UnitList.pop(iRandNum)
			if gc.getGame().getSorenRandNum(100, "write or black") < 50:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WHITE'),True)
			else:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLACK'),True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def help_EIKI_PHANTASM1(szText, caster, CAL):

	CvGameUtils.doprint(szText)
	if szText == "001":
		return CAL/3+1




#
def req_NAZRIN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_NAZRIN1','UNIT_NAZRIN6',cost)

def spell_NAZRIN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_RATHOLE'),1)
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_NAZRIN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_NAZRIN1','UNIT_NAZRIN6',cost)

def spell_NAZRIN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	BonusList = [ 'BONUS_SILK', 'BONUS_DYE', 'BONUS_SPICES', 'BONUS_INCENSE', 'BONUS_GEMS',]
	
	if pPlot.getBonusType(caster.getTeam()) == -1 and caster.plot().getPlotType() != PlotTypes.PLOT_OCEAN:
		BonusType = gc.getGame().getSorenRandNum(len(BonusList),"nazrin Ex spell")
		pPlot.setBonusType(gc.getInfoTypeForString(BonusList[BonusType]))
		
		caster.setPower(caster.getPower() - cost)
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False







#
def req_KOGASA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_KOGASA1','UNIT_KOGASA6',cost)

def spell_KOGASA_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SCARY_HOUSE'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_KOGASA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_KOGASA1','UNIT_KOGASA6',cost)

def spell_KOGASA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_OOPS',True,CAL*4,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#
def req_ICHIRIN_SKILL1(bTestVisible,caster,sCAL,eCAL,cost):
	flag = Functions.req_Spell(bTestVisible,caster,'PROMOTION_ICHIRIN_SKILL1','UNIT_ICHIRIN1','UNIT_ICHIRIN6',cost)
	if bTestVisible:
		return flag
	if caster.getSpecialNumber() > 0:
		return False
	return flag

def spell_ICHIRIN_SKILL1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(caster.getLevel()/4+1):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_UNARGUABLE_PUNCH'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'),True)
		newUnit1.setSpecialNumber(caster.baseCombatStr()-1)
		
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT1')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT2')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT2'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT3')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT3'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT4')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT4'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT5')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT5'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_COMBAT6')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT6'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL1')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL1'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL2')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL2'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL3')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL3'),True)
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOHO_DRILL4')):
			newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DRILL4'),True)
		
	caster.setSpecialNumber(1) #げんこつ使用フラグ
	#caster.setPower(caster.getPower()-cost)
	
	#画面更新用
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_ICHIRIN_SKILL1'),False )
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_ICHIRIN_SKILL1'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True




def req_ICHIRIN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_ICHIRIN1','UNIT_ICHIRIN6',cost)

def spell_ICHIRIN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Religion = gc.getPlayer(caster.getOwner()).getStateReligion()
	Building = -10
	if Religion == gc.getInfoTypeForString('RELIGION_JUDAISM'):
		Building = gc.getInfoTypeForString('BUILDING_JEWISH_TEMPLE')
	if Religion == gc.getInfoTypeForString('RELIGION_CHRISTIANITY'):
		Building = gc.getInfoTypeForString('BUILDING_CHRISTIAN_TEMPLE')
	if Religion == gc.getInfoTypeForString('RELIGION_ISLAM'):
		Building = gc.getInfoTypeForString('BUILDING_ISLAMIC_TEMPLE')
	if Religion == gc.getInfoTypeForString('RELIGION_HINDUISM'):
		Building = gc.getInfoTypeForString('BUILDING_HINDU_TEMPLE')
	if Religion == gc.getInfoTypeForString('RELIGION_BUDDHISM'):
		Building = gc.getInfoTypeForString('BUILDING_BUDDHIST_TEMPLE')
	if Religion == gc.getInfoTypeForString('RELIGION_CONFUCIANISM'):
		Building = gc.getInfoTypeForString('BUILDING_CONFUCIAN_TEMPLE')
	if Religion == gc.getInfoTypeForString('RELIGION_TAOISM'):
		Building = gc.getInfoTypeForString('BUILDING_TAOIST_TEMPLE')
	
	pPlot = caster.plot()
	if pPlot.isCity() and Building != -10:
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(Building,1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_ICHIRIN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_ICHIRIN1','UNIT_ICHIRIN6',cost)

def spell_ICHIRIN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iX = caster.getX()
	iY = caster.getY()
	UnitList = []
	
	for iiX in range(iX-1,iX+2):
		for iiY in range(iY-1,iY+2):
			if iiX!=iX or iiY!=iY:
				if Functions.isPlot(iiX,iiY):
					pPlot = gc.getMap().plot(iiX,iiY)
					for i in range(pPlot.getNumUnits()):
						if pPlot.getUnit(i).getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
							if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getUnit(i).getTeam()) == True:
								UnitList.append(pPlot.getUnit(i))
								
	if len(UnitList) != 0:
		for i in range(CAL*2):
			UnitNum = gc.getGame().getSorenRandNum(len(UnitList),"YOUMU Phantasm")
			iDamage = (100 - UnitList[UnitNum].getDamage()) * 15 / 100
			iDamage = iDamage * (100 - UnitList[UnitNum].countSpellTolerance()) / 100
			UnitList[UnitNum].changeDamage(iDamage,caster.getOwner())
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#
def req_MINAMITSU_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MINAMITSU1','UNIT_MINAMITSU6',cost)

def spell_MINAMITSU_EXTRA1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_MEIRENJI1")):
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MEIRENJI1"),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MEIRENJI2"),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MEIRENJI3"),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MEIRENJI4"),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MEIRENJI5"),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MEIRENJI6"),0)
			newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SEIRENSEN'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_MINAMITSU_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MINAMITSU1','UNIT_MINAMITSU6',cost)

def spell_MINAMITSU_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pMap = gc.getMap()
	iWidth = pMap.getGridWidth()
	iHeight = pMap.getGridHeight()
	
	for iX in range(iWidth):
		for iY in range(iHeight):
			pPlot = gc.getMap().plot(iX,iY)
			if pPlot.getPlotType() == PlotTypes.PLOT_OCEAN:
				if pPlot.getTeam() == caster.getTeam():
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_VORTEX'),1)
					pPlot.setNumVortexTrun(3)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#
def req_SYOU_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SYOU1','UNIT_SYOU6',cost)

def spell_SYOU_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	if ( pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_COTTAGE') or
	     pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_HAMLET') ):
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_VILLAGE'))
		caster.setPower(caster.getPower() - cost)
		
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	return False
	
	
def req_SYOU_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SYOU1','UNIT_SYOU6',cost)

def spell_SYOU_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GATHERING_TREASURE1'),1)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GATHERING_TREASURE2'),1)
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GATHERING_TREASURE3'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#
def req_BYAKUREN_SKILL1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_BYAKUREN_SKILL1','UNIT_BYAKUREN1','UNIT_BYAKUREN6',cost)

def spell_BYAKUREN_SKILL1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	caster.changeDamage(-50,caster.getOwner())
		
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	



def req_BYAKUREN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_BYAKUREN1','UNIT_BYAKUREN6',cost)

def spell_BYAKUREN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BYAKUREN_SERMON'),1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_BYAKUREN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_BYAKUREN1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_BYAKUREN6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_PHANTASM')):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if caster.getNumSpellPhantasmBreakTime() <= 0:
					return True
	return False

def spell_BYAKUREN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.changePopulation( CAL/8 + 1 )
		
		iNumBreakTime = 3
		#ゲーム速度による変化
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
			iNumBreakTime = iNumBreakTime * 100 / 50
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
			iNumBreakTime = iNumBreakTime * 100 / 75
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
			iNumBreakTime = iNumBreakTime * 100 / 125
		if gc.getGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_TENGU'):
			iNumBreakTime = iNumBreakTime * 100 / 150
		caster.setNumSpellPhantasmBreakTime(iNumBreakTime)
		
		caster.setPower(caster.getPower()-cost)
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	
	return False







#
def req_NUE_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_NUE1','UNIT_NUE6',cost)

def spell_NUE_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pMap = gc.getMap()
	iWidth = pMap.getGridWidth()
	iHeight = pMap.getGridHeight()
	
	for iX in range(iWidth):
		for iY in range(iHeight):
			pPlot = gc.getMap().plot(iX,iY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_RED_UFO'):
					pUnit.setSpecialNumber(CAL)
					
					#戦闘力更新用
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_NUE_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_NUE1','UNIT_NUE6',cost)

def spell_NUE_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	killList = []
	createNum = 0
	
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if gc.getInfoTypeForString('UNIT_PROPHET') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_GREAT_SPY'):
			if pUnit.getTeam() == caster.getTeam():
				killList.append(pUnit)
				createNum = createNum + 1
			
	for pUnit in killList:
		pUnit.changeDamage(100,caster.getOwner())
	for i in range(createNum):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PROPHET') + gc.getGame().getSorenRandNum(7, "nue Phantasm"), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	caster.setPower(caster.getPower() - cost)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#芳香

def req_YOSHIKA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YOSHIKA1','UNIT_YOSHIKA6',cost)

def spell_YOSHIKA_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.changeDamage(RangeList0,caster,-CAL,-CAL,100,False,True,True,False,-1,True,True,True,True,-1,True,0)
				
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)

	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

	return True
	
	
def req_YOSHIKA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YOSHIKA1','UNIT_YOSHIKA6',cost)

def spell_YOSHIKA_PHANTASM1(caster,cost):
	
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SCORE_DESIRE'),True)
	caster.setNumTurnPromo(caster.getNumTurnPromo() +1)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#青娥

def req_SEIGA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SEIGA1','UNIT_SEIGA6',cost)

def spell_SEIGA_EXTRA1(caster,cost):
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_KABENUKE',True,100,True,False,False,-1,True,True,True,True,-1,True,0,0,False,False,-1,+1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_SEIGA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SEIGA1','UNIT_SEIGA6',cost)

def spell_SEIGA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if gc.getInfoTypeForString('UNIT_YOSHIKA1') <= pUnit.getUnitType() and  pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_YOSHIKA6'):
			pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
			pUnit.changeDamage(-100-pUnit.countCardAttackLevel(),caster.getOwner())
			
	Functions.changeDamage(RangeList0,caster,-CAL*4/3,-CAL*4/3,100,False,True,True,False,-1,False,True,True,True,-1,True,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#屠自古

def req_TOJIKO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_TOJIKO1','UNIT_TOJIKO6',cost)

def spell_TOJIKO_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ZUIGAKUKENKYUU'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_TOJIKO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_TOJIKO1','UNIT_TOJIKO6',cost)

def spell_TOJIKO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_IRUKANOKAMINARI'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#布都

def req_FUTO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_FUTO1','UNIT_FUTO6',cost)

def spell_FUTO_EXTRA1(caster,cost):
	
	if caster.plot().getTeam() == caster.getTeam():
		CAL = caster.countCardAttackLevel()
		
		for iX in range(-1,2):
			for iY in range(-1,2):
				if Functions.isPlot(caster.getX()+iX,caster.getY()+iY):
					pPlot = gc.getMap().plot(caster.getX()+iX,caster.getY()+iY)
					if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RYUMYAKU'):
						pPlot = caster.plot()
						if pPlot.getBonusType(caster.getTeam()) == -1:
							if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_COAST') and pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_OCEAN'):
								if pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_FOREST') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_JUNGLE') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_OASIS'):
									pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_RYUKETU'))

		caster.setPower(caster.getPower()-cost)
		
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
		point = caster.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
		return True
	return False
	
def req_FUTO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_FUTO1','UNIT_FUTO6',cost)

def spell_FUTO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_AMANOIWAHUNE'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True







#神子

def req_MIMIMIKO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_MIMIMIKO1','UNIT_MIMIMIKO6',cost)

def spell_MIMIMIKO_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_OOPARTS'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def req_MIMIMIKO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_MIMIMIKO1','UNIT_MIMIMIKO6',cost)

def spell_MIMIMIKO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if gc.getInfoTypeForString('UNIT_TOJIKO1') <= pUnit.getUnitType() and  pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_TOJIKO6'):
			pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
			pUnit.changeMoves(-100)
		if gc.getInfoTypeForString('UNIT_FUTO1') <= pUnit.getUnitType() and  pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_FUTO6'):
			pUnit.setXY(caster.getX(),caster.getY(),False,True,True)
			pUnit.changeMoves(-100)
			
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True





#八橋EX/PH

def req_YATUHASHI_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YATUHASHI1','UNIT_YATUHASHI6',cost)

def spell_YATUHASHI_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		#仏教採用中（都市に仏像があれば）は強化版を設置
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_BUTUZOU")):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SYOGYOU_MUJOU_B'),1)
		
		else:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SYOGYOU_MUJOU_A'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_YATUHASHI_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YATUHASHI1','UNIT_YATUHASHI6',cost)

def spell_YATUHASHI_PHANTASM1(caster,cost):
	
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iNumUnit = pPlot.getNumUnits()
	UnitList = []
	
	#スタック内に大芸術家がいるかどうかの捜索
	for i in range(iNumUnit):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ARTIST'):
			if pUnit.getTeam() == caster.getTeam():
				UnitList.append(i)
	
	#その中から一人を抜き出して核兵器化
	if len(UnitList)>0:
		pUnit = pPlot.getUnit( UnitList[ gc.getGame().getSorenRandNum(len(UnitList), "BUNKA BOMB") ] )
		pUnit.changeDamage(100,caster.getOwner())
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CULTURE_BOMB'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#べんべんEX/PH

def req_BENBEN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_BENBEN1','UNIT_BENBEN6',cost)

def spell_BENBEN_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		#都市にアンコールワットがあれば強化版を設置
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_ANGKOR_WAT")):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GION_SYOUJA_B'),1)
		
		else:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GION_SYOUJA_A'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_BENBEN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_BENBEN1','UNIT_BENBEN6',cost)

def spell_BENBEN_PHANTASM1(caster,cost):
	
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iNumUnit = pPlot.getNumUnits()
	UnitList = []

	#スタック内に偉人がいるかどうかの捜索
	
	for i in range(iNumUnit):
		pUnit = pPlot.getUnit(i)
		if gc.getInfoTypeForString('UNIT_PROPHET') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_GREAT_SPY'):
			if pUnit.getTeam() == caster.getTeam():
				UnitList.append(i)
	
	#その中から一人を抜き出して大芸術家に変換
	#核芸術家と殆ど同じ処理なのは気にしない
	
	if len(UnitList)>0:
		pUnit = pPlot.getUnit( UnitList[ gc.getGame().getSorenRandNum(len(UnitList), "BUNKA BOMB") ] )
		pUnit.changeDamage(100,caster.getOwner())
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARTIST'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#正邪EX/PH

def req_SEIJA_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SEIJA1','UNIT_SEIJA6',cost)

def spell_SEIJA_EXTRA1(caster,cost):
	
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iNumUnit = pPlot.getNumUnits()
	
	#範囲1マス内にいる味方及び敵対ユニットの都市駐留・攻撃の反転
	
	for iX in range(caster.getX()-1,caster.getX()+2):
		for iY in range(caster.getY()-1,caster.getY()+2):
			if Functions.isPlot(iX,iY):
				pPlot = gc.getMap().plot(iX,iY);
				for i in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					if pUnit.getTeam() == caster.getTeam() or gc.getTeam(caster.getTeam()).isAtWar(pUnit.getTeam()):
						if (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER1')) and pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1'))) == False:
							if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER1')):
								pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER1'),False)
								pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1'),True)
								if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER2')):
									pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER2'),False)
									pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON2'),True)
									if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER3')):
										pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER3'),False)
										pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON3'),True)
							elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1')):
								pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1'),False)
								pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER1'),True)
								if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON2')):
									pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON2'),False)
									pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER2'),True)
									if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON3')):
										pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON3'),False)
										pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER3'),True)

	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
	
def req_SEIJA_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SEIJA1','UNIT_SEIJA6',cost)

def spell_SEIJA_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	
	#ユニット針妙丸の捜索
	
	if pPlayer.getNumWorldSpell()>0:
	
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if gc.getInfoTypeForString('UNIT_SHINMYOUMARU1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_SHINMYOUMARU6'):
				if caster.getTeam() == pPlot.getUnit(i).getTeam():
					break
	
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHINMYOUMARU')):
			shinmyoumarucost = 1.00
			#以下、針妙丸が居る場合の処理
			if (pUnit.getPower()>=shinmyoumarucost) and (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPELL_CASTED')) == False):
				#Functions.setPromotion(RangeList0,caster,'PROMOTION_UCHIDENO_KODUCHI_3TURN',False,100,True,True,True,-1,True,True,True,True,-1,True)
				#Functions.setPromotion(RangeList0,caster,'PROMOTION_UCHIDENO_KODUCHI_2TURN',False,100,True,True,True,-1,True,True,True,True,-1,True)
				#Functions.setPromotion(RangeList0,caster,'PROMOTION_UCHIDENO_KODUCHI_1TURN',False,100,True,True,True,-1,True,True,True,True,-1,True)
				#Functions.setPromotion(RangeList0,caster,'PROMOTION_KODUCHI_HANDOU_3TURN',False,100,True,True,True,-1,True,True,True,True,-1,True)
				#Functions.setPromotion(RangeList0,caster,'PROMOTION_KODUCHI_HANDOU_2TURN',False,100,True,True,True,-1,True,True,True,True,-1,True)
				#Functions.setPromotion(RangeList0,caster,'PROMOTION_KODUCHI_HANDOU_1TURN',False,100,True,True,True,-1,True,True,True,True,-1,True)
			
				Functions.setPromotion(RangeList0,caster,'PROMOTION_UCHIDENO_KODUCHI_5TURN',True,100,True,False,False,-1,False,True,True,True,-1,True,0,0,False,False,-1,+1)
			
				for i in range(pPlot.getNumUnits()):
					pSiege = pPlot.getUnit(i)
					if caster.getTeam() == pPlot.getUnit(i).getTeam():
						if pPlot.getUnit(i).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
							pSiege.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TSUKUMOGAMI'),True)
			
			pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			pUnit.setPower(pUnit.getPower()-shinmyoumarucost)
			pPlayer.setNumWorldSpell(0)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#しんみょうまるEX/PH

def req_SHINMYOUMARU_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SHINMYOUMARU1','UNIT_SHINMYOUMARU6',cost)

def spell_SHINMYOUMARU_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType()  == gc.getInfoTypeForString('UNIT_KOBITO_TYOUSAHEIDAN'):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KISHINKEN_1UP'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KISHINKEN_2UP'),False)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KISHINKEN_3UP'),False)
			
			if CAL <= 12:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KISHINKEN_1UP'),True)
			elif CAL <= 18:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KISHINKEN_2UP'),True)
			else:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KISHINKEN_3UP'),True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	

def req_SHINMYOUMARU_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SHINMYOUMARU1','UNIT_SHINMYOUMARU6',cost)

def spell_SHINMYOUMARU_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if gc.getPlayer(caster.getOwner()).hasTrait(gc.getInfoTypeForString('TRAIT_TRADELIST')):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KOBITO_SYUUKAIJO_B'),1)
		else:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KOBITO_SYUUKAIJO_A'),1)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#雷鼓EX/PH

def req_RAIKO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_RAIKO1','UNIT_RAIKO6',cost)

def spell_RAIKO_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TSUKUMOGAMI')):
			pUnit.changeDamage(-CAL,caster.getOwner())
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PRISTINE_BEAT'),True)
			pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
	
def req_RAIKO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_RAIKO1','UNIT_RAIKO6',cost)

def spell_RAIKO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		#企業本社によって設置する建造物を変える
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CORPORATION_1")):#シリアル・ミル
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TOWER_FARM'),1)
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CORPORATION_2")):#シド寿司
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SOYLENT_SID'),1)
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CORPORATION_3")):#スタンダード・エタノール
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_LITTLE_MAID_FARM'),1)
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CORPORATION_4")):#クリエイティブ建設
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_COBBLESTONE_MAKER'),1)
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CORPORATION_5")):#マイニング社
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BRANCH_MINING'),1)
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CORPORATION_6")):#アルミニウム社
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_FARLEYS_FOUNDRY'),1)
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_CORPORATION_7")):#シヴィライズド・ジュエリー
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_FORTUNE_PICKEL'),1)

	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_RAIKO_PHANTASM2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_RAIKO1','UNIT_RAIKO6',cost)

def spell_RAIKO_PHANTASM2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_A")):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_RAIKO_MAGIC_A'),0)
			iPlayer = pCity.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)#ミステリウム用変数を使用
			
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_RAIKO_MAGIC_B")):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_RAIKO_MAGIC_B'),0)
			#呪法・内の場合は建造物変換処理も
			iPlayer = pCity.getOwner()
			py = PyPlayer(iPlayer)
			pPlayer = gc.getPlayer(iPlayer)
			pPlayer.setMysteryiumFlag(pPlayer.getMysteryiumFlag()+1)#ミステリウム用変数を使用
			for pPyCity in py.getCityList():
				ppCity = pPlayer.getCity(pPyCity.getID())
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_PERSIAN_APOTHECARY")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_GROCER'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PERSIAN_APOTHECARY'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_SPANISH_CITADEL")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CASTLE'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_PORTUGAL_FEITORIA")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CUSTOM_HOUSE'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_PORTUGAL_FEITORIA'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_FACTORY'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_GERMAN_ASSEMBLY_PLANT'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_COAL_PLANT'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_JAPANESE_SHALE_PLANT'),0)
					
				if ppCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_KISHINJOU_AMERICAN_MALL")):
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_SUPERMARKET'),1)
					ppCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_AMERICAN_MALL'),0)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#よりひめEX/PH

def req_YORIHIME_SKILL1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_YORIHIME_SKILL1','UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spell_YORIHIME_SKILL1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	caster.changeDamage(-50,caster.getOwner())
		
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_YORIHIME_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spell_YORIHIME_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	SigenList = ['BONUS_COPPER','BONUS_IRON']

	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MINE'):
		if CAL <= 15:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_GREATMINE1'))
		else:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_GREATMINE2'))
		caster.setPower(caster.getPower()-cost)
		iRandSigen = gc.getGame().getSorenRandNum( (CAL+200),"Yorihime Extra")
		if pPlot.getBonusType(caster.getTeam()) == -1:
			if iRandSigen > 200:
				sigen = gc.getGame().getSorenRandNum(len(SigenList),"Yorihime Extra Sigen")
				caster.plot().setBonusType(gc.getInfoTypeForString(SigenList[sigen]))
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_YORIHIME_EXTRA2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spell_YORIHIME_EXTRA2(caster,cost):
	pPlot = caster.plot()
	iKagamiPercent = (caster.countCardAttackLevel())*4
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if caster.getTeam() == pUnit.getTeam():
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN1')):
				if gc.getGame().getSorenRandNum(100, "spellcard cast") < iKagamiPercent:
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN1'),False )
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3'),True )
					pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN2')):
				if gc.getGame().getSorenRandNum(100, "spellcard cast") < iKagamiPercent:
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN2'),False )
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3'),True )
					pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
			else:
				if gc.getGame().getSorenRandNum(100, "spellcard cast") < iKagamiPercent:
					pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3'),True )
					pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
	
	#八咫鏡の味方付与率はCAL比確率で上下　ただし本人には確定付与
	#ちなみにこれを追記している時点では消失処理がまだ。後々忘れないように
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN1')):
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN1'),False )
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3'),True )
		caster.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
	elif caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN2')):
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN2'),False )
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3'),True )
		caster.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
	else:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_YATANOKAGAMI_TURN3'),True )
		caster.setNumTurnPromo(pUnit.getNumTurnPromo() +1)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_YORIHIME_EXTRA3(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spell_YORIHIME_EXTRA3(caster,cost):
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_FORGE')) and not pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_KAMINOHI')):
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KAMINOHI'),1)
			caster.setPower(caster.getPower()-cost)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_YORIHIME_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spell_YORIHIME_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer.getAmenouzumeFlag() == 0:
		pPlayer.setAmenouzumeFlag(1)
	
	Functions.setPromotion(RangeList1,caster,'PROMOTION_CHARM',True,CAL*2,False,False,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def help_YORIHIME_PHANTASM1(szText, caster, CAL):

	CvGameUtils.doprint(szText)
	if szText == "001":
		return CAL*2


def req_YORIHIME_PHANTASM2(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spell_YORIHIME_PHANTASM2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KOUTENGEN'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_YORIHIME_PHANTASM3(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_YORIHIME1','UNIT_YORIHIME6',cost)

def spell_YORIHIME_PHANTASM3(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	py = PyPlayer(caster.getOwner())
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	bFlag = False
	if CAL > 30:
		CAL = 30
	for pUnit in py.getUnitList():
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_AURIC'):
			pUnit.setSpecialNumber((CAL*3/2)-1)
			bFlag = True
			#戦闘力更新用
			pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
			break
	if bFlag == False:
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AURIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setSpecialNumber((CAL*3/2)-1)
		newUnit1.changeExperience(CAL/3,-1,False,False,False)
		#戦闘力更新用
		pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),False )
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def help_YORIHIME_PHANTASM3(szText, caster, CAL):
	
	CALset = CAL
	if CAL > 30:
		CALset = 30
	
	CvGameUtils.doprint(szText)
	if szText == "001":
		return CAL
	if szText == "002":
		return (CALset*3/2)

#姉の方EX/PH

def req_TOYOHIME_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):

	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_TOYOHIME1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_TOYOHIME6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False and caster.getPower() >= cost:
			if (caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_EXTRA')) or \
			caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOYOHIME_SKILL1'))) and \
			gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
				Flag = True
				py = PyPlayer(caster.getOwner())
				for pUnit in py.getUnitList():
					if gc.getInfoTypeForString('UNIT_TUKINOMITTEI') == pUnit.getUnitType():
						Flag = False
				return Flag
	return False

def spell_TOYOHIME_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	newUnit1 = gc.getPlayer(caster.getOwner()).initUnit(gc.getInfoTypeForString('UNIT_TUKINOMITTEI'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOYOHIME_SKILL1')):
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_COMMANDO'),True )
		newUnit1.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SENTRY'),True )
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_TOYOHIME_EXTRA2(bTestVisible,caster,sCAL,eCAL,cost):
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_TOYOHIME1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_TOYOHIME6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
			if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MODE_EXTRA')) and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
				Flag = False
				py = PyPlayer(caster.getOwner())
				for pUnit in py.getUnitList():
					if gc.getInfoTypeForString('UNIT_TUKINOMITTEI') == pUnit.getUnitType():
						#敵対ユニットが居ないかのチェック
						pTeam = gc.getTeam(caster.getTeam())
						for k in range(pUnit.plot().getNumUnits()):
							if pTeam.isAtWar(pUnit.plot().getUnit(k).getTeam()):
								return False
						Flag = True
				return Flag
	return False

def spell_TOYOHIME_EXTRA2(caster,cost):
	CAL = caster.countCardAttackLevel()
	point1 = caster.plot().getPoint()
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if gc.getInfoTypeForString('UNIT_TUKINOMITTEI') == pUnit.getUnitType():
			MitteiUnit = pUnit
	
	pPlot = caster.plot()
	UnitList = []
	WarpUnitList = []
	WarpUnitList.append(caster)
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).getID() != caster.getID():
			UnitList.append( pPlot.getUnit(i) )
	while len(WarpUnitList) < CAL and len(UnitList) > 0:
		UnitNum = gc.getGame().getSorenRandNum(len(UnitList), "Toyohime warp")
		WarpUnitList.append(UnitList[UnitNum])
		del UnitList[UnitNum]
	for pUnit in WarpUnitList:
		if pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_BOSS') and pUnit.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_STANDBY"):
			pUnit.setXY(MitteiUnit.getX(),MitteiUnit.getY(),False,True,True)
			pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
			#pUnit.finishMoves()
	
	MitteiUnit.changeDamage(100,caster.getOwner())
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point2 = caster.plot().getPoint()
	
	#移動前の場所で発生するエフェクト
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point1)
	CyAudioGame().Play3DSound("AS3D_spell_use",point1.x,point1.y,point1.z)
	
	#移動後の場所で発生するエフェクト
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point2)
	CyAudioGame().Play3DSound("AS3D_spell_use",point2.x,point2.y,point2.z)
	
	return True

def req_TOYOHIME_SKILL1(bTestVisible,caster,sCAL,eCAL,cost):
	if bTestVisible:
		if gc.getInfoTypeForString('UNIT_TOYOHIME1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_TOYOHIME6'):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
			if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_TOYOHIME_SKILL1')):
				Flag = False
				py = PyPlayer(caster.getOwner())
				for pUnit in py.getUnitList():
					if gc.getInfoTypeForString('UNIT_TUKINOMITTEI') == pUnit.getUnitType():
						#敵対ユニットが居ないかのチェック
						pTeam = gc.getTeam(caster.getTeam())
						for k in range(pUnit.plot().getNumUnits()):
							if pTeam.isAtWar(pUnit.plot().getUnit(k).getTeam()):
								return False
						Flag = True
				return Flag
	return False

def spell_TOYOHIME_SKILL1(caster,cost):
	CAL = caster.countCardAttackLevel()
	point1 = caster.plot().getPoint()
	
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if gc.getInfoTypeForString('UNIT_TUKINOMITTEI') == pUnit.getUnitType():
			MitteiUnit = pUnit
	
	pPlot = caster.plot()
	caster.setXY(MitteiUnit.getX(),MitteiUnit.getY(),False,True,True)
	pUnit.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	#pUnit.finishMoves()
	
	MitteiUnit.changeDamage(100,caster.getOwner())
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point2 = caster.plot().getPoint()
	
	#移動前の場所で発生するエフェクト
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point1)
	CyAudioGame().Play3DSound("AS3D_spell_use",point1.x,point1.y,point1.z)
	
	#移動後の場所で発生するエフェクト
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point2)
	CyAudioGame().Play3DSound("AS3D_spell_use",point2.x,point2.y,point2.z)
	
	return True


def req_TOYOHIME_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_TOYOHIME1','UNIT_TOYOHIME6',cost)

def spell_TOYOHIME_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	if CAL <= 8:
		Functions.setPromotion(RangeList1,caster,'PROMOTION_SPELL_CASTED',True,100,False,False,True,-1,True,False,True,True,-1,True,1)
		Functions.setPromotion(RangeList1,caster,'PROMOTION_STAN',True,100,False,False,True,-1,True,False,True,True,-1,False,0,6,False,False,-1,+1)
	elif CAL <= 16:
		Functions.setPromotion(RangeList2,caster,'PROMOTION_SPELL_CASTED',True,100,False,False,True,-1,True,False,True,True,-1,True,1)
		Functions.setPromotion(RangeList2,caster,'PROMOTION_STAN',True,100,False,False,True,-1,True,False,True,True,-1,False,0,6,False,False,-1,+1)
	else:
		Functions.setPromotion(RangeList3,caster,'PROMOTION_SPELL_CASTED',True,100,False,False,True,-1,True,False,True,True,-1,True,1)
		Functions.setPromotion(RangeList3,caster,'PROMOTION_STAN',True,100,False,False,True,-1,True,False,True,True,-1,False,0,6,False,False,-1,+1)
		
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#せーらんEX/PH

def req_SEIRAN_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SEIRAN1','UNIT_SEIRAN6',cost)

def spell_SEIRAN_EXTRA1(caster,cost):
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	CAL = caster.countCardAttackLevel()
	
	for i in range(CAL/6+1):
		newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_EAGLE'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'),True)
	
	caster.setPower(caster.getPower()-cost)
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def help_SEIRAN_EXTRA1(szText, caster, CAL):
	
	CvGameUtils.doprint(szText)
	if szText == "001":
		return (CAL/6+1)


def req_SEIRAN_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	flag = Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SEIRAN1','UNIT_SEIRAN6',cost)
	if bTestVisible:
		return flag
	if caster.getSpecialNumber() > 0:
		return False
	return flag

def spell_SEIRAN_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	Functions.setPromotion(RangeList0,caster,'PROMOTION_SPEED_STRIKE',True,100,True,False,False,-1,True,False,True,True,-1,True,0,0,False,False,-1,+1)
	
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setSpecialNumber(1)
	
	caster.setPower(caster.getPower()-cost)
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#りんごEX/PH

def req_RINGO_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_RINGO1','UNIT_RINGO6',cost)

def spell_RINGO_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DANGOYA'),1)
		caster.setPower(caster.getPower()-cost)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_RINGO_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_RINGO1','UNIT_RINGO6',cost)

def spell_RINGO_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	#pDirection = caster.GetFacingDirection()
	
	if pPlot.getTeam() == caster.getTeam():
		if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_COAST') and \
		pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_OCEAN'):
			pPlot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
			caster.setPower(caster.getPower()-cost)

	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#どれみEX/PH

def req_DOREMY_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_DOREMY1','UNIT_DOREMY6',cost)

def spell_DOREMY_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_COAST') and \
	pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_OCEAN') and \
	caster.plot().isCity() == False:
		pPlot.setRouteType(gc.getInfoTypeForString('ROUTE_DREAM_EXPRESS'))
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def req_DOREMY_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_DOREMY1','UNIT_DOREMY6',cost)

def spell_DOREMY_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DAGON'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#さぐめEX/PH

def req_SAGUME_EXTRA1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_EXTRA','UNIT_SAGUME1','UNIT_SAGUME6',cost)

def spell_SAGUME_EXTRA1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	if CAL<=7:
		iGetJibaku = 2
	elif CAL<=15:
		iGetJibaku = 4
	else:
		iGetJibaku = 6
	
	UnitList = []
	iNumUnit = pPlot.getNumUnits()
	for i in range(iNumUnit):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_SPY'):
			if pUnit.getTeam() == caster.getTeam():
				if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_JIBAKU')):
					UnitList.append(pUnit)
	
	if len(UnitList) != 0:
		iLoopNum = iGetJibaku
		if iLoopNum > len(UnitList):
			iLoopNum = len(UnitList)
		for i in range(iLoopNum):
			iRandNum = gc.getGame().getSorenRandNum(len(UnitList),"Sagume Extra Spell")
			pUnit = UnitList.pop(iRandNum)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_JIBAKU'),True)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.setPower(caster.getPower()-cost)
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def help_SAGUME_EXTRA1(szText, caster, CAL):
	
	CvGameUtils.doprint(szText)
	if szText == "001":
		if CAL<=7:
			return 2
		elif CAL<=15:
			return 4
		else:
			return 6

def req_SAGUME_PHANTASM1(bTestVisible,caster,sCAL,eCAL,cost):
	return Functions.req_Spell(bTestVisible,caster,'PROMOTION_MODE_PHANTASM','UNIT_SAGUME1','UNIT_SAGUME6',cost)

def spell_SAGUME_PHANTASM1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	
	pPlot = caster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KATAYOKU'),1)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#月の都特殊ユニットスペル
#オーリックさん
def req_SPECIAL_AURIC(bTestVisible,caster,sCAL,eCAL,cost):
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_AURIC'):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			return True
	
	return False
	

def spell_SPECIAL_AURIC(caster,cost):
	
	CAL = caster.countCardAttackLevel()

	Functions.changeDamage(RangeList1,caster,10,10,0,False,False,False,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList1,caster,5,5,0,False,False,False,True,-1,True,False,True,True,-1,False,0)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#ハロウィンフィーバー
def req_SPECIAL_HALLOWEEN_FEVER(bTestVisible,caster,sCAL,eCAL,cost):
	pPlot = caster.plot()
	if bTestVisible:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			return True
	
	return False
	

def spell_SPECIAL_HALLOWEEN_FEVER(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	if caster.getTeam() == pPlot.getTeam():
		if pPlot.getImprovementType() != -1:
			Functions.isImprovementUpgrade(caster,pPlot)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#ダンゴフィーバー
def req_SPECIAL_DANGO_FEVER(bTestVisible,caster,sCAL,eCAL,cost):
	pPlot = caster.plot()
	if bTestVisible:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			return True
	
	return False
	

def spell_SPECIAL_DANGO_FEVER(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	if caster.getTeam() == pPlot.getTeam():
		if pPlot.getImprovementType() != -1:
			Functions.isImprovementUpgrade(caster,pPlot)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True




#穢身探知型機雷

def req_SPECIAL_TANTIGATA_KIRAI_1_1(bTestVisible,caster,sCAL,eCAL,cost):
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_3'):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			if gc.getTeam(caster.getTeam()).isAtWar(pPlot.getTeam()):
				if pPlot.getImprovementType() != -1:
					return True
	
	return False
	

def spell_SPECIAL_TANTIGATA_KIRAI_1_1(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()

	pPlot.setImprovementType(-1)
	caster.changeDamage(100,caster.getOwner())
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_SPECIAL_TANTIGATA_KIRAI_1_2(bTestVisible,caster,sCAL,eCAL,cost):
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_4'):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			if caster.getTeam() != pPlot.getTeam():
				if pPlot.getImprovementType() != -1:
					return True
	
	return False
	

def spell_SPECIAL_TANTIGATA_KIRAI_1_2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()

	pPlot.setImprovementType(-1)
	iRandNum = gc.getGame().getSorenRandNum(100,"Sagumespell Seizon Hantei")
	
	if iRandNum < 50:
		caster.changeDamage(100,caster.getOwner())
	else:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_SPECIAL_TANTIGATA_KIRAI_2(bTestVisible,caster,sCAL,eCAL,cost):
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_3') or \
		caster.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_4'):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			return True
	
	return False
	

def spell_SPECIAL_TANTIGATA_KIRAI_2(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()

	Functions.changeDamage(RangeList0,caster,-20,-20,100,False,True,True,False,-1,True,True,True,True,-1,True,0)
	caster.changeDamage(100,caster.getOwner())
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_SPECIAL_TANTIGATA_KIRAI_3(bTestVisible,caster,sCAL,eCAL,cost):
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TANTIGATA_KIRAI_4'):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			return True
	
	return False
	

def spell_SPECIAL_TANTIGATA_KIRAI_3(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()

	Functions.setPromotion(RangeList0,caster,'PROMOTION_POISON2',True,25,False,True,True,-1,False,True,True,True,-1,False,0,0,False,False,-1,+1)
	caster.changeDamage(100,caster.getOwner())
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


def req_SPECIAL_JIBAKU(bTestVisible,caster,sCAL,eCAL,cost):
	pPlot = caster.plot()
	if bTestVisible:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_JIBAKU') ):
			return True
		else:
			return False

	else:
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
			return True
	
	return False
	

def spell_SPECIAL_JIBAKU(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		pCity.changeDefenseDamage(25)
		iRandNum = gc.getGame().getSorenRandNum(100,"Jibaku Hakai Hantei")
		if iRandNum < 75:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_WALLS'),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_WALL_ISSUN'),0)
		if iRandNum < 50:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BUNKER'),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_BOMB_SHELTER'),0)
		if iRandNum < 25:
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_CASTLE'),0)
			pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_KISHINJOU_SPANISH_CITADEL'),0)
		
	Functions.changeDamage(RangeList0,caster,10,20,40,False,False,True,True,-1,False,True,True,True,-1,False,0)
	Functions.changeDamage(RangeList0,caster,5,10,40,False,False,True,True,-1,True,False,True,True,-1,False,0)
	
	caster.changeDamage(100,caster.getOwner())
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

#######################################
#テラフォーミング・平原化系列
def req_TERRAFORM_PLAIN(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_MOON_WAR_FIRST')):
			if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		#色々試したけど、ユニットが常時動く関係上単純な構造だけど多分これでいいと思う
		#犠牲版に限ると無駄が多い記述だけど、どうせ以後にこれらの条件付けが生きてくると思うのでテンプレ代わりに
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
			return False
		
		elif pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
			if caster.isHuman():
				return False
		
		elif pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA') and \
		not pTeam.isHasTech(gc.getInfoTypeForString('TECH_APOLLO_CONSPIRACY')):
			if caster.isHuman():
				return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_PLAIN(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	FeverFlag = False
	
	#これを記述している現時点では使用判定こそ入れていないが、将来的なことも想定しAIが使う場合も記述する
	#その場合AIに限り即反映されるように
	if caster.isHuman():
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
		caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
			FeverFlag = True
		
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_APOLLO_CONSPIRACY')):
				pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'))
		
		else:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'))
	
	else:
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
		
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	if FeverFlag:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
		caster.finishMoves()
	else:
		if caster.isHuman():
			caster.changeDamage(100,caster.getOwner())
		else:
			caster.finishMoves()
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spell_TERRAFORM_PLAIN_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iBonus = pPlot.getBonusType(caster.getTeam())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
	
	if pPlot.getTeam() == caster.getTeam():
		if pPlot.getPlotType() != PlotTypes.PLOT_OCEAN:
			if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_PLAINS'):
				if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_GRASS'):
					if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA') or \
					pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
						estimatePoint = estimatePoint + 100
					if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT'):
						estimatePoint = estimatePoint + 100
						if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
							estimatePoint = estimatePoint + 100
					if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
						estimatePoint = estimatePoint + 100
			
			
					if pPlot.getBonusType(caster.getTeam()) != -1:
						estimatePoint = estimatePoint + 100
	
	if estimatePoint < 90:
		estimatePoint = 0
	
	return estimatePoint

#######################################
#無犠牲版
#こっちが本命
def req_TERRAFORM_PLAIN_NO_SACRIFICE(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_MOON_WAR_FIRST')):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
			return False
		
		elif pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS') and \
		not pTeam.isHasTech(gc.getInfoTypeForString('TECH_SAKE_OF_THE_WATATSUKI')):
			if caster.isHuman():
				return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_PLAIN_NO_SACRIFICE(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	SacrificeFlag = False
	
	if caster.isHuman() and not pTeam.isHasTech(gc.getInfoTypeForString('TECH_THE_TRUMP_CARD_IS_ALWAYS_A_BAD_MOVE')):
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'))
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
			caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
			else:
				SacrificeFlag = True
		
		elif pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_SAKE_OF_THE_WATATSUKI')):
				pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'))
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
				caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
					caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
					caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
				else:
					SacrificeFlag = True
		
		else:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'))
		
	else:
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
			caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
			else:
				SacrificeFlag = True
		elif pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
			caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
			else:
				SacrificeFlag = True
		else:
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
	
	if SacrificeFlag:
		if caster.isHuman():
			caster.changeDamage(100,caster.getOwner())
		else:
			caster.finishMoves()
			caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	else:
		caster.finishMoves()
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・草原化系列
def req_TERRAFORM_GRASS(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_MOON_WAR_FIRST')):
			if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		#平原であることが前提なので、これはこの一行でいいはず
		if not pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
			return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_GRASS(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	FeverFlag = False
	
	#これを記述している現時点では使用判定こそ入れていないが、将来的なことも想定しAIが使う場合も記述する
	#その場合AIに限り即反映されるように
	if caster.isHuman():
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
		caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
			FeverFlag = True
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS'))
	
	else:
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
		
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	if FeverFlag:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
		caster.finishMoves()
	else:
		caster.changeDamage(100,caster.getOwner())
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True

def spell_TERRAFORM_GRASS_Estimate(caster):

	estimatePoint = 0
	CAL = caster.countCardAttackLevel()
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iBonus = pPlot.getBonusType(caster.getTeam())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
	
	if pPlot.getTeam() == caster.getTeam():
		if pPlot.getPlotType() != PlotTypes.PLOT_OCEAN:
			if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_GRASS'):
				if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
					estimatePoint = estimatePoint + 100
					if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
						estimatePoint = estimatePoint + 100
					if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
						estimatePoint = estimatePoint + 100
					if pPlot.getBonusType(caster.getTeam()) != -1:
						estimatePoint = estimatePoint + 100
	
	if estimatePoint < 90:
		estimatePoint = 0
	
	return estimatePoint

#######################################
#無犠牲版
def req_TERRAFORM_GRASS_NO_SACRIFICE(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_MOON_WAR_FIRST')):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		if not pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
			return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_GRASS_NO_SACRIFICE(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	SacrificeFlag = False
	
	if caster.isHuman() and not pTeam.isHasTech(gc.getInfoTypeForString('TECH_THE_TRUMP_CARD_IS_ALWAYS_A_BAD_MOVE')):
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS'))
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
			caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
			else:
				SacrificeFlag = True
		
		elif pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_SAKE_OF_THE_WATATSUKI')):
				pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS'))
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
				caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
					caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
					caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
				else:
					SacrificeFlag = True
		
		else:
			pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS'))
		
	else:
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
			caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
			else:
				SacrificeFlag = True
		elif pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
			if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
			caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
			else:
				SacrificeFlag = True
		else:
			pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
	
	if SacrificeFlag:
		caster.changeDamage(100,caster.getOwner())
	else:
		caster.finishMoves()
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・丘陵化系列
def req_TERRAFORM_HILL(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_APOLLO')):
			if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getPlotType() == PlotTypes.PLOT_HILLS:
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_HILL(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	FeverFlag = False
	
	if caster.isHuman():
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
		caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
			FeverFlag = True
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_HILL'))
	
	else:
		pPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
		
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	if FeverFlag:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
		caster.finishMoves()
	else:
		caster.changeDamage(100,caster.getOwner())
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
#######################################
#無犠牲版
def req_TERRAFORM_HILL_NO_SACRIFICE(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_APOLLO')):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getPlotType() == PlotTypes.PLOT_HILLS:
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_HILL_NO_SACRIFICE(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	
	if caster.isHuman() and not pTeam.isHasTech(gc.getInfoTypeForString('TECH_THE_TRUMP_CARD_IS_ALWAYS_A_BAD_MOVE')):
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_HILL'))
		
	else:
		pPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
	
	caster.finishMoves()
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・平地化系列
def req_TERRAFORM_FLATLAND(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_APOLLO')):
			if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getPlotType() == PlotTypes.PLOT_LAND:
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_FLATLAND(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	FeverFlag = False
	
	if caster.isHuman():
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
		caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
			FeverFlag = True
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FLATLAND'))
	
	else:
		pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
		
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	if FeverFlag:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
		caster.finishMoves()
	else:
		caster.changeDamage(100,caster.getOwner())
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True
#######################################
#無犠牲版
def req_TERRAFORM_FLATLAND_NO_SACRIFICE(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_APOLLO')):
			if pTeam.isHasTech(gc.getInfoTypeForString('TECH_LUNAR_CAPITAL_TRANSFER_PLAN')):
				return True
		else:
			return False

	else:
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getPlotType() == PlotTypes.PLOT_LAND:
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_FLATLAND_NO_SACRIFICE(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	
	if caster.isHuman() and not pTeam.isHasTech(gc.getInfoTypeForString('TECH_THE_TRUMP_CARD_IS_ALWAYS_A_BAD_MOVE')):
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FLATLAND'))
		
	else:
		pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
	
	caster.finishMoves()
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・植林
def req_TERRAFORM_FOREST(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_APOLLO_CONSPIRACY')):
			return True
		else:
			return False

	else:
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_NONE'):
			return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_FOREST(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	FeverFlag = False
	
	if caster.isHuman():
		if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER') ) or \
		caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_DANGO_FEVER') ):
			FeverFlag = True
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FOREST'))
	
	else:
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_REGENERATION_FOREST'), 1)
		
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	if FeverFlag:
		caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HALLOWEEN_FEVER'),False)
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DANGO_FEVER'),False)
		caster.finishMoves()
	else:
		caster.changeDamage(100,caster.getOwner())
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・埋め立て
def req_TERRAFORM_LANDFILL(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_LANDFILLER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_SAKE_OF_THE_WATATSUKI')):
			return True
		else:
			return False

	else:
		if pPlot.getBonusType(caster.getTeam()) != -1:
			return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if pPlot.getNumUnits() == 1:
					if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
					pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN'):
						if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
							return True
	
	return False
	
def spell_TERRAFORM_LANDFILL(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	
	#※注意！
	#本来この処理はそのままやろうとするとゲームが強制終了する
	#（陸と海を埋め立てる時にユニットが存在すると例外処理になってしまいゲームが落ちる
	#その時仮に同時にユニットを消してもゲーム上では存在する事になっているので同じ事）
	#そのためはまき氏の力を借りてSDK側で無理矢理落ちないようにしているが
	#それはそれで「もしも万が一、陸地に他のユニットが存在する状態」だったら何が起こるか分からない
	#なのでもしも私以外の人がスペルの追加をするとなったら
	#この処理だけは神経質なくらい、発動タイルに他のユニットがスタックしている状態だけは回避して
	#その上で同時にキャスターユニットは消滅させ、とにかく「海タイルから陸に上がるヤツ」状態にならないようにすることを推奨
	#何が起こるかわからないし、何が起きても保障はできないため
	
	if pPlot.getNumUnits() == 1 and pPlot.getBonusType(caster.getTeam()) == -1 :
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN'):
			#この例外処理をする場合setTerrainTypeではなくこちらのsetTerrainTypeWithoutUnitEraseを使うように
			#なお上記でも触れたが、これはSDK側の変更が必要なのでその処理をしない限りこのままコピペしても動作はしない
			#もしも他MODでこの処理を参考にしたい場合は注意
			#pPlot.setTerrainTypeWithoutUnitErase(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
			#チルノちゃんのフラグを雑に流用してありえない値を入れておく
			pPlot.setOriginalTerrain(512)
	
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.changeDamage(100,caster.getOwner())
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・砕氷
def req_TERRAFORM_CRUSHICE(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_ICEBREAKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_SAKE_OF_THE_WATATSUKI')):
			return True
		else:
			return False

	else:
		
		if caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
				caster.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN'):
					for iiX in range(iX-1,iX+2):
						for iiY in range(iY-1,iY+2):
							if Functions.isPlot(iiX,iiY):
								pPlot = gc.getMap().plot(iiX,iiY)
								if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_ICE'):
									#if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
									return True
	
	return False
	
def spell_TERRAFORM_CRUSHICE(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	for iiX in range(iX-1,iX+2):
		for iiY in range(iY-1,iY+2):
			if Functions.isPlot(iiX,iiY):
				pPlot = gc.getMap().plot(iiX,iiY)
				if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_ICE'):
					pPlot.setFeatureType (gc.getInfoTypeForString('FEATURE_NONE'),1)
	
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.changeDamage(100,caster.getOwner())
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・海洋化
def req_TERRAFORM_OCEANIZATION(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_OCEANIWORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_SAKE_OF_THE_WATATSUKI')):
			return True
		else:
			return False

	else:
		
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_NONE'):
			return False
		
		elif pPlot.getBonusType(caster.getTeam()) != -1:
			return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if pPlot.getNumUnits() == 1:
					if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
						return True
	
	return False
	
def spell_TERRAFORM_OCEANIZATION(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	
	#※注意！
	#これも埋め立てと同じく本来は強制終了する処理の回避処置が取られている
	#なので上記と同じく発動タイルにユニットが1人も残らないようにすることを推奨
	
	if pPlot.getNumUnits() == 1 and pPlot.getBonusType(caster.getTeam()) == -1 :
		if pPlot.getPlotType() == PlotTypes.PLOT_LAND or \
		pPlot.getPlotType() == PlotTypes.PLOT_HILLS:
			pPlot.setImprovementType(-1)
			pPlot.setRouteType(-1)
			#埋め立てと同じく処理見直し・チルノちゃんのフラグを雑に流用してありえない値を入れておく
			#pPlot.setPlotTypeWithoutUnitErase(PlotTypes.PLOT_OCEAN,True,True)
			pPlot.setOriginalTerrain(513)
	
	#caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	caster.changeDamage(100,caster.getOwner())
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True


#######################################
#テラフォーミング・氾濫源
def req_TERRAFORM_FLOOD(bTestVisible,caster,sCAL,eCAL,cost):
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	
	if bTestVisible:
		if caster.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER') and \
		pTeam.isHasTech(gc.getInfoTypeForString('TECH_THE_TRUMP_CARD_IS_ALWAYS_A_BAD_MOVE')):
			return True
		else:
			return False

	else:
		if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST') or \
		pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_OCEAN') or \
		pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_NONE'):
			return False
		
		elif caster.plot().isCity():
			return False
		
		elif not caster.canMove():
			return False
		
		#可能であれば動的に月の都UWが5人いるかどうかをここで判定したいけど…
		#リストを利用する形だとリストのリセットが上手くいかないため結果的に判定も上手くいかない
		#なにか上手い方法があればどなたかplz
		else:
			if caster.plot().getTeam() == caster.getTeam():
				if caster.isHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED') ) == False:
					return True
	
	return False
	
def spell_TERRAFORM_FLOOD(caster,cost):
	
	CAL = caster.countCardAttackLevel()
	pTeam = gc.getTeam(caster.getTeam())
	pPlot = caster.plot()
	iNumUnit = pPlot.getNumUnits()
	UnitList = []
	
	#妥協案で5人以上いる場合ならスペル成功、いないならスペル発動済みの昇進を与える
	if caster.isHuman():
		for i in range(iNumUnit):
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_TUKI_NO_MIYAKO_WORKER'):
				if pUnit.getTeam() == caster.getTeam():
					UnitList.append(pUnit)
		if len(UnitList)>4:
			for i in range(5):
				iRandNum = gc.getGame().getSorenRandNum(len(UnitList),"Flood Plains Sacrifice")
				pUnit = UnitList.pop(iRandNum)
				pUnit.changeDamage(100,caster.getOwner())
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'), 1)
			pPlot.setImprovementType(-1)
	
	else:
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'), 1)
		
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	
	point = caster.plot().getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	
	return True






#######################################
#以下、世界魔法系列
#######################################

def req_NINGENNOSATO1(bTestVisible,caster,sCAL,eCAL,cost):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCiv = pPlayer.getCivilizationType()
	
	if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
		if pPlayer.getNumWorldSpell()>0:
			if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'): 
				return True
	
	return False

def spell_NINGENNOSATO1(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	pPlayer.changeGoldenAgeTurns(pPlayer.getGoldenAgeLength())
	pPlayer.setNumWorldSpell(0)
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	#人間の里が結束を高め黄金期が発動しました
	CyInterface().addImmediateMessage("&#20154;&#38291;&#12398;&#37324;&#12364;&#32080;&#26463;&#12434;&#39640;&#12417;&#40644;&#37329;&#26399;&#12364;&#30330;&#21205;&#12375;&#12414;&#12375;&#12383;","")

	return True

def req_HYOUSEIRENGOU1(bTestVisible,caster,sCAL,eCAL,cost):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCiv = pPlayer.getCivilizationType()
	
	if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
		if pPlayer.getNumWorldSpell()>0:
			if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'): 
				return True
	
	return False

def spell_HYOUSEIRENGOU1(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	#沸いてくるユニットは時代依存
	iNumUnit = 5
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT'):
		iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
		iNumUnit = 2
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL'):
		iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
		iNumUnit = 3
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL'):
		iUnit = gc.getInfoTypeForString('UNIT_MACEMAN')
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE'):
		iUnit = gc.getInfoTypeForString('UNIT_MUSKETMAN')
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL'):
		iUnit = gc.getInfoTypeForString('UNIT_RIFLEMAN')
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN'):
		iUnit = gc.getInfoTypeForString('UNIT_INFANTRY')
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE'):
		iUnit = gc.getInfoTypeForString('UNIT_MECHANIZED_INFANTRY')
	
	py = PyPlayer(iPlayer)
	for pPyCity in py.getCityList():
		pCity = pPlayer.getCity(pPyCity.getID())
		iNum = pCity.getPopulation() / iNumUnit
		if iNum < 1:
			iNum = 1
		if iNum > 3:
			iNum = 3
		for i in range(iNum):
			newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.changeExperience(gc.getGame().getSorenRandNum(6, "world spell rengou no kessoku"),-1,False,False,False)
	pPlayer.setNumWorldSpell(0)
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	#妖精たちが結束を高め都市に集結しました
	CyInterface().addImmediateMessage("&#22934;&#31934;&#12383;&#12385;&#12364;&#32080;&#26463;&#12434;&#39640;&#12417;&#37117;&#24066;&#12395;&#38598;&#32080;&#12375;&#12414;&#12375;&#12383;","")

	return True



def req_KISHINJOU1(bTestVisible,caster,sCAL,eCAL,cost):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCiv = pPlayer.getCivilizationType()
	
	if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALI'):
		if pPlayer.getNumWorldSpell()>0:
			if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'): 
				return True
	
	return False

def spell_KISHINJOU1(caster,cost):
	#caster=CyInterface().getHeadSelectedUnit()
	#caster.setMadeAttack(True)
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	
	TAIKOFlag = False
	TYUUSEIFlag = False
	KINDAIFlag = False
	
	#時代によって沸かせるユニットや計算式を変動させる
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TAIKO')
		iNumCityCountKOU = 3
		TAIKOFlag = True
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TYUUSEI')
		iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_TYUUSEI')
		iNumCityCountKOU = 5
		iNumCityCountOTU = 8
		TYUUSEIFlag = True
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_KINDAI')
		iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_KINDAI')
		iNumCityCountKOU = 5
		iNumCityCountOTU = 8
		KINDAIFlag = True
	
	py = PyPlayer(iPlayer)
	for pPyCity in py.getCityList():
		pCity = pPlayer.getCity(pPyCity.getID())
		
		if TAIKOFlag == True:
			iNumKOU = pCity.getPopulation() / iNumCityCountKOU
			if iNumKOU > 2:
				iNumKOU = 2
			iNumOTU = 0
		
		elif TYUUSEIFlag == True:
			iNumKOU = pCity.getPopulation() / iNumCityCountKOU
			if iNumKOU < 1:
				iNumKOU = 1
			if iNumKOU > 3:
				iNumKOU = 3

			iNumOTU = pCity.getPopulation() / iNumCityCountOTU
			if iNumOTU > 1:
				iNumOTU = 1
		
		else:
			iNumKOU = pCity.getPopulation() / iNumCityCountKOU
			if iNumKOU < 1:
				iNumKOU = 1
			if iNumKOU > 3:
				iNumKOU = 3
			
			iNumOTU = pCity.getPopulation() / iNumCityCountOTU
			if iNumOTU < 1:
				iNumOTU = 1
			if iNumOTU > 3:
				iNumOTU = 3
		
		if iNumKOU >= 1:
			for i in range(iNumKOU):
				newUnit = pPlayer.initUnit(iUnitKOU, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iNumOTU >= 1:
			for i in range(iNumOTU):
				newUnit = pPlayer.initUnit(iUnitOTU, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	pPlayer.setNumWorldSpell(0)
	
	
	caster.setHasPromotion( gc.getInfoTypeForString('PROMOTION_SPELL_CASTED'),True )
	pPlot = caster.plot()
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	#輝針城の各都市で付喪神が大量発生しました！
	CyInterface().addImmediateMessage("&#36637;&#37341;&#22478;&#12398;&#21508;&#37117;&#24066;&#12391;&#20184;&#21930;&#31070;&#12364;&#22823;&#37327;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")

	return True




