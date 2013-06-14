#!/usr/bin/env python

import sys

class Memory(object):
  def __init__(self, parent = None):
    self.parent = parent

    self.values = {}
    self.num_values = {}
    self.unset_keys = []

  def set(self, key, value):
    current_value = self.get_current_value(key)

    # Remove value counter
    if current_value:
      self.decr_counter(current_value)

    # Assign new value
    self.values[key] = value

    if key in self.unset_keys:
      self.unset_keys.pop(key)

    # Add value counter
    if value in self.num_values.keys():
      self.num_values[value] += 1
    else:
      self.num_values[value] = 1

  def get(self, key):
    return self.get_current_value(key)

  def unset(self, key):
    current_value = self.get_current_value(key)

    # Remove value counter
    self.decr_counter(current_value)

    self.unset_keys.append(key)

    if key in self.values:
      self.values.pop(key)

  def numequalto(self, value):
    return self.get_current_counter(value)

  def get_current_value(self, key):
    if key in self.unset_keys:
      return None
    if key in self.values.keys():
      return self.values[key]
    elif self.parent:
      return self.parent.get_current_value(key)
    return None

  def get_current_counter(self, value):
    if value in self.num_values.keys():
      return self.num_values[value]
    elif self.parent:
      return self.parent.get_current_counter(value)
    return 0

  def incr_counter(self, value):
    self.num_values[value] = self.get_current_counter(value) + 1

  def decr_counter(self, value):
    self.num_values[value] = self.get_current_counter(value) - 1

  def merge(self):
    for key in self.values:
      self.parent.values[key] = self.values[key]
    for key in self.num_values:
      self.parent.num_values[key] = self.num_values[key]
    for key in self.unset_keys:
      self.parent.values.pop(key)

main_memory = Memory()
current_memory = main_memory

while 1:
  cmd = raw_input()

  #print cmd

  args = cmd.split(' ')[1:]
  cmd = cmd.split(' ')[0]

  if cmd == 'END':
    break

  if cmd == 'SET' and len(args) == 2:
    current_memory.set(args[0], args[1])

  elif cmd == 'GET' and len(args) == 1:
    value = current_memory.get(args[0])

    if value:
      print value
    else:
      print 'NULL'

  elif cmd == 'UNSET' and len(args) == 1: 
    current_memory.unset(args[0])

  elif cmd == 'NUMEQUALTO' and len(args) == 1:
    print current_memory.numequalto(args[0])

  elif cmd == 'BEGIN':
    new_memory = Memory(current_memory)
    current_memory = new_memory

  elif cmd == 'ROLLBACK':
    old_memory_parent = current_memory.parent

    # Destroy current_memory
    del current_memory

    current_memory = old_memory_parent

  elif cmd == 'COMMIT':
    # Merge
    current_memory.merge()

    # Save old instance for deletion
    old_memory = current_memory

    current_memory = current_memory.parent

    del old_memory

  else:
    print "Invalid command / arguments"

