#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage CheckPoint Firewall (c) 2019
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: cp_mgmt_set_https_advanced_settings
short_description: Edit HTTPS Inspection's Blades' Settings.
description:
  - Edit HTTPS Inspection's Blades' Settings.
  - All operations are performed over Web Services API.
version_added: "6.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  bypass_on_client_failure:
    description:
      - Whether all requests should be bypassed or blocked-in case of client errors (Client closes the connection due to authentication issues during
        handshake)<br>true - Fail-open (bypass all requests)<br>false - Fail-close (block all requests).
    type: bool
  bypass_on_failure:
    description:
      - Whether all requests should be bypassed or blocked-in case of server errors (for example validation error during GW-Server
        authentication)<br>true - Fail-open (bypass all requests)<br>false - Fail-close (block all requests).
    type: bool
  bypass_under_load:
    description:
      - Bypass the HTTPS Inspection temporarily to improve connectivity during a heavy load on the Security Gateway. The HTTPS Inspection would resume
        as soon as the load decreases.
    type: dict
    suboptions:
      track:
        description:
          - Whether to log and send a notification for the bypass under load,<ul style="list-style-type,square"><li>None - Does not record the
            event.</li><li>Log - Records the event details. Use SmartConsole or SmartView to see the logs.</li><li>Alert - Logs the event and executes a
            command you configured.</li><li>Mail - Sends an email to the administrator.</li><li>SNMP Trap - Sends an SNMP alert to the configured SNMP
            Management Server.</li><li>User Defined Alert - Sends a custom alert.</li></ul>.
        type: str
        choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                 'user defined alert no.3']
  site_categorization_allow_mode:
    description:
      - Whether all requests should be allowed or blocked until categorization is complete.<br>Background - in order to allow requests until
        categorization is complete.<br>Hold- in order to block requests until categorization is complete.
    type: str
    choices: ['background', 'hold']
  deny_untrusted_server_cert:
    description:
      - Set to be true in order to drop traffic from servers with untrusted server certificate.
    type: bool
  deny_revoked_server_cert:
    description:
      - Set to be true in order to drop traffic from servers with revoked server certificate (validate CRL).
    type: bool
  deny_expired_server_cert:
    description:
      - Set to be true in order to drop traffic from servers with expired server certificate.
    type: bool
  track_validation_errors:
    description:
      - Whether to log and send a notification for the server validation errors,<br><ul style="list-style-type,square"><li>None - Does not record the
        event.</li><li>Log - Records the event details in SmartView.</li><li>Alert - Logs the event and executes a command.</li><li>Mail - Sends an email to
        the administrator.</li><li>SNMP Trap - Sends an SNMP alert to the SNMP GU.</li><li>User Defined Alert - Sends customized alerts.</li></ul>.
    type: str
    choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2', 'user defined alert no.3']
  retrieve_intermediate_ca_certificates:
    description:
      - Configure the value "true" to use the "Certificate Authority Information Access" extension to retrieve certificates that are missing from the
        certificate chain.
    type: bool
  blocked_certificates:
    description:
      - Collection of certificates objects identified by serial number.<br>Drop traffic from servers using the blocked certificate.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Describes the name, cannot be overridden.
        type: str
      cert_serial_number:
        description:
          - Certificate Serial Number (unique) in hexadecimal format HH,HH.
        type: str
      comments:
        description:
          - Describes the certificate by default, can be overridden by any text.
        type: str
  blocked_certificate_tracking:
    description:
      - Controls whether to log and send a notification for dropped traffic.<br><ul style="list-style-type,square"><li>None - Does not record the
        event.</li><li>Log - Records the event details in SmartView.</li><li>Alert - Logs the event and executes a command.</li><li>Mail - Sends an email to
        the administrator.</li><li>SNMP Trap - Sends an SNMP alert to the SNMP GU.</li><li>User Defined Alert - Sends customized alerts.</li></ul>.
    type: str
    choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2', 'user defined alert no.3']
  bypass_certificate_pinned_apps:
    description:
      - Configure the value "true" to bypass traffic from certificate-pinned applications approved by Check Point.<br>HTTPS Inspection cannot inspect
        connections initiated by certificate-pinned applications.
    type: bool
  bypass_update_services:
    description:
      - Configure the value "true" to bypass traffic to well-known software update services.
    type: bool
  httpsi_statistics_logs:
    description:
      - Configure the value "true" to send logs for every TLS session for all rules in HTTPS Inspection policy.
    type: bool
  log_empty_ssl_connections:
    description:
      - Configure the value "true" to send logs about SSL connections that are closed without data or are closed in the middle of a handshake.
    type: bool
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  domains_to_process:
    description:
      - Indicates which domains to process the commands on. It cannot be used with the details-level full, must be run from the System Domain only and
        with ignore-warnings true. Valid values are, CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.
    type: list
    elements: str
  ignore_warnings:
    description:
      - Apply changes ignoring warnings.
    type: bool
  ignore_errors:
    description:
      - Apply changes ignoring errors. You won't be able to publish such a changes. If ignore-warnings flag was omitted - warnings will also be ignored.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: set-https-advanced-settings
  cp_mgmt_set_https_advanced_settings:
    blocked_certificate_tracking: popup alert
    bypass_certificate_pinned_apps: 'false'
    bypass_on_client_failure: 'false'
    bypass_on_failure: 'false'
    bypass_under_load:
     track: log
    bypass_update_services: 'true'
    deny_expired_server_cert: 'true'
    deny_revoked_server_cert: 'false'
    deny_untrusted_server_cert: 'true'
    httpsi_statistics_logs: 'true'
    log_empty_ssl_connections: 'true'
    retrieve_intermediate_ca_certificates: 'true'
    site_categorization_allow_mode: background
    track_validation_errors: snmp trap alert
"""

RETURN = """
cp_mgmt_set_https_advanced_settings:
  description: The checkpoint set-https-advanced-settings output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        bypass_on_client_failure=dict(type='bool'),
        bypass_on_failure=dict(type='bool'),
        bypass_under_load=dict(type='dict', options=dict(
            track=dict(type='str', choices=['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert',
                                            'user defined alert no.1', 'user defined alert no.2', 'user defined alert no.3'])
        )),
        site_categorization_allow_mode=dict(type='str', choices=['background', 'hold']),
        deny_untrusted_server_cert=dict(type='bool'),
        deny_revoked_server_cert=dict(type='bool'),
        deny_expired_server_cert=dict(type='bool'),
        track_validation_errors=dict(type='str', choices=['none', 'log', 'popup alert', 'mail alert',
                                                          'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2', 'user defined alert no.3']),
        retrieve_intermediate_ca_certificates=dict(type='bool'),
        blocked_certificates=dict(type='list', elements='dict', options=dict(
            name=dict(type='str'),
            cert_serial_number=dict(type='str'),
            comments=dict(type='str')
        )),
        blocked_certificate_tracking=dict(type='str', choices=['none', 'log', 'popup alert',
                                                               'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                                                               'user defined alert no.3']),
        bypass_certificate_pinned_apps=dict(type='bool'),
        bypass_update_services=dict(type='bool'),
        httpsi_statistics_logs=dict(type='bool'),
        log_empty_ssl_connections=dict(type='bool'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        domains_to_process=dict(type='list', elements='str'),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "set-https-advanced-settings"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
