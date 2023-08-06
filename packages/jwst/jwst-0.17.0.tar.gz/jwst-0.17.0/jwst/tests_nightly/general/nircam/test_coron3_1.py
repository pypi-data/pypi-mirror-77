import pytest

from jwst.tests.base_classes import BaseJWSTTest, raw_from_asn
from jwst.pipeline import Coron3Pipeline


@pytest.mark.bigdata
class TestCoron3Pipeline(BaseJWSTTest):
    rtol = 0.00001
    atol = 0.00001
    input_loc = 'nircam'
    ref_loc = ['test_coron3', 'truth']

    def test_coron3_1(self):
        """Regression test of calwebb_coron3 pipeline.

        Test is performed on NIRCam simulated data.
        """
        asn_name = 'jw99999-a3001_20170327t121212_coron3_001_asn.json'
        override_psfmask = 'jwst_nircam_psfmask_somb.fits'

        # get a local copy of the inputs
        asn_file = self.get_data('test_coron3', asn_name)
        psfmask_file = self.get_data('test_coron3', override_psfmask)
        for file in raw_from_asn(asn_file):
            self.get_data('test_coron3', file)

        pipe = Coron3Pipeline()
        pipe.align_refs.override_psfmask = psfmask_file
        pipe.outlier_detection.resample_data = False
        pipe.run(asn_file)

        self.ignore_keywords += ['NAXIS1', 'TFORM*']
        self.ignore_fields = self.ignore_keywords

        outputs = [( # Compare psfstack product
                    'jw99999-a3001_t1_nircam_f140m-maskbar_psfstack.fits',
                    'jw99999-a3001_t1_nircam_f140m-maskbar_psfstack_ref.fits'
                   ),
                   ( # Compare psfalign product
                    'jw9999947001_02102_00001_nrcb3_a3001_psfalign.fits',
                    'jw99999-a3001_t1_nircam_f140m-maskbar_psfalign_ref.fits'
                   ),
                   ( # Compare psfsub product
                    'jw9999947001_02102_00001_nrcb3_a3001_psfsub.fits',
                    'jw9999947001_02102_00001_nrcb3_psfsub_ref.fits'
                   ),
                   ( # Compare level-2c products
                    'jw9999947001_02102_00001_nrcb3_a3001_crfints.fits',
                    'jw9999947001_02102_00001_nrcb3_a3001_crfints_ref.fits'
                   ),
                   (
                    'jw9999947001_02102_00002_nrcb3_a3001_crfints.fits',
                    'jw9999947001_02102_00002_nrcb3_a3001_crfints_ref.fits'
                   ),
                   ( # Compare i2d product
                    'jw99999-a3001_t1_nircam_f140m-maskbar_i2d.fits',
                    'jw99999-a3001_t1_nircam_f140m-maskbar_i2d_ref.fits'
                   )
                  ]
        self.compare_outputs(outputs)
