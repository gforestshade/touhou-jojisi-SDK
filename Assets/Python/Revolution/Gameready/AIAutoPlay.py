# AI_AUTO_PLAY_MOD
#
# by jdog5000
# version 2.0

from CvPythonExtensions import *
import CvScreenEnums
import CvTopCivs
import CvUtil
import PyHelpers
import Popup as PyPopup
# --------- Revolution mod -------------
import RevDefs
import SdToolKitAdvanced
import RevUtils
##### <written by F> #####
import TohoUnitList
import Functions
import SpellInfo

import math
import CvGameUtils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
game = CyGame()
localText = CyTranslator()

class AIAutoPlay :

    def __init__(self, customEM, config = None ) :

        print "Initializing AIAutoPlay Mod"

        self.LOG_DEBUG = False
        self.SHOW_NEW_LEADER_POPUP = True
        self.blockPopups = True
        self.refortify = True
        self.bSaveAllDeaths = True

        if( not config == None ) :
            self.LOG_DEBUG = config.getboolean("AIAutoPlay", "DebugMode", self.LOG_DEBUG)
            self.SHOW_NEW_LEADER_POPUP = config.getboolean("AIAutoPlay", "ShowNewLeaderPopup", self.SHOW_NEW_LEADER_POPUP)
            self.blockPopups = config.getboolean("AIAutoPlay", "BlockPopups", self.blockPopups)
            self.refortify = config.getboolean("AIAutoPlay", "Refortify", self.refortify)
            self.bSaveAllDeaths = config.getboolean("AIAutoPlay", "SaveAllDeaths", self.bSaveAllDeaths)

        self.TurnsToAuto = 10

        self.playerID = 0
        self.AutoCounter = 0

        self.AutoTypes={
            0 : localText.getText("TXT_KEY_AIAUTOPLAY_NO", ()),
            1 : localText.getText("TXT_KEY_AIAUTOPLAY_FULLY", ()),
            #2 : localText.getText("TXT_KEY_AIAUTOPLAY_UNIT", ()),
            #3 : localText.getText("TXT_KEY_AIAUTOPLAY_DEBUG", ()),
            }

        self.customEM = customEM

        self.customEM.addEventHandler( "kbdEvent", self.onKbdEvent )
#        self.customEM.addEventHandler( "EndGameTurn", self.onEndGameTurn )
#        self.customEM.addEventHandler( 'BeginPlayerTurn', self.onBeginPlayerTurn )
#        self.customEM.addEventHandler( 'EndPlayerTurn', self.onEndPlayerTurn )
#        self.customEM.addEventHandler( 'OnLoad', self.onGameLoad )
#        self.customEM.addEventHandler( 'GameStart', self.onGameStart )
#        self.customEM.addEventHandler( 'victory', self.onVictory )

        self.customEM.setPopupHandler( RevDefs.toAIChooserPopup, ["toAIChooserPopup",self.AIChooserHandler,self.blankHandler] )
        self.customEM.setPopupHandler( RevDefs.abdicatePopup, ["abdicatePopup",self.abdicateHandler,self.blankHandler] )
        self.customEM.setPopupHandler( RevDefs.pickHumanPopup, ["pickHumanPopup",self.pickHumanHandler,self.blankHandler] )

#        if( self.blockPopups ) :
#            print "Removing some event handlers"
#            try :
#                self.customEM.removeEventHandler( "cityBuilt", customEM.onCityBuilt )
#                self.customEM.addEventHandler( "cityBuilt", self.onCityBuilt )
#            except ValueError :
#                print "Failed to remove 'onCityBuilt', perhaps not registered"
#                self.customEM.setEventHandler( "cityBuilt", self.onCityBuilt )
            
#            try :
#                self.customEM.removeEventHandler( "BeginGameTurn", customEM.onBeginGameTurn )
#                self.customEM.addEventHandler( "BeginGameTurn", self.onBeginGameTurn )
#            except ValueError :
#                print "Failed to remove 'onBeginGameTurn', perhaps not registered"
#                self.customEM.setEventHandler( "BeginGameTurn", self.onBeginGameTurn )


    def removeEventHandlers( self ) :
        print "Removing event handlers from AIAutoPlay"
        
        self.customEM.removeEventHandler( "kbdEvent", self.onKbdEvent )
#        self.customEM.removeEventHandler( "EndGameTurn", self.onEndGameTurn )
#        self.customEM.removeEventHandler( 'BeginPlayerTurn', self.onBeginPlayerTurn )
#        self.customEM.removeEventHandler( 'EndPlayerTurn', self.onEndPlayerTurn )
#        self.customEM.removeEventHandler( 'OnLoad', self.onGameLoad )
#        self.customEM.removeEventHandler( 'GameStart', self.onGameStart )
#        self.customEM.removeEventHandler( 'victory', self.onVictory )

