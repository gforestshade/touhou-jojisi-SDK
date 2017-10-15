##### <written by F> #####
#�����g���p�֐��Q

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import math
import SpellInfo

import TohoCivList

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

RangeList0 = [[0,0],]

RangeList1 = [	[-1,-1],[ 0,-1],[ 1,-1],
				[-1, 0],        [ 1, 0],
				[-1, 1],[ 0, 1],[ 1, 1], ]

# �f�o�b�O�o��
def doprint(str):
	#cd sys.stderr.write(str)
	if not logInited:
		initLog()
	sys.stdout.write(str)
	sys.stdout.write("\n")
#	sys.stdout.flush()


#�w�肳�ꂽ�ꏊ���L����plot�ł��邩�ǂ����𔻕�
#�f�t�H�̂��ƃ��[�v��������肭�����Ȃ��̂Ŏ��O�Ŏ���
def isPlot(iX,iY):
	pMap = gc.getMap()
	iWidth = pMap.getGridWidth()
	iHeight = pMap.getGridHeight()
	
	#X���L���͈͓����ǂ����`�F�b�N
	bFlagX = False
	if -1<iX and iX<iWidth:
		bFlagX = True
	else:
		if pMap.isWrapX():
			bFlagX = True
	
	#Y���L���͈͓����ǂ����`�F�b�N
	bFlagY = False
	if -1<iY and iY<iHeight:
		bFlagY = True
	else:
		if pMap.isWrapY():
			bFlagY = True
	
	if bFlagX and bFlagY:
		return True
	
	return False


#�͈͓��Ɏw�肳�ꂽ���j�b�g�����邩�ǂ������`�F�b�N����
def checkUnit(iX,iY,squeaList,iStartUnit,iEndUnit,returnUnitFlag = 0):
	UnitList = []
	for squea in squeaList:
		iiX = iX + squea[0]
		iiY = iY + squea[1]
		if isPlot(iiX,iiY):
			pPlot = gc.getMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if iStartUnit <= pUnit.getUnitType() and pUnit.getUnitType() <= iEndUnit:
					if returnUnitFlag == 1:
						return pUnit
					elif returnUnitFlag == 2:
						UnitList.append(pUnit)
					else:
						return True
	if returnUnitFlag == 2:
		return UnitList
	else:
		return False


#���X�^�b�N�̖����������j�b�g��T���ă��X�g��Ԃ�
def searchTeamTohoUnit(pPlot,unit):
	UnitList=[]
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
			if unit.getTeam() == pUnit.getTeam():
				UnitList.append(pUnit)
	
	return UnitList



#�X�y�J��req�֐��̔ėp�֐�
def req_SpellCard(bTestVisible,caster,iStartCAL,iEndCAL,sStartUnit,sEndUnit,cost=0):

	if bTestVisible:
		if iStartCAL <= caster.countCardAttackLevel() and caster.countCardAttackLevel() <= iEndCAL:
			if gc.getInfoTypeForString(sStartUnit) <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString(sEndUnit):
				return True
			if gc.getInfoTypeForString('UNIT_SATORI1') <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString('UNIT_SATORI6'):
				RangeList = [ [-1,-1],[ 0,-1],[ 1,-1],[-1, 0], [ 0, 0],[ 1, 0],[-1, 1],[ 0, 1],[ 1, 1], ]
				if checkUnit(caster.getX(),caster.getY(),RangeList,gc.getInfoTypeForString(sStartUnit),gc.getInfoTypeForString(sEndUnit)):
					return True
	else:
		#if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELLCARD")):
		if caster.getPower() >= cost:
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False:
				if caster.getPower() >= cost:
					if caster.getNumSpellCardBreakTime() <= 0:
						return True
				
	return False

#�X�y����req�֐��̔ėp�֐�
def req_Spell(bTestVisible,caster,sPromotion,sStartUnit,sEndUnit,cost=0):

	if bTestVisible:
		if gc.getInfoTypeForString(sStartUnit) <= caster.getUnitType() and caster.getUnitType() <= gc.getInfoTypeForString(sEndUnit):
			return True
	else:
		if caster.isHasPromotion(gc.getInfoTypeForString(sPromotion)):
			if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SPELL_CASTED")) == False and caster.getPower() >= cost:
				if sPromotion == 'PROMOTION_MODE_EXTRA' and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE2') ):
					return True
				if sPromotion == 'PROMOTION_MODE_PHANTASM' and gc.getTeam(caster.getTeam()).isHasTech( gc.getInfoTypeForString('TECH_SHOOTING_TECHNIQUE3') ):
					return True
				if sPromotion == 'PROMOTION_FLAN':
					return True
				if sPromotion == 'PROMOTION_ICHIRIN_SKILL1':
					return True
				if sPromotion == 'PROMOTION_BYAKUREN_SKILL1':
					return True
				if sPromotion == 'PROMOTION_YORIHIME_SKILL1':
					return True
	return False



