from tactic import Tactic
import time
import sys
from math import *

K_OP_DIST=10
K_SUPP_DIST=10
K_ANGLE_DIFF=10
ANGLE_THRESH=15*pi/180
MIN_HALF_BIS_ANGLE=10*pi/180

sys.path.append('/home/shubham00/krssg-ssl/catkin_ws/src/skills_py/scripts/skills')
sys.path.append('/home/shubham00/krssg-ssl/catkin_ws/src/plays_py/scripts/utils/')
sys.path.insert(0, '/home/shubham00/krssg-ssl/catkin_ws/src/navigation_py/scripts/navigation/src')
sys.path.insert(0, '/home/shubham00/krssg-ssl/catkin_ws/src/navigation_py/scripts/navigation')

from geometry import * 
import skills_union
from config import *
import obstacle
import sGoToPoint

class TPosition(Tactic):
    def __init__(self, bot_id, state, param=None):
        super(TPosition, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()

    def angle_1_wrt_2(p1, p2):                  #p1 & p2 ->Vector2D
        angle_calc=0
        angle_calc=atan2((p1.y-p2.y),(p1.x-p2.x))


        return angle_calc

    def execute(self, state, pub):
        bot_id=0                                #attacker bot_id
        att_pos=Vector2D(int(state.awayPos[bot_id].x),int(state.awayPos[bot_id].y))
        opponents=[]                            #appending opponent posn, id, opp_angle wrt att
        supports=[]                             #appending support posn, id
        angles=[]                               #[0]->angle-th, [1]->angle+th, [2]->opp_id
        bis_angles=[]                           #[0]-> angle of bisectors wrt x-axis
        for i in range(state.awayPos):
        	opp_pos=Vector2D(int(state.awayPos[i].x),int(state.awayPos[i].y))
        	angle=angle_1_wrt_2(opp_pos,att_pos)
            opponents.append(opp_pos,i, angle)
           
        for i in range(len(state.homePos)):
            supports.append(Vector2D(int(state.homePos[i].x),int(state.homePos[i].y)),i)  

        opponents.sort(key=lambda x:x[2])
        for opponent in opponents:
        	angles.append(opponent[2]-ANGLE_THRESH, opponent[2]+ANGLE_THRESH, opponent[1])
        for i in xrange(len(opponents)-1):	     
        	if(angles[(i+1)%6][0]-angles[i][1]>2*MIN_HALF_BIS_ANGLE):
        		bis_angles.append((angles[(i+1)%6][0]-angles[i][0])/2)
        if(fabs(opponents[0][2]-opponents[5][2])<2*pi-2*(ANGLE_THRESH+MIN_HALF_BIS_ANGLE)):
        	bis_angles.append((angles[0][0]-angles[5][0])/2)
        			



        def cover_the_region(cx, cy, iter, mscore, closest_bis_angle):
            if(iter>N_ITER):
                return Vector2D(int(cx), int(cy))
            row=[-1, 0,1,0]
            col=[ 0,-1,0,1]
            index=-1
            cscore=0
            for k in [0:3]:
                cscore=assign_score(cx+row[k], cy+col[k], closest_bis_angle)
                if(cscore>mscore):
                    mscore=cscore
                    index=k
            if(index==-1):
                return Vector2D(int(cx), int(cy))
            else
                return cover_the_region(cx+row[index], cy+col[index], iter+1, mscore, closest_bis_angle)            

        def score_dist_opp(dist):
            return exp(-K_OP_DIST*dist)

        def score_dist_supp(dist):
            return exp(+K_SUPP_DIST*dist)

        def bis_angle_diff(ang_diff):
            return (-K_ANGLE_DIFF*ang_diff)     

        def assign_score(x , y, closest_bis_angle):         #p1: opponent dist, p2: support dist, p3: safe region & angle bis
            flag=1; 
            sc1=sc2=sc3=0
            this_angle=angle_1_wrt_2(Vector2D(x,y), Vector2D(supports[bot_id][0]))
            this_pos=Vector2D(int(x),int(y))
            for angle in angles:
                if(angle[0]<this_angle<angle[1]):
                    if(opponent[0].dist(supports[bot_id][0])<this_pos.dist(supports[bot_id][0]))
                      flag=0
                      break
            if(flag==0):                        #if in black region & behind opp, score=0
                return 0

            for opponent in opponents:
                sc1+=score_dist_opp(opponent[0].dist(this_pos))

            for support in supports:
                sc2+=score_dist_supp(support[0].dist(this_pos)) 
            
            sc3=bis_angle_diff(fabs(this_angle-closest_bis_angle))

            return sc1+sc2+sc3

        sx=0 sy=0
        this_bot_angle=angle_1_wrt_2(supports[self.bot_id][0],supports[bot_id][0])
        closest_bis_angle=bis_angles[0];
        for bise in bis_angles:
            if(fabs(bise- this_bot_angle)<fabs(closest_bis_angle- this_bot_angle)):
                closest_bis_angle=bise;

        distance= supports[bot_id].dist(supports[self.bot_id])
        sx=distance*cos(closest_bis_angle)
        sy=distance*sin(closest_bis_angle)      

        best_pos=cover_the_region(sx, sy, 0, assign_score(sx,sy, closest_bis_angle), closest_bis_angle)

        self.sParam.GoToPointP.x=best_pos.x
        self.sParam.GoToPointP.y=best_pos.y
        self.sParam.GoToPointP.finalslope=angle_1_wrt_2(supports[bot_id][0], best_pos)
        self.sParam.GoToPointP.align=1
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

        
         




