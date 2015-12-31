## Sid Meier's Civilization 4'
## Copyright Firaxis Games 2005

##### <written by F> #####

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvGameUtils
import re

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
		
		self.X_TOHO_UNIT_PANE0 = 20
		self.Y_TOHO_UNIT_PANE0 = 55
		self.W_TOHO_UNIT_PANE0 = 433
		self.H_TOHO_UNIT_PANE0 = 54
		
		self.X_TOHO_UNIT_MARK = 20
		self.Y_TOHO_UNIT_MARK = 330
		self.W_TOHO_UNIT_MARK = 210
		self.H_TOHO_UNIT_MARK = 130
		
		self.X_TOHO_UNIT_SKILL = 243
		self.Y_TOHO_UNIT_SKILL = 330
		self.W_TOHO_UNIT_SKILL = 210
		self.H_TOHO_UNIT_SKILL = 130
		
		self.X_TOHO_UNIT_STACK_BONUS = 20
		self.Y_TOHO_UNIT_STACK_BONUS = 465
		self.W_TOHO_UNIT_STACK_BONUS = 210
		self.H_TOHO_UNIT_STACK_BONUS = 130
		
		self.X_TOHO_UNIT_STG_SKILL = 243
		self.Y_TOHO_UNIT_STG_SKILL = 465
		self.W_TOHO_UNIT_STG_SKILL = 210
		self.H_TOHO_UNIT_STG_SKILL = 130
		
		self.X_CAL = 475
		self.Y_CAL = 275
		self.W_CAL = 303
		self.H_CAL = 50
		
		self.X_SPELL_CARD = 475
		self.Y_SPELL_CARD = 330
		self.W_SPELL_CARD = 303
		self.H_SPELL_CARD = 124
		
		self.X_SPELL_EXTRA = 475
		self.Y_SPELL_EXTRA = 459
		self.W_SPELL_EXTRA = 303
		self.H_SPELL_EXTRA = 124
		
		self.X_SPELL_PHANTASM = 475
		self.Y_SPELL_PHANTASM = 588
		self.W_SPELL_PHANTASM = 303
		self.H_SPELL_PHANTASM = 124
		
		
		self.X_UNIT_PANE = 20
		self.Y_UNIT_PANE = 70
		self.W_UNIT_PANE = 433
		self.H_UNIT_PANE = 210

		self.X_UNIT_ANIMATION = 475
		self.Y_UNIT_ANIMATION = 78
		self.W_UNIT_ANIMATION = 303
		self.H_UNIT_ANIMATION = 200
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0

		self.X_ICON = 48
		self.Y_ICON = 105
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 64

		self.BUTTON_SIZE = 64
		self.PROMOTION_ICON_SIZE = 32

		self.X_STATS_PANE = 210
		self.Y_STATS_PANE = 145
		self.W_STATS_PANE = 250
		self.H_STATS_PANE = 200

		self.X_SPECIAL_PANE = 20
		self.Y_SPECIAL_PANE = 600
		self.W_SPECIAL_PANE = 433
		self.H_SPECIAL_PANE = 114

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
		
		
		
						
	# Screen construction function
	def interfaceScreen(self, iUnit):	
		
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
						]
		
		self.SkillDic = {}
		for i in range(len(self.SkillList)):
			self.SkillDic[gc.getInfoTypeForString(self.SkillList[i][0])] = self.SkillList[i][1]
		
		
		
		self.SpellList = [
							 [ 'UNIT_SANAE1' , [    [   [1,3,'SANAE1_1','SANAE1_1'],[4,7,'SANAE1_1','SANAE1_2'],[8,11,'SANAE1_2','SANAE1_3',],[12,15,'SANAE1_2','SANAE1_4',], [16,19,'SANAE1_2','SANAE1_5',],[20,23,'SANAE1_2','SANAE1_6',],[24,255,'SANAE1_2','SANAE1_7',],], ['TXT_KEY_SPELL_SANAE_EXTRA1',],  ['TXT_KEY_SPELL_SANAE_PHANTASM1',],   ],   ],
							 [ 'UNIT_REMILIA1' , [    [   [1,7,'REMILIA1_1','REMILIA1_1'],[8,255,'REMILIA1_2','REMILIA1_1'], ], ['TXT_KEY_SPELL_REMILIA_EXTRA1',],  ['TXT_KEY_SPELL_REMILIA_PHANTASM1',],   ],   ],
							 [ 'UNIT_CHEN1' , [    [   [1,3,'CHEN1_1','CHEN1_1'],[4,7,'CHEN1_1','CHEN1_2'],[8,11,'CHEN1_1','CHEN1_3'],[12,15,'CHEN1_1','CHEN1_4',],[16,19,'CHEN1_1','CHEN1_5'],[20,255,'CHEN1_1','CHEN1_6'], ], ['TXT_KEY_SPELL_CHEN_EXTRA1',],  ['TXT_KEY_SPELL_CHEN_PHANTASM1',],   ],   ],
							 [ 'UNIT_WRIGGLE1' , [    [   [1,7,'WRIGGLE1_1','WRIGGLE1_1'],[8,255,'WRIGGLE1_2','WRIGGLE1_1'], ], ['TXT_KEY_SPELL_WRIGGLE_EXTRA1',],  ['TXT_KEY_SPELL_WRIGGLE_PHANTASM1',],   ],   ],
							 [ 'UNIT_TEWI1' , [    [   [1,3,'TEWI1_1','TEWI1_1'],[4,7,'TEWI1_1','TEWI1_2'],[8,11,'TEWI1_1','TEWI1_3'],[12,255,'TEWI1_2','TEWI1_4',  ], ], ['TXT_KEY_SPELL_TEWI_EXTRA1',],  ['TXT_KEY_SPELL_TEWI_PHANTASM1',],   ],   ],
							 [ 'UNIT_NITORI1' , [    [   [1,3,'NITORI1_1','NITORI1_1'],[4,7,'NITORI1_1','NITORI1_2'],[8,11,'NITORI1_1','NITORI1_3'],[12,255,'NITORI1_1','NITORI1_4',  ], ], ['TXT_KEY_SPELL_NITORI_EXTRA1',],  ['TXT_KEY_SPELL_NITORI_PHANTASM1',],   ],   ],
							 [ 'UNIT_MARISA1' , [    [   [1,7,'MARISA1_1','MARISA1_1'],[8,255,'MARISA1_1','MARISA1_2'], ], ['TXT_KEY_SPELL_MARISA_EXTRA1',],  ['TXT_KEY_SPELL_MARISA_PHANTASM1',],   ],   ],
							 [ 'UNIT_FLAN1' , [    [   [1,3,'FLAN1_1','FLAN1_1'],[4,7,'FLAN1_1','FLAN1_2'],[8,11,'FLAN1_1','FLAN1_3'],[12,15,'FLAN1_1','FLAN1_4',],[16,19,'FLAN1_1','FLAN1_5',],[20,23,'FLAN1_1','FLAN1_6',],[24,255,'FLAN1_1','FLAN1_7',], ], ['TXT_KEY_SPELL_FLAN_EXTRA1',],  ['TXT_KEY_SPELL_FLAN_PHANTASM1',],   ],   ],
							 [ 'UNIT_YOUMU1' , [    [   [1,7,'YOUMU1_1','YOUMU1_1'],[8,11,'YOUMU1_2','YOUMU1_1'],[12,255,'YOUMU1_2','YOUMU1_2'], ], ['TXT_KEY_SPELL_YOUMU_EXTRA1',],  ['TXT_KEY_SPELL_YOUMU_PHANTASM1',],   ],   ],
							 [ 'UNIT_CIRNO1' , [    [   [1,3,'CIRNO1_1','CIRNO1_1'],[4,255,'CIRNO1_2','CIRNO1_2'], ], ['TXT_KEY_SPELL_CIRNO_EXTRA1',],  ['TXT_KEY_SPELL_CIRNO_PHANTASM1',],   ],   ],
							 [ 'UNIT_EIRIN1' , [    [   [1,3,'EIRIN1_1','EIRIN1_1'],[4,7,'EIRIN1_1','EIRIN1_2'],[8,11,'EIRIN1_1','EIRIN1_3'],[12,255,'EIRIN1_1','EIRIN1_4',  ], ], ['TXT_KEY_SPELL_EIRIN_EXTRA1',],  ['TXT_KEY_SPELL_EIRIN_PHANTASM1',],   ],   ],
							 [ 'UNIT_SUWAKO1' , [    [   [1,255,'SUWAKO1_1','SUWAKO1_1'], ], ['TXT_KEY_SPELL_SUWAKO_EXTRA1',],  ['TXT_KEY_SPELL_SUWAKO_PHANTASM1',],   ],   ],
							 [ 'UNIT_ALICE1' , [    [   [1,3,'ALICE1_1','ALICE1_1'],[4,7,'ALICE1_1','ALICE1_2'],[8,11,'ALICE1_1','ALICE1_3'],[12,15,'ALICE1_1','ALICE1_4',],[16,19,'ALICE1_1','ALICE1_5',],[20,255,'ALICE1_1','ALICE1_6',], ], ['TXT_KEY_SPELL_ALICE_EXTRA1',],  ['TXT_KEY_SPELL_ALICE_PHANTASM1',],   ],   ],
							 [ 'UNIT_MOKOU1' , [    [   [1,255,'MOKOU1_1','MOKOU1_1'], ], ['TXT_KEY_SPELL_MOKOU_EXTRA1',],  ['TXT_KEY_SPELL_MOKOU_PHANTASM1',],   ],   ],
							 [ 'UNIT_KEINE1' , [    [   [1,3,'KEINE1_1','KEINE1_1'],[4,7,'KEINE1_1','KEINE1_2'],[8,11,'KEINE1_2','KEINE1_3'],[12,15,'KEINE1_2','KEINE1_4',],[16,19,'KEINE1_2','KEINE1_5',],[20,255,'KEINE1_2','KEINE1_6',], ], ['TXT_KEY_SPELL_KEINE_EXTRA1',],  ['TXT_KEY_SPELL_KEINE_PHANTASM1',],   ],   ],
							 [ 'UNIT_PARSEE1' , [    [   [1,7,'PARSEE1_1','PARSEE1_1'],[8,255,'PARSEE1_2','PARSEE1_1'], ], ['TXT_KEY_SPELL_PARSEE_EXTRA1',],  ['TXT_KEY_SPELL_PARSEE_PHANTASM1',],   ],   ],
							 [ 'UNIT_YUGI1' , [    [   [1,255,'YUGI1_1','YUGI1_1'], ], ['TXT_KEY_SPELL_YUGI_EXTRA1',],  ['TXT_KEY_SPELL_YUGI_PHANTASM1',],   ],   ],
							 [ 'UNIT_HAKUTAKUKEINE1' , [    [   [1,255,'HAKUTAKUKEINE1_1','HAKUTAKUKEINE1_1'], ], ['TXT_KEY_SPELL_HAKUTAKUKEINE_EXTRA1',],  ['TXT_KEY_SPELL_HAKUTAKUKEINE_PHANTASM1',],   ],   ],
							 [ 'UNIT_SAKUYA1' , [    [   [1,3,'SAKUYA1_1','SAKUYA1_1'],[4,7,'SAKUYA1_1','SAKUYA1_2'],[8,11,'SAKUYA1_1','SAKUYA1_3'],[12,255,'SAKUYA1_1','SAKUYA1_4',  ], ], ['TXT_KEY_SPELL_SAKUYA_EXTRA1',],  ['TXT_KEY_SPELL_SAKUYA_PHANTASM1',],   ],   ],
							 [ 'UNIT_YUYUKO1' , [    [   [1,3,'YUYUKO1_1','YUYUKO1_1'],[4,7,'YUYUKO1_2','YUYUKO1_1'],[8,11,'YUYUKO1_3','YUYUKO1_1'],[12,255,'YUYUKO1_4','YUYUKO1_1'], ], ['TXT_KEY_SPELL_YUYUKO_EXTRA1',],  ['TXT_KEY_SPELL_YUYUKO_PHANTASM1',],   ],   ],
							 [ 'UNIT_RUMIA1' , [    [   [1,255,'RUMIA1_1','RUMIA1_1'], ], ['TXT_KEY_SPELL_RUMIA_EXTRA1',],  ['TXT_KEY_SPELL_RUMIA_PHANTASM1',],   ],   ],
							 [ 'UNIT_MEDICIN1' , [    [   [1,3,'MEDICIN1_1','MEDICIN1_1'],[4,7,'MEDICIN1_1','MEDICIN1_2'],[8,11,'MEDICIN1_2','MEDICIN1_3'],[12,255,'MEDICIN1_2','MEDICIN1_4',  ], ], ['TXT_KEY_SPELL_MEDICIN_EXTRA1',],  ['TXT_KEY_SPELL_MEDICIN_PHANTASM1',],   ],   ],
							 [ 'UNIT_KANAKO1' , [    [   [1,7,'KANAKO1_1','KANAKO1_1'],[8,255,'KANAKO1_2','KANAKO1_1'], ], ['TXT_KEY_SPELL_KANAKO_EXTRA1',],  ['TXT_KEY_SPELL_KANAKO_PHANTASM1',],   ],   ],
							 [ 'UNIT_REIMU1' , [    [   [1,255,'REIMU1_1','REIMU1_1'], ], ['TXT_KEY_SPELL_REIMU_EXTRA1',],  ['TXT_KEY_SPELL_REIMU_PHANTASM1',],   ],   ],
							 [ 'UNIT_YUKA1' , [    [   [1,255,'YUKA1_1','YUKA1_1'], ], ['TXT_KEY_SPELL_YUKA_EXTRA1',],  ['TXT_KEY_SPELL_YUKA_PHANTASM1',],   ],   ],
							 [ 'UNIT_KOISHI1' , [    [   [1,255,'KOISHI1_1','KOISHI1_1'], ], ['TXT_KEY_SPELL_KOISHI_EXTRA1','TXT_KEY_SPELL_KOISHI_SKILL1',],  ['TXT_KEY_SPELL_KOISHI_PHANTASM1',],   ],   ],
							 [ 'UNIT_KOISHI_FADE1' , [    [    ], ['TXT_KEY_SPELL_KOISHI_EXTRA1','TXT_KEY_SPELL_KOISHI_SKILL2',],  ['TXT_KEY_SPELL_KOISHI_PHANTASM1',],   ],   ],
							 [ 'UNIT_PATCHOULI1' , [    [   [1,255,'PATCHOULI1_1','PATCHOULI1_1'],[1,255,'PATCHOULI2_1','PATCHOULI2_1'], ], ['TXT_KEY_SPELL_PATCHOULI_EXTRA1','TXT_KEY_SPELL_PATCHOULI_EXTRA2',],  ['TXT_KEY_SPELL_PATCHOULI_PHANTASM1','TXT_KEY_SPELL_PATCHOULI_PHANTASM2','TXT_KEY_SPELL_PATCHOULI_PHANTASM3',],   ],   ],
							 [ 'UNIT_RAN1' , [    [   [1,3,'RAN1_1','RAN1_1'],[4,7,'RAN1_1','RAN1_2'],[8,11,'RAN1_1','RAN1_3'],[12,255,'RAN1_1','RAN1_4',  ], ], ['TXT_KEY_SPELL_RAN_EXTRA1',],  ['TXT_KEY_SPELL_RAN_PHANTASM1',],   ],   ],
							 [ 'UNIT_REISEN1' , [    [   [1,7,'REISEN1_1','REISEN1_1'],[8,255,'REISEN1_2','REISEN1_1'], ], ['TXT_KEY_SPELL_REISEN_EXTRA1',],  ['TXT_KEY_SPELL_REISEN_PHANTASM1',],   ],   ],
							 [ 'UNIT_IKU1' , [    [   [1,3,'IKU1_1','IKU1_1'],[4,7,'IKU1_1','IKU1_2'],[8,11,'IKU1_1','IKU1_3'],[12,255,'IKU1_1','IKU1_4',  ], ], ['TXT_KEY_SPELL_IKU_EXTRA1',],  ['TXT_KEY_SPELL_IKU_PHANTASM1',],   ],   ],
							 [ 'UNIT_SATORI1' , [    [   [1,3,'SATORI1_1','SATORI1_1'],[4,7,'SATORI1_1','SATORI1_2'],[8,11,'SATORI1_2','SATORI1_3'],[12,15,'SATORI1_2','SATORI1_4'],[16,255,'SATORI1_2','SATORI1_5',], ], ['TXT_KEY_SPELL_SATORI_EXTRA1',],  ['TXT_KEY_SPELL_SATORI_PHANTASM1',],   ],   ],
							 [ 'UNIT_MYSTIA1' , [    [   [1,7,'MYSTIA1_1','MYSTIA1_1'],[8,11,'MYSTIA1_2','MYSTIA1_1'],[12,255,'MYSTIA1_2','MYSTIA1_2'], ], ['TXT_KEY_SPELL_MYSTIA_EXTRA1',],  ['TXT_KEY_SPELL_MYSTIA_PHANTASM1',],   ],   ],
							 [ 'UNIT_SUIKA1' , [    [   [1,3,'SUIKA1_1','SUIKA1_1'],[4,7,'SUIKA1_1','SUIKA1_2'],[8,11,'SUIKA1_2','SUIKA1_3'],[12,255,'SUIKA1_2','SUIKA1_4',], ], ['TXT_KEY_SPELL_SUIKA_EXTRA1',],  ['TXT_KEY_SPELL_SUIKA_PHANTASM1',],   ],   ],
							 [ 'UNIT_SUIKA_BIG1' ,  [   [ ], [ ],  [ ],   ],   ],
							 [ 'UNIT_SUIKA_SMALL1' , [    [  ], [ ],  [ ],   ],   ],
							 [ 'UNIT_KOMACHI1' , [    [   [1,255,'KOMACHI1_1','KOMACHI1_1'], ], ['TXT_KEY_SPELL_KOMACHI_EXTRA1',],  ['TXT_KEY_SPELL_KOMACHI_PHANTASM1',],   ],   ],
							 [ 'UNIT_MEDICINwithSU1' , [    [   [1,3,'MEDICIN1_1','MEDICIN1_1'],[4,7,'MEDICIN1_1','MEDICIN1_2'],[8,11,'MEDICIN1_2','MEDICIN1_3'],[12,255,'MEDICIN1_2','MEDICIN1_4',  ], ], ['TXT_KEY_SPELL_MEDICIN_EXTRA1',],  ['TXT_KEY_SPELL_MEDICIN_PHANTASM1',],   ],   ],
							 [ 'UNIT_MEIRIN1' , [    [   [1,7,'MEIRIN1_1','MEIRIN1_1'],[8,255,'MEIRIN1_2','MEIRIN1_1'], ], ['TXT_KEY_SPELL_MEIRIN_EXTRA1',],  ['TXT_KEY_SPELL_MEIRIN_PHANTASM1',],   ],   ],
							 [ 'UNIT_YUKARI1' , [    [   [1,7,'YUKARI1_1','YUKARI1_1'],[8,255,'YUKARI1_2','YUKARI1_1'], ], ['TXT_KEY_SPELL_YUKARI_EXTRA1',],  ['TXT_KEY_SPELL_YUKARI_PHANTASM1','TXT_KEY_SPELL_YUKARI_PHANTASM2','TXT_KEY_SPELL_YUKARI_PHANTASM3',],   ],   ],
							 [ 'UNIT_KAGUYA1' , [    [   [1,3,'KAGUYA1_1','KAGUYA1_1'],[4,7,'KAGUYA1_2','KAGUYA1_1'],[8,11,'KAGUYA1_3','KAGUYA1_1'],[12,255,'KAGUYA1_4','KAGUYA1_1'], ], ['TXT_KEY_SPELL_KAGUYA_EXTRA1','TXT_KEY_SPELL_KAGUYA_EXTRA2','TXT_KEY_SPELL_KAGUYA_EXTRA3','TXT_KEY_SPELL_KAGUYA_EXTRA4','TXT_KEY_SPELL_KAGUYA_EXTRA5',],  ['TXT_KEY_SPELL_KAGUYA_PHANTASM1','TXT_KEY_SPELL_KAGUYA_PHANTASM2','TXT_KEY_SPELL_KAGUYA_PHANTASM3','TXT_KEY_SPELL_KAGUYA_PHANTASM4',],   ],   ],
							 [ 'UNIT_TENSHI1' , [    [   [1,7,'TENSHI1_1','TENSHI1_1'],[8,11,'TENSHI1_2','TENSHI1_1'],[12,255,'TENSHI1_3','TENSHI1_1'], ], ['TXT_KEY_SPELL_TENSHI_EXTRA1',],  ['TXT_KEY_SPELL_TENSHI_PHANTASM1',],   ],   ],
							 [ 'UNIT_RIN1' , [    [   [1,7,'RIN1_1','RIN1_1'],[8,255,'RIN1_2','RIN1_1'], ], ['TXT_KEY_SPELL_RIN_TO_CAT',],  ['TXT_KEY_SPELL_RIN_PHANTASM1',],   ],   ],
							 [ 'UNIT_RIN_CATMODE1' , [    [    ], ['TXT_KEY_SPELL_RIN_TO_RIN',],  [ ],   ],   ],
							 [ 'UNIT_LETTY1' , [    [   [1,255,'LETTY1_1','LETTY1_1'], ], ['TXT_KEY_SPELL_LETTY_EXTRA1',],  ['TXT_KEY_SPELL_LETTY_PHANTASM1',],   ],   ],
							 [ 'UNIT_MIMA1' , [    [   [1,255,'MIMA1_1','MIMA1_1'], ], ['TXT_KEY_SPELL_MIMA_EXTRA1',],  ['TXT_KEY_SPELL_MIMA_PHANTASM1',],   ],   ],
							 [ 'UNIT_EIKI1' , [    [   [1,255,'EIKI1_1','EIKI1_1'], ], ['TXT_KEY_SPELL_EIKI_EXTRA1',],  ['TXT_KEY_SPELL_EIKI_PHANTASM1',],   ],   ],
							 [ 'UNIT_NAZRIN1' , [    [   [1,7,'NAZRIN1_1','NAZRIN1_1'], [8,15,'NAZRIN1_2','NAZRIN1_2'], [16,255,'NAZRIN1_3','NAZRIN1_3'],   ], ['TXT_KEY_SPELL_NAZRIN_EXTRA1',],  ['TXT_KEY_SPELL_NAZRIN_PHANTASM1',],   ],   ],
							 [ 'UNIT_KOGASA1' , [    [   [1,7,'KOGASA1_1','KOGASA1_1'], [8,11,'KOGASA1_2','KOGASA1_1'], [12,255,'KOGASA1_3','KOGASA1_1'],   ], ['TXT_KEY_SPELL_KOGASA_EXTRA1',],  ['TXT_KEY_SPELL_KOGASA_PHANTASM1',],   ],   ],
							 [ 'UNIT_ICHIRIN1' , [    [   [1,7,'ICHIRIN1_1','ICHIRIN1_1'], [8,11,'ICHIRIN1_2','ICHIRIN1_1'], [12,255,'ICHIRIN1_3','ICHIRIN1_1'],   ], ['TXT_KEY_SPELL_ICHIRIN_EXTRA1',],  ['TXT_KEY_SPELL_ICHIRIN_PHANTASM1',],   ],   ],
							 [ 'UNIT_MINAMITSU1' , [    [   [1,3,'MINAMITSU1_1','MINAMITSU1_1'], [4,7,'MINAMITSU1_2','MINAMITSU1_1'], [8,255,'MINAMITSU1_3','MINAMITSU1_1'],   ], ['TXT_KEY_SPELL_MINAMITSU_EXTRA1',],  ['TXT_KEY_SPELL_MINAMITSU_PHANTASM1',],   ],   ],
							 [ 'UNIT_SYOU1' , [    [   [1,7,'SYOU1_1','SYOU1_1'],  [8,255,'SYOU1_2','SYOU1_1'],   ], ['TXT_KEY_SPELL_SYOU_EXTRA1',],  ['TXT_KEY_SPELL_SYOU_PHANTASM1',],   ],   ],
							 [ 'UNIT_BYAKUREN1' , [    [   [1,3,'BYAKUREN1_1','BYAKUREN1_1'], [4,7,'BYAKUREN1_2','BYAKUREN1_2'], [8,11,'BYAKUREN1_3','BYAKUREN1_3'], [12,15,'BYAKUREN1_4','BYAKUREN1_4'], [16,19,'BYAKUREN1_5','BYAKUREN1_5'], [20,255,'BYAKUREN1_6','BYAKUREN1_6'],    ], ['TXT_KEY_SPELL_BYAKUREN_EXTRA1',],  ['TXT_KEY_SPELL_BYAKUREN_PHANTASM1',],   ],   ],
							 [ 'UNIT_NUE1' , [    [   [1,255,'NUE1_1','NUE1_1'],    ], ['TXT_KEY_SPELL_NUE_EXTRA1',],  ['TXT_KEY_SPELL_NUE_PHANTASM1',],   ],   ],
							 [ 'UNIT_YOSHIKA1' , [    [   [1,7,'YOSHIKA1_1','YOSHIKA1_1'],[8,255,'YOSHIKA1_2','YOSHIKA1_1'],    ], ['TXT_KEY_SPELL_YOSHIKA_EXTRA1',],  ['TXT_KEY_SPELL_YOSHIKA_PHANTASM1',],   ],   ],
							 [ 'UNIT_SEIGA1' , [    [   [1,255,'SEIGA1_1','SEIGA1_1'],    ], ['TXT_KEY_SPELL_SEIGA_EXTRA1',],  ['TXT_KEY_SPELL_SEIGA_PHANTASM1',],   ],   ],
							 [ 'UNIT_TOJIKO1' , [    [   [1,7,'TOJIKO1_1','TOJIKO1_1'],[8,255,'TOJIKO1_2','TOJIKO1_1'],    ], ['TXT_KEY_SPELL_TOJIKO_EXTRA1',],  ['TXT_KEY_SPELL_TOJIKO_PHANTASM1',],   ],   ],
							 [ 'UNIT_FUTO1' , [    [   [1,7,'FUTO1_1','FUTO1_1'],[8,255,'FUTO1_2','FUTO1_1'],    ], ['TXT_KEY_SPELL_FUTO_EXTRA1',],  ['TXT_KEY_SPELL_FUTO_PHANTASM1',],   ],   ],
							 [ 'UNIT_MIMIMIKO1' , [    [   [1,15,'MIMIMIKO1_1','MIMIMIKO1_1'],[16,255,'MIMIMIKO1_2','MIMIMIKO1_1'],    ], ['TXT_KEY_SPELL_MIMIMIKO_EXTRA1',],  ['TXT_KEY_SPELL_MIMIMIKO_PHANTASM1',],   ],   ],
							 [ 'UNIT_YATUHASHI1' , [    [   [1,255,'YATUHASHI1_1','YATUHASHI1_1'],    ], ['TXT_KEY_SPELL_YATUHASHI_EXTRA1',],  ['TXT_KEY_SPELL_YATUHASHI_PHANTASM1',],   ],   ],
							 [ 'UNIT_BENBEN1' , [    [   [1,255,'BENBEN1_1','BENBEN1_1'],    ], ['TXT_KEY_SPELL_BENBEN_EXTRA1',],  ['TXT_KEY_SPELL_BENBEN_PHANTASM1',],   ],   ],
							 [ 'UNIT_SEIJA1' , [    [   [1,11,'SEIJA1_1','SEIJA1_1'],[12,255,'SEIJA1_2','SEIJA1_1'],    ], ['TXT_KEY_SPELL_SEIJA_EXTRA1',],  ['TXT_KEY_SPELL_SEIJA_PHANTASM1',],   ],   ],
							 [ 'UNIT_SHINMYOUMARU1' , [    [   [1,15,'SHINMYOUMARU1_1','SHINMYOUMARU1_1'],[16,255,'SHINMYOUMARU1_2','SHINMYOUMARU1_1'],    ], ['TXT_KEY_SPELL_SHINMYOUMARU_EXTRA1',],  ['TXT_KEY_SPELL_SHINMYOUMARU_PHANTASM1',],   ],   ],
							 [ 'UNIT_RAIKO1' , [    [   [1,255,'RAIKO1_1','RAIKO1_1'],    ], ['TXT_KEY_SPELL_RAIKO_EXTRA1',],  ['TXT_KEY_SPELL_RAIKO_PHANTASM1',],  ['TXT_KEY_SPELL_RAIKO_PHANTASM2',]   ],   ],

						]
		
		self.SpellDic = {}
		for i in range(len(self.SpellList)):
			self.SpellDic[gc.getInfoTypeForString(self.SpellList[i][0])] = self.SpellList[i][1]
		
		
		
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
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TOHOUNIT, iUnit)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TOHOUNIT, -1)

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
		screen.addPanel(self.top.getNextWidgetName(), localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_STACK_BONUS", ()), "", true, true, self.X_TOHO_UNIT_STACK_BONUS, self.Y_TOHO_UNIT_STACK_BONUS, self.W_TOHO_UNIT_STACK_BONUS, self.H_TOHO_UNIT_STACK_BONUS, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setImageButton(self.top.getNextWidgetName(), gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS')).getButton(), self.X_TOHO_UNIT_STACK_BONUS + 5, self.Y_TOHO_UNIT_STACK_BONUS + 30 , 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS'), -1)
		screen.setText(self.top.getNextWidgetName(), "", u"<font=3><color=140,255,40,255>" + "%s" %gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS')).getDescription() + u"</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_STACK_BONUS + 60, self.Y_TOHO_UNIT_STACK_BONUS + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
		screen.addMultilineText(self.top.getNextWidgetName(), CyGameTextMgr().getPromotionHelp( gc.getInfoTypeForString('PROMOTION_TEMP_STACK_BONUS'), True )[1:] , self.X_TOHO_UNIT_STACK_BONUS+55, self.Y_TOHO_UNIT_STACK_BONUS+50, self.W_TOHO_UNIT_STACK_BONUS-60, self.H_TOHO_UNIT_STACK_BONUS-60, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
		#STGスキル
		screen.addPanel(self.top.getNextWidgetName(), localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_STG_SKILL", ()), "", true, true, self.X_TOHO_UNIT_STG_SKILL, self.Y_TOHO_UNIT_STG_SKILL, self.W_TOHO_UNIT_STG_SKILL, self.H_TOHO_UNIT_STG_SKILL, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setImageButton(self.top.getNextWidgetName(), gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL')).getButton(), self.X_TOHO_UNIT_STG_SKILL + 5, self.Y_TOHO_UNIT_STG_SKILL + 30 , 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL'), -1)
		screen.setText(self.top.getNextWidgetName(), "", u"<font=3><color=140,255,40,255>" + "%s" %gc.getPromotionInfo(gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL')).getDescription() + u"</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TOHO_UNIT_STG_SKILL + 60, self.Y_TOHO_UNIT_STG_SKILL + 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 0, 0)
		screen.addMultilineText(self.top.getNextWidgetName(), CyGameTextMgr().getPromotionHelp( gc.getInfoTypeForString('PROMOTION_TEMP_STG_SKILL'), True )[1:] , self.X_TOHO_UNIT_STG_SKILL+55, self.Y_TOHO_UNIT_STG_SKILL+50, self.W_TOHO_UNIT_STG_SKILL-60, self.H_TOHO_UNIT_STG_SKILL-60, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		
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
				szText = szText + "\n\n<color=254,140,50,254>" + localText.getText( "TXT_KEY_SPELLCARD_" + Spell[2], ()) + "</color>\n"
				tempText = "TXT_KEY_SPELLCARD_" + Spell[3] + "_HELP"
				szText = szText + localText.getText(tempText, ())
		szText = self.TextToInt(szText[2:])
		screen.addMultilineText(self.SpellPanel[1], szText , self.X_SPELL_CARD+5, self.Y_SPELL_CARD+30, self.W_SPELL_CARD-10, self.H_SPELL_CARD-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		#Exスペル
		screen.addPanel(self.SpellPanel[2], localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_SPELL_EXTRA", ()), "", true, true, self.X_SPELL_EXTRA, self.Y_SPELL_EXTRA, self.W_SPELL_EXTRA, self.H_SPELL_EXTRA, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		for Spell in self.SpellDic[self.iUnit][1]:
		
			szText = szText + "\n\n<color=255,140,50,255>" + localText.getText(Spell, ()) + "</color>\n"
			tempText = Spell + "_HELP"
			szText = szText + localText.getText(tempText, ())
		szText = self.TextToInt(szText[2:])
			
		screen.addMultilineText(self.SpellPanel[3], szText , self.X_SPELL_EXTRA+5, self.Y_SPELL_EXTRA+30, self.W_SPELL_EXTRA-10, self.H_SPELL_EXTRA-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		#Phanスペル
		screen.addPanel(self.SpellPanel[4], localText.getText("TXT_KEY_PEDIA_CATEGORY_TOHOUNIT_SPELL_PHANTASM", ()), "", true, true, self.X_SPELL_PHANTASM, self.Y_SPELL_PHANTASM, self.W_SPELL_PHANTASM, self.H_SPELL_PHANTASM, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		for Spell in self.SpellDic[self.iUnit][2]:
		
			szText = szText + "\n\n<color=255,140,50,255>" + localText.getText(Spell, ()) + "</color>\n"
			tempText = Spell + "_HELP"
			szText = szText + localText.getText(tempText, ())
		szText = self.TextToInt(szText[2:])
			
		screen.addMultilineText(self.SpellPanel[5], szText , self.X_SPELL_PHANTASM+5, self.Y_SPELL_PHANTASM+30, self.W_SPELL_PHANTASM-10, self.H_SPELL_PHANTASM-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

		
		
		
	
	#[***]の置換
	def TextToInt(self,szText):
		match = re.compile(r"\[...\]")
		match3 = re.compile("%")
		match4 = re.compile("@@")
		searchList = match.findall(szText)
		searchList2 = match3.findall(szText)
		for str in searchList2:
			szText = match3.sub("@@",szText,1)
		for str in searchList:
			match2 = re.compile(str[1:4])
			szText = match2.sub("%d",szText,1)
			szText = szText % gc.getTextToSpellInt(str[1:4].encode("utf-8"),self.CAL)
		for str in searchList2:
			szText = match4.sub("%",szText,1)
			
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
			screen.clearListBoxGFC(self.top.LIST_ID)
		
		# sort Units alphabetically
		unitsList=[(0,0)]*gc.getNumUnitInfos()
		for j in range(gc.getNumUnitInfos()):
			unitsList[j] = (gc.getUnitInfo(j).getDescription(), j)
		
		unitsList.sort()
		
		listCopy = unitsList[:]
		for item in listCopy:
			if item[1] > 0:
				if gc.getUnitInfo(item[1]-1).getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
					unitsList.remove(item)
			else:
				unitsList.remove(item)
		
		#ソートなんてめんどうだ、自分でリストを作ってしまえ
		unitsList=[(0,0)]*len(self.SortList)
		for j in range(len(self.SortList)):
			unitsList[j] = ( self.SortList[j][2] + gc.getUnitInfo(gc.getInfoTypeForString(self.SortList[j][0])).getDescription() + "</color>", gc.getInfoTypeForString(self.SortList[j][0]))
		
		i = 0
		iSelected = 0
		#print unitsList
		#for iI in range(gc.getNumUnitInfos()):
		for iI in range(len(unitsList)):
			if (not gc.getUnitInfo(unitsList[iI][1]).isGraphicalOnly()):
				if (not gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") or not gc.getGame().isFinalInitialized() or gc.getGame().isUnitEverActive(unitsList[iI][1])):
					if bRedraw:
						screen.appendListBoxStringNoUpdate( self.top.LIST_ID, unitsList[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_TOHOUNIT, unitsList[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY )
					if unitsList[iI][1] == self.iUnit:
						iSelected = i
					i += 1
					
		if bRedraw:
			screen.updateListBox(self.top.LIST_ID)

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)
			
	def placePromotions(self):
		screen = self.top.getScreen()
		
		# add pane and text
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", true, true, self.X_PROMO_PANE, self.Y_PROMO_PANE, self.W_PROMO_PANE, self.H_PROMO_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
				
		# add promotion buttons
		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.X_PROMO_PANE+15, self.Y_PROMO_PANE+40, self.W_PROMO_PANE-20, self.H_PROMO_PANE-40, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
	
		for k in range(gc.getNumPromotionInfos()):
			if (isPromotionValid(k, self.iUnit, false) and not gc.getPromotionInfo(k).isGraphicalOnly()):
				screen.appendMultiListButton( rowListName, gc.getPromotionInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, k, -1, false )
								
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


##### </written by F> #####