import pytest

from jwst.tests.base_classes import BaseJWSTTestSteps
from jwst.tests.base_classes import pytest_generate_tests # noqa: F401

from jwst.ami import AmiAnalyzeStep
from jwst.refpix import RefPixStep
from jwst.dark_current import DarkCurrentStep
from jwst.dq_init import DQInitStep
from jwst.flatfield import FlatFieldStep
from jwst.jump import JumpStep
from jwst.linearity import LinearityStep
from jwst.saturation import SaturationStep
from jwst.pathloss import PathLossStep


# Parameterized regression tests for NIRISS processing
# All tests in this set run with 1 input file and
#  only generate 1 output for comparison.
#
@pytest.mark.bigdata
class TestNIRISSSteps(BaseJWSTTestSteps):
    input_loc = 'niriss'

    params = {'test_steps':
                [dict(input='ami_analyze_input_16.fits',
                      test_dir='test_ami_analyze',
                      step_class=AmiAnalyzeStep,
                      step_pars=dict(oversample=3, rotation=1.49),
                      output_truth=('ami_analyze_ref_output_16.fits',
                                    dict(rtol = 0.00001)),
                      output_hdus=['primary','fit','resid','closure_amp',
                                         'closure_pha','fringe_amp','fringe_pha',
                                         'pupil_pha','solns'],
                      id='ami_analyze_niriss'
                      ),
                 dict(input='jw00034001001_01101_00001_NIRISS_dq_init.fits',
                      test_dir='test_bias_drift',
                      step_class=RefPixStep,
                      step_pars=dict(odd_even_columns=True,
                                     use_side_ref_pixels=False,
                                     side_smoothing_length=10,
                                     side_gain=1.0),
                      output_truth='jw00034001001_01101_00001_NIRISS_bias_drift.fits',
                      output_hdus=[],
                      id='refpix_niriss'
                      ),
                 dict(input='jw00034001001_01101_00001_NIRISS_saturation.fits',
                      test_dir='test_dark_step',
                      step_class=DarkCurrentStep,
                      step_pars=dict(),
                      output_truth='jw00034001001_01101_00001_NIRISS_dark_current.fits',
                      output_hdus=[],
                      id='dark_current_niriss'
                      ),
                 dict(input='jw00034001001_01101_00001_NIRISS_uncal.fits',
                      test_dir='test_dq_init',
                      step_class=DQInitStep,
                      step_pars=dict(),
                      output_truth='jw00034001001_01101_00001_NIRISS_dq_init.fits',
                      output_hdus=[],
                      id='dq_init_niriss'
                      ),
                 dict(input='jw00034001001_01101_00001_NIRISS_ramp_fit.fits',
                      test_dir='test_flat_field',
                      step_class=FlatFieldStep,
                      step_pars=dict(),
                      output_truth='jw00034001001_01101_00001_NIRISS_flat_field.fits',
                      output_hdus=[],
                      id='flat_field_niriss'
                      ),
                 dict(input='jw00034001001_01101_00001_NIRISS_linearity.fits',
                      test_dir='test_jump',
                      step_class=JumpStep,
                      step_pars=dict(rejection_threshold=20.0),
                      output_truth='jw00034001001_01101_00001_NIRISS_jump.fits',
                      output_hdus=[],
                      id='jump_niriss'
                      ),
                 dict(input='jw00034001001_01101_00001_NIRISS_dark_current.fits',
                      test_dir='test_linearity',
                      step_class=LinearityStep,
                      step_pars=dict(),
                      output_truth='jw00034001001_01101_00001_NIRISS_linearity.fits',
                      output_hdus=[],
                      id='linearity_niriss'
                      ),
                 dict(input='jw00034001001_01101_00001_NIRISS_bias_drift.fits',
                      test_dir='test_saturation',
                      step_class=SaturationStep,
                      step_pars=dict(),
                      output_truth='jw00034001001_01101_00001_NIRISS_saturation.fits',
                      output_hdus=[],
                      id='saturation_niriss'
                      ),
                 dict(input='soss_2AB_results_int_assign_wcs.fits',
                      test_dir='test_pathloss',
                      step_class=PathLossStep,
                      step_pars=dict(),
                      output_truth='soss_2AB_results_int_pathloss.fits',
                      output_hdus=[],
                      id='pathloss_niriss'
                      ),
                ]
              }
