
from ucsmsdk.ucshandle import UcsHandle, UcsException
from ucsmsdk import mometa
from pycrypt.encryption import AESCipher
from pyucs.log.decorators import addClassLogger
from pyucs.ucs.vlan.comparison import ListComparison, ComparisonObject
from pyucs.statsd.portstats import EthPortStat, EthPortChannelStat, FcPortStat, FcPortChannelStat


@addClassLogger
class Ucs(UcsHandle):
    """
        This is a custom UCS class that is used to simplify some of the methods and processes
        with ucsmsdk into a single class class with simple method calls. The ucsmsdk lacks
        a lot of built-in 'functionality' and really only provides raw data returned via
        query_dn and query_classid. These are the only two meaningful methods of ucsmsdk
        and this class is an attempt to bring some simplified method calls to ucsmsdk.
        This class also encrypts the password so that it is not stored in clear text in memory.
    """

    def __init__(self, ip, username, password, port=None, secure=None,
                 proxy=None, timeout=None, query_classids=None):
        super().__init__(ip, username, password, port=port, secure=secure, proxy=proxy, timeout=timeout)
        self.cipher = AESCipher()
        self._password = self.cipher.encrypt(self._UcsSession__password)
        self._UcsSession__password = None
        self._connected = False
        # define default classids in which the Ucs object will by default
        # have properties for. Since these are default we assign immutable
        # and hidden Tuple object here.
        self._default_classids = ('OrgOrg',
                                  'FabricChassisEp',
                                  'FabricVlan',
                                  'ComputeBlade',
                                  'VnicLanConnTempl',
                                  'LsServer')
        self._query_classids = list(self._default_classids)
        # allow at initialization the option to add to the 'default' property list of managed objects
        if query_classids:
            self._query_classids.append(query_classids)
        # make the _query_classids property an immutable object after initialization
        self._query_classids = tuple(self._query_classids)

    def login(self, **kwargs):

        try:
            self.__log.debug(f'{self.name}: Connecting')
            self.connect(**kwargs)
        except BaseException as e:
            self.__log.error(f'{self.name}: Error connecting')
            self.__log.exception(f'{self.name}: Exception: {e}, \n Args: {e.args}')

    def connect(self, **kwargs):
        """
        Connect method so that the password can be decrypted for the connection
        as well as to populate the default properties of the Ucs object
        :param kwargs:
        :return:
        """
        try:
            self._UcsSession__password = self.cipher.decrypt(self._password, self.cipher.AES_KEY)
            self._connected = self._login(**kwargs)
            self._UcsSession__password = None
            self.refresh_inventory()
        except BaseException as e:
            raise e

    def logout(self, **kwargs):
        try:
            self.__log.debug(f'{self.name}: Disconnecting')
            self.disconnect(**kwargs)
        except BaseException as e:
            self.__log.error(f'{self.name}: Error Disconnecting')
            self.__log.exception(f'{self.name}: Exception: {e}, \n Args: {e.args}')

    def disconnect(self, **kwargs):
        try:
            resp = self._logout(**kwargs)
            self._connected = False
        except UcsException as e:
            self._connected = False
            raise e

    def refresh_inventory(self):
        try:
            self._is_connected()
            q = self.query_classids(*self._query_classids)
            for k in q.keys():
                setattr(self, k, q[k])
        except UcsException as e:
            raise e

    def clear_default_properties(self):
        try:
            self._is_connected()
            q = self.query_classids(*self._query_classids)
            for k in q.keys():
                delattr(self, k)
        except UcsException as e:
            raise e

    def _is_connected(self):
        """
        method to check if there is a connection to ucsm
        and raise an exception if not.
        This is used as a check prior to running any other
        methods.
        """
        if self._connected:
            return True
        else:
            raise UcsException(error_code=1,
                               error_descr='Not currently logged in. Please connect to a UCS domain first')

    def query_rn(self, rn, class_id):
        """
        Added a missing method that Cisco should add in the ability to query the relative_name (rn)
        of a managed object
        :param rn:
        :param class_id:
        :return:
        """
        return self.query_classid(class_id=class_id,
                                  filter_str='(rn, "{}")'.format(rn)
                                  )

    def _query_mo(self, class_id, chassis=None, slot=None, vlan_id=None, name=None,
                  service_profile=None, org=None, fabric=None, port=None, portchannel=None,
                  dn=None, rn=None):
        """
        This is a beast of a method and really the brains of the operation of all the
        availbel methods in this class.
        :param class_id: Required parameter
        :param chassis: required for chassis query
        :param slot: required for chassis/blade query
        :param vlan_id: required for vlan query
        :param name:
        :param service_profile: required for service_profile query
        :param org: required for org query
        :param dn: required for dn query
        :param rn: required for rn query
        :return: one or more managedObjects
        """
        try:
            self._is_connected()

            # The below is fairly self explanatory and won't be commented
            # built-in query_dn method
            if dn:
                return self.query_dn(dn=dn)

            # custom query_rn method with an optional org search filter
            if rn:
                if org:
                    return self.query_classid(class_id=class_id,
                                              filter_str='((rn, "{}") and (dn, "{}"))'.format(rn, org))
                return self.query_rn(rn=rn, class_id=class_id)

            # vlan_id and optionally adding the name of the vlan
            if vlan_id:
                if name:
                    return self.query_classid(class_id=class_id,
                                              filter_str='((id, "{}") and (name, "{}"))'.format(vlan_id, name))
                return self.query_classid(class_id=class_id,
                                          filter_str='(id, "{}")'.format(vlan_id))
            # search for anything with a name parameter and optionally use an org search filter
            if name:
                if org:
                    return self.query_classid(class_id=class_id,
                                              filter_str='((name, "{}") and (dn, "{}"))'.format(name, org))
                return self.query_rn(rn=name, class_id=class_id)

            # chassis ID and optionally a blade slot id
            if chassis:
                if slot:
                    return self.query_classid(class_id=class_id,
                                              filter_str='((chassis_id, "{}") and (slot_id, "{}"))'.format(chassis, slot))
                return self.query_classid(class_id=class_id,
                                          filter_str='(chassis_id, "{}")'.format(chassis))

            # all chassis blade slots with slot id
            if slot:
                return self.query_classid(class_id=class_id,
                                          filter_str='((slot_id, "{}"))'.format(slot))

            # service profile managedobject
            if service_profile:
                return self.query_classid(class_id=class_id,
                                          filter_str='((dn, "{}"))'.format(service_profile.dn)
                                          )

            if fabric:
                return self.query_classid(class_id=class_id,
                                          filter_str='((dn, "{}"))'.format(fabric.dn)
                                          )

            # by default return all managedObjects from classid
            return self.query_classid(class_id=class_id)
        except UcsException as e:
            raise e

    def get_vnic_template(self, vnic=None, name=None, org=None, dn=None, rn=None):
        try:
            self._is_connected()

            if vnic and isinstance(vnic, list):
                tmp = []
                for v in vnic:
                    if v.oper_nw_templ_name:
                        tmp.append(self._query_mo(class_id='VnicLanConnTempl', dn=v.oper_nw_templ_name))
                return tmp

            return self._query_mo(class_id='VnicLanConnTempl',
                                  name=name,
                                  org=org,
                                  dn=dn,
                                  rn=rn
                                  )
        except UcsException as e:
            raise e

    def get_vnic(self, service_profile=None, dn=None):
        try:
            self._is_connected()

            if service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
                return self._query_mo(class_id='VnicEther',
                                      service_profile=service_profile,
                                      dn=dn
                                      )
            elif service_profile and isinstance(service_profile, list):
                tmp = []
                for s in service_profile:
                    tmp = tmp.__add__(self._query_mo(class_id='VnicEther',
                                                     service_profile=s
                                                     ))
                return tmp
            elif service_profile and isinstance(service_profile, str):
                raise UcsException(
                    "InvalidType: Parameter 'service_profile' expected type "
                    "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

            elif dn:
                self._query_mo(class_id='VnicEther',
                               dn=dn
                               )
            return self._query_mo(class_id='VnicEther')
        except UcsException as e:
            raise e

    def get_vnic_vlans(self, vnic=None, vnic_template=None, service_profile=None, dn=None):
        try:
            self._is_connected()

            if vnic and isinstance(vnic, mometa.vnic.VnicEther.VnicEther):
                return self.query_classid('VnicEtherIf',
                                          filter_str='(dn, "{}")'.format(vnic.dn))

            elif vnic and isinstance(vnic, list):
                tmp = []
                for v in vnic:
                    tmp.append(self.query_classid('VnicEtherIf',
                                                  filter_str='(dn, "{}")'.format(v.dn)))
                return tmp

            elif vnic_template and isinstance(vnic_template, mometa.vnic.VnicLanConnTempl.VnicLanConnTempl):
                return self.query_classid('VnicEtherIf',
                                          filter_str='(dn, "{}")'.format(vnic_template.dn))
            elif vnic_template and isinstance(vnic_template, list):
                tmp = []
                for v in vnic_template:
                    tmp.append(self.query_classid('VnicEtherIf',
                                                  filter_str='(dn, "{}")'.format(v.dn)))
                return tmp

            elif vnic and isinstance(vnic, str):
                raise UcsException(
                    "InvalidType: Parameter 'vnic' expected type "
                    "'ucsmsdk.mometa.vnic.VnicEther.VnicEther' and recieved 'str'")

            elif service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
                return self._query_mo(class_id='VnicEtherIf',
                                      service_profile=service_profile,
                                      dn=dn
                                      )
            elif service_profile and isinstance(service_profile, str):
                raise UcsException(
                    "InvalidType: Parameter 'service_profile' expected type "
                    "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

            elif dn:
                self._query_mo(class_id='VnicEther',
                               dn=dn
                               )
            return self._query_mo(class_id='VnicEther')
        except UcsException as e:
            raise e

    def get_vhba(self, service_profile=None, dn=None):
        try:
            self._is_connected()

            if service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
                return self._query_mo(class_id='VnicFc',
                                      service_profile=service_profile,
                                      dn=dn
                                      )
            elif service_profile and isinstance(service_profile, str):
                raise UcsException(
                    "InvalidType: Parameter 'service_profile' expected type "
                    "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

            elif dn:
                self._query_mo(class_id='VnicFc',
                               dn=dn
                               )
            return self._query_mo(class_id='VnicFc')
        except UcsException as e:
            raise e

    def get_org(self, name=None, org=None, dn=None, rn=None):
        try:
            self._is_connected()
            return self._query_mo(class_id='OrgOrg',
                                  name=name,
                                  org=org,
                                  dn=dn,
                                  rn=rn
                                  )
        except UcsException as e:
            raise e

    def get_vlan(self, name=None, vlan_id=None, dn=None, rn=None):
        try:
            self._is_connected()
            return self._query_mo(class_id='FabricVlan',
                                  name=name,
                                  vlan_id=vlan_id,
                                  dn=dn,
                                  rn=rn
                                  )
        except UcsException as e:
            raise e

    def get_service_profile(self, name=None, org=None, dn=None, rn=None, only_active=False):
        try:
            self._is_connected()
            tmp = self._query_mo(class_id='LsServer',
                                 name=name,
                                 org=org,
                                 dn=dn,
                                 rn=rn
                                 )
            if only_active:
                tmp = [s for s in tmp if s.assoc_state == 'associated']

            return tmp
        except UcsException as e:
            raise e

    def get_chassis(self, name=None, dn=None, rn=None):
        try:
            self._is_connected()
            return self._query_mo(class_id='FabricChassisEp',
                                  name=name,
                                  dn=dn,
                                  rn=rn
                                  )
        except UcsException as e:
            raise e

    def get_blade(self, chassis=None, slot=None, dn=None, rn=None):
        try:
            self._is_connected()
            return self._query_mo(class_id='ComputeBlade',
                                  chassis=chassis,
                                  slot=slot,
                                  dn=dn,
                                  rn=rn
                                  )
        except UcsException as e:
            raise e

    def get_switch_fabric(self, name=None, dn=None):
        try:
            self._is_connected()
            return self._query_mo(class_id='NetworkElement',
                                  name=name,
                                  dn=dn
                                  )
        except UcsException as e:
            raise e

    def get_fabric_etherport(self, dn=None, rn=None):
        try:
            self._is_connected()

            if dn:
                return self._query_mo(class_id='EtherPIo',
                                      dn=dn
                                      )
            return self._query_mo(class_id='EtherPIo')
        except UcsException as e:
            raise e

    def get_fabric_fcport(self, dn=None, rn=None):
        try:
            self._is_connected()

            if dn:
                return self._query_mo(class_id='FcPIo',
                                      dn=dn
                                      )
            return self._query_mo(class_id='FcPIo')
        except UcsException as e:
            raise e

    def get_port_channel(self, port_type=None, dn=None, rn=None):
        try:
            self._is_connected()

            if dn:
                if dn.find('fabric/lan') >= 0:
                    return self._query_mo(class_id='FabricEthLanPc',
                                          dn=dn
                                          )
                if dn.find('fabric/san') >= 0:
                    return self._query_mo(class_id='FabricFcSanPc',
                                          dn=dn
                                          )
            elif port_type == 'Ethernet':
                return self._query_mo(class_id='FabricEthLanPc')

            elif port_type == 'Fc':
                return self._query_mo(class_id='FabricFcSanPc')

            tmp = []
            tmp.append(self._query_mo(class_id='FabricEthLanPc'))
            tmp.append(self._query_mo(class_id='FabricFcSanPc'))
            return tmp
        except UcsException as e:
            raise e

    def get_system_storage(self, fabric=None, dn=None):
        try:
            self._is_connected()

            if fabric and isinstance(fabric, mometa.network.NetworkElement.NetworkElement):
                return self._query_mo(class_id='StorageItem',
                                      fabric=fabric,
                                      dn=dn
                                      )
            elif fabric and isinstance(fabric, str):
                raise UcsException(
                    "InvalidType: Parameter 'fabric' expected type "
                    "'mometa.network.NetworkElement.NetworkElement' and recieved 'str'")

            elif dn:
                return self._query_mo(class_id='StorageItem',
                                      dn=dn
                                      )
            return self._query_mo(class_id='StorageItem')
        except UcsException as e:
            raise e

    def get_vnic_stats(self, vnic=None, service_profile=None, ignore_error=False):
        try:
            self._is_connected()

            # check if a service profile was provided as a way to reduce returned results
            if isinstance(service_profile, mometa.ls.LsServer.LsServer):
                stats = self.get_vnic_stats(vnic=self.get_vnic(service_profile=service_profile), ignore_error=ignore_error)
                if stats:
                    return stats

            # check if the vnic parameter is a managedobject
            if isinstance(vnic, mometa.vnic.VnicEther.VnicEther):
                if vnic.equipment_dn:
                    return self.query_dn("{}/vnic-stats".format(vnic.equipment_dn))

            # if vnic is a list/tuple then use query_dns() to get all stats
            if isinstance(vnic, list) or isinstance(vnic, tuple):
                stats = []
                stats_query = [v for v in vnic if isinstance(v, str) and v.endswith('vnic-stats')]
                if not stats_query:
                    stats_query = ["{}/vnic-stats".format(v.equipment_dn) for v in vnic if v.equipment_dn]
                if stats_query:
                    stats = self.query_dns(stats_query)
                return list(stats.values())
            if not ignore_error:
                raise UcsException("InvalidType: Unexpected type with parameter 'vnic'."
                                   "Use type VnicEther or list/tuple of VnicEther")
        except UcsException as e:
            if not ignore_error:
                raise e

    def get_vhba_stats(self, vhba=None, service_profile=None, ignore_error=False):
        try:
            self._is_connected()

            # check if a service profile was provided as a way to reduce returned results
            if isinstance(service_profile, mometa.ls.LsServer.LsServer):
                stats = self.get_vhba_stats(vhba=self.get_vnic(service_profile=service_profile), ignore_error=ignore_error)
                if stats:
                    return stats

            # check if the vnic parameter is a managedobject
            if isinstance(vhba, mometa.vnic.VnicFc.VnicFc):
                if vhba.equipment_dn:
                    return self.query_dn("{}/vnic-stats".format(vhba.equipment_dn))

            # if vhba is a list/tuple then use query_dns() to get all stats
            if isinstance(vhba, list) or isinstance(vhba, tuple):
                stats = []
                stats_query = [v for v in vhba if isinstance(v, str) and v.endswith('vnic-stats')]
                if not stats_query:
                    stats_query = ["{}/vnic-stats".format(v.equipment_dn) for v in vhba if v.equipment_dn]
                if stats_query:
                    stats = self.query_dns(stats_query)
                return list(stats.values())
            if not ignore_error:
                raise UcsException("InvalidType: Unexpected type with parameter 'vhba'."
                                   "Use type VnicFc or list/tuple of VnicFc")
        except UcsException as e:
            if not ignore_error:
                raise e

    def get_fabric_etherport_stats(self, port=None, ignore_error=False):
        try:
            self._is_connected()

            # check if the port parameter is a managedobject
            if isinstance(port, mometa.ether.EtherPIo.EtherPIo):
                port_stats = None
                if port.oper_state == 'up':
                    stats_query = ["{}/pause-stats".format(port.dn),
                                  "{}/loss-stats".format(port.dn),
                                  "{}/err-stats".format(port.dn),
                                  "{}/rx-stats".format(port.dn),
                                  "{}/tx-stats".format(port.dn)]
                    port_stats = EthPortStat()
                    port_stats.pop_base_params(port)
                    stats = self.query_dns(stats_query)
                    for stat in stats:
                        if isinstance(stats[stat], mometa.ether.EtherPauseStats.EtherPauseStats):
                            port_stats.pause_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherLossStats.EtherLossStats):
                            port_stats.loss_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherErrStats.EtherErrStats):
                            port_stats.err_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherRxStats.EtherRxStats):
                            port_stats.rx_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherTxStats.EtherTxStats):
                            port_stats.tx_stats(stats[stat])

                return port_stats

            # if ethport is a list/tuple then loop through each one to get the stats of each
            if isinstance(port, list) or isinstance(port, tuple):
                stats_query = []
                port_stats_dict = {}
                port_dict = {}

                # build the list of stats dn's for querying
                for p in port:
                    if p.oper_state == 'up':
                        port_dict.update({p.dn: p})
                        tmp = ["{}/pause-stats".format(p.dn),
                               "{}/loss-stats".format(p.dn),
                               "{}/err-stats".format(p.dn),
                               "{}/rx-stats".format(p.dn),
                               "{}/tx-stats".format(p.dn)]
                        stats_query = stats_query.__add__(tmp)

                stats = self.query_dns(stats_query)
                for stat in stats:
                    parent_dn = stats[stat]._ManagedObject__parent_dn
                    if not port_stats_dict.get(parent_dn or None):
                        port_stats_dict.update({parent_dn: EthPortStat()})
                        port_stats_dict[parent_dn].pop_base_params(port_dict[parent_dn])

                    if isinstance(stats[stat], mometa.ether.EtherPauseStats.EtherPauseStats):
                        port_stats_dict[parent_dn].pause_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherLossStats.EtherLossStats):
                        port_stats_dict[parent_dn].loss_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherErrStats.EtherErrStats):
                        port_stats_dict[parent_dn].err_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherRxStats.EtherRxStats):
                        port_stats_dict[parent_dn].rx_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherTxStats.EtherTxStats):
                        port_stats_dict[parent_dn].tx_stats(stats[stat])
                return list(port_stats_dict.values())
            if not ignore_error:
                raise UcsException(99,
                    "InvalidType: Unexpected type with parameter 'port'.Use type EtherPIo or list/tuple of EtherPIo")
        except UcsException as e:
            if not ignore_error:
                raise e

    def get_fabric_fcport_stats(self, port=None, ignore_error=False):
        try:
            self._is_connected()

            # check if the port parameter is a managedobject
            if isinstance(port, mometa.fc.FcPIo.FcPIo):
                port_stats = None
                if port.oper_state == 'up':
                    stats_query = ["{}/stats".format(port.dn),
                                   "{}/err-stats".format(port.dn)]
                    port_stats = FcPortStat()
                    port_stats.pop_base_params(port)
                    stats = self.query_dns(stats_query)

                    for stat in stats:
                        if isinstance(stats[stat], mometa.fc.FcStats.FcStats):
                            port_stats.stats(stats[stat])
                        elif isinstance(stats[stat], mometa.fc.FcErrStats.FcErrStats):
                            port_stats.err_stats(stats[stat])

                return port_stats

            # if fcport is a list/tuple then loop through each one to get the stats of each
            if isinstance(port, list) or isinstance(port, tuple):
                stats_query = []
                port_stats_dict = {}
                port_dict = {}
                for p in port:
                    if p.oper_state == 'up':
                        port_dict.update({p.dn: p})
                        tmp = ["{}/stats".format(p.dn),
                               "{}/err-stats".format(p.dn)]
                        stats_query = stats_query.__add__(tmp)
                stats = self.query_dns(stats_query)
                for stat in stats:
                    parent_dn = stats[stat]._ManagedObject__parent_dn
                    if not port_stats_dict.get(parent_dn or None):
                        port_stats_dict.update({parent_dn: FcPortStat()})
                        port_stats_dict[parent_dn].pop_base_params(port_dict[parent_dn])

                    if isinstance(stats[stat], mometa.fc.FcStats.FcStats):
                        port_stats_dict[parent_dn].stats(stats[stat])
                    elif isinstance(stats[stat], mometa.fc.FcErrStats.FcErrStats):
                        port_stats_dict[parent_dn].err_stats(stats[stat])

                return list(port_stats_dict.values())
            if not ignore_error:
                raise UcsException(99,
                    "InvalidType: Unexpected type with parameter 'port'.Use type FcPIo or list/tuple of FcPIo")
        except UcsException as e:
            if not ignore_error:
                raise e

    def get_fabric_etherportchannel_stats(self, portchannel=None, ignore_error=False):
        try:
            self._is_connected()

            # check if the vnic parameter is a managedobject
            if isinstance(portchannel, mometa.fabric.FabricEthLanPc.FabricEthLanPc):
                port_stats = None
                if portchannel.oper_state == 'up':
                    stats_query = ["{}/pause-stats".format(portchannel.dn),
                                   "{}/loss-stats".format(portchannel.dn),
                                   "{}/err-stats".format(portchannel.dn),
                                   "{}/rx-stats".format(portchannel.dn),
                                   "{}/tx-stats".format(portchannel.dn)]
                    port_stats = EthPortChannelStat()
                    port_stats.pop_base_params(portchannel)
                    stats = self.query_dns(stats_query)
                    for stat in stats:
                        if isinstance(stats[stat], mometa.ether.EtherPauseStats.EtherPauseStats):
                            port_stats.pause_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherLossStats.EtherLossStats):
                            port_stats.loss_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherErrStats.EtherErrStats):
                            port_stats.err_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherRxStats.EtherRxStats):
                            port_stats.rx_stats(stats[stat])
                        elif isinstance(stats[stat], mometa.ether.EtherTxStats.EtherTxStats):
                            port_stats.tx_stats(stats[stat])

                return port_stats

            # if vnic is a list/tuple then loop through each one to get the stats of each
            if isinstance(portchannel, list) or isinstance(portchannel, tuple):
                stats_query = []
                port_stats_dict = {}
                port_dict = {}

                # build the list of stats dn's for querying
                for p in portchannel:
                    if p.oper_state == 'up':
                        port_dict.update({p.dn: p})
                        tmp = ["{}/pause-stats".format(p.dn),
                               "{}/loss-stats".format(p.dn),
                               "{}/err-stats".format(p.dn),
                               "{}/rx-stats".format(p.dn),
                               "{}/tx-stats".format(p.dn)]
                        stats_query = stats_query.__add__(tmp)

                stats = self.query_dns(stats_query)
                for stat in stats:
                    parent_dn = stats[stat]._ManagedObject__parent_dn
                    if port_stats_dict.get(parent_dn or None):
                        port_stats = port_stats_dict[parent_dn]
                    else:
                        port_stats_dict.update({parent_dn: EthPortChannelStat()})
                        port_stats_dict[parent_dn].pop_base_params(port_dict[parent_dn])

                    if isinstance(stats[stat], mometa.ether.EtherPauseStats.EtherPauseStats):
                        port_stats_dict[parent_dn].pause_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherLossStats.EtherLossStats):
                        port_stats_dict[parent_dn].loss_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherErrStats.EtherErrStats):
                        port_stats_dict[parent_dn].err_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherRxStats.EtherRxStats):
                        port_stats_dict[parent_dn].rx_stats(stats[stat])
                    elif isinstance(stats[stat], mometa.ether.EtherTxStats.EtherTxStats):
                        port_stats_dict[parent_dn].tx_stats(stats[stat])

                return list(port_stats_dict.values())
            if not ignore_error:
                raise UcsException(99,
                    "InvalidType: Unexpected type with parameter 'portchannel'.Use type EtherPIo or list/tuple of EtherPIo")
        except UcsException as e:
            if not ignore_error:
                raise e

    def get_fabric_fcportchannel_stats(self, portchannel=None, ignore_error=False):
        try:
            self._is_connected()

            # check if the vnic parameter is a managedobject
            if isinstance(portchannel, mometa.fabric.FabricFcSanPc.FabricFcSanPc):
                port_stats = None
                if portchannel.oper_state == 'up':
                    stats_query = ["{}/stats".format(portchannel.dn),
                                   "{}/err-stats".format(portchannel.dn)]
                    port_stats = FcPortChannelStat()
                    port_stats.pop_base_params(portchannel)
                    stats = self.query_dns(stats_query)

                    for stat in stats:
                        if isinstance(stats[stat], mometa.fc.FcStats.FcStats):
                            port_stats.stats(stats[stat])
                        elif isinstance(stats[stat], mometa.fc.FcErrStats.FcErrStats):
                            port_stats.err_stats(stats[stat])

                return port_stats

                # if fcport is a list/tuple then loop through each one to get the stats of each
            if isinstance(portchannel, list) or isinstance(portchannel, tuple):
                stats_query = []
                port_stats_dict = {}
                port_dict = {}
                for p in portchannel:
                    if p.oper_state == 'up':
                        port_dict.update({p.dn: p})
                        tmp = ["{}/stats".format(p.dn),
                               "{}/err-stats".format(p.dn)]
                        stats_query = stats_query.__add__(tmp)
                stats = self.query_dns(stats_query)
                for stat in stats:
                    parent_dn = stats[stat]._ManagedObject__parent_dn
                    if not port_stats_dict.get(parent_dn or None):
                        port_stats_dict.update({parent_dn: FcPortChannelStat()})
                        port_stats_dict[parent_dn].pop_base_params(port_dict[parent_dn])

                    if isinstance(stats[stat], mometa.fc.FcStats.FcStats):
                        port_stats_dict[parent_dn].stats(stats[stat])
                    elif isinstance(stats[stat], mometa.fc.FcErrStats.FcErrStats):
                        port_stats_dict[parent_dn].err_stats(stats[stat])

                return list(port_stats_dict.values())
            if not ignore_error:
                raise UcsException(99,
                    "InvalidType: Unexpected type with parameter 'portchannel'.Use type FcPIo or list/tuple of FcPIo")
        except UcsException as e:
            if not ignore_error:
                raise e

    def get_system_storage_stats(self, storageitem=None, ignore_error=False):
        try:
            self._is_connected()
            if isinstance(storageitem, mometa.storage.StorageItem.StorageItem):
                return storageitem

            if isinstance(storageitem, list) or isinstance(storageitem, tuple):
                tmp = []
                for s in storageitem:
                    if isinstance(storageitem, mometa.storage.StorageItem.StorageItem):
                        tmp.append(storageitem)

                return tmp

            return self.query_classid('StorageItem')
        except UcsException as e:
            if not ignore_error:
                raise e

    def get_system_stats(self, ignore_error=False):
        try:
            self._is_connected()
            tmp = self.query_classid('SWSystemStatsHist')
            return tmp
        except UcsException as e:
            if not ignore_error:
                raise e

    def assign_vlan_to_vnic(self, mo, vlan_name, commit=True):
        try:
            from ucsmsdk.mometa.vnic.VnicEther import VnicEther
            from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
            from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
            if isinstance(mo, str):
                # assume this is a dn value
                mo = self.query_dn(mo)
            if isinstance(mo, VnicEther) or isinstance(mo, VnicLanConnTempl):

                vnic_vlan = VnicEtherIf(parent_mo_or_dn=mo,
                                        name=vlan_name)
                self.add_mo(vnic_vlan)
                if commit:
                    self.commit()
                    return self.query_dn(vnic_vlan.dn)
                return vnic_vlan
            else:
                raise UcsException("ManagedObject Invalid Type")
        except BaseException as e:
                raise e

    def create_vlan_global(self, vlan_name, vlan_id, commit=True):
        vlan_mo = mometa.fabric.FabricVlan.FabricVlan(parent_mo_or_dn='fabric/lan',
                                                      sharing='none',
                                                      name=vlan_name,
                                                      id=vlan_id,
                                                      mcast_policy_name='',
                                                      policy_owner='local',
                                                      default_net='no',
                                                      pub_nw_name='',
                                                      compression_type='included'
                                                      )
        self.add_mo(vlan_mo)
        if commit:
            self.commit()
            return self.get_vlan(name=vlan_name, vlan_id=vlan_id)
        return vlan_mo

    @staticmethod
    def audit_vnic_vlans(ucs, vnic_vlans, ignore_same=False):
        """
        Takes a list of vnic_vlans and compares them to each other. vnic_vlans must have len >= 2
        :param vnic_vlans: [[vnic1_vlans],[vnic2_vlans],[vnic3_vlans],[vnicN_vlans]]
        :param ignore_same: [BOOL] Output the items that are different or output everything including items that are the same
        :return: comparison_obj
        """

        from operator import attrgetter
        meta = {}  # structure will be { vnic.dn: [vlan_id_list] }
        if vnic_vlans and isinstance(vnic_vlans, list) and len(vnic_vlans) >= 2:
            for vlans in vnic_vlans:
                vlans.sort(key=lambda x: x.rn)
                tmp_dict = {
                    vlans[0]._ManagedObject__parent_dn: list(map(attrgetter('rn'), vlans))
                }
                meta.update(tmp_dict)

            max_index = len(list(meta.keys())) - 1
            comparison_list = []
            for i in range(0, max_index+1):
                if not i == max_index:
                    for x in range(i+1, max_index+1):
                        ref = list(meta.keys())[i]
                        dif = list(meta.keys())[x]
                        comparison_list.append(
                            ListComparison(reference_dict={ref: meta[ref]},
                                           difference_dict={dif: meta[dif]},
                                           ucs=ucs)
                        )
            results = []
            for l in comparison_list:
                tmp = l.compare(ignore_same=ignore_same)
                if tmp:
                    results.append(tmp)

            if len(results) > 0:
                return results
            return None

    def remediate_vnic_vlan_audit(self, vnic_audit):
        if isinstance(vnic_audit, ComparisonObject):
            if vnic_audit.ucs == self.ucs:
                if vnic_audit.operator == '=>':
                    self.assign_vlan_to_vnic(vnic_audit.reference, vnic_audit.value.replace('if-', ''))
                elif vnic_audit.operator == '<=':
                    self.assign_vlan_to_vnic(vnic_audit.difference, vnic_audit.value.replace('if-', ''))
        elif isinstance(vnic_audit, list):
            for audit in vnic_audit:
                if isinstance(audit, ComparisonObject):
                    if audit.ucs == self.ucs:
                        if audit.operator == '=>':
                            self.assign_vlan_to_vnic(audit.reference, audit.value.replace('if-', ''))
                        elif audit.operator == '<=':
                            self.assign_vlan_to_vnic(audit.difference, audit.value.replace('if-', ''))
                else:
                    raise UcsException(
                        "Invalid Paramter Type: Expected type 'ComparisonObject' or 'list' of 'ComparisonObject'")
        else:
            raise UcsException("Invalid Paramter Type: Expected type 'ComparisonObject' or 'list' of 'ComparisonObject'")
