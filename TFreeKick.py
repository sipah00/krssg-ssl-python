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
import sKickToPoint
import sGoToBall
from numpy import inf

x1 = 3000
x2 = 3250
y1 = 400
y2 = -400

onePoint = Vector2D(int(x1), int(y1))
secPoint = Vector2D(int(x2), int(y2))
optimal_dist=HALF_FIELD_MAXX*3/5.0


class Pair():
    def __init__(self, first = 0, second = 0):
        self.first = first
        self.second = second

class TFreeKick(Tactic):
    def __init__(self, bot_id, state,  param = None,):
        super(TFreeKick, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()


    def is_goal_possible(self, opponents, ballPos_):         #opponents->[opp_pos, id, angle]
        MIN_ANGLE_DIFF=10*pi/180
        opponents.sort(key=lambda x:x[2])
        min_angle=atan2((y2- ballPos_.y), (x2- ballPos_.x))
        max_angle=atan2((y1- ballPos_.y), (x2- ballPos_.x))

        prev_angle=min_angle
        max_diff=0
        kicking_point=Vector2D(int((x1+x2)/2), int((y1+y2)/2))
        flag=False
        no_opp=0
        count=0
        diff=0
        # print("min_angle=",min_angle*180/pi,"  max_angle=",max_angle*180/pi)
        for opponent in opponents:
            # print("opp_no ",count," at ",opponent[2]*180/pi)
            if(min_angle<opponent[2]<max_angle):
                no_opp+=1
                curr_angle=opponent[2]
                diff=curr_angle- prev_angle
                THRESHHOLD_ANGLE=atan(BOT_RADIUS/ballPos_.dist(opponent[0]))
                if(diff > THRESHHOLD_ANGLE and diff>max_diff):
                    shooting_angle=(curr_angle+prev_angle)/2.0
                    max_diff = diff
                    kicking_point=Vector2D(int(optimal_dist*cos(shooting_angle)), int(optimal_dist*sin(shooting_angle)))
                    flag = True
            count+=1   
        if(diff< MIN_ANGLE_DIFF):
            flag= False         
        if(no_opp==0):
            flag=True   

        print("no_opp=",no_opp," DIFF_______=",max_diff)             
        return kicking_point, flag    
            
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

    def getKickPoint(self, ballPos, state):
        point_to_kick=self.find_supports_based_kick_position(ballPos, state)    

        return point_to_kick
        # redZone = []
        # for point in obs:
        #     theta = atan2((ballPos.y - point.y), (ballPos.x - point.x))
        #     theta-=pi/2
        #     x1 = BOT_RADIUS * cos(theta) + point.x
        #     y1 = BOT_RADIUS * sin(theta) + point.y

        #     x2 = -BOT_RADIUS * cos(theta) + point.x
        #     y2 = -BOT_RADIUS * sin(theta) + point.y

        #     oneP = Vector2D(int(x1), int(y1))
        #     secP = Vector2D(int(x2), int(y2))

        #     redAngle1 = atan2(y1 - ballPos.y, x1 - ballPos.x)
        #     redAngle2 = atan2(y2 - ballPos.y, x2 - ballPos.x)

        #     # a =  ballPos.dist(oneP)
        #     # b = ballPos.dist(secP)
        #     # c = oneP.dist(secP)
        #     # ang = acos((a * a + b * b - c * c) / 2 * a * b)

        #     redZone.append(Pair(min(redAngle1, redAngle2), max(redAngle1, redAngle2)))

        # redZone.sort(key = lambda x : x.first)

        # safeZone = []

        # for i in range(0, len(redZone) - 1):
        #     safeZone.append(Pair(redZone[i].second, redZone[i+1].first))
        
        # safeZone.sort(key = lambda x : x.second - x.first)
        # if(len(safeZone)>=1):                    ########## ************************
        #     bisectAng = (safeZone[-1].first + safeZone[-1].second) / 2
        #     print "/*/*/**//"*1000
        # else:
        #     point_to_kick=self.find_supports_based_kick_position(ballPos, state)    

        #     return point_to_kick
        # yPoint = ballPos.y + tan(bisectAng) * (x1 - ballPos.x)

        # return Vector2D(int(x1), int(yPoint))

    def find_shooting_angle(self, state, angle_to_shoot, ballPos):
        shooting_angle=angle_to_shoot[0]
        min_diff=inf
        id=None
        for support in state.homePos:
            pos=Vector2D(int(support.x), int(support.y))
            angle=pos.angle(ballPos)  
            count=0  
            for angle_to_s in angle_to_shoot:
                if(fabs(angle- angle_to_s)<min_diff):
                    min_diff=fabs(angle_to_s- angle)
                    id=count
                count+=1    
        print("min_diff_angle=",min_diff*180/pi)        
        return angle_to_shoot[id]        

    def find_supports_based_kick_position(self, ballPos_, state):
        ballPos=Vector2D(int(ballPos_.x), int(ballPos_.y))
        opponents=[]
        for i in xrange(len(state.homePos)):
            opp_pos=Vector2D(int(state.awayPos[i].x),int(state.awayPos[i].y))
            angle=opp_pos.normalizeAngle(opp_pos.angle(ballPos))
            opponents.append([opp_pos,i , angle])

        opponents.sort(key=lambda x:x[2])
        angles=[]
        for opponent in opponents:
            angles.append([opponent[2],opponent[1]])
        
        self.Opp_sorted_Angles=[]
        for angle in angles:
            ANGLE_THRESH = pi/12
            self.Opp_sorted_Angles.append([angle[0]-ANGLE_THRESH,angle[0]+ANGLE_THRESH,angle[1]])

        lineangles=[]
        angle_gap=8.314*pi/180
        angle_to_shoot=[]
        i=0; j=1
        weights=[]
        ##print "Opp angles: "+str(self.Opp_sorted_Angles)
        for i in xrange(len(self.Opp_sorted_Angles)):
            origin_angle=self.Opp_sorted_Angles[i][1]
            j=i+1
            flag=0
            if j>=len(self.Opp_sorted_Angles): j=0; flag=1
            diff=self.Opp_sorted_Angles[j][0]-self.Opp_sorted_Angles[i][1]
            
            if flag:
                diff*=-1
                diff = 2*pi - diff


            if (diff>angle_gap) :
                angle_here=diff
                ##print "angle here inside: "+str(array(angle_here)*(180/pi))
                if angle_here>pi:
                    angle_to_shoot.extend([origin_angle+(angle_here/3),origin_angle+(angle_here*2/3)])
                else:
                    angle_to_shoot.append(origin_angle+angle_here/2) 

        angle_to_shoot = map(Vector2D().normalizeAngle , angle_to_shoot)

        shooting_angle=self.find_shooting_angle(state, angle_to_shoot, ballPos)
        min_angle=2*pi
        support_angle=[]
        count=0
        id=0
        for support in state.homePos:
            supp_pos = Vector2D(int(support.x), int(support.y))
            angle=supp_pos.angle(ballPos)
            support_angle.append(angle)
            
            if(fabs(angle - shooting_angle)<min_angle):
                min_angle=fabs(angle - shooting_angle)
                id = count
            count+=1
            
        ######## GOT THE RECEIVER AS ID #######
        
        kicking_point= Vector2D(int((optimal_dist)*cos(shooting_angle)), int(optimal_dist*sin(shooting_angle)))  
        return kicking_point      

    def execute(self, state, pub):
        #print "CHAL RAHA HAI" 

        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        goliPos = Vector2D()

        # if state.opp_goalie != 10:   #if opp_goalie will not be detected it's value will be 10
        #     goliPos.x = int(state.awayPos[state.opp_goalie].x)
        #     goliPos.y = int(state.awayPos[state.opp_goalie].y)

        goliPos.x = int(3000)
        goliPos.y = int(0)

        opponents=[]
        count=0
        for opponent in state.awayPos:
            pos=Vector2D(int(opponent.x), int(opponent.y))
            angle=pos.angle(ballPos)
            # print("opp_no ",count," at ",pos.x,pos.y," ball at ",ballPos.x,ballPos.y)
            # print("opp_no ",count," at ",angle*180/pi,"*****")
            opponents.append([pos, count, angle])
            count+=1

        kicking_point, flag= self.is_goal_possible(opponents, ballPos)
        print(" got_flag=",flag)
        if(flag):
                self.sParam.KickToPointP.x = kicking_point.x
                self.sParam.KickToPointP.y = kicking_point.y
                self.sParam.KickToPointP.power = 7

                print(" TP1 ",kicking_point.x,kicking_point.y)
                sKickToPoint.execute(self.sParam, state, self.bot_id, pub)
                #print "CHAL RAHA HAI" *100
                return
        else:
                targetPoint = self.getKickPoint(state.ballPos, state)
                self.sParam.KickToPointP.x = targetPoint.x
                self.sParam.KickToPointP.y = targetPoint.y
                self.sParam.KickToPointP.power = 7
                print(" TP2 ",targetPoint.x,targetPoint.y)
                sKickToPoint.execute(self.sParam, state, self.bot_id, pub)
                #print "CHAL RAHA HAI" *100
                return        


        # *********** #

        # if self.ballInGoal(ballPos) == False :         

        #     if botPos.dist(ballPos) > BOT_BALL_THRESH:
        #         self.sParam.GoToBallP.intercept = False
        #         sGoToBall.execute(self.sParam, state, self.bot_id, pub)
        #         #print "/*/" *1000
        #         return

        #     isSafe = True
        #     #print "/"*1000

        #     for i in range(6):
        #         opp = state.homePos[i]
        #         if self.pointInTri(opp, onePoint, secPoint, ballPos) == True:
        #             isSafe = False

        #     for i in range(6):
        #         opp = state.awayPos[i]
        #         if self.pointInTri(opp, onePoint, secPoint, ballPos) == True:
        #             isSafe = False

        #     if isSafe == True :          
        #         #print "*"*100000
        #         target = Vector2D()
        #         midPoint = Vector2D((int(onePoint.x + secPoint.x) / 2), int((onePoint.y + secPoint.y) / 2))

        #         if self.pointInTri(goliPos, onePoint, midPoint, ballPos):
        #             target.x = (midPoint.x + secPoint.x) / 2
        #             target.y = (midPoint.y + secPoint.y) / 2
        #         else:
        #             target.x = (midPoint.x + onePoint.x) / 2
        #             target.y = (midPoint.y + onePoint.y) / 2


        #         print ("\n\n\n\n____TP_____"+str(target.x)+","+str(target.y))    
        #         self.sParam.KickToPointP.x = target.x
        #         self.sParam.KickToPointP.y = target.y
        #         self.sParam.KickToPointP.power = 4
        #         sKickToPoint.execute(self.sParam, state, self.bot_id, pub)
        #         #print "CHAL RAHA HAI" *100
        #         return

        #     else:
        #         #find max open angle to kick
        #         obs = []
        #         for i in range(0, len(state.homeDetected)):
        #             if fabs(state.homePos[i].x) >= fabs(state.homePos[self.bot_id].x) and self.pointInTri(state.homePos[i], onePoint, secPoint, ballPos) == True: 
        #                 obs.append(Vector2D(int(state.homePos[i].x), int(state.homePos[i].y)))  

        #         for i in range(0, len(state.awayDetected)):
        #             if fabs(state.awayPos[i].x) >= fabs(state.homePos[self.bot_id].x) and self.pointInTri(state.awayPos[i], onePoint, secPoint, ballPos) == True:
        #                 obs.append(Vector2D(int(state.awayPos[i].x), int(state.awayPos[i].y)))

        #         targetPoint = self.getKickPoint(obs, state.ballPos, state)
        #         #print "*/*/*/*" * 100

        #         #print "*/*/*/*/*" + str(targetPoint.x) + "        " + str(targetPoint.y)


        #         self.sParam.KickToPointP.x = targetPoint.x
        #         self.sParam.KickToPointP.y = targetPoint.y
        #         self.sParam.KickToPointP.power = 4
        #         sKickToPoint.execute(self.sParam, state, self.bot_id, pub)
        #         return

    def isComplete(self, state):
        if self.ballInGoal(Vector2D(int(state.ballPos.x), int(state.ballPos.y))) == True:
            return True
        else:
            return False


    def updateParams(self, state):
        pass

