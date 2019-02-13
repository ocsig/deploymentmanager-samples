"""
Network (VPC) provider implements GCP Network(VPC) specific transaltions
Supports V1 CFT versions
"""
from providers.subnetwork import SubnetworkCFT
import providers.baseprovider as base


class NetworkBase(base.BaseProvider):
    """
    Common implementation shared accross all Network versions.
    This class should not be used outside of it's child classes.
    """

    network_readonly_properties = [
        "kind",
        "routingConfig",
        "x_gcloud_bgp_routing_mode",
        "x_gcloud_subnet_mode"]

    def __init__(self, dm_api, gcloud_stage, gcloud_flags=''):
        
        self.readonly_properties += self.network_readonly_properties

        base.BaseProvider.__init__(
            self, "compute", "networks", dm_api, gcloud_stage, gcloud_flags)

    def get_new(self):
        return None  # not supposed to run


class NetworkV1(NetworkBase):
    """ Network V1 API provider"""

    def __init__(self, gcloud_flags=''):
        NetworkBase.__init__(
            self, "gcp-types/compute-v1:networks", "", gcloud_flags)

    def get_new(self):
        return NetworkV1()

class NetworkCFT(NetworkBase):
    """ Firewall-rules CFT API provider"""

    def __init__(self, gcloud_flags=''):
        NetworkBase.__init__(
            self, "../templates/networks/network.py", " ", gcloud_flags)


    def get_list(self, gcloud_flags=""):
        
        network_list = super(NetworkCFT, self).get_list(gcloud_flags)
        
        for network in network_list:
            subnetworks =[]
            for subnet in SubnetworkCFT().get_list(' --network ' + network.properties['name']):
                subnetworks.append(subnet.base_yaml)
            network.properties['subnetworks'] = subnetworks

        return network_list

    def get_new(self):
        return NetworkCFT()