#�_���[�W�֐�
#�w�肳�ꂽ�͈͂ɐݒ肳�ꂽ��ނ̃��j�b�g�Ƀ_���[�W��^���� �v���C���[��`�h�݂̂Ɍ��ʂ����邩�H�@�X�y���ϐ����ђʂ��邩�ǂ����H
#�͈͂�caster����̑��΃p�X�@�_���[�W����Ƌ����ɂ��␳
#�_���[�W��^����ő僆�j�b�g���H�@�񕜂��ł���悤�ɁH
#�X�^���h�o�C���j�b�g�ɂ͌��ʂ��o�Ȃ��悤��
#iBorder�͈Ӗ��̂Ȃ��ϐ��@�������������ČĂяo���ۂɂ�₱�����Ă��傤���Ȃ������̂ŁA��؂蕶�������
#bTrialCalc��True�̂Ƃ��̓_���[�W��or�񕜗ʂ̍��v���v�Z���ĕԂ�
def changeDamage(squeaList,caster,minDamage,maxDamage,iLimitDamage,bPercent,bFriend,bNeutral,bEnemy,iBorder1,bToho,bGeneral,bPlayer,bAI,iBorder2,bAntiSpellBarrier,iDistanceCorrect,iSpecial=0,bTrialCalc = False):
	iTrialCalcNum = 0
	damageUnitList = []
	
	for squea in squeaList:
		iX = caster.getX() + squea[0]
		iY = caster.getY() + squea[1]
		if not isPlot(iX,iY):
			continue
		iNumKOTohoUnit = 0
		pPlot = gc.getMap().plot(iX,iY)
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i+iNumKOTohoUnit).getDamage() >= 100:
				iNumKOTohoUnit = iNumKOTohoUnit + 1
			pUnit = pPlot.getUnit(i+iNumKOTohoUnit)
			pTeam = gc.getTeam(caster.getTeam())

			#### �_����ނ̃��j�b�g�łȂ��Ȃ��΂�
			
			# �F�D�E�����E�G��
			bFlag = False 
			if bFriend and caster.getTeam() == pUnit.getTeam():
				bFlag = True
			if bNeutral and caster.getTeam() != pUnit.getTeam() and not pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if not bFlag:
				continue

			# �v���C���[�EAI
			bFlag = False
			if pUnit.isHuman() and bPlayer:
				bFlag = True
			if not pUnit.isHuman() and bAI:
				bFlag = True
			if not bFlag:
				continue

			# �������j�b�g�E��ʕ�
			bFlag = False
			if bToho and pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				bFlag = True
			elif bGeneral:
				bFlag = True
			if not bFlag:
				continue

			#### �ǉ��̐���

			# �ނ炳�p�t���O�Ȃ� �D�����j�b�g�ȊO�͔�΂�
			if iSpecial == 5:
				if pUnit.getDomainType() != gc.getInfoTypeForString('DOMAIN_SEA'):
					continue
			
			#### �_���[�W�ʂ̌v�Z
			if minDamage == maxDamage:
				iDamage = minDamage
			elif minDamage >= 0: #�_���[�W�̂Ƃ�
				iDamage = minDamage + gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")
			else: #�񕜂̂Ƃ�
				iDamage = maxDamage - gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")

			#### ��b�_���[�W�ւ̒ǉ��̕␳
			
			# �߁[���p�t���O�Ȃ�
			if iSpecial == 2:
				iDamage -= pUnit.countAutoHeal()
			# �������p�t���O�Ȃ�Ώۃ��j�b�g�̌o���l�ɔ�Ⴕ���_���[�W
			if iSpecial == 3:
				iDamage = int(pUnit.getExperience() * ( caster.countCardAttackLevel() * 0.1 + 1  ) )

			#### �␳
			
			# �e���ϐ�
			if not bAntiSpellBarrier:
				iDamage = (iDamage * (100 - pUnit.countSpellTolerance())) / 100
			
			# �����ɂ��␳
			if iDistanceCorrect == 1:
				# �ς����X�y�J�ł����g���ĂȂ�����
				# �g�p�҂ƑΏێ҂Ƃ̋��������[�N���b�h�����ŋ��߂�
				iDistance = math.sqrt(  (caster.getX()-pUnit.getX())**2 + (caster.getY()-pUnit.getY())**2 )
				iDamage = iDamage * (  ( math.sqrt( (caster.getLevel()**2) * 2) - iDistance  )  / math.sqrt( (caster.getLevel()**2) * 2)    )  
				iDamage = int(iDamage)

			# �����_���[�W
			# ��HP * iDamage[%]
			if bPercent: 
				if minDamage >= 0: #�_���[�W�̂Ƃ�
					iDamage = (100 - pUnit.getDamage()) * iDamage/100
				else:
					iDamage = pUnit.getDamage() * iDamage / 100

			# �_���[�W���������Ȃ炻���Ŏ~�܂�
			if minDamage >= 0: #�_���[�W�̂Ƃ�
				if 100 - pUnit.getDamage() <= iLimitDamage:
					iDamage = 0
				elif 100 - pUnit.getDamage() - iDamage <= iLimitDamage:
					iDamage = 100 - pUnit.getDamage() - iLimitDamage
			else: #�񕜂̂Ƃ�
				if 100 - pUnit.getDamage() >= iLimitDamage:
					iDamage = 0
				elif 100 - pUnit.getDamage() - iDamage >= iLimitDamage:
					iDamage = 100 - pUnit.getDamage() - iLimitDamage

			ow = pUnit.getOwner()
			iTrialCalcNum += iDamage
			if not bTrialCalc:
				# ��x�L������
				damageUnitList.append( [pUnit,ow,iDamage] )
			
				# �_���[�W��^���郆�j�b�g�ւ̒ǉ��̏���
				
				# �����p�t���O�Ȃ�5G�𓾂�
				if iSpecial == 1: 
					if pUnit.getDamage() + iDamage >= 100:
						#caster.changeExperience(1,-1,False,False,False)
						gc.getPlayer(caster.getOwner()).changeGold(5)
	
	
	# ���ۂɂ̓_���[�W��^�������_���[�W�ʂ�Ԃ�
	if bTrialCalc:
		if iTrialCalcNum < 0:
			iTrialCalcNum = 0 - iTrialCalcNum
		return iTrialCalcNum
	
	# �_���[�W
	for item in damageUnitList:
		if iLimitDamage <= 0:
			# �L���b�v0�ȉ��̏ꍇ�A�D�ƈꏏ�ɒ��񂾉\��������̂ŁA�{���ɂ��邩�ēx�m�F����
			if gc.getPlayer(item[1]).getUnit(item[0].getID()).getUnitType() != -1:
				item[0].changeDamage(item[2],caster.getOwner())
		else:
			item[0].changeDamage(item[2],caster.getOwner())
	
	
	
