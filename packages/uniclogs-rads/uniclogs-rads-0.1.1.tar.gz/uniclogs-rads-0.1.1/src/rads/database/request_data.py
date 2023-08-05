from datetime import datetime
from pass_calculator.orbitalpass import OrbitalPass


_DT_STR_FORMAT = "%Y/%m/%d %H:%M:%S"
_STR_FORMAT = "{:7} | {:8} | {:15} | {:19} | {:^5} | {:7} | {:19} | {:19} | {:30} | {:9.5f} | {:10.5f} | {:7.2f}"
RequestHeader = "{:>7} | {:8} | {:15} | {:19} | {:5} | {:7} | {:19} | {:19} | {:30} | {:9} | {:10} | {:7}".format(
        "ID", "Status", "Type", "Created", "Sent", "Pass ID", "AOS", "LOS", "City, State", "Latitude", "Longitude", "Elevation (m)")


class RequestData():
    _id = 0
    _user_token = ""
    _pass_id = 0
    _pass_data = None
    _is_approved = False
    _is_sent = False
    _created_dt = None
    _updated_dt = None
    _observation_type = None
    _data_updated = False

    def __init__(
            self,
            id: int,
            user_token: str,
            pass_id: int,
            is_approved: bool,
            is_sent: bool,
            created_dt: datetime,
            updated_dt: datetime,
            observation_type: str,
            latitude: float,
            longitude: float,
            elevation_m: float,
            aos: datetime,
            los: datetime
            ):
        self._id = id
        self._user_token = user_token
        self._pass_id = pass_id
        self._pass_data = OrbitalPass(
                latitude,
                longitude,
                aos,
                los,
                elevation_m
                )
        self._is_approved = is_approved
        self._is_sent = is_sent
        self._created_dt = created_dt
        self._updated_dt = updated_dt
        self._observation_type = observation_type

        # dont need to be properties
        # also are faster to handle with a list of RequestData objects
        # make sure these are differnt for every obj
        self.geo = None
        self.db_approved_overlap = []
        self.new_overlap = []

    def __str__(self):
        obs_type = self._observation_type
        if obs_type is None:  # TODO fix this
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

        loc = self.geo["name"] + ", " + self.geo["admin1"]
        return _STR_FORMAT.format(
                self._id,
                ad_status,
                obs_type,
                self._created_dt.strftime(_DT_STR_FORMAT),
                sent_status,
                self._pass_id,
                self._pass_data.aos_utc.strftime(_DT_STR_FORMAT),
                self._pass_data.los_utc.strftime(_DT_STR_FORMAT),
                loc,
                self._pass_data.gs_latitude_deg,
                self._pass_data.gs_longitude_deg,
                self._pass_data.gs_elevation_m
                )

    @property
    def id(self):
        return self._id

    @property
    def user_token(self):
        return self._user_token

    @property
    def pass_id(self):
        return self._pass_id

    @property
    def pass_data(self):
        return self._pass_data

    @property
    def is_approved(self):
        return self._is_approved

    @is_approved.setter
    def is_approved(self, value: bool):
        if self.pass_data.aos_utc > datetime.utcnow():
            self._is_approved = value
            self._data_updated = True

    @property
    def is_sent(self):
        return self._is_sent

    @property
    def created_dt(self):
        return self._created_dt

    @property
    def updated_dt(self):
        return self._updated_dt

    @property
    def observation_type(self):
        return self._observation_type

    @property
    def updated(self):
        return self._data_updated
