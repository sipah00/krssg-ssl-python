from tactic import Tactic
import time
import sys
from math import *

sys.path.append('../../../skills_py/scripts/skills')
sys.path.append('../../../plays_py/scripts/utils/')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '../../../navigation_py/scripts/navigation')


from geometry import * 
from math import *
from config import *
import skills_union
import sGoToBall
import sGoToPoint
import sDropBall

TARGET_AREA_RADIUS = 10

class TGoToFix(Tactic):
    def __init__(self, bot_id, state,  param=None):
        super(TGoToFix, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()
        

    def execute(self, state, pub):
        print "CHAL RAHA HAI"
        target = Vector2D(int(0),int(0))
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))

        MAXX = HALF_FIELD_MAXX / 2
        MAXY = HALF_FIELD_MAXY * 2  - (HALF_FIELD_MAXY * 2  - 8 * BOT_RADIUS) / 2
        MAXY = MAXY - BOT_RADIUS


        if ballPos.dist(target) < 150:
            self.sParam.GoToPointP.x = MAXX - 1.5 * BOT_RADIUS
            self.sParam.GoToPointP.y = 0
            self.sParam.GoToPointP.finalslope = pi
            self.sParam.GoToPointP.align = True
            sGoToPoint.execute(self.sParam, state, self.bot_id, pub)
            return
        
        if ballPos.dist(botPos) > 1 * BOT_BALL_THRESH:

            self.sParam.GoToBallP.intercept = False   #may be true
            sGoToBall.execute(self.sParam, state, self.bot_id, pub)
            return 

        else:

            self.sParam.sDropBall.x = target.x
            self.sParam.sDropBall.y = target.y
            sDropBall.execute(self.sParam, state, self.bot_id, pub)
            return

    def isComplete(self, state):

        if ballPos.intersects(target, TARGET_AREA_RADIUS):
            return True
        else:
            return False

    def updateParams(self, state):
        # No parameter to update here
        pass        