# RevolutionInit.py
#
# by jdog5000
# Version 2.2

# This file should be imported into CvCustomEventManager and the
# __init__ function then called from the event handler initilization
# spot using:
#
# RevolutionInit.RevolutionInit( self, configFileName )
#
# where configFileName is nominally "Revolution.ini".

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup as PyPopup
import CvConfigParser
import CvModName
import CvPath
# --------- Revolution mod -------------
import RevDefs
#import RevEvents
#import BarbarianCiv
import AIAutoPlay
#import ChangePlayer
#import Revolution
#import Tester
#import TechDiffusion
#import DynamicCivNames
import RevInstances

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
game = CyGame()
localText = CyTranslator()

class RevolutionInit :

    def __init__( self, customEM, configFileName = None ) :
        
        CvUtil.pyPrint("Initializing Revolution Mod")

        self.EventKeyDown = 6
        self.customEM = customEM
        self.configFileName = configFileName

        config = CvConfigParser.CvConfigParser(configFileName)
        self.config = config

        self.bFoundConfig = config.getboolean("RevConfig", "FoundConfig", False)
        self.bShowActivePopup = config.getboolean("RevConfig", "ActivePopup", True)
        
        self.revComponentsText = ""

        customEM.addEventHandler( "kbdEvent", self.onKbdEvent )
        customEM.addEventHandler( 'GameStart', self.onGameStart )
        customEM.addEventHandler( 'OnLoad', self.onGameLoad )
        #customEM.addEventHandler( 'Init', self.onInit )
        
        # Determine if game is already running and Python has just been reloaded
        if( game.isFinalInitialized() ) :
            #print "Game initialized!"
            self.onGameLoad( None, bShowPopup = False )



    def onKbdEvent(self, argsList ):
        'keypress handler'
        eventType,key,mx,my,px,py = argsList

        if ( eventType == RevDefs.EventKeyDown ):
            theKey=int(key)

            # For debug or trial only
            if( theKey == int(InputTypes.KB_Q) and self.customEM.bShift and self.customEM.bCtrl ) :
                self.showActivePopup()

    def onInit( self, argsList ) :
        print "Init fired"
    
    def onGameStart( self, argsList ) :
        
        print "Gaming starting now"
        
        self.onGameLoad( None )

    def onGameLoad( self, argsList, bForceReinit = False, bShowPopup = True ) :
        
        # Remove any running mod components
        bDoUnInit = (bForceReinit or RevInstances.bIsInitialized)
        bDoInit = (bDoUnInit or not RevInstances.bIsInitialized)
        
        if( bDoUnInit ) :
            print "PY:  Uninitializing Revolution Mod components"
            
            if( not RevInstances.AIAutoPlayInst == None ) :
                RevInstances.AIAutoPlayInst.removeEventHandlers()
                RevInstances.AIAutoPlayInst = None
            
            RevInstances.bIsInitialized = False
        
        # Initialize mod components
        if( bDoInit ) :
            print "PY:  Initializing Revolution Mod components"
            RevInstances.bIsInitialized = True

        revComponentsText = "AIAutoPlay mod running with the following components: <color=0,255,0,255>on<color=255,255,255,255>/<color=255,0,0,255>off\n"

        if( self.config.getboolean("AIAutoPlay", "Enable", True) ) :
            if( bDoInit ) : RevInstances.AIAutoPlayInst = AIAutoPlay.AIAutoPlay(self.customEM, self.config)
            revComponentsText += "<color=0,255,0,255>" + "\nAIAutoPlay"
        else :
            revComponentsText += "<color=255,0,0,255>" + "\nAIAutoPlay"
        
        revComponentsText += "<color=255,255,255,255>"
        self.revComponentsText = revComponentsText
        
        if( bShowPopup and self.bShowActivePopup ) :
            self.showActivePopup()
        
        if( not self.bFoundConfig ) :
            popup = PyPopup.PyPopup( )
            bodStr = "WARNING:  " + self.configFileName + " not found!  Revolution components using default settings."
            bodStr += "  Check mod installation directory, should be:\n\n" + CvPath.installActiveModDir
            bodStr += "\n\nOr:\n\n" + CvPath.userActiveModDir
            popup.setBodyString( bodStr )
            popup.launch()
        
        if( bDoInit ) :
            CyInterface().setDirty( InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True )
            CyInterface().setDirty( InterfaceDirtyBits.CityScreen_DIRTY_BIT, True )
            CyInterface().setDirty( InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True )
    
    def showActivePopup( self ) :
    
        # Display popups showing configuration of Revolution mod        
        bodStr = self.revComponentsText

        bodStr += "\n\nMax civs in DLL: %d"%(gc.getMAX_CIV_PLAYERS())
        bodStr += "\nTurns in game: %d"%(game.getMaxTurns())
        bodStr += "\nDefault num players: %d"%(gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers())

        popup = PyPopup.PyPopup( )
        popup.setBodyString( bodStr )
        popup.launch()

