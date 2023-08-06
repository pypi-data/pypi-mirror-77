import os
import numpy as np
import cvxpy as cp
from redis import StrictRedis
import redis
import scipy.stats
import logging
import pathos

from dragg.redis_client import RedisClient
from dragg.logger import Logger

def manage_home_forecast(home):
    """
    Calls class method as a top level function (picklizable)
    :return: list
    """
    return home.forecast_home()

def manage_home(home):
    """
    Calls class method as a top level function (picklizable)
    :return: None
    """
    home.run_home()
    return

class MPCCalc:
    def __init__(self, home):
        """
        params
        home: Dictionary with keys
        """
        self.q = None # depricated for threaded uses
        self.home = home  # reset every time home retrieved from Queue
        self.name = home['name']
        self.type = self.home['type']  # reset every time home retrieved from Queue
        self.start_hour_index = None  # set once upon thread init
        self.current_values = None  # set once upon thread init
        self.all_ghi = None  # list, all values in the GHI list, set once upon thread init
        self.all_oat = None  # list, all values in the OAT list, set once upon thread init
        self.all_spp = None  # list, all values in the SPP list, set once upon thread init
        self.home_r = None
        self.home_c = None
        self.hvac_p_c = None
        self.hvac_p_h = None
        self.wh_r = None
        self.wh_c = None
        self.wh_p = None
        self.temp_in_init = None
        self.temp_wh_init = None
        self.p_load = None
        self.plug_load = None
        self.temp_in = None
        self.temp_wh = None
        self.p_grid = None
        self.hvac_cool_on = None
        self.hvac_heat_on = None
        self.wh_heat_on = None
        self.spp = None
        self.oat = None
        self.ghi = None
        self.temp_wh_min = None
        self.temp_wh_max = None
        self.temp_in_min = None
        self.temp_in_max = None
        self.optimal_vals = {}
        self.iteration = None
        self.timestep = None
        self.assumed_wh_draw = None
        self.prev_optimal_vals = None  # set after timestep > 0, set_vals_for_current_run

        # setup cvxpy verbose solver
        self.verbose_flag = os.environ.get('VERBOSE','False')
        if not self.verbose_flag.lower() == 'true':
            self.verbose_flag = False
        else:
            self.verbose_flag = True

        # calls redis and gets all the environmental variables from beginning of simulation to end
        self.initialize_environmental_variables()

        # setup the base variables of HVAC and water heater
        self.setup_base_problem()
        if 'battery' in self.type:
            # setup the battery variables
            self.setup_battery_problem()
        if 'pv' in self.type:
            # setup the pv variables
            self.setup_pv_problem()

    def redis_write_optimal_vals(self):
        """
        Sends the optimal values for each home to the redis server.
        :return: None
        """
        key = self.name
        for field, value in self.optimal_vals.items():
            self.redis_client.conn.hset(key, field, value)

    def redis_get_prev_optimal_vals(self):
        """
        Collects starting point environmental values for all homes (such as current temperature).
        :return: None
        """
        key = self.name
        self.prev_optimal_vals = self.redis_client.conn.hgetall(key)

    def initialize_environmental_variables(self):
        # get a connection to redis
        self.redis_client = RedisClient()

        # collect all values necessary
        self.start_hour_index = self.redis_client.conn.get('start_hour_index')
        self.all_ghi = self.redis_client.conn.lrange('GHI', 0, -1)
        self.all_oat = self.redis_client.conn.lrange('OAT', 0, -1)
        self.all_spp = self.redis_client.conn.lrange('SPP', 0, -1)
        self.all_tou = self.redis_client.conn.lrange('tou', 0, -1)

        # cast all values to proper type
        self.start_hour_index = int(float(self.start_hour_index))
        self.all_ghi = [float(i) for i in self.all_ghi]
        self.all_oat = [float(i) for i in self.all_oat]
        self.all_spp = [float(i) for i in self.all_spp]

    def setup_base_problem(self):
        """
        Sets variable objects for CVX optimization problem. Includes "base home"
        systems of HVAC and water heater.
        :return: None
        """
        # Set up the solver parameters
        solvers = {"GUROBI": cp.GUROBI, "GLPK_MI": cp.GLPK_MI}
        try:
            self.solver = solvers[self.home['hems']['solver']]
        except:
            self.solver = cp.GUROBI

        # Set up the horizon for the MPC calc (min horizon = 1, no MPC)
        self.sub_subhourly_steps = max(1, int(self.home['hems']['sub_subhourly_steps']))
        self.dt = max(1, int(self.home['hems']['hourly_agg_steps'])) * self.sub_subhourly_steps
        self.horizon = max(1, int(self.home['hems']['horizon'] * self.dt))
        self.h_plus = self.horizon + 1

        # Initialize RP structure so that non-forecasted RPs have an expected value of 0.
        self.reward_price = np.zeros(self.horizon)

        self.home_r = cp.Constant(float(self.home["hvac"]["r"]))
        self.home_c = cp.Constant(float(self.home["hvac"]["c"]))
        self.hvac_p_c = cp.Constant(float(self.home["hvac"]["p_c"]))
        self.hvac_p_h = cp.Constant((float(self.home["hvac"]["p_h"])))
        self.wh_r = cp.Constant(float(self.home["wh"]["r"]))
        self.wh_c = cp.Constant(float(self.home["wh"]["c"]))
        self.wh_p = cp.Constant(float(self.home["wh"]["p"]))

        # Define optimization variables
        self.p_load = cp.Variable(self.horizon)
        self.temp_in = cp.Variable(self.h_plus)
        self.temp_wh = cp.Variable(self.h_plus)
        self.p_grid = cp.Variable(self.horizon)
        self.hvac_cool_on = cp.Variable(self.horizon, boolean=True)
        self.hvac_heat_on = cp.Variable(self.horizon, boolean=True)
        self.wh_heat_on = cp.Variable(self.horizon, boolean=True)

        # Water heater temperature constraints
        self.temp_wh_min = float(self.home["wh"]["temp_wh_min"])
        self.temp_wh_max = cp.Constant(float(self.home["wh"]["temp_wh_max"]))
        self.temp_wh_sp = cp.Constant(float(self.home["wh"]["temp_wh_sp"]))
        self.t_wh_init = float(self.home["wh"]["temp_wh_init"])
        self.wh_size = cp.Constant(float(self.home["wh"]["tank_size"]))
        self.tap_temp = cp.Constant(12) # assumed cold tap water is about 55 deg F

        # Home temperature constraints
        self.temp_in_min = cp.Constant(float(self.home["hvac"]["temp_in_min"]))
        self.temp_in_max = cp.Constant(float(self.home["hvac"]["temp_in_max"]))
        self.temp_in_sp = cp.Constant(float(self.home["hvac"]["temp_in_sp"]))
        self.t_in_init = float(self.home["hvac"]["temp_in_init"])

    def water_draws(self):
        # Do water draws with no prior knowledge
        draw_times = np.array(self.home["wh"]["draw_times"])
        draw_size_list = []
        for h in range(self.h_plus):
            t = self.timestep + (h % self.sub_subhourly_steps)
            if t in draw_times:
                ind = np.where(draw_times == t)[0]
                total_draw = sum(np.array(self.home["wh"]["draw_sizes"])[ind])
            else:
                total_draw = 0
            draw_size_list.append(total_draw)
        np.repeat(draw_size_list, self.sub_subhourly_steps)
        self.draw_size = cp.Constant(draw_size_list)
        # self.draw_size = cp.Constant(draw_size_list[0])
        # ed = sum(draw_size_list) / len(draw_size_list)
        # self.expected_draw = cp.Constant(ed)

    def set_environmental_variables(self):
        """
        Slices cast values of the environmental values for the current timestep.
        :return: None
        """
        start_slice = self.start_hour_index + self.timestep
        end_slice = start_slice + (self.horizon // self.sub_subhourly_steps) + 1 # Need to extend 1 timestep past horizon for OAT slice

        # Get the current values from a list of all values
        self.ghi_current = self.all_ghi[start_slice:end_slice]
        self.oat_current = self.all_oat[start_slice:end_slice]
        self.tou_current = self.all_tou[start_slice:end_slice]

        # Repeat the current values to align with intermediary optimization intervals
        self.tou_current = np.repeat(self.tou_current, self.sub_subhourly_steps)
        self.oat_current = np.repeat(self.oat_current, self.sub_subhourly_steps)
        self.ghi_current = np.repeat(self.ghi_current, self.sub_subhourly_steps)
        self.base_price = np.array(self.tou_current, dtype=float)

        # Set values as cvxpy values
        self.oat = cp.Constant(self.oat_current)
        self.ghi = cp.Constant(self.ghi_current)
        self.cast_redis_curr_rps()
        # self.set_vals_for_current_run()

    def setup_battery_problem(self):
        """
        Adds CVX variables for battery subsystem in battery and battery_pv homes.
        :return: None
        """
        # Define constants
        self.batt_max_rate = cp.Constant(float(self.home["battery"]["max_rate"]))
        self.batt_cap_total = cp.Constant(float(self.home["battery"]["capacity"]))
        self.batt_cap_min = cp.Constant(float(self.home["battery"]["capacity_lower"]))
        self.batt_cap_max = cp.Constant(float(self.home["battery"]["capacity_upper"]))
        self.batt_ch_eff = cp.Constant(float(self.home["battery"]["ch_eff"]))
        self.batt_disch_eff = cp.Constant(float(self.home["battery"]["disch_eff"]))
        self.batt_cons = cp.Constant(float(self.home["battery"]["batt_cons"]))

        # Define battery optimization variables
        self.p_batt_ch = cp.Variable(self.horizon)
        self.p_batt_disch = cp.Variable(self.horizon)
        self.e_batt = cp.Variable(self.h_plus)

    def setup_pv_problem(self):
        """
        Adds CVX variables for photovoltaic subsystem in pv and battery_pv homes.
        :return: None
        """
        # Define constants
        self.pv_area = cp.Constant(float(self.home["pv"]["area"]))
        self.pv_eff = cp.Constant(float(self.home["pv"]["eff"]))

        # Define PV Optimization variables
        self.p_pv = cp.Variable(self.horizon)
        self.u_pv_curt = cp.Variable(self.horizon)

    def get_initial_conditions(self):
        if self.timestep == 0:
            self.temp_in_init = cp.Constant(self.t_in_init)
            self.temp_wh_init = cp.Constant(self.t_wh_init)

            if 'battery' in self.type:
                self.e_batt_init = cp.Constant(float(self.home["battery"]["e_batt_init"]))
                self.p_batt_ch_init = cp.Constant(0)

        else:
            self.temp_in_init = cp.Constant(float(self.prev_optimal_vals["temp_in_opt"]))
            self.temp_wh_init = cp.Constant(float(self.prev_optimal_vals["temp_wh_opt"]))

            if 'battery' in self.type:
                self.e_batt_init = cp.Constant(float(self.prev_optimal_vals["e_batt_opt"]))
                self.p_batt_ch_init = cp.Constant(float(self.prev_optimal_vals["p_batt_ch"])
                                                - float(self.prev_optimal_vals["p_batt_disch"]))

    def add_base_constraints(self):
        """
        Creates the system dynamics for thermal energy storage systems: HVAC and
        water heater.
        :return: None
        """
        self.constraints = [
            # Indoor air temperature constraints
            self.temp_in[0] == self.temp_in_init,
            self.temp_in[1:self.h_plus] == self.temp_in[0:self.horizon]
                                            + (((self.oat[1:self.h_plus] - self.temp_in[0:self.horizon]) / self.home_r)
                                            - self.hvac_cool_on * self.hvac_p_c
                                            + self.hvac_heat_on * self.hvac_p_h) / (self.home_c * self.dt),
            self.temp_in[1:self.h_plus] >= self.temp_in_min,
            self.temp_in[1:self.h_plus] <= self.temp_in_max,

            # Hot water heater contraints
            self.temp_wh[0] == self.temp_wh_init,
            # self.temp_wh[1:] == (cp.multiply(self.temp_wh[:self.horizon],(self.wh_size - self.draw_size[1:]))/self.wh_size + cp.multiply(self.tap_temp, self.draw_size[1:])/self.wh_size)
            self.temp_wh[1:] == self.temp_wh[:self.horizon]
                                + (((self.temp_in[1:self.h_plus] - self.temp_wh[:self.horizon]) / self.wh_r)
                                + self.wh_heat_on * self.wh_p) / (self.wh_c * self.dt),

            self.temp_wh[1:self.h_plus] >= self.temp_wh_min,
            self.temp_wh[1:self.h_plus] <= self.temp_wh_max,

            self.p_load == self.hvac_p_c * self.hvac_cool_on + self.hvac_p_h * self.hvac_heat_on + self.wh_p * self.wh_heat_on,

            self.hvac_cool_on <= 1,
            self.hvac_cool_on >= 0,
            self.hvac_heat_on <= 1,
            self.hvac_heat_on >= 0,
            self.wh_heat_on <= 1,
            self.wh_heat_on >= 0
        ]

        # Set constraints on HVAC by season
        if max(self.oat_current) <= 26: # "winter"
            self.constraints += [self.hvac_cool_on == 0]

        if min(self.oat_current) >= 15: # "summer"
            self.constraints += [self.hvac_heat_on == 0]

        # set total price for electricity
        total_price_values = np.array(self.reward_price, dtype=float) + self.base_price[:self.horizon]
        self.total_price = cp.Constant(total_price_values)

    def add_battery_constraints(self):
        """
        Creates the system dynamics for chemical energy storage.
        :return: None
        """
        self.charge_mag = cp.Variable()
        self.constraints += [
            # Battery constraints
            self.e_batt[1:self.h_plus] == self.e_batt[0:self.horizon]
                                        + (self.batt_ch_eff * self.p_batt_ch[0:self.horizon]
                                        + self.p_batt_disch[0:self.horizon] / self.batt_disch_eff) / self.dt,
            self.e_batt[0] == self.e_batt_init,
            self.p_batt_ch[0:self.horizon] <= self.batt_max_rate,
            self.p_batt_ch[0:self.horizon] >= 0,
            -self.p_batt_disch[0:self.horizon] <= self.batt_max_rate,
            self.p_batt_disch[0:self.horizon] <= 0,
            self.e_batt[1:self.h_plus] <= self.batt_cap_max,
            self.e_batt[1:self.h_plus] >= self.batt_cap_min,
            self.p_load + self.p_batt_ch + self.p_batt_disch >= 0
        ]

    def add_pv_constraints(self):
        """
        Creates the system dynamics for photovoltaic generation. (Using measured GHI.)
        :return: None
        """
        self.constraints += [
            # PV constraints.  GHI provided in W/m2 - convert to kWh
            self.p_pv == self.pv_area * self.pv_eff * cp.multiply(self.ghi[0:self.horizon], (1 - self.u_pv_curt)) / 1000,
            self.u_pv_curt >= 0,
            self.u_pv_curt <= 1,
        ]

    def set_base_p_grid(self):
        """
        Sets p_grid of home to equal the load of the HVAC and water heater. To
        be used if and only if home type is base.
        :return: None
        """
        self.constraints += [
            # Set grid load
            self.p_grid == self.p_load # p_load = p_hvac + p_wh
        ]

    def set_battery_only_p_grid(self):
        """
        Sets p_grid of home to equal the load of the HVAC and water heater, plus
        or minus the charge/discharge of the battery. To be used if and only if
        home is of type battery_only.
        :return: None
        """
        self.constraints += [
            # Set grid load
            self.p_grid == self.p_load + self.p_batt_ch + self.p_batt_disch
        ]

    def set_pv_only_p_grid(self):
        """
        Sets p_grid of home equal to the load of the HVAC and water heater minus
        potential generation from the PV subsystem. To be used if and only if the
        home is of type pv_only.
        :return: None
        """
        self.constraints += [
            # Set grid load
            self.p_grid == self.p_load - self.p_pv
        ]

    def set_pv_battery_p_grid(self):
        """
        Sets p_grid of home equal to the load of the HVAC and water heater, plus
        or minus the charge/discharge of the battery, minus potential generation
        from the PV subsystem. To be used if and only if the home is of type pv_battery.
        :return: None
        """
        self.constraints += [
            # Set grid load
            self.p_grid == self.p_load + self.p_batt_ch + self.p_batt_disch - self.p_pv
        ]

    def solve_mpc(self):
        """
        Sets the objective function of the Home Energy Management System to be the
        minimization of cost over the MPC time horizon and solves via CVXPY.
        Used for all home types.
        :return: None
        """
        self.cost = cp.Variable(self.horizon)
        self.objective = cp.Variable(self.horizon)
        self.constraints += [self.cost == cp.multiply(self.total_price, self.p_grid)] # think this should work
        self.weights = cp.Constant(np.power(0.95*np.ones(self.horizon), np.arange(self.horizon)))
        self.obj = cp.Minimize(cp.sum(cp.multiply(self.weights, self.cost)))
        self.prob = cp.Problem(self.obj, self.constraints)
        if not self.prob.is_dcp():
            self.log.error("Problem is not DCP")
        try:
            self.prob.solve(solver=self.solver, verbose=self.verbose_flag)
            self.solved = True
        except:
            self.solved = False

    def get_min_hvac_setbacks(self):
        """
        Solves for the minimimum change required by the HEMS HVAC deadband in
        order to make the optimization feasible.
        Resets the HEMS constraints with the new temperature bounds.
        :return: None
        """
        self.log.info("Setting minimum changes to HVAC.")
        new_temp_in_min = cp.Variable()
        new_temp_in_max = cp.Variable()
        obj = cp.Minimize(new_temp_in_max - new_temp_in_min) # minimize change to deadband
        cons = [self.temp_in[0] == self.temp_in_init,
                self.temp_in[1:self.h_plus] == self.temp_in[0:self.horizon]
                                                + (((self.oat[1:self.h_plus] - self.temp_in[0:self.horizon]) / self.home_r)
                                                - self.hvac_cool_on * self.hvac_p_c
                                                + self.hvac_heat_on * self.hvac_p_h) / (self.home_c * self.dt),

                self.temp_in[1:self.h_plus] >= new_temp_in_min,
                self.temp_in[1:self.h_plus] <= new_temp_in_max,
                new_temp_in_min <= self.temp_in_min,
                new_temp_in_max >= self.temp_in_max,

                self.hvac_heat_on <= 1,
                self.hvac_heat_on >= 0,
                self.hvac_cool_on <= 1,
                self.hvac_cool_on >= 0,
                ]

        # set constraints on HVAC by season
        if max(self.oat_current) <= 26: # "winter"
            cons += [self.hvac_cool_on == 0]

        if min(self.oat_current) >= 15: # "summer"
            cons += [self.hvac_heat_on == 0]

        prob = cp.Problem(obj, cons)
        prob.solve(solver=self.solver, verbose=self.verbose_flag)
        self.temp_in_min = cp.Constant(new_temp_in_min.value)
        self.temp_in_max = cp.Constant(new_temp_in_max.value)
        self.hvac_cool_on = cp.Constant(self.hvac_cool_on.value)
        self.hvac_heat_on = cp.Constant(self.hvac_heat_on.value)

    def get_min_wh_setbacks(self):
        """
        Solves for the minimimum change required by the HEMS water heater deadband in
        order to make the optimization feasible.
        Resets the HEMS constraints with the new temperature bounds.
        :return: None
        """
        self.log.info("Setting minimum changes to water heater.")
        new_temp_wh_min = cp.Variable()
        new_temp_wh_max = cp.Variable()
        obj = cp.Minimize(cp.abs(self.temp_wh_min - new_temp_wh_min) + cp.abs(self.temp_wh_max - new_temp_wh_max)) # minimize change to deadband
        cons = [self.temp_wh[0] == self.temp_wh_init,
                # self.temp_wh[1:] == (cp.multiply(self.temp_wh[:self.horizon],(self.wh_size - self.draw_size[1:]))/self.wh_size + cp.multiply(self.tap_temp, self.draw_size[1:])/self.wh_size)
                self.temp_wh[1:] == self.temp_wh[:self.horizon]
                                    + (((self.temp_in[1:self.h_plus] - self.temp_wh[:self.horizon]) / self.wh_r)
                                    + self.wh_heat_on * self.wh_p) / (self.wh_c * self.dt),

                self.temp_wh >= new_temp_wh_min,
                self.temp_wh <= new_temp_wh_max,
                new_temp_wh_max >= self.temp_wh_max,
                new_temp_wh_min <= self.temp_wh_min,

                self.wh_heat_on >= 0,
                self.wh_heat_on <= 1
                ]
        prob = cp.Problem(obj, cons)
        prob.solve(solver=self.solver, verbose=self.verbose_flag)
        self.log.info(f"Problem status {prob.status}")
        self.temp_wh_min = cp.Constant(new_temp_wh_min.value)
        self.temp_wh_max = cp.Constant(new_temp_wh_max.value)
        self.wh_heat_on = cp.Constant(self.wh_heat_on.value)

    def get_alt_p_grid(self):
        self.log.info("Setting p_grid using alternate objectives.")
        self.constraints = [self.p_load == self.hvac_p_c * self.hvac_cool_on + self.hvac_p_h * self.hvac_heat_on + self.wh_p * self.wh_heat_on,
                            self.cost == cp.multiply(self.total_price, self.p_grid)] # reset constraints

        if self.type=="pv_battery":
            self.set_pv_battery_p_grid()
        elif self.type=="battery_only":
            self.set_battery_only_p_grid()
        elif self.type=="pv_only":
            self.set_pv_only_p_grid()
        else:
            self.set_base_p_grid()
        self.obj = cp.Minimize(cp.multiply(self.total_price, self.p_grid))
        self.prob = cp.Problem(self.obj, self.constraints)
        self.prob.solve(solver=self.solver, verbose=self.verbose_flag)
        self.log.info(f"Problem status {self.prob.status}")

    def error_handler(self):
        """
        Utilizes the CVXPY problem as setup previously to brute force a control signal.
        Turns on HVAC (cooling or heating) and water heater for all timesteps.
        May exceed the desired deadband conditions.
        Not intended to consider costs, only to resolve errors in normal solve process.
        :return:
        """
        new_temp_in_min = cp.Variable()
        new_temp_in_max = cp.Variable()
        new_temp_wh_min = cp.Variable()
        new_temp_wh_max = cp.Variable()
        obj = cp.Maximize(cp.sum(self.hvac_heat_on) + cp.sum(self.hvac_cool_on))
        cons = [self.temp_wh[0] == self.temp_wh_init,
                self.temp_wh[1:] == self.temp_wh[:self.horizon]
                                    + (((self.temp_in[1:self.h_plus] - self.temp_wh[:self.horizon]) / self.wh_r)
                                    + self.wh_heat_on * self.wh_p) / (self.wh_c * self.dt),

                self.temp_wh >= new_temp_wh_min,
                self.temp_wh <= new_temp_wh_max,
                new_temp_wh_max >= self.temp_wh_max,
                new_temp_wh_min <= self.temp_wh_min,

                self.wh_heat_on >= 0,
                self.wh_heat_on <= 1,
                self.wh_heat_on == 1,

                self.temp_in[0] == self.temp_in_init,
                self.temp_in[1:self.h_plus] == self.temp_in[0:self.horizon]
                                                + (((self.oat[1:self.h_plus] - self.temp_in[0:self.horizon]) / self.home_r)
                                                - self.hvac_cool_on * self.hvac_p_c
                                                + self.hvac_heat_on * self.hvac_p_h) / (self.home_c * self.dt),
                self.temp_in[1:self.h_plus] >= self.temp_in_min,
                self.temp_in[1:self.h_plus] <= self.temp_in_max,

                self.temp_in[1:self.h_plus] >= new_temp_in_min,
                self.temp_in[1:self.h_plus] <= new_temp_in_max,
                new_temp_in_min <= self.temp_in_min,
                new_temp_in_max >= self.temp_in_max,

                self.hvac_heat_on >= 0,
                self.hvac_heat_on <= 1,
                self.hvac_cool_on >= 0,
                self.hvac_cool_on <= 1,

                self.p_load == self.hvac_p_c * self.hvac_cool_on + self.hvac_p_h * self.hvac_heat_on + self.wh_p * self.wh_heat_on,
                self.p_grid == self.p_load,
                self.cost == cp.multiply(self.total_price, self.p_grid)
        ]

        if 'battery' in self.type:
            self.constraints += [self.p_batt_ch == 0,
                                 self.p_batt_disch == 0]

        if 'pv' in self.type:
            self.constraints += [self.u_pv_curt == 0]

        prob = cp.Problem(obj, cons)
        prob.solve(solver=self.solver, verbose=self.verbose_flag)

        self.temp_wh_min = cp.Constant(new_temp_wh_min.value)
        self.temp_wh_max = cp.Constant(new_temp_wh_max.value)
        self.temp_in_min = cp.Constant(new_temp_in_min.value)
        self.temp_in_max = cp.Constant(new_temp_in_max.value)

    def cleanup_and_finish(self):
        """
        Resolves .solve_mpc() with error handling and collects all data on solver.
        :return: None
        """
        n_iterations = 0
        while not self.solved and n_iterations < 10:
            self.log.error(f"Couldn't solve problem for {self.name} of type {self.home['type']}: {self.prob.status}")
            self.temp_in_min -= 0.2
            self.temp_wh_min -= 0.2
            self.solve_type_problem()
            n_iterations +=1

        if not self.solved:
            self.error_handler()

        end_slice = max(1, self.sub_subhourly_steps)
        self.log.info(f"Status for {self.name}: {self.prob.status}")
        try: # if the problem has been solved
            self.stored_optimal_vals = {
                "p_grid_opt": np.average(self.p_grid.value.reshape(self.sub_subhourly_steps, -1), axis=0),
                "p_load_opt": np.average(self.p_load.value.reshape(self.sub_subhourly_steps, -1), axis=0),
                "temp_in_opt": self.temp_in.value.reshape(self.sub_subhourly_steps, -1)[-1][1:],
                "temp_wh_opt": self.temp_wh.value.reshape(self.sub_subhourly_steps, -1)[-1][1:],
                "hvac_cool_on_opt": np.average(self.hvac_cool_on.value.reshape(self.sub_subhourly_steps, -1), axis=0),
                "hvac_heat_on_opt": np.average(self.hvac_heat_on.value.reshape(self.sub_subhourly_steps, -1), axis=0),
                "wh_heat_on_opt": np.average(self.wh_heat_on.value.reshape(self.sub_subhourly_steps, -1), axis=0),
                "cost_opt": np.average(self.cost.value.reshape(self.sub_subhourly_steps, -1), axis=0)
            }
            if 'pv' in self.type:
                self.stored_optimal_vals["p_pv_opt"] = np.average(self.p_pv.value.reshape(self.sub_subhourly_steps, -1), axis=0)
                self.stored_optimal_vals["u_pv_curt_opt"] = np.average(self.u_pv_curt.value.reshape(self.sub_subhourly_steps, -1), axis=0)
            if 'battery' in self.type:
                self.stored_optimal_vals["e_batt_opt"] = self.e_batt.value.reshape(self.sub_subhourly_steps, -1)[-1][1:]
                self.stored_optimal_vals["p_batt_ch"] = np.average(self.p_batt_ch.value.reshape(self.sub_subhourly_steps, -1), axis=0)
                self.stored_optimal_vals["p_batt_disch"] = np.average(self.p_batt_disch.value.reshape(self.sub_subhourly_steps, -1), axis=0)
        except:
            self.log.warning(f"Unable to solve for house {self.name}. Reverting to optimal solution from last timestep.")
            pass

        try:
            for k in self.stored_optimal_vals:
                self.optimal_vals[k] = self.stored_optimal_vals[k][0]
                self.stored_optimal_vals[k] = self.stored_optimal_vals[k][1:]
        except:
            self.error_handler()
        self.log.info(f"MPC solved with status {self.prob.status} for {self.name}; {self.optimal_vals}")

    def mpc_base(self):
        """
        Type specific routine for setting up a CVXPY optimization problem.
        self.home == "base"
        :return:
        """
        self.set_environmental_variables()
        self.add_base_constraints()
        self.set_base_p_grid()
        self.solve_mpc()

    def mpc_battery(self):
        """
        Type specific routine for setting up a CVXPY optimization problem.
        self.home == "battery_only"
        :return:
        """
        self.set_environmental_variables()
        self.add_base_constraints()
        self.add_battery_constraints()
        self.set_battery_only_p_grid()
        self.solve_mpc()

    def mpc_pv(self):
        """
        Type specific routine for setting up a CVXPY optimization problem.
        self.home == "pv_only"
        :return:
        """
        self.set_environmental_variables()
        self.add_base_constraints()
        self.add_pv_constraints()
        self.set_pv_only_p_grid()
        self.solve_mpc()

    def mpc_pv_battery(self):
        """
        Type specific routine for setting up a CVXPY optimization problem.
        self.home == "pv_battery"
        :return:
        """
        self.set_environmental_variables()
        self.add_base_constraints()
        self.add_battery_constraints()
        self.add_pv_constraints()
        self.set_pv_battery_p_grid()
        self.solve_mpc()

    def redis_get_initial_values(self):
        """
        Collects the values from the outside environment including GHI, OAT, and
        the base price set by the utility.
        :return: None
        """
        self.current_values = self.redis_client.conn.hgetall("current_values")

    def cast_redis_timestep(self):
        """
        Sets the timestep of the current time with respect to total simulation time.
        :return: None
        """
        self.timestep = int(self.current_values["timestep"])

    def cast_redis_curr_rps(self):
        """
        Casts the reward price signal values for the current timestep.
        :return: None
        """
        rp = self.redis_client.conn.lrange('reward_price', 0, -1)

        num_agg_steps_seen = int(np.ceil(self.horizon / self.sub_subhourly_steps))
        self.reward_price[:min(len(rp), num_agg_steps_seen)] = rp[:min(len(rp), num_agg_steps_seen)]
        self.reward_price = np.repeat(self.reward_price, self.sub_subhourly_steps)[:self.horizon]
        self.log.info(f"ts: {self.timestep}; RP: {self.reward_price[0]}")

    def solve_type_problem(self):
        """
        Selects routine for MPC optimization problem setup and solve using home type.
        :return: None
        """
        if self.type == "base":
            self.mpc_base()
        elif self.type == "battery_only":
            self.mpc_battery()
        elif self.type == "pv_only":
            self.mpc_pv()
        elif self.type == "pv_battery":
            self.mpc_pv_battery()

    def run_home(self):
        """
        Intended for parallelization in parent class (e.g. aggregator); runs a
        single MPCCalc home.
        :return: None
        """
        fh = logging.FileHandler(os.path.join("home_logs", f"{self.name}.log"))
        fh.setLevel(logging.WARN)

        self.log = pathos.logger(level=logging.INFO, handler=fh, name=self.name)

        self.redis_client = RedisClient()
        self.redis_get_initial_values()
        self.cast_redis_timestep()

        if self.timestep > 0:
            self.redis_get_prev_optimal_vals()

        self.get_initial_conditions()
        self.solve_type_problem()
        self.cleanup_and_finish()
        self.redis_write_optimal_vals()

        self.log.removeHandler(fh)

    def forecast_home(self):
        """
        Intended for parallelization in parent class (e.g. aggregator); runs a
        single MPCCalc home.
        For use of aggregator agent only; does not implement the solution on a house-by-house
        basis, only tells the forecasting agent what the expected p_grid_agg is for the community.
        :return: list (type float) of length self.horizon
        """
        fh = logging.FileHandler(os.path.join("home_logs", f"{self.name}.log"))
        fh.setLevel(logging.WARN)

        self.log = pathos.logger(level=logging.INFO, handler=fh, name=self.name)

        self.redis_client = RedisClient()
        self.redis_get_initial_values()
        self.cast_redis_timestep()

        if self.timestep > 0:
            self.redis_get_prev_optimal_vals()

        self.get_initial_conditions()
        self.solve_type_problem()
        self.cleanup_and_finish()

        self.log.removeHandler(fh)

        return self.p_grid.value.tolist()
