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

# デバッグ出力
def doprint(str):
	#cd sys.stderr.write(str)
	if not logInited:
		initLog()
	sys.stdout.write(str)
	sys.stdout.write("\n")
#	sys.stdout.flush()


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
				if sPromotion == 'PROMOTION_YORIHIME_SKILL1':
					return True
	return False



#ダメージ関数
#指定された範囲に設定された種類のユニットにダメージを与える プレイヤーやＡＩのみに効果があるか？　スペル耐性を貫通するかどうか？
#範囲はcasterからの相対パス　ダメージ上限と距離による補正
#ダメージを与える最大ユニット数？　回復もできるように？
#スタンドバイユニットには効果が出ないように
#iBorderは意味のない変数　引数が多すぎて呼び出す際にややこしくてしょうがなかったので、区切り文字代わりに
#bTrialCalcがTrueのときはダメージ量or回復量の合計を計算して返す
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

			#### 狙う種類のユニットでないなら飛ばす
			
			# 友好・中立・敵対
			bFlag = False 
			if bFriend and caster.getTeam() == pUnit.getTeam():
				bFlag = True
			if bNeutral and caster.getTeam() != pUnit.getTeam() and not pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if not bFlag:
				continue

			# プレイヤー・AI
			bFlag = False
			if pUnit.isHuman() and bPlayer:
				bFlag = True
			if not pUnit.isHuman() and bAI:
				bFlag = True
			if not bFlag:
				continue

			# 東方ユニット・一般兵
			bFlag = False
			if bToho and pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				bFlag = True
			elif bGeneral:
				bFlag = True
			if not bFlag:
				continue

			#### 追加の制約

			# むらさ用フラグなら 船舶ユニット以外は飛ばす
			if iSpecial == 5:
				if pUnit.getDomainType() != gc.getInfoTypeForString('DOMAIN_SEA'):
					continue
			
			#### ダメージ量の計算
			if minDamage == maxDamage:
				iDamage = minDamage
			elif minDamage >= 0: #ダメージのとき
				iDamage = minDamage + gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")
			else: #回復のとき
				iDamage = maxDamage - gc.getGame().getSorenRandNum((maxDamage - minDamage + 1), "Damage")

			#### 基礎ダメージへの追加の補正
			
			# めーりん用フラグなら
			if iSpecial == 2:
				iDamage -= pUnit.countAutoHeal()
			# えいき用フラグなら対象ユニットの経験値に比例したダメージ
			if iSpecial == 3:
				iDamage = int(pUnit.getExperience() * ( caster.countCardAttackLevel() * 0.1 + 1  ) )

			#### 補正
			
			# 弾幕耐性
			if not bAntiSpellBarrier:
				iDamage = (iDamage * (100 - pUnit.countSpellTolerance())) / 100
			
			# 距離による補正
			if iDistanceCorrect == 1:
				# ぱちぇスペカでしか使ってないかも
				# 使用者と対象者との距離をユークリッド距離で求める
				iDistance = math.sqrt(  (caster.getX()-pUnit.getX())**2 + (caster.getY()-pUnit.getY())**2 )
				iDamage = iDamage * (  ( math.sqrt( (caster.getLevel()**2) * 2) - iDistance  )  / math.sqrt( (caster.getLevel()**2) * 2)    )  
				iDamage = int(iDamage)

			# 割合ダメージ
			# 現HP * iDamage[%]
			if bPercent: 
				if minDamage >= 0: #ダメージのとき
					iDamage = (100 - pUnit.getDamage()) * iDamage/100
				else:
					iDamage = pUnit.getDamage() * iDamage / 100

			# ダメージ上限があるならそこで止まる
			if minDamage >= 0: #ダメージのとき
				if 100 - pUnit.getDamage() <= iLimitDamage:
					iDamage = 0
				elif 100 - pUnit.getDamage() - iDamage <= iLimitDamage:
					iDamage = 100 - pUnit.getDamage() - iLimitDamage
			else: #回復のとき
				if 100 - pUnit.getDamage() >= iLimitDamage:
					iDamage = 0
				elif 100 - pUnit.getDamage() - iDamage >= iLimitDamage:
					iDamage = 100 - pUnit.getDamage() - iLimitDamage

			ow = pUnit.getOwner()
			iTrialCalcNum += iDamage
			if not bTrialCalc:
				# 一度記憶する
				damageUnitList.append( [pUnit,iDamage] )
			
				# ダメージを与えるユニットへの追加の処理
				
				# 小町用フラグなら5Gを得る
				if iSpecial == 1: 
					if pUnit.getDamage() + iDamage >= 100:
						#caster.changeExperience(1,-1,False,False,False)
						gc.getPlayer(caster.getOwner()).changeGold(5)
	
	
	# 実際にはダメージを与えず総ダメージ量を返す
	if bTrialCalc:
		if iTrialCalcNum < 0:
			iTrialCalcNum = 0 - iTrialCalcNum
		return iTrialCalcNum
	
	# ダメージ第１弾
	damageCargoUnitList = []
	for item in damageUnitList:
		pUnit, iDamage = item
		if iLimitDamage <= 0 and pUnit.getCargo() > 0:
			# 上限なしで、ユニットを積載中なら後回し
			# 船を殺すと一緒に沈んだ乗員ユニットがヌルポるため
			damageCargoUnitList.append([pUnit,iDamage])
		else:
			pUnit.changeDamage(iDamage,caster.getOwner())
	
	# ダメージ第２弾、運搬ユニット用
	for item in damageCargoUnitList:
		item[0].changeDamage(item[1],caster.getOwner())
	
	