#        self.customEM.setPopupHandler( RevDefs.toAIChooserPopup, ["toAIChooserPopup",self.blankHandler,self.blankHandler] )
#        self.customEM.setPopupHandler( RevDefs.abdicatePopup, ["abdicatePopup",self.blankHandler,self.blankHandler] )
#        self.customEM.setPopupHandler( RevDefs.pickHumanPopup, ["pickHumanPopup",self.blankHandler,self.blankHandler] )
        
#        if( self.blockPopups ) :
#            self.customEM.removeEventHandler( "cityBuilt", self.onCityBuilt )
#            self.customEM.addEventHandler( "cityBuilt", self.customEM.onCityBuilt )
            
#            self.customEM.removeEventHandler( "BeginGameTurn", self.onBeginGameTurn )
#            self.customEM.addEventHandler( "BeginGameTurn", self.customEM.onBeginGameTurn )
    
    def blankHandler( self, playerID, netUserData, popupReturn ) :
        # Dummy handler to take the second event for popup
        return


    def onGameStart( self, argsList ) :
        self.onGameLoad([])

    def onGameLoad( self, argsList ) :
        # Init things which require a game object or other game data to exist

        if( not SdToolKitAdvanced.sdObjectExists( "AIAutoPlay", game ) ) :
            SdToolKitAdvanced.sdObjectInit( "AIAutoPlay", game, {} )
            SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", True )
        elif( SdToolKitAdvanced.sdObjectGetVal( "AIAutoPlay", game, "bCanCancelAuto" ) == None ) :
            SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", True )

    def onVictory( self, argsList ) :
        self.checkPlayer()
        game.setAIAutoPlay(0)
        
    def onEndGameTurn( self, argsList ) :
        if( game.getAIAutoPlay() == 1 ) :
            # About to turn off automation
            #SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", False )
            pass

    def pickHumanHandler( self, iPlayerID, netUserData, popupReturn ) :

        CvUtil.pyPrint('Handling pick human popup')

        if( popupReturn.getButtonClicked() == 0 ):  # if you pressed cancel
            CyInterface().addImmediateMessage("Kill your remaining units if you'd like to see end game screens","")
            return

        toKillPlayer = gc.getActivePlayer()

        newHumanIdx = popupReturn.getSelectedPullDownValue( 1 )
        newPlayer = gc.getPlayer(newHumanIdx)

        # game.setActivePlayer( newHumanIdx, False )
        # newPlayer.setIsHuman(True)

        # CvUtil.pyPrint("You now control the %s"%(newPlayer.getCivilizationDescription(0)))
        # CyInterface().addImmediateMessage("You now control the %s"%(newPlayer.getCivilizationDescription(0)),"")
        
        RevUtils.changeHuman( newHumanIdx, toKillPlayer.getID() )

        if( toKillPlayer.getNumCities() == 0 ) :
            # Kills off the lion in the ice field
            CvUtil.pyPrint("Killing off player %d"%(toKillPlayer.getID()))
            toKillPlayer.killUnits()
            toKillPlayer.setIsHuman(False)
            #success = game.changePlayer( toKillPlayer.getID(), toKillPlayer.getCivilizationType(), toKillPlayer.getLeaderType(), -1, False, False )
            toKillPlayer.setNewPlayerAlive(False)
            toKillPlayer.setFoundedFirstCity(True)

    def onBeginPlayerTurn( self, argsList ) :
        iGameTurn, iPlayer = argsList

        if( game.getAIAutoPlay() == 1 and iPlayer > game.getActivePlayer() and gc.getActivePlayer().isAlive() ) :
            # Forces isHuman checks to come through positive for everything after human players turn

            self.checkPlayer()
            #SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", False )
            game.setAIAutoPlay(0)
        
        elif( self.bSaveAllDeaths ) :
            if( game.getAIAutoPlay() == 0 and not gc.getActivePlayer().isAlive() and iPlayer > game.getActivePlayer() ) :
                self.checkPlayer()
                #SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", False )
                game.setAIAutoPlay(0)

    def onEndPlayerTurn( self, argsList ) :
        iGameTurn, iPlayer = argsList

        # Can't use isHuman as isHuman has been deactivated by automation
        if( self.refortify and iPlayer == game.getActivePlayer() and game.getAIAutoPlay() == 1 ) :
            RevUtils.doRefortify( game.getActivePlayer() )
        
        if( iPlayer == gc.getBARBARIAN_PLAYER() and game.getAIAutoPlay() == 1 ) :
            # About to turn off automation
            #SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", False )
            #self.checkPlayer()
            pass

    def checkPlayer( self ) :
        
        pPlayer = gc.getActivePlayer()

        if( not pPlayer.isAlive() ) :
            # popup = PyPopup.PyPopup(RevDefs.pickHumanPopup,contextType = EventContextTypes.EVENTCONTEXT_ALL)
            # popup.setHeaderString( localText.getText("TXT_KEY_AIAUTOPLAY_PICK_CIV", ()) )
            # popup.setBodyString( localText.getText("TXT_KEY_AIAUTOPLAY_CIV_DIED", ()) )
            # popup.addSeparator()

            # popup.createPythonPullDown( localText.getText("TXT_KEY_AIAUTOPLAY_TAKE_CONTROL_CIV", ()), 1 )
            # for i in range(0,gc.getMAX_CIV_PLAYERS()) :
                # player = PyPlayer(i)
                # if( not player.isNone() and not i == pPlayer.getID() ) :
                    # if( player.isAlive() ) :
                        # popup.addPullDownString( localText.getText("TXT_KEY_AIAUTOPLAY_OF_THE", ())%(player.getName(),player.getCivilizationName()), i, 1 )

            # activePlayerIdx = gc.getActivePlayer().getID()
            # popup.popup.setSelectedPulldownID( activePlayerIdx, 1 )

            # popup.addSeparator()

            # popup.addButton( localText.getText("TXT_KEY_AIAUTOPLAY_NONE", ()) )
            # CvUtil.pyPrint('Launching pick human popup')
            # popup.launch()

            gc.getActivePlayer().setNewPlayerAlive( True )
            iSettler = CvUtil.findInfoTypeNum(gc.getUnitInfo,gc.getNumUnitInfos(),'UNIT_SETTLER')
            gc.getActivePlayer().initUnit( iSettler, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH )
            gc.getActivePlayer().setFoundedFirstCity( False )
            gc.getActivePlayer().setIsHuman( True )

        CvUtil.pyPrint('CDP: Setting autoplay to 0')
        game.setAIAutoPlay(0)
        
        if( not pPlayer.isHuman() ) :
            CvUtil.pyPrint('Returning human player to control of %s'%(pPlayer.getCivilizationDescription(0)))
            game.setActivePlayer( pPlayer.getID(), False )
            pPlayer.setIsHuman( True )

        #CvUtil.pyPrint('CDP: Setting autoplay to 1')
        #game.setAIAutoPlay(1)


    def onKbdEvent( self, argsList ) :
        'keypress handler'
        eventType,key,mx,my,px,py = argsList

        if ( eventType == RevDefs.EventKeyDown ):
            theKey=int(key)

            if( theKey == int(InputTypes.KB_X) and self.customEM.bShift and self.customEM.bCtrl ) :
                # Get it?  Shift ... control ... to the AI
                if( game.getAIAutoPlay() > 0 ) :
                    try :
                        bCanCancelAuto = SdToolKitAdvanced.sdObjectGetVal( "AIAutoPlay", game, "bCanCancelAuto" )
                        if( bCanCancelAuto is None ) :
                            bCanCancelAuto = True
                            SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", True )
                    except :
                        print "Error!  AIAutoPlay: Can't find bCanCancelAuto, assuming it would be True"
                        bCanCancelAuto = True

                    if( bCanCancelAuto ) :
                        if( self.refortify ) :
                            RevUtils.doRefortify( game.getActivePlayer() )
                        game.setAIAutoPlay( 0 )
                        self.checkPlayer()
                else :
                    self.toAIChooser()

            if( theKey == int(InputTypes.KB_M) and self.customEM.bShift and self.customEM.bCtrl ) :
                # Toggle auto moves
                if( self.LOG_DEBUG ) : CyInterface().addImmediateMessage("Moving your units...","")
                #self.playerID = gc.getActivePlayer().getID()
                game.setAIAutoPlay( 1 )

            if( theKey == int(InputTypes.KB_O) and self.customEM.bShift and self.customEM.bCtrl ) :
                RevUtils.doRefortify( game.getActivePlayer() )


    def onBeginGameTurn( self, argsList):
        'Called at the beginning of the end of each turn'
        iGameTurn = argsList[0]
        if( game.getAIAutoPlay() == 0 ) :
            CvTopCivs.CvTopCivs().turnChecker(iGameTurn)

    def onCityBuilt(self, argsList):
        'City Built'
        city = argsList[0]
        if (city.getOwner() == CyGame().getActivePlayer() and game.getAIAutoPlay() == 0 ):
                self.customEM.onCityBuilt(argsList)
        else :
                try :
                    CvUtil.pyPrint('City Built Event: %s' %(city.getName()))
                except :
                    CvUtil.pyPrint('City Built Event: Error processing city name' )


    def toAIChooser( self ) :
        'Chooser window for when user switches to AI auto play'

        screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
        xResolution = screen.getXResolution()
        yResolution = screen.getYResolution()
        popupSizeX = 400
        popupSizeY = 250

        popup = PyPopup.PyPopup(RevDefs.toAIChooserPopup,contextType = EventContextTypes.EVENTCONTEXT_ALL)
        popup.setPosition((xResolution - popupSizeX )/2, (yResolution-popupSizeY)/2-50)
        popup.setSize(popupSizeX,popupSizeY)
        popup.setHeaderString( localText.getText("TXT_KEY_AIAUTOPLAY_TURN_ON", ()) )
        popup.setBodyString( localText.getText("TXT_KEY_AIAUTOPLAY_TURNS", ()) )
        popup.addSeparator()
        popup.createPythonEditBox( '10', 'Number of turns to turn over to AI', 0)
        popup.setEditBoxMaxCharCount( 4, 2, 0 )

        

        popup.createPythonPullDown( localText.getText("TXT_KEY_AIAUTOPLAY_AUTOMATION", ()), 2 )
        for i in range(0,len(self.AutoTypes)) :
            popup.addPullDownString( self.AutoTypes[i], i, 2 )

        popup.popup.setSelectedPulldownID( 1, 2 )

        #popup.createPythonCheckBoxes( 4, 3 )
        #popup.setPythonCheckBoxText( 0, 'Pause at turn end', 'Pauses automation at the end of the turn, so you can inspect things', 3 )
        #popup.setPythonCheckBoxText( 1, 'Pause every 10', 'Pauses automation every 10 turns', 3 )
        #popup.setPythonCheckBoxText( 2, 'Cancel on war declared', 'Cancel automation if your civ becomes involved in a war', 3 )
        #popup.setPythonCheckBoxText( 3, 'Wake-up on game end', 'If someone (your civ?) wins, automation cancelled', 3 )

        popup.addSeparator()
        popup.addButton("OK")
        popup.addButton(localText.getText("TXT_KEY_AIAUTOPLAY_CANCEL", ()))

        popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

    def AIChooserHandler( self, playerID, netUserData, popupReturn ) :
        'Handles AIChooser popup'
        if( popupReturn.getButtonClicked() == 1 ):  # if you pressed cancel
            return

        numTurns = 0
        self.playerID = playerID
        if( popupReturn.getEditBoxString(0) != '' ) :
            numTurns = int( popupReturn.getEditBoxString(0) )

        autoIdx = popupReturn.getSelectedPullDownValue( 2 )

        if( autoIdx == 0 ) :
            if( self.LOG_DEBUG ) : CyInterface().addImmediateMessage("Clearing all automation","")
            #self.clearAllAutomation( )
        elif( autoIdx == 1 ) :
            if( numTurns > 0 ) :
                if( self.LOG_DEBUG ) : CyInterface().addImmediateMessage("Fully automating for %d turns"%(numTurns),"")
                self.abdicate( numTurns = numTurns, voluntary = True )
        elif( autoIdx == 2 and numTurns > 0 ) :
            if( self.LOG_DEBUG ) : CyInterface().addImmediateMessage("Auto Move","")
            self.setAutoMoves( numTurns )
        elif( autoIdx == 3 and numTurns > 0 ) :
            if( self.LOG_DEBUG ) : CyInterface().addImmediateMessage("Debug Mode","")
            self.setDebugMode( numTurns )

        # How to read out checkboxes?  popupReturn doesn't seem to have a function
        #bitField = popupReturn.getCheckBoxBitfield( 3 )
        #self.bPause =
        #CyInterface().addImmediateMessage("bitfieldsize: %d"%(len(bitField)),"")

    def abdicate( self, numTurns = -1, voluntary = False ) :
        'Turn over control to the AI'
        if( numTurns > 0 ) :
            self.TurnsToAuto = numTurns

        if( self.TurnsToAuto < 1 ) :
            return

        if( voluntary and self.SHOW_NEW_LEADER_POPUP ) :
            popup = PyPopup.PyPopup(RevDefs.abdicatePopup,contextType = EventContextTypes.EVENTCONTEXT_ALL)
            popup.setHeaderString( localText.getText("TXT_KEY_AIAUTOPLAY_NEW_LEADER", ()) )
            if( voluntary ) :
                bodStr = localText.getText("TXT_KEY_AIAUTOPLAY_ABDICATE", ())
            else :
                bodStr = localText.getText("TXT_KEY_AIAUTOPLAY_USURPATOR", ())
            bodStr = bodStr +  localText.getText("TXT_KEY_AIAUTOPLAY_GOOD_NEWS", ()) %(self.TurnsToAuto)
            popup.setBodyString( bodStr )
            popup.launch()
        else :
            if( voluntary ) : SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", True )
            game.setAIAutoPlay( self.TurnsToAuto )

    def abdicateHandler( self, playerID, netUserData, popupReturn ) :
        'Handle abdicate popup'
        SdToolKitAdvanced.sdObjectSetVal( "AIAutoPlay", game, "bCanCancelAuto", True )
        game.setAIAutoPlay( self.TurnsToAuto )
