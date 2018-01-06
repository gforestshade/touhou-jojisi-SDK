# Civics functions for Revolution Mod
#
# by jdog5000
# Version 1.5

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import pickle
# --------- Revolution mod -------------
import RevDefs
import RevData
import SdToolKitAdvanced
import RevInstances


# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
game = CyGame()
localText = CyTranslator()

LOG_DEBUG = True

# civicsList[0] is a list of all civics of option type 0
civicsList = list()


def initCivicsList( ) :

    CvUtil.pyPrint("  Rev - Initializing Civics List")

    global civicsList

    for i in range(0,gc.getNumCivicOptionInfos()) :
        civicsList.append(list())

    for i in range(0,gc.getNumCivicInfos()) :
        civicInfo = gc.getCivicInfo(i)
        civicsList[civicInfo.getCivicOptionType()].append(i)


########################## Civics effect helper functions #####################


def getCivicsRevIdxLocal( iPlayer ) :

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() ) :
        return [0,list(),list()]

    if( pPlayer.getNumCities() == 0 ) :
        return [0,list(),list()]

    if( len(civicsList) < gc.getNumCivicOptionInfos() ) :
        initCivicsList()

    localRevIdx = 0
    posList = list()
    negList = list()

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            civicEffect = civicInfo.getRevIdxLocal()

            # Effect doubles for some when a much better alternative exists
            if( civicEffect > 0 and civicInfo.getRevLaborFreedom() < -1 ) :
                for j in civicsList[civicInfo.getCivicOptionType()] :
                    if( pPlayer.canDoCivics(j) ) :
                        jInfo = gc.getCivicInfo(j)
                        if( jInfo.getRevLaborFreedom() > 1 ) :
                            civicEffect = 2*civicEffect
                            #CvUtil.pyPrint("  Rev - Effect of %s doubled to %d because can do %s"%(civicInfo.getDescription(),civicEffect,jInfo.getDescription()))
                            break

            if( civicEffect > 0 and civicInfo.getRevDemocracyLevel() < -1 ) :
                for j in civicsList[civicInfo.getCivicOptionType()] :
                    if( pPlayer.canDoCivics(j) ) :
                        jInfo = gc.getCivicInfo(j)
                        if( jInfo.getRevDemocracyLevel() > 1 ) :
                            civicEffect = 2*civicEffect
                            #CvUtil.pyPrint("  Rev - Effect of %s doubled to %d because can do %s"%(civicInfo.getDescription(),civicEffect,jInfo.getDescription()))
                            break

            if( civicEffect > 0 ) :
                negList.append( (civicEffect, civicInfo.getDescription()) )
            elif( civicEffect < 0 ) :
                posList.append( (civicEffect, civicInfo.getDescription()) )

            #CvUtil.pyPrint("  Rev - %s local effect: %d"%(civicInfo.getDescription(),civicEffect))

            localRevIdx += civicEffect

    return [localRevIdx,posList,negList]

