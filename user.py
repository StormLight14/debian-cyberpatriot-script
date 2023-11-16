class User:
  def __init__(self, username, is_authorized, has_sudo):
    self.username = username
    self.is_authorized = is_authorized
    self.has_sudo = has_sudo
