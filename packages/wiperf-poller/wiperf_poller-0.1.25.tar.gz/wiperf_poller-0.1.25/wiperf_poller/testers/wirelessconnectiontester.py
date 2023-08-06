import sys
import time
from socket import gethostbyname

from wiperf_poller.helpers.wirelessadapter import WirelessAdapter
from wiperf_poller.testers.mgtconnectiontester import MgtConnectionTester
from wiperf_poller.helpers.route import check_correct_mode_interface, inject_default_route
from wiperf_poller.testers.pingtester import PingTester

class WirelessConnectionTester(object):
    """
    Class to implement network connection tests for wiperf
    """

    def __init__(self, file_logger, interface, platform):

        self.platform = platform
        self.file_logger = file_logger
        self.adapter_obj = WirelessAdapter(interface, self.file_logger, platform)

    def run_tests(self, watchdog_obj, lockf_obj, config_vars, exporter_obj):

        # if we have no network connection (i.e. no bssid), no point in proceeding...
        self.file_logger.info("  Checking wireless connection available.")
        if self.adapter_obj.get_wireless_info() == False:

            self.file_logger.error("  Unable to get wireless info due to failure with ifconfig command")
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj)  # exit here

        self.file_logger.info("Checking we're connected to the network (layer3)")
        if self.adapter_obj.get_bssid() == 'NA':
            self.file_logger.error("  Problem with wireless connection: not associated to network")
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj)  # exit here

        self.file_logger.info("  Checking we have an IP address.")
        # if we have no IP address, no point in proceeding...
        if self.adapter_obj.get_adapter_ip() == False:
            self.file_logger.error("  Unable to get wireless adapter IP info")
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj)  # exit here

        # TODO: Fix this. Currently breaks when we have Eth & Wireless ports both up
        '''
        if self.adapter_obj.get_route_info() == False:
            file_logger.error("Unable to get wireless adapter route info - maybe you have multiple interfaces enabled that are stopping the wlan interface being used?")
            self.adapter_obj.bounce_error_exit(lockf_obj) # exit here
        '''

        if self.adapter_obj.get_ipaddr() == 'NA':
            self.file_logger.error("  Problem with wireless connection: no valid IP address")
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj) # exit here

        # final connectivity check: see if we can resolve an address
        # (network connection and DNS must be up)
        self.file_logger.info("  Checking we can do a DNS lookup to {}".format(config_vars['connectivity_lookup']))

        # Run a ping to seed arp cache
        ping_obj = PingTester(self.file_logger, platform=self.platform)
        ping_obj.ping_host(config_vars['connectivity_lookup'], 1)

        try:
            gethostbyname(config_vars['connectivity_lookup'])
        except Exception as ex:
            self.file_logger.error("  DNS seems to be failing, bouncing wireless interface. Err msg: {}".format(ex))
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj)  # exit here
        
        # check we are going to the Internet over the correct interface
        ip_address = gethostbyname(config_vars['connectivity_lookup'])
        if not check_correct_mode_interface(ip_address, config_vars, self.file_logger):

            self.file_logger.warning("  We are not using the interface required to perform our tests due to a routing issue in this unit - attempt route addition to fix issue")
            
            if inject_default_route(config_vars['connectivity_lookup'], config_vars, self.file_logger):
            
                self.adapter_obj.bounce_wlan_interface()
                self.file_logger.info("  Checking if route injection worked...")

                if check_correct_mode_interface(ip_address, config_vars, self.file_logger):
                    self.file_logger.info("  Routing issue corrected OK.")
                else:
                    self.file_logger.warning("  We still have a routing issue. Will have to exit as testing over correct interface not possible")
                    self.file_logger.warning("  Suggest making static routing additions or adding an additional metric to the interface causing the issue.")
                    lockf_obj.delete_lock_file()
                    sys.exit()

        # Check we can get to the mgt platform (function will exit script if no connectivity)
        self.file_logger.info("Checking we can get to the management platform...")

        mgt_connection_obj = MgtConnectionTester(config_vars, self.file_logger, self.platform)
        mgt_connection_obj.check_connection(watchdog_obj, lockf_obj)

        # hold all results in one place
        results_dict = {}

        # define column headers
        column_headers = ['time', 'ssid', 'bssid', 'freq_ghz', 'channel', 'phy_rate_mbps', 'signal_level_dbm', 'tx_retries', 'ip_address', 'location']

        results_dict['time'] = int(time.time())
        results_dict['ssid'] = self.adapter_obj.get_ssid()
        results_dict['bssid'] = self.adapter_obj.get_bssid()
        results_dict['freq_ghz'] = self.adapter_obj.get_freq()
        results_dict['center_freq_ghz'] = self.adapter_obj.get_center_freq()
        results_dict['channel'] = self.adapter_obj.get_channel()
        results_dict['channel_width'] = self.adapter_obj.get_channel_width()
        results_dict['tx_rate_mbps'] = self.adapter_obj.get_tx_bit_rate()
        results_dict['rx_rate_mbps'] = self.adapter_obj.get_rx_bit_rate()
        results_dict['tx_mcs'] = self.adapter_obj.get_tx_mcs()
        results_dict['rx_mcs'] = self.adapter_obj.get_rx_mcs()
        results_dict['signal_level_dbm'] = self.adapter_obj.get_signal_level()
        results_dict['tx_retries'] = self.adapter_obj.get_tx_retries()
        results_dict['ip_address'] = self.adapter_obj.get_ipaddr()
        results_dict['location'] = config_vars['location']

        # dump out adapter info to log file
        self.file_logger.info("########## Wireless Connection ##########")
        self.file_logger.info("Wireless connection data: SSID:{}, BSSID:{}, Freq:{}, Center Freq:{}, Channel: {}, Channel Width: {}, Tx Phy rate:{}, \
            Rx Phy rate:{}, Tx MCS: {}, Rx MCS: {}, RSSI:{}, Tx retries:{}, IP address:{}".format(
            results_dict['ssid'], results_dict['bssid'], results_dict['freq_ghz'], results_dict['center_freq_ghz'], results_dict['channel'], 
            results_dict['channel_width'],  results_dict['tx_rate_mbps'], results_dict['rx_rate_mbps'], results_dict['tx_mcs'],
            results_dict['rx_mcs'], results_dict['signal_level_dbm'], results_dict['tx_retries'], results_dict['ip_address']))
        # dump the results
        data_file = config_vars['network_data_file']
        test_name = "Network Tests"
        if exporter_obj.send_results(config_vars, results_dict, column_headers, data_file, test_name, self.file_logger):
            self.file_logger.info("Connection results sent OK.")
            return True
        else:
            self.file_logger.error("Issue sending connection results. Exiting")
            lockf_obj.delete_lock_file()
            sys.exit()