def getCivicsRevIdxNational( iPlayer ) :

    pPlayer = gc.getPlayer(iPlayer)
    
    revIdx = 0
    posList = list()
    negList = list()

    if( pPlayer.isNone() ) :
        return [revIdx,posList,negList]

    if( pPlayer.getNumCities() == 0 ) :
        return [revIdx,posList,negList]

    if( len(civicsList) < gc.getNumCivicOptionInfos() ) :
        initCivicsList()

    revIdx = 0
    posList = list()
    negList = list()

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            civicEffect = -civicInfo.getRevIdxNational()

            # Effect doubles for some when a much better alternative exists
            if( civicEffect < 0 and civicInfo.getRevLaborFreedom() < -1 ) :
                for j in civicsList[civicInfo.getCivicOptionType()] :
                    if( pPlayer.canDoCivics(j) ) :
                        jInfo = gc.getCivicInfo(j)
                        if( jInfo.getRevLaborFreedom() > 1 ) :
                            civicEffect = 2*civicEffect
                            #CvUtil.pyPrint("  Rev - Effect of %d doubled to %d because can do %s"%(civicInfo.getDescription(),civicEffect,jInfo.getDescription()))
                            break

            if( civicEffect < 0 and civicInfo.getRevDemocracyLevel() < -1 ) :
                for j in civicsList[civicInfo.getCivicOptionType()] :
                    if( pPlayer.canDoCivics(j) ) :
                        jInfo = gc.getCivicInfo(j)
                        if( jInfo.getRevDemocracyLevel() > 1 ) :
                            civicEffect = 2*civicEffect
                            #CvUtil.pyPrint("  Rev - Effect of %d doubled to %d because can do %s"%(civicInfo.getDescription(),civicEffect,jInfo.getDescription()))
                            break

            if( civicEffect > 0 ) :
                posList.append( (civicEffect, civicInfo.getDescription()) )
            elif( civicEffect < 0 ) :
                negList.append( (civicEffect, civicInfo.getDescription()) )

            #CvUtil.pyPrint("  Rev - %s local effect: %d"%(civicInfo.getDescription(),civicEffect))

            revIdx += civicEffect

    return [revIdx,posList,negList]

def getCivicsHolyCityEffects( iPlayer ) :

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() ) :
        return [0,0]

    if( pPlayer.getNumCities() == 0 ) :
        return [0,0]

    goodEffect = 0
    badEffect = 0

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            goodEffect += civicInfo.getRevIdxHolyCityGood()
            badEffect += civicInfo.getRevIdxHolyCityBad()

    return [goodEffect,badEffect]

def getCivicsReligionMods( iPlayer ) :

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() ) :
        return [0,0]

    if( pPlayer.getNumCities() == 0 ) :
        return [0,0]

    goodMod = 0
    badMod = 0

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            goodMod += civicInfo.getRevIdxGoodReligionMod()
            badMod += civicInfo.getRevIdxBadReligionMod()

    return [goodMod,badMod]

def getCivicsDistanceMod( iPlayer ) :

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() ) :
        return 0

    if( pPlayer.getNumCities() == 0 ) :
        return 0

    distMod = 0

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            distMod += civicInfo.getRevIdxDistanceMod()

    return distMod

def getCivicsNationalityMod( iPlayer ) :

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() ) :
        return 0

    if( pPlayer.getNumCities() == 0 ) :
        return 0

    natMod = 0

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            natMod += civicInfo.getRevIdxNationalityMod()

    return natMod

def getCivicsViolentRevMod( iPlayer ) :

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() ) :
        return 0

    if( pPlayer.getNumCities() == 0 ) :
        return 0

    vioMod = 0

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            vioMod += civicInfo.getRevIdxNationalityMod()

    return vioMod

def canDoCommunism( iPlayer ) :
    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return [False,None]

    for i in range(0,gc.getNumCivicInfos()) :
        civicInfo = gc.getCivicInfo(i)
        if( civicInfo.IsCommunism() and pPlayer.canDoCivics(i) ) :
            if( not pPlayer.isCivic(i) ) :
                return [True,i]

    return [False,None]

def isCommunism( iPlayer ) :
    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return False

    for i in range(0,gc.getNumCivicInfos()) :
        civicInfo = gc.getCivicInfo(i)
        if( civicInfo.IsCommunism() and pPlayer.isCivic(i) ) :
                return True

    return False

def canDoFreeSpeech( iPlayer ) :
    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return [False,None]

    for i in range(0,gc.getNumCivicInfos()) :
        civicInfo = gc.getCivicInfo(i)
        if( civicInfo.IsFreeSpeech() and pPlayer.canDoCivics(i) ) :
            if( not pPlayer.isCivic(i) ) :
                return [True,i]

    return [False,None]

def isFreeSpeech( iPlayer ) :
    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return False

    for i in range(0,gc.getNumCivicInfos()) :
        civicInfo = gc.getCivicInfo(i)
        if( civicInfo.IsFreeSpeech() and pPlayer.isCivic(i) ) :
                return True

    return False

