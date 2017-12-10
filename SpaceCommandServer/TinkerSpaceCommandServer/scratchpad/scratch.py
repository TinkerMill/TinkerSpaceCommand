# Test attribute validations

from datetime import datetime
import pdb

class TestClass:

  def __init__(self, x):
    self.x = x

  @property
  def x(self):
    return self.__x

  @x.setter
  def x(self, x):
    if x < 0:
      raise ValueError("Timestamp must be a valid instance of DateTime")
      print('x < 0')
    else:
      self.__x = x
      print('value set')

class P:

  def __init__(self,x):
    self.x = x

  @property
  def x(self):
    return self.__x

  @x.setter
  def x(self, x):
    if x < 0:
      self.__x = 0
    elif x > 1000:
      self.__x = 1000
    else:
      self.__x = x


