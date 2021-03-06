from tactic import Tactic
import time
import sys
import math

sys.path.append('/home/shubham00/krssg-ssl/catkin_ws/src/skills_py/scripts/skills')
sys.path.append('/home/shubham00/krssg-ssl/catkin_ws/src/plays_py/scripts/utils/')
sys.path.insert(0, '/home/shubham00/krssg-ssl/catkin_ws/src/navigation_py/scripts/navigation/src')
sys.path.insert(0, '/home/shubham00/krssg-ssl/catkin_ws/src/navigation_py/scripts/navigation')

from geometry import * 
import skills_union
from config import *
import obstacle
import sGoToPoint

KICK_RANGE_THRESH = MAX_DRIBBLE_R   #ASK
THRES  = 0.8
THETA_THRESH = 0.005
TURNING_THRESH = 10


class TMark(Tactic):
    def __init__(self, bot_id, state, param=None):
        super(TMark, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()

    def execute(self, state, pub):
        botpos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        markedPos = Vector2D(int(state.homePos[self.param.MarkBotP.awayBotID].x), int(state.homePos[self.param.MarkBotP.awayBotID].y))
        ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
        guardPos = Vector2D()
        v = Vector2D()

        passer = -1
        passer_dist = 99999999999999

        for oppID in range(4):
            oppPos = Vector2D(int(state.homePos[oppID].x), int(state.homePos[oppID].y))
            kick_range_test = v.absSq((oppPos - ballPos))

            if kick_range_test < KICK_RANGE_THRESH and kick_range_test < passer_dist:
                passer_dist = oppID
                passer_dist = kick_range_test

        if passer != -1:
            if fabs(ballPos.x - markedPos.x) > fabs(ballPos.y - markedPos.y):
                if ballPos.x > markedPos.x:
                    guardPos.x = int(markedPos.x + DBOX_WIDTH/4)
                else:
                    guardPos.x = int(markedPos.x - DBOX_WIDTH/4)

            guardPos.y = ( ((state.ballPos.y - state.awayPos[passer].y) / (state.ballPos.x - state.awayPos[passer].x)) * (guardPos.x - state.ballPos.x) ) + state.ballPos.y
        else:
            if ballPos.y > markedPos.y:
                guardPos.y = int(markedPos.y + DBOX_WIDTH/4)
            else:
                guardPos.y = int(markedPos.y - DBOX_WIDTH/4)

            guardPos.x = int(( ((markedPos.x - state.ballPos.x) / (markedPos.y - state.ballPos.y)) * (guardPos.y - state.ballPos.y) ) + state.ballPos.x)


        self.sParam.GoToPointP.x             = guardPos.x
        self.sParam.GoToPointP.y             = guardPos.y
        self.sParam.GoToPointP.align         = False   #ASK

        angleToTurn = guardPos.normalizeAngle(ballPos.angle(guardPos))

        self.sParam.GoToPointP.finalslope    = angleToTurn
        self.sParam.GoToPointP.finalVelocity = 0

        sGoToPoint.execute(self.sParam, state, self.bot_id, pub)


    def isComplete(self, state):
        # TO DO use threshold distance instead of actual co ordinates
        if self.destination.dist(state.homePos[self.bot_id]) < self.threshold:
            return True
        elif time.time()-self.begin_time > self.time_out:
            return True
        else:
            return False

    def updateParams(self, state):
        # No parameter to update here
        pass

