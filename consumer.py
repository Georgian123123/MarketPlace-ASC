"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

QUANTITY = "quantity"
PRODUCT = "product"
TYPE = "type"
ADD = "add"
REMOVE = "remove"

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        ret_val = False
        for element in self.carts:
            id_element = self.marketplace.new_cart()

            for elem in element:
                i = 0
                while i < elem["quantity"] :
                    if elem["type"] == "add":
                        ret_val = self.marketplace.add_to_cart(id_element, elem["product"])
                    else:
                        ret_val = self.marketplace.remove_from_cart(id_element, elem["product"])

                    if ret_val:
                        i += 1
                    else:
                        time.sleep(self.retry_wait_time)

            self.marketplace.place_order(id_element)
