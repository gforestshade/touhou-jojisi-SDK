## Sid Meier's Civilization 4'
## Copyright Firaxis Games 2005

##### <written by F> #####

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvGameUtils
import re

import SpellInfo
import SpellInterface

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaTohoUnit:
	"Civilopedia Screen for Toho Units"

	def __init__(self, main):
		self.iUnit = -1
		self.top = main
		self.CAL = 6

	# Screen construction function
	def interfaceScreen(self, iUnit):	
		self.iUnit = iUnit
		self.top.deleteAllWidgets()										
		screen = self.top.getScreen()
		
		self.H_ICON = 150
		self.W_MAIN_PANE = (self.top.W_ITEMS_PANE - self.top.W_BORDER * 2)/3
		self.H_MAIN_PANE = 210
		self.X_ICON = self.top.X_ITEMS_PANE + 30
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
		self.H_ALLOWS = 110
		self.W_ALLOWS = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.Y_ALLOWS = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_ALLOWS
		self.X_RIGHT = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_SPECIAL = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_SPECIAL = self.Y_ALLOWS - self.Y_SPECIAL - 10
		
		self.X_STATS_PANE = self.X_ICON + self.H_ICON
		self.Y_STATS_PANE = self.Y_ICON + self.H_ICON /4
		self.W_STATS_PANE = self.top.X_ITEMS_PANE + self.W_MAIN_PANE - self.X_STATS_PANE + self.top.X_ITEMS_PANE
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE
		
		self.X_TOHO_UNIT_PANE0 = self.X_ICON - 30
		self.Y_TOHO_UNIT_PANE0 = self.Y_ICON - 50
		self.W_TOHO_UNIT_PANE0 = 433
		self.H_TOHO_UNIT_PANE0 = 54
		
		self.X_TOHO_UNIT_MARK = self.X_ICON - 30
		self.Y_TOHO_UNIT_MARK = self.top.Y_ITEMS_PANE + (self.H_MAIN_PANE *2/3) + self.Y_ICON +5
		self.W_TOHO_UNIT_MARK = self.W_MAIN_PANE + 4
		self.H_TOHO_UNIT_MARK = 130
		
		self.X_TOHO_UNIT_SKILL = self.X_ICON - 30
		self.Y_TOHO_UNIT_SKILL = self.top.Y_ITEMS_PANE + (self.H_MAIN_PANE *5/3) + 30
		self.W_TOHO_UNIT_SKILL = self.W_MAIN_PANE + 4
		self.H_TOHO_UNIT_SKILL = 130
		
#		self.X_TOHO_UNIT_STACK_BONUS = 20
#		self.Y_TOHO_UNIT_STACK_BONUS = 465
#		self.W_TOHO_UNIT_STACK_BONUS = 210
#		self.H_TOHO_UNIT_STACK_BONUS = 130
#		
#		self.X_TOHO_UNIT_STG_SKILL = 243
#		self.Y_TOHO_UNIT_STG_SKILL = 465
#		self.W_TOHO_UNIT_STG_SKILL = 210
#		self.H_TOHO_UNIT_STG_SKILL = 130
		
		self.X_CAL = self.top.X_ITEMS_PANE + (self.W_MAIN_PANE *2) - self.top.W_BORDER
		self.Y_CAL = 280
		self.W_CAL = 303
		self.H_CAL = 50
		
		self.X_SPELL_CARD = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_SPELL_CARD = self.top.Y_ITEMS_PANE + (self.H_MAIN_PANE *2/3) + self.Y_ICON +5
		self.W_SPELL_CARD = self.W_MAIN_PANE + 4
		self.H_SPELL_CARD = self.Y_ALLOWS - (self.Y_SPECIAL *2/3)
		
		self.X_SPELL_EXTRA = self.X_RIGHT + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_SPELL_EXTRA = self.top.Y_ITEMS_PANE + (self.H_MAIN_PANE *2/3) + self.Y_ICON +5
		self.W_SPELL_EXTRA = self.W_MAIN_PANE
		self.H_SPELL_EXTRA = (self.Y_ALLOWS /2) - (self.Y_SPECIAL /3) - 10
		
		self.X_SPELL_PHANTASM = self.X_RIGHT + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_SPELL_PHANTASM = self.Y_SPECIAL + (self.Y_ALLOWS *2/5) - 10
		self.W_SPELL_PHANTASM = self.W_MAIN_PANE
		self.H_SPELL_PHANTASM = (self.Y_ALLOWS /2) - (self.Y_SPECIAL /3) - 10
		
		
		self.X_UNIT_PANE = 20
		self.Y_UNIT_PANE = 70
		self.W_UNIT_PANE = 433
		self.H_UNIT_PANE = 210
		
		self.X_UNIT_ANIMATION = self.top.X_ITEMS_PANE + (self.W_MAIN_PANE *2) - self.top.W_BORDER
		self.Y_UNIT_ANIMATION = self.top.Y_ITEMS_PANE + 8
		self.W_UNIT_ANIMATION = self.W_MAIN_PANE
		self.H_UNIT_ANIMATION = self.H_MAIN_PANE - 10
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0
		
#		self.X_ICON = 48
#		self.Y_ICON = 105
		self.W_ICON = 150
#		self.H_ICON = 150
		self.ICON_SIZE = 64

		self.BUTTON_SIZE = 64
		self.PROMOTION_ICON_SIZE = 32

