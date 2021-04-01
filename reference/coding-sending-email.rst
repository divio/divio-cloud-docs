.. _sending-email:

Sending email in Divio applications
===================================

Divio does not provide mail services.

To send mail from your Django applications, you will need either to connect to a third-party email relay provided via
an API, or an SMTP gateway. The former option is preferred, because it is generally more reliable.

SMTP traffic is liable to being blocked; often IP ranges as well as particular originating addresses are blocked in
response to certain behaviour. In addition, some vendors (`for example AWS
<https://aws.amazon.com/premiumsupport/knowledge-center/ec2-port-25-throttle/>`_) block certain traffic by default.

Using an API to a provider bypasses these problems and can also give you better control and more feedback.

Providers including `Mailjet <https://www.mailjet.com>`_ and `Mailgun <https://www.mailgun.com>`_ offer both API and
SMTP gateway options.