#���i�t�^�֐�
def setPromotion(squeaList,caster,sPromotion,bSet,iPercent,bFriend,bNeutral,bEnemy,iBorder1,bToho,bGeneral,bPlayer,bAI,iBorder2,bAntiSpellBarrier,onEffect=0,iSpecial=0,bGain=False,bSpell=False,iBorder3=0,iTurnPromo=0):
	iPromotion = gc.getInfoTypeForString(sPromotion)
	iUnitNum = 0
	for squea in squeaList:
		iX = caster.getX() + squea[0]
		iY = caster.getY() + squea[1]
		if not isPlot(iX,iY):
			continue
		
		iNumKOTohoUnit = 0
		pPlot = gc.getMap().plot(iX,iY)
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i+iNumKOTohoUnit).getDamage() >= 100:
				iNumKOTohoUnit = iNumKOTohoUnit + 1
			pUnit = pPlot.getUnit(i+iNumKOTohoUnit)
			pTeam = gc.getTeam(caster.getTeam())

			#### �_����ނ̃��j�b�g�łȂ��Ȃ��΂�

			# �F�D�E�����E�G��
			bFlag = False 
			if bFriend and caster.getTeam() == pUnit.getTeam():
				bFlag = True
			if bNeutral and caster.getTeam() != pUnit.getTeam() and not pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if not bFlag:
				continue

			# �v���C���[�EAI
			bFlag = False
			if pUnit.isHuman() and bPlayer:
				bFlag = True
			if not pUnit.isHuman() and bAI:
				bFlag = True
			if not bFlag:
				continue
			
			# �������j�b�g�E��ʕ�
			bFlag = False
			if bToho and pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				bFlag = True
			elif bGeneral:
				bFlag = True
			if not bFlag:
				continue

			#### �m���ւ̕␳
			iPer = iPercent
			
			# �e���ϐ�
			if bAntiSpellBarrier == False:
				iPer = (iPer * (100 - pUnit.countSpellTolerance())) / 100

			#### �ǉ��̊m���␳
			
			# ���e�BPhan�X�y���p�t���O�Ȃ�
			# �ጴ��3�{ �c���h����2�{
			if iSpecial == 4: 
				if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
					iPer = iPer * 3
				if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
					iPer = iPer * 2

			#### �T�C�R����U���ē��������Ȃ�
			if gc.getGame().getSorenRandNum(100, "spellcard cast") < iPer:
				# �����Phan�X�y���Ȃ�
				
				if iSpecial == 3:
					if ( (gc.getInfoTypeForString('UNIT_CIRNO1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_CIRNO6')  ) or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN')  ):
						pUnit.setHasPromotion(iPromotion,bSet)
				else:
					pUnit.setHasPromotion(iPromotion,bSet)
					iUnitNum += 1

				#### ���i��^���邱�Ƃɐ����������j�b�g�ւ̒ǉ��̏���

				# �G�t�F�N�g�H
				if onEffect == 1:
					point = pUnit.plot().getPoint()
					CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
					CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

				# ���~���APhan�X�y���p�t���O�Ȃ�
				# �ő��������Ă���Ή�
				if iSpecial == 1: 
					if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KENZOKU')):
						pUnit.changeDamage(-caster.countCardAttackLevel()/2,caster.getOwner())

				# �䂩���X�y�J�p�t���O�Ȃ�
				# �e�����E��^����1�^�[���̈ړ��s��
				if iSpecial == 2: 
					pUnit.setDanmakuKekkai(0,caster.countCardAttackLevel()/4 + 1)
					pUnit.setImmobileTimer(1)
				# �������X�y�J�p�t���O�Ȃ�s���I��
				if iSpecial == 5: 
					pUnit.finishMoves()
				# �Ƃ�Ђ�Phan�X�y���p�t���O�Ȃ�1�^�[���̈ړ��s��
				if iSpecial == 6: 
					pUnit.setImmobileTimer(1)

				# �ꎞ�I�ȏ��i�������Ȃ�܂� ���� �̂�iTurnPromo�^�[��
				if iTurnPromo > 0:
					pUnit.setNumTurnPromo( pUnit.getNumTurnPromo() + iTurnPromo )
	
	#caster�ւ�Power�Q�C��
	#���̍ۂ���������bGain�͑S��False�ɂ���H
	if bGain:
		#��l�̌v�Z
		iBase = iPercent * 30.0 / 100.0
		if bSpell:
			iBase = iBase * 5
		caster.setPower( caster.getPower() + ( 0.5 * iUnitNum / iBase  )  )


#�e���ϐ����J�E���g
def countSpellTolerance(pUnit):
	
	return pUnit.countSpellTolerance()

#AI�̓�Փx�␳�����߂�
def getHandicap():
	
	Handi = 0;
	for i in range(TohoCivList.iMaxPlayer):
		pPlayer = gc.getPlayer(i)
		if pPlayer.isHuman() == True:
			if Handi < pPlayer.getHandicapType():
				Handi = pPlayer.getHandicapType()
	return Handi


#AI�̃X�y���g�p
def AISpellCast(caster):
	
	CAL = caster.countCardAttackLevel()
	
	if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_AI_NOT_SPEL_CAST')):
		return False
	
	#AI�ɂ��X�y�J�g�p
	
	Spells = SpellInfo.spells
	canSpellList = []
	
	#�g�p�\���]���O�ȏ�̃X�y���𔲂��o��
	for i in range( len(Spells) ):
		Spell = Spells[i]
		if Spell.isVisible(caster) and Spell.isAbled(caster):
			EstimatePoint = Spell.estimate(caster) #�]���l���g�p�m��
			if EstimatePoint > 0:
			
				#Power�̎c�ʂ⏸�i���[�g�ɂ���ĕ]���l�𑝌�����
				if caster.getPower()<2:
					EstimatePoint = EstimatePoint * 0.7
				elif caster.getPower()<3:
					EstimatePoint = EstimatePoint * 0.8
				elif caster.getPower()<4:
					EstimatePoint = EstimatePoint * 0.9
				
				if caster.getAIPromotionRoute() == 1: #COMBAT
					EstimatePoint = EstimatePoint * 0.15
				if caster.getAIPromotionRoute() == 2: #STG
					EstimatePoint = EstimatePoint * 0.30
				
				canSpellList.append([i,EstimatePoint])
	
	#�]���l�ō~���Ƀ\�[�g
	for i in range( len(canSpellList) ):
		for j in range(i+1,len(canSpellList)):
			if canSpellList[i][1] < canSpellList[j][1]:
				temp = canSpellList[i]
				canSpellList[i] = canSpellList[j]
				canSpellList[j] = temp
	
	#�]���l�̍������Ɏg�p����
	for i in range(len(canSpellList)):
		if gc.getGame().getSorenRandNum(100,"AI Spell cast") < canSpellList[i][1]:
			if Spells[ canSpellList[i][0] ].cast(caster):
				#�����������E����MOD�ǋL
				#�X�y���̏����ύX�ɔ��������ύX@gforest_shade������
				#iNum = canSpellList[i][0]+5
				iNum = gc.getInfoTypeForString( Spells[ canSpellList[i][0] ].getName() )
			#	if iNum <= gc.getInfoTypeForString("SPELLCARD_MIMIMIKO1_2"): #�X�y�J�ł����
				caster.setNumCastSpellCard( caster.getNumCastSpellCard() + 1 )
				if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
					caster.setNumSpellCardBreakTime( 2 )
				CyInterface().addImmediateMessage(gc.getUnitInfo(caster.getUnitType()).getDescription() + "&#12364;" + gc.getAutomateInfo(iNum).getDescription() + "&#12434;&#20351;&#29992;&#12375;&#12414;&#12375;&#12383;","")
				
				return True



	
#�ėp�����֐�(��s�����͂����ň���Ȃ�)
def RevivalUnit(pRevivalUnit,pKilledUnit):
	
	
	pRevivalUnit.changeExperience(pKilledUnit.getExperience(),-1,false,false,false)
	pRevivalUnit.changeLevel(pKilledUnit.getLevel()-1)
	
	pRevivalUnit.setNumCastSpellCard(pKilledUnit.getNumCastSpellCard())
	pRevivalUnit.setNumAcquisSpellPromotion(pKilledUnit.getNumAcquisSpellPromotion())
	pRevivalUnit.setSinraDelayTurn(pKilledUnit.getSinraDelayTurn())
	pRevivalUnit.setNumTransformTime(pKilledUnit.getNumTransformTime())
	pRevivalUnit.setSpecialNumber(pKilledUnit.getSpecialNumber())
	
	pRevivalUnit.setDanmakuKekkai(pKilledUnit.getNowDanmakuKekkai(),pKilledUnit.getMaxDanmakuKekkai() )
	pRevivalUnit.setAIPromotionRoute(pKilledUnit.getAIPromotionRoute())
	pRevivalUnit.setPower( pKilledUnit.getPower())
	
	for i in range(3):
		pRevivalUnit.setNumPowerUp(i,pKilledUnit.getNumPowerUp(i));
	
	
	#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
	PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
	PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
	PromotionNum = PromotionEnd - PromotionStart
	
	for iPromotion in range(PromotionNum):
		if pKilledUnit.isHasPromotion(iPromotion):
			pRevivalUnit.setHasPromotion(iPromotion,True)



#���镶�����ؑ��ȊO�̕����Ɛ푈��Ԃɂ��邩�ǂ������`�F�b�N
def isWar(iPlayer):

	pTeam = gc.getTeam( gc.getPlayer(iPlayer).getTeam() )
	iNumTeam = gc.getMAX_CIV_TEAMS()
	for i in range(iNumTeam):
		ppTeam = gc.getTeam(i)
		if ppTeam.isBarbarian() == False:
			if pTeam.isAtWar(i):
				return True
	
	return False

# # # �����������E����MOD�ǋL

def changeTurnPromo(pUnit, i):
	pUnit.setTurnPromo(pUnit.getTurnPromo() + i)

def setPromotionEx(pUnit, sPromotion):
	iPromotion = gc.getInfoTypeForString(sPromotion)
	
	for p,i in TohoUnitList.TempPromotionList:
		if p == sPromotion:
			pUnit.setHasPromotion(iPromotion, True)
			changeTurnPromo(pUnit, i)
			return
	
	pUnit.setHasPromotion(iPromotion, True)
	return

# �e���t�H�[���\�����P�𑦎���������
# �ł�����True, �ł��Ȃ�������False��Ԃ�
def terraformImprovementUpgrade(pPlot):
	iX = pPlot.getX()
	iY = pPlot.getY()
	
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_PLAIN'):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
		pPlot.setImprovementType(-1)
		CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_PLAIN_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/plains.dds',ColorTypes(11),iX,iY,True,True)
		return True
	
	elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_GRASS'):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)
		pPlot.setImprovementType(-1)
		CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_GRASS_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(11),iX,iY,True,True)
		return True
		
	elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_HILL'):
		pPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
		pPlot.setImprovementType(-1)
		CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_HILL_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/hill.dds',ColorTypes(11),iX,iY,True,True)
		return True
	
	elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FLATLAND'):
		pPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
		pPlot.setImprovementType(-1)
		CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FLATLAND_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/baseterrain/grassland.dds',ColorTypes(11),iX,iY,True,True)
		return True
	
	elif pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TERRAFORM_FOREST'):
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_REGENERATION_FOREST'), 1)
		pPlot.setImprovementType(-1)
		spellFlag = True
		CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_TERRAFORMING_COMPLETED_FOREST_ANNOUNCE",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/terrainfeatures/forest.dds',ColorTypes(11),iX,iY,True,True)
		return True

	else:
		return False


