"""
Cookie Clicker Simulator

Copy to codeskulptor.com and run.
"""

import simpleplot
import math
#counter = 0
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 16.0
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return 'T=' + str(self._current_time) + ' CC=' + str(self._current_cookies) \
                    + ' CPS=' + str(self._current_cps) + ' TC=' + str(self._total_cookies)
        
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
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history_list = self._history
        return history_list

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        wait_time = math.ceil((cookies - self._current_cookies) / self._current_cps)
        if wait_time > 0:
            return wait_time
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            #print item_name
            #print 'Before buying', self._current_cookies
            self._current_cookies -= cost
            #print 'After buying', self._current_cookies
            self._current_cps += additional_cps
            current_time = self._current_time
            total_cookies = self._total_cookies
            self._history.append((current_time, item_name, cost, total_cookies))
    
def simulate_clicker(build_info, duration, strategy):
    #global counter
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    simulation = ClickerState()
    builds = build_info.clone()
    while simulation.get_time() < duration:
        #counter += 1
        #print counter
        #print 'Simulation =', simulation.get_time(), 'Duration =', duration
        time_left = duration - simulation.get_time()
        #print 'Time left =', time_left
        cookies = simulation.get_cookies()
        cps = simulation.get_cps()
        history = simulation.get_history()
        to_buy = strategy(cookies, cps, history, time_left, builds)
        if to_buy == None:
            simulation.wait(duration - simulation.get_time())
            break
        cost_to_buy = builds.get_cost(to_buy)
        time_to_wait = simulation.time_until(cost_to_buy)
        #print 'Time to wait =', time_to_wait
        if time_to_wait <= time_left:
            cps_increment = builds.get_cps(to_buy)
            simulation.wait(time_to_wait)
            #print 'Wait time', time_to_wait
            #print simulation.get_time(), to_buy
            while cost_to_buy <= simulation.get_cookies():
                simulation.buy_item(to_buy, cost_to_buy, cps_increment)
                builds.update_item(to_buy)  
                cookies = simulation.get_cookies()
                cps = simulation.get_cps()
                history = simulation.get_history()
                time_left = duration - simulation.get_time()
                to_buy = strategy(cookies, cps, history, time_left, builds)
                #print to_buy
                if to_buy == None:
                    simulation.wait(duration - simulation.get_time())
                    break
                cost_to_buy = builds.get_cost(to_buy)
                cps_increment = builds.get_cps(to_buy)
                #print cost_to_buy, cookies, time_left
        else:
            simulation.wait(duration - simulation.get_time())
    #print builds.get_cost('Cursor')
    #print builds.get_cost('Farm')
    #print len(simulation.get_history())
    # Replace with your code
    return simulation

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

#print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0, strategy_cursor_broken)

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
    all_items = build_info.build_items()
    affordable_cheapest_item = None
    affordable_cheapest_cost = float('inf')
    for item in all_items:
        item_cost = build_info.get_cost(item)
        if cookies + cps * time_left >= item_cost:
            if item_cost < affordable_cheapest_cost:
                affordable_cheapest_item = item
                affordable_cheapest_cost = item_cost
    return affordable_cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    all_items = build_info.build_items()
    affordable_max_item = None
    affordable_max_cost = float('-inf')
    for item in all_items:
        item_cost = build_info.get_cost(item)
        if cookies + cps * time_left >= item_cost:
            if item_cost > affordable_max_cost:
                affordable_max_item = item
                affordable_max_cost = item_cost
    #print 'Item', affordable_max_item
    return affordable_max_item

#buildss = provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001], 'Portal': [1666666.0, 6666.0], 'Shipment': [40000.0, 100.0], 'Grandma': [100.0, 0.5], 'Farm': [500.0, 4.0], 'Time Machine': [123456789.0, 98765.0], 'Alchemy Lab': [200000.0, 400.0], 'Factory': [3000.0, 10.0], 'Antimatter Condenser': [3999999999.0, 999999.0], 'Mine': [10000.0, 40.0]}, 1.15)
#print simulate_clicker(buildss, 10000000000.0, strategy_expensive)


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    all_items = build_info.build_items()
    affordable_efficient_item = None
    highest_efficiency = float('-inf')
    for item in all_items:
        item_cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        efficiency = item_cps / item_cost
        if cookies + cps * time_left >= item_cost:
            if efficiency > highest_efficiency:
                affordable_efficient_item = item
                highest_efficiency = efficiency
    return affordable_efficient_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    print state.get_history()

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
#run()


    