#昇進付与関数
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

			#### 狙う種類のユニットでないなら飛ばす

			# 友好・中立・敵対
			bFlag = False 
			if bFriend and caster.getTeam() == pUnit.getTeam():
				bFlag = True
			if bNeutral and caster.getTeam() != pUnit.getTeam() and not pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if bEnemy and caster.getTeam() != pUnit.getTeam() and pTeam.isAtWar(pUnit.getTeam()):
				bFlag = True
			if not bFlag:
				continue

			# プレイヤー・AI
			bFlag = False
			if pUnit.isHuman() and bPlayer:
				bFlag = True
			if not pUnit.isHuman() and bAI:
				bFlag = True
			if not bFlag:
				continue
			
			# 東方ユニット・一般兵
			bFlag = False
			if bToho and pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BOSS'):
				bFlag = True
			elif bGeneral:
				bFlag = True
			if not bFlag:
				continue

			#### 確率への補正
			iPer = iPercent
			
			# 弾幕耐性
			if bAntiSpellBarrier == False:
				iPer = (iPer * (100 - pUnit.countSpellTolerance())) / 100

			#### 追加の確率補正
			
			# レティPhanスペル用フラグなら
			# 雪原で3倍 ツンドラで2倍
			if iSpecial == 4: 
				if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
					iPer = iPer * 3
				if pUnit.plot().getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA'):
					iPer = iPer * 2

			#### サイコロを振って当たったなら
			if gc.getGame().getSorenRandNum(100, "spellcard cast") < iPer:
				# おりんPhanスペルなら
				
				if iSpecial == 3:
					if ( (gc.getInfoTypeForString('UNIT_CIRNO1') <= pUnit.getUnitType() and pUnit.getUnitType() <= gc.getInfoTypeForString('UNIT_CIRNO6')  ) or pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_GUN')  ):
						pUnit.setHasPromotion(iPromotion,bSet)
				else:
					pUnit.setHasPromotion(iPromotion,bSet)
					iUnitNum += 1

				#### 昇進を与えることに成功したユニットへの追加の処理

				# エフェクト？
				if onEffect == 1:
					point = pUnit.plot().getPoint()
					CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
					CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

				# レミリアPhanスペル用フラグなら
				# 眷属を持っていれば回復
				if iSpecial == 1: 
					if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_KENZOKU')):
						pUnit.changeDamage(-caster.countCardAttackLevel()/2,caster.getOwner())

				# ゆかりんスペカ用フラグなら
				# 弾幕結界を与えて1ターンの移動不可
				if iSpecial == 2: 
					pUnit.setDanmakuKekkai(0,caster.countCardAttackLevel()/4 + 1)
					pUnit.setImmobileTimer(1)
				# えいきスペカ用フラグなら行動終了
				if iSpecial == 5: 
					pUnit.finishMoves()
				# とよひめPhanスペル用フラグなら1ターンの移動不可
				if iSpecial == 6: 
					pUnit.setImmobileTimer(1)

				# 一時的な昇進が無くなるまで あと のべiTurnPromoターン
				if iTurnPromo > 0:
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
	for i in range(TohoCivList.iMaxPlayer):
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
				#東方叙事詩・統合MOD追記
				#スペルの処理変更に伴う処理変更@gforest_shade氏感謝
				#iNum = canSpellList[i][0]+5
				iNum = gc.getInfoTypeForString( Spells[ canSpellList[i][0] ].getName() )
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

	pTeam = gc.getTeam( gc.getPlayer(iPlayer).getTeam() )
	iNumTeam = gc.getMAX_CIV_TEAMS()
	for i in range(iNumTeam):
		ppTeam = gc.getTeam(i)
		if ppTeam.isBarbarian() == False:
			if pTeam.isAtWar(i):
				return True
	
	return False

# # # 東方叙事詩・統合MOD追記

def rangeListToPlotList(center, squareList):
	plotList = []
	for sq in squareList:
		iX = center.getX() + sq[0]
		iY = center.getY() + sq[1]
		if not isPlot(iX,iY):
			continue
		
		plotList.append( gc.getMap().plot(iX,iY) )
	
	return plotList

def plotListToRangeList(center, plotList):
	cx, cy = center.getX(), center.getY()
	return [[pPlot.getX()-cx, pPlot.getY()-cy] for pPlot in plotList]

def getPlotUnits(pPlot):
	return ( pPlot.getUnit(i) for i in range(pPlot.getNumUnits()) )

def getNumEnemies(pPlot, iFriendTeam):
	myTeam = gc.getTeam(iFriendTeam)
	return sum(1 for pUnit in getPlotUnits(pPlot) if myTeam.isAtWar(pUnit.getTeam()))

def getRangePlotList(center, i_range, include_center):
	"""
	中心から周囲nタイルのCyPlotのリストを返す
	center - 中心タイル
	i_range - 範囲
	include_center - Trueならリストに中心タイルを含める
	"""

	pMap = gc.getMap()
	result = []
	
	for xx in range(-i_range, i_range+1):
		for yy in range(-i_range, i_range+1):
			x = xx + center.getX()
			y = yy + center.getY()
			
			if not isValidPlot(x,y):
				continue
			if (xx == 0 and yy == 0) and not include_center:
				continue

			result.append( pMap.plot(x,y) )

	return result

def searchMaxEnemyPlot(lPlot, iFriendTeam):
	m = max( (getNumEnemies(pPlot, iFriendTeam), pPlot) for pPlot in lPlot )
	return m[1]


pickplot_callback = None
def pickPlot(callback):
	global pickplot_callback
	pickplot_callback = callback
	CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)



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