# �n�`���P�𑦎��A�b�v�O���[�h����
# �ł�����True, �ł��Ȃ�������False��Ԃ�
def improvementUpgrade(pPlot):
	
	imprInfo = gc.getImprovementInfo( pPlot.getImprovementType() )
	iUpgrade = imprInfo.getImprovementUpgrade()
	
	if iUpgrade != -1:
		pPlot.setImprovementType(iUpgrade)
		return True

	return False

# ���i��ʂ̃��j�b�g�ɃR�s�[����
# pSourceUnit �̎����Ă��鏸�i���ׂĂ� pDestinationUnit �Ɏ�������
# pSourceUnit �̎����Ă��Ȃ����i�͂Ȃɂ����Ȃ� pDestinationUnit ��������킯�ł͂Ȃ�
def copyPromotions(pSourceUnit, pDestinationUnit):

	PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
	PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
	PromotionNum = PromotionEnd - PromotionStart
	
	for iPromotion in range(PromotionNum):
		if pSourceUnit.isHasPromotion(iPromotion):
			pDestinationUnit.setHasPromotion(iPromotion,True)

	pDestinationUnit.setNumTurnPromo(pSourceUnit.getNumTurnPromo())

#�ؑ���
def uncivilize(pUnit):
	BarBarianUnit = pUnit.getUnitType()
	plotX = pUnit.getX()
	plotY = pUnit.getY()
	iExperience = pUnit.getExperience()
	iLevel = pUnit.getLevel()
	
	#���͂P�}�X�ŋ󂢂Ă�ꏊ��T���A�Ȃ���Ώ���
	ClearPlotList = []
	for iX in range(plotX-1,plotX+2):
		for iY in range(plotY-1,plotY+2):
			if gc.getMap().plot(iX,iY).getNumUnits() == 0:
				ClearPlotList.append([iX,iY])
	
	if ClearPlotList:
		iNum = gc.getGame().getSorenRandNum(len(ClearPlotList), "create barbarian plot")
		iiX = ClearPlotList[iNum][0]
		iiY = ClearPlotList[iNum][1]
		newUnit1 = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(BarBarianUnit, iiX, iiY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		newUnit1.changeExperience(iExperience,-1,false,false,false)
		newUnit1.changeLevel(iLevel-1)
		
		#���Ƃ��Ǝ����Ă������i�����̂܂܈ڍs������
		copyPromotions(pUnit, newUnit1)
		
		newUnit1.finishMoves()

		# ���i�S����̔ؑ���...���ǂ����͂킩��Ȃ����A�����Ă������
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_EASY'),False)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_NORMAL'),False)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_HARD'),False)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_LUNATIC'),False)
		
		pUnit.changeDamage(100,pUnit.getOwner())
		

