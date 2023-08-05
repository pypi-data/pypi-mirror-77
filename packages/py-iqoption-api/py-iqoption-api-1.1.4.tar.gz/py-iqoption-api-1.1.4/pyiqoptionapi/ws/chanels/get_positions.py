# -*- coding: utf-8 -*-
from pyiqoptionapi.ws.chanels.base import Base


class Get_positions(Base):

    name = "sendMessage"

    def __call__(self, instrument_type):
        if instrument_type == "digital-option":
            name = "digital-options.get-positions"
        elif instrument_type == "fx-option":
            name = "trading-fx-option.get-positions"
        else:
            name = "get-positions"

        data = {
                "name": name,
                "body": {
                            "instrument_type": instrument_type,
                            "user_balance_id": int(self.api.global_value.balance_id)
                        }
                }

        self.send_websocket_request(self.name, data)


class Get_position(Base):

    name = "sendMessage"

    def __call__(self, position_id):
        data = {
                    "name": "get-position",
                    "body": {
                                "position_id": int(position_id),
                             }
        }
        self.send_websocket_request(self.name, data)


class Get_position_history(Base):

    name = "sendMessage"

    def __call__(self, instrument_type):
        data = {
                "name":"get-position-history",
                "body": {
                         "instrument_type": instrument_type,
                         "user_balance_id": int(self.api.global_value.balance_id)
                         }
        }
        self.send_websocket_request(self.name, data)


class Get_position_history_v2(Base):

    name = "sendMessage"

    def __call__(self, instrument_types, limit, offset, start=0, end=0):
        data = {
                  "name":"portfolio.get-history-positions",
                    "body":{
                            "instrument_types":[instrument_types],
                            "limit":limit,
                            "offset":offset,
                            "start":start,
                            "end":end,
                            "user_balance_id":int(self.api.global_value.balance_id)
                            }
                }
        self.send_websocket_request(self.name, data)



class Get_position_history_v3(Base):

    name = "sendMessage"

    def __call__(self, user_id, instrument_types, limit, offset, start=0, end=0):
        data = {
                  "name": "portfolio.get-history-positions",
                    "body": {
                            "instrument_types": [instrument_types],
                            "limit": limit,
                            "offset": offset,
                            "start": start,
                            "end": end,
                            "user_balance_id": int(user_id)
                            }
                }
        self.send_websocket_request(self.name, data, request_id='users_history_data')


class Get_digital_position(Base):

    name = "sendMessage"

    def __call__(self,position_id):
        data = {
                "name":"digital-options.get-position",
                "body":{
                        "position_id": int(position_id),
                        }
                }
        self.send_websocket_request(self.name, data)
