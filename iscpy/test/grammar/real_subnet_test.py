from iscpy.test.grammar.test_utils import BaseTest, make_simple, pp


class ISCRealSubnetTests(BaseTest):

    def setUp(self):
        super(ISCRealSubnetTests, self).setUp()

        self.real_grammar = self.isc_grammar + """
            S = subnet_stmt
        """
    def test_real(self):
        test_param = """
            subnet 10.0.0.0 netmask 255.255.255.0 {
                pool {
                    failover peer "dhcp-failover";
                    deny dynamic bootp clients;
                    range 10.0.0.0 10.0.0.247;
                }

                option ntp-servers         10.0.0.5;
                option subnet-mask         255.255.255.0;
                option routers             10.0.0.1;
                option domain-name-servers 10.22.75.40, 10.22.75.41;
                option domain-search       "foobar.com", "dc1.foobar.com", "foobar.org", "foobar.net";
                option domain-name         "foobar.com";
                next-server                10.0.0.5;
                filename                   "/pxelinux.0";

                if exists gpxe.bus-id {
                    site-option-space "pxelinux";

                    if exists dhcp-parameter-request-list {
                        option dhcp-parameter-request-list = concat(option dhcp-parameter-request-list,d0,d1,d2,d3);
                    }

                    option pxelinux.magic f1:00:74:7e;
                    option pxelinux.configfile "pxelinux.cfg/foobar";
                }

                host app1.metrics.scl3.mozilla.com-nic1  {
                    hardware ethernet 00:00:00:00:00:00;
                    fixed-address 10.0.0.13;
                }
                host app1.metrics.scl3.mozilla.com-nic2  {
                    hardware ethernet 00:00:00:00:00:00;
                    fixed-address 10.0.0.13;
                }
            }

        """
        # If it parses, we are probably good
        make_simple(self.real_grammar, test_param)

    def test_real1(self):
        test_param = """
            subnet 10.22.80.0 netmask 255.255.255.0 {
                    # Always send the PXELINUX options (specified in hexadecimal)
                    foo bar;

            }
        """
        # If it parses, we are probably good
        make_simple(self.real_grammar, test_param)

    def test_real2(self):
        test_param = """
##                                                                                                                                                                                                                     
## Vlan 75
##
subnet 10.22.70.0 netmask 255.255.255.0 {
    pool {
        failover peer "dhcp-failover";
        deny dynamic bootp clients;
        range 10.22.70.200 10.22.70.247;
    }

    option ntp-servers         10.22.70.5;
    option subnet-mask         255.255.255.0;
    option routers             10.22.70.1;
    option domain-name-servers 10.22.75.40, 10.22.75.41;
    option domain-search       "mozilla.com", "scl3.mozilla.com", "mozilla.org", "mozilla.net";
    option domain-name         "mozilla.com";
    next-server                10.22.75.5;
    filename                   "/pxelinux.0";

    if exists gpxe.bus-id {
        site-option-space "pxelinux";

        if exists dhcp-parameter-request-list {
            # Always send the PXELINUX options (specified in hexadecimal)
            option dhcp-parameter-request-list = concat(option dhcp-parameter-request-list,d0,d1,d2,d3);
        }

        option pxelinux.magic f1:00:74:7e;
        option pxelinux.configfile "pxelinux.cfg/seamicro";
    }

    #include "/etc/dhcpconfig-autodeploy/vlan70_generated_hosts.conf";
}

        """
        # If it parses, we are probably good
        make_simple(self.real_grammar, test_param)

    def test_real3(self):
        test_param = """subnet 10.22.70.0 netmask 255.255.255.0 {
        option domain-name         "mozilla.com";
}
    """
        make_simple(self.real_grammar, test_param)


if __name__ == '__main__':
    import unittest
    unittest.main()
