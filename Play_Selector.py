import sys
sys.path.append('../../../tactics_py/scripts/tactic_factory')
sys.path.append('../../../plays_py/scripts/utils')

import pTestPlay
import rospy
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
import threading
import time
import pStall
from std_msgs.msg import Int8
# import pDefence
import pCordinatedPass
from geometry import Vector2D
from config import *
from tactic_factory import TGoalie
import ref_plays

ref_play_id = 0
cur_play = None
start_time = 0
goalie_tac = None
cur_goalie = 7

def select_play(state):
	global start_time,pub
	# TO DO Proper play selection
	play_testplay=pTestPlay.pTestPlay(pub)
	#play_cordinatedpass=pCordinatedPass.pCordinatedPass()
	#play_stall=pStall.pStall(pub)
	start_time = time.clock()
	# play_testplay.execute()
	#return play_stall
	return play_testplay
	# #play_stall.execute()
	# play_Defence = pDefence.pDefence()
	# play_Defence.execute()

def ref_callback(play_id):
	global ref_play_id
	ref_play_id = play_id

def goalKeeper_callback(state):
	global pub,goalie_tac,cur_goalie
	if goalie_tac == None :
		cur_goalie = state.our_goalie
		goalie_tac = TGoalie.TGoalie(cur_goalie,state)
		
	if cur_goalie != state.our_goalie :
		cur_goalie_pos = Vector2D(state.homePos[cur_goalie].x,state.homePos[cur_goalie].y)
		new_goalie_pos = Vector2D(state.homePos[state.our_goalie].x,state.homePos[state.our_goalie].y)
		if(cur_goalie_pos.dist(new_goalie_pos) < 2.5 * BOT_RADIUS):
			goalie_tac.execute(state,pub)
			return
		cur_goalie = state.our_goalie
		goalie_tac = TGoalie.TGoalie(cur_goalie,state)
	goalie_tac.execute(state,pub)
	print ("goalie : ",cur_goalie)


def bs_callback(state):
	######
	global cur_play,start_time
	if ref_play_id == 0 :  # 0 signifies normal game play
		if(cur_play == None):
			cur_play = select_play(state)
		cur_time = time.clock()
		if(cur_time - start_time >=60): # TIME OUT IS 60 seconds for now
			cur_play = select_play(state)
		cur_play.execute(state)
	else :
		cur_play = None
		start_time = 0

		Rplace = ref_plays.ref_placement_blue(state, pub)
		Rplace.tactic_instance()
		Rplace.execute()


		# TO DO call corresponding refree plays here
		# Basically corresponding TPosition except goalie

if __name__=='__main__':
    global pub
    print "Initializing the node "
    rospy.init_node('play_py_node',anonymous=False)
    pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, bs_callback, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, goalKeeper_callback, queue_size=1000)
    rospy.Subscriber('/ref_play', Int8, ref_callback, queue_size=1000)
    rospy.spin()            
