# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables


class RandomShuffle(pulumi.CustomResource):
    inputs: pulumi.Output[list]
    """
    The list of strings to shuffle.
    """
    keepers: pulumi.Output[dict]
    """
    Arbitrary map of values that, when changed, will
    trigger a new id to be generated.
    """
    result_count: pulumi.Output[float]
    """
    The number of results to return. Defaults to
    the number of items in the `input` list. If fewer items are requested,
    some elements will be excluded from the result. If more items are requested,
    items will be repeated in the result but not more frequently than the number
    of items in the input list.
    """
    results: pulumi.Output[list]
    """
    Random permutation of the list of strings given in `input`.
    """
    seed: pulumi.Output[str]
    """
    Arbitrary string with which to seed the random number
    generator, in order to produce less-volatile permutations of the list.
    **Important:** Even with an identical seed, it is not guaranteed that the
    same permutation will be produced across different versions of the provider.
    This argument causes the result to be *less volatile*, but not fixed for
    all time.
    """
    def __init__(__self__, resource_name, opts=None, inputs=None, keepers=None, result_count=None, seed=None, __props__=None, __name__=None, __opts__=None):
        """
        The resource `RandomShuffle` generates a random permutation of a list
        of strings given as an argument.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_random as random

        az = random.RandomShuffle("az",
            inputs=[
                "us-west-1a",
                "us-west-1c",
                "us-west-1d",
                "us-west-1e",
            ],
            result_count=2)
        example = aws.elb.LoadBalancer("example", availability_zones=az.results)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] inputs: The list of strings to shuffle.
        :param pulumi.Input[dict] keepers: Arbitrary map of values that, when changed, will
               trigger a new id to be generated.
        :param pulumi.Input[float] result_count: The number of results to return. Defaults to
               the number of items in the `input` list. If fewer items are requested,
               some elements will be excluded from the result. If more items are requested,
               items will be repeated in the result but not more frequently than the number
               of items in the input list.
        :param pulumi.Input[str] seed: Arbitrary string with which to seed the random number
               generator, in order to produce less-volatile permutations of the list.
               **Important:** Even with an identical seed, it is not guaranteed that the
               same permutation will be produced across different versions of the provider.
               This argument causes the result to be *less volatile*, but not fixed for
               all time.
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
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if inputs is None:
                raise TypeError("Missing required property 'inputs'")
            __props__['inputs'] = inputs
            __props__['keepers'] = keepers
            __props__['result_count'] = result_count
            __props__['seed'] = seed
            __props__['results'] = None
        super(RandomShuffle, __self__).__init__(
            'random:index/randomShuffle:RandomShuffle',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, inputs=None, keepers=None, result_count=None, results=None, seed=None):
        """
        Get an existing RandomShuffle resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] inputs: The list of strings to shuffle.
        :param pulumi.Input[dict] keepers: Arbitrary map of values that, when changed, will
               trigger a new id to be generated.
        :param pulumi.Input[float] result_count: The number of results to return. Defaults to
               the number of items in the `input` list. If fewer items are requested,
               some elements will be excluded from the result. If more items are requested,
               items will be repeated in the result but not more frequently than the number
               of items in the input list.
        :param pulumi.Input[list] results: Random permutation of the list of strings given in `input`.
        :param pulumi.Input[str] seed: Arbitrary string with which to seed the random number
               generator, in order to produce less-volatile permutations of the list.
               **Important:** Even with an identical seed, it is not guaranteed that the
               same permutation will be produced across different versions of the provider.
               This argument causes the result to be *less volatile*, but not fixed for
               all time.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["inputs"] = inputs
        __props__["keepers"] = keepers
        __props__["result_count"] = result_count
        __props__["results"] = results
        __props__["seed"] = seed
        return RandomShuffle(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