def terraformImprovementUpgrade(pPlot):
	"""
	テラフォーム予備改善を即時完了する
	できたらTrue, できなかったらFalseを返す
	"""
	
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


def improvementUpgrade(pPlot):
	"""
	地形改善を即時アップグレードする
	できたらTrue, できなかったらFalseを返す
	"""
	
	imprInfo = gc.getImprovementInfo( pPlot.getImprovementType() )
	iUpgrade = imprInfo.getImprovementUpgrade()
	
	if iUpgrade != -1:
		pPlot.setImprovementType(iUpgrade)
		return True

	return False

def copyPromotions(pSourceUnit, pDestinationUnit):
	"""
	昇進を別のユニットにコピーする
	pSourceUnit の持っている昇進すべてを pDestinationUnit に持たせる
	pSourceUnit の持っていない昇進はなにもしない pDestinationUnit から消すわけではない
	"""
	
	PromotionStart = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()
	PromotionEnd = gc.getNumCommandInfos()+InterfaceModeTypes.NUM_INTERFACEMODE_TYPES+gc.getNumBuildInfos()+gc.getNumPromotionInfos()
	PromotionNum = PromotionEnd - PromotionStart
	
	for iPromotion in range(PromotionNum):
		if pSourceUnit.isHasPromotion(iPromotion):
			pDestinationUnit.setHasPromotion(iPromotion,True)

	pDestinationUnit.setNumTurnPromo(pSourceUnit.getNumTurnPromo())

