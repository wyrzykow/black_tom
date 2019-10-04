from tom_observations.facility import GenericObservationFacility, GenericObservationForm
from django import forms


class ASVTelescopeForm(GenericObservationForm):
    exposure_time = forms.IntegerField()
    exposure_count = forms.IntegerField()

class ASVTelescope(GenericObservationFacility):
    name = 'ASV'
    observation_types = [('IMAGING', 'Imaging'), ('SPECTRA', 'Spectroscopy')]

    SITES = {
        'ASV1.4': {
            'sitecode': 'asv2',
            'latitude': 43.14,
            'longitude': 21.56,
            'elevation': 1143
        },
        }

    def data_products(self, observation_id, product_id=None):
        return []

    def get_form(self, observation_type):
        return ASVTelescopeForm

    def get_observation_status(self, observation_id):
        return ['IN_PROGRESS']
        
    def get_observation_url(self, observation_id):
        return ''
    
    def get_observing_sites(self):
        return self.SITES
        
    def get_terminal_observing_states(self):
        return ['IN_PROGRESS', 'COMPLETED']
    
    def submit_observation(self, observation_payload):
        print(observation_payload)
        return [1]
        
    def validate_observation(self, observation_payload):
        pass




