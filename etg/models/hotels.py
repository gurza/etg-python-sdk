# -*- coding: utf-8 -*-
class GuestData:
    def __init__(self, adults, children=None):
        """Init.

        :param adults: number of adult guests.
        :type adults: int
        :param children: (optional) age of children who will stay in the room.
        :type children: list[int] or None
        """
        self.adults = adults
        self.children = children if children is not None else []

    def to_json(self):
        return {
            'adults': self.adults,
            'children': self.children,
        }
