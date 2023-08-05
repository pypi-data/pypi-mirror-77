"""
The classes to handle display eb passes.
"""

from rads.database.query import query_upcomming_requests
from rads.database.update import update_approve_deny
from rads.database.request_data import RequestData
from rads.command.schedule_pass import Schedule_Pass
from loguru import logger
import reverse_geocoder as rg

_DT_STR_FORMAT = "%Y/%m/%d %H:%M:%S"
_STR_FORMAT = "{:7} | {:8} | {:15} | {:^5} | {:19} | {:19} | {:30}"


class Request(RequestData):
    """
    A wrapper class ontop of request data for the ui to use.
    """
    def __init__(self, request):
        super().__init__(
            request.id,
            request.user_token,
            request.pass_id,
            request.is_approved,
            request.is_sent,
            request.created_dt,
            request.updated_dt,
            request.observation_type,
            request.pass_data.gs_latitude_deg,
            request.pass_data.gs_longitude_deg,
            request.pass_data.gs_elevation_m,
            request.pass_data.aos_utc,
            request.pass_data.los_utc
            )
        self.deny_count = 0
        self.geo = request.geo

    def __str__(self):

        obs_type = self.observation_type
        if obs_type is None:
            obs_type = " "

        if self.is_approved is True:
            ad_status = "approved"
        elif self.is_approved is False:
            ad_status = "denied"
        else:
            ad_status = "pending"

        if self._is_sent is True:
            sent_status = "Y"
        else:
            sent_status = "N"

        if self.geo is not None:
            loc = self.geo["name"] + ", " + self.geo["admin1"]
        else:
            loc = " "

        return _STR_FORMAT.format(
            self.id,
            ad_status,
            obs_type,
            sent_status,
            self.pass_data.aos_utc.strftime(_DT_STR_FORMAT),
            self.pass_data.los_utc.strftime(_DT_STR_FORMAT),
            loc
            )

    def deny(self):
        """
        Deny request.
        """
        self.deny_count += 1
        self.is_approved = False

    def undeny(self):
        """
        Undo the denied request.
        """
        if self.deny_count > 0:
            self.deny_count -= 1
            if self.deny_count == 0:
                self.is_approved = True


class RequestTable():
    """
    A list of request that approved and upcomming.
    """

    def __init__(self):
        self.data = []
        coordinates = []

        requests = query_upcomming_requests()
        for r in requests:
            self.data.append(Request(r))
            coor = (r.pass_data.gs_latitude_deg, r.pass_data.gs_longitude_deg)
            coordinates.append(coor)

        if requests:
            locations = rg.search(coordinates, verbose=False)
            for i in range(len(self.data)):
                self.data[i].geo = locations[i]

        self.data_len = len(self.data)
        self.header = _STR_FORMAT.format(
            "ID",
            "Status",
            "Type",
            "Sent",
            "AOS",
            "LOS",
            "City, State"
            )

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.data_len

    def save(self):
        """
        Save data to db and update cosmos.
        """
        update_approve_deny(self.data)
        try:
            schedule_pass = Schedule_Pass(self.data)
            schedule_pass.schedule_all()
        except Exception as e:
            logger.error("cosmos command interface failed with: {}".format(e))