# �X���A���̐��E���@
# pPlayer �̌��Ƀ��j�b�g���W�܂�(�K�������X���A���ł���K�v�͂Ȃ�)
# pPlot �Ŕ����G�t�F�N�g����������(�K������caster.plot()�ł���K�v�͂Ȃ�)
def worldspell_HYOUSEIRENGOU1(pPlayer, pPlot):

	#�����Ă��郆�j�b�g�Ɛ��͎���ˑ�
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT'):
		iUnit = gc.getInfoTypeForString('UNIT_WARRIOR')
		iNumUnit = 2
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL'):
		iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
		iNumUnit = 3
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL'):
		iUnit = gc.getInfoTypeForString('UNIT_MACEMAN')
		iNumUnit = 5
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE'):
		iUnit = gc.getInfoTypeForString('UNIT_MUSKETMAN')
		iNumUnit = 5
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL'):
		iUnit = gc.getInfoTypeForString('UNIT_RIFLEMAN')
		iNumUnit = 5
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN'):
		iUnit = gc.getInfoTypeForString('UNIT_INFANTRY')
		iNumUnit = 5
	if pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE'):
		iUnit = gc.getInfoTypeForString('UNIT_MECHANIZED_INFANTRY')
		iNumUnit = 5
	
	py = PyPlayer( pPlayer.getID() )
	for pyCity in py.getCityList():
		#pCity = pPlayer.getCity(pPyCity.getID())
		iNum = pyCity.getPopulation() / iNumUnit
		if iNum < 1:
			iNum = 1
		if iNum > 3:
			iNum = 3
		for i in range(iNum):
			newUnit = py.initUnit(iUnit, pyCity.getX(), pyCity.getY())
			exp = gc.getGame().getSorenRandNum(6, "world spell rengou no kessoku")
			newUnit.changeExperience(exp, -1, False, False, False)
	
	pPlayer.setNumWorldSpell(0)

	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	#�d�����������������ߓs�s�ɏW�����܂���
	CyInterface().addImmediateMessage("&#22934;&#31934;&#12383;&#12385;&#12364;&#32080;&#26463;&#12434;&#39640;&#12417;&#37117;&#24066;&#12395;&#38598;&#32080;&#12375;&#12414;&#12375;&#12383;","")

