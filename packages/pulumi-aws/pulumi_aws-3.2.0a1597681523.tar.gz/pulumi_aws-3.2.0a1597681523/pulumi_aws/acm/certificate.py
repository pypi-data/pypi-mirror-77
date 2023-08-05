# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Certificate(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of the certificate
    """
    certificate_authority_arn: pulumi.Output[str]
    """
    ARN of an ACMPCA
    """
    certificate_body: pulumi.Output[str]
    """
    The certificate's PEM-formatted public key
    """
    certificate_chain: pulumi.Output[str]
    """
    The certificate's PEM-formatted chain
    * Creating a private CA issued certificate
    """
    domain_name: pulumi.Output[str]
    """
    A domain name for which the certificate should be issued
    """
    domain_validation_options: pulumi.Output[list]
    """
    Set of domain validation objects which can be used to complete certificate validation. Can have more than one element, e.g. if SANs are defined. Only set if `DNS`-validation was used.

      * `domain_name` (`str`) - A domain name for which the certificate should be issued
      * `resourceRecordName` (`str`) - The name of the DNS record to create to validate the certificate
      * `resourceRecordType` (`str`) - The type of DNS record to create
      * `resourceRecordValue` (`str`) - The value the DNS record needs to have
    """
    options: pulumi.Output[dict]
    """
    Configuration block used to set certificate options. Detailed below.
    * Importing an existing certificate

      * `certificateTransparencyLoggingPreference` (`str`) - Specifies whether certificate details should be added to a certificate transparency log. Valid values are `ENABLED` or `DISABLED`. See https://docs.aws.amazon.com/acm/latest/userguide/acm-concepts.html#concept-transparency for more details.
    """
    private_key: pulumi.Output[str]
    """
    The certificate's PEM-formatted private key
    """
    status: pulumi.Output[str]
    """
    Status of the certificate.
    """
    subject_alternative_names: pulumi.Output[list]
    """
    Set of domains that should be SANs in the issued certificate. To remove all elements of a previously configured list, set this value equal to an empty list (`[]`) to trigger recreation.
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the resource.
    """
    validation_emails: pulumi.Output[list]
    """
    A list of addresses that received a validation E-Mail. Only set if `EMAIL`-validation was used.
    """
    validation_method: pulumi.Output[str]
    """
    Which method to use for validation. `DNS` or `EMAIL` are valid, `NONE` can be used for certificates that were imported into ACM and then into the provider.
    """
    def __init__(__self__, resource_name, opts=None, certificate_authority_arn=None, certificate_body=None, certificate_chain=None, domain_name=None, options=None, private_key=None, subject_alternative_names=None, tags=None, validation_method=None, __props__=None, __name__=None, __opts__=None):
        """
        The ACM certificate resource allows requesting and management of certificates
        from the Amazon Certificate Manager.

        It deals with requesting certificates and managing their attributes and life-cycle.
        This resource does not deal with validation of a certificate but can provide inputs
        for other resources implementing the validation. It does not wait for a certificate to be issued.
        Use a `acm.CertificateValidation` resource for this.

        Most commonly, this resource is used together with `route53.Record` and
        `acm.CertificateValidation` to request a DNS validated certificate,
        deploy the required validation records and wait for validation to complete.

        Domain validation through E-Mail is also supported but should be avoided as it requires a manual step outside
        of this provider.

        It's recommended to specify `create_before_destroy = true` in a [lifecycle](https://www.terraform.io/docs/configuration/resources.html#lifecycle) block to replace a certificate
        which is currently in use (eg, by `lb.Listener`).

        ## Example Usage
        ### Certificate creation

        ```python
        import pulumi
        import pulumi_aws as aws

        cert = aws.acm.Certificate("cert",
            domain_name="example.com",
            tags={
                "Environment": "test",
            },
            validation_method="DNS")
        ```
        ### Importing an existing certificate

        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_tls as tls

        example_private_key = tls.PrivateKey("examplePrivateKey", algorithm="RSA")
        example_self_signed_cert = tls.SelfSignedCert("exampleSelfSignedCert",
            key_algorithm="RSA",
            private_key_pem=example_private_key.private_key_pem,
            subjects=[{
                "commonName": "example.com",
                "organization": "ACME Examples, Inc",
            }],
            validity_period_hours=12,
            allowed_uses=[
                "key_encipherment",
                "digital_signature",
                "server_auth",
            ])
        cert = aws.acm.Certificate("cert",
            private_key=example_private_key.private_key_pem,
            certificate_body=example_self_signed_cert.cert_pem)
        ```
        ### Referencing domain_validation_options With for_each Based Resources

        See the `acm.CertificateValidation` resource for a full example of performing DNS validation.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = []
        for range in [{"key": k, "value": v} for [k, v] in enumerate({dvo.domainName: {
            name: dvo.resourceRecordName,
            record: dvo.resourceRecordValue,
            type: dvo.resourceRecordType,
        } for dvo in aws_acm_certificate.example.domain_validation_options})]:
            example.append(aws.route53.Record(f"example-{range['key']}",
                allow_overwrite=True,
                name=range["value"]["name"],
                records=[range["value"]["record"]],
                ttl=60,
                type=range["value"]["type"],
                zone_id=aws_route53_zone["example"]["zone_id"]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_authority_arn: ARN of an ACMPCA
        :param pulumi.Input[str] certificate_body: The certificate's PEM-formatted public key
        :param pulumi.Input[str] certificate_chain: The certificate's PEM-formatted chain
               * Creating a private CA issued certificate
        :param pulumi.Input[str] domain_name: A domain name for which the certificate should be issued
        :param pulumi.Input[dict] options: Configuration block used to set certificate options. Detailed below.
               * Importing an existing certificate
        :param pulumi.Input[str] private_key: The certificate's PEM-formatted private key
        :param pulumi.Input[list] subject_alternative_names: Set of domains that should be SANs in the issued certificate. To remove all elements of a previously configured list, set this value equal to an empty list (`[]`) to trigger recreation.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] validation_method: Which method to use for validation. `DNS` or `EMAIL` are valid, `NONE` can be used for certificates that were imported into ACM and then into the provider.

        The **options** object supports the following:

          * `certificateTransparencyLoggingPreference` (`pulumi.Input[str]`) - Specifies whether certificate details should be added to a certificate transparency log. Valid values are `ENABLED` or `DISABLED`. See https://docs.aws.amazon.com/acm/latest/userguide/acm-concepts.html#concept-transparency for more details.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['certificate_authority_arn'] = certificate_authority_arn
            __props__['certificate_body'] = certificate_body
            __props__['certificate_chain'] = certificate_chain
            __props__['domain_name'] = domain_name
            __props__['options'] = options
            __props__['private_key'] = private_key
            __props__['subject_alternative_names'] = subject_alternative_names
            __props__['tags'] = tags
            __props__['validation_method'] = validation_method
            __props__['arn'] = None
            __props__['domain_validation_options'] = None
            __props__['status'] = None
            __props__['validation_emails'] = None
        super(Certificate, __self__).__init__(
            'aws:acm/certificate:Certificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, certificate_authority_arn=None, certificate_body=None, certificate_chain=None, domain_name=None, domain_validation_options=None, options=None, private_key=None, status=None, subject_alternative_names=None, tags=None, validation_emails=None, validation_method=None):
        """
        Get an existing Certificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the certificate
        :param pulumi.Input[str] certificate_authority_arn: ARN of an ACMPCA
        :param pulumi.Input[str] certificate_body: The certificate's PEM-formatted public key
        :param pulumi.Input[str] certificate_chain: The certificate's PEM-formatted chain
               * Creating a private CA issued certificate
        :param pulumi.Input[str] domain_name: A domain name for which the certificate should be issued
        :param pulumi.Input[list] domain_validation_options: Set of domain validation objects which can be used to complete certificate validation. Can have more than one element, e.g. if SANs are defined. Only set if `DNS`-validation was used.
        :param pulumi.Input[dict] options: Configuration block used to set certificate options. Detailed below.
               * Importing an existing certificate
        :param pulumi.Input[str] private_key: The certificate's PEM-formatted private key
        :param pulumi.Input[str] status: Status of the certificate.
        :param pulumi.Input[list] subject_alternative_names: Set of domains that should be SANs in the issued certificate. To remove all elements of a previously configured list, set this value equal to an empty list (`[]`) to trigger recreation.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[list] validation_emails: A list of addresses that received a validation E-Mail. Only set if `EMAIL`-validation was used.
        :param pulumi.Input[str] validation_method: Which method to use for validation. `DNS` or `EMAIL` are valid, `NONE` can be used for certificates that were imported into ACM and then into the provider.

        The **domain_validation_options** object supports the following:

          * `domain_name` (`pulumi.Input[str]`) - A domain name for which the certificate should be issued
          * `resourceRecordName` (`pulumi.Input[str]`) - The name of the DNS record to create to validate the certificate
          * `resourceRecordType` (`pulumi.Input[str]`) - The type of DNS record to create
          * `resourceRecordValue` (`pulumi.Input[str]`) - The value the DNS record needs to have

        The **options** object supports the following:

          * `certificateTransparencyLoggingPreference` (`pulumi.Input[str]`) - Specifies whether certificate details should be added to a certificate transparency log. Valid values are `ENABLED` or `DISABLED`. See https://docs.aws.amazon.com/acm/latest/userguide/acm-concepts.html#concept-transparency for more details.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["certificate_authority_arn"] = certificate_authority_arn
        __props__["certificate_body"] = certificate_body
        __props__["certificate_chain"] = certificate_chain
        __props__["domain_name"] = domain_name
        __props__["domain_validation_options"] = domain_validation_options
        __props__["options"] = options
        __props__["private_key"] = private_key
        __props__["status"] = status
        __props__["subject_alternative_names"] = subject_alternative_names
        __props__["tags"] = tags
        __props__["validation_emails"] = validation_emails
        __props__["validation_method"] = validation_method
        return Certificate(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