def isCanDoElections( iPlayer ) :
    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() or pPlayer.isBarbarian() ) :
        return False

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            if( civicInfo.IsCanDoElection() ) :
                return True


    return False

def getReligiousFreedom( iPlayer ) :
    # Returns [freedom level, option type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return [0,None]

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            if( not civicInfo.getRevReligiousFreedom() == 0 ) :
                return [civicInfo.getRevReligiousFreedom(),i]

    return [0,None]


def getBestReligiousFreedom( iPlayer, relOptionType ) :
    # Returns [best level, civic type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() or relOptionType == None ) :
        return [0,None]

    bestFreedom = -11
    bestCivic = None

    for i in civicsList[relOptionType] :
        civicInfo = gc.getCivicInfo(i)
        civicFreedom = civicInfo.getRevReligiousFreedom()
        if( pPlayer.canDoCivics(i) and not civicFreedom == 0 ) :
            if( civicInfo.getRevReligiousFreedom() > bestFreedom ) :
                bestFreedom = civicFreedom
                bestCivic = i

    return [bestFreedom, bestCivic]

def getDemocracyLevel( iPlayer ) :
    # Returns [level, option type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return [0,None]

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            if( not civicInfo.getRevDemocracyLevel() == 0 ) :
                return [civicInfo.getRevDemocracyLevel(),i]

    return [0,None]


def getBestDemocracyLevel( iPlayer, optionType ) :
    # Returns [best level, civic type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() or optionType == None ) :
        return [0,None]

    bestLevel = -11
    bestCivic = None

    for i in civicsList[optionType] :
        civicInfo = gc.getCivicInfo(i)
        civicLevel = civicInfo.getRevDemocracyLevel()
        if( pPlayer.canDoCivics(i) and not civicLevel == 0 ) :
            if( civicLevel > bestLevel ) :
                bestLevel = civicLevel
                bestCivic = i

    return [bestLevel, bestCivic]

def getLaborFreedom( iPlayer ) :
    # Returns [level, option type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return [0,None]

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            if( not civicInfo.getRevLaborFreedom() == 0 ) :
                return [civicInfo.getRevLaborFreedom(),i]

    return [0,None]


def getBestLaborFreedom( iPlayer, optionType ) :
    # Returns [best level, civic type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() or optionType == None ) :
        return [0,None]

    bestLevel = -11
    bestCivic = None

    for i in civicsList[optionType] :
        civicInfo = gc.getCivicInfo(i)
        civicLevel = civicInfo.getRevLaborFreedom()
        if( pPlayer.canDoCivics(i) and not civicLevel == 0 ) :
            if( civicLevel > bestLevel ) :
                bestLevel = civicLevel
                bestCivic = i

    return [bestLevel, bestCivic]

def getEnvironmentalProtection( iPlayer ) :
    # Returns [level, option type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() ) :
        return [0,None]

    for i in range(0,gc.getNumCivicOptionInfos()) :
        iCivic = pPlayer.getCivics(i)
        if( iCivic >= 0 ) :
            civicInfo = gc.getCivicInfo(iCivic)
            if( not civicInfo.getRevEnvironmentalProtection() == 0 ) :
                return [civicInfo.getRevEnvironmentalProtection(),i]

    return [0,None]


def getBestEnvironmentalProtection( iPlayer, optionType ) :
    # Returns [best level, civic type]

    pPlayer = gc.getPlayer(iPlayer)

    if( pPlayer.isNone() or not pPlayer.isAlive() or optionType == None ) :
        return [0,None]

    bestLevel = -11
    bestCivic = None

    for i in civicsList[optionType] :
        civicInfo = gc.getCivicInfo(i)
        civicLevel = civicInfo.getRevEnvironmentalProtection()
        if( pPlayer.canDoCivics(i) and not civicLevel == 0 ) :
            if( civicLevel > bestLevel ) :
                bestLevel = civicLevel
                bestCivic = i

    return [bestLevel, bestCivic]