# �P�j��̐��E���@
# pPlayer �̌��ɕt�r�_������(�K�������P�j��ł���K�v�͂Ȃ�)
# pPlot �Ŕ����G�t�F�N�g����������(�K������caster.plot()�ł���K�v�͂Ȃ�)
def worldspell_KISHINJOU1(pPlayer, pPlot):
	# iPlayer = caster.getOwner()
	pTeam = gc.getTeam(pPlayer.getTeam())
	
	TAIKO = 1
	TYUUSEI = 2
	KINDAI = 4
	era = 0
	
	#����ɂ���ĕ������郆�j�b�g��v�Z����ϓ�������
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_ANCIENT')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_CLASSICAL')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TAIKO')
		iNumCityCountKOU = 3
		era = TAIKO
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MEDIEVAL')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_RENAISSANCE')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_TYUUSEI')
		iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_TYUUSEI')
		iNumCityCountKOU = 5
		iNumCityCountOTU = 8
		era = TYUUSEI
	if (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_INDUSTRIAL')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_MODERN')) or (pPlayer.getCurrentEra() == gc.getInfoTypeForString('ERA_FUTURE')):
		iUnitKOU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_KOU_KINDAI')
		iUnitOTU = gc.getInfoTypeForString('UNIT_TSUKUMOGAMI_OTU_KINDAI')
		iNumCityCountKOU = 5
		iNumCityCountOTU = 8
		era = KINDAI
	
	py = PyPlayer( pPlayer.getID() )
	for pyCity in py.getCityList():
		if era == TAIKO:
			# �b��2�𒴂����A���͔������Ȃ�
			iNumKOU = pyCity.getPopulation() / iNumCityCountKOU
			iNumKOU = min(iNumKOU, 2)
			iNumOTU = 0
		
		elif era == TYUUSEI or era == KINDAI:
			# �b���Ƃ�1������炸�A3�𒴂��Ȃ�
			iNumKOU = pyCity.getPopulation() / iNumCityCountKOU
			iNumKOU = max(1, iNumKOU)
			iNumKOU = min(iNumKOU, 3)

			iNumOTU = pyCity.getPopulation() / iNumCityCountOTU
			iNumOTU = max(1, iNumOTU)
			iNumOTU = min(iNumOTU, 3)

		else:
			# �����ɂ͗��Ȃ��͂�����
			doprint("KISHINJOU1: era error")
			iNumKOU = 0
			iNumOTU = 0
			
		if iNumKOU > 0:
			for i in range(iNumKOU):
				pyCity.initUnit(iUnitKOU)
		if iNumOTU > 0:
			for i in range(iNumOTU):
				pyCity.initUnit(iUnitOTU)

	pPlayer.setNumWorldSpell(0)
	# ���Z�܂�
	pPlayer.setTohoFlag(TohoFlags.TOHOFLAGS_TURNCOUNT_X, 3)
	
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	#�P�j��̊e�s�s�ŕt�r�_����ʔ������܂����I
	CyInterface().addImmediateMessage("&#36637;&#37341;&#22478;&#12398;&#21508;&#37117;&#24066;&#12391;&#20184;&#21930;&#31070;&#12364;&#22823;&#37327;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")

