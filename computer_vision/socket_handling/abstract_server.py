#!/usr/bin/env python
"""abstract_server.py: Abstract class for communication server."""

from abc import (ABC, abstractmethod,)

class BasicServer(ABC):
  '''Basic server'''

  def __init__(self):
    '''Initialized server object'''

  @abstractmethod
  def start(self):
    '''start server'''

  @abstractmethod
  def stop(self):
    '''Stopping server'''

  @abstractmethod
  def send_to_all(self, message):
    '''Send message to all!'''

  @abstractmethod
  def get_next_message(self):
    '''Get next available message!'''
