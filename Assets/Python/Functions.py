##### <written by F> #####
#自分使い用関数群

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import math
import SpellInfo

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

RangeList0 = [[0,0],]

RangeList1 = [	[-1,-1],[ 0,-1],[ 1,-1],
				[-1, 0],        [ 1, 0],
				[-1, 1],[ 0, 1],[ 1, 1], ]

#指定された場所が有効なplotであるかどうかを判別
#デフォのだとループ部分が上手くいかないので自前で実装
def isPlot(iX,iY):
	pMap = gc.getMap()
	iWidth = pMap.getGridWidth()
	iHeight = pMap.getGridHeight()
	
	#Xが有効範囲内かどうかチェック
	bFlagX = False
	if -1<iX and iX<iWidth:
		bFlagX = True
	else:
		if pMap.isWrapX():
			bFlagX = True
	
	#Yが有効範囲内かどうかチェック
	bFlagY = False
	if -1<iY and iY<iHeight:
		bFlagY = True
	else:
		if pMap.isWrapY():
			bFlagY = True
	
	if bFlagX and bFlagY:
		return True
	
	return False


#範囲内に指定されたユニットがいるかどうかをチェックする
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


#同スタックの味方東方ユニットを探してリストを返す
def searchTeamTohoUnit(pPlot,unit):
	UnitList=[]
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
			if unit.getTeam() == pUnit.getTeam():
				UnitList.append(pUnit)
	
	return UnitList



#スペカのreq関数の汎用関数
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

#スペルのreq関数の汎用関数
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
	return False



#ダメージ関数
#指定された範囲に設定された種類のユニットにダメージを与える プレイヤーやＡＩのみに効果があるか？　スペル耐性を貫通するかどうか？
#範囲はcasterからの相対パス　ダメージ上限と距離による補正
#ダメージを与える最大ユニット数？　回復もできるように？
#スタンドバイユニットには効果が出ないように
#iBorderは意味のない変数　引数が多すぎて呼び出す際にややこしくてしょうがなかったので、区切り文字代わりに
#bTrialCalcがTrueのときはダメージ量or回復量の合計を計算して返す
def changeDamage(squeaList,caster,minDamage,maxDamage,iLimitDamage,bPercent,bFriend,bNeutral,bEnemy,iBorder1,bToho,bGeneral,bPlayer,bAI,iBorder2,bAntiSpellBarrier,iDistanceCorrect,iSpecial=0,bTrialCalc = False,bSpell = False):
	iTrialCalcNum = 0
	damageUnitList = []
	
	for squea in squeaList:
		iX = caster.getX() + squea[0]
		iY = caster.getY() + squea[1]
		if isPlot(iX,iY):
			iNumKOTohoUnit = 0
			pPlot = gc.getMap().plot(iX,iY)
			for i in range(pPlot.getNumUnits()):
				if pPlot.getUnit(i+iNumKOTohoUnit).getDamage() >= 100:
					iNumKOTohoUnit = iNumKOTohoUnit + 1
				pUnit = pPlot.getUnit(i+iNumKOTohoUnit)
				pTeam = gc.getTeam(caster.getTeam())
				bFlag = False #ダメージを与える所属であるかどうかのチェック
				if bFriend and caster.getTeam() == pUnit.getTeam():
					bFlag = True
				if bNeutral and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == False:
					bFlag = True
				if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == True:
					bFlag = True
				if bFlag:
					bFlag = False
					if pUnit.isHuman() and bPlayer:
						bFlag = True
					if pUnit.isHuman() == False and bAI:
						bFlag = True
					
					if iSpecial == 5: #むらさ用　船舶ユニット以外には無効
						if pUnit.getDomainType() != gc.getInfoTypeForString('DOMAIN_SEA'):
							bFlag = False
					
					if bFlag:
						bFlag = False
						if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
							if bToho and pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
								bFlag = True
						else:
							if bGeneral:
								bFlag = True
								
						if bFlag: #ダメージ量の計算
							if minDamage == maxDamage:
								iDamage = minDamage
							else:
								if minDamage >= 0: #ダメージのとき
									iDamage = minDamage
									iDamage = iDamage + gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")
								else: #回復のとき
									iDamage = maxDamage
									iDamage = iDamage - gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")
							if iSpecial == 2: #めーりん用
								iDamage -= pUnit.countAutoHeal()
							if iSpecial == 3: #えいき用
								iDamage = int(pUnit.getExperience() * ( caster.countCardAttackLevel() * 0.1 + 1  ) )
							
							if bAntiSpellBarrier == False:
								iDamage = iDamage * (100 - countSpellTolerance(pUnit)) / 100
							
							#距離による補正
							if iDistanceCorrect == 1: #ぱちぇスペカ用
								#使用者と対象者との距離をユークリッド距離で求める
								iDistance = math.sqrt(  (caster.getX()-pUnit.getX())**2 + (caster.getY()-pUnit.getY())**2 )
								iDamage = iDamage * (  ( math.sqrt( (caster.getLevel()**2) * 2) - iDistance  )  / math.sqrt( (caster.getLevel()**2) * 2)    )  
								iDamage = int(iDamage)
								
							if bPercent: #割合ダメージかどうか
								if minDamage >= 0: #ダメージのとき
									iDamage = (100 - pUnit.getDamage()) * iDamage/100
								else:
									iDamage = pUnit.getDamage() * iDamage / 100
							
							if minDamage >= 0: #ダメージのとき
								if (100-pUnit.getDamage()) <= iLimitDamage:
									iDamage = 0
								if 100 - pUnit.getDamage() - iDamage <= iLimitDamage and (100-pUnit.getDamage()) >= iLimitDamage:
									iDamage = (100-pUnit.getDamage()) - iLimitDamage
							else: #回復のとき
								if (100-pUnit.getDamage()) >= iLimitDamage:
									iDamage = 0
								if 100 - pUnit.getDamage() - iDamage >= iLimitDamage and (100-pUnit.getDamage()) <= iLimitDamage:
									iDamage = (100-pUnit.getDamage()) - iLimitDamage
							
							if iSpecial == 4: #てゐトラップ用
								if gc.getGame().getSorenRandNum(100,"Tewi Trap") < 50:
									#pUnit.changeDamage(iDamage,caster.getOwner())
									damageUnitList.append( [pUnit,iDamage] )
							else:
								iTrialCalcNum = iTrialCalcNum + iDamage
								if bTrialCalc == False:
									#pUnit.changeDamage(iDamage,caster.getOwner())
									damageUnitList.append( [pUnit,iDamage] )
								
							if iSpecial == 1: #小町用
								if pUnit.getDamage() + iDamage >= 100:
									#caster.changeExperience(1,-1,False,False,False)
									gc.getPlayer(caster.getOwner()).changeGold(5)
	
	
	
	if bTrialCalc:
		if iTrialCalcNum < 0:
			iTrialCalcNum = 0 - iTrialCalcNum
		return iTrialCalcNum
	
	#実際のダメージ計算
	for item in damageUnitList:
		item[0].changeDamage(item[1],caster.getOwner())
	
	##casterへのPowerゲイン ダメージ系のときのみ
	#if minDamage >= 0 and maxDamage>=0:
	#	#統合MOD追記部分
	#	#小町スペルの場合、Powerは回復しないように
	#	if bFlag:
	#		if iSpecial == 1:
	#			iBase = 1
	#			caster.setPower( caster.getPower() + iBase  )
	#	
	#	#基準値の計算
	#		else:
	#			iBase = (minDamage + maxDamage)/2 * 30.0
	#			if bSpell:
	#				iBase = iBase * 5
	#			if iBase == 0:
	#				iBase = 1
	#			caster.setPower( caster.getPower() + ( 0.5 * iTrialCalcNum / iBase  )  )
	
	
