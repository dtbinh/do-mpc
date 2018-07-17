#
#   This file is part of do-mpc
#
#   do-mpc: An environment for the easy, modular and efficient implementation of
#        robust nonlinear model predictive control
#
#   Copyright (c) 2014-2016 Sergio Lucia, Alexandru Tatulea-Codrean
#                        TU Dortmund. All rights reserved
#
#   do-mpc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as
#   published by the Free Software Foundation, either version 3
#   of the License, or (at your option) any later version.
#
#   do-mpc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with do-mpc.  If not, see <http://www.gnu.org/licenses/>.
#

from casadi import *
import core_do_mpc
import numpy as NP
def observer(model):

	method = 'MHE' # 'EKF' or 'MHE' or 'state-feedback'

	"""
	--------------------------------------------------------------------------
	template_observer: preprocess model information
	--------------------------------------------------------------------------
	"""

	# Variables
	x = model.x
	u = model.u
	p = model.p
	tv_p = model.tv_p
	y = model.y
	meas_fcn = Function("meas_fcn",[x,u,p,tv_p],[y])

	nx = x.size(1)
	nu = u.size(1)
	np = p.size(1)
	ny = y.size(1)

	"""
	--------------------------------------------------------------------------
	template_observer: integration options
	--------------------------------------------------------------------------
	"""
	# Choose the simulator time step
	t_step_observer = 0.005
	# Choose options for the integrator
	opts = {"abstol":1e-10,"reltol":1e-10, 'tf':t_step_observer}
	# Choose integrator: for example 'cvodes' for ODEs or 'idas' for DAEs
	integration_tool = 'cvodes'

	"""
	--------------------------------------------------------------------------
	template_observer: tuning parameters
	--------------------------------------------------------------------------
	"""

	# Prediction horizon
	n_horizon = 10
	# Robust horizon, set to 0 for standard NMPC
	n_robust = 0
	# open_loop robust NMPC (1) or multi-stage NMPC (0). Only important if n_robust > 0
	open_loop = 0
	# Choose if optimal control instead of MPC
	optimal_control = 0
	# Sampling time
	t_step = 0.005
	# Choose type of state discretization (collocation or multiple-shooting)
	state_discretization = 'collocation'
	# Degree of interpolating polynomials: 1 to 5
	poly_degree = 2
	# Collocation points: 'legendre' or 'radau'
	collocation = 'radau'
	# Number of finite elements per control interval
	n_fin_elem = 3
	# NLP Solver and linear solver
	nlp_solver = 'ipopt'
	qp_solver = 'qpoases'

	# It is highly recommended that you use a more efficient linear solver
	# such as the hsl linear solver MA27, which can be downloaded as a precompiled
	# library and can be used by IPOPT on run time

	linear_solver = 'ma27'

	# GENERATE C CODE shared libraries NOTE: Not currently supported
	generate_code = 0

	"""
	--------------------------------------------------------------------------
	template_optimizer: uncertain parameters
	--------------------------------------------------------------------------
	"""
	# Define the different possible values of the uncertain parameters in the scenario tree
	alpha_values = NP.array([1.0, 1.1, 0.9])
	beta_values = NP.array([1.0, 1.1, 0.9])
	uncertainty_values = NP.array([alpha_values,beta_values])

	"""
	--------------------------------------------------------------------------
	template_observer: tuning parameters mhe
	--------------------------------------------------------------------------
	"""

	P_states = NP.diag(NP.ones(nx))*0

	P_param = NP.diag([np])

	P_inputs = NP.diag(NP.ones([nu]))*1e5

	# P_meas = NP.diag([10000, 1, 1, 1, 1])
	P_meas = NP.diag([1.0, 100.0, 1.0])
	# P_meas = NP.diag([1.0, 100.0, 100.0])

	"""
	--------------------------------------------------------------------------
	template_observer: measurement function
	--------------------------------------------------------------------------
	"""

	noise = 'gaussian'
	mag = NP.array([0.01, 0.001, 0.001]) #standard deviation


	"""
	--------------------------------------------------------------------------
	template_observer: pass information (not necessary to edit)
	--------------------------------------------------------------------------
	"""
	observer_dict = {'n_horizon':n_horizon,'state_discretization':state_discretization,
	'poly_degree':poly_degree,'collocation':collocation,'n_fin_elem':n_fin_elem,
	'nlp_solver':nlp_solver,'qp_solver':qp_solver,'linear_solver':linear_solver,
	'generate_code':generate_code,'x':x,'meas_fcn':meas_fcn,'noise':noise,
	'mag':mag,'t_step':t_step,'open_loop':open_loop,'n_robust':n_robust,
	'integration_tool':integration_tool,'method':method,
	't_step_observer': t_step_observer, 'integrator_opts': opts,
	'P_states': P_states, 'P_param': P_param, 'P_inputs': P_inputs,
	'P_meas': P_meas, 'uncertainty_values':uncertainty_values}

	observer_1 = core_do_mpc.observer(model,observer_dict)

	return observer_1
