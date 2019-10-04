from tom_observations.facilities.lco import LCOFacility, LCOBaseObservationForm
from django import forms
from crispy_forms.layout import Div
from copy import deepcopy

class LCOMultiFilterForm(LCOBaseObservationForm):
    filter2 = forms.ChoiceField(choices=LCOBaseObservationForm.filter_choices)
    exposure_time2 = forms.FloatField(min_value=0.1)
    filter3 = forms.ChoiceField(choices=LCOBaseObservationForm.filter_choices)
    exposure_time3 = forms.FloatField(min_value=0.1)

    def layout(self):
        return Div(
                Div(
                    Div(
                        'name', 'proposal', 'ipp_value', 'observation_type', 'start', 'end',
                        css_class='col'
                    ),
                    Div(
                        'instrument_type', 'exposure_count', 'max_airmass',
                        css_class='col'
                    ),
                    css_class='form-row'
                ),
                Div(
                    Div(
                        'filter', 'exposure_time',
                        css_class='col'
                    ),
                    Div(
                        'filter2', 'exposure_time2',
                        css_class='col'
                    ),
                    Div(
                        'filter3', 'exposure_time3',
                        css_class='col'
                    ),
                    css_class='form-row'
                )
        )

    def observation_payload(self):
        payload = super().observation_payload()
        configuration2 = deepcopy(payload['requests'][0]['configurations'][0])
        configuration3 = deepcopy(payload['requests'][0]['configurations'][0])
        configuration2['instrument_configs'][0]['optical_elements']['filter'] = self.cleaned_data['filter2']
        configuration2['instrument_configs'][0]['exposure_time'] = self.cleaned_data['exposure_time2']
        configuration3['instrument_configs'][0]['optical_elements']['filter'] = self.cleaned_data['filter3']
        configuration3['instrument_configs'][0]['exposure_time'] = self.cleaned_data['exposure_time3']
        payload['requests'][0]['configurations'].extend([configuration2, configuration3])
        return payload


class LCOMultiFilterFacility(LCOFacility):
    name = 'LCOMultiFilter'
    form = LCOMultiFilterForm