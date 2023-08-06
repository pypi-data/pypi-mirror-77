import pytest

from jwst.tests.base_classes import BaseJWSTTest, raw_from_asn

from jwst.pipeline import (
    Ami3Pipeline,
    Detector1Pipeline,
)
from jwst.ramp_fitting import RampFitStep
from jwst.photom import PhotomStep
from jwst.pipeline.collect_pipeline_cfgs import collect_pipeline_cfgs
from jwst.stpipe import Step


@pytest.mark.bigdata
class TestAMIPipeline(BaseJWSTTest):
    input_loc = 'niriss'
    ref_loc = ['test_ami_pipeline', 'truth']
    test_dir = 'test_ami_pipeline'

    def test_ami_pipeline(self):
        """
        Regression test of the AMI pipeline performed on NIRISS AMI data.
        """
        asn_file = self.get_data(self.test_dir,
                                 'test_lg1_asn.json')
        for file in raw_from_asn(asn_file):
            self.get_data(self.test_dir, file)

        pipe = Ami3Pipeline()
        pipe.save_averages = True
        pipe.ami_analyze.oversample = 3
        pipe.ami_analyze.rotation = 1.49
        pipe.run(asn_file)

        outputs = [('test_targ_aminorm.fits',
                    'ami_pipeline_targ_lgnorm.fits'),
                  ]
        self.compare_outputs(outputs, rtol=0.00001,
                             ignore_hdus=['ASDF', 'HDRTAB'])


@pytest.mark.bigdata
class TestDetector1Pipeline(BaseJWSTTest):
    input_loc = 'niriss'
    ref_loc = ['test_detector1pipeline', 'truth']
    test_dir = 'test_detector1pipeline'

    def test_niriss_detector1(self):
        """
        Regression test of calwebb_detector1 pipeline performed on NIRISS data.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw00034001001_01101_00001_NIRISS_uncal.fits')
        step = Detector1Pipeline()
        step.save_calibrated_ramp = True
        step.ipc.skip = True
        step.persistence.skip = True
        step.refpix.odd_even_columns = True
        step.refpix.use_side_ref_pixels = True
        step.refpix.side_smoothing_length = 11
        step.refpix.side_gain = 1.0
        step.refpix.odd_even_rows = True
        step.jump.rejection_threshold = 250.0
        step.ramp_fit.save_opt = False
        step.ramp_fit.suffix = 'ramp'
        step.output_file = 'jw00034001001_01101_00001_NIRISS_rate.fits'

        step.run(input_file)

        outputs = [('jw00034001001_01101_00001_NIRISS_ramp.fits',
                    'jw00034001001_01101_00001_NIRISS_ramp_ref.fits'),
                   ('jw00034001001_01101_00001_NIRISS_rate.fits',
                    'jw00034001001_01101_00001_NIRISS_rate_ref.fits')
                  ]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestNIRISSSOSS2Pipeline(BaseJWSTTest):
    input_loc = 'niriss'
    ref_loc = ['test_spec2pipeline', 'truth']
    test_dir = 'test_spec2pipeline'

    def test_nirisssoss2pipeline1(self):
        """
        Regression test of calwebb_tso_spec2 pipeline performed on NIRISS SOSS data.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw10003001002_03101_00001-seg003_nis_rateints.fits')
        collect_pipeline_cfgs()
        args = [
            'calwebb_tso-spec2.cfg',
            input_file
        ]
        Step.from_cmdline(args)

        outputs = [{'files':('jw10003001002_03101_00001-seg003_nis_calints.fits',
                    'jw10003001002_03101_00001-seg003_nis_calints_ref.fits'),
                    'pars':dict(ignore_hdus=['INT_TIMES', 'VAR_POISSON',
                                             'VAR_RNOISE', 'ASDF'])},
                   {'files':('jw10003001002_03101_00001-seg003_nis_x1dints.fits',
                    'jw10003001002_03101_00001-seg003_nis_x1dints_ref.fits'),
                    'pars':dict(ignore_hdus=['INT_TIMES', 'ASDF'])}
                  ]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestNIRISSPhotom(BaseJWSTTest):
    input_loc = 'niriss'
    ref_loc = ['test_photom', 'truth']
    test_dir = 'test_photom'

    def test_photom_niriss(self):
        """
        Regression test of photom step performed on NIRISS imaging data.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw00034001001_01101_00001_NIRISS_flat_field.fits')

        result = PhotomStep.call(input_file)
        output_file = result.meta.filename
        result.save(output_file)
        result.close()

        outputs = [(output_file,
                    'jw00034001001_01101_00001_NIRISS_photom.fits')
                  ]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestNIRISSRampFit(BaseJWSTTest):
    input_loc = 'niriss'
    ref_loc = ['test_ramp_fit', 'truth']
    test_dir = 'test_ramp_fit'

    def test_ramp_fit_niriss(self):
        """
        Regression test of ramp_fit step performed on NIRISS data.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw00034001001_01101_00001_NIRISS_jump.fits')

        result, result_int = RampFitStep.call(input_file,
                          save_opt=True,
                          opt_name='rampfit_opt_out.fits'
        )
        output_file = result.meta.filename
        result.save(output_file)
        result.close()

        outputs = [(output_file,
                    'jw00034001001_01101_00001_NIRISS_ramp_fit.fits'),
                    ('rampfit_opt_out_fitopt.fits',
                     'jw00034001001_01101_00001_NIRISS_uncal_opt.fits',
                     ['primary','slope','sigslope','yint','sigyint',
                      'pedestal','weights','crmag'])
                  ]
        self.compare_outputs(outputs)
