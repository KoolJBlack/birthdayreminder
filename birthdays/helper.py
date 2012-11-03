def is_int(s):
  """Returns true if a stirng represents an interger"""
  try:
    int(s)
    return True
  except ValueError:
    return False