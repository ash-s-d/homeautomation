#!/usr/bin/python

"""homeautomationdatastore.py: Class implementing the object to interact with the persistent data store"""

import re

from classes.sqlitedatastore import SQLiteDataStore

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class HomeAutomationDataStore(SQLiteDataStore):

    def __init__(self, path_to_db_file):
        SQLiteDataStorage.__init__(self, path_to_db_file)

    def get_zones(self):
        result_set = self.execute_reader (   """
                                                SELECT
                                                    Zone.id as IDENTIFIER,
                                                    Zone.description as DESCRIPTION,
                                                    Zone.short_name as SHORT_NAME,
                                                    WifiBridge.id as BRIDGE_IDENTIFIER,
                                                    Camera.id as CAMERA_IDENTIFIER
                                                FROM 
                                                    Zone
                                                    LEFT OUTER JOIN WifiBridge ON WifiBridge.zone_id = Zone.id
                                                    LEFT OUTER JOIN Camera ON Camera.zone_id = Zone.id
                                                ORDER BY
                                                    Zone.short_name;
                                                """
                                             )

        return result_set

    def get_wifi_bridge_in_zone(self, zone_identifier):
        result_set = self.execute_reader (   """
                                                SELECT
                                                    WifiBridge.mac_address AS MAC_ADDRESS,
                                                    WifiBridge.ip_address AS IP_ADDRESS
                                                FROM
                                                    Zone
                                                    INNER JOIN WifiBridge ON WifiBridge.zone_id = Zone.id
                                                WHERE
                                                    Zone.id = """ + str(zone_identifier) + """;
                                                """
                                             )

        return result_set

    def update_wifi_bridges(self, bridges):
        for index, value in enumerate(bridges):
            scalar = self.execute_scalar(   """
                                            SELECT
                                                COUNT(*)
                                            FROM
                                                WifiBridge
                                            WHERE
                                                mac_address = '""" + value + """';
                                            """
                                            )

            if scalar > 0:
                self.execute_non_query (   """
                                            UPDATE
                                                WifiBridge
                                            SET
                                                ip_address = '""" + bridges[value][0] + """',
                                                name = '""" + bridges[value][1] + """'
                                            WHERE
                                                mac_address = '""" + value + """';
                                            """
                                           )
            else:
                self.execute_non_query (   """
                                            INSERT INTO
                                                WifiBridge (mac_address, ip_address, name)
                                            VALUES (
                                                        '""" + value + """', 
                                                        '""" + bridges[value][0] + """',
                                                        '""" + bridges[value][1] + """'
                                                    );
                                            """
                                           )
