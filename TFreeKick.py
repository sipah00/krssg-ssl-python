from tactic import Tactic
import time
import sys

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
import sKickToPoint

DIST_THRESH=BOT_BALL_THRESH/4.0
MAXX = 15000/3

class TFreekick(Tactic):
    def __init__(self, bot_id, state,  param = None,):
        super(TFreekick, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()


    def ballInGoal(self, ballPos):
        x1 = 3000
        x2 = 3250
        y1 = 400
        y2 = -400
        if ballPos.x > min(x1, x2) and ballPos.y > min(y1, y2) and ballPos.x < max(x1, x2) and ballPos.y < max(y1 ,y2):
            return True
        else:
            return False

    def sign(self, p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    def pointInTri(self, pt, v1, v2, v3):
        b1 = self.sign(pt, v1, v2) < 0.0
        b2 = self.sign(pt, v2, v3) < 0.0
        b3 = self.sign(pt, v3, v1) < 0.0
        
        return b1 == b2 and b2 == b3

    def execute(self, state, pub):
        print "CHAL RAHA HAI"

        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))

        onePoint = Vector2D(int(x1), int(y1))
        secPoint = Vector2D(int(x2), int(y2))

        goliPos = #Vector2D(int(), int())

        if self.ballInGoal(ballPos) == False:
            if botPos.dist(ballPos) > BOT_BALL_THRESH:
                self.sParam.GoToBallP.intercept = False
                sGoToPoint.execute(self.sParam, state, self.bot_id, pub)
                return

            isSafe = True

            for opp in state.awayPos:
                if self.pointInTri(opp, onePoint, secPoint, ballPos) == True:
                    isSafe = False

            if isSafe == True:
                target = Vector2D()
                midPoint = Vector2D((int(onePoint.x + secPoint.x) / 2) + int((onePoint.y + secPoint.y) / 2))

                if self.pointInTri(goliPos, onePoint, midPoint, ballPos):
                    target.x = (midPoint.x + secPoint.x) / 2
                    target.y = (midPoint.y + secPoint.y) / 2
                else:
                    target.x = (midPoint.x + onePoint.x) / 2
                    target.y = (midPoint.y + onePoint.y) / 2

                self.sParam.KickToPointP.x = target.x
                self.sParam.KickToPointP.y = target.y
                self.sParam.KickToPointP.power = 7
                sKickToPoint.execute(self.sParam, state, self.bot_id, pub)
                return


    def isComplete(self, state):
        if self.ballInGoal(Vector2D(int(state.ballPos.x), int(state.ballPos.y))) == True:
            return True
        else:
            return False

    def updateParams(self, state):
        # No parameter to update here
        pass        