def uncivilize(pUnit):
	"""蛮族化"""
	
	BarBarianUnit = pUnit.getUnitType()
	plotX = pUnit.getX()
	plotY = pUnit.getY()
	iExperience = pUnit.getExperience()
	iLevel = pUnit.getLevel()
	
	#周囲１マスで空いてる場所を探す、なければ消滅
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
		
		#もともと持っていた昇進をそのまま移行させる
		copyPromotions(pUnit, newUnit1)
		
		newUnit1.finishMoves()

		# 嫉妬心からの蛮族化...かどうかはわからないが、持ってたら消す
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_EASY'),False)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_NORMAL'),False)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_HARD'),False)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHITTOSHIN_LUNATIC'),False)
		
		pUnit.changeDamage(100,pUnit.getOwner())
		

def worldspell_HYOUSEIRENGOU1(pPlayer, pPlot):
	"""
	氷精連合の世界魔法
	pPlayer の元にユニットが集まる(必ずしも氷精連合である必要はない)
	pPlot で発動エフェクトが発生する(必ずしもcaster.plot()である必要はない)
	"""
	
	#沸いてくるユニットと数は時代依存
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
	#妖精たちが結束を高め都市に集結しました
	CyInterface().addImmediateMessage("&#22934;&#31934;&#12383;&#12385;&#12364;&#32080;&#26463;&#12434;&#39640;&#12417;&#37117;&#24066;&#12395;&#38598;&#32080;&#12375;&#12414;&#12375;&#12383;","")

def worldspell_KISHINJOU1(pPlayer, pPlot):
	"""
	輝針城の世界魔法
	pPlayer の元に付喪神が沸く(必ずしも輝針城である必要はない)
	pPlot で発動エフェクトが発生する(必ずしもcaster.plot()である必要はない)
	"""
	
	# iPlayer = caster.getOwner()
	pTeam = gc.getTeam(pPlayer.getTeam())
	
	TAIKO = 1
	TYUUSEI = 2
	KINDAI = 4
	era = 0
	
	#時代によって沸かせるユニットや計算式を変動させる
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
			# 甲は2を超えず、乙は発生しない
			iNumKOU = pyCity.getPopulation() / iNumCityCountKOU
			iNumKOU = min(iNumKOU, 2)
			iNumOTU = 0
		
		elif era == TYUUSEI or era == KINDAI:
			# 甲乙とも1を下回らず、3を超えない
			iNumKOU = pyCity.getPopulation() / iNumCityCountKOU
			iNumKOU = max(1, iNumKOU)
			iNumKOU = min(iNumKOU, 3)

			iNumOTU = pyCity.getPopulation() / iNumCityCountOTU
			iNumOTU = max(1, iNumOTU)
			iNumOTU = min(iNumOTU, 3)

		else:
			# ここには来ないはずだが
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
	
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
	CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
	#輝針城の各都市で付喪神が大量発生しました！
	CyInterface().addImmediateMessage("&#36637;&#37341;&#22478;&#12398;&#21508;&#37117;&#24066;&#12391;&#20184;&#21930;&#31070;&#12364;&#22823;&#37327;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")

def processTEWITrap(pTrapUnit):
	"""てゐのトラップ処理"""
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
			
	#スパイが居ればスパイと引き換えにトラップ除去
	if len(SpyList2) > 0:
		SpyList2[0].changeDamage(100,pTrapUnit.getOwner())
		pTrapUnit.changeDamage(100,pTrapUnit.getOwner())
		
		point = pTrapUnit.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)
		
	#スパイが居ないままユニットが踏んだようならば
	elif len(UnitList2) > 0:
		changeDamage(RangeList1,pTrapUnit,0,20,0,True,False,False,True,-1,True,True,True,True,-1,False,0,4)
		pTrapUnit.changeDamage(100,pTrapUnit.getOwner())
		
		point = pTrapUnit.plot().getPoint()
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL'),point)
		CyAudioGame().Play3DSound("AS3D_spell_use",point.x,point.y,point.z)

def initCombatKyonshii(pWinner, pLoser):
	"""
	戦闘でのキョンシー化
	pWinnerの支配下でpLoserをキョンシーとして生成する
	"""
	
	RevivalUnit = pLoser.getUnitType()
	plotX = pWinner.getX()
	plotY = pWinner.getY()
	newUnit1 = gc.getPlayer(pWinner.getOwner()).initUnit(RevivalUnit, plotX, plotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KYONSHII'),True)
	newUnit1.finishMoves()
	CyInterface().addImmediateMessage(PyHelpers.PyInfo.UnitInfo(pLoser.getUnitType()).getDescription() + "&#12364;&#12461;&#12519;&#12531;&#12471;&#12540;&#12392;&#12375;&#12390;&#24489;&#27963;&#12375;&#12414;&#12375;&#12383;&#65281;","")

def initCombatShinrei(pWinner):
	"""
	戦闘での神霊発生
	pWinnerの支配下で神霊を発生させる
	"""
	
	iPlayer = pWinner.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iX = pWinner.getX()
	iY = pWinner.getY()
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHINREI'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	CyInterface().addImmediateMessage("&#31070;&#38666;&#12364;&#30330;&#29983;&#12375;&#12414;&#12375;&#12383;&#65281;","")

def getCivilizationUnitType(player, sUnitClass):
	"""
	プレイヤーとユニットクラス名からそのプレイヤーのユニットIDをひっぱる(UUを考慮する)
	プレイヤーはCyPlayerでもPyPlayerでもよい
	"""
	civinfo = gc.getCivilizationInfo( player.getID() )
	iUnitClass = gc.getInfoTypeForString(sUnitClass)
	return civinfo.getCivilizationUnits(iUnitClass)

def initCityUnit(city, sUnitClass):
	"""
	都市とユニットクラス名を指定して、都市のオーナーの支配下でユニットを生成する
	都市はCyCityでもPyCityでもよい
	"""
	pyPlayer = PyHelpers.PyPlayer( city.getOwner() )
	iUnit = getCivilizationUnitType(pyPlayer, sUnitClass)
	return pyPlayer.initUnit(iUnit, city.getX(), city.getY())

def initCityUnitDirect(city, sUnit):
	"""
	都市とユニット名を指定して、都市のオーナーの支配下でユニットを生成する
	都市はCyCityでもPyCityでもよい
	UnitClassでやるほうがいろいろと潰しがきくと思うので一応程度に
	"""
	pyPlayer = PyHelpers.PyPlayer( city.getOwner() )
	iUnit = gc.getInfoTypeForString(sUnit)
	return pyPlayer.initUnit(iUnit, city.getX(), city.getY())

##### </written by F> #####
