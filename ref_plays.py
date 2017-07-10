import sys

sys.path.append('../../../tactics_py/scripts')
sys.path.append('..')

from tactic_factory import TPosition
from tactic_factory import TPositionK
from tactic_factory import TStop
from tactic_factory import TWall
from utils import tactics_union
from utils.robot_threads import robot_thread as thread
from math import *

CONST_DIST = 50

class RefPlay(object):
    def __init__(self, state, tactic, params, publisher):
        self.active_robots = 6 # Might change if any of our bot is given red card
        self.role_list = [['' for i in range(2)] for j in range(6)]
        self.instances = []
        self.robots = []
        self.state = state
        self.tactic = tactic
        self.publisher = publisher
        for i in range(6):
            self.role_list[i][0] = tactic[i]
            self.role_list[i][1] = params[i]

    def tactic_instance(self):
        for i in range(self.active_robots):
            if self.tactic[i] == "TPosition":
                self.instances.append(TPosition.TPosition(i, self.role_list[i][0], self.role_list[i][1]))
            elif self.tactic[i]=="TStop":
                self.instances.append(TStop.TStop(i, self.role_list[i][0], self.role_list[i][1]))
            elif self.tactic[i] == "TGoalie":
                self.instances.append(TGoalie.TGoalie(i, self.role_list[i][0], self.role_list[i][1]))
            elif self.tactic[i] == "TGoToFix":
                self.instances.append(TGoToFix.TGoToFix(i, self.role_list[i][0], self.role_list[i][1]))
            else:
                self.instances.append(None)

            #self.instances.append(i, self.role_list[i][0], self.role_list[i][1])

    def execute(self):
        for i in range(self.active_robots):
            self.robots.append(thread(self.instances[i], self.state, self.publisher))
        print '____Begin threads_____'
        for i in range(self.active_robots):
            self.robots[i].start()
        for robot in self.robots:
            robot.join()
        print '____Exit threads_____'

class ref_halt(RefPlay):
    def __init__(self, state, publisher):
        params = tactics_union.Param()
        tactic = {0:"TStop", 1:"TStop", 2:"TStop", 3:"TStop", 4:"TStop", 5:"TStop"}
        params = {0:params, 1:params, 2:params, 3:params, 4:params, 5:params}
        RefPlay.__init__(self, state, tactic, params, publisher)

    def tactic_instance(self):
        RefPlay.tactic_instance(self)

    def execute(self):
        RefPlay.execute(self)

class ref_stop(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_normal_start(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_force_start(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_kickoff_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_kickoff_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_penalty_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_penalty_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_direct_free_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_direct_free_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_indirect_free_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_indirect_free_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_timeout_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_timeout_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_goal_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_goal_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_ball_placement_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_placement_blue(RefPlay):
    def __init__(self, state, publisher):
        params0 = tactics_union.Param()
        params1 = tactics_union.Param()
        params2 = tactics_union.Param()
        params3 = tactics_union.Param()
        params  = tactics_union.Param()
        
        MAXX = HALF_FIELD_MAXX / 2
        MAXY = HALF_FIELD_MAXY * 2  - (HALF_FIELD_MAXY * 2  - 8 * BOT_RADIUS) / 2
        MAXY = MAXY - BOT_RADIUS
        
        params0.PositionP.x = MAXX
        params0.PositionP.y = MAXY

        params1.PositionP.x = MAXX

        MAXY = MAXY - 2.2 * BOT_RADIUS

        params1.PositionP.y = MAXY

        params2.PositionP.x = MAXX

        MAXY = MAXY - 2.2 * BOT_RADIUS

        params2.PositionP.y = MAXY

        params3.PositionP.x = MAXX

        MAXY = MAXY - 2.2 * BOT_RADIUS
        
        params3.PositionP.y = MAXY

        params0.PositionP.finalSlope = pi
        params1.PositionP.finalSlope = pi
        params2.PositionP.finalSlope = pi
        params3.PositionP.finalSlope = pi 


        tactic = {0:"TPosition", 1:"TPosition", 2:"TPositon", 3:"TPosition", 4:"TGoalie", 5:"TGoToFix"}
        params = {0:params0, 1:params1, 2:params2, 3:params3, 4:params, 5:params}
        RefPlay.__init__(self, state, tactic, params, publisher)

    def tactic_instance(self):
        #pass
        RefPlay.tactic_instance()

    def execute(self):
        #pass
        RefPlay.execute(self)