#昇進付与関数
def setPromotion(squeaList,caster,sPromotion,bSet,iPercent,bFriend,bNeutral,bEnemy,iBorder1,bToho,bGeneral,bPlayer,bAI,iBorder2,bAntiSpellBarrier,onEffect=0,iSpecial=0,bGain=False,bSpell=False,iBorder3=0,iTurnPromo=0):
	iPromotion = gc.getInfoTypeForString(sPromotion)
	iUnitNum = 0
	for squea in squeaList:
		iX = caster.getX() + squea[0]
		iY = caster.getY() + squea[1]
		if isPlot(iX,iY):
			iNumKOTohoUnit = 0
			pPlot = gc.getMap().plot(iX,iY)
			for i in range(pPlot.getNumUnits()):
				if pPlot.getUnit(i+iNumKOTohoUnit).getDamage() >= 100:
					iNumKOTohoUnit = iNumKOTohoUnit + 1
				pUnit = pPlot.getUnit(i+iNumKOTohoUnit)
				pTeam = gc.getTeam(caster.getTeam())
				bFlag = False #昇進を与える所属であるかどうかのチェック
				if bFriend and caster.getTeam() == pUnit.getTeam():
					bFlag = True
				if bNeutral and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == False:
					bFlag = True
				if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()) == True:
					bFlag = True
				if bFlag:
					bFlag = False
					if pUnit.isHuman() and bPlayer:
						bFlag = True
					if pUnit.isHuman() == False and bAI:
						bFlag = True
					
					if bFlag:
						bFlag = False
						if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_STANDBY') or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
							if bToho and pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_STANDBY'):
								bFlag = True
						else:
							if bGeneral:
								bFlag = True

						if bFlag: #確率で昇進の付与or剥奪
							
							iPer = iPercent
							if bAntiSpellBarrier == False:
								iPer = iPercent * (100 - countSpellTolerance(pUnit)) / 100
							
							if iSpecial == 4: #レティPhanスペル用
								if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
									iPer = iPer * 3
								if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
									iPer = iPer * 2
							
							if gc.getGame().getSorenRandNum(100, "spellcard cast") < iPer:
								if iSpecial == 3: #おりんPhanスペル用
									if ( (gc.getInfoTypeForString('UNIT_CIRNO1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_CIRNO6')  ) or
										pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN')  ):
										pUnit.setHasPromotion(iPromotion,bSet)
								else:
									pUnit.setHasPromotion(iPromotion,bSet)
									iUnitNum = iUnitNum+1
								if onEffect == 1:
									point = pUnit.plot().getPoint()
									CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
									CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
								if iSpecial == 1: #レミリアPhanスペル用
									if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KENZOKU')):
										pUnit.changeDamage(-caster.countCardAttackLevel()/2,caster.getOwner())
								if iSpecial == 2: #ゆかりんスペカ用
									pUnit.setDanmakuKekkai(0,caster.countCardAttackLevel()/4 + 1)
									pUnit.setImmobileTimer(1)
								if iSpecial == 5: #えいきスペカ用
									pUnit.finishMoves()
								if iSpecial == 6: #とよひめPhanスペル用
									pUnit.setImmobileTimer(1)
								#東方叙事詩・統合MOD追記
								#ちなみに足したり引いたりで管理する方式を採用
								if iTurnPromo >= 0:
									pUnit.setNumTurnPromo( pUnit.getNumTurnPromo() + iTurnPromo )
	
	#casterへのPowerゲイン
	#この際だしいっそbGainは全てFalseにする？
	if bGain: 
		#基準値の計算
		iBase = iPercent * 30.0 / 100.0
		if bSpell:
			iBase = iBase * 5
		caster.setPower( caster.getPower() + ( 0.5 * iUnitNum / iBase  )  )


#弾幕耐性をカウント
def countSpellTolerance(pUnit):
	
	return pUnit.countSpellTolerance()

#AIの難易度補正を求める
def getHandicap():
	
	Handi = 0;
	for i in range(19):
		pPlayer = gc.getPlayer(i)
		if pPlayer.isHuman() == True:
			if Handi < pPlayer.getHandicapType():
				Handi = pPlayer.getHandicapType()
	return Handi


#AIのスペル使用
def AISpellCast(caster):
	
	CAL = caster.countCardAttackLevel()
	
	if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_AI_NOT_SPEL_CAST')):
		return False
	
	#AIによるスペカ使用
	
	Spells = SpellInfo.spells
	canSpellList = []
	
	#使用可能かつ評価０以上のスペルを抜き出し
	for i in range( len(Spells) ):
		Spell = Spells[i]
		if Spell.isVisible(caster) and Spell.isAbled(caster):
			EstimatePoint = Spell.estimate(caster) #評価値＝使用確率
			if EstimatePoint > 0:
			
				#Powerの残量や昇進ルートによって評価値を増減する
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
	
	#評価値で降順にソート
	for i in range( len(canSpellList) ):
		for j in range(i+1,len(canSpellList)):
			if canSpellList[i][1] < canSpellList[j][1]:
				temp = canSpellList[i]
				canSpellList[i] = canSpellList[j]
				canSpellList[j] = temp
	
	#評価値の高い順に使用判定
	for i in range(len(canSpellList)):
		if gc.getGame().getSorenRandNum(100,"AI Spell cast") < canSpellList[i][1]:
			if Spells[ canSpellList[i][0] ].cast(caster):
		
				iNum = canSpellList[i][0]+5
			#	if iNum <= gc.getInfoTypeForString("SPELLCARD_MIMIMIKO1_2"): #スペカであれば
				caster.setNumCastSpellCard( caster.getNumCastSpellCard() + 1 )
				if gc.getGame().isOption(gc.getInfoTypeForString('GAMEOPTION_MULTI')):
					caster.setNumSpellCardBreakTime( 2 )
				CyInterface().addImmediateMessage(gc.getUnitInfo(caster.getUnitType()).getDescription() + "&#12364;" + gc.getAutomateInfo(iNum).getDescription() + "&#12434;&#20351;&#29992;&#12375;&#12414;&#12375;&#12383;","")
				
				return True



	
#汎用復活関数(首都復活はここで扱わない)
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
	
	
	#もともと持っていた昇進をそのまま移行させる
	PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
	PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
	PromotionNum = PromotionEnd - PromotionStart
	
	for iPromotion in range(PromotionNum):
		if pKilledUnit.isHasPromotion(iPromotion):
			pRevivalUnit.setHasPromotion(iPromotion,True)



#ある文明が蛮族以外の文明と戦争状態にあるかどうかをチェック
def isWar(iPlayer):

	pTeam = gc.getTeam(iPlayer)
	iNumTeam = gc.getGame().countCivTeamsAlive() + gc.getGame().countCivTeamsEverAlive()
	for i in range(iNumTeam):
		ppTeam = gc.getTeam(i)
		if ppTeam.isBarbarian() == False:
			if pTeam.isAtWar(i):
				return True
	
	return False


### 全時限昇進のリスト
### NumTurnPromoはやっぱり「のべターン数」と思った方がするっと書ける気がするんだ
### ex. のこり1ターンが3個、残り5ターンが1個なら合計で8
### そう思う前提だと無いところから残り5ターンにするのは+5すればいいので簡単ですが、
### 残り1ターンを残り5ターンに戻したりするのとか面倒なので、いっそつけたい昇進だけ指定すれば
### 全部いいかんじにやってくれるのを目指してみる
### 確率式だったり外すときに追加の処理があったとしても気にせず入れてよい
### ほんとはこの手のリストはTohoUnitList.pyにあるべきですが、実験中なのでうんぬん
TurnPromotions = [
	['', 'PROMOTION_YATANOKAGAMI_TURN1', 'PROMOTION_YATANOKAGAMI_TURN2', 'PROMOTION_YATANOKAGAMI_TURN3'],
]

# 時限式の昇進をセットする
# sPromo: の昇進をつける
# その際、時限昇進リストから残りターン数を読み取って、NumTurnPromoに足す
# 指定の昇進と同じ段の昇進をすでに持っている場合、持っているのを消して指定昇進にセットしなおす
# その際のターンの差分とかはよしなにやる
def setTurnPromotion(pUnit, sPromo):
	### リストから探して
	for tpl in TurnPromotions:
		for i in range(1, len(tpl)):
			if tpl[i] == sPromo:
				### おそうじして
				for j in range(1, len(tpl)):
					if pUnit.isHasPromotion(gc.getInfoTypeForString(tpl[j])):
						pUnit.setHasPromotion(gc.getInfoTypeForString(tpl[j]),False)
						pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() - j)
						### NumTurnPromoの解釈が「昇進の数」でないと不安なら代わりに
						### pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() - 1)
				### 足す
				pUnit.setHasPromotion(gc.getInfoTypeForString(tpl[i]),True)
				pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() + i)
				### NumTurnPromoの解釈が「昇進の数」でないと不安なら代わりに
				### pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() + 1)
				return True

