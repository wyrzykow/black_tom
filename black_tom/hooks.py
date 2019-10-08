#THIS IS LW's hook, but there is also other hook in custom_code; 
#change the settings accordingly

import logging
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def observation_change_state(observation, previous_status):
    if observation.status == 'COMPLETED':
        logger.info(
            'Sending email, observation %s changed state from %s to %s',
            observation, previous_status, observation.status
        )
        send_mail(
            'Observation complete',
            'The observation {} has completed'.format(observation),
            'wyrzykow@gmail.com',
            ['wyrzykow@gmail.com'],
            fail_silently=False,
        )

