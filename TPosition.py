from tactic import Tactic
import time
import sys
from math import *

sys.path.append('../../../skills_py/scripts/skills')
sys.path.append('../../../plays_py/scripts/utils/')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '../../../navigation_py/scripts/navigation')

from geometry import * 
import skills_union
from config import *
import obstacle
import sGoToPoint

THRESHOLD = 10 # by testing we can put better value


class TPosition(Tactic):
    def __init__(self, bot_id, state, param = None):
        super(TPosition, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()
        self.bot_id = bot_id
        self.destination = Vector2D(int(self.param.x), int(self.param.y))

    def execute(self, state, pub):
        #GO_TO_POINT

        self.sParam.GoToPointP.x = self.param.x
        self.sParam.GoToPointP.y = self.param.y
        self.sParam.GoToPointP.finalslope = self.param.finalSlope
        sGoToPoint.execute(self.sParam, state, self.bot_id, pub)

     
    def isComplete(self, state):
        # TO DO use threshold distance instead of actual co ordinates
        if self.destination.dist(state.homePos[self.bot_id]) < THRESHOLD:
            return True
        elif time.time()-self.begin_time > self.time_out:
            return True
        else:
            return False

    def updateParams(self, state):
        # No parameter to update here
        pass
