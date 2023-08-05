#!python
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
import numpy
cimport numpy
from libc.math cimport exp, fabs, log, sin, cos, tan, asin, acos, atan, isnan, isinf
from libc.math cimport NAN as nan
from libc.math cimport INFINITY as inf
from libc.stdio cimport *
from libc.stdlib cimport *
import cython
from cpython.mem cimport PyMem_Malloc
from cpython.mem cimport PyMem_Realloc
from cpython.mem cimport PyMem_Free
from hydpy.cythons.autogen import pointerutils
from hydpy.cythons.autogen cimport pointerutils
from hydpy.cythons.autogen cimport configutils
from hydpy.cythons.autogen cimport smoothutils
from hydpy.cythons.autogen cimport annutils
from hydpy.cythons.autogen cimport rootutils

@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double k
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class FluxSequences:
    cdef public double q
    cdef public int _q_ndim
    cdef public int _q_length
    cdef public double[:] _q_points
    cdef public double[:] _q_results
    cdef public double[:] _q_integrals
    cdef public double _q_sum
    cdef public bint _q_diskflag
    cdef public str _q_path
    cdef FILE *_q_file
    cdef public bint _q_ramflag
    cdef public double[:] _q_array
    cdef public bint _q_outputflag
    cdef double *_q_outputpointer
    cpdef open_files(self, int idx):
        if self._q_diskflag:
            self._q_file = fopen(str(self._q_path).encode(), "rb+")
            fseek(self._q_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._q_diskflag:
            fclose(self._q_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._q_diskflag:
            fread(&self.q, 8, 1, self._q_file)
        elif self._q_ramflag:
            self.q = self._q_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._q_diskflag:
            fwrite(&self.q, 8, 1, self._q_file)
        elif self._q_ramflag:
            self._q_array[idx] = self.q
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "q":
            self._q_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._q_outputflag:
            self._q_outputpointer[0] = self.q
@cython.final
cdef class StateSequences:
    cdef public double s
    cdef public int _s_ndim
    cdef public int _s_length
    cdef public double[:] _s_points
    cdef public double[:] _s_results
    cdef public bint _s_diskflag
    cdef public str _s_path
    cdef FILE *_s_file
    cdef public bint _s_ramflag
    cdef public double[:] _s_array
    cdef public bint _s_outputflag
    cdef double *_s_outputpointer
    cpdef open_files(self, int idx):
        if self._s_diskflag:
            self._s_file = fopen(str(self._s_path).encode(), "rb+")
            fseek(self._s_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._s_diskflag:
            fclose(self._s_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._s_diskflag:
            fread(&self.s, 8, 1, self._s_file)
        elif self._s_ramflag:
            self.s = self._s_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._s_diskflag:
            fwrite(&self.s, 8, 1, self._s_file)
        elif self._s_ramflag:
            self._s_array[idx] = self.s
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "s":
            self._s_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._s_outputflag:
            self._s_outputpointer[0] = self.s
@cython.final
cdef class NumConsts:
    cdef public numpy.int32_t nmb_methods
    cdef public numpy.int32_t nmb_stages
    cdef public double dt_increase
    cdef public double dt_decrease
    cdef public configutils.Config pub
    cdef public double[:, :, :] a_coefs
cdef class NumVars:
    cdef public bint use_relerror
    cdef public numpy.int32_t nmb_calls
    cdef public numpy.int32_t idx_method
    cdef public numpy.int32_t idx_stage
    cdef public double t0
    cdef public double t1
    cdef public double dt
    cdef public double dt_est
    cdef public double abserror
    cdef public double relerror
    cdef public double last_abserror
    cdef public double last_relerror
    cdef public double extrapolated_abserror
    cdef public double extrapolated_relerror
    cdef public bint f0_ready

@cython.final
cdef class Model:
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public NumConsts numconsts
    cdef public NumVars numvars
    cpdef inline void simulate(self, int idx)  nogil:
        self.idx_sim = idx
        self.solve()
        self.update_outputs()
    cpdef inline void open_files(self):
        self.sequences.fluxes.open_files(self.idx_sim)
        self.sequences.states.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.fluxes.close_files()
        self.sequences.states.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.fluxes.save_data(self.idx_sim)
        self.sequences.states.save_data(self.idx_sim)
    cpdef inline void new2old(self) nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        self.sequences.old_states.s = self.sequences.new_states.s
    cpdef inline void update_inlets(self) nogil:
        pass
    cpdef inline void update_outlets(self) nogil:
        pass
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) nogil:
        self.sequences.fluxes.update_outputs()
        self.sequences.states.update_outputs()
    cpdef inline void solve(self)  nogil:
        cdef int decrease_dt
        self.numvars.use_relerror = not isnan(            self.parameters.solver.relerrormax)
        self.numvars.t0, self.numvars.t1 = 0., 1.
        self.numvars.dt_est = 1.*self.parameters.solver.reldtmax
        self.numvars.f0_ready = False
        self.reset_sum_fluxes()
        while self.numvars.t0 < self.numvars.t1-1e-14:
            self.numvars.last_abserror = inf
            self.numvars.last_relerror = inf
            self.numvars.dt = min(                self.numvars.t1-self.numvars.t0,                1.*self.parameters.solver.reldtmax,                max(self.numvars.dt_est, self.parameters.solver.reldtmin))
            if not self.numvars.f0_ready:
                self.calculate_single_terms()
                self.numvars.idx_method = 0
                self.numvars.idx_stage = 0
                self.set_point_fluxes()
                self.set_point_states()
                self.set_result_states()
            for self.numvars.idx_method in range(                    1, self.numconsts.nmb_methods+1):
                for self.numvars.idx_stage in range(                        1, self.numvars.idx_method):
                    self.get_point_states()
                    self.calculate_single_terms()
                    self.set_point_fluxes()
                for self.numvars.idx_stage in range(                        1, self.numvars.idx_method+1):
                    self.integrate_fluxes()
                    self.calculate_full_terms()
                    self.set_point_states()
                self.set_result_fluxes()
                self.set_result_states()
                self.calculate_error()
                self.extrapolate_error()
                if self.numvars.idx_method == 1:
                    continue
                if ((self.numvars.abserror <=                     self.parameters.solver.abserrormax) or                        (self.numvars.relerror <=                         self.parameters.solver.relerrormax)):
                    self.numvars.dt_est =                         self.numconsts.dt_increase*self.numvars.dt
                    self.numvars.f0_ready = False
                    self.addup_fluxes()
                    self.numvars.t0 = self.numvars.t0+self.numvars.dt
                    self.new2old()
                    break
                decrease_dt = self.numvars.dt > self.parameters.solver.reldtmin
                decrease_dt = decrease_dt and (                    self.numvars.extrapolated_abserror >                    self.parameters.solver.abserrormax)
                if self.numvars.use_relerror:
                    decrease_dt = decrease_dt and (                        self.numvars.extrapolated_relerror >                        self.parameters.solver.relerrormax)
                if decrease_dt:
                    self.numvars.f0_ready = True
                    self.numvars.dt_est = (self.numvars.dt /                                           self.numconsts.dt_decrease)
                    break
                self.numvars.last_abserror = self.numvars.abserror
                self.numvars.last_relerror = self.numvars.relerror
                self.numvars.f0_ready = True
            else:
                if self.numvars.dt <= self.parameters.solver.reldtmin:
                    self.numvars.f0_ready = False
                    self.addup_fluxes()
                    self.numvars.t0 = self.numvars.t0+self.numvars.dt
                    self.new2old()
                else:
                    self.numvars.f0_ready = True
                    self.numvars.dt_est = (self.numvars.dt /                                           self.numconsts.dt_decrease)
        self.get_sum_fluxes()
    cpdef inline void calculate_single_terms(self) nogil:
        self.numvars.nmb_calls =self.numvars.nmb_calls+1
        self.calc_q_v1()
    cpdef inline void calculate_full_terms(self) nogil:
        self.calc_s_v1()
    cpdef inline void get_point_states(self) nogil:
        self.sequences.states.s = self.sequences.states._s_points[self.numvars.idx_stage]
    cpdef inline void set_point_states(self) nogil:
        self.sequences.states._s_points[self.numvars.idx_stage] = self.sequences.states.s
    cpdef inline void set_result_states(self) nogil:
        self.sequences.states._s_results[self.numvars.idx_method] = self.sequences.states.s
    cpdef inline void get_sum_fluxes(self) nogil:
        self.sequences.fluxes.q = self.sequences.fluxes._q_sum
    cpdef inline void set_point_fluxes(self) nogil:
        self.sequences.fluxes._q_points[self.numvars.idx_stage] = self.sequences.fluxes.q
    cpdef inline void set_result_fluxes(self) nogil:
        self.sequences.fluxes._q_results[self.numvars.idx_method] = self.sequences.fluxes.q
    cpdef inline void integrate_fluxes(self) nogil:
        cdef int jdx
        self.sequences.fluxes.q = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.q = self.sequences.fluxes.q +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._q_points[jdx]
    cpdef inline void reset_sum_fluxes(self) nogil:
        self.sequences.fluxes._q_sum = 0.
    cpdef inline void addup_fluxes(self) nogil:
        self.sequences.fluxes._q_sum = self.sequences.fluxes._q_sum + self.sequences.fluxes.q
    cpdef inline void calculate_error(self) nogil:
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._q_results[self.numvars.idx_method]-self.sequences.fluxes._q_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._q_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._q_results[self.numvars.idx_method]))
    cpdef inline void extrapolate_error(self)  nogil:
        if self.numvars.idx_method > 2:
            self.numvars.extrapolated_abserror = exp(                log(self.numvars.abserror) +                (log(self.numvars.abserror) -                 log(self.numvars.last_abserror)) *                (self.numconsts.nmb_methods-self.numvars.idx_method))
        else:
            self.numvars.extrapolated_abserror = -999.9
        if self.numvars.use_relerror:
            if self.numvars.idx_method > 2:
                self.numvars.extrapolated_relerror = exp(                    log(self.numvars.relerror) +                    (log(self.numvars.relerror) -                     log(self.numvars.last_relerror)) *                    (self.numconsts.nmb_methods - self.numvars.idx_method))
            else:
                self.numvars.extrapolated_relerror = -999.9
        else:
            self.numvars.extrapolated_relerror = inf
    cpdef inline void calc_q_v1(self)  nogil:
        self.sequences.fluxes.q = self.parameters.control.k*self.sequences.states.s
    cpdef inline void calc_q(self)  nogil:
        self.sequences.fluxes.q = self.parameters.control.k*self.sequences.states.s
    cpdef inline void calc_s_v1(self)  nogil:
        self.sequences.new_states.s = self.sequences.old_states.s-self.sequences.fluxes.q
    cpdef inline void calc_s(self)  nogil:
        self.sequences.new_states.s = self.sequences.old_states.s-self.sequences.fluxes.q
