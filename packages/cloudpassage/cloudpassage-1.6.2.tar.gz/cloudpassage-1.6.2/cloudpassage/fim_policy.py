"""FimPolicy and FimBaseline classes"""

import cloudpassage.sanity as sanity
from .halo_endpoint import HaloEndpoint
from .http_helper import HttpHelper


class FimPolicy(HaloEndpoint):
    """FimPolicy class:

    The list_all() method allows filtering of results with keyword arguments.
    An exhaustive list of keyword arguments can be found here:
    https://api-doc.cloudpassage.com/help#file-integrity-policies

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.
    """

    object_name = "fim_policy"
    objects_name = "fim_policies"
    default_endpoint_version = 1

    def endpoint(self):
        """Return endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)

    @classmethod
    def pagination_key(cls):
        """Defines the pagination key for parsing paged results"""
        return cls.objects_name

    @classmethod
    def object_key(cls):
        """Defines the key used to pull the policy from the json document"""
        return cls.object_name


class FimBaseline(HaloEndpoint):
    """Initializing the FimBaseline class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    """
    object_name = "baseline"
    objects_name = "baselines"
    default_endpoint_version = 1

    def endpoint(self, policy_id):
        """Return endpoint for API requests."""
        return "/v{}/fim_policies/{}/{}".format(self.endpoint_version,
                                                policy_id, self.objects_name)

    def list_all(self, fim_policy_id):
        """Returns a list of all baselines for the indicated FIM policy

        Args:
            fim_policy_id (str): ID of fim policy

        Returns:
            list: List of all baselines for the given policy

        """

        request = HttpHelper(self.session)
        endpoint = self.endpoint(fim_policy_id)
        max_pages = 30
        response = request.get_paginated(endpoint, self.objects_name,
                                         max_pages)
        return response

    def describe(self, fim_policy_id, baseline_id):
        """Returns the body of the baseline indicated by fim_baseline_id.

        Args
            fim_policy_id (str): ID of FIM policy
            fim_baseline_id (str): ID of baseline

        Returns:
            dict: Dictionary describing FIM baseline

        """

        request = HttpHelper(self.session)
        endpoint = "{}/{}/details".format(self.endpoint(fim_policy_id),
                                          baseline_id)
        response = request.get(endpoint)
        result = response[self.object_name]
        return result

    def create(self, fim_policy_id, server_id, **kwargs):
        """Creates a FIM baseline

        Args:
            fim_policy_id (str): ID of FIM policy to baseline
            server_id (str): ID of server to use for generating baseline

        Keyword Args:
            expires (int): Number of days from today for expiration of baseline
            comment (str): Guess.

        Returns:
            str: ID of new baseline

        """

        sanity.validate_object_id([fim_policy_id, server_id])
        request = HttpHelper(self.session)
        endpoint = self.endpoint(fim_policy_id)
        request_body = {"baseline": {"server_id": server_id,
                                     "expires": None,
                                     "comment": None}}
        if "expires" in kwargs:
            request_body["baseline"]["expires"] = kwargs["expires"]
        if "comment" in kwargs:
            request_body["baseline"]["comment"] = kwargs["comment"]
        response = request.post(endpoint, request_body)
        policy_id = response["baseline"]["id"]
        return policy_id

    def delete(self, fim_policy_id, fim_baseline_id):
        """Delete a FIM baseline by ID

        Args:
            fim_policy_id (str): ID of FIM policy
            fim_baseline_id (str): ID of baseline to be deleted

        Returns:
            None if successful, exceptions throw otherwise.

        """

        sanity.validate_object_id([fim_policy_id, fim_baseline_id])
        request = HttpHelper(self.session)
        endpoint = "{}/{}".format(self.endpoint(fim_policy_id),
                                  fim_baseline_id)
        request.delete(endpoint)
        return None

    def update(self, fim_policy_id, fim_baseline_id, server_id):
        """Update a FIM policy baseline.

        Args:
            fim_policy_id (str): ID of fim policy
            fim_baseline_id (str): ID of baseline to be updated
            server_id (str): ID of server to use when generating new baseline

        Returns:
            None if successful, exceptions throw otherwise.

        """

        sanity.validate_object_id([fim_policy_id, fim_baseline_id, server_id])
        request = HttpHelper(self.session)
        endpoint = "{}/{}".format(self.endpoint(fim_policy_id),
                                  fim_baseline_id)
        request_body = {"baseline": {"server_id": server_id}}
        request.put(endpoint, request_body)
        return None
