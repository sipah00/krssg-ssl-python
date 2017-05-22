import skill_node
import math
import sys

sys.path.append('/home/shubham00/krssg-ssl/catkin_ws/src/skills_py/scripts/skills')
sys.path.insert(0, '/home/shubham00/krssg-ssl/catkin_ws/src/navigation_py/scripts/navigation')
sys.path.insert(0, '/home/shubham00/krssg-ssl/catkin_ws/src/navigation_py/scripts/navigation/src')
sys.path.insert(0, '/home/shubham00/krssg-ssl/catkin_ws/src/plays_py/scripts/utils')

from config import *
from wrapperpy import *
from obstacle import Obstacle
from geometry import *

import skills_union
import sGoToBall
import sTurnToPoint

def execute(param, state, bot_id, pub):
    botPos=Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))
    destPoint=Vector2D(int(param.KickToPointP.x), int(param.KickToPointP.y))
    ob = Vector2D()

    finalSlope = destPoint.angle(botPos)
    turnAngleLeft = ob.normalizeAngle(finalSlope - state.homePos[bot_id].theta)  #Angle left to turn
    dist = ballPos.dist(botPos)

    if dist > BOT_BALL_THRESH :
        sGoToBall.execute(param, state, bot_id, pub)
        return

    if math.fabs(turnAngleLeft) > SATISFIABLE_THETA/2 : # SATISFIABLE_THETA in config file
        sParam = skills_union.SParam()
        sParam.TurnToPointP.x = destPoint.x
        sParam.TurnToPointP.y = destPoint.y
        sParam.TurnToPointP.max_omega = MAX_BOT_OMEGA*3
        sTurnToPoint.execute(sParam, state, bot_id, pub)
        return

    skill_node.send_command(pub, state.isteamyellow, bot_id ,0, 0, 0, param.KickToPointP.power, False)


    
      
     
    