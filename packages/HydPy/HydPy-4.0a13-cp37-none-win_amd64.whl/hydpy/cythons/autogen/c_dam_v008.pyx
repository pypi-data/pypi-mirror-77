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
    cdef public DerivedParameters derived
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double catchmentarea
    cdef public double[:] neardischargeminimumthreshold
    cdef public double[:] watervolumeminimumthreshold
    cdef public annutils.ANN watervolume2waterlevel
    cdef public annutils.SeasonalANN waterlevel2flooddischarge
    cdef public double allowedwaterleveldrop
    cdef public double[:] allowedrelease
    cdef public double[:] targetvolume
    cdef public double targetrangeabsolute
    cdef public double targetrangerelative
    cdef public double volumetolerance
    cdef public double dischargetolerance
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int32_t[:] toy
    cdef public double seconds
    cdef public double volumesmoothparlog1
    cdef public double volumesmoothparlog2
    cdef public double dischargesmoothpar
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InletSequences:
    cdef double *q
    cdef public int _q_ndim
    cdef public int _q_length
    cpdef inline set_pointer0d(self, str name, pointerutils.PDouble value):
        if name == "q":
            self.q = value.p_value
    cpdef get_value(self, str name):
        cdef int idx
        if name == "q":
            return self.q[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self.q[0] = value
@cython.final
cdef class FluxSequences:
    cdef public double inflow
    cdef public int _inflow_ndim
    cdef public int _inflow_length
    cdef public double[:] _inflow_points
    cdef public double[:] _inflow_results
    cdef public double[:] _inflow_integrals
    cdef public double _inflow_sum
    cdef public bint _inflow_diskflag
    cdef public str _inflow_path
    cdef FILE *_inflow_file
    cdef public bint _inflow_ramflag
    cdef public double[:] _inflow_array
    cdef public bint _inflow_outputflag
    cdef double *_inflow_outputpointer
    cdef public double actualrelease
    cdef public int _actualrelease_ndim
    cdef public int _actualrelease_length
    cdef public double[:] _actualrelease_points
    cdef public double[:] _actualrelease_results
    cdef public double[:] _actualrelease_integrals
    cdef public double _actualrelease_sum
    cdef public bint _actualrelease_diskflag
    cdef public str _actualrelease_path
    cdef FILE *_actualrelease_file
    cdef public bint _actualrelease_ramflag
    cdef public double[:] _actualrelease_array
    cdef public bint _actualrelease_outputflag
    cdef double *_actualrelease_outputpointer
    cdef public double flooddischarge
    cdef public int _flooddischarge_ndim
    cdef public int _flooddischarge_length
    cdef public double[:] _flooddischarge_points
    cdef public double[:] _flooddischarge_results
    cdef public double[:] _flooddischarge_integrals
    cdef public double _flooddischarge_sum
    cdef public bint _flooddischarge_diskflag
    cdef public str _flooddischarge_path
    cdef FILE *_flooddischarge_file
    cdef public bint _flooddischarge_ramflag
    cdef public double[:] _flooddischarge_array
    cdef public bint _flooddischarge_outputflag
    cdef double *_flooddischarge_outputpointer
    cdef public double outflow
    cdef public int _outflow_ndim
    cdef public int _outflow_length
    cdef public double[:] _outflow_points
    cdef public double[:] _outflow_results
    cdef public double[:] _outflow_integrals
    cdef public double _outflow_sum
    cdef public bint _outflow_diskflag
    cdef public str _outflow_path
    cdef FILE *_outflow_file
    cdef public bint _outflow_ramflag
    cdef public double[:] _outflow_array
    cdef public bint _outflow_outputflag
    cdef double *_outflow_outputpointer
    cpdef open_files(self, int idx):
        if self._inflow_diskflag:
            self._inflow_file = fopen(str(self._inflow_path).encode(), "rb+")
            fseek(self._inflow_file, idx*8, SEEK_SET)
        if self._actualrelease_diskflag:
            self._actualrelease_file = fopen(str(self._actualrelease_path).encode(), "rb+")
            fseek(self._actualrelease_file, idx*8, SEEK_SET)
        if self._flooddischarge_diskflag:
            self._flooddischarge_file = fopen(str(self._flooddischarge_path).encode(), "rb+")
            fseek(self._flooddischarge_file, idx*8, SEEK_SET)
        if self._outflow_diskflag:
            self._outflow_file = fopen(str(self._outflow_path).encode(), "rb+")
            fseek(self._outflow_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._inflow_diskflag:
            fclose(self._inflow_file)
        if self._actualrelease_diskflag:
            fclose(self._actualrelease_file)
        if self._flooddischarge_diskflag:
            fclose(self._flooddischarge_file)
        if self._outflow_diskflag:
            fclose(self._outflow_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._inflow_diskflag:
            fread(&self.inflow, 8, 1, self._inflow_file)
        elif self._inflow_ramflag:
            self.inflow = self._inflow_array[idx]
        if self._actualrelease_diskflag:
            fread(&self.actualrelease, 8, 1, self._actualrelease_file)
        elif self._actualrelease_ramflag:
            self.actualrelease = self._actualrelease_array[idx]
        if self._flooddischarge_diskflag:
            fread(&self.flooddischarge, 8, 1, self._flooddischarge_file)
        elif self._flooddischarge_ramflag:
            self.flooddischarge = self._flooddischarge_array[idx]
        if self._outflow_diskflag:
            fread(&self.outflow, 8, 1, self._outflow_file)
        elif self._outflow_ramflag:
            self.outflow = self._outflow_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._inflow_diskflag:
            fwrite(&self.inflow, 8, 1, self._inflow_file)
        elif self._inflow_ramflag:
            self._inflow_array[idx] = self.inflow
        if self._actualrelease_diskflag:
            fwrite(&self.actualrelease, 8, 1, self._actualrelease_file)
        elif self._actualrelease_ramflag:
            self._actualrelease_array[idx] = self.actualrelease
        if self._flooddischarge_diskflag:
            fwrite(&self.flooddischarge, 8, 1, self._flooddischarge_file)
        elif self._flooddischarge_ramflag:
            self._flooddischarge_array[idx] = self.flooddischarge
        if self._outflow_diskflag:
            fwrite(&self.outflow, 8, 1, self._outflow_file)
        elif self._outflow_ramflag:
            self._outflow_array[idx] = self.outflow
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "inflow":
            self._inflow_outputpointer = value.p_value
        if name == "actualrelease":
            self._actualrelease_outputpointer = value.p_value
        if name == "flooddischarge":
            self._flooddischarge_outputpointer = value.p_value
        if name == "outflow":
            self._outflow_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._inflow_outputflag:
            self._inflow_outputpointer[0] = self.inflow
        if self._actualrelease_outputflag:
            self._actualrelease_outputpointer[0] = self.actualrelease
        if self._flooddischarge_outputflag:
            self._flooddischarge_outputpointer[0] = self.flooddischarge
        if self._outflow_outputflag:
            self._outflow_outputpointer[0] = self.outflow
@cython.final
cdef class StateSequences:
    cdef public double watervolume
    cdef public int _watervolume_ndim
    cdef public int _watervolume_length
    cdef public double[:] _watervolume_points
    cdef public double[:] _watervolume_results
    cdef public bint _watervolume_diskflag
    cdef public str _watervolume_path
    cdef FILE *_watervolume_file
    cdef public bint _watervolume_ramflag
    cdef public double[:] _watervolume_array
    cdef public bint _watervolume_outputflag
    cdef double *_watervolume_outputpointer
    cpdef open_files(self, int idx):
        if self._watervolume_diskflag:
            self._watervolume_file = fopen(str(self._watervolume_path).encode(), "rb+")
            fseek(self._watervolume_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._watervolume_diskflag:
            fclose(self._watervolume_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._watervolume_diskflag:
            fread(&self.watervolume, 8, 1, self._watervolume_file)
        elif self._watervolume_ramflag:
            self.watervolume = self._watervolume_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._watervolume_diskflag:
            fwrite(&self.watervolume, 8, 1, self._watervolume_file)
        elif self._watervolume_ramflag:
            self._watervolume_array[idx] = self.watervolume
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "watervolume":
            self._watervolume_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._watervolume_outputflag:
            self._watervolume_outputpointer[0] = self.watervolume
@cython.final
cdef class AideSequences:
    cdef public double waterlevel
    cdef public int _waterlevel_ndim
    cdef public int _waterlevel_length
    cdef public double[:] _waterlevel_points
    cdef public double[:] _waterlevel_results
    cdef public double surfacearea
    cdef public int _surfacearea_ndim
    cdef public int _surfacearea_length
    cdef public double[:] _surfacearea_points
    cdef public double[:] _surfacearea_results
    cdef public double alloweddischarge
    cdef public int _alloweddischarge_ndim
    cdef public int _alloweddischarge_length
    cdef public double[:] _alloweddischarge_points
    cdef public double[:] _alloweddischarge_results
@cython.final
cdef class OutletSequences:
    cdef double *q
    cdef public int _q_ndim
    cdef public int _q_length
    cpdef inline set_pointer0d(self, str name, pointerutils.PDouble value):
        if name == "q":
            self.q = value.p_value
    cpdef get_value(self, str name):
        cdef int idx
        if name == "q":
            return self.q[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self.q[0] = value
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
        self.update_inlets()
        self.solve()
        self.update_outlets()
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
        self.sequences.old_states.watervolume = self.sequences.new_states.watervolume
    cpdef inline void update_inlets(self) nogil:
        self.pic_inflow_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_outflow_v1()
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
        self.pic_inflow_v1()
        self.calc_waterlevel_v1()
        self.calc_surfacearea_v1()
        self.calc_alloweddischarge_v2()
        self.calc_actualrelease_v3()
        self.calc_flooddischarge_v1()
        self.calc_outflow_v1()
    cpdef inline void calculate_full_terms(self) nogil:
        self.update_watervolume_v1()
    cpdef inline void get_point_states(self) nogil:
        self.sequences.states.watervolume = self.sequences.states._watervolume_points[self.numvars.idx_stage]
    cpdef inline void set_point_states(self) nogil:
        self.sequences.states._watervolume_points[self.numvars.idx_stage] = self.sequences.states.watervolume
    cpdef inline void set_result_states(self) nogil:
        self.sequences.states._watervolume_results[self.numvars.idx_method] = self.sequences.states.watervolume
    cpdef inline void get_sum_fluxes(self) nogil:
        self.sequences.fluxes.inflow = self.sequences.fluxes._inflow_sum
        self.sequences.fluxes.actualrelease = self.sequences.fluxes._actualrelease_sum
        self.sequences.fluxes.flooddischarge = self.sequences.fluxes._flooddischarge_sum
        self.sequences.fluxes.outflow = self.sequences.fluxes._outflow_sum
    cpdef inline void set_point_fluxes(self) nogil:
        self.sequences.fluxes._inflow_points[self.numvars.idx_stage] = self.sequences.fluxes.inflow
        self.sequences.fluxes._actualrelease_points[self.numvars.idx_stage] = self.sequences.fluxes.actualrelease
        self.sequences.fluxes._flooddischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._outflow_points[self.numvars.idx_stage] = self.sequences.fluxes.outflow
    cpdef inline void set_result_fluxes(self) nogil:
        self.sequences.fluxes._inflow_results[self.numvars.idx_method] = self.sequences.fluxes.inflow
        self.sequences.fluxes._actualrelease_results[self.numvars.idx_method] = self.sequences.fluxes.actualrelease
        self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method] = self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._outflow_results[self.numvars.idx_method] = self.sequences.fluxes.outflow
    cpdef inline void integrate_fluxes(self) nogil:
        cdef int jdx
        self.sequences.fluxes.inflow = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._inflow_points[jdx]
        self.sequences.fluxes.actualrelease = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.actualrelease = self.sequences.fluxes.actualrelease +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._actualrelease_points[jdx]
        self.sequences.fluxes.flooddischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.flooddischarge = self.sequences.fluxes.flooddischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._flooddischarge_points[jdx]
        self.sequences.fluxes.outflow = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.outflow = self.sequences.fluxes.outflow +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._outflow_points[jdx]
    cpdef inline void reset_sum_fluxes(self) nogil:
        self.sequences.fluxes._inflow_sum = 0.
        self.sequences.fluxes._actualrelease_sum = 0.
        self.sequences.fluxes._flooddischarge_sum = 0.
        self.sequences.fluxes._outflow_sum = 0.
    cpdef inline void addup_fluxes(self) nogil:
        self.sequences.fluxes._inflow_sum = self.sequences.fluxes._inflow_sum + self.sequences.fluxes.inflow
        self.sequences.fluxes._actualrelease_sum = self.sequences.fluxes._actualrelease_sum + self.sequences.fluxes.actualrelease
        self.sequences.fluxes._flooddischarge_sum = self.sequences.fluxes._flooddischarge_sum + self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._outflow_sum = self.sequences.fluxes._outflow_sum + self.sequences.fluxes.outflow
    cpdef inline void calculate_error(self) nogil:
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._inflow_results[self.numvars.idx_method]-self.sequences.fluxes._inflow_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._inflow_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._inflow_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._actualrelease_results[self.numvars.idx_method]-self.sequences.fluxes._actualrelease_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._actualrelease_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._actualrelease_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method]-self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._outflow_results[self.numvars.idx_method]-self.sequences.fluxes._outflow_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._outflow_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._outflow_results[self.numvars.idx_method]))
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
    cpdef inline void pic_inflow_v1(self)  nogil:
        self.sequences.fluxes.inflow = self.sequences.inlets.q[0]
    cpdef inline void pic_inflow(self)  nogil:
        self.sequences.fluxes.inflow = self.sequences.inlets.q[0]
    cpdef inline void calc_waterlevel_v1(self)  nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.sequences.aides.waterlevel = self.parameters.control.watervolume2waterlevel.outputs[0]
    cpdef inline void calc_surfacearea_v1(self)  nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.parameters.control.watervolume2waterlevel.calculate_derivatives(0)
        self.sequences.aides.surfacearea = 1./self.parameters.control.watervolume2waterlevel.output_derivatives[0]
    cpdef inline void calc_alloweddischarge_v2(self)  nogil:
        self.sequences.aides.alloweddischarge = smoothutils.smooth_min1(            self.parameters.control.allowedwaterleveldrop/self.parameters.derived.seconds*self.sequences.aides.surfacearea*1e6 +            self.sequences.fluxes.inflow,            self.parameters.control.allowedrelease[self.parameters.derived.toy[self.idx_sim]],            self.parameters.derived.dischargesmoothpar,        )
    cpdef inline void calc_actualrelease_v3(self)  nogil:
        cdef double d_weight
        cdef double d_release2
        cdef double d_neutral
        cdef double d_release1
        cdef double d_upperbound
        cdef double d_factor
        cdef double d_qmax
        cdef double d_qmin
        cdef double d_range
        cdef double d_target
        cdef int idx_toy
        idx_toy = self.parameters.derived.toy[self.idx_sim]
        d_target = self.parameters.control.targetvolume[idx_toy]
        d_range = max(            max(                self.parameters.control.targetrangeabsolute,                self.parameters.control.targetrangerelative*d_target),            1e-6,        )
        d_qmin = self.parameters.control.neardischargeminimumthreshold[idx_toy]
        d_qmax = smoothutils.smooth_max1(            d_qmin,            self.sequences.aides.alloweddischarge,            self.parameters.derived.dischargesmoothpar        )
        d_factor = smoothutils.smooth_logistic3(            (self.sequences.new_states.watervolume-d_target+d_range)/d_range,            self.parameters.derived.volumesmoothparlog2,        )
        d_upperbound = smoothutils.smooth_min1(            d_qmax,            self.sequences.fluxes.inflow,            self.parameters.derived.dischargesmoothpar        )
        d_release1 = (            (1.-d_factor)*d_qmin +            d_factor*smoothutils.smooth_max1(                d_qmin,                d_upperbound,                self.parameters.derived.dischargesmoothpar,            )        )
        d_factor = smoothutils.smooth_logistic3(            (d_target+d_range-self.sequences.new_states.watervolume)/d_range,            self.parameters.derived.volumesmoothparlog2,        )
        d_neutral = smoothutils.smooth_max1(            d_qmin,            self.sequences.fluxes.inflow,            self.parameters.derived.dischargesmoothpar        )
        d_release2 = (            (1.-d_factor)*d_qmax +            d_factor*smoothutils.smooth_min1(                d_qmax,                d_neutral,                self.parameters.derived.dischargesmoothpar,            )        )
        d_weight = smoothutils.smooth_logistic1(            d_target-self.sequences.new_states.watervolume,            self.parameters.derived.volumesmoothparlog1        )
        self.sequences.fluxes.actualrelease = d_weight*d_release1+(1.-d_weight)*d_release2
        if self.parameters.derived.volumesmoothparlog1 > 0.:
            d_weight = exp(                -((self.sequences.new_states.watervolume-d_target)/self.parameters.derived.volumesmoothparlog1)**2            )
        else:
            d_weight = 0.
        d_neutral = smoothutils.smooth_max1(            d_upperbound,            d_qmin,            self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.actualrelease = d_weight*d_neutral+(1.-d_weight)*self.sequences.fluxes.actualrelease
        self.sequences.fluxes.actualrelease = smoothutils.smooth_max1(            self.sequences.fluxes.actualrelease,            0.,            self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.actualrelease = self.sequences.fluxes.actualrelease * (smoothutils.smooth_logistic1(            self.sequences.new_states.watervolume-self.parameters.control.watervolumeminimumthreshold[idx_toy],            self.parameters.derived.volumesmoothparlog1        ))
    cpdef inline void calc_flooddischarge_v1(self)  nogil:
        self.parameters.control.waterlevel2flooddischarge.inputs[0] = self.sequences.aides.waterlevel
        self.parameters.control.waterlevel2flooddischarge.calculate_values(self.parameters.derived.toy[self.idx_sim])
        self.sequences.fluxes.flooddischarge = self.parameters.control.waterlevel2flooddischarge.outputs[0]
    cpdef inline void calc_outflow_v1(self)  nogil:
        self.sequences.fluxes.outflow = max(self.sequences.fluxes.actualrelease + self.sequences.fluxes.flooddischarge, 0.)
    cpdef inline void calc_waterlevel(self)  nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.sequences.aides.waterlevel = self.parameters.control.watervolume2waterlevel.outputs[0]
    cpdef inline void calc_surfacearea(self)  nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.parameters.control.watervolume2waterlevel.calculate_derivatives(0)
        self.sequences.aides.surfacearea = 1./self.parameters.control.watervolume2waterlevel.output_derivatives[0]
    cpdef inline void calc_alloweddischarge(self)  nogil:
        self.sequences.aides.alloweddischarge = smoothutils.smooth_min1(            self.parameters.control.allowedwaterleveldrop/self.parameters.derived.seconds*self.sequences.aides.surfacearea*1e6 +            self.sequences.fluxes.inflow,            self.parameters.control.allowedrelease[self.parameters.derived.toy[self.idx_sim]],            self.parameters.derived.dischargesmoothpar,        )
    cpdef inline void calc_actualrelease(self)  nogil:
        cdef double d_weight
        cdef double d_release2
        cdef double d_neutral
        cdef double d_release1
        cdef double d_upperbound
        cdef double d_factor
        cdef double d_qmax
        cdef double d_qmin
        cdef double d_range
        cdef double d_target
        cdef int idx_toy
        idx_toy = self.parameters.derived.toy[self.idx_sim]
        d_target = self.parameters.control.targetvolume[idx_toy]
        d_range = max(            max(                self.parameters.control.targetrangeabsolute,                self.parameters.control.targetrangerelative*d_target),            1e-6,        )
        d_qmin = self.parameters.control.neardischargeminimumthreshold[idx_toy]
        d_qmax = smoothutils.smooth_max1(            d_qmin,            self.sequences.aides.alloweddischarge,            self.parameters.derived.dischargesmoothpar        )
        d_factor = smoothutils.smooth_logistic3(            (self.sequences.new_states.watervolume-d_target+d_range)/d_range,            self.parameters.derived.volumesmoothparlog2,        )
        d_upperbound = smoothutils.smooth_min1(            d_qmax,            self.sequences.fluxes.inflow,            self.parameters.derived.dischargesmoothpar        )
        d_release1 = (            (1.-d_factor)*d_qmin +            d_factor*smoothutils.smooth_max1(                d_qmin,                d_upperbound,                self.parameters.derived.dischargesmoothpar,            )        )
        d_factor = smoothutils.smooth_logistic3(            (d_target+d_range-self.sequences.new_states.watervolume)/d_range,            self.parameters.derived.volumesmoothparlog2,        )
        d_neutral = smoothutils.smooth_max1(            d_qmin,            self.sequences.fluxes.inflow,            self.parameters.derived.dischargesmoothpar        )
        d_release2 = (            (1.-d_factor)*d_qmax +            d_factor*smoothutils.smooth_min1(                d_qmax,                d_neutral,                self.parameters.derived.dischargesmoothpar,            )        )
        d_weight = smoothutils.smooth_logistic1(            d_target-self.sequences.new_states.watervolume,            self.parameters.derived.volumesmoothparlog1        )
        self.sequences.fluxes.actualrelease = d_weight*d_release1+(1.-d_weight)*d_release2
        if self.parameters.derived.volumesmoothparlog1 > 0.:
            d_weight = exp(                -((self.sequences.new_states.watervolume-d_target)/self.parameters.derived.volumesmoothparlog1)**2            )
        else:
            d_weight = 0.
        d_neutral = smoothutils.smooth_max1(            d_upperbound,            d_qmin,            self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.actualrelease = d_weight*d_neutral+(1.-d_weight)*self.sequences.fluxes.actualrelease
        self.sequences.fluxes.actualrelease = smoothutils.smooth_max1(            self.sequences.fluxes.actualrelease,            0.,            self.parameters.derived.dischargesmoothpar        )
        self.sequences.fluxes.actualrelease = self.sequences.fluxes.actualrelease * (smoothutils.smooth_logistic1(            self.sequences.new_states.watervolume-self.parameters.control.watervolumeminimumthreshold[idx_toy],            self.parameters.derived.volumesmoothparlog1        ))
    cpdef inline void calc_flooddischarge(self)  nogil:
        self.parameters.control.waterlevel2flooddischarge.inputs[0] = self.sequences.aides.waterlevel
        self.parameters.control.waterlevel2flooddischarge.calculate_values(self.parameters.derived.toy[self.idx_sim])
        self.sequences.fluxes.flooddischarge = self.parameters.control.waterlevel2flooddischarge.outputs[0]
    cpdef inline void calc_outflow(self)  nogil:
        self.sequences.fluxes.outflow = max(self.sequences.fluxes.actualrelease + self.sequences.fluxes.flooddischarge, 0.)
    cpdef inline void update_watervolume_v1(self)  nogil:
        self.sequences.new_states.watervolume = (self.sequences.old_states.watervolume +                           self.parameters.derived.seconds*(self.sequences.fluxes.inflow-self.sequences.fluxes.outflow)/1e6)
    cpdef inline void update_watervolume(self)  nogil:
        self.sequences.new_states.watervolume = (self.sequences.old_states.watervolume +                           self.parameters.derived.seconds*(self.sequences.fluxes.inflow-self.sequences.fluxes.outflow)/1e6)
    cpdef inline void pass_outflow_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.outflow)
    cpdef inline void pass_outflow(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.outflow)