def processTEWITrap(pTrapUnit):
	pTeam = gc.getTeam( pTrapUnit.getTeam() )
	SpyList = checkUnit(pTrapUnit.getX(),pTrapUnit.getY(),RangeList1,gc.getInfoTypeForString('UNIT_SPY'),gc.getInfoTypeForString('UNIT_SPY'),2)
	UnitList = checkUnit(pTrapUnit.getX(),pTrapUnit.getY(),RangeList1,gc.getInfoTypeForString('UNIT_SANAE0'),gc.getInfoTypeForString('UNIT_GREAT_SPY'),2)
	SpyList2 = []
	UnitList2 = []
	for pSpy in SpyList:
		if pTeam.isAtWar(pSpy.getTeam()) and pSpy.getDamage()<100:
			SpyList2.append(pSpy)
	for pUnit2 in UnitList:
		if pTeam.isAtWar(pUnit2.getTeam()):
			UnitList2.append(pUnit2)
			
	#�X�p�C������΃X�p�C�ƈ��������Ƀg���b�v����
	if len(SpyList2) > 0:
		SpyList2[0].changeDamage(100,pTrapUnit.getOwner())
		pTrapUnit.changeDamage(100,pTrapUnit.getOwner())
		
		point = pTrapUnit.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
	#�X�p�C�����Ȃ��܂܃��j�b�g�����񂾂悤�Ȃ��
	elif len(UnitList2) > 0:
		changeDamage(RangeList1,pTrapUnit,0,20,0,True,False,False,True,-1,True,True,True,True,-1,False,0,4)
		pTrapUnit.changeDamage(100,pTrapUnit.getOwner())
		
		point = pTrapUnit.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

