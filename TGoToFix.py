from tactic import Tactic
import time
import sys
from math import *

sys.path.append('../../../skills_py/scripts/skills')
sys.path.append('../../../plays_py/scripts/utils/')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '../../../navigation_py/scripts/navigation')
from config import *

from geometry import * 
from math import *
import skills_union
import sGoToBall
import sGoToPoint



class TGoToFix(Tactic):
    def __init__(self, bot_id, state,  param=None):
        super(TGoToFix, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()
        

    def execute(self, state, pub):
        target = Vector2D(int(0),int(0))
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        flag = 0
        
        theta = atan2((ballPos.y - target.y), (ballPos.x - target.x))

        if ballPos.dist(botPos) > 2 * BOT_RADIUS:
            x1 = BOT_RADIUS * cos(theta) + float(state.ballPos.x)
            y1 = BOT_RADIUS * sin(theta) + float(state.ballPos.y)

            fpoint = Vector2D(int(x1), int(y1))

            x2 = -BOT_RADIUS * cos(theta) + float(state.ballPos.x)
            y2 = -BOT_RADIUS * sin(theta) + float(state.ballPos.y)

            spoint = Vector2D(int(x2), int(y2))

            fix = Vector2D()
  
            if target.dist(fpoint) > target.dist(spoint):
                fix.x = int(fpoint.x)
                fix.y = int(fpoint.y)
            else:
                fix.x = int(spoint.x)
                fix.y = int(spoint.y)

            #angleToTurn = ballPos.normalizeAngle((ballPos.angle(botPos))-(state.homePos[bot_id].theta))

            print "*******BALL POS  "+str(ballPos.x)+"   "+str(ballPos.y)

            print "#####FIX POINT   "+str(fix.x)+"     "+str(fix.y)
            
            self.sParam.GoToPointP.x = fix.x
            self.sParam.GoToPointP.y = fix.y
            self.sParam.GoToPointP.finalslope = ballPos.angle(target)
            self.sParam.GoToPointP.align = True
            sGoToPoint.execute(self.sParam, state, self.bot_id, pub)
            print "################GOTOPOINT WHEN SELECTING POINT##############"

        elif ballPos.dist(botPos) < 2 * BOT_RADIUS and ballPos.dist(botPos) > BOT_RADIUS:

            self.sParam.GoToBallP.intercept = False #may be true
            sGoToBall.execute(self.sParam, state, self.bot_id, pub)
            print "###############GOTOBALL################"


        elif ballPos.dist(botPos) <= BOT_RADIUS:
            self.sParam.GoToPointP.x = target.x
            self.sParam.GoToPointP.y = target.y
            self.sParam.GoToPointP.finalslope = ballPos.angle(target)
            self.sParam.GoToPointP.align = True
            sGoToPoint.execute(self.sParam, state, self.bot_id, pub)
            print "#################GOING FOR TARGET########"




    def isComplete(self, state):

        if ballPos.x == int(0) and ballPos.y == int(0):
            return True
        else:
            return False


        # TO DO use threshold distance instead of actual co ordinates
        # if self.destination.dist(state.homePos[self.bot_id]) < self.threshold:
        #     return True
        # elif time.time()-self.begin_time > self.time_out:
        #     return True
        # else:
        #     return False

    def updateParams(self, state):
        # No parameter to update here
        pass        