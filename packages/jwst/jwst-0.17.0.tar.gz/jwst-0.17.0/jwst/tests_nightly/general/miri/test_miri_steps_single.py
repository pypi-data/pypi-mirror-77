import os
import numpy as np
from numpy.testing import assert_allclose
import pytest
from gwcs.wcstools import grid_from_bounding_box
from ci_watson.artifactory_helpers import get_bigdata

from jwst import datamodels
from jwst.datamodels import ImageModel, RegionsModel, CubeModel
from jwst.stpipe import crds_client
from jwst.lib.set_telescope_pointing import add_wcs
from jwst.tests.base_classes import BaseJWSTTest, raw_from_asn
from jwst.pipeline.collect_pipeline_cfgs import collect_pipeline_cfgs
from jwst.assign_wcs import AssignWcsStep
from jwst.cube_build import CubeBuildStep
from jwst.linearity import LinearityStep
from jwst.ramp_fitting import RampFitStep
from jwst.master_background import MasterBackgroundStep


@pytest.mark.bigdata
class TestMIRIRampFit(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_ramp_fit', 'truth']
    test_dir = 'test_ramp_fit'

    def test_ramp_fit_miri1(self):
        """
        Regression test of ramp_fit step performed on MIRI data.
        """
        input_file = self.get_data(self.test_dir, 'jw00001001001_01101_00001_MIRIMAGE_jump.fits')

        result = RampFitStep.call(input_file,
                         save_opt=True,
                         opt_name='rampfit1_opt_out.fits')
        output_file = result[0].save(path=result[0].meta.filename.replace('jump','rampfit'))
        int_output = result[1].save(path=result[1].meta.filename.replace('jump','rampfit_int'))
        result[0].close()
        result[1].close()

        outputs = [(output_file,
                    'jw00001001001_01101_00001_MIRIMAGE_ramp_fit.fits'),
                   (int_output,
                    'jw00001001001_01101_00001_MIRIMAGE_int.fits'),
                   ('rampfit1_opt_out_fitopt.fits',
                    'jw00001001001_01101_00001_MIRIMAGE_opt.fits')
                  ]
        self.compare_outputs(outputs)

    def test_ramp_fit_miri2(self):
        """
        Regression test of ramp_fit step performed on MIRI data.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw80600012001_02101_00003_mirimage_jump.fits')

        result = RampFitStep.call(input_file,
                          save_opt=True,
                          opt_name='rampfit2_opt_out.fits')

        output_file = result[0].save(path=result[0].meta.filename.replace('jump','rampfit'))
        int_output = result[1].save(path=result[1].meta.filename.replace('jump','rampfit_int'))
        result[0].close()
        result[1].close()

        outputs = [(output_file,
                    'jw80600012001_02101_00003_mirimage_ramp.fits'),
                   (int_output,
                    'jw80600012001_02101_00003_mirimage_int.fits'),
                   ('rampfit2_opt_out_fitopt.fits',
                    'jw80600012001_02101_00003_mirimage_opt.fits')
                  ]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestMIRICube(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_cube_build', 'truth']
    test_dir = 'test_cube_build'
    rtol = 0.000001

    def test_cubebuild_miri(self):
        """
        Regression test of cube_build performed on MIRI MRS data.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw10001001001_01101_00001_mirifushort_cal.fits')

        input_model = datamodels.IFUImageModel(input_file)
        CubeBuildStep.call(input_model, output_type='multi', save_results=True)

        outputs = [('jw10001001001_01101_00001_mirifushort_s3d.fits',
                    'jw10001001001_01101_00001_mirifushort_s3d_ref.fits',
                    ['primary','sci','err','dq','wmap']) ]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestMIRILinearity(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_linearity','truth']
    test_dir ='test_linearity'

    def test_linearity_miri3(self):
        """
        Regression test of linearity step performed on MIRI data.
        """
        input_file = self.get_data(self.test_dir,
                                    'jw00001001001_01109_00001_MIRIMAGE_dark_current.fits')
        # get supplemental input
        override_file = self.get_data(self.test_dir,
                                      "lin_nan_flag_miri.fits")
        # run calibration step
        result = LinearityStep.call(input_file,
                           override_linearity=override_file)

        output_file = result.meta.filename
        result.save(output_file)
        result.close()

        outputs = [(output_file,
                    'jw00001001001_01109_00001_MIRIMAGE_linearity.fits') ]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestMIRIWCSFixed(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_wcs','fixed','truth']
    test_dir = os.path.join('test_wcs','fixed')

    def test_miri_fixed_slit_wcs(self):
        """
        Regression test of creating a WCS object and doing pixel to sky transformation.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw00035001001_01101_00001_mirimage_rate.fits')
        result = AssignWcsStep.call(input_file, save_results=True)

        cwd = os.path.abspath('.')
        os.makedirs('truth', exist_ok=True)
        os.chdir('truth')
        truth_file = self.get_data(*self.ref_loc,
                                 'jw00035001001_01101_00001_mirimage_assign_wcs.fits')
        os.chdir(cwd)
        truth = ImageModel(truth_file)

        x, y = grid_from_bounding_box(result.meta.wcs.bounding_box)
        ra, dec, lam = result.meta.wcs(x, y)
        raref, decref, lamref = truth.meta.wcs(x, y)
        assert_allclose(ra, raref)
        assert_allclose(dec, decref)
        assert_allclose(lam, lamref)


@pytest.mark.bigdata
class TestMIRIWCSIFU(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_wcs', 'ifu', 'truth']
    test_dir = os.path.join('test_wcs', 'ifu')

    def test_miri_ifu_wcs(self):
        """
        Regression test of creating a WCS object and doing pixel to sky transformation.
        """
        input_file = self.get_data(self.test_dir,
                                   'jw00024001001_01101_00001_MIRIFUSHORT_uncal_MiriSloperPipeline.fits')
        result = AssignWcsStep.call(input_file, save_results=True)

        # Get the region file
        region = RegionsModel(crds_client.get_reference_file(result, 'regions'))
        # Choose the same plane as in the miri.py file (hardcoded for now).
        regions = region.regions[7, :, :]

        # inputs
        x, y = grid_from_bounding_box(result.meta.wcs.bounding_box)

        # Get indices where pixels == 0. These should be NaNs in the output.
        ind_zeros = regions == 0

        cwd = os.path.abspath('.')
        os.makedirs('truth', exist_ok=True)
        os.chdir('truth')
        truth_file = self.get_data(*self.ref_loc,
                                 'jw00024001001_01101_00001_MIRIFUSHORT_assign_wcs.fits')
        os.chdir(cwd)
        truth = ImageModel(truth_file)

        ra, dec, lam = result.meta.wcs(x, y)
        raref, decref, lamref = truth.meta.wcs(x, y)
        assert_allclose(ra, raref, equal_nan=True)
        assert_allclose(dec, decref, equal_nan=True)
        assert_allclose(lam, lamref, equal_nan=True)

        # Test that we got NaNs at ind_zero
        assert(np.isnan(ra).nonzero()[0] == ind_zeros.nonzero()[0]).all()
        assert(np.isnan(ra).nonzero()[1] == ind_zeros.nonzero()[1]).all()

        # Test the inverse transform
        x1, y1 = result.meta.wcs.backward_transform(ra, dec, lam)
        assert(np.isnan(x1).nonzero()[0] == ind_zeros.nonzero()[0]).all()
        assert (np.isnan(x1).nonzero()[1] == ind_zeros.nonzero()[1]).all()

        # Also run a smoke test with values outside the region.
        dec[100][200] = -80
        ra[100][200] = 7
        lam[100][200] = 15

        x2, y2 = result.meta.wcs.backward_transform(ra, dec, lam)
        assert np.isnan(x2[100][200])
        assert np.isnan(x2[100][200])


@pytest.mark.bigdata
class TestMIRIWCSImage(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_wcs', 'image', 'truth']
    test_dir = os.path.join('test_wcs', 'image')

    def test_miri_image_wcs(self):
        """
        Regression test of creating a WCS object and doing pixel to sky transformation.
        """

        input_file = self.get_data(self.test_dir,
                                    "jw00001001001_01101_00001_MIRIMAGE_ramp_fit.fits")
        result = AssignWcsStep.call(input_file, save_results=True)

        cwd = os.path.abspath('.')
        os.makedirs('truth', exist_ok=True)
        os.chdir('truth')
        truth_file = self.get_data(*self.ref_loc,
                                 "jw00001001001_01101_00001_MIRIMAGE_assign_wcs.fits")
        os.chdir(cwd)
        truth = ImageModel(truth_file)

        x, y = grid_from_bounding_box(result.meta.wcs.bounding_box)
        ra, dec = result.meta.wcs(x, y)
        raref, decref = truth.meta.wcs(x, y)
        assert_allclose(ra, raref)
        assert_allclose(dec, decref)


@pytest.mark.bigdata
class TestMIRIWCSSlitless(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_wcs', 'slitless', 'truth']
    test_dir = os.path.join('test_wcs', 'slitless')

    def test_miri_slitless_wcs(self):
        """
        Regression test of creating a WCS object and doing pixel to sky transformation.
        """
        input_file = self.get_data(self.test_dir,
                                   "jw80600012001_02101_00003_mirimage_rateints.fits")
        result = AssignWcsStep.call(input_file, save_results=True)

        cwd = os.path.abspath('.')
        os.makedirs('truth', exist_ok=True)
        os.chdir('truth')
        truth_file = self.get_data(*self.ref_loc,
                                 "jw80600012001_02101_00003_mirimage_assignwcsstep.fits")
        os.chdir(cwd)
        truth = CubeModel(truth_file)

        x, y = grid_from_bounding_box(result.meta.wcs.bounding_box)
        ra, dec, lam = result.meta.wcs(x, y)
        raref, decref, lamref = truth.meta.wcs(x, y)
        assert_allclose(ra, raref)
        assert_allclose(dec, decref)
        assert_allclose(lam, lamref)


@pytest.mark.bigdata
class TestMIRISetPointing(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_pointing', 'truth']
    test_dir = 'test_pointing'
    rtol = 0.000001

    def test_miri_setpointing(self):
        """
        Regression test of the set_telescope_pointing script on a level-1b MIRI file.
        """

        # Copy original version of file to test file, which will get overwritten by test
        input_file = self.get_data(self.test_dir,
                                    'jw80600010001_02101_00001_mirimage_uncal_orig.fits')
        # Get SIAF PRD database file
        siaf_prd_loc = ['jwst-pipeline', self.env, 'common', 'prd.db']
        siaf_path = get_bigdata(*siaf_prd_loc)

        add_wcs(input_file, allow_default=True, siaf_path=siaf_path)

        outputs = [(input_file,
                    'jw80600010001_02101_00001_mirimage_uncal_ref.fits')]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestMIRIMasterBackgroundLRS(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_masterbackground', 'lrs', 'truth']
    test_dir = ['test_masterbackground', 'lrs']

    rtol = 0.000001

    def test_miri_lrs_masterbg_user(self):
        """
        Regression test of masterbackgound subtraction with lrs, with user provided 1-D background
        """

        # input file has the background added
        input_file = self.get_data(*self.test_dir, 'miri_lrs_sci+bkg_cal.fits')
        # user provided 1-D background
        user_background = self.get_data(*self.test_dir, 'miri_lrs_bkg_x1d.fits')

        result = MasterBackgroundStep.call(input_file,
                                           user_background=user_background,
                                           save_results=True)

        # Compare result (background subtracted image) to science image with no
        # background. Subtract these images, smooth the subtracted image and
        # the mean should be close to zero.
        input_sci_cal_file = self.get_data(*self.test_dir,
                                            'miri_lrs_sci_cal.fits')
        input_sci = datamodels.open(input_sci_cal_file)

        # find the LRS region
        bb = result.meta.wcs.bounding_box
        x, y = grid_from_bounding_box(bb)
        result_lrs_region = result.data[y.astype(int), x.astype(int)]
        sci_lrs_region = input_sci.data[y.astype(int), x.astype(int)]

        # do a 5 sigma clip on the science image
        sci_mean = np.nanmean(sci_lrs_region)
        sci_std = np.nanstd(sci_lrs_region)
        upper = sci_mean + sci_std*5.0
        lower = sci_mean - sci_std*5.0
        mask_clean = np.logical_and(sci_lrs_region < upper, sci_lrs_region > lower)

        sub = result_lrs_region - sci_lrs_region
        mean_sub = np.absolute(np.mean(sub[mask_clean]))

        atol = 0.1
        rtol = 0.001
        assert_allclose(mean_sub, 0, atol=atol, rtol=rtol)

        # Test 3 Compare background subtracted science data (results)
        #  to a truth file.
        truth_file = self.get_data(*self.ref_loc,
                                  'miri_lrs_sci+bkg_masterbackgroundstep.fits')

        result_file = result.meta.filename
        outputs = [(result_file, truth_file)]
        self.compare_outputs(outputs)
        result.close()
        input_sci.close()


@pytest.mark.bigdata
class TestMIRIMasterBackgroundMRSDedicated(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_masterbackground', 'mrs', 'dedicated', 'truth']
    test_dir = ['test_masterbackground', 'mrs', 'dedicated']

    rtol = 0.000001

    def test_miri_masterbg_mrs_dedicated(self):
        """Run masterbackground step on MIRI MRS association"""
        asn_file = self.get_data(*self.test_dir,
                                  'miri_mrs_mbkg_0304_spec3_asn.json')
        for file in raw_from_asn(asn_file):
            self.get_data(*self.test_dir, file)

        collect_pipeline_cfgs('./config')
        result = MasterBackgroundStep.call(
            asn_file,
            config_file='config/master_background.cfg',
            save_background=True,
            save_results=True,
            )

        # test 1
        # loop over the background subtracted data and compare to truth files
        # check that the  cal_step master_background ran to complete
        for model in result:
            assert model.meta.cal_step.master_background == 'COMPLETE'
            truth_file = self.get_data(*self.ref_loc,
                                        model.meta.filename)
            outputs = [(model.meta.filename, truth_file)]
            self.compare_outputs(outputs)

        # test 2
        # compare the master background combined file to truth file
        master_combined_bkg_file = 'MIRI_MRS_seq1_MIRIFULONG_34LONGexp1_bkg_o002_masterbg.fits'
        truth_background = self.get_data(*self.ref_loc,
                                          master_combined_bkg_file)
        outputs = [(master_combined_bkg_file, truth_background)]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestMIRIMasterBackgroundMRSNodded(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_masterbackground', 'mrs', 'nodded', 'truth']
    test_dir = ['test_masterbackground', 'mrs', 'nodded']

    rtol = 0.000001

    def test_miri_masterbg_mrs_nodded(self):
        """Run masterbackground step on MIRI MRS association"""
        asn_file = self.get_data(*self.test_dir,
                                  'miri_mrs_mbkg_spec3_asn.json')
        for file in raw_from_asn(asn_file):
            self.get_data(*self.test_dir, file)

        collect_pipeline_cfgs('./config')
        result = MasterBackgroundStep.call(
            asn_file,
            config_file='config/master_background.cfg',
            save_background=True,
            save_results=True,
            )

        # test 1
        # loop over the background subtracted data and compare to truth files
        # check that the  cal_step master_background ran to complete
        for model in result:
            assert model.meta.cal_step.master_background == 'COMPLETE'
            truth_file = self.get_data(*self.ref_loc,
                                        model.meta.filename)
            outputs = [(model.meta.filename, truth_file)]
            self.compare_outputs(outputs)

        # test 2
        # compare the master background combined file to truth file
        master_combined_bkg_file = 'MIRI_MRS_nod_seq1_MIRIFUSHORT_12SHORTexp1_o001_masterbg.fits'
        truth_background = self.get_data(*self.ref_loc,
                                          master_combined_bkg_file)
        outputs = [(master_combined_bkg_file, truth_background)]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestMIRIMasterBackgroundLRSNodded(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_masterbackground', 'lrs', 'nodded', 'truth']
    test_dir = ['test_masterbackground', 'lrs', 'nodded']

    rtol = 0.000001

    def test_miri_masterbg_lrs_nodded(self):
        """Run masterbackground step on MIRI LRS association"""
        asn_file = self.get_data(*self.test_dir,
                                  'miri_lrs_mbkg_nodded_spec3_asn.json')
        for file in raw_from_asn(asn_file):
            self.get_data(*self.test_dir, file)

        collect_pipeline_cfgs('./config')
        result = MasterBackgroundStep.call(
            asn_file,
            config_file='config/master_background.cfg',
            save_background=True,
            save_results=True,
            )

        # test 1
        # loop over the background subtracted data and compare to truth files
        for model in result:
            assert model.meta.cal_step.master_background == 'COMPLETE'
            truth_file = self.get_data(*self.ref_loc,
                                        model.meta.filename)
            outputs = [(model.meta.filename, truth_file)]
            self.compare_outputs(outputs)

        # test 2
        # compare the master background combined file to truth file
        master_combined_bkg_file = 'MIRI_LRS_nod_seq1_MIRIMAGE_P750Lexp1_o002_masterbg.fits'
        truth_background = self.get_data(*self.ref_loc,
                                          master_combined_bkg_file)
        outputs = [(master_combined_bkg_file, truth_background)]
        self.compare_outputs(outputs)


@pytest.mark.bigdata
class TestMIRIMasterBackgroundLRSDedicated(BaseJWSTTest):
    input_loc = 'miri'
    ref_loc = ['test_masterbackground', 'lrs', 'dedicated', 'truth']
    test_dir = ['test_masterbackground', 'lrs', 'dedicated']

    rtol = 0.000001

    def test_miri_masterbg_lrs_dedicated(self):
        """Run masterbackground step on MIRI LRS association"""
        asn_file = self.get_data(*self.test_dir,
                                  'miri_lrs_mbkg_dedicated_spec3_asn.json')
        for file in raw_from_asn(asn_file):
            self.get_data(*self.test_dir, file)

        collect_pipeline_cfgs('./config')
        result = MasterBackgroundStep.call(
            asn_file,
            config_file='config/master_background.cfg',
            save_background=True,
            save_results=True,
            )

        # test 1
        # loop over the background subtracted data and compare to truth files
        for model in result:
            assert model.meta.cal_step.master_background == 'COMPLETE'
            truth_file = self.get_data(*self.ref_loc,
                                        model.meta.filename)
            outputs = [(model.meta.filename, truth_file)]
            self.compare_outputs(outputs)

        # test 2
        # compare the master background combined file to truth file
        master_combined_bkg_file = 'MIRI_LRS_seq1_MIRIMAGE_P750Lexp1_o001_masterbg.fits'
        truth_background = self.get_data(*self.ref_loc,
                                          master_combined_bkg_file)
        outputs = [(master_combined_bkg_file, truth_background)]
        self.compare_outputs(outputs)
