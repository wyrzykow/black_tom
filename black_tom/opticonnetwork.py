from tom_observations.facility import GenericObservationFacility, GenericObservationForm
from django import forms
from crispy_forms.layout import Layout, Div



class OpticonNetworkForm(GenericObservationForm):
    name = forms.CharField()
    ipp_value = forms.FloatField()
    start = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    end = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    exposure_count = forms.IntegerField(min_value=1)
    exposure_time = forms.FloatField(min_value=0.1)
    max_airmass = forms.FloatField()
    observation_mode = forms.ChoiceField(
        choices=(('RELAXED', 'Normal'), ('URGENT', 'Urgent'))
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proposal'] = forms.ChoiceField(choices=self.proposal_choices())
        self.fields['filter'] = forms.ChoiceField(choices=self.filter_choices())
        self.fields['instrument_type'] = forms.ChoiceField(choices=self.instrument_choices())
        self.helper.layout = Layout(
            self.common_layout,
            self.layout(),
            self.extra_layout()
        )

    def layout(self):
        return Div(
            Div(
                'name', 'proposal', 'ipp_value', 'observation_mode', 'start', 'end',
                css_class='col'
            ),
            Div(
                'filter', 'instrument_type', 'exposure_count', 'exposure_time', 'max_airmass',
                css_class='col'
            ),
            css_class='form-row'
        )

    def extra_layout(self):
        # If you just want to add some fields to the end of the form, add them here.

        return Div()

    def instrument_choices(self):
        return [('ASV1.4','ccdcam')]

    def proposal_choices(self):
        return [('OPTICON','OPTICON')]

    def filter_choices(self):
        return [('g','g'), ('r','r'),('i','i'),('B','B'),('V','V'), ('R','R'), ('I','I')]

    # def filter_choices(self):
    #     return set([
    #         (f['code'], f['name']) for ins in self._get_instruments().values() for f in
    #         ins['optical_elements'].get('filters', []) + ins['optical_elements'].get('slits', [])
    #         ])

class OpticonNetwork(GenericObservationFacility):
    name = 'OPTICON'
    observation_types = [('IMAGING', 'Imaging'), ('SPECTRA', 'Spectroscopy')]

    SITES = {
        'ASV1.4': {
            'sitecode': 'asv2',
            'latitude': 43.14,
            'longitude': 21.56,
            'elevation': 1143
        },
        'ASV0.6': {
            'sitecode': 'asv1',
            'latitude': 43.14,
            'longitude': 21.56,
            'elevation': 1136
        },
        'REM0.6': {
            'sitecode': 'rem',
            'latitude': -29.25,
            'longitude': -70.73,
            'elevation': 2340
        },
        }

    def data_products(self, observation_id, product_id=None):
        return []

    def get_form(self, observation_type):
        return OpticonNetworkForm

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
