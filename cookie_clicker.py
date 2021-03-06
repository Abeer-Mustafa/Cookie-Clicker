"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("Total Cookies: " + str(self._total_cookies) + "\n" + 
                "Current Cookies: " + str(self._current_cookies) + "\n" + 
                "CPS: " + str(self._cps) + "\n" +
                "Time: " + str(self._time))
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            return 0.0
        return (float(int(math.ceil((cookies-self._current_cookies)/(self._cps)))))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_cookies += time*self._cps
            self._total_cookies += time*self._cps
            self._time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost<= self._current_cookies:
            self._cps += additional_cps
            self._current_cookies-=cost
            self._history.append((self._time, item_name, cost, self._total_cookies))

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    clicker_state = ClickerState()
    copy_build = build_info.clone()
    while clicker_state.get_time()<=duration:
        cookies = clicker_state.get_cookies()
        cps = clicker_state.get_cps()
        history = clicker_state.get_history()
        time_left= duration - clicker_state.get_time()
        item = strategy(cookies, cps, history, time_left,copy_build)
        if item == None:
            break
            
        additional_cps = copy_build.get_cps(item)
        cost_item = copy_build.get_cost(item)
        wait_time=clicker_state.time_until(cost_item)
        
        if wait_time > time_left:
            break
        else:
            clicker_state.wait(wait_time)
            clicker_state.buy_item(item, cost_item, additional_cps)
            copy_build.update_item(item)
            
    time_rem = duration - clicker_state.get_time()   
    clicker_state.wait(time_rem)
        
    return clicker_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    choosen_item = None
    cheapest = float("inf")
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost <= cheapest:
            cheapest = cost
            choosen_item = item
    if (cookies + cps*time_left) < cheapest:
        return None
    return choosen_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    choosen_item = None
    expensive = 0.0
    can_afford = cookies + cps*time_left
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost >= expensive and cost <= can_afford:
            expensive = cost
            choosen_item = item
    return choosen_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    choosen_item = None
    best_ratio = 0.0
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        cps = build_info.get_cps(item)
        ratio = cps/cost
        if ratio > best_ratio:
            best_ratio = ratio
            choosen_item = item
    return choosen_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    
    # Plot total cookies over time
    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
