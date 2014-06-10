import twilio.rest
from twilio.rest import TwilioRestClient

c = twilio.rest.TwilioRestClient('account', 'token', 'base', 'version', 'client')
c = twilio.rest.TwilioRestClient('account')
c = twilio.rest.TwilioRestClient('account', timeout=0)
c = TwilioRestClient('account')
c = TwilioRestClient('account')
c = twilio.rest.TwilioRestClient('account', 'token', 'base', 'version', 'client', 0)
