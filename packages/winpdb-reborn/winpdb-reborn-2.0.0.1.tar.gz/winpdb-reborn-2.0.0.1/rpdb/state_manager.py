import _thread as thread
import threading
import time

from rpdb.const import PING_TIMEOUT
from rpdb.events import CEventState
from rpdb.utils import safe_wait

g_alertable_waiters = {}


# TODO: remove these compatibility functions and change the code using them directly
def lock_notify_all(lock):
    return lock.notify_all()


class CStateManager:
    """
    Manage possible debugger states (broken, running, etc...)

    The state manager can receive state changes via an input event
    dispatcher or via the set_state() method

    It sends state changes forward to the output event dispatcher.

    The state can also be queried or waited for.
    """

    def __init__(self, initial_state, event_dispatcher_output = None, event_dispatcher_input = None):
        self.m_event_dispatcher_input = event_dispatcher_input
        self.m_event_dispatcher_output = event_dispatcher_output

        if self.m_event_dispatcher_input is not None:
            event_type_dict = {CEventState: {}}
            self.m_event_dispatcher_input.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

            if self.m_event_dispatcher_output is not None:
                self.m_event_dispatcher_output.register_chain_override(event_type_dict)

        self.m_state_lock = threading.Condition()

        self.m_state_queue = []
        self.m_state_index = 0
        self.m_waiter_list = {}

        self.set_state(initial_state)


    def shutdown(self):
        if self.m_event_dispatcher_input is not None:
            self.m_event_dispatcher_input.remove_callback(self.event_handler)


    def event_handler(self, event):
        self.set_state(event.m_state)


    def get_state(self):
        return self.m_state_queue[-1]


    def __add_state(self, state):
        self.m_state_queue.append(state)
        self.m_state_index += 1

        self.__remove_states()


    def __remove_states(self, treshold = None):
        """
        Clean up old state changes from the state queue.
        """

        index = self.__calc_min_index()

        if (treshold is not None) and (index <= treshold):
            return

        _delta = 1 + self.m_state_index - index

        self.m_state_queue = self.m_state_queue[-_delta:]


    def __calc_min_index(self):
        """
        Calc the minimum state index.
        The calculated index is the oldest state of which all state
        waiters are aware of. That is, no one cares for older states
        and these can be removed from the state queue.
        """

        if len(self.m_waiter_list) == 0:
            return self.m_state_index

        index_list = list(self.m_waiter_list.keys())
        min_index = min(index_list)

        return min_index


    def __add_waiter(self):
        index = self.m_state_index
        n = self.m_waiter_list.get(index, 0)
        self.m_waiter_list[index] = n + 1

        return index


    def __remove_waiter(self, index):
        n = self.m_waiter_list[index]
        if n == 1:
            del self.m_waiter_list[index]
            self.__remove_states(index)
        else:
            self.m_waiter_list[index] = n - 1


    def __get_states(self, index):
        _delta = 1 + self.m_state_index - index
        states = self.m_state_queue[-_delta:]
        return states


    def set_state(self, state = None, fLock = True):
        try:
            if fLock:
                self.m_state_lock.acquire()

            if state is None:
                state = self.get_state()

            self.__add_state(state)

            lock_notify_all(self.m_state_lock)

        finally:
            if fLock:
                self.m_state_lock.release()

        if self.m_event_dispatcher_output is not None:
            event = CEventState(state)
            self.m_event_dispatcher_output.fire_event(event)


    def wait_for_state(self, state_list):
        """
        Wait for any of the states in the state list.
        """

        try:
            self.m_state_lock.acquire()

            if self.get_state() in state_list:
                return self.get_state()

            while True:
                index = self.__add_waiter()

                alertable_wait(self.m_state_lock, PING_TIMEOUT)

                states = self.__get_states(index)
                self.__remove_waiter(index)

                for state in states:
                    if state in state_list:
                        return state

        finally:
            self.m_state_lock.release()


    def acquire(self):
        self.m_state_lock.acquire()


    def release(self):
        self.m_state_lock.release()


def alertable_wait(lock, timeout = None):
    jobs = []
    tid = thread.get_ident()
    g_alertable_waiters[tid] = (lock, jobs)

    try:
        safe_wait(lock, timeout)

        while len(jobs) != 0:
            job = jobs.pop(0)
            try:
                job()
            except:
                pass

            if len(jobs) == 0:
                time.sleep(0.1)

    finally:
        del g_alertable_waiters[tid]