#		self.X_STATS_PANE = 210
#		self.Y_STATS_PANE = 145
#		self.W_STATS_PANE = 250
#		self.H_STATS_PANE = 200

		self.X_SPECIAL_PANE = self.X_ICON - 30
		self.Y_SPECIAL_PANE = self.top.Y_ITEMS_PANE + (self.H_MAIN_PANE *5/2) - 10
		self.W_SPECIAL_PANE = self.W_MAIN_PANE + 4
		self.H_SPECIAL_PANE = self.Y_ALLOWS - (self.Y_SPECIAL *3/2) - 20

		self.X_PREREQ_PANE = 20
		self.Y_PREREQ_PANE = 292
		self.W_PREREQ_PANE = 433
		self.H_PREREQ_PANE = 124

		self.X_UPGRADES_TO_PANE = 475
		self.Y_UPGRADES_TO_PANE = 292
		self.W_UPGRADES_TO_PANE = 303
		self.H_UPGRADES_TO_PANE = 124

		self.X_PROMO_PANE = 20
		self.Y_PROMO_PANE = 574
		self.W_PROMO_PANE = 433
		self.H_PROMO_PANE = 124

		self.X_HISTORY_PANE = 475
		self.Y_HISTORY_PANE = 420
		self.W_HISTORY_PANE = 303
		self.H_HISTORY_PANE = 278
		
		#self.CAL = 1;
		
		self.MarkList = [
							['UNIT_SANAE1' , gc.getInfoTypeForString('PROMOTION_SANAE')],
							['UNIT_REMILIA1' , gc.getInfoTypeForString('PROMOTION_REMILIA')],
							['UNIT_CHEN1' , gc.getInfoTypeForString('PROMOTION_CHEN')],
							['UNIT_WRIGGLE1' , gc.getInfoTypeForString('PROMOTION_WRIGGLE')],
							['UNIT_TEWI1' , gc.getInfoTypeForString('PROMOTION_TEWI')],
							['UNIT_NITORI1' , gc.getInfoTypeForString('PROMOTION_NITORI')],
							['UNIT_MARISA1' , gc.getInfoTypeForString('PROMOTION_MARISA')],
							['UNIT_FLAN1' , gc.getInfoTypeForString('PROMOTION_FLAN')],
							['UNIT_YOUMU1' , gc.getInfoTypeForString('PROMOTION_YOUMU')],
							['UNIT_CIRNO1' , gc.getInfoTypeForString('PROMOTION_CIRNO')],
							['UNIT_EIRIN1' , gc.getInfoTypeForString('PROMOTION_EIRIN')],
							['UNIT_SUWAKO1' , gc.getInfoTypeForString('PROMOTION_SUWAKO')],
							['UNIT_ALICE1' , gc.getInfoTypeForString('PROMOTION_ALICE')],
							['UNIT_MOKOU1' , gc.getInfoTypeForString('PROMOTION_MOKOU')],
							['UNIT_KEINE1' , gc.getInfoTypeForString('PROMOTION_KEINE')],
							['UNIT_PARSEE1' , gc.getInfoTypeForString('PROMOTION_PARSEE')],
							['UNIT_YUGI1' , gc.getInfoTypeForString('PROMOTION_YUGI')],
							['UNIT_HAKUTAKUKEINE1' , gc.getInfoTypeForString('PROMOTION_KEINE')],
							['UNIT_SAKUYA1' , gc.getInfoTypeForString('PROMOTION_SAKUYA')],
							['UNIT_YUYUKO1' , gc.getInfoTypeForString('PROMOTION_YUYUKO')],
							['UNIT_RUMIA1' , gc.getInfoTypeForString('PROMOTION_RUMIA')],
							['UNIT_MEDICIN1' , gc.getInfoTypeForString('PROMOTION_MEDICIN')],
							['UNIT_KANAKO1' , gc.getInfoTypeForString('PROMOTION_KANAKO')],
							['UNIT_REIMU1' , gc.getInfoTypeForString('PROMOTION_REIMU')],
							['UNIT_YUKA1' , gc.getInfoTypeForString('PROMOTION_YUKA')],
							['UNIT_KOISHI1' , gc.getInfoTypeForString('PROMOTION_KOISHI')],
							['UNIT_KOISHI_FADE1' , gc.getInfoTypeForString('PROMOTION_KOISHI')],
							['UNIT_PATCHOULI1' , gc.getInfoTypeForString('PROMOTION_PATCHOULI')],
							['UNIT_RAN1' , gc.getInfoTypeForString('PROMOTION_RAN')],
							['UNIT_REISEN1' , gc.getInfoTypeForString('PROMOTION_REISEN')],
							['UNIT_IKU1' , gc.getInfoTypeForString('PROMOTION_IKU')],
							['UNIT_SATORI1' , gc.getInfoTypeForString('PROMOTION_SATORI')],
							['UNIT_MYSTIA1' , gc.getInfoTypeForString('PROMOTION_MYSTIA')],
							['UNIT_SUIKA1' , gc.getInfoTypeForString('PROMOTION_SUIKA')],
							['UNIT_SUIKA_BIG1' , gc.getInfoTypeForString('PROMOTION_SUIKA')],
							['UNIT_SUIKA_SMALL1' , gc.getInfoTypeForString('PROMOTION_SUIKA')],
							['UNIT_KOMACHI1' , gc.getInfoTypeForString('PROMOTION_KOMACHI')],
							['UNIT_MEDICINwithSU1' , gc.getInfoTypeForString('PROMOTION_MEDICIN')],
							['UNIT_MEIRIN1' , gc.getInfoTypeForString('PROMOTION_MEIRIN')],
							['UNIT_YUKARI1' , gc.getInfoTypeForString('PROMOTION_YUKARI')],
							['UNIT_KAGUYA1' , gc.getInfoTypeForString('PROMOTION_KAGUYA')],
							['UNIT_TENSHI1' , gc.getInfoTypeForString('PROMOTION_TENSHI')],
							['UNIT_RIN1' , gc.getInfoTypeForString('PROMOTION_RIN')],
							['UNIT_RIN_CATMODE1' , gc.getInfoTypeForString('PROMOTION_RIN')],
							['UNIT_LETTY1' , gc.getInfoTypeForString('PROMOTION_LETTY')],
							['UNIT_MIMA1' , gc.getInfoTypeForString('PROMOTION_MIMA')],
							['UNIT_EIKI1' , gc.getInfoTypeForString('PROMOTION_EIKI')],
							['UNIT_NAZRIN1' , gc.getInfoTypeForString('PROMOTION_NAZRIN')],
							['UNIT_KOGASA1' , gc.getInfoTypeForString('PROMOTION_KOGASA')],
							['UNIT_ICHIRIN1' , gc.getInfoTypeForString('PROMOTION_ICHIRIN')],
							['UNIT_MINAMITSU1' , gc.getInfoTypeForString('PROMOTION_MINAMITSU')],
							['UNIT_SYOU1' , gc.getInfoTypeForString('PROMOTION_SYOU')],
							['UNIT_BYAKUREN1' , gc.getInfoTypeForString('PROMOTION_BYAKUREN')],
							['UNIT_NUE1' , gc.getInfoTypeForString('PROMOTION_NUE')],
							['UNIT_YOSHIKA1' , gc.getInfoTypeForString('PROMOTION_YOSHIKA')],
							['UNIT_SEIGA1' , gc.getInfoTypeForString('PROMOTION_SEIGA')],
							['UNIT_TOJIKO1' , gc.getInfoTypeForString('PROMOTION_TOJIKO')],
							['UNIT_FUTO1' , gc.getInfoTypeForString('PROMOTION_FUTO')],
							['UNIT_MIMIMIKO1' , gc.getInfoTypeForString('PROMOTION_MIMIMIKO')],
							['UNIT_YATUHASHI1' , gc.getInfoTypeForString('PROMOTION_YATUHASHI')],
							['UNIT_BENBEN1' , gc.getInfoTypeForString('PROMOTION_BENBEN')],
							['UNIT_SEIJA1' , gc.getInfoTypeForString('PROMOTION_SEIJA')],
							['UNIT_SHINMYOUMARU1' , gc.getInfoTypeForString('PROMOTION_SHINMYOUMARU')],
							['UNIT_RAIKO1' , gc.getInfoTypeForString('PROMOTION_RAIKO')],
							['UNIT_YORIHIME1' , gc.getInfoTypeForString('PROMOTION_YORIHIME')],
							['UNIT_TOYOHIME1' , gc.getInfoTypeForString('PROMOTION_TOYOHIME')],
							['UNIT_SEIRAN1' , gc.getInfoTypeForString('PROMOTION_SEIRAN')],
							['UNIT_RINGO1' , gc.getInfoTypeForString('PROMOTION_RINGO')],
							['UNIT_DOREMY1' , gc.getInfoTypeForString('PROMOTION_DOREMY')],
							['UNIT_SAGUME1' , gc.getInfoTypeForString('PROMOTION_SAGUME')],
						]
						
		self.MarkDic = {}
		for i in range(len(self.MarkList)):
			self.MarkDic[gc.getInfoTypeForString(self.MarkList[i][0])] = self.MarkList[i][1]
			
		
		self.SkillList = [
							['UNIT_SANAE1' , gc.getInfoTypeForString('PROMOTION_SANAE_SKILL1')],
							['UNIT_REMILIA1' , gc.getInfoTypeForString('PROMOTION_REMILIA_SKILL1')],
							['UNIT_CHEN1' , gc.getInfoTypeForString('PROMOTION_CHEN_SKILL1')],
							['UNIT_WRIGGLE1' , gc.getInfoTypeForString('PROMOTION_WRIGGLE_SKILL1')],
							['UNIT_TEWI1' , gc.getInfoTypeForString('PROMOTION_TEWI_SKILL1')],
							['UNIT_NITORI1' , gc.getInfoTypeForString('PROMOTION_NITORI_SKILL1')],
							['UNIT_MARISA1' , gc.getInfoTypeForString('PROMOTION_MARISA_SKILL1')],
							['UNIT_FLAN1' , gc.getInfoTypeForString('PROMOTION_FLAN_SKILL1')],
							['UNIT_YOUMU1' , gc.getInfoTypeForString('PROMOTION_YOUMU_SKILL1')],
							['UNIT_CIRNO1' , gc.getInfoTypeForString('PROMOTION_CIRNO_SKILL1')],
							['UNIT_EIRIN1' , gc.getInfoTypeForString('PROMOTION_EIRIN_SKILL1')],
							['UNIT_SUWAKO1' , gc.getInfoTypeForString('PROMOTION_SUWAKO_SKILL1')],
							['UNIT_ALICE1' , gc.getInfoTypeForString('PROMOTION_ALICE_SKILL1')],
							['UNIT_MOKOU1' , gc.getInfoTypeForString('PROMOTION_MOKOU_SKILL1')],
							['UNIT_KEINE1' , gc.getInfoTypeForString('PROMOTION_KEINE_SKILL1')],
							['UNIT_PARSEE1' , gc.getInfoTypeForString('PROMOTION_PARSEE_SKILL1')],
							['UNIT_YUGI1' , gc.getInfoTypeForString('PROMOTION_YUGI_SKILL1')],
							['UNIT_HAKUTAKUKEINE1' , gc.getInfoTypeForString('PROMOTION_KEINE_SKILL1')],
							['UNIT_SAKUYA1' , gc.getInfoTypeForString('PROMOTION_SAKUYA_SKILL1')],
							['UNIT_YUYUKO1' , gc.getInfoTypeForString('PROMOTION_YUYUKO_SKILL1')],
							['UNIT_RUMIA1' , gc.getInfoTypeForString('PROMOTION_RUMIA_SKILL1')],
							['UNIT_MEDICIN1' , gc.getInfoTypeForString('PROMOTION_MEDICIN_SKILL1')],
							['UNIT_KANAKO1' , gc.getInfoTypeForString('PROMOTION_KANAKO_SKILL1')],
							['UNIT_REIMU1' , gc.getInfoTypeForString('PROMOTION_REIMU_SKILL1')],
							['UNIT_YUKA1' , gc.getInfoTypeForString('PROMOTION_YUKA_SKILL1')],
							['UNIT_KOISHI1' , gc.getInfoTypeForString('PROMOTION_KOISHI_SKILL1')],
							['UNIT_KOISHI_FADE1' , gc.getInfoTypeForString('PROMOTION_KOISHI_SKILL1')],
							['UNIT_PATCHOULI1' , gc.getInfoTypeForString('PROMOTION_PATCHOULI_SKILL1')],
							['UNIT_RAN1' , gc.getInfoTypeForString('PROMOTION_RAN_SKILL1')],
							['UNIT_REISEN1' , gc.getInfoTypeForString('PROMOTION_REISEN_SKILL1')],
							['UNIT_IKU1' , gc.getInfoTypeForString('PROMOTION_IKU_SKILL1')],
							['UNIT_SATORI1' , gc.getInfoTypeForString('PROMOTION_SATORI_SKILL1')],
							['UNIT_MYSTIA1' , gc.getInfoTypeForString('PROMOTION_MYSTIA_SKILL1')],
							['UNIT_SUIKA1' , gc.getInfoTypeForString('PROMOTION_SUIKA_SKILL1')],
							['UNIT_SUIKA_BIG1' , gc.getInfoTypeForString('PROMOTION_SUIKA_SKILL1')],
							['UNIT_SUIKA_SMALL1' , gc.getInfoTypeForString('PROMOTION_SUIKA_SKILL1')],
							['UNIT_KOMACHI1' , gc.getInfoTypeForString('PROMOTION_KOMACHI_SKILL1')],
							['UNIT_MEDICINwithSU1' , gc.getInfoTypeForString('PROMOTION_MEDICIN_SKILL1')],
							['UNIT_MEIRIN1' , gc.getInfoTypeForString('PROMOTION_MEIRIN_SKILL1')],
							['UNIT_YUKARI1' , gc.getInfoTypeForString('PROMOTION_YUKARI_SKILL1')],
							['UNIT_KAGUYA1' , gc.getInfoTypeForString('PROMOTION_KAGUYA_SKILL1')],
							['UNIT_TENSHI1' , gc.getInfoTypeForString('PROMOTION_TENSHI_SKILL1')],
							['UNIT_RIN1' , gc.getInfoTypeForString('PROMOTION_RIN_SKILL1')],
							['UNIT_RIN_CATMODE1' , gc.getInfoTypeForString('PROMOTION_RIN_SKILL1')],
							['UNIT_LETTY1' , gc.getInfoTypeForString('PROMOTION_LETTY_SKILL1')],
							['UNIT_MIMA1' , gc.getInfoTypeForString('PROMOTION_MIMA_SKILL1')],
							['UNIT_EIKI1' , gc.getInfoTypeForString('PROMOTION_EIKI_SKILL1')],
							['UNIT_NAZRIN1' , gc.getInfoTypeForString('PROMOTION_NAZRIN_SKILL1')],
							['UNIT_KOGASA1' , gc.getInfoTypeForString('PROMOTION_KOGASA_SKILL1')],
							['UNIT_ICHIRIN1' , gc.getInfoTypeForString('PROMOTION_ICHIRIN_SKILL1')],
							['UNIT_MINAMITSU1' , gc.getInfoTypeForString('PROMOTION_MINAMITSU_SKILL1')],
							['UNIT_SYOU1' , gc.getInfoTypeForString('PROMOTION_SYOU_SKILL1')],
							['UNIT_BYAKUREN1' , gc.getInfoTypeForString('PROMOTION_BYAKUREN_SKILL1')],
							['UNIT_NUE1' , gc.getInfoTypeForString('PROMOTION_NUE_SKILL1')],
							['UNIT_YOSHIKA1' , gc.getInfoTypeForString('PROMOTION_YOSHIKA_SKILL1')],
							['UNIT_SEIGA1' , gc.getInfoTypeForString('PROMOTION_SEIGA_SKILL1')],
							['UNIT_TOJIKO1' , gc.getInfoTypeForString('PROMOTION_TOJIKO_SKILL1')],
							['UNIT_FUTO1' , gc.getInfoTypeForString('PROMOTION_FUTO_SKILL1')],
							['UNIT_MIMIMIKO1' , gc.getInfoTypeForString('PROMOTION_MIMIMIKO_SKILL1')],
							['UNIT_YATUHASHI1' , gc.getInfoTypeForString('PROMOTION_YATUHASHI_SKILL1')],
							['UNIT_BENBEN1' , gc.getInfoTypeForString('PROMOTION_BENBEN_SKILL1')],
							['UNIT_SEIJA1' , gc.getInfoTypeForString('PROMOTION_SEIJA_SKILL1')],
							['UNIT_SHINMYOUMARU1' , gc.getInfoTypeForString('PROMOTION_SHINMYOUMARU_SKILL1')],
							['UNIT_RAIKO1' , gc.getInfoTypeForString('PROMOTION_RAIKO_SKILL1')],
							['UNIT_YORIHIME1' , gc.getInfoTypeForString('PROMOTION_YORIHIME_SKILL1')],
							['UNIT_TOYOHIME1' , gc.getInfoTypeForString('PROMOTION_TOYOHIME_SKILL1')],
							['UNIT_SEIRAN1' , gc.getInfoTypeForString('PROMOTION_SEIRAN_SKILL1')],
							['UNIT_RINGO1' , gc.getInfoTypeForString('PROMOTION_RINGO_SKILL1')],
							['UNIT_DOREMY1' , gc.getInfoTypeForString('PROMOTION_DOREMY_SKILL1')],
							['UNIT_SAGUME1' , gc.getInfoTypeForString('PROMOTION_SAGUME_SKILL1')],
						]
		
		self.SkillDic = {}
		for i in range(len(self.SkillList)):
			self.SkillDic[gc.getInfoTypeForString(self.SkillList[i][0])] = self.SkillList[i][1]
		
		
		self.SpellDic = {}
		for i in range(len(SpellInfo.TohoUnitSpellHelpList)):
			self.SpellDic[gc.getInfoTypeForString(SpellInfo.TohoUnitSpellHelpList[i][0])] = SpellInfo.TohoUnitSpellHelpList[i][1]

		# for 統合叙事詩 17.06
		# ゲーム開始前にペディア開く人用
		SpellInfo.init_helpfunclist()
		
		self.SortList = []
		tempNum = 0;
		#紅魔館
		self.SortList.append(['UNIT_REMILIA1' , tempNum,'<color=255,75,100,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_FLAN1' , tempNum,'<color=255,75,100,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SAKUYA1' , tempNum,'<color=255,75,100,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_PATCHOULI1' , tempNum,'<color=255,75,100,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MEIRIN1' , tempNum,'<color=255,75,100,255>']); tempNum = tempNum + 1
		#白玉楼
		self.SortList.append(['UNIT_YOUMU1' , tempNum,'<color=255,165,220,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_YUYUKO1' , tempNum,'<color=255,165,220,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_CHEN1' , tempNum,'<color=255,165,220,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_RAN1' , tempNum,'<color=255,165,220,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_YUKARI1' , tempNum,'<color=255,165,220,255>']); tempNum = tempNum + 1
		#永遠亭
		self.SortList.append(['UNIT_TEWI1' , tempNum,'<color=255,255,45,255>'],); tempNum = tempNum + 1
		self.SortList.append(['UNIT_REISEN1' , tempNum,'<color=255,255,45,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_EIRIN1' , tempNum,'<color=255,255,45,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_KAGUYA1' , tempNum,'<color=255,255,45,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MEDICIN1' , tempNum,'<color=255,255,45,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MEDICINwithSU1' , tempNum,'<color=255,255,45,255>']); tempNum = tempNum + 1
		#妖怪の山
		self.SortList.append(['UNIT_NITORI1' , tempNum,'<color=140,200,140,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_IKU1' , tempNum,'<color=140,200,140,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_TENSHI1' , tempNum,'<color=140,200,140,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SANAE1' , tempNum,'<color=140,200,140,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_KANAKO1' , tempNum,'<color=140,200,140,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SUWAKO1' , tempNum,'<color=140,200,140,255>']); tempNum = tempNum + 1
		#地霊殿
		self.SortList.append(['UNIT_PARSEE1' , tempNum,'<color=155,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_YUGI1' , tempNum,'<color=155,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_RIN1' , tempNum,'<color=155,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_RIN_CATMODE1' , tempNum,'<color=155,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SATORI1' , tempNum,'<color=155,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_KOISHI1' , tempNum,'<color=155,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_KOISHI_FADE1' , tempNum,'<color=155,255,255,255>']); tempNum = tempNum + 1
		#氷精連合
		self.SortList.append(['UNIT_CIRNO1' , tempNum,'<color=128,180,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_WRIGGLE1' , tempNum,'<color=128,180,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MYSTIA1' , tempNum,'<color=128,180,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_RUMIA1' , tempNum,'<color=128,180,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_LETTY1' , tempNum,'<color=128,180,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_KOGASA1' , tempNum,'<color=128,180,255,255>']); tempNum = tempNum + 1
		#博麗神社
		self.SortList.append(['UNIT_REIMU1' , tempNum,'<color=255,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MARISA1' , tempNum,'<color=255,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_ALICE1' , tempNum,'<color=255,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SUIKA1' , tempNum,'<color=255,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SUIKA_BIG1' , tempNum,'<color=255,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SUIKA_SMALL1' , tempNum,'<color=255,255,255,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MIMA1' , tempNum,'<color=255,255,255,255>']); tempNum = tempNum + 1
		#人間の里
		self.SortList.append(['UNIT_MOKOU1' , tempNum,'<color=230,165,75,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_KEINE1' , tempNum,'<color=230,165,75,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_HAKUTAKUKEINE1' , tempNum,'<color=230,165,75,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_YUKA1' , tempNum,'<color=230,165,75,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_KOMACHI1' , tempNum,'<color=230,165,75,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_EIKI1' , tempNum,'<color=230,165,75,255>']); tempNum = tempNum + 1
		#星蓮船
		self.SortList.append(['UNIT_NAZRIN1' , tempNum,'<color=252,89,0,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_ICHIRIN1' , tempNum,'<color=252,89,0,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MINAMITSU1' , tempNum,'<color=252,89,0,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SYOU1' , tempNum,'<color=252,89,0,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_BYAKUREN1' , tempNum,'<color=252,89,0,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_NUE1' , tempNum,'<color=252,89,0,255>']); tempNum = tempNum + 1
		#神霊廟
		self.SortList.append(['UNIT_YOSHIKA1' , tempNum,'<color=40,0,163,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SEIGA1' , tempNum,'<color=40,0,163,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_TOJIKO1' , tempNum,'<color=40,0,163,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_FUTO1' , tempNum,'<color=40,0,163,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_MIMIMIKO1' , tempNum,'<color=40,0,163,255>']); tempNum = tempNum + 1
		#輝針城
		self.SortList.append(['UNIT_YATUHASHI1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_BENBEN1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SEIJA1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SHINMYOUMARU1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_RAIKO1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		#月の都
		self.SortList.append(['UNIT_YORIHIME1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_TOYOHIME1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SEIRAN1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_RINGO1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_DOREMY1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		self.SortList.append(['UNIT_SAGUME1' , tempNum,'<color=114,0,124,255>']); tempNum = tempNum + 1
		
		
		self.SortDic = {}
		for i in range(len(self.SortList)):
			CvGameUtils.doprint(self.SortList[i][0])
			self.SortDic[gc.getUnitInfo(gc.getInfoTypeForString(self.SortList[i][0])).getDescription()] = self.SortList[i][1]
			
			#gc.getInfoTypeForString(self.SortList[i][0])

		self.iUnit = iUnit
	
		self.top.deleteAllWidgets()						
							
		screen = self.top.getScreen()
		
		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getUnitInfo(self.iUnit).getDescription().upper() + u"</font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TOHOUNIT, iUnit)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TOHOUNIT, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_TOHOUNIT or bNotActive:		
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_TOHOUNIT
		else:
			self.placeLinks(false)
		
		# Icon
		#screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
		#    self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		#screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
		#    self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		#szButton = gc.getUnitInfo(self.iUnit).getButton()
		#if self.top.iActivePlayer != -1:
		#	szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(self.iUnit)
		#screen.addDDSGFC(self.top.getNextWidgetName(), szButton,
		#    self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Unit animation
		screen.addUnitGraphicGFC(self.top.getNextWidgetName(), self.iUnit, self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_UNIT_ANIMATION, self.Z_ROTATION_UNIT_ANIMATION, self.SCALE_ANIMATION, True)


		#東方ユニットの基本ステータス表示
		self.placeTohoUnitSpec()
		
		#固有の昇進表示
		self.placeUniqueSkill()
		
		#CALボードの表示 あらかじめ枠はとっておく
		self.CALPanel = []
		for i in range(4):
			self.CALPanel.append( self.top.getNextWidgetName() )
		self.placeCAL()
		
		#スペル・スペカの表示
		self.SpellPanel = []
		for i in range(6):
			self.SpellPanel.append( self.top.getNextWidgetName() )
		self.placeSpell()

		#self.placeStats()

		#self.placeUpgradesTo()
		
		#self.placeRequires()
				
		self.placeSpecial()
		
		#self.placePromotions()
										
		#self.placeHistory()
		
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_UNIT and screen.isActive())

	# Place strength/movement
	def placeStats(self):

		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()

		# Unit combat group
		iCombatType = gc.getUnitInfo(self.iUnit).getUnitCombatType()
		if (iCombatType != -1):
			screen.setImageButton(self.top.getNextWidgetName(), gc.getUnitCombatInfo(iCombatType).getButton(), self.X_STATS_PANE, self.Y_STATS_PANE - 40, 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + gc.getUnitCombatInfo(iCombatType).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 37, self.Y_STATS_PANE - 35, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)

		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		
		if (gc.getUnitInfo(self.iUnit).getAirCombat() > 0 and gc.getUnitInfo(self.iUnit).getCombat() == 0):
			iStrength = gc.getUnitInfo(self.iUnit).getAirCombat()
		else:
			iStrength = gc.getUnitInfo(self.iUnit).getCombat()
			
		szName = self.top.getNextWidgetName()		
		szStrength = localText.getText("TXT_KEY_PEDIA_STRENGTH", ( iStrength, ) )
		screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szStrength.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
		szName = self.top.getNextWidgetName()
		szMovement = localText.getText("TXT_KEY_PEDIA_MOVEMENT", ( gc.getUnitInfo(self.iUnit).getMoves(), ) )
		screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szMovement.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getUnitInfo(self.iUnit).getProductionCost() >= 0 and not gc.getUnitInfo(self.iUnit).isFound()):
			szName = self.top.getNextWidgetName()
			if self.top.iActivePlayer == -1:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ((gc.getUnitInfo(self.iUnit).getProductionCost() * gc.getDefineINT("UNIT_PRODUCTION_PERCENT"))/100,))
			else:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ( gc.getActivePlayer().getUnitProductionNeeded(self.iUnit), ) )
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getUnitInfo(self.iUnit).getAirRange() > 0):
			szName = self.top.getNextWidgetName()
			szRange = localText.getText("TXT_KEY_PEDIA_RANGE", ( gc.getUnitInfo(self.iUnit).getAirRange(), ) )
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szRange.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
			
		screen.updateListBox(panelName)
	
	
	
	def getCAL(self,UnitStage):
		if UnitStage < 1:
			return 0
		elif UnitStage < 2:
			return 1
		elif UnitStage < 3:
			return 2
		elif UnitStage < 4:
			return 3
		elif UnitStage < 5:
			return 4
		elif UnitStage < 6:
			return 5
		else:
			return 6
	
	def changeCAL(self,iNum):
		self.CAL = self.CAL + iNum
		if self.CAL < 1:
			self.CAL = 1
		if self.CAL > 50:
			self.CAL = 50
		self.placeCAL()
		self.placeSpell()
	
	def placeTohoUnitSpec(self):
		screen = self.top.getScreen()
		
		iNumSukima = 36
		for k in range(7):
		
			# パネルの追加
			if k==0:
				screen.addPanel(self.top.getNextWidgetName(), localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_SPEC", ()), "", true, true, self.X_TOHO_UNIT_PANE0, self.Y_TOHO_UNIT_PANE0 + k*iNumSukima, self.W_TOHO_UNIT_PANE0, self.H_TOHO_UNIT_PANE0, PanelStyles.PANEL_STYLE_BLUE50 )
			else:
				screen.addPanel(self.top.getNextWidgetName(), " ", "", true, true, self.X_TOHO_UNIT_PANE0, self.Y_TOHO_UNIT_PANE0 + k*iNumSukima, self.W_TOHO_UNIT_PANE0, self.H_TOHO_UNIT_PANE0, PanelStyles.PANEL_STYLE_BLUE50 )
			#テク追加
			screen.setImageButton(self.top.getNextWidgetName(), gc.getTechInfo(gc.getUnitInfo(self.iUnit + k - 1).getPrereqAndTech() ).getButton(), self.X_TOHO_UNIT_PANE0 + 70, self.Y_TOHO_UNIT_PANE0 + 22 + k*iNumSukima , 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, gc.getUnitInfo(self.iUnit + k - 1).getPrereqAndTech(), -1)
			#文字追加
			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + localText.getText("TXT_KEY_PEDIA_PREREQ_TECH", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_PANE0 + 10, self.Y_TOHO_UNIT_PANE0 + 28 + k*iNumSukima, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + u"%c:" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + str(gc.getUnitInfo(self.iUnit + k - 1).getCombat()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_PANE0 + 120, self.Y_TOHO_UNIT_PANE0 + 24 + k*iNumSukima, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + u"%c:" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + str(gc.getUnitInfo(self.iUnit + k - 1).getMoves()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_PANE0 + 180, self.Y_TOHO_UNIT_PANE0 + 24 + k*iNumSukima, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + u"STG%c:" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + str(gc.getUnitInfo(self.iUnit + k - 1).getAirCombat()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_PANE0 + 240, self.Y_TOHO_UNIT_PANE0 + 24 + k*iNumSukima, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + u"CA Level: " + str(self.getCAL(k)) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_PANE0 + 330, self.Y_TOHO_UNIT_PANE0 + 28 + k*iNumSukima, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
			
		
		
	def placeUniqueSkill(self):
		
		screen = self.top.getScreen()
		
		#   u"<img=%s size=16>" %gc.getTechInfo(gc.getUnitInfo(self.iUnit + k - 1).getPrereqAndTech() ).getButton()
		
		
		#キャラクターマーク
		screen.addPanel(self.top.getNextWidgetName(), localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_MARK", ()), "", true, true, self.X_TOHO_UNIT_MARK, self.Y_TOHO_UNIT_MARK, self.W_TOHO_UNIT_MARK, self.H_TOHO_UNIT_MARK, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setImageButton(self.top.getNextWidgetName(), gc.getPromotionInfo(self.MarkDic[self.iUnit]).getButton(), self.X_TOHO_UNIT_MARK + 5, self.Y_TOHO_UNIT_MARK + 30 , 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, self.MarkDic[self.iUnit], -1)
		screen.setText(self.top.getNextWidgetName(), "", u"<font=3><color=140,255,40,255>" + "%s" %gc.getPromotionInfo(self.MarkDic[self.iUnit]).getDescription() + u"</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_MARK + 60, self.Y_TOHO_UNIT_MARK + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
		screen.addMultilineText(self.top.getNextWidgetName(), CyGameTextMgr().getPromotionHelp( self.MarkDic[self.iUnit], True )[1:] , self.X_TOHO_UNIT_MARK+55, self.Y_TOHO_UNIT_MARK+50, self.W_TOHO_UNIT_MARK-60, self.H_TOHO_UNIT_MARK-60, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
		#スキル
		screen.addPanel(self.top.getNextWidgetName(), localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_SKILL", ()), "", true, true, self.X_TOHO_UNIT_SKILL, self.Y_TOHO_UNIT_SKILL, self.W_TOHO_UNIT_SKILL, self.H_TOHO_UNIT_SKILL, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setImageButton(self.top.getNextWidgetName(), gc.getPromotionInfo(self.SkillDic[self.iUnit]).getButton(), self.X_TOHO_UNIT_SKILL + 5, self.Y_TOHO_UNIT_SKILL + 30 , 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, self.SkillDic[self.iUnit], -1)
		screen.setText(self.top.getNextWidgetName(), "", u"<font=3><color=140,255,40,255>" + "%s" %gc.getPromotionInfo(self.SkillDic[self.iUnit]).getDescription() + u"</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_SKILL + 60, self.Y_TOHO_UNIT_SKILL + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
		screen.addMultilineText(self.top.getNextWidgetName(), CyGameTextMgr().getPromotionHelp( self.SkillDic[self.iUnit], True )[1:] , self.X_TOHO_UNIT_SKILL+55, self.Y_TOHO_UNIT_SKILL+50, self.W_TOHO_UNIT_SKILL-60, self.H_TOHO_UNIT_SKILL-60, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		#スタックボーナス
		#screen.addPanel(self.top.getNextWidgetName(), localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_STACK_BONUS", ()), "", true, true, self.X_TOHO_UNIT_STACK_BONUS, self.Y_TOHO_UNIT_STACK_BONUS, self.W_TOHO_UNIT_STACK_BONUS, self.H_TOHO_UNIT_STACK_BONUS, PanelStyles.PANEL_STYLE_BLUE50 )
		#screen.setImageButton(self.top.getNextWidgetName(), gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS')).getButton(), self.X_TOHO_UNIT_STACK_BONUS + 5, self.Y_TOHO_UNIT_STACK_BONUS + 30 , 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS'), -1)
		#screen.setText(self.top.getNextWidgetName(), "", u"<font=3><color=140,255,40,255>" + "%s" %gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS')).getDescription() + u"</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_STACK_BONUS + 60, self.Y_TOHO_UNIT_STACK_BONUS + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
		#screen.addMultilineText(self.top.getNextWidgetName(), CyGameTextMgr().getPromotionHelp( gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS'), True )[1:] , self.X_TOHO_UNIT_STACK_BONUS+55, self.Y_TOHO_UNIT_STACK_BONUS+50, self.W_TOHO_UNIT_STACK_BONUS-60, self.H_TOHO_UNIT_STACK_BONUS-60, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
		#STGスキル
		#screen.addPanel(self.top.getNextWidgetName(), localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_STG_SKILL", ()), "", true, true, self.X_TOHO_UNIT_STG_SKILL, self.Y_TOHO_UNIT_STG_SKILL, self.W_TOHO_UNIT_STG_SKILL, self.H_TOHO_UNIT_STG_SKILL, PanelStyles.PANEL_STYLE_BLUE50 )
		#screen.setImageButton(self.top.getNextWidgetName(), gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL')).getButton(), self.X_TOHO_UNIT_STG_SKILL + 5, self.Y_TOHO_UNIT_STG_SKILL + 30 , 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL'), -1)
		#screen.setText(self.top.getNextWidgetName(), "", u"<font=3><color=140,255,40,255>" + "%s" %gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL')).getDescription() + u"</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_STG_SKILL + 60, self.Y_TOHO_UNIT_STG_SKILL + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
		#screen.addMultilineText(self.top.getNextWidgetName(), CyGameTextMgr().getPromotionHelp( gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL'), True )[1:] , self.X_TOHO_UNIT_STG_SKILL+55, self.Y_TOHO_UNIT_STG_SKILL+50, self.W_TOHO_UNIT_STG_SKILL-60, self.H_TOHO_UNIT_STG_SKILL-60, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		
		#ごみ置き場
		#screen.setImageButton(self.top.getNextWidgetName(), gc.getPromotionInfo(self.MarkDic[self.iUnit]).getButton(), self.X_TOHO_UNIT_MARK + 178, self.Y_TOHO_UNIT_MARK , 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, self.MarkDic[self.iUnit], -1)
		#screen.attachImageButton( panelName, "", gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_COMBAT1')).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString('PROMOTION_COMBAT1'), 1, False )
		#szText = u"<img=%s size=16>" %gc.getPromotionInfo(self.MarkDic[self.iUnit]).getButton() + " %s" %gc.getPromotionInfo(self.MarkDic[self.iUnit]).getDescription() 
		# str(gc.getTextToSpellInt('111',20))

	
	#CALボードの表示
	def placeCAL(self):
		screen = self.top.getScreen()
		
		screen.addPanel(self.CALPanel[0], "", "", true, true, self.X_CAL, self.Y_CAL, self.W_CAL, self.H_CAL, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setText(self.CALPanel[1], "", u"Card Attack Level (CAL) : " + str(self.CAL), CvUtil.FONT_LEFT_JUSTIFY, self.X_CAL + 20, self.Y_CAL + 17, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
		screen.setText(self.CALPanel[2], "", u"<color=255,50,50,255>[CAL+1]</color>", CvUtil.FONT_LEFT_JUSTIFY, self.X_CAL + 230, self.Y_CAL + 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_CAL_UP, -1, 0)
		screen.setText(self.CALPanel[3], "", u"<color=50,50,255,255>[CAL-1]</color>", CvUtil.FONT_LEFT_JUSTIFY, self.X_CAL + 230, self.Y_CAL + 27, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_CAL_DOWN, -1, 0)
		
	
	#スペル・スペカ
	def placeSpell(self):
		screen = self.top.getScreen()
		
		#スペカ
		screen.addPanel(self.SpellPanel[0], localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_SPELL_CARD", ()), "", true, true, self.X_SPELL_CARD, self.Y_SPELL_CARD, self.W_SPELL_CARD, self.H_SPELL_CARD, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		for Spell in self.SpellDic[self.iUnit][0]:
			if Spell[0] <= self.CAL and self.CAL <= Spell[1]:
				szText = szText + "\n\n<color=254,140,50,254>" + localText.getText(Spell[3], ()) + "</color>\n"
				helpKey = Spell[4]
				szHelpText = self.TextToInt(localText.getText(helpKey, ()), Spell[2])
				szText = szText + szHelpText

		szText = szText[2:]
		screen.addMultilineText(self.SpellPanel[1], szText , self.X_SPELL_CARD+5, self.Y_SPELL_CARD+30, self.W_SPELL_CARD-10, self.H_SPELL_CARD-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		#Exスペル
		screen.addPanel(self.SpellPanel[2], localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_SPELL_EXTRA", ()), "", true, true, self.X_SPELL_EXTRA, self.Y_SPELL_EXTRA, self.W_SPELL_EXTRA, self.H_SPELL_EXTRA, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		for Spell in self.SpellDic[self.iUnit][1]:
			if Spell[0] <= self.CAL and self.CAL <= Spell[1]:
				szText = szText + "\n\n<color=255,140,50,255>" + localText.getText(Spell[3], ()) + "</color>\n"
				helpKey = Spell[4]
				szHelpText = self.TextToInt(localText.getText(helpKey, ()), Spell[2])
				szText = szText + szHelpText

		szText = szText[2:]
		screen.addMultilineText(self.SpellPanel[3], szText , self.X_SPELL_EXTRA+5, self.Y_SPELL_EXTRA+30, self.W_SPELL_EXTRA-10, self.H_SPELL_EXTRA-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		#Phanスペル
		screen.addPanel(self.SpellPanel[4], localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_SPELL_PHANTASM", ()), "", true, true, self.X_SPELL_PHANTASM, self.Y_SPELL_PHANTASM, self.W_SPELL_PHANTASM, self.H_SPELL_PHANTASM, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		for Spell in self.SpellDic[self.iUnit][2]:
			if Spell[0] <= self.CAL and self.CAL <= Spell[1]:
				szText = szText + "\n\n<color=255,140,50,255>" + localText.getText(Spell[3], ()) + "</color>\n"
				helpKey = Spell[4]
				szHelpText = self.TextToInt(localText.getText(helpKey, ()), Spell[2])
				szText = szText + szHelpText

		szText = szText[2:]
		screen.addMultilineText(self.SpellPanel[5], szText , self.X_SPELL_PHANTASM+5, self.Y_SPELL_PHANTASM+30, self.W_SPELL_PHANTASM-10, self.H_SPELL_PHANTASM-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		
		    
	#[***]の置換
	def TextToInt(self,szText,spellName):

		# 置換関数
		def ctoi(m):
			s = m.group(0)
			
			if s[1] == "p":
				# ペディア経由だと実物のユニットがいなくてスペル探せないので名前から専用リストと照合
				foundItem = filter(lambda s: s[0]==spellName, SpellInfo.SpellToHelpfuncList)
				if foundItem:
					helpfunc = foundItem[0][1]
					i = helpfunc(s[2:-1], None, self.CAL)
					return "[%d]" % i
			else:
				# 直接ぶん投げ用関数に回す。もはやC++を呼び出さない 
				i = SpellInterface.getTextToSpellInt([ s[1:-1].encode("utf-8"), None, self.CAL, -1])
				return "[%d]" % i

		#本体
		match = re.compile(r"\[[a-zA-Z0-9]{3,10}\]")
		szText = match.sub(ctoi, szText)
		return szText
	
	
	# Place prereqs (techs, resources)
	def placeRequires(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")

		# add tech buttons
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTech()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )
				
		for j in range(gc.getDefineINT("NUM_UNIT_AND_TECH_PREREQS")):
			iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTechs(j)
			if (iPrereq >= 0):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, -1, False )

		# add resource buttons
		bFirst = True
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndBonus()
		if (iPrereq >= 0):
			bFirst = False
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		# count the number of OR resources
		nOr = 0
		for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			if (gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j) > -1):
				nOr += 1

		szLeftDelimeter = ""
		szRightDelimeter = ""
		#  Display a bracket if we have more than one OR resource and an AND resource
		if (not bFirst):
			if (nOr > 1):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ()) + "( "
				szRightDelimeter = " ) "
			elif (nOr > 0):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ())

		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panelName, "", szLeftDelimeter)

		bFirst = True
		for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			eBonus = gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j)
			if (eBonus > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getBonusInfo(eBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False )					

		if len(szRightDelimeter) > 0:
			screen.attachLabel(panelName, "", szRightDelimeter)

		# add religion buttons
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqReligion()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, -1, False )
		
		# add building buttons
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqBuilding()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPrereq, -1, False )		
		
	# Place upgrades
	def placeUpgradesTo(self):

		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_UPGRADES_TO", ()), "", false, true, self.X_UPGRADES_TO_PANE, self.Y_UPGRADES_TO_PANE, self.W_UPGRADES_TO_PANE, self.H_UPGRADES_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		
		screen.attachLabel(panelName, "", "  ")

		for k in range(gc.getNumUnitClassInfos()):
			if self.top.iActivePlayer == -1:
				eLoopUnit = gc.getUnitClassInfo(k).getDefaultUnitIndex()
			else:
				eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(k)
				
			if (eLoopUnit >= 0 and gc.getUnitInfo(self.iUnit).getUpgradeUnitClass(k)):
				szButton = gc.getUnitInfo(eLoopUnit).getButton()
				if self.top.iActivePlayer != -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(eLoopUnit)
				screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TOHOUNIT, eLoopUnit, 1, False )

	# Place Special abilities
	def placeSpecial(self):

		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false,
                                 self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getUnitHelp( self.iUnit+5, True, False, False, None )[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
					
	def placeHistory(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True,
						self.X_HISTORY_PANE, self.Y_HISTORY_PANE,
						self.W_HISTORY_PANE, self.H_HISTORY_PANE,
						PanelStyles.PANEL_STYLE_BLUE50 )
		
		textName = self.top.getNextWidgetName()
		szText = u"" 
		if len(gc.getUnitInfo(self.iUnit).getStrategy()) > 0:
			szText += localText.getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += gc.getUnitInfo(self.iUnit).getStrategy()
			szText += u"\n\n"
		szText += localText.getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		szText += gc.getUnitInfo(self.iUnit).getCivilopedia()
		screen.addMultilineText( textName, szText, self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40,
		    self.W_HISTORY_PANE - (15 * 2), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self, bRedraw):

		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortTohoUnits(0)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sUnitIcon, ()), self.iUnit, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TOHOUNIT, -1)

	def placePromotions(self):
#		screen = self.top.getScreen()
#		
#		# add pane and text
#		panelName = self.top.getNextWidgetName()
#		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", true, true, self.X_PROMO_PANE, self.Y_PROMO_PANE, self.W_PROMO_PANE, self.H_PROMO_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
#				
#		# add promotion buttons
#		rowListName = self.top.getNextWidgetName()
#		screen.addMultiListControlGFC(rowListName, "", self.X_PROMO_PANE+15, self.Y_PROMO_PANE+40, self.W_PROMO_PANE-20, self.H_PROMO_PANE-40, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
#	
#		for k in range(gc.getNumPromotionInfos()):
#			if (isPromotionValid(k, self.iUnit, false) and not gc.getPromotionInfo(k).isGraphicalOnly()):
#				screen.appendMultiListButton( rowListName, gc.getPromotionInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, k, -1, false )

		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", true, true, self.top.X_ITEMS_PANE, self.Y_PROMO_PANE, self.W_MAIN_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.top.X_ITEMS_PANE + 15, self.Y_PROMO_PANE + 40, self.W_MAIN_PANE - 20, self.H_SPECIAL_PANE - 40, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
		for k in xrange(gc.getNumPromotionInfos()):
			if isPromotionValid(k, self.iUnit, True) and not gc.getPromotionInfo(k).isGraphicalOnly():
				screen.appendMultiListButton(rowListName, gc.getPromotionInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, k, -1, false )


	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


##### </written by F> #####