### NumTurnPromoの解釈をどちらにするにせよ、ずらずらと同じ段の判定をしなくてよくなるので
### わざわざ関数を経由する意義はそれなりにありそうな気がする


# 昇進のターンを減らす
# spPromo: 移動元の昇進名　を持っているなら
# iPer: の確率で(sRand: によって発生した乱数で)
# かつ beforeCallback: の条件を満たすなら
# snPromo: 移動先の昇進名(ここが空文字列なら単に消す)にかえて
# afterCallback: で指定されている後処理をして
# pUnit.NumTurnPromoを-1する(残りターン数の総和だと思っているので、ここは一律-1)
# 入れ替えが発生したらTrue、持ってなかったり確率に失敗したらFalseを返す
def changeTurnPromotion(pUnit, spPromo, snPromo, iPer=100, sRand="", beforeCallback=None, afterCallback=None):
	### もろもろの条件を満たすなら
	if pUnit.isHasPromotion(gc.getInfoTypeForString(spPromo)) and \
	   (iPer >= 100 or gc.getGame().getSorenRandNum(100, sRand) < iPer) and \
	   (beforeCallback is None or beforeCallback(pUnit)):
		### 昇進をかえて
		pUnit.setHasPromotion(gc.getInfoTypeForString(spPromo),False)
		if snPromo != "": pUnit.setHasPromotion(gc.getInfoTypeForString(snPromo),True)

		### 後処理が指定されていればやる
		if afterCallback is not None: afterCallback(pUnit)

		### decrement
		pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() - 1)
		### 昇進の数でないと不安なら代わりに
		### if snPromo == "": pUnit.setNumTurnPromo(pUnit.getNumTurnPromo() - 1)
		###
		### NumTurnPromoの解釈としてこっちを採用する場合でも移動先として空文字列が指定されたかどうかを自動判定するので
		### 自分で-1する手間くらいは省けるかもしれない...ですが、やっぱりつける方はともかく減らす方の便利関数の存在意義は
		### 微妙かもしれない
		return True
	
	return False