# �퓬�ł̃L�����V�[��
# pWinner�̎x�z����pLoser���L�����V�[�Ƃ��Đ�������
def initCombatKyonshii(pWinner, pLoser):
	RevivalUnit = pLoser.getUnitType()
	plotX = pWinner.getX()
	plotY = pWinner.getY()
	newUnit1 = gc.getPlayer(pWinner.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KYONSHII'),True)
	newUnit1.finishMoves()
	CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pLoser.getUnitType()).getDescription() + "&#12364;&#12461;&#12519;&#12531;&#12471;&#12540;&#12392;&#12375;&#12390;&#24489;&#27963;&#12375;&#12414;&#12375;&#12383;&#65281;","")

# �퓬�ł̐_�씭��
# pWinner�̎x�z���Ő_��𔭐�������
def initCombatShinrei(pWinner):
	iPlayer = pWinner.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iX = pWinner.getX()
	iY = pWinner.getY()
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")

# �v���C���[�ƃ��j�b�g�N���X�����炻�̃v���C���[�̃��j�b�gID���Ђ��ς�(UU���l������)
# �v���C���[��CyPlayer�ł�PyPlayer�ł��悢
def getCivilizationUnitType(player, sUnitClass):
	civinfo = gc.getCivilizationInfo( player.getID() )
	iUnitClass = gc.getInfoTypeForString(sUnitClass)
	return civinfo.getCivilizationUnits(iUnitClass)

# �s�s�ƃ��j�b�g�N���X�����w�肵�āA�s�s�̃I�[�i�[�̎x�z���Ń��j�b�g�𐶐�����
# �s�s��CyCity�ł�PyCity�ł��悢
def initCityUnit(city, sUnitClass):
	pyPlayer = PyHelpers.PyPlayer( city.getOwner() )
	pPlot = city.plot()
	iUnit = getCivilizationUnitType(pyPlayer, sUnitClass)
	
	pyPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY())

# �s�s�ƃ��j�b�g�����w�肵�āA�s�s�̃I�[�i�[�̎x�z���Ń��j�b�g�𐶐�����
# �s�s��CyCity�ł�PyCity�ł��悢
# UnitClass�ł��ق������낢��ƒׂ��������Ǝv���̂ňꉞ���x��
def initCityUnitDirect(city, sUnit):
	pyPlayer = PyHelpers.PyPlayer( city.getOwner() )
	pPlot = city.plot()
	iUnit = gc.getInfoTypeForString(sUnit)
	
	pyPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY())

##### </written by F> #####