# 確定時限昇進のリスト
### ターンごとに確定で一個左にずれる類の昇進のためのリスト
### ほんとはこの手のリストはTohoUnitList.pyにあるべきですが(ry
### 減らす方もこのリスト化までやればそれなりにらくちんになるので、やるならここまでやるべきかも
DeterminateTurnPromotions = [
	['', 'PROMOTION_YATANOKAGAMI_TURN1', 'PROMOTION_YATANOKAGAMI_TURN2', 'PROMOTION_YATANOKAGAMI_TURN3'],
]


# 各確定時限昇進をいっこ左にずらす
# TURN1の次には消えてほしいので、リストの一番左には空文字列を入れている
# (see changeTurnPromotion.snPromoが空文字列のとき)
def changeDeterminateTurnPromotions(pUnit):
	bFound = False
	### リストから探して
	for p in DeterminateTurnPromotions:
		for i in range(1, len(p)):
			if pUnit.isHasPromotion(gc.getInfoTypeForString(p[i])):
				### ずらす
				changeTurnPromotion(pUnit, p[i], p[i-1])
				bFound = True
				break
	return bFound

##### 確率時限昇進もリスト化するならこんな感じかなあ(未テスト)
#
# # 確率時限昇進のリスト
# ### ターンごとに確率で消える類の昇進のためのリスト
# ### ほんとはこの手のリストはTohoUnitList.pyに(ry
# ProbableTurnPromotions = [
# 	['PROMOTION_KURAYAMI', 20],
# ]
#
#
# # 各確率時限昇進を消す
# def changeProbableTurnPromotions(pUnit):
# 	bFound = False
# 	### リストの中で当てはまるのがあったら
# 	for p in ProbableTurnPromotions:
# 		if pUnit.isHasPromotion(gc.getInfoTypeForString(p[0])):
# 			### 消そうと試みる(確率判定は関数の中で)
# 			changeTurnPromotion(pUnit, p[0], '', p[1], "remove kakuritsu")
# 			bFound = True
# 			break
# 	return bFound
##########################################################

##### </written by F